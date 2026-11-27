# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Frictional force (Interactions)
  python tools/gen_sg_science_p6_frictional_force.py
Friction is a contact force between two surfaces that are in contact; it opposes motion and acts in the opposite direction.
Rougher surfaces give more friction; friction produces heat and wears surfaces away. Friction can be useful (walking, braking,
writing, gripping) or unwanted (wear, heat, wasted energy); ways to increase it (treads, grips, sand) and reduce it
(lubricants, ball bearings, smooth surfaces, wheels). UK Year 3 and Year 5 friction tests are reused with "spring balance".
Wrong answers come from real mistakes: "friction acts in the direction of motion", "friction is always bad",
"smooth surfaces have more friction", "friction only happens when things are moving fast".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto

U = Unit(63604)
R = U.R
P = People(R)
REP = [(r"newton metre", "spring balance"), (r"\btoward\b", "towards")]
DROP = ["winter", "snow", "ice skat", "sledge"]
FR = use(U, "gen_uk_science_y5_friction", rep=REP, drop=DROP)
SU = use(U, "gen_uk_science_y3_pushes_pulls_and_surfaces", rep=REP, drop=DROP)

HELP = ["the soles of shoes gripping the floor when we walk", "bicycle brakes stopping the wheel", "a pencil leaving marks on paper",
        "tyres gripping a wet road", "our hands gripping a badminton racket", "a match being struck to light it", "a nail holding two pieces of wood together"]
HARM = ["the soles of shoes wearing out", "car tyres becoming smooth over time", "a door hinge squeaking and being hard to open",
        "the moving parts of a machine getting hot", "a cyclist having to pedal harder on a rough road", "carpet wearing thin where people walk"]


def g_use():
    k = R.choice(["h", "u"])
    a = R.choice(HELP if k == "h" else HARM)
    if not once(("us", a)):
        return None
    if k == "h":
        return item("In which of these is friction useful?", a, R.sample(HARM, 3), "Friction helps us grip, stop and write.")
    return item("In which of these is friction a problem?", a, R.sample(HELP, 3), "Friction wears surfaces away, produces heat and wastes energy.")


INC = ["adding treads to tyres", "putting rubber grips on handlebars", "spreading sand on a slippery path", "wearing studded football boots",
       "using a rubber mat in the bathroom", "putting chalk on a gymnast's hands"]
DEC = ["oiling a squeaky door hinge", "using ball bearings in a bicycle wheel", "putting wheels on a heavy suitcase", "polishing a playground slide",
       "waxing a surfboard's bottom", "spraying lubricant on a bicycle chain"]


def g_how():
    k = R.choice(["i", "d"])
    a = R.choice(INC if k == "i" else DEC)
    if not once(("hw", a)):
        return None
    if k == "i":
        return item("Which of these increases friction?", a, R.sample(DEC, 3), "Rough or grippy surfaces increase friction.")
    return item("Which of these reduces friction?", a, R.sample(INC, 3), "Lubricants, smooth surfaces, wheels and ball bearings reduce friction.")


def g_block():
    mats = {"glass": (2, 3), "smooth wood": (4, 6), "cardboard": (7, 9), "carpet": (11, 14), "sandpaper": (16, 20), "rubber mat": (21, 25)}
    pick = R.sample(sorted(mats), 4)
    f = [R.randint(*mats[m]) for m in pick]
    k = R.choice(["most", "least", "order", "var", "why"])
    if not once(("bk", k, tuple(sorted(pick)))) or not once(("bkn", k), {"most": 2, "order": 2}.get(k, 1)):
        return None
    tb = table(["Surface", "Force needed to pull the block (N)"], [[m, str(x)] for m, x in zip(pick, f)])
    q0 = "%s pulled the same wooden block across different surfaces with a spring balance.<br>%s" % (P.next()[0], tb)
    s = sorted(zip(f, pick))
    if k == "most":
        return item(q0 + "Which surface has the most friction?", s[-1][1], [m for _, m in s[:-1]], "The biggest force was needed to overcome the friction.")
    if k == "least":
        return item(q0 + "Which surface would be best for a slide?", s[0][1], [m for _, m in s[1:]], "It has the least friction, so things slide easily.")
    if k == "order":
        return item(q0 + "Which shows the surfaces from least to most friction?", ", ".join(m for _, m in s),
                    [", ".join(m for _, m in s[::-1]), ", ".join([s[1][1], s[0][1], s[2][1], s[3][1]]), ", ".join([s[0][1], s[2][1], s[1][1], s[3][1]])],
                    "A smaller pulling force means less friction.")
    if k == "var":
        return item(q0 + "Which variable was changed?", "the type of surface", ["the mass of the block", "the spring balance", "the force needed"], "Only the surface was changed; the force was measured.")
    return item(q0 + "Why was the same block used on every surface?", "so that only the surface affected the force needed", ["to make the block lighter", "to save time", "to make the force bigger"],
                "A heavier block would need more force.")


