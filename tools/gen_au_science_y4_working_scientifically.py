# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 4, Science inquiry (AC9S4I01-I06): questions and predictions, fair tests, safe and
accurate measuring, tables and column graphs, patterns and simple conclusions.
  python tools/gen_au_science_y4_working_scientifically.py
Own Year 4 questions plus question makers from the AU Year 5 and 6 inquiry units (testable questions, equipment and units,
choosing a graph, observations and explanations) and the UK Year 5 working scientifically banks.
Wrong answers come from real mistakes: changing more than one thing, reading the wrong mark on a scale, forgetting units.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 4, 7
U, R, P, src = AU(seed_of(YEAR, SORT))

Y5 = "gen_au_science_y5_working_scientifically"
Y6 = "gen_au_science_y6_working_scientifically"
y5_test = src.mod(Y5).g_test
y5_eq = src.mod(Y5).g_eq
y6_type = src.mod(Y6).g_type
y6_obs = src.mod(Y6).g_obs
uk5_b1 = src.B("gen_uk_science_y5_working_scientifically", "B1")
uk5_b5 = src.B("gen_uk_science_y5_working_scientifically", "B5")


def scale(kind):
    if kind == "ruler":
        v = R.randint(3, 14)
        x = 10 + v * 24
        ticks = "".join("<line x1='%d' y1='40' x2='%d' y2='%d' stroke='#333'/><text x='%d' y='68' font-size='11' text-anchor='middle'>%d</text>" %
                        (10 + i * 24, 10 + i * 24, 58, 10 + i * 24, i) for i in range(16))
        return v, "cm", ("<svg viewBox='0 0 400 80' width='400' role='img' aria-label='ruler measuring a pencil'><rect x='10' y='14' width='%d' height='18' rx='4' fill='#f5c542' stroke='#333'/>"
                         "<rect x='4' y='40' width='378' height='30' fill='none' stroke='#333'/>%s</svg>" % (x - 10, ticks))
    v = R.choice([20, 25, 30, 35, 40, 45, 55, 60, 65, 70, 80, 85])
    y = 190 - v * 1.6
    ticks = "".join("<line x1='60' y1='%.1f' x2='%d' y2='%.1f' stroke='#333'/>%s" % (190 - t * 1.6, 72 if t % 10 == 0 else 66, 190 - t * 1.6,
                    "<text x='78' y='%.1f' font-size='11'>%d</text>" % (194 - t * 1.6, t) if t % 10 == 0 else "") for t in range(0, 101, 5))
    return v, "°C", ("<svg viewBox='0 0 140 220' width='140' role='img' aria-label='thermometer'><rect x='48' y='20' width='14' height='175' rx='7' fill='#fff' stroke='#333'/>"
                     "<rect x='51' y='%.1f' width='8' height='%.1f' fill='#d33'/><circle cx='55' cy='200' r='11' fill='#d33' stroke='#333'/>%s</svg>" % (y, 192 - y, ticks))


def g_scale():
    k = R.choice(["ruler", "thermometer"])
    v, u, svg = scale(k)
    from au_sci import once
    if not once(("scale", k, v)):
        return None
    sp = " "
    w = [v + (1 if k == "ruler" else 5), v - (1 if k == "ruler" else 5), v + (2 if k == "ruler" else 10)]
    return tq("%s<br>%s" % (svg, "How long is the pencil?" if k == "ruler" else "What temperature does the thermometer show?"), "%d%s%s" % (v, sp, u), ["%d%s%s" % (x, sp, u) for x in w],
              "Read the mark at the end of the %s." % ("pencil" if k == "ruler" else "red liquid"))


