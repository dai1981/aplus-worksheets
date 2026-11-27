# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 10, Science inquiry (AC9S10I01-I08): research and investigable questions, hypotheses,
risk assessment, independent and dependent variables, analysing data and gradients, correlation and causation, uncertainty,
evaluating methods, claims and secondary sources, and communicating with evidence.
  python tools/gen_au_science_y10_working_scientifically.py
Own questions on gradients, correlation strength and risk assessment, plus the AU Year 9 and Year 8 inquiry makers with new numbers.
Wrong answers come from real mistakes: reading a correlation as proof of cause, calculating a gradient as x ÷ y, and evaluating
a method by its results instead of its design.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once

YEAR, SORT = 10, 8
U, R, P, src = AU(seed_of(YEAR, SORT))

Y9 = src.mod("gen_au_science_y9_working_scientifically")
y9_unc = limit(Y9.g_unc, 6)
y9_flaw = limit(Y9.g_flaw, 8)
y9_pct = limit(Y9.g_pct, 4)
Y8 = src.mod("gen_au_science_y8_working_scientifically")
y8_claim = limit(Y8.g_claim, 6)
y8_rel = limit(Y8.g_rel, 3)

GR = [("force (N)", "extension of a spring (cm)", "cm per N"), ("time (s)", "distance travelled (m)", "m/s"),
      ("time (s)", "velocity (m/s)", "m/s²"), ("voltage (V)", "current (A)", "A per V"), ("mass (kg)", "weight (N)", "N/kg"),
      ("time (min)", "volume of gas collected (mL)", "mL/min")]


def g_grad():
    x, y, u = R.choice(GR)
    m = R.choice([0.5, 2, 3, 4, 5, 9.8] if "weight" in y else [0.5, 1.5, 2, 3, 4, 5])
    if "weight" in y:
        m = 9.8
    x1 = R.choice([1, 2, 4])
    x2 = x1 + R.choice([2, 4, 6])
    y1, y2 = m * x1, m * x2
    if not once(("gr", x, x1, x2, m)):
        return None
    f = lambda v: "%g" % round(v, 2)
    return tq("A straight-line graph of %s (y-axis) against %s (x-axis) passes through (%s, %s) and (%s, %s). What is the gradient?" %
              (y, x, f(x1), f(y1), f(x2), f(y2)), "%s %s" % (f(m), u),
              ["%s %s" % (f(1 / m), u), "%s %s" % (f(y2 - y1), u), "%s %s" % (f(y2 / x1), u)],
              "Gradient = rise ÷ run = (%s − %s) ÷ (%s − %s) = %s." % (f(y2), f(y1), f(x2), f(x1), f(m)))


CORR = [("Points rise steeply and lie close to a straight line.", "a strong positive correlation"),
        ("Points rise but are widely scattered around the line.", "a weak positive correlation"),
        ("Points fall and lie close to a straight line.", "a strong negative correlation"),
        ("Points are spread everywhere with no pattern.", "no correlation")]


def g_corr():
    ctx, kind = R.choice([("hours of sunlight and tomato yield", "pos"), ("study time and test scores", "pos"), ("car speed and stopping distance", "pos"),
                          ("fertiliser amount and plant height", "pos"), ("altitude and air temperature", "neg"), ("distance from a lamp and light reading", "neg"),
                          ("hours of screen time and hours of sleep", "neg"), ("shoe size and reaction time", "none"), ("birth month and height", "none")])
    if kind == "none":
        d, a = CORR[3]
    else:
        d, a = R.choice(CORR[:2] if kind == "pos" else CORR[2:3] + [("Points fall but are widely scattered around the line.", "a weak negative correlation")])
    if not once(("co", d, ctx)):
        return None
    opts = ["a strong positive correlation", "a weak positive correlation", "a strong negative correlation", "a weak negative correlation", "no correlation"]
    return tq("A scatter graph of %s: %s How would you describe it?" % (ctx, d), a, R.sample([o for o in opts if o != a], 3),
              "Direction (positive/negative) and how close the points are to a line (strong/weak).")


