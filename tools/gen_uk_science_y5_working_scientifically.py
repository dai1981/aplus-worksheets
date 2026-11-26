# -*- coding: utf-8 -*-
"""
UK Year 5 science: Working Scientifically
  python tools/gen_uk_science_y5_working_scientifically.py
Upper key stage 2 enquiry skills with Year 5 investigations (dissolving, parachutes, friction, insulation, rusting):
variables, fair tests, repeat readings and means, choosing graphs, predictions and conclusions.
Uses the question makers of the Year 6 unit with new investigations, a new seed and new hand-written questions.
"""
import uk_sci
from uk_sci import Unit, bank, lesson, make_uk, People
import gen_uk_science_y6_working_scientifically as W

W.U = Unit(61514)
W.R = W.U.R
W.P = People(W.R)
uk_sci.USED.clear()
U, R = W.U, W.R

W.EXP = [("Does the temperature of water affect how fast salt dissolves?", "the temperature of the water", "the time for the salt to dissolve", "the same amount of salt and water, and stirring the same way"),
         ("Does the size of a parachute affect how long it takes to fall?", "the size of the parachute", "the time taken to fall", "the same load, the same material and the same drop height"),
         ("Does the type of surface affect how far a toy car rolls?", "the type of surface", "how far the car rolls", "the same car, the same ramp height and letting go without pushing"),
         ("Does the material of a wrapping affect how fast an ice cube melts?", "the material of the wrapping", "the time for the ice cube to melt", "the same size of ice cube, the same thickness of wrapping and the same room"),
         ("Does the shape of plasticine affect how fast it sinks in water?", "the shape of the plasticine", "the time taken to sink", "the same mass of plasticine and the same tube of water"),
         ("Does salt water make iron nails rust faster than tap water?", "the type of water", "how much rust forms in a week", "the same kind of nail, the same amount of water and the same place"),
         ("Does the number of spoons of bicarbonate of soda affect how much a balloon inflates?", "the number of spoons of bicarbonate of soda", "the width of the balloon", "the same amount of vinegar and the same size of bottle and balloon"),
         ("Does the length of a lever affect the force needed to lift a load?", "the length of the lever", "the force needed to lift the load", "the same load and the same pivot position"),
         ("Does stirring affect how fast sugar dissolves?", "how much the water is stirred", "the time for the sugar to dissolve", "the same amount of sugar and water at the same temperature"),
         ("Does the amount of sunlight affect how tall a sunflower grows?", "the amount of sunlight", "the height of the sunflower after three weeks", "the same seeds, soil, pot size and amount of water")]
W.CONC = [(["Sugar cube", "Granulated sugar", "Caster sugar"], [180, 90, 50], "time to dissolve (s)", "The smaller the pieces, the faster the sugar dissolved.",
           ["Sugar cubes dissolved fastest.", "Size made no difference.", "All sugar dissolves in 90 seconds."]),
          (["Wool", "Foil", "Newspaper"], [52, 41, 46], "temperature after 20 minutes (°C)", "Wool was the best thermal insulator of the three.",
           ["Foil was the best thermal insulator.", "All three insulated equally well.", "Wool is the best material for every job."]),
          (["Ice", "Wood", "Carpet"], [2, 6, 11], "force to pull the shoe (N)", "Carpet gave the most friction.",
           ["Ice gave the most friction.", "Wood gave the least friction.", "Friction was the same on all surfaces."]),
          (["Tap water", "Salt water", "Dry air"], [3, 8, 0], "rust score after a week (0 to 10)", "The nail in salt water rusted most.",
           ["The nail in dry air rusted most.", "Rusting needs only air.", "Salt stops rusting."])]