POOL1 = pool(R, [
    ("What is a fair test?", "a test where you change only one thing and keep everything else the same", ["a test that everyone likes", "a test you do once", "a test where you change everything"], "Then you know what caused the result."),
    ("Before a test, Mia says, 'I think the ice will melt fastest in the sun.' What is this?", "a prediction", ["a result", "a conclusion", "a measurement"], "A prediction is what you think will happen."),
    ("Why do we write results in a table?", "to keep them neat and easy to compare", ["to make them change", "so we do not need to measure", "to make the test fair"], "Tables have headings with units."),
    ("Which tool should you use to measure the length of a leaf?", "a ruler", ["a thermometer", "a stopwatch", "scales"], "Length is measured in millimetres or centimetres."),
    ("What should you do if one result is very different from the others?", "check it by doing the test again", ["cross out all the results", "change it to match", "ignore every result"], "Repeating checks for mistakes."),
    ("Which is the safest way to look at a hot liquid in class?", "let an adult pour it and keep your hands away", ["hold the cup over your lap", "taste it to check", "run with it"], "Safety first."),
    ("Which question can be tested in class?", "Does a ball bounce higher on concrete or on grass?", ["Why is blue the best colour?", "Do people like footy?", "Is Monday a good day?"], "You can measure the bounce."),
    ("What is a conclusion?", "a sentence that says what the results show", ["a guess before the test", "a list of equipment", "the title"], "It answers the question."),
    ("Mia drops a ball from 1 m three times: 54 cm, 56 cm, 55 cm. What does this tell her?", "The results are close, so they are reliable.", ["The ball is broken.", "She must have changed the ball.", "The results cannot be used."], "Close repeated results are reliable."),
    ("Which graph is best for showing the number of birds of each kind seen at school?", "a column graph", ["a line graph", "a map", "a thermometer"], "Use a column graph for separate kinds."),
])
POOL5 = pool(R, [
    ("Jack tests which paper towel soaks up the most water. What should he change?", "the brand of paper towel", ["the amount of water", "the size of the pieces", "the time he waits"], "Change one thing."),
    ("In Jack's test, what should he measure?", "how much water each towel soaks up", ["the colour of each towel", "the price of each towel", "the length of the room"], "Measure the result."),
    ("Ruby's table: Brand A 30 mL, Brand B 45 mL, Brand C 20 mL. Which soaks up the most?", "Brand B", ["Brand A", "Brand C", "They are all the same."], "45 mL is the largest amount."),
    ("Kai says, 'Brand B is the best paper towel for everything.' Why is this not a good conclusion?", "He only tested how much water it soaks up.", ["Brand B soaked up the least.", "He did not use a table.", "Paper towels cannot be tested."], "A conclusion must match what was tested."),
    ("Ella's group and Noah's group get different results for the same test. What should they do?", "compare their methods and repeat the test", ["choose the result they like", "stop the test", "make up new results"], "Comparing methods finds mistakes."),
    ("Mia records the temperature of water in the sun every 10 minutes: 20, 24, 27, 29 °C. What pattern does she see?", "The water gets warmer over time.", ["The water gets colder.", "The temperature stays the same.", "There is no pattern."], "Each reading is higher than the one before."),
    ("Which unit should Mia write in her table heading for temperature?", "°C (degrees Celsius)", ["cm", "kg", "minutes only"], "Write the unit in the heading."),
    ("Why do scientists share their results?", "so others can check them and learn from them", ["to keep them secret", "to change them", "because they are not sure"], "Sharing is part of science."),
])


def main():
    sets = U.sets([
        ("Questions and predictions", [(POOL1, 5), (y5_test, 8), (uk5_b1, 4), (y6_obs, 3)]),
        ("Fair tests", [(POOL5, 6), (uk5_b1, 4), (POOL1, 3), (y5_test, 4), (uk5_b5, 3)]),
        ("Measuring", [(g_scale, 8), (y5_eq, 10), (POOL1, 2)]),
        ("Tables and graphs", [(y6_type, 8), (y6_obs, 5), (y5_eq, 4), (g_scale, 3)]),
        ("Patterns and conclusions", [(POOL5, 2), (uk5_b5, 2), (y6_obs, 4), (y6_type, 2), (g_scale, 8), (y5_eq, 2)]),
    ])
    make_au(YEAR, "working-scientifically", SORT, "AC9S4I01, AC9S4I02, AC9S4I03, AC9S4I04, AC9S4I05, AC9S4I06", "Science inquiry",
            "Pose questions and make predictions; plan and conduct fair tests safely; use equipment to measure and record observations in "
            "tables and graphs; identify patterns; and communicate findings (summary of the Australian Curriculum v9.0 Year 4 science inquiry content descriptions).",
            "Working Scientifically", "Working scientifically",
            "Free Year 4 science worksheets on working scientifically: testable questions, predictions, fair tests, reading rulers and "
            "thermometers, tables, column graphs and conclusions. 100 questions with answers.",
            "Change one thing and measure carefully.", "A fair test changes only one thing; careful measuring makes results reliable.",
            "<p><b>Scientists ask a question, make a prediction and test it fairly.</b></p><ul>"
            "<li>Change only one thing and keep everything else the same.</li>"
            "<li>Measure with the right tool (ruler, thermometer, stopwatch, scales) and write the unit.</li>"
            "<li>Record results in a table, look for a pattern, and write a conclusion that matches the results.</li></ul>",
            [("Which tool measures temperature?", ["temperature is measured in °C"], "a thermometer"),
             ("Ball bounces: 54, 56, 55 cm. Reliable?", ["the results are close together"], "yes")],
            ["Changing more than one thing in a test.", "Reading the wrong mark on a scale.", "Forgetting to write units such as cm or °C."],
            [("What is a fair test?", "A fair test changes only one thing and keeps everything else the same, so you know what caused the result."),
             ("Why do we repeat tests?", "Repeating tests checks that the results are reliable. If one result is very different, test again."),
             ("What is the difference between a prediction and a conclusion?", "A prediction is what you think will happen before the test. A conclusion says what the results showed.")],
            sets, allow=("meter",))


if __name__ == "__main__":
    main()
