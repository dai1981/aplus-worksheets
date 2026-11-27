# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 9, Science inquiry (AC9S9I01-I08): investigable questions and hypotheses, planning
valid and safe methods, ethics, processing data (means, ranges, uncertainty, rates and percentage change), evaluating sources
and methods, and communicating conclusions.
  python tools/gen_au_science_y9_working_scientifically.py
Own data questions (mean and uncertainty, rate from a table, percentage change), plus the AU Year 8 inquiry makers
(relationships, interpolation, claims) and the AU Year 7 inquiry makers with new numbers.
Wrong answers come from real mistakes: treating the range as the mean, calling a conclusion "proven" from one trial, and
trusting a source because it is popular rather than peer reviewed.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once

YEAR, SORT = 9, 8
U, R, P, src = AU(seed_of(YEAR, SORT))

Y8 = src.mod("gen_au_science_y8_working_scientifically")
y8_rel = limit(Y8.g_rel, 6)
y8_interp = limit(Y8.g_interp, 5)
y8_extra = limit(Y8.g_extra, 3)
Y7 = src.mod("gen_au_science_y7_working_scientifically")
y7_mean = limit(Y7.g_mean, 4)

CTX = [("time for a trolley to roll down a ramp", "s", 2.0, 4.0, 0.1), ("temperature rise of 100 mL of water heated for 1 minute", "°C", 8.0, 20.0, 0.5),
       ("length of a spring with a 200 g mass", "cm", 12.0, 20.0, 0.1), ("time for 10 swings of a pendulum", "s", 12.0, 20.0, 0.1),
       ("height of a bean seedling after 7 days", "cm", 4.0, 9.0, 0.1), ("volume of gas made in 1 minute", "mL", 20.0, 40.0, 1.0)]


def f1(v, step):
    return ("%.1f" % v) if step < 1 else ("%d" % round(v))


def g_unc():
    what, u, lo, hi, step = R.choice(CTX)
    n = round(R.uniform(lo, hi) / step) * step
    d = R.choice([1, 2, 3]) * step
    xs = [n - d, n, n + d, n]
    R.shuffle(xs)
    k = R.choice(["mean", "range", "unc"])
    if not once(("unc", what, round(n, 2), round(d, 2), k)):
        return None
    f = lambda v: "%s %s" % (f1(v, step), u)
    data = ", ".join(f(x) for x in xs)
    if k == "mean":
        return tq("A group repeated a test of the %s four times: %s. What is the mean?" % (what, data), f(n),
                  [f(2 * d), f(n + d), f(sum(xs))], "Add the results and divide by 4: %s ÷ 4 = %s." % (f1(sum(xs), step), f(n)))
    if k == "range":
        return tq("A group repeated a test of the %s four times: %s. What is the range of the results?" % (what, data), f(2 * d),
                  [f(n), f(d), f(n + d)], "Range = largest − smallest = %s − %s = %s." % (f1(n + d, step), f1(n - d, step), f(2 * d)))
    return tq("A group repeated a test of the %s four times: %s. How should the mean be reported with its uncertainty (half the range)?" % (what, data),
              "%s ± %s %s" % (f1(n, step), f1(d, step), u), ["%s ± %s %s" % (f1(n, step), f1(2 * d, step), u), "%s ± 0 %s" % (f1(n, step), u),
                                                               "%s ± %s %s" % (f1(2 * d, step), f1(d, step), u)],
              "Mean %s; half the range is %s ÷ 2 = %s." % (f1(n, step), f1(2 * d, step), f1(d, step)))


RATE = [("Volume of gas collected", "mL", "s", [5, 10, 20]), ("Distance travelled by a trolley", "cm", "s", [10, 20, 40]),
        ("Mass lost by a flask", "g", "min", [0.5, 1, 2]), ("Height of a seedling", "mm", "day", [2, 3, 5])]