RISK = [("heating a liquid with a Bunsen burner", "burns from hot glassware or flame", "use a heatproof mat, tongs and tie hair back"),
        ("using dilute hydrochloric acid", "acid splashing in the eyes", "wear safety glasses and wipe up spills"),
        ("using a scalpel to dissect a flower", "cuts", "cut away from your body on a board"),
        ("connecting a circuit to a power pack", "electric shock or hot wires", "use low voltage and switch off before changing wires"),
        ("collecting water samples from a creek", "slipping or falling into the water", "stay on firm ground and work with a partner"),
        ("culturing bacteria on agar plates", "growing harmful microbes", "seal the plates and do not open them after incubation"),
        ("dropping masses from a height", "masses falling on feet", "use a sand tray and keep feet clear"),
        ("observing the Sun", "eye damage", "never look directly at the Sun; use a pinhole projector")]


def g_risk():
    act, haz, ctl = R.choice(RISK)
    k = R.choice(["haz", "ctl"])
    if not once(("rk", act, k)):
        return None
    if k == "haz":
        return tq("In a risk assessment for %s, what is the main hazard?" % act, haz, R.sample([x[1] for x in RISK if x[1] != haz], 3),
                  "A risk assessment lists each hazard and how to control it.")
    return tq("In a risk assessment for %s, which is the best control?" % act, ctl, R.sample([x[2] for x in RISK if x[2] != ctl], 3),
              "The hazard is %s." % haz)


POOL1 = pool(R, [
    ("What is a research question?", "a focused question that can be answered by collecting and analysing data", ["any question about science", "a conclusion", "a list of equipment"], "Example: How does temperature affect the rate of enzyme activity?"),
    ("What is the difference between primary and secondary data?", "Primary data you collect yourself; secondary data comes from other sources.", ["They are the same.", "Secondary data is always wrong.", "Primary data comes from websites."], "Both can be used to support a conclusion."),
    ("Why is a correlation not enough to prove that one variable causes another?", "A third factor might cause both, or the link could be chance.", ["Correlations are always causes.", "Graphs cannot show correlations.", "Causes never show correlations."], "Controlled experiments test cause."),
    ("What does a line of best fit show?", "the overall trend in the data", ["every point exactly", "only the first and last points", "the uncertainty"], "Points may be above and below the line."),
    ("What makes data reliable?", "repeated measurements that give similar results", ["one very careful measurement", "results that match the hypothesis", "using a new ruler"], "Repeatability builds confidence."),
    ("What is accuracy?", "how close a measurement is to the true value", ["how close repeats are to each other", "the number of decimal places", "the size of the sample"], "Precision is how close repeats are."),
    ("What is the purpose of a risk assessment?", "to identify hazards and plan controls before an investigation", ["to predict the results", "to choose the graph", "to write the conclusion"], "It keeps everyone safe."),
    ("Why should a scientific report include limitations?", "so readers know how reliable the conclusion is and how it could be improved", ["to make the report longer", "to hide errors", "because results are always wrong"], "Honest evaluation is part of science."),
    ("What does peer review do?", "experts check research for errors before it is published", ["friends vote on results", "a computer marks the work", "it proves the hypothesis"], "It increases trust in findings."),
    ("Why do CSIRO and BoM scientists use data from many weather stations?", "to reduce the effect of errors at any one station and show true trends", ["to make graphs colourful", "because one station is enough", "to change the data"], "Large data sets give more reliable conclusions."),
])
POOL5 = pool(R, [
    ("Mia writes: 'If light intensity increases, the rate of photosynthesis in pondweed will increase, because light provides energy.' What is the independent variable?", "light intensity", ["rate of photosynthesis", "the type of pondweed", "the temperature"], "It is the variable she changes."),
    ("Jack measures bubbles from pondweed at 10, 20, 30 and 40 cm from a lamp. Which variable must he control?", "the temperature of the water", ["the distance", "the number of bubbles", "nothing"], "A lamp also heats the water; use a heat screen."),
    ("Ruby's graph of rate against temperature rises to 37 °C and then falls. How should she describe it?", "The rate increases up to an optimum of about 37 °C, then decreases.", ["The rate always increases.", "There is no pattern.", "The rate is fastest at 0 °C."], "Enzymes denature at high temperatures."),
    ("Kai finds a news article claiming a supplement improves memory, based on a study of 8 people with no control group. How should he evaluate it?", "The evidence is weak: small sample and no control.", ["It is strong evidence.", "Eight people is plenty.", "Control groups are not needed."], "Look for large, controlled, peer-reviewed studies."),
    ("Ella's two sets of results have the same mean, but set A has a range of 0.2 s and set B a range of 1.5 s. Which set is more precise?", "set A", ["set B", "they are equally precise", "neither"], "A smaller range means more precise data."),
    ("Noah wants to know whether a creek is polluted. Which is the best method?", "sample water at several sites over several weeks and test it", ["test one cup of water once", "ask people if the creek looks dirty", "guess from a photo"], "More samples give more reliable conclusions."),
    ("Zara's experiment did not support her hypothesis. What should she write?", "that the data did not support it, with possible reasons and improvements", ["that the hypothesis was proven anyway", "nothing", "change the results"], "Science reports results honestly."),
    ("Liam uses a motion sensor instead of a stopwatch to measure a falling ball. How does this change the uncertainty?", "It reduces the uncertainty in the time measurements.", ["It increases uncertainty.", "It makes no difference.", "It removes the need to repeat."], "Better equipment improves precision."),
])


