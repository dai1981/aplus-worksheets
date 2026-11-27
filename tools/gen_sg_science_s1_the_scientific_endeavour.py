# -*- coding: utf-8 -*-
"""
Singapore Secondary 1 science (Lower Secondary Science): The Scientific Endeavour
  python tools/gen_sg_science_s1_the_scientific_endeavour.py
How science works: asking questions, hypotheses, independent, dependent and controlled variables, fair tests, repeating and
averaging, anomalous results, choosing graphs, conclusions; laboratory apparatus and SI units of measurement; hazard symbols,
laboratory safety and using a Bunsen burner; science knowledge changes with new evidence.
UK working-scientifically makers are reused for anomalies, graphs, predictions and conclusions.
Wrong answers come from real mistakes: "the dependent variable is the one you change", "a hypothesis is the result",
"a beaker measures volume accurately", "the luminous flame is used for heating".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64101)
R = U.R
P = People(R)
WS = luse(U, "gen_uk_science_y6_working_scientifically")

INV = [("how the temperature of water affects the time for sugar to dissolve", "the temperature of the water", "the time for the sugar to dissolve", "the mass of sugar"),
       ("how the length of a pendulum affects the time for one swing", "the length of the pendulum", "the time for one swing", "the mass of the bob"),
       ("how the amount of light affects the height of bean seedlings", "the amount of light", "the height of the seedlings", "the volume of water given"),
       ("how the number of turns of wire affects the strength of an electromagnet", "the number of turns of wire", "the number of paper clips picked up", "the size of the iron nail"),
       ("how the mass of a load affects the extension of a spring", "the mass of the load", "the extension of the spring", "the type of spring"),
       ("how the surface area of a container affects the rate of evaporation", "the surface area of the container", "the volume of water lost in a day", "the starting volume of water"),
       ("how the thickness of a cloth affects the time for hot water to cool", "the thickness of the cloth", "the temperature of the water after 10 minutes", "the starting temperature of the water"),
       ("how the concentration of acid affects the time for a magnesium ribbon to react", "the concentration of the acid", "the time for the magnesium to disappear", "the length of the magnesium ribbon"),
       ("how the height of a ramp affects the distance a toy car travels", "the height of the ramp", "the distance the car travels", "the toy car used"),
       ("how the type of surface affects the force needed to pull a block", "the type of surface", "the force needed to pull the block", "the mass of the block")]


def g_var():
    s, iv, dv, cv = R.choice(INV)
    k = R.choice(["iv", "dv", "cv"])
    if not once(("vr", s, k)):
        return None
    nm, he, his = P.next()
    q = "%s is investigating %s. " % (nm, s)
    a = {"iv": iv, "dv": dv, "cv": cv}[k]
    name = {"iv": "independent variable (the one that is changed)", "dv": "dependent variable (the one that is measured)", "cv": "variable that should be kept constant"}[k]
    return item(q + "What is the %s?" % name, a, [x for x in [iv, dv, cv, "the name of the student"] if x != a][:3],
                "Independent: changed. Dependent: measured. Controlled: kept the same so the test is fair.")


APP = [("a measuring cylinder", "to measure the volume of a liquid"), ("a beaker", "to hold and heat liquids (it gives only a rough volume)"),
       ("a conical flask", "to hold liquids that are swirled, so they do not splash out"), ("a burette", "to add a liquid drop by drop and measure the volume added accurately"),
       ("a pipette", "to transfer a fixed volume of liquid accurately"), ("a tripod stand and wire gauze", "to support a beaker over a Bunsen burner"),
       ("a test-tube holder", "to hold a hot test tube"), ("an evaporating dish", "to evaporate a solution to get the solid"),
       ("a thermometer", "to measure temperature"), ("an electronic balance", "to measure mass"), ("a stopwatch", "to measure time"),
       ("a retort stand with a clamp", "to hold apparatus firmly in place")]


def g_app():
    a, u = R.choice(APP)
    k = R.choice(["name", "use"])
    if not once(("ap", a, k)):
        return None
    if k == "name":
        return item("Which apparatus is used %s?" % u, a, R.sample([x[0] for x in APP if x[0] != a], 3), "%s is used %s." % (a[0].upper() + a[1:], u))
    return item("What is %s used for?" % a, u[0].upper() + u[1:] + ".", [x[1][0].upper() + x[1][1:] + "." for x in R.sample([x for x in APP if x[0] != a], 3)], "%s is used %s." % (a[0].upper() + a[1:], u))


UNITS = [("length", "metre (m)"), ("mass", "kilogram (kg)"), ("time", "second (s)"), ("temperature", "kelvin (K)"), ("electric current", "ampere (A)"),
         ("volume", "cubic metre (m³)"), ("force", "newton (N)"), ("energy", "joule (J)")]


def g_unit():
    q, a = R.choice(UNITS)
    if not once(("un", q)):
        return None
    return item("What is the SI unit of %s?" % q, a, R.sample([x[1] for x in UNITS if x[1] != a], 3), "The SI unit of %s is the %s." % (q, a))


HAZ = [("flammable", "catches fire easily", "ethanol"), ("corrosive", "destroys living tissue and some materials on contact", "concentrated sulfuric acid"),
       ("toxic", "can cause death or serious harm if swallowed, breathed in or absorbed through the skin", "mercury"),
       ("harmful or irritant", "can cause redness or blisters on the skin, or is less dangerous than toxic", "dilute ammonia solution"),
       ("oxidising", "provides oxygen and makes other substances burn more fiercely", "hydrogen peroxide"),
       ("explosive", "may explode when heated, struck or exposed to a flame", "a mixture of hydrogen and oxygen")]


def g_haz():
    h, d, ex = R.choice(HAZ)
    k = R.choice(["mean", "ex"])
    if not once(("hz", h, k)):
        return None
    if k == "mean":
        return item("What does the hazard symbol for a %s substance warn you about?" % h, "The substance " + d + ".", ["The substance " + x[1] + "." for x in R.sample([x for x in HAZ if x[0] != h], 3)], "This is the meaning of the %s symbol." % h)
    return item("Which hazard label is most suitable for %s?" % ex, h, R.sample([x[0] for x in HAZ if x[0] != h], 3), "%s %s." % (ex[0].upper() + ex[1:], d))


B1 = bank([
    ("What is a hypothesis?", "a possible explanation that can be tested by an experiment", ["the result of an experiment", "a fact that can never change", "a list of apparatus"], "For example: 'Sugar dissolves faster in hot water because particles move faster.'"),
    ("Why should only one variable be changed in a fair test?", "so that any change in the results is caused by that variable only", ["to make the test faster", "to use less apparatus", "so the results are always the same"], "All other variables are kept constant."),
    ("How should you read the volume of water in a measuring cylinder?", "at eye level, at the bottom of the meniscus", ["from above, at the top of the meniscus", "from below, at any point", "by guessing"], "This avoids parallax error."),
    ("Why must you wear safety goggles when heating chemicals?", "to protect your eyes from splashes and hot chemicals", ["to see the flame more clearly", "to keep warm", "to measure temperature"], "Goggles protect against splashes."),
    ("When heating a liquid in a test tube, where should you point the mouth of the tube?", "away from yourself and other people", ["towards your face", "towards your partner", "straight down"], "Hot liquid may spurt out."),
    ("Which Bunsen burner flame is used for heating?", "the blue non-luminous flame, with the air hole open", ["the yellow luminous flame, with the air hole closed", "any flame with no air", "a flame with the gas turned off"], "The blue flame is hotter and does not leave soot."),
    ("Why should the air hole of a Bunsen burner be closed when it is lit?", "to get a visible yellow safety flame", ["to make it hotter", "to save gas", "to stop it lighting"], "The safety flame is easy to see when the burner is not in use."),
    ("Scientific knowledge sometimes changes. Why?", "New evidence may show that an old idea needs to be improved.", ["Scientists change ideas at random.", "Science is just opinions.", "Old ideas were always wrong."], "This is how science progresses."),
])
B5 = bank([
    ("A student timed 10 swings of a pendulum as 15.2 s. What is the time for one swing?", "1.52 s", ["15.2 s", "152 s", "0.152 s"], "Timing many swings and dividing reduces the error."),
    ("What should you do first if a chemical splashes on your skin?", "Wash it with plenty of running water and tell the teacher.", ["Wipe it with paper and continue.", "Cover it with a bandage.", "Ignore it."], "Report every accident."),
    ("Why should long hair be tied back in the laboratory?", "so that it does not catch fire or fall into chemicals", ["to see the board", "to keep cool", "to look neat for photographs"], "Safety first near flames."),
    ("A student repeats an experiment three times: 24 s, 25 s, 41 s. What should she do?", "treat 41 s as anomalous, repeat it, and average the reliable results", ["average all three", "use only 41 s", "stop the experiment"], "Anomalous results do not fit the pattern."),
    ("What is the purpose of a control set-up in an experiment?", "to compare with the experimental set-up, to show that the change is caused by the variable tested", ["to make the experiment longer", "to use more apparatus", "to change many variables"], "For example, a set-up without light when testing the effect of light."),
    ("Which statement is a conclusion rather than an observation?", "Sugar dissolves faster in hotter water.", ["The water turned clear after 30 s.", "The thermometer showed 60 °C.", "There were crystals at the bottom."], "A conclusion explains a pattern in the results."),
])


def body():
    think = ("<p><b>Science answers questions by testing ideas with fair experiments.</b></p>"
             "<ul><li><b>Independent variable</b>: what you change. <b>Dependent variable</b>: what you measure. <b>Controlled variables</b>: kept the same.</li>"
             "<li>Repeat measurements and take an average. Look out for <b>anomalous</b> results.</li>"
             "<li>Use the right apparatus and SI units: metre, kilogram, second, kelvin.</li>"
             "<li>Follow safety rules: goggles, tie back hair, read hazard symbols, use the blue flame for heating.</li></ul>")
    ex = [("Testing how temperature affects the time for sugar to dissolve. Dependent variable?", ["It is what you measure"], "the time for the sugar to dissolve"),
          ("Which apparatus measures 25.0 cm³ of liquid accurately for a titration?", ["A beaker is only rough"], "a pipette")]
    mist = ["Mixing up the independent (changed) and dependent (measured) variables.", "Thinking a hypothesis is the result. It is a testable idea.",
            "Measuring volume with a beaker. Use a measuring cylinder, pipette or burette.", "Heating with the yellow luminous flame. Use the blue flame."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Variables and fair tests", B1[:2] + WS.B1 + [(g_var, 12)]),
        ("Results, graphs and conclusions", [(WS.g_anom, 5), (WS.g_graph, 4), (WS.g_pred, 4), (WS.g_conc, 4), (g_var, 3)]),
        ("Apparatus and measurement", B1[2:3] + [(g_app, 12), (g_unit, 7)]),
        ("Laboratory safety", B1[3:] + [(g_haz, 10), (g_app, 3), (g_unit, 1)]),
        ("Exam-style questions", B5 + WS.B5 + [(g_var, 4), (WS.g_anom, 3), (g_haz, 2), (WS.g_conc, 3)]),
    ])
    make_lss(1, "the-scientific-endeavour", 1, "The Scientific Endeavour", "The Scientific Endeavour",
             "Understand how science works: ask questions, form hypotheses and plan fair investigations with independent, dependent and controlled variables; collect, present "
             "and analyse data and draw conclusions; use laboratory apparatus and SI units correctly and safely; recognise hazard symbols; appreciate that scientific knowledge "
             "changes with new evidence (summary of the MOE Lower Secondary Science Syllabus).",
             "The Scientific Endeavour: Investigations and Lab Safety", seo(1, "Scientific Method and Lab Safety"), "Scientific endeavour",
             "Free Secondary 1 science worksheets for Singapore students on the scientific endeavour: variables and fair tests, results and graphs, apparatus, SI units, hazard symbols and lab safety. With answers.",
             "Change one variable, measure one, keep the rest the same.", "Repeat, average and look for anomalous results.",
             body(),
             [("What is the difference between independent and dependent variables?", "The independent variable is the one you change. The dependent variable is the one you measure."),
              ("Why do we repeat experiments?", "To check that results are reliable and to find anomalous results. We then take an average."),
              ("Which Bunsen burner flame is used for heating?", "The blue non-luminous flame, with the air hole open.")],
             sets)


if __name__ == "__main__":
    main()