def g_rate():
    what, u, tu, opts = R.choice(RATE)
    r = R.choice(opts)
    t0 = R.choice([1, 2, 5])
    ts = [0, t0, 2 * t0, 3 * t0, 4 * t0]
    k = R.choice([1, 2, 3, 4])
    if not once(("rate", what, r, t0, k)):
        return None
    tab = "<table class='sn-table'><tr><th>Time (%s)</th>%s</tr><tr><th>%s (%s)</th>%s</tr></table>" % (
        tu, "".join("<td>%g</td>" % t for t in ts), what, u, "".join("<td>%g</td>" % (r * t) for t in ts))
    per = "%g %s per %s" % (r, u, tu)
    return tq("%sThe %s increases at a steady rate. What is the rate?" % (tab, what.lower()), per,
              ["%g %s per %s" % (r * ts[k], u, tu), "%g %s per %s" % (r * t0, u, tu) if t0 != 1 else "%g %s per %s" % (r * 2, u, tu),
               "%g %s per %s" % (round(1 / r, 2), u, tu) if r != 1 else "%g %s per %s" % (r + 1, u, tu)],
              "Rate = change in %s ÷ change in time = %g ÷ %g = %g %s per %s." % (what.lower(), r * ts[k], ts[k], r, u, tu))


def g_pct():
    a = R.choice([20, 25, 40, 50, 80, 120, 200, 250])
    p = R.choice([10, 20, 25, 50, 75])
    up = R.random() < 0.5
    b = a + a * p // 100 if up else a - a * p // 100
    what = R.choice(["mass of a plant over two weeks", "height of a seedling", "number of yeast cells"] if up else
                    ["number of bacteria colonies after adding antiseptic", "count rate of a radioactive source", "temperature of a cooling cup of water"])
    if a * p % 100 or not once(("pct", a, p, up, what)):
        return None
    u = {"mass of a plant over two weeks": " g", "height of a seedling": " mm", "count rate of a radioactive source": " counts per minute",
         "temperature of a cooling cup of water": " °C"}.get(what, "")
    if "temperature" in what and a > 90:
        return None
    return tq("In an experiment, the %s changed from %d%s to %d%s. What is the percentage %s?" % (what, a, u, b, u, "increase" if up else "decrease"),
              "%d%%" % p, ["%d%%" % abs(b - a), "%d%%" % (100 - p), "%d%%" % round(abs(b - a) * 100 / b) if round(abs(b - a) * 100 / b) != p else "%d%%" % (p * 2)],
              "Percentage change = change ÷ original × 100 = %d ÷ %d × 100 = %d%%." % (abs(b - a), a, p))


