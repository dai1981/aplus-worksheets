# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Gravitational force and elastic spring force (Interactions)
  python tools/gen_sg_science_p6_gravitational_and_elastic_spring_force.py
Gravitational force is the pull of the Earth on all objects; the weight of an object is the gravitational force on it,
measured in newtons with a spring balance. A spring that is stretched or compressed exerts an elastic spring force;
the extension increases with the load until the spring is stretched too far. Spring-extension tables are generated here;
UK Year 5 gravity and Year 7 spring questions are reused with "spring balance".
Wrong answers come from real mistakes: "heavier objects always fall much faster", "weight is measured in kilograms",
"a spring gets shorter when more weight is added", "gravity only acts on falling objects", "the extension is the total length".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto

U = Unit(63605)
R = U.R
P = People(R)
REP = [(r"newton metre", "spring balance"), (r"\btoward\b", "towards")]
GR = use(U, "gen_uk_science_y5_gravity", rep=REP, drop=["has a pupil", "has a dog", "Galileo", "planet"])
FO = use(U, "gen_uk_science_y7_forces", rep=REP, drop=["upthrust", "water resistance", "drag"])
import gen_sg_science_p6_forces_and_their_effects as FE


def g_spring():
    L0 = R.choice([8, 10, 12, 15])
    per = R.choice([1, 2, 3])
    loads = [0, 1, 2, 3, 4, 5]
    lens = [L0 + per * w for w in loads]
    k = R.choice(["ext", "len", "pred", "trend", "load", "orig"])
    if not once(("sp", k, L0, per)) or not once(("spn", k), 3):
        return None
    tb = table(["Load (N)"] + [str(w) for w in loads], [["Length of spring (cm)"] + [str(x) for x in lens]])
    q0 = "%s hung loads on a spring and measured its length.<br>%s" % (P.next()[0], tb)
    if k == "ext":
        return item(q0 + "What was the extension of the spring with a load of 3 N?", "%d cm" % (3 * per),
                    ["%d cm" % lens[3], "%d cm" % (2 * per) if per != 0 else "1 cm", "%d cm" % L0], "Extension = %d − %d = %d cm." % (lens[3], L0, 3 * per))
    if k == "len":
        return item(q0 + "How long was the spring with a load of 4 N?", "%d cm" % lens[4], ["%d cm" % x for x in (lens[3], lens[5], 4 * per)], "Read the table.")
    if k == "pred":
        return item(q0 + "If the pattern continues, how long will the spring be with a load of 7 N?", "%d cm" % (L0 + 7 * per),
                    ["%d cm" % x for x in (L0 + 6 * per, 7 * per, L0 + 8 * per)], "The spring stretches %d cm for every 1 N." % per)
    if k == "trend":
        return item(q0 + "What does the table show?", "The greater the load, the longer the spring.", ["The greater the load, the shorter the spring.", "The load does not change the length.", "The spring breaks at 1 N."],
                    "The spring extends more when a bigger force pulls it.")
    if k == "load":
        t = L0 + 6 * per
        return item(q0 + "What load would make the spring %d cm long?" % t, "6 N", ["5 N", "%d N" % t, "7 N"], "Each 1 N adds %d cm, and %d − %d = %d cm." % (per, t, L0, 6 * per))
    return item(q0 + "What is the original length of the spring?", "%d cm" % L0, ["%d cm" % x for x in (lens[1], per, lens[5])], "It is the length with no load (0 N).")


def g_compare():
    a = (R.choice([1, 2, 3]), R.choice([10, 12]))
    b = (a[0] + R.choice([1, 2]), a[1])
    k = R.choice(["stiff", "which"])
    if not once(("cm", a, b, k)) or not once(("cmn", k), 3):
        return None
    tb = table(["Load (N)", "0", "2", "4"], [["Spring A length (cm)", str(a[1]), str(a[1] + 2 * a[0]), str(a[1] + 4 * a[0])],
                                         ["Spring B length (cm)", str(b[1]), str(b[1] + 2 * b[0]), str(b[1] + 4 * b[0])]])
    q0 = "Two springs of the same original length were tested with the same loads.<br>%s" % tb
    if k == "stiff":
        return item(q0 + "Which spring is stiffer (harder to stretch)?", "Spring A", ["Spring B", "They are equally stiff.", "Neither stretches."], "Spring A stretches less for the same load.")
    return item(q0 + "Which spring would be better for a spring balance that measures heavy loads?", "Spring A, because it stretches less for each newton",
                ["Spring B, because it stretches more for each newton", "Either; there is no difference", "Neither; springs cannot measure loads"], "A stiffer spring can measure bigger forces without being overstretched.")


