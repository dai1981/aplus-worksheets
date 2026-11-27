# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 3, Science inquiry (AC9S3I01-I06): asking questions, predicting, safe fair tests,
observing and measuring with simple tools, recording in tables and simple graphs, and sharing what was found.
  python tools/gen_au_science_y3_working_scientifically.py
Own Year 3 questions plus makers from the AU Year 4-6 inquiry units (reading a ruler and thermometer, testable questions,
equipment, choosing a graph, observations) and the UK Year 5 working scientifically banks.
Wrong answers come from real mistakes: changing more than one thing, not repeating, and guessing instead of measuring.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 3, 6
U, R, P, src = AU(seed_of(YEAR, SORT))

y4_scale = src.mod("gen_au_science_y4_working_scientifically").g_scale
y5_test = src.mod("gen_au_science_y5_working_scientifically").g_test
y5_eq = src.mod("gen_au_science_y5_working_scientifically").g_eq
y6_type = src.mod("gen_au_science_y6_working_scientifically").g_type
y6_obs = src.mod("gen_au_science_y6_working_scientifically").g_obs
uk5_b1 = src.B("gen_uk_science_y5_working_scientifically", "B1")


BIRDS = ["magpies", "galahs", "rosellas", "kookaburras", "lorikeets", "willie wagtails", "crows", "ibises"]