POOL1 = pool(R, [
    ("Which source is most reliable for a science report?", "a peer-reviewed journal article", ["a social media post", "an advertisement", "a blog with no author"], "Peer review means other experts checked it."),
    ("Why do scientists use a control group?", "to compare against the group that gets the treatment", ["to make the test longer", "to change two variables", "so the results always match the hypothesis"], "Differences can then be linked to the variable."),
    ("What makes an experiment valid?", "it tests what it is meant to test, with all other variables controlled", ["it has many decimal places", "the results match the prediction", "it is quick"], "Validity is about a fair design."),
    ("What does 'reproducible' mean?", "other scientists get the same results when they repeat the method", ["the result is surprising", "the data is secret", "only one trial was done"], "Clear methods make results reproducible."),
    ("Why is it unethical to test a new medicine on people without telling them?", "People must give informed consent before taking part.", ["It is too expensive.", "Medicines never need testing.", "It makes the results less accurate only."], "Ethics protect participants."),
    ("Why do some Australian studies of animals need approval from an animal ethics committee?", "to make sure animals are treated humanely and only used when needed", ["to make the study faster", "to choose the graph", "because animals cannot be studied"], "The 3Rs: replace, reduce, refine."),
    ("What is a random error?", "an unpredictable error that makes repeated readings vary", ["an error that is the same every time", "a mistake in the conclusion", "a planned change"], "Repeating and averaging reduces random error."),
    ("What is a systematic error?", "an error that shifts all readings by the same amount", ["an unpredictable error", "an anomaly only", "a calculation shortcut"], "Calibrating equipment removes systematic error."),
    ("A conclusion should do what?", "answer the question and say whether the data supports the hypothesis", ["repeat the method", "list the equipment", "give an opinion with no data"], "Use evidence from the results."),
    ("Why do scientists report uncertainty, such as 4.2 ± 0.1 s?", "to show how much the results could vary", ["to make results look bigger", "because the answer is wrong", "it is not needed"], "Smaller uncertainty means more precise data."),
    ("Why should graphs have the independent variable on the x-axis?", "it is the convention, so the graph shows how the dependent variable changes with it", ["to make it look nicer", "because it is always time", "so the line goes down"], "The dependent variable goes on the y-axis."),
    ("What is the best way to show the relationship between two continuous variables?", "a scatter graph or line graph", ["a pie chart", "a column graph of categories", "a table only"], "Draw a line of best fit."),
])
POOL5 = pool(R, [
    ("Mia's hypothesis: 'If the temperature increases, enzymes in pineapple will break down gelatine faster, up to a point.' Why is this a good hypothesis?", "It is testable and names the variables and a reason.", ["It cannot be tested.", "It has no variables.", "It is a conclusion."], "Good hypotheses can be tested."),
    ("Jack tests five sunscreens on UV beads. Which control would improve his method?", "beads with no sunscreen in the same sunlight", ["beads in the dark only", "a different kind of bead for each", "no beads"], "A control shows the effect without sunscreen."),
    ("Ruby's data have a large range between trials. What should she do?", "repeat the trials and look for sources of random error", ["report only her favourite result", "change the variable", "delete the data"], "A large range means low precision."),
    ("Kai reads a news story that says a new food 'cures' colds. What should he check first?", "whether the claim is based on peer-reviewed research with a large sample", ["how many likes it got", "whether the article has pictures", "whether it is new"], "Good evidence comes from controlled studies."),
    ("Ella's line of best fit goes through most points, but one point is far away. What should she do?", "check that point for a mistake and repeat it", ["move the line to the point", "remove all points", "draw a new axis"], "It may be an anomaly."),
    ("Noah measures plant growth in 3 pots for each fertiliser. Why is 3 better than 1?", "The mean of several plants is more reliable than one plant.", ["One plant is always enough.", "It makes the test shorter.", "It changes the variable."], "More samples reduce the effect of chance."),
    ("Zara's results support her hypothesis. Can she say it is proven?", "No, the data support it, but more testing could change our understanding.", ["Yes, forever.", "Only if her friends agree.", "Yes, if the graph is neat."], "Science is open to new evidence."),
    ("Liam uses a data logger to record the temperature every second. What is the main advantage?", "more frequent and precise readings without reaction-time error", ["it changes the independent variable", "it makes the hypothesis true", "no advantage"], "Technology improves data collection."),
])


FLAWS = [
    ("A student tests whether music helps plants grow. She puts the music plants by a sunny window and the others in a dark cupboard.", "Light was not controlled, so the music may not be the cause.", "Control light, water and soil for both groups."),
    ("A group times a ball rolling down a ramp once for each height.", "One trial per height is not reliable; random errors are not reduced.", "Repeat each height several times and find the mean."),
    ("A student measures the temperature of water by reading the thermometer from above at an angle.", "Parallax error can make every reading wrong.", "Read the scale at eye level."),
    ("A company tests its own sports drink on 5 of its sponsored athletes and says it improves performance.", "The sample is tiny and the test may be biased.", "Use a large, independent, blind trial with a control group."),
    ("A student uses a balance that reads 0.5 g with nothing on it.", "There is a systematic (zero) error in every reading.", "Zero (tare) the balance before measuring."),
    ("A class tests five fertilisers but uses different amounts of water for each pot.", "Water is an uncontrolled variable.", "Give every pot the same amount of water."),
    ("A survey asks only students at one surf club about their favourite sport.", "The sample is not representative of all students.", "Survey a random sample from many schools."),
    ("A student draws a conclusion that one antacid is best after testing each antacid once.", "The conclusion is not supported by enough data.", "Repeat the test and compare means."),
    ("A student times 1 swing of a pendulum with a stopwatch.", "Reaction time is large compared with one short swing.", "Time 10 swings and divide by 10."),
    ("A group reports that bean plants grew 5.23847 cm.", "The result has more decimal places than the ruler can measure.", "Record to the precision of the ruler, such as 5.2 cm."),
    ("A student heats water in beakers of different sizes to test which stove heats fastest.", "The beaker size and amount of water were not controlled.", "Use the same beaker and volume of water."),
    ("A student leaves out an unusual result without checking it.", "An anomaly may be a real result or a mistake; it should be checked.", "Repeat the trial to see if the result happens again."),
]
FW = ["The method is perfect.", "The results should be changed to match the prediction.", "There were too many controlled variables.",
      "The student should use a different hypothesis after the test."]


