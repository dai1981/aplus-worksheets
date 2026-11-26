# -*- coding: utf-8 -*-
"""
UK Year 4 science: Working Scientifically
  python tools/gen_uk_science_y4_working_scientifically.py
Lower key stage 2 enquiry skills with Year 4 investigations (evaporation, sound, circuits, melting, teeth): asking
questions, fair tests, careful measurement (thermometers, sound meters), recording in tables and bar charts, spotting
results that do not fit, and simple conclusions. Uses the variable, repeat-reading, prediction and conclusion makers
of the Year 6 unit with Year 4 investigations, a new seed and new questions; the graph question is Year 4's own
(tables, bar charts, labelled diagrams and keys).
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, People, once
import gen_uk_science_y6_working_scientifically as W

W.U = Unit(61414)
W.R = W.U.R
W.P = People(W.R)
uk_sci.USED.clear()
U, R = W.U, W.R

W.EXP = [("Does the temperature of a room affect how fast a puddle of water evaporates?", "the temperature of the room", "the time for the water to evaporate", "the same amount of water and the same size of dish"),
         ("Does the length of an elastic band affect the pitch of the twang?", "the length of the elastic band", "how high or low the note sounds", "the same band thickness and the same tightness"),
         ("Does the number of cells affect how bright a bulb is?", "the number of cells", "the brightness of the bulb", "the same bulb and the same wires"),
         ("Does the material wrapped round an ice cube affect how fast it melts?", "the material of the wrapping", "the time for the ice cube to melt", "the same size of ice cube and the same room"),
         ("Does the distance from a radio affect how loud it sounds?", "the distance from the radio", "the sound level on a sound meter", "the same radio at the same volume setting"),
         ("Do different drinks damage eggshell differently?", "the type of drink", "how much the eggshell is damaged", "the same size of eggshell, the same amount of drink and the same time"),
         ("Does the material of a cup affect how fast hot water cools?", "the material of the cup", "the temperature after 15 minutes", "the same amount of water at the same starting temperature"),
         ("Does the type of material in a circuit gap affect whether a bulb lights?", "the material in the gap", "whether the bulb lights", "the same cell, bulb and wires"),
         ("Does the amount of water in a bottle affect the note it makes when tapped?", "the amount of water", "how high or low the note sounds", "identical bottles tapped with the same spoon"),
         ("Do snails prefer damp or dry places?", "how damp the place is", "how many snails go to each side", "the same tray, the same snails and the same light")]

PRES = [("the number of each kind of minibeast found under a log", "a bar chart"), ("the favourite instrument of each pupil in a class", "a bar chart"),
        ("how many seconds ice cubes took to melt in four different wrappings", "a bar chart"), ("the parts of a plant and what each does", "a labelled diagram"),
        ("the parts of the digestive system", "a labelled diagram"), ("how to identify six garden birds", "a classification key"),
        ("which materials did and did not conduct electricity", "a table"), ("the temperature readings of a cup every 5 minutes", "a table")]


def g_present():
    d, a = R.choice(PRES)
    if not once(("pr", d)):
        return None
    return item("What is the best way to present %s?" % d, a, [x for x in ["a bar chart", "a labelled diagram", "a classification key", "a table"] if x != a],
                "Bar charts compare amounts; tables record results; labelled diagrams name parts; keys identify things.")


B1 = bank([
    ("What is a scientific question?", "a question you can answer by observing or testing", ["a question about your opinion", "any question at all", "a question with no answer"], "For example: does salt make ice melt faster?"),
    ("Which equipment measures temperature?", "a thermometer", ["a ruler", "a stopwatch", "a newton meter"], "Read in °C."),
    ("Which equipment measures time?", "a stopwatch or timer", ["a thermometer", "a measuring jug", "a ruler"], "Seconds and minutes."),
    ("Which equipment measures how much liquid there is?", "a measuring jug or cylinder", ["a stopwatch", "a ruler", "a magnet"], "Millilitres (ml)."),
    ("In a fair test, how many things should you change?", "one", ["two", "all of them", "none"], "Change one, keep the rest the same."),
    ("Why do scientists write results in a table?", "to keep them organised and easy to read", ["to make them longer", "to hide them", "to change them later"], "Record as you go."),
    ("What is a prediction?", "what you think will happen, and why", ["what did happen", "a list of equipment", "a type of graph"], "Made before the test."),
    ("What does a conclusion do?", "says what you found out and answers the question", ["lists the equipment", "repeats the question only", "gives the date"], "Based on the results."),
])
B5 = bank([
    ("A pupil times an ice cube melting and gets 25 minutes, but everyone else gets about 15. What should they do?", "repeat the test to check it", ["copy someone else's answer", "make up a new number", "ignore everyone else"], "Odd results should be checked."),
    ("Why is it better to measure sound with a sound meter than by listening?", "It gives a number, so results can be compared fairly.", ["It is louder.", "Ears cannot hear.", "Sound meters change the sound."], "Accurate measurements."),
    ("What could you do next after finding that warm water evaporates faster?", "ask a new question, such as whether wind makes it faster too", ["stop doing science", "repeat the same test forever", "forget the result"], "Results lead to new questions."),
    ("Why should you read a thermometer at eye level?", "to read the scale accurately", ["to make the liquid move", "to warm the thermometer", "it does not matter"], "Avoid mistakes."),
    ("Why might two groups get slightly different results for the same test?", "Small differences in how they measured or did the test.", ["Science never works.", "One group must have cheated.", "Results should always be identical."], "Repeat and compare."),
])


def body():
    think = ("<p><b>Scientists ask questions and answer them with fair tests and careful measurements.</b></p>"
             "<ul><li>Change one thing, measure one thing, keep the rest the same.</li>"
             "<li>Measure with the right equipment: thermometers, stopwatches, measuring jugs, sound meters.</li>"
             "<li>Record results in tables and bar charts, check results that do not fit, and say what you found out.</li></ul>")
    ex = [("Room temperature and evaporation: change what?", ["The question names it"], "the temperature of the room"),
          ("Minibeasts found under a log: present how?", ["Comparing amounts of each kind"], "a bar chart")]
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
    make_uk(4, "working-scientifically", 14, "Working scientifically",
            "Ask relevant questions and use different types of scientific enquiries to answer them; set up simple practical enquiries, comparative and fair tests; make systematic and careful observations and, where appropriate, take accurate measurements using standard units, using a range of equipment, including thermometers and data loggers; "
            "gather, record, classify and present data in a variety of ways; record findings using simple scientific language, drawings, labelled diagrams, keys, bar charts, and tables; use results to draw simple conclusions, make predictions for new values, suggest improvements and raise further questions.",
            "Working Scientifically",
            "Year 4 Science: Working Scientifically Worksheets (Fair Tests, Tables and Bar Charts)",
            "Working Scientifically",
            "Free Year 4 science worksheets on working scientifically: asking questions, fair tests, measuring with thermometers and stopwatches, tables, bar charts, odd results and conclusions. 100 questions with answers.",
            "Ask, test fairly, measure, conclude.",
            "Change one thing and keep everything else the same.",
            body(),
            [("What is a fair test?", "A test where you change only one thing and keep everything else the same, so you know what caused the result."),
             ("How should I record my results?", "In a table as you go, then in a bar chart or labelled diagram if it helps others understand them."),
             ("What do I do with a result that does not fit?", "Check it by repeating the test. It might be a measuring mistake.")],
            sets)


if __name__ == "__main__":
    main()