def g_weight():
    obj, ms = R.choice([("bag of rice", [5, 10]), ("watermelon", [2, 3, 4]), ("box of books", [6, 8]), ("pail of sand", [3, 5]),
                        ("bottle of cooking oil", [1, 2]), ("pineapple", [1, 1.5]), ("packet of flour", [0.5, 1])])
    m = R.choice(ms)
    if not once(("wt", m)):
        return None
    n = m * 10
    ns = ("%g" % n)
    return item("On Earth, gravity pulls with about 10 N on every 1 kg. A %s has a mass of %g kg. What is its weight?" % (obj, m), "%s N" % ns,
                ["%g kg" % m, "%g N" % m, "%g N" % (n * 10)], "%g × 10 = %s N." % (m, ns))


B1 = bank([
    ("What is gravitational force?", "the pull of the Earth on objects", ["the push of air on objects", "a force between two magnets", "the force between rubbing surfaces"], "The Earth pulls everything towards its centre."),
    ("In which direction does gravity pull objects on Earth?", "towards the centre of the Earth (downwards)", ["upwards", "sideways", "towards the Sun only"], "That is why things fall down."),
    ("What is the weight of an object?", "the gravitational force acting on it", ["the amount of matter in it", "its size", "its volume"], "Weight is measured in newtons."),
    ("Which unit is weight measured in?", "newtons (N)", ["kilograms (kg)", "centimetres (cm)", "millilitres (ml)"], "Mass is measured in kg; weight is a force in N."),
    ("Which instrument measures weight?", "a spring balance", ["a measuring cylinder", "a thermometer", "a ruler"], "The spring stretches when an object hangs on it."),
    ("Does gravity act on an object resting on a table?", "Yes. The table pushes up to balance it.", ["No, only on falling objects.", "Only at night.", "Only if it is heavy."], "Gravity acts on all objects all the time."),
    ("Why does a ball thrown upwards come back down?", "Gravity pulls it back towards the Earth.", ["It runs out of force.", "Air pushes it down.", "The ball wants to come back."], "Gravity acts on it the whole time."),
    ("Which statement about mass and weight is correct?", "Mass is the amount of matter; weight is the pull of gravity on it.", ["They are the same thing.", "Mass is measured in newtons.", "Weight is measured in kilograms."], "A 1 kg mass weighs about 10 N on Earth."),
])
B2 = bank([
    ("What is elastic spring force?", "the force exerted by a spring when it is stretched or compressed", ["the pull of the Earth", "the force between magnets", "the force when surfaces rub"], "The spring pushes or pulls back towards its original length."),
    ("What happens to a spring when a load is hung on it?", "It extends (stretches).", ["It gets shorter.", "Nothing happens.", "It becomes a magnet."], "The weight of the load pulls it."),
    ("What is the extension of a spring?", "the increase in its length", ["its total length", "its original length", "its mass"], "Extension = stretched length − original length."),
    ("A spring is 10 cm long. With a load, it is 16 cm long. What is the extension?", "6 cm", ["16 cm", "26 cm", "10 cm"], "16 − 10 = 6 cm."),
    ("What happens if a spring is stretched too far?", "It may not return to its original length.", ["It becomes stronger.", "It shrinks.", "It turns into a magnet."], "It has been overstretched."),
    ("Which of these uses a compressed spring?", "a retractable pen", ["a measuring cylinder", "a thermometer", "a magnet"], "Pressing the button compresses the spring."),
    ("Why do mattresses have springs?", "The compressed springs push back and support our body.", ["Springs make the mattress lighter.", "Springs keep the mattress cold.", "Springs attract metal."], "Springs exert a force when compressed."),
    ("Which of these uses a stretched spring?", "a spring balance", ["a stapler's paper", "a glass cup", "a wooden ruler"], "The spring extends under the load."),
])
B5 = bank([
    ("Siti hung loads on a spring and measured the extension. Why did she use the same spring for all the loads?", "so that only the load affected the extension", ["to make the spring longer", "to save time", "to change the spring's material"], "Different springs stretch differently."),
    ("Ravi dropped a golf ball and a ping-pong ball of the same size from the same height. Which reached the ground first?", "almost at the same time, the golf ball very slightly earlier", ["the ping-pong ball, by a long time", "the golf ball, ten times faster", "neither fell"], "Gravity makes both fall; air resistance slows the light ball a little."),
    ("A spring balance reads 0 N with nothing on it and 8 N with a pail of sand. What is the weight of the sand and pail?", "8 N", ["0 N", "80 N", "8 kg"], "The reading is the weight."),
    ("Mei Ling added 2 N loads to a spring. The extension went 3 cm, 6 cm, 9 cm, then 15 cm. What most likely happened at the last load?", "The spring was overstretched.", ["The spring became stiffer.", "Gravity became weaker.", "She read the ruler correctly."], "The pattern broke: the spring no longer stretched evenly."),
    ("Why should a pupil read a spring balance at eye level?", "to read the scale accurately", ["to make the load lighter", "to stretch the spring", "to make the reading bigger"], "Reading from an angle gives errors."),
])