def g_flaw():
    a, b, c = R.choice(FLAWS)
    k = R.choice(["what", "fix"])
    if not once(("fl", a, k)):
        return None
    if k == "what":
        return tq("%s What is the main problem with this method?" % a, b, R.sample(FW, 3), c)
    fixes = [x[2] for x in FLAWS if x[2] != c]
    return tq("%s Which change would best improve the investigation?" % a, c, R.sample(fixes, 3), b)


def main():
    sets = U.sets([
        ("Questions, hypotheses and ethics", [(POOL1, 6), (POOL5, 4), (y8_rel, 2), (g_pct, 4), (g_unc, 4)]),
        ("Processing data", [(g_unc, 10), (y7_mean, 3), (g_pct, 4), (POOL1, 3)]),
        ("Rates and relationships", [(g_rate, 8), (y8_rel, 4), (y8_interp, 5), (y8_extra, 3)]),
        ("Errors, uncertainty and validity", [(POOL1, 3), (g_unc, 4), (g_flaw, 8), (g_pct, 3), (g_rate, 2)]),
        ("Evaluating and communicating", [(g_flaw, 10), (POOL5, 4), (POOL1, 3), (g_pct, 2), (y8_interp, 1)]),
    ])
    make_au(YEAR, "working-scientifically", SORT, "AC9S9I01, AC9S9I02, AC9S9I03, AC9S9I04, AC9S9I05, AC9S9I06, AC9S9I07, AC9S9I08", "Science inquiry",
            "Develop investigable questions and hypotheses; plan and conduct safe, ethical and valid investigations; process data "
            "using means, ranges, rates and percentage change; analyse uncertainty and errors; evaluate sources, claims and methods; "
            "and communicate evidence-based conclusions (summary of the Australian Curriculum v9.0 Year 9 science inquiry content descriptions).",
            "Working Scientifically", "Working scientifically",
            "Free Year 9 science worksheets on working scientifically: hypotheses, control groups, ethics, means and uncertainty, "
            "rates from data, percentage change, errors and evaluating sources. 100 questions with answers.",
            "Report the mean with its uncertainty.", "Repeat trials, calculate a mean and report uncertainty as half the range.",
            "<p><b>Good investigations are valid, reliable and ethical.</b></p><ul>"
            "<li>A testable hypothesis names the variables and gives a reason. A control group allows a fair comparison.</li>"
            "<li>Process data: mean, range, uncertainty (± half the range), rate = change ÷ time, percentage change = change ÷ original × 100.</li>"
            "<li>Evaluate: random and systematic errors, sample size, bias, peer review and whether the data really supports the conclusion.</li></ul>",
            [("Results 3.1, 3.3, 3.2, 3.2 s. Mean ± uncertainty?", ["mean 3.2", "range 0.2, half is 0.1"], "3.2 ± 0.1 s"),
             ("Seedlings 40 → 50. Percentage increase?", ["10 ÷ 40 × 100"], "25%")],
            ["Using the range or the total instead of the mean.", "Saying one experiment 'proves' a hypothesis.",
             "Trusting a source because it is popular rather than peer reviewed."],
            [("How do I calculate uncertainty?", "Find the range of the repeated results (largest − smallest) and halve it. Report the mean ± this value, such as 4.2 ± 0.1 s."),
             ("What is the difference between random and systematic errors?", "Random errors make readings vary unpredictably; repeating and averaging helps. Systematic errors shift every reading the same way; calibrating equipment fixes them."),
             ("Why does ethics matter in science?", "Investigations must protect people, animals and the environment. People must give informed consent, and animal studies need ethics approval.")],
            sets)


if __name__ == "__main__":
    main()
