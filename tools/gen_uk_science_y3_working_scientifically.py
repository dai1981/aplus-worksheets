# -*- coding: utf-8 -*-
"""
UK Year 3 science: Working Scientifically
  python tools/gen_uk_science_y3_working_scientifically.py
Lower key stage 2 enquiry skills with Year 3 investigations (plant growth, celery, rocks, soils, shadows, magnets,
surfaces): asking questions, fair tests, measuring with rulers and stopwatches, recording in tables and bar charts,
spotting results that do not fit, predictions and simple conclusions. Uses the variable, odd-result, prediction and
conclusion makers of the Year 6 unit with Year 3 investigations, a new seed and new questions.
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, People, once
import gen_uk_science_y6_working_scientifically as W

W.U = Unit(61315)
W.R = W.U.R
W.P = People(W.R)
uk_sci.USED.clear()
U, R = W.U, W.R

W.EXP = [("Does the amount of light affect how a bean plant grows?", "the amount of light", "the height of the plant", "the same kind of seed, the same soil and the same amount of water"),
         ("Does the type of soil affect how much water drains through it?", "the type of soil", "the amount of water that drains through", "the same amount of soil and the same amount of water"),
         ("Does the distance from the torch affect the size of a shadow?", "the distance from the torch to the object", "the height of the shadow", "the same torch, the same object and the same screen"),
         ("Which magnet is the strongest?", "the magnet being tested", "the number of paperclips it holds", "the same kind and size of paperclips"),
         ("Does the surface affect how far a toy car rolls?", "the type of surface", "how far the car rolls", "the same car, the same ramp and the same height"),
         ("Does the time in coloured water affect how far the colour climbs up celery?", "the time the celery stands in the water", "how far the colour has climbed", "the same length of celery and the same coloured water"),
         ("Which rock is the hardest?", "the type of rock", "whether it can be scratched", "the same nail and the same pressure"),
         ("Do people with longer legs jump further?", "the person (with their leg length)", "how far they jump", "the same kind of jump from the same start line"),
         ("Does the amount of water affect how tall a cress plant grows?", "the amount of water given each day", "the height of the cress", "the same seeds, the same tray and the same window"),
         ("Can a magnet attract a paperclip through different materials?", "the material between the magnet and the paperclip", "whether the paperclip is still attracted", "the same magnet, the same paperclip and the same thickness")]
W.CONC = [(["Sunny window", "Dark cupboard", "Shady corner"], [12, 4, 7], "number of green leaves after 2 weeks", "The plant in the sunny window grew most leaves.",
           ["The plant in the dark grew best.", "Light makes no difference to plants.", "All plants grow 7 leaves."]),
          (["Sandy soil", "Clay soil", "Loam"], [80, 15, 55], "water that drained through (ml)", "Water drained fastest through sandy soil.",
           ["Clay soil drained fastest.", "All soils drained the same.", "Loam held the least water."]),
          (["Bar magnet", "Horseshoe magnet", "Button magnet"], [8, 12, 3], "paperclips held", "The horseshoe magnet was the strongest of the three.",
           ["The button magnet was the strongest.", "All magnets are equally strong.", "Bigger magnets are always strongest."]),
          (["Carpet", "Wood", "Foil"], [45, 120, 170], "distance the car rolled (cm)", "The car rolled furthest on foil.",
           ["The car rolled furthest on carpet.", "Carpet has the least friction.", "The surface made no difference."])]

PRES = [("the number of each kind of bird seen in the playground", "a bar chart"), ("how many paperclips each magnet held", "a bar chart"),
        ("the parts of a flowering plant", "a labelled diagram"), ("the bones of the human skeleton", "a labelled diagram"),
        ("which objects were or were not attracted to a magnet", "a table"), ("the height of a bean plant measured every 3 days", "a table"),
        ("how to tell apart four kinds of rock", "a classification key"), ("how far a car rolled on four different surfaces", "a bar chart")]


def g_present():
    d, a = R.choice(PRES)
    if not once(("pr", d)):
        return None
    return item("What is the best way to present %s?" % d, a, [x for x in ["a bar chart", "a labelled diagram", "a classification key", "a table"] if x != a],
                "Bar charts compare amounts; tables record results; labelled diagrams name parts; keys identify things.")


B1 = bank([
    ("What is a fair test?", "a test where only one thing is changed and everything else stays the same", ["a test everyone wins", "a test done only once", "a test where everything changes"], "Change one thing."),
    ("Which equipment measures length?", "a ruler or tape measure", ["a stopwatch", "a thermometer", "a magnet"], "Centimetres and metres."),
    ("Which equipment measures time?", "a stopwatch", ["a ruler", "a measuring jug", "a magnifying glass"], "Seconds and minutes."),
    ("Which equipment helps you look closely at soil or rocks?", "a magnifying glass", ["a thermometer", "a stopwatch", "a measuring jug"], "Observe closely."),
    ("What is a prediction?", "what you think will happen, and why", ["what did happen", "a list of equipment", "a type of chart"], "Made before the test."),
    ("Why do scientists record results in a table?", "to keep them organised and easy to read", ["to make them longer", "to hide them", "to change them later"], "Record as you go."),
    ("What is a conclusion?", "what you found out, answering the question", ["a guess before the test", "the equipment list", "the title"], "Based on the results."),
    ("Why should you repeat a measurement?", "to check that the result is right", ["to use up time", "to get a different answer", "because the first one is always wrong"], "Check results."),
])
B5 = bank([
    ("A result does not fit the pattern. What should you do?", "repeat the test to check it", ["copy a friend's result", "make up a new number", "ignore all the results"], "Odd results need checking."),
    ("Why should every bean plant in a test be the same kind?", "so the only difference is the thing being tested", ["so they look nice", "so they grow faster", "it does not matter"], "Fair test."),
    ("After finding that sandy soil drains fastest, what could you ask next?", "Does adding compost change how fast it drains?", ["What colour is sand?", "Is sand a magnet?", "Nothing, science is finished."], "Results lead to new questions."),
    ("Why is a ruler better than guessing the height of a shadow?", "It gives an accurate measurement that can be compared.", ["Rulers make shadows bigger.", "Guessing is always right.", "Rulers are light sources."], "Measure accurately."),
    ("Why might two groups get slightly different results in the same test?", "Small differences in how they measured or carried out the test.", ["Science never works.", "One group cheated.", "Results must always be identical."], "Repeat and compare."),
])


def body():
    think = ("<p><b>Scientists ask questions and answer them with fair tests and careful measurements.</b></p>"
             "<ul><li>Change one thing, measure one thing, keep everything else the same.</li>"
             "<li>Measure with rulers, stopwatches and measuring jugs. Look closely with a magnifying glass.</li>"
             "<li>Record results in tables and bar charts, check odd results and say what you found out.</li></ul>")
    ex = [("Light and bean plants: change what?", ["The question names it"], "the amount of light"),
          ("Paperclips held by each magnet: present how?", ["Comparing amounts"], "a bar chart")]
    mist = ["Changing two things at once.", "Not checking a result that does not fit.", "Writing a conclusion that is not based on the results."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Asking questions", B1 + [(W.g_var, 12)]),
        ("Fair tests", [(W.g_var, 14), (g_present, 6)]),
        ("Results that do not fit", [(W.g_anom, 20)]),
        ("Predictions and conclusions", [(W.g_pred, 14), (W.g_conc, 6)]),
        ("Thinking scientifically", B5 + [(W.g_conc, 5), (W.g_anom, 8), (g_present, 2)]),
    ])
    make_uk(3, "working-scientifically", 15, "Working scientifically",
            "Ask relevant questions and use different types of scientific enquiries to answer them; set up simple practical enquiries, comparative and fair tests; make systematic and careful observations and, where appropriate, take accurate measurements using standard units, using a range of equipment, including thermometers and data loggers; "
            "gather, record, classify and present data in a variety of ways; record findings using simple scientific language, drawings, labelled diagrams, keys, bar charts, and tables; use results to draw simple conclusions, make predictions for new values, suggest improvements and raise further questions.",
            "Working Scientifically",
            "Year 3 Science: Working Scientifically Worksheets (Fair Tests, Tables and Bar Charts)",
            "Working Scientifically",
            "Free Year 3 science worksheets on working scientifically: asking questions, fair tests, measuring, tables, bar charts, odd results, predictions and conclusions. 100 questions with answers.",
            "Ask, test fairly, measure, conclude.",
            "Change one thing and keep everything else the same.",
            body(),
            [("What is a fair test?", "A test where you change only one thing and keep everything else the same, so you know what caused the result."),
             ("How should I record my results?", "In a table as you go, then in a bar chart or labelled diagram if it helps others understand them."),
             ("What do I do with a result that does not fit?", "Check it by repeating the test. It might be a measuring mistake.")],
            sets)


if __name__ == "__main__":
    main()