def g_mass():
    m = [100, 200, 300, 400]
    base = R.choice([2, 3])
    f = [base * (i + 1) for i in range(4)]
    k = R.choice(["trend", "read", "pred"])
    if not once(("ms", k)):
        return None
    tb = table(["Mass of block (g)", "Force needed to pull it on carpet (N)"], [[str(a), str(b)] for a, b in zip(m, f)])
    q0 = "%s pulled blocks of different mass across the same carpet.<br>%s" % (P.next()[0], tb)
    if k == "trend":
        return item(q0 + "What does the table show?", "The heavier the block, the more friction there is.", ["The heavier the block, the less friction there is.", "Mass does not affect friction.", "Carpet has no friction."],
                    "A heavier object presses harder on the surface.")
    if k == "read":
        return item(q0 + "What force was needed for the 300 g block?", "%d N" % f[2], ["%d N" % x for x in (f[1], f[3], 300)], "Read the row for 300 g.")
    return item(q0 + "Predict the force for a 500 g block.", "%d N" % (base * 5), ["%d N" % x for x in (f[3], base * 6, 500)], "The force goes up by %d N for every 100 g." % base)


B1 = bank([
    ("What is friction?", "a force between two surfaces in contact that opposes motion", ["a force that pulls objects towards the Earth", "a force that only magnets have", "a kind of energy"], "Friction acts where surfaces touch."),
    ("In which direction does friction act on a moving object?", "opposite to the direction of motion", ["in the same direction as the motion", "always upwards", "always towards the Earth"], "Friction slows things down."),
    ("Which surface usually has the most friction?", "a rough surface such as sandpaper", ["a smooth glass surface", "a polished floor", "an oiled metal plate"], "Rough surfaces grip more."),
    ("What does friction produce when two surfaces rub together?", "heat", ["light only", "magnetism", "electricity only"], "Rubbing hands together makes them warm."),
    ("Why do the soles of shoes wear out?", "Friction with the ground wears them away.", ["Gravity pulls them off.", "Air makes them thin.", "Water melts them."], "Friction causes wear."),
    ("Is friction a contact or a non-contact force?", "a contact force", ["a non-contact force", "it is not a force", "both"], "The surfaces must touch."),
    ("Can friction act on an object that is not moving?", "Yes. It can stop an object on a slope from sliding.", ["No, never.", "Only on ice.", "Only in water."], "A box resting on a ramp stays still because of friction."),
    ("Why do we slip on a wet floor?", "Water reduces the friction between our shoes and the floor.", ["Water increases friction.", "Gravity is stronger when wet.", "Wet floors push us."], "Less friction means less grip."),
])
B2 = bank([
    ("Why do bicycle tyres have treads?", "to increase friction so they grip the road", ["to reduce friction", "to make the tyre lighter", "to make the bicycle faster on ice"], "Treads give grip."),
    ("Why do we oil a bicycle chain?", "to reduce friction so the chain moves easily", ["to increase friction", "to make the chain heavier", "to make the chain rust"], "Oil is a lubricant."),
    ("Why are ball bearings used in wheels?", "They roll, which reduces friction.", ["They increase friction.", "They make the wheel heavier.", "They stop the wheel turning."], "Rolling has less friction than sliding."),
    ("Why is a heavy suitcase easier to move when it has wheels?", "Wheels reduce friction.", ["Wheels make it lighter.", "Wheels increase gravity.", "Wheels add a push."], "Rolling needs less force than sliding."),
    ("Why does a gymnast put chalk on her hands?", "to increase friction so her hands do not slip", ["to reduce friction", "to cool her hands", "to make her lighter"], "Chalk absorbs sweat and improves grip."),
    ("Why does a car need more distance to stop on a wet road?", "There is less friction between the tyres and the road.", ["There is more friction on wet roads.", "Wet roads are steeper.", "The car is heavier when wet."], "Less friction means less grip."),
    ("Why do we rub our hands together on a cold morning?", "Friction produces heat.", ["Friction makes cold.", "Our hands make light.", "It reduces gravity."], "Kinetic energy is converted into heat."),
    ("Which statement about friction is correct?", "Friction can be both useful and a problem.", ["Friction is always a problem.", "Friction is always useful.", "Friction only acts on wheels."], "It helps us walk but also wears things out."),
])
B5 = bank([
    ("Siti let a toy car run down a ramp onto different floor coverings. Which variable did she keep the same?", "the height of the ramp", ["the floor covering", "the distance the car travelled", "the friction"], "The starting height must be the same."),
    ("In Siti's test, the car travelled the shortest distance on carpet. What does this show?", "Carpet has the most friction.", ["Carpet has the least friction.", "Gravity is stronger on carpet.", "The car was lighter on carpet."], "More friction stops the car sooner."),
    ("Ravi pulled a block across sandpaper three times: 12 N, 13 N, 11 N. What is the average force?", "12 N", ["13 N", "36 N", "11 N"], "(12 + 13 + 11) ÷ 3 = 12 N."),
    ("Why did Ravi repeat the pull three times?", "to make the result more reliable", ["to wear out the block", "to change the surface", "to make the force bigger"], "An average reduces errors."),
    ("Mei Ling found that a block needed 6 N on dry wood and 3 N on wood with soapy water. What can she conclude?", "Soapy water reduces friction.", ["Soapy water increases friction.", "The block became heavier.", "Wood has no friction."], "The soap acts like a lubricant."),
])