B1 = bank([
    ("What is a variable in an investigation?", "something that can change or be changed", ["the name of the investigation", "the result you hoped for", "the equipment list"], "Change one, measure one, control the rest."),
    ("Which variable do you change on purpose?", "the independent variable", ["the dependent variable", "the control variable", "no variable"], "It goes in the first column of a table."),
    ("Which variable do you measure?", "the dependent variable", ["the independent variable", "the control variable", "the weather"], "It is the result."),
    ("Why is a fair test important?", "so you know the change you made caused the result", ["so the test is quick", "so everyone gets the same mark", "so the result is what you predicted"], "Only one thing changes."),
    ("What is a mean?", "the total of the results divided by how many results there are", ["the biggest result", "the result in the middle of the table", "the first result"], "An average."),
    ("Why should measurements be read at eye level?", "to read the scale accurately", ["to make the test fair", "to change the result", "it does not matter"], "Avoid reading at an angle."),
    ("Which is the best way to measure 50 ml of water?", "a measuring cylinder", ["a teaspoon", "a ruler", "a newton meter"], "Use the right equipment."),
    ("What should a good prediction include?", "what you think will happen and why", ["only the result", "a drawing of the equipment", "the date"], "Use what you know."),
])
B5 = bank([
    ("Two groups get different results for the same parachute. What is the best thing to do?", "repeat the test and compare the results", ["choose the faster time", "ignore both", "change the parachute"], "Repeat to check."),
    ("Why might a stopwatch give slightly different times for the same fall?", "People take a moment to react when starting and stopping it.", ["Stopwatches are always wrong.", "Gravity changes.", "Time goes faster in the morning."], "Human reaction time."),
    ("How could you make timing a falling parachute more accurate?", "drop it from a greater height and take the mean of several tries", ["drop it from lower down", "time it only once", "guess the time"], "Longer times and repeats."),
    ("A result does not fit the pattern. What should a scientist do first?", "check it by repeating that test", ["delete all the results", "change the other results", "ignore the whole investigation"], "Anomalous results."),
    ("What does it mean if a conclusion is 'supported by evidence'?", "The results agree with it.", ["Someone important said it.", "It was guessed before the test.", "It sounds right."], "Evidence-based."),
])
W.B1, W.B5 = B1, B5


def body():
    think = ("<p><b>A fair test changes one variable, measures one variable and keeps the rest the same.</b></p>"
             "<ul><li>Plan: question, prediction, variables, equipment.</li>"
             "<li>Measure carefully; repeat readings; spot anomalous results; find the mean.</li>"
             "<li>Show results in a table and the right graph; write a conclusion that the evidence supports.</li></ul>")
    ex = [("Parachute size and fall time: what do you change?", ["The question names it"], "the size of the parachute"),
          ("Times 3.1, 3.3, 3.2 s. Mean?", ["(3.1 + 3.3 + 3.2) ÷ 3"], "3.2 s")]
    mist = ["Changing two things at once.", "Doing a test only once.", "Writing a conclusion that goes further than the results."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Fair tests", B1 + [(W.g_var, 12)]),
        ("Variables", [(W.g_var, 14), (W.g_graph, 6)]),
        ("Repeat readings", [(W.g_anom, 20)]),
        ("Graphs and predictions", [(W.g_pred, 14), (W.g_conc, 6)]),
        ("Conclusions", B5 + [(W.g_conc, 5), (W.g_anom, 7), (W.g_graph, 3)]),
    ])
    make_uk(5, "working-scientifically", 14, "Working scientifically",
            "Plan different types of scientific enquiries to answer questions, including recognising and controlling variables where necessary; take measurements with increasing accuracy and precision, taking repeat readings when appropriate; "
            "record data and results using tables, bar and line graphs; use test results to make predictions to set up further comparative and fair tests; report and present findings, including conclusions.",
            "Working Scientifically",
            "Year 5 Science: Working Scientifically Worksheets (Variables, Fair Tests, Means)",
            "Working Scientifically",
            "Free Year 5 science worksheets on working scientifically: variables in Year 5 investigations, fair tests, repeat readings, means, graphs, predictions and conclusions. 100 questions with answers.",
            "Plan it fairly, measure it carefully.",
            "Change one thing, measure one thing, repeat and let the results decide.",
            body(),
            [("What makes a test fair?", "Only one variable is changed, one is measured, and all the others are kept the same."),
             ("Why do we repeat readings?", "To check our results, spot anomalous ones and work out a more reliable mean."),
             ("How do I write a conclusion?", "Say what the results show, answer the question you asked, and only claim what the evidence supports.")],
            sets)


if __name__ == "__main__":
    main()
