# -*- coding: utf-8 -*-
"""
Singapore Secondary 2 science (Lower Secondary Science, Interactions): Application of Forces and Transfer of Energy (forces and pressure)
  python tools/gen_sg_science_s2_forces_and_pressure.py
Contact forces (friction, normal force, air resistance, tension, upthrust) and non-contact forces (gravitational, magnetic,
electrostatic); a force can change an object's motion, shape or size, cause a turning effect or exert pressure; forces in
newtons; mass and weight; balanced and unbalanced forces; pressure = force / area and pressure in everyday life
(high heels, knives, suction cups, straws, submarines).
UK KS3 force and pressure makers are reused (no W = mg or moment formulas: not in the Singapore syllabus).
Wrong answers come from real mistakes: "gravity is a contact force", "mass and weight are the same", "a sharp knife has a
larger area", "atmospheric pressure sucks the drink up".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64201)
R = U.R
P = People(R)
FO = luse(U, "gen_uk_science_y7_forces", drop=[r"weigh\w* \d", r"\bkg\b.*\bN\b", r"gravitational field"])
PR = luse(U, "gen_uk_science_y9_pressure", drop=[r"float or sink", r"hovers"])

CONTACT = ["friction", "air resistance", "the normal force", "tension in a rope", "upthrust", "water resistance"]
NONCONTACT = ["gravitational force", "magnetic force", "electrostatic force"]


def g_kind():
    k = R.choice(["c", "n"])
    a = R.choice(CONTACT if k == "c" else NONCONTACT)
    if not once(("kd", a)):
        return None
    w = R.sample(NONCONTACT, 3) if k == "c" else R.sample(CONTACT, 3)
    return item("Which of these is a %s force?" % ("contact" if k == "c" else "non-contact"), a, w,
                "Contact forces act only when objects touch. Non-contact forces (gravitational, magnetic, electrostatic) act at a distance.")


EFF = [("A goalkeeper catches a moving ball.", "It stops a moving object."), ("A cyclist pedals harder to go up a slope.", "It changes the speed of a moving object."),
       ("A footballer heads the ball towards the goal.", "It changes the direction of a moving object."), ("A baker presses a ball of dough flat.", "It changes the shape of an object."),
       ("A spring is pulled and gets longer.", "It changes the size of an object."), ("A spanner is used to loosen a nut.", "It causes a turning effect."),
       ("A door is pushed open at its handle.", "It causes a turning effect."), ("A trolley at rest is pushed.", "It makes a stationary object move."),
       ("A drawing pin is pushed into a notice board.", "It exerts a pressure on a small area.")]
EALL = ["It stops a moving object.", "It changes the speed of a moving object.", "It changes the direction of a moving object.", "It changes the shape of an object.",
        "It changes the size of an object.", "It causes a turning effect.", "It makes a stationary object move.", "It exerts a pressure on a small area."]


def g_eff():
    s, a = R.choice(EFF)
    if not once(("ef", s)):
        return None
    return item(s + " Which effect of a force is shown?", a, R.sample([x for x in EALL if x != a], 3), "Forces can change motion, shape or size, cause turning and exert pressure.")


def g_p():
    k = R.choice(["p", "f", "a"])
    f = R.choice([20, 30, 40, 60, 80, 120, 150, 200, 500, 600])
    a = R.choice([0.1, 0.2, 0.5, 2, 4, 5])
    p = round(f / a, 6)
    if p != int(p) or not once(("pp", k, f, a)) or not once(("pk", k), 6):
        return None
    p = int(p)
    fa = "%g" % a
    if k == "p":
        return item("A force of %d N acts on an area of %s m². What is the pressure?" % (f, fa), "%d Pa" % p, ["%g Pa" % (f * a), "%g Pa" % (a / f), "%g Pa" % (f + a)],
                    "Pressure = force ÷ area = %d ÷ %s = %d Pa (N/m²)." % (f, fa, p))
    if k == "f":
        return item("A pressure of %d Pa acts on an area of %s m². What is the force?" % (p, fa), "%d N" % f, ["%g N" % (p / a), "%g N" % (p + a), "%d N" % p],
                    "Force = pressure × area = %d × %s = %d N." % (p, fa, f))
    return item("A force of %d N gives a pressure of %d Pa. What is the area?" % (f, p), "%s m²" % fa, ["%g m²" % (f * p), "%g m²" % (p / f), "%g m²" % (p - f)],
                "Area = force ÷ pressure = %d ÷ %d = %s m²." % (f, p, fa))


def g_cmp():
    nm, he, his = P.next()
    k = R.choice(["heels", "knife", "block", "snow"])
    if not once(("cm", k)):
        return None
    if k == "heels":
        return item("%s wears high-heeled shoes and then flat shoes. Why do the high heels sink into soft grass more?" % nm, "The same weight acts on a smaller area, so the pressure is greater.",
                    ["High heels make %s heavier." % nm, "The force is smaller with high heels.", "Flat shoes have a smaller area."], "Pressure = force ÷ area.")
    if k == "knife":
        return item("Why does a sharp knife cut better than a blunt one?", "Its thin edge has a small area, so the same force gives a greater pressure.",
                    ["Its edge has a large area.", "A sharp knife is heavier.", "A blunt knife gives more pressure."], "A small area means high pressure.")
    if k == "block":
        return item("A brick is placed on a table first on its largest face, then on its smallest face. When is the pressure on the table greatest?", "on its smallest face",
                    ["on its largest face", "it is the same both ways", "when it is lifted up"], "The weight is the same; a smaller area gives a greater pressure.")
    return item("Why do people wear snowshoes or use wide skis to walk on deep snow?", "They spread the weight over a large area, so the pressure is lower.",
                ["They make the person lighter.", "They increase the pressure.", "They melt the snow."], "Large area, low pressure.")


B1 = bank([
    ("What is the difference between mass and weight?", "Mass is the amount of matter in an object (kg); weight is the gravitational force on it (N).", ["They are the same thing.", "Weight is measured in kg and mass in N.", "Mass changes on the Moon but weight does not."], "On the Moon your mass is the same, but your weight is less."),
    ("Which instrument measures force?", "a spring balance (newton meter)", ["an electronic balance", "a metre rule", "a thermometer"], "Force is measured in newtons (N)."),
    ("An astronaut goes from the Earth to the Moon. What happens?", "Her mass stays the same but her weight decreases.", ["Her mass and weight both decrease.", "Her mass decreases but her weight stays the same.", "Nothing changes."], "Gravity on the Moon is weaker."),
    ("What happens to a moving object when the forces on it are balanced?", "It keeps moving at the same speed in the same direction.", ["It stops at once.", "It speeds up.", "It changes direction."], "Balanced forces do not change motion."),
    ("Why is it easier to loosen a nut with a long spanner than a short one?", "A force further from the pivot gives a larger turning effect.", ["A long spanner is heavier.", "The nut gets smaller.", "Friction disappears."], "Pushing far from the pivot helps."),
    ("How does a suction cup stick to a smooth wall?", "Air is pushed out, so the air pressure outside pushes the cup against the wall.", ["The cup sucks the wall.", "Glue in the cup holds it.", "Magnetism holds it."], "Atmospheric pressure does the pushing."),
    ("How do you drink through a straw?", "You lower the air pressure in the straw, and atmospheric pressure pushes the drink up.", ["The straw pulls the drink up.", "Gravity pushes the drink up.", "The drink is lighter than air."], "There is no 'suction force'."),
    ("Why can a submarine dive only to a certain depth?", "Water pressure increases with depth and could crush the hull.", ["Water gets lighter with depth.", "There is no water deep down.", "Pressure decreases with depth."], "Deep-sea submarines need very strong hulls."),
])
B5 = bank([
    ("A student of weight 500 N stands on both feet with a total area of 0.05 m². What pressure does he exert on the floor?", "10 000 Pa", ["25 Pa", "100 Pa", "500 Pa"], "500 ÷ 0.05 = 10 000 Pa."),
    ("Why are dams built thicker at the bottom than at the top?", "Water pressure is greater at greater depth.", ["Water is lighter at the bottom.", "To save concrete.", "Fish live at the bottom."], "Pressure in a liquid increases with depth."),
    ("A car brakes and slows down. Which force mainly causes this?", "friction between the brakes and the wheels, and the tyres and the road", ["gravitational force", "magnetic force", "upthrust"], "Friction acts against motion."),
    ("A box is pushed with 30 N to the right while friction is 30 N to the left. The box was moving. What happens?", "It moves at a steady speed.", ["It speeds up.", "It stops immediately.", "It moves to the left."], "The forces are balanced."),
    ("Which statement about gravitational force is correct?", "It is a non-contact force that pulls objects towards the Earth.", ["It only acts when objects touch.", "It pushes objects away from the Earth.", "It only acts on metals."], "Gravity acts at a distance."),
    ("Earthquakes and tsunamis release huge forces. Why do engineers in some countries build earthquake-resistant buildings?", "to reduce damage and save lives when these forces act on buildings", ["to stop earthquakes from happening", "to make buildings heavier", "because buildings attract earthquakes"], "Understanding forces helps us design safer structures."),
])


def body():
    think = ("<p><b>A force is a push or a pull. It is measured in newtons (N).</b></p>"
             "<ul><li><b>Contact forces</b>: friction, normal force, tension, air resistance, upthrust. <b>Non-contact forces</b>: gravitational, magnetic, electrostatic.</li>"
             "<li>A force can change an object's speed, direction, shape or size, cause a <b>turning effect</b>, or exert <b>pressure</b>.</li>"
             "<li><b>Mass</b> (kg) is the amount of matter; <b>weight</b> (N) is the pull of gravity on it.</li>"
             "<li><b>Pressure = force ÷ area</b>, in Pa (N/m²). A smaller area gives a greater pressure.</li></ul>")
    ex = [("A force of 60 N acts on 0.2 m². Pressure?", ["60 ÷ 0.2"], "300 Pa"),
          ("Why does a knife cut better when sharp?", ["Smaller area"], "The same force gives a greater pressure.")]
    mist = ["Calling gravity a contact force. It acts at a distance.", "Thinking mass and weight are the same. Weight is a force in newtons.",
            "Thinking a large area gives a large pressure. It is the opposite.", "Saying a straw 'sucks' the drink. Atmospheric pressure pushes it up."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Types of forces", FO.B1 + [(g_kind, 8), (FO.g_name, 6), (B1[1], 1)]),
        ("Effects of forces", [(g_eff, 9), (FO.g_res, 5), (FO.g_bal, 4), (B1[3], 1), (B1[4], 1)]),
        ("Mass, weight and measuring force", [B1[0], B1[2]] + [(FO.g_spring, 8), (FO.g_res, 5), (FO.g_bal, 3), (g_kind, 2)]),
        ("Pressure", PR.B1 + [(g_p, 10), (g_cmp, 4), (PR.g_ex, 4)]),
        ("Exam-style questions", B5 + B1[5:] + [(PR.g_depth, 2), (PR.g_calc, 3), (PR.g_ex, 2), (g_p, 2), (PR.g_gas, 2)]),
    ])
    make_lss(2, "forces-and-pressure", 1, "Interactions", "Application of Forces and Transfer of Energy (Forces and pressure)",
             "Distinguish contact forces such as friction from non-contact forces such as magnetic and gravitational forces; recognise that a force can change an object's motion, "
             "cause a turning effect, change its size or shape, or exert pressure; measure force in newtons and compare weight and mass; investigate pressure using "
             "pressure = force / area and appreciate examples such as high heels, knives, suction cups, straws and submarines (summary of the MOE Lower Secondary Science Syllabus).",
             "Forces and Pressure", seo(2, "Forces and Pressure"), "Forces and pressure",
             "Free Secondary 2 science worksheets for Singapore students on forces and pressure: contact and non-contact forces, effects of forces, mass and weight, pressure = force / area. With answers.",
             "A force is a push or a pull, measured in newtons.", "Pressure = force ÷ area.",
             body(),
             [("What is the difference between mass and weight?", "Mass is the amount of matter (kg) and is the same everywhere. Weight is the gravitational force on the object (N) and changes with gravity."),
              ("What are contact and non-contact forces?", "Contact forces act when objects touch (friction, tension). Non-contact forces act at a distance (gravitational, magnetic, electrostatic)."),
              ("What is the unit of pressure?", "The pascal (Pa), which is one newton per square metre (N/m²).")],
             sets)


if __name__ == "__main__":
    main()