def body():
    think = ("<p><b>Friction is a force between two surfaces in contact. It acts against the motion.</b></p>"
             "<ul><li>Rougher surfaces and heavier objects give more friction.</li>"
             "<li>Friction produces heat and wears surfaces away.</li>"
             "<li><b>Useful</b>: walking, braking, gripping, writing. <b>A problem</b>: wear, heat, wasted energy.</li>"
             "<li>Increase friction: treads, grips, rough surfaces. Reduce friction: oil, wheels, ball bearings, smooth surfaces.</li></ul>")
    ex = [("A box slides to the right. Which way does friction act?", ["Friction opposes motion"], "To the left."),
          ("Why do we oil a door hinge?", ["Oil is a lubricant", "It reduces friction"], "To reduce friction so it opens easily.")]
    mist = ["Thinking friction acts in the same direction as the motion.",
            "Thinking friction is always bad. We could not walk or brake without it.",
            "Thinking smooth surfaces have more friction.",
            "Changing the block and the surface at the same time in a friction test."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is friction?", B1 + FR.B1 + [(FR.g_dir, 4)]),
        ("Surfaces and friction", [(SU.g_surf, 6), (g_block, 5), (FR.g_dir, 3), (FR.g_ramp, 3), (g_mass, 3)]),
        ("Useful or a problem?", B2 + [(g_use, 6), (FR.g_use, 3), (g_how, 3)]),
        ("Increasing and reducing friction", [(g_how, 8), (FR.g_chg, 5), (g_use, 4), (FR.g_pull, 3)]),
        ("PSLE-style experiments", B5 + FR.B5 + SU.B5 + [(FR.g_pull, 3), (g_block, 3)]),
    ])
    make_sg(6, "frictional-force", 4, "Interactions", "Interaction of forces (Frictional force)",
            "Recognise that friction is a force that opposes motion between two surfaces in contact, and investigate the effect of different surfaces on friction. "
            "Recognise the advantages and disadvantages of friction and ways to increase or reduce it (summary of the MOE Primary Science Syllabus).",
            "Frictional Force",
            "Primary 6 Science: Frictional Force Worksheets (PSLE Practice with Answers)",
            "Frictional force",
            "Free Primary 6 science worksheets for Singapore pupils on friction: surfaces, direction of friction, advantages and disadvantages, increasing and reducing friction, and fair tests. PSLE practice with answers.",
            "Friction acts against motion.",
            "Rough surfaces give more friction; oil and wheels reduce it.",
            body(),
            [("What is frictional force?", "A force between two surfaces in contact. It acts in the opposite direction to the motion and slows things down."),
             ("Is friction useful?", "Yes. It lets us walk, grip things, write and stop bicycles. It can also be a problem because it wears things out and produces heat."),
             ("How can we reduce friction?", "Use lubricants such as oil, smooth surfaces, wheels or ball bearings.")],
            sets)


if __name__ == "__main__":
    main()