def body():
    think = ("<p><b>Gravitational force is the pull of the Earth on objects. Weight is the gravitational force on an object.</b></p>"
             "<ul><li>Weight is measured in newtons (N) with a spring balance. On Earth, 1 kg weighs about 10 N.</li>"
             "<li>A stretched or compressed spring exerts an <b>elastic spring force</b> back towards its original length.</li>"
             "<li><b>Extension</b> = stretched length − original length. A bigger load gives a bigger extension, until the spring is overstretched.</li></ul>")
    ex = [("A spring is 12 cm long. With a 3 N load it is 18 cm. What is the extension?", ["18 − 12"], "6 cm."),
          ("A 2 kg bag of rice: what is its weight on Earth?", ["About 10 N for every kg", "2 × 10"], "About 20 N.")]
    mist = ["Measuring weight in kilograms. Weight is a force, measured in newtons.",
            "Giving the total length instead of the extension.",
            "Thinking heavier objects fall much faster. Without air resistance, they fall at the same rate.",
            "Thinking gravity only acts on falling objects. It acts on everything all the time."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Gravitational force", B1 + GR.B1 + [(g_weight, 3), (FE.g_read, 3)]),
        ("Weight", [(g_weight, 4), (FE.g_read, 4), (GR.g_m, 4), (GR.g_moon, 2), (FO.g_name, 3), (g_spring, 3)]),
        ("Elastic spring force", B2 + [(g_spring, 8), (g_compare, 2), (FO.g_spring, 2)]),
        ("Spring experiments", [(g_spring, 8), (g_compare, 4), (FO.g_spring, 3), (GR.g_w, 3), (g_weight, 2)]),
        ("PSLE-style questions", B5 + GR.B5 + [(g_spring, 5), (g_compare, 2), (FO.g_spring, 2)]),
    ])
    make_sg(6, "gravitational-and-elastic-spring-force", 5, "Interactions", "Interaction of forces (Gravitational force and elastic spring force)",
            "Recognise that gravitational force is the pull of the Earth on objects and that the weight of an object is the gravitational force acting on it. "
            "Investigate the effect of a force on a spring: the extension of a spring increases as the load increases "
            "(summary of the MOE Primary Science Syllabus).",
            "Gravitational Force and Elastic Spring Force",
            "Primary 6 Science: Gravity and Spring Force Worksheets (PSLE Practice with Answers)",
            "Gravity and spring force",
            "Free Primary 6 science worksheets for Singapore pupils on gravitational force, weight in newtons, spring balances and the extension of springs. PSLE practice with answers.",
            "Gravity pulls; springs push or pull back.",
            "Weight is in newtons; extension grows with the load.",
            body(),
            [("What is the difference between mass and weight?", "Mass is the amount of matter in an object, in kilograms. Weight is the pull of gravity on it, a force in newtons."),
             ("How do I find the extension of a spring?", "Subtract the original length from the stretched length. For example, 16 cm − 10 cm = 6 cm."),
             ("What happens if a spring is overstretched?", "It may not go back to its original length, and it no longer stretches evenly with the load.")],
            sets)


if __name__ == "__main__":
    main()