def g_tally():
    from au_sci import once
    bs = R.sample(BIRDS, 4)
    ns = R.sample(range(2, 14), 4)
    k = R.choice(["most", "least", "count", "total"])
    if not once(("tally", k, tuple(bs))):
        return None
    tab = "<table class='sn-table'><tr><th>Bird</th><th>Tally</th></tr>%s</table>" % "".join(
        "<tr><td>%s</td><td style='font-family:monospace'>%s</td></tr>" % (b, "||||/ " * (n // 5) + "|" * (n % 5)) for b, n in zip(bs, ns))
    tab = tab.replace("||||/", "<s>||||</s>")
    if k == "most":
        a = bs[ns.index(max(ns))]
        return tq("%sA class counted birds in the school yard. Which bird did they see most often?" % tab, a, [b for b in bs if b != a], "Count the tally marks; each crossed group is 5.")
    if k == "least":
        a = bs[ns.index(min(ns))]
        return tq("%sA class counted birds in the school yard. Which bird did they see least often?" % tab, a, [b for b in bs if b != a], "Count the tally marks; each crossed group is 5.")
    if k == "count":
        i = R.randrange(4)
        return tq("%sA class counted birds in the school yard. How many %s did they see?" % (tab, bs[i]), str(ns[i]),
                  [str(x) for x in sorted({ns[i] + 1, ns[i] - 1, ns[i] + 5, ns[i] - 5} - {ns[i]}) if x > 0][:3], "Each crossed group of tally marks is 5.")
    t = sum(ns)
    return tq("%sA class counted birds in the school yard. How many birds did they see altogether?" % tab, str(t), [str(t + 1), str(t - 2), str(t + 5)], "Add up all the counts.")


POOL1 = pool(R, [
    ("What do scientists do first in an investigation?", "ask a question they can test", ["write the conclusion", "draw a graph", "clean up"], "A good question leads to a fair test."),
    ("Which sense would you use to find out if a surface is rough or smooth?", "touch", ["hearing", "taste", "smell"], "Never taste things in a science test unless an adult says it is safe."),
    ("Why should you never taste things in a science investigation?", "Some substances can make you sick.", ["Tasting is too slow.", "Tasting changes the result.", "Tasting is not a sense."], "Stay safe."),
    ("Which is a measurement, not a guess?", "The plant is 12 cm tall.", ["The plant is quite tall.", "The plant looks big.", "I think it is tall."], "Measurements use numbers and units."),
    ("Why do we use the same cup for each test?", "so the test is fair", ["so we can drink from it", "because cups are cheap", "to change the result"], "Keep everything the same except what you are testing."),
    ("Which tool helps you see tiny things such as insect legs?", "a magnifying glass", ["a ruler", "a thermometer", "scales"], "It makes things look bigger."),
    ("How do you show your results so others can understand them?", "in a table or a simple graph", ["by keeping them secret", "by guessing", "by drawing only the equipment"], "Tables and graphs make results clear."),
    ("What is a prediction?", "what you think will happen, and why", ["what happened", "the equipment list", "a measurement"], "Make it before the test."),
    ("Why do we repeat a test?", "to check that the result is the same again", ["to make it take longer", "to change the question", "to use more equipment"], "Repeats make results more trustworthy."),
    ("What should you do after an investigation?", "clean up safely and wash your hands", ["leave the equipment out", "taste the results", "run around the room"], "Safety includes cleaning up."),
])
POOL5 = pool(R, [
    ("Mia drops a ball onto grass, concrete and sand from 1 m. Bounce heights: 30 cm, 60 cm, 5 cm. Which surface gave the highest bounce?", "concrete", ["grass", "sand", "they were the same"], "60 cm is the highest."),
    ("In Mia's test, what should she keep the same?", "the ball and the drop height", ["the surface", "nothing", "the bounce height"], "Only the surface should change."),
    ("Jack wants to know which paper plane flies furthest. What should he measure?", "how far each plane flies", ["the colour of each plane", "how long it took to fold", "the weather tomorrow"], "Measure the result."),
    ("Ruby says her seeds grew because she sang to them. How could she test this fairly?", "grow two sets of seeds the same way and sing to only one set", ["sing louder", "grow only one set", "change the soil for one set as well"], "Change one thing only."),
    ("Kai's results do not match his prediction. What should he do?", "say what really happened", ["change the results", "throw them away", "make a new prediction and pretend"], "Honest results are part of science."),
    ("Ella's group shares their results. Another group got different results. What is the best next step?", "compare how each group did the test and try again", ["decide who is right by voting", "ignore the other group", "stop the investigation"], "Scientists check each other's work."),
])


def main():
    sets = U.sets([
        ("Asking and predicting", [(POOL1, 6), (y5_test, 8), (y6_obs, 3), (uk5_b1, 3)]),
        ("Fair tests and safety", [(POOL5, 6), (POOL1, 4), (y5_test, 4), (uk5_b1, 3), (y6_obs, 3)]),
        ("Measuring", [(y4_scale, 10), (y5_eq, 8), (POOL1, 0), (y6_obs, 2)]),
        ("Tables and graphs", [(g_tally, 10), (y6_type, 7), (y5_eq, 3)]),
        ("Sharing results", [(g_tally, 4), (y4_scale, 6), (y6_type, 3), (y6_obs, 4), (y5_eq, 3)]),
    ])
    make_au(YEAR, "working-scientifically", SORT, "AC9S3I01, AC9S3I02, AC9S3I03, AC9S3I04, AC9S3I05, AC9S3I06", "Science inquiry",
            "Pose questions and make predictions; plan and conduct safe, fair investigations; observe and measure with simple equipment; "
            "record data in tables and simple graphs; identify patterns; and share findings (summary of the Australian Curriculum v9.0 Year 3 science inquiry content descriptions).",
            "Working Scientifically", "Working scientifically",
            "Free Year 3 science worksheets on working scientifically: questions and predictions, fair and safe tests, measuring with a ruler "
            "and thermometer, tally tables and graphs, and sharing results. 100 questions with answers.",
            "Ask, predict, test fairly, measure.", "A fair test changes one thing; measuring with tools beats guessing.",
            "<p><b>Scientists find out by asking questions and testing them fairly.</b></p><ul>"
            "<li>Ask a question you can test and make a prediction.</li>"
            "<li>Change one thing, keep everything else the same, and stay safe.</li>"
            "<li>Measure with tools, record in a table or tally, and share what you found, even if it surprised you.</li></ul>",
            [("Ball on grass 30 cm, concrete 60 cm. Highest bounce?", ["compare the numbers"], "concrete"),
             ("Tally: ||||/ ||. How many?", ["a crossed group is 5", "5 + 2"], "7")],
            ["Changing more than one thing at a time.", "Guessing instead of measuring.", "Changing results so they match the prediction."],
            [("What is a fair test?", "A fair test changes only one thing and keeps everything else the same."),
             ("How do tally marks work?", "Each stroke is one. The fifth stroke crosses the first four, so each crossed group is 5."),
             ("Why should results be honest?", "Science is about finding out what really happens. Surprising results help us learn.")],
            sets, allow=("meter",))


if __name__ == "__main__":
    main()