def main():
    sets = U.sets([
        ("Questions, hypotheses and risk", [(POOL1, 5), (g_risk, 8), (POOL5, 4), (y9_flaw, 3)]),
        ("Analysing data", [(g_grad, 8), (y9_unc, 5), (y9_pct, 4), (y8_rel, 3)]),
        ("Correlation and cause", [(g_corr, 8), (y8_claim, 4), (POOL1, 4), (POOL5, 2), (g_grad, 2)]),
        ("Evaluating methods", [(y9_flaw, 5), (g_risk, 4), (POOL5, 3), (y9_unc, 1), (POOL1, 1), (g_grad, 3), (g_corr, 3)]),
        ("Evaluating claims and communicating", [(y8_claim, 2), (POOL5, 3), (y9_flaw, 1), (g_corr, 4), (g_grad, 4), (g_risk, 4), (y9_pct, 2)]),
    ])
    make_au(YEAR, "working-scientifically", SORT, "AC9S10I01, AC9S10I02, AC9S10I03, AC9S10I04, AC9S10I05, AC9S10I06, AC9S10I07, AC9S10I08", "Science inquiry",
            "Develop investigable and research questions and testable hypotheses; plan safe, ethical investigations with risk "
            "assessments; analyse primary and secondary data including gradients, correlations and uncertainty; evaluate methods, "
            "claims and sources; and communicate evidence-based conclusions (summary of the Australian Curriculum v9.0 Year 10 science inquiry content descriptions).",
            "Working Scientifically", "Working scientifically",
            "Free Year 10 science worksheets on working scientifically: research questions, hypotheses, risk assessments, gradients, "
            "correlation and cause, uncertainty, evaluating methods and claims. 100 questions with answers.",
            "Gradient = rise ÷ run.", "Analyse trends with gradients and correlations, and evaluate the method before trusting the conclusion.",
            "<p><b>Senior science depends on careful analysis and honest evaluation.</b></p><ul>"
            "<li>Plan: a research question, a testable hypothesis, variables and a risk assessment with controls for each hazard.</li>"
            "<li>Analyse: gradient = rise ÷ run (with units); describe correlations by direction and strength; report uncertainty.</li>"
            "<li>Evaluate: sample size, controls, bias, sources of error and whether a correlation could have another cause.</li></ul>",
            [("Line through (2, 6) and (6, 18). Gradient?", ["rise 18 − 6 = 12", "run 6 − 2 = 4", "12 ÷ 4"], "3"),
             ("Ice-cream sales and sunburn both rise. Cause?", ["both rise in sunny weather"], "correlation, not cause")],
            ["Treating a correlation as proof of cause.", "Calculating a gradient as run ÷ rise.",
             "Judging a method by whether the results matched the prediction rather than by its design."],
            [("How do I calculate the gradient of a graph?", "Choose two points far apart on the line of best fit. Gradient = (change in y) ÷ (change in x), with units of y-units per x-unit."),
             ("What is a risk assessment?", "A table that lists each hazard in an investigation, the risk it causes and the control used to reduce it, such as safety glasses for acids."),
             ("How do I evaluate an investigation?", "Check whether variables were controlled, samples were large enough, measurements were precise and accurate, and whether the conclusion goes beyond the evidence.")],
            sets)


if __name__ == "__main__":
    main()
