# -*- coding: utf-8 -*-
"""
Singapore Primary 6 science: Forces and their effects (Interactions)
  python tools/gen_sg_science_p6_forces_and_their_effects.py
A force is a push or a pull. A force can move a stationary object, speed up, slow down or stop a moving object,
change its direction of motion, or change its shape. Forces are measured in newtons (N) with a spring balance.
Contact and non-contact forces (magnetic and gravitational forces act at a distance); balanced and unbalanced forces.
UK Year 3 and Year 7 and US Grade 3 force questions are reused with Singapore names ("spring balance" for newton metre).
Wrong answers come from real mistakes: "a force is needed to keep an object moving at a steady speed",
"a still object has no forces on it", "only living things can exert forces", "forces only make things move".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use, upto

U = Unit(63603)
R = U.R
P = People(R)
REP = [(r"newton metre", "spring balance"), (r"\btoward\b", "towards"), (r"\bkids\b", "pupils"), (r"\bkid\b", "pupil")]
PP = use(U, "gen_uk_science_y3_pushes_pulls_and_surfaces", rep=REP, drop=["winter", "snow", "friction", "ice", "surface"])
BU = use(U, "gen_us_science_g3_balanced_and_unbalanced_forces", rep=REP)
FO = use(U, "gen_uk_science_y7_forces", rep=REP, drop=["upthrust", "tension", "Jupiter", "Mars", "joule", "resultant", "normal (reaction)", "g = "])

EFFECTS = ["It moves a stationary object.", "It makes a moving object speed up.", "It makes a moving object slow down or stop.",
           "It changes the direction of a moving object.", "It changes the shape of an object."]
SCENE = [("A pupil kicks a football that is lying still on the field.", 0), ("A pupil pushes a trolley that is standing still at FairPrice.", 0),
         ("A cyclist pedals harder on a straight road.", 1), ("A bus driver presses the accelerator.", 1), ("The wind blows a moving sailboat forward faster.", 1),
         ("A goalkeeper catches a ball flying towards the goal.", 2), ("A cyclist squeezes the brakes.", 2), ("A parachute opens behind a falling skydiver.", 2),
         ("A badminton player hits back a shuttlecock coming towards her.", 3), ("A pupil kicks a rolling ball sideways.", 3), ("A hockey player hits a moving ball towards the goal at an angle.", 3),
         ("A baker presses dough into a flat shape.", 4), ("A pupil squeezes a sponge.", 4), ("A pupil stretches a rubber band.", 4), ("A car hits a lamp post and its bonnet is dented.", 4),
         ("A pupil bends a plastic ruler.", 4)]


def g_eff():
    s, i = R.choice(SCENE)
    if not once(("ef", s)):
        return None
    return item("%s Which effect of a force does this show?" % s, EFFECTS[i], R.sample([x for j, x in enumerate(EFFECTS) if j != i], 3), EFFECTS[i])


def balance_svg(n, mx):
    """a spring balance: vertical scale 0..mx N, pointer at n"""
    from sg_sci import svg_wrap, rect, line, text, INK, RED
    top, bot, x = 30, 230, 70

    def y(v):
        return top + (bot - top) * v / float(mx)
    p = [rect(x - 22, top - 20, 76, bot - top + 40, fill="#f4f4f4", stroke=INK, rx=6), line(x + 16, 4, x + 16, top - 20, col=INK, w=3)]
    step = 1 if mx <= 10 else (5 if mx <= 50 else 10)
    v = 0
    while v <= mx:
        p.append(line(x - 2, y(v), x + 14, y(v), col=INK, w=1.5))
        p.append(text(x + 18, y(v) + 4, "%d" % v, fs=11, anchor="start"))
        v += step
    p.append(line(x - 18, y(n), x + 4, y(n), col=RED, w=4))
    p.append(line(x - 10, y(n), x - 10, bot + 30, col=INK, w=2))
    p.append(rect(x - 28, bot + 30, 36, 26, fill="#c9d6e8", stroke=INK, rx=3))
    p.append(text(x + 42, top - 6, "N", fs=12, anchor="start"))
    return svg_wrap(150, bot + 70, "".join(p), "spring balance")


def g_read():
    mx = R.choice([10, 50])
    step = 1 if mx == 10 else 5
    n = R.randrange(step, mx, step)
    if not once(("rd", mx, n)) or not once(("rdn",), 8):
        return None
    w = sorted({n + step, max(step, n - step), n * 10} - {n})
    if len(w) < 3:
        w = sorted({n + step, n + 2 * step, n * 10} - {n})
    obj = R.choice(["a pencil case", "an apple", "a bottle of water", "a packet of biscuits"] if mx == 10 else
                   (["a school bag", "a bag of rice", "a durian", "a pail of water"] if n >= 15 else ["a box of books", "a bunch of bananas"]))
    return item("<div class='qfig'>%s</div>%s hangs from the spring balance. What force does the spring balance show?" % (balance_svg(n, mx), obj.capitalize()),
                "%d N" % n, ["%d N" % v for v in w[:3]], "Read the scale at the red pointer. Force is measured in newtons (N).")


def g_net():
    a = R.randrange(10, 60, 5)
    b = R.randrange(10, 60, 5)
    if a == b:
        k = "bal"
    else:
        k = "unb"
    if not once(("nt", a, b)) or not once(("ntn", k), 5 if k == "unb" else 2):
        return None
    if k == "bal":
        return item("Two pupils push a box from opposite sides, each with a force of %d N. What happens to the box?" % a, "It stays still.",
                    ["It moves towards the first pupil.", "It moves towards the second pupil.", "It is lifted up."], "The forces are balanced.")
    big = "Siti" if a > b else "Ravi"
    other = "Ravi" if a > b else "Siti"
    return item("Siti pushes a box to the right with %d N. Ravi pushes it to the left with %d N. Which way does the box move?" % (a, b),
                "towards the %s" % ("right" if a > b else "left"), ["towards the %s" % ("left" if a > b else "right"), "It stays still.", "It moves upwards."],
                "The forces are unbalanced; the box moves in the direction of the bigger force (%s's push)." % big)


B1 = bank([
    ("What is a force?", "a push or a pull", ["a kind of energy", "the speed of an object", "a kind of matter"], "Forces can change how objects move or their shape."),
    ("What is the unit of force?", "the newton (N)", ["the kilogram (kg)", "the metre (m)", "the degree Celsius (°C)"], "It is named after Isaac Newton."),
    ("Which instrument is used to measure force?", "a spring balance", ["a thermometer", "a measuring cylinder", "a ruler"], "The spring stretches more when the force is bigger."),
    ("Which of these is NOT an effect of a force?", "It changes the colour of an object.", ["It changes the shape of an object.", "It changes the direction of an object.", "It makes an object speed up."], "Forces change motion or shape."),
    ("Which force acts on an object without touching it?", "gravitational force", ["frictional force", "the push of a hand", "the pull of a rope"], "Gravitational and magnetic forces act at a distance."),
    ("A book is lying still on a table. Which statement is correct?", "Forces act on it but they are balanced.", ["No forces act on it.", "Only gravity acts on it.", "It is moving very slowly."], "Gravity pulls it down; the table pushes it up."),
    ("Which of these is a pull?", "opening a drawer", ["kicking a ball", "pressing a lift button", "pushing a trolley"], "A pull moves something towards you."),
    ("Can a force change the shape of an object without moving it from place to place?", "Yes, for example squeezing a sponge.", ["No, forces only move objects.", "Only magnetic forces can.", "Only if the object is metal."], "Forces can change shape."),
])
B2 = bank([
    ("A ball rolls across a field and slowly stops. Which force made it stop?", "friction between the ball and the grass", ["gravity pushing it forward", "no force: it ran out of force", "magnetism"], "Friction acts against the motion."),
    ("Why does a football change direction when it hits a goalpost?", "The goalpost exerts a force on the ball.", ["The ball changes direction by itself.", "Gravity pushes it sideways.", "No force acts on it."], "A force can change the direction of motion."),
    ("A pupil holds a bag still in the air. Is she exerting a force?", "Yes. She pulls up on the bag to balance its weight.", ["No, because the bag is not moving.", "No, only gravity acts.", "Only if she lifts it higher."], "Balanced forces keep the bag still."),
    ("Which shows two forces acting on a moving bicycle?", "the cyclist's push on the pedals and friction from the road", ["only the cyclist's push", "only gravity", "no forces"], "Several forces can act at once."),
    ("Which force makes a dropped durian fall to the ground?", "gravitational force", ["frictional force", "magnetic force", "elastic spring force"], "The Earth pulls objects towards it."),
    ("Why does a stretched rubber band go back to its shape when released?", "It exerts an elastic force.", ["It loses all its force.", "Gravity pulls it back.", "Friction pushes it."], "Stretched elastic objects exert forces."),
    ("Which statement about forces is correct?", "A bigger force usually gives a bigger effect.", ["A bigger force gives a smaller effect.", "Forces only act on living things.", "Forces always make things speed up."], "Kicking harder sends the ball further."),
    ("A magnet pulls a steel paper clip across a table. What kind of force is this?", "a magnetic force, a non-contact force", ["a frictional force", "a contact push", "gravitational force"], "Magnets attract magnetic materials at a distance."),
])
B5 = bank([
    ("Siti hung a stone on a spring balance. It read 6 N. She lowered the stone into water and it read 4 N. What can she conclude?", "Water pushed up on the stone with a force of 2 N.", ["The stone lost 2 kg.", "Gravity stopped working.", "The spring balance broke."], "6 − 4 = 2 N."),
    ("Ravi pulled a toy cart with a spring balance. It read 3 N on a smooth floor and 7 N on carpet. Why?", "There is more friction on carpet.", ["The cart is heavier on carpet.", "Gravity is stronger on carpet.", "Carpet pushes the cart forward."], "Rougher surfaces give more friction."),
    ("Mei Ling kicked a ball with different forces and measured how far it went. What was she changing?", "the force of the kick", ["the size of the ball", "the place she kicked it", "the distance travelled"], "The distance is what she measured."),
    ("A pupil wants to compare forces fairly. Why should he use the same spring balance each time?", "so that the readings can be compared accurately", ["so that the force is smaller", "so that the spring breaks", "to make the object lighter"], "Different balances may read differently."),
    ("Why should a spring balance read 0 N before an object is hung on it?", "to make sure the reading is accurate", ["to make the spring stronger", "to make the object lighter", "so the spring does not stretch"], "Check the zero first."),
])


def body():
    think = ("<p><b>A force is a push or a pull. It is measured in newtons (N) with a spring balance.</b></p>"
             "<p>A force can:</p><ul><li>move a stationary object,</li><li>make a moving object speed up, slow down or stop,</li>"
             "<li>change the direction of a moving object,</li><li>change the shape of an object.</li></ul>"
             "<p>Gravitational and magnetic forces can act without touching. When forces are balanced, a still object stays still.</p>")
    ex = [("A pupil squeezes a ball of plasticine. What does the force do?", ["The plasticine is pressed", "Its shape changes"], "It changes the shape."),
          ("Siti pushes a box right with 30 N; Ravi pushes left with 20 N. Which way does it move?", ["The forces are unbalanced", "30 N is bigger"], "To the right.")]
    mist = ["Thinking a still object has no forces on it. The forces are balanced.",
            "Thinking a force is needed to keep a moving object going. Without friction it would keep moving.",
            "Thinking forces can only make things move. They can also change shape or direction.",
            "Measuring force in kilograms. Force is measured in newtons."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What is a force?", B1 + PP.B1 + [(PP.g_pp, 4), (PP.g_contact, 4)]),
        ("Effects of forces", [(g_eff, 10), (PP.g_do, 6), (PP.g_pp, 2), (g_read, 2)]),
        ("Measuring forces", [(g_read, 6), (FO.g_name, 4), (FO.g_bal, 3), (PP.g_contact, 3), (g_eff, 4)]),
        ("Balanced and unbalanced forces", B2 + [(BU.g_pic, 3), (BU.g_tug, 3), (BU.g_still, 2), (g_net, 4)]),
        ("PSLE-style questions", B5 + [(g_net, 4), (BU.g_change, 4), (g_eff, 3), (FO.g_spring, 2), (BU.g_tug, 2)]),
    ])
    make_sg(6, "forces-and-their-effects", 3, "Interactions", "Interaction of forces (Forces and their effects)",
            "Recognise that a force is a push or a pull and that it can move a stationary object, speed up, slow down or stop a moving object, "
            "change the direction of motion and change the shape of an object. Measure forces in newtons with a spring balance "
            "(summary of the MOE Primary Science Syllabus).",
            "Forces and Their Effects",
            "Primary 6 Science: Forces and Their Effects Worksheets (PSLE Practice with Answers)",
            "Forces and their effects",
            "Free Primary 6 science worksheets for Singapore pupils on forces: pushes and pulls, effects of forces, measuring forces with a spring balance, balanced and unbalanced forces. PSLE practice with answers.",
            "A force is a push or a pull.",
            "It can change speed, direction or shape.",
            body(),
            [("What can a force do?", "A force can move a still object, speed up, slow down or stop a moving object, change its direction and change its shape."),
             ("How do we measure force?", "With a spring balance. Force is measured in newtons (N)."),
             ("Are there forces on an object that is not moving?", "Yes. The forces are balanced. For example, gravity pulls a book down and the table pushes it up.")],
            sets)


if __name__ == "__main__":
    main()
