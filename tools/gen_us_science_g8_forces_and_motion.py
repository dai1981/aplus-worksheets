# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Forces and Motion (MS-PS2-2)
  python tools/gen_us_science_g8_forces_and_motion.py
Plan an investigation to provide evidence that the change in an object's motion depends on the sum of the forces on
the object and the mass of the object. Net force in one dimension (newtons), balanced vs. unbalanced, Newton's first law
(inertia), Newton's second law as a relationship (a = F / m), one variable changed at a time.
Wrong answers come from real mistakes: "a moving object needs a net force to keep moving", "heavier objects speed up more
with the same push", "add forces in opposite directions".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, svg_wrap, rect, arrow, text, People, INK, BLUE, RED

U = Unit(80102)
R = U.R
P = People(R)
USED = {}


def once(key, n=3):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def fpic(fr, fl, obj="box"):
    W, H = 400, 100
    s = [rect(160, 30, 80, 44, "#f6dcb4", INK, 2), text(200, 57, obj, 13, weight=400)]
    if fr:
        s.append(arrow(242, 52, 242 + 10 + fr * 4, 52, BLUE, 4, 11) + text(250 + fr * 2, 44, "%d N" % fr, 13, col=BLUE))
    if fl:
        s.append(arrow(158, 52, 148 - fl * 4, 52, RED, 4, 11) + text(150 - fl * 2, 44, "%d N" % fl, 13, col=RED))
    return svg_wrap(W, H, "".join(s), "a %s with forces of %d N to the right and %d N to the left" % (obj, fr, fl))


def g_net():
    fr = R.choice(range(5, 36, 5))
    fl = R.choice([x for x in range(0, 36, 5) if x != fr] + [fr])
    obj = R.choice(["box", "cart", "sled", "crate", "wagon"])
    net = fr - fl
    who = P.next()[0]
    d = "to the right" if net > 0 else ("to the left" if net < 0 else "")
    ans = "%d N %s" % (abs(net), d) if net else "0 N (balanced)"
    w = ["%d N %s" % (fr + fl, "to the right"), "%d N %s" % (abs(net), "to the left" if net > 0 else "to the right") if net else "%d N to the right" % fr, "%d N to the right" % max(fr, fl)]
    w = [x for x in dict.fromkeys(w) if x != ans]
    if len(w) < 3:
        w.append("%d N to the left" % (fr + fl))
    return item(fig(fpic(fr, fl, obj)) + "%s's force diagram shows two forces on a %s. What is the net force?" % (who, obj), ans, w[:3],
                "Subtract forces in opposite directions: %d − %d = %d N." % (max(fr, fl), min(fr, fl), abs(net)) if net else "Equal and opposite forces add to zero.")


def g_motion():
    fr = R.choice(range(10, 41, 5))
    fl = R.choice([fr, fr - 5, fr + 5, fr - 10])
    if fl < 0:
        return None
    who = P.next()[0]
    state = R.choice(["at rest", "moving to the right at a steady speed"])
    pic = fig(fpic(fr, fl, "cart"))
    net = fr - fl
    if net == 0:
        a = "It stays at rest." if state == "at rest" else "It keeps moving right at the same speed."
        w = ["It speeds up to the right.", "It slows down and stops.", "It moves to the left."]
    elif net > 0:
        a = "It starts moving to the right." if state == "at rest" else "It speeds up to the right."
        w = ["It stays at rest." if state == "at rest" else "It keeps the same speed.", "It moves to the left.", "It stops right away."]
    else:
        a = "It starts moving to the left." if state == "at rest" else "It slows down."
        w = ["It speeds up to the right.", "It keeps the same speed." if state != "at rest" else "It stays at rest.", "It moves up."]
    return item(pic + "In %s's diagram, the cart is %s. What happens next?" % (who, state), a, w,
                "Balanced forces do not change motion; an unbalanced force changes speed or direction in the direction of the net force.")


def g_mass():
    F = R.choice([10, 20, 30, 40, 60])
    m1, m2 = R.sample([1, 2, 4, 5, 10], 2)
    if F % m1 or F % m2:
        return None
    who = P.next()[0]
    rows = [["%d kg" % m1, "%d N" % F, "%d m/s²" % (F // m1)], ["%d kg" % m2, "%d N" % F, "%d m/s²" % (F // m2)]]
    tab = table(["Mass of cart", "Net force", "Acceleration"], rows)
    k = R.choice(["which", "rule", "predict", "predict"])
    if k in ("which", "rule") and not once(k):
        return None
    small = min(m1, m2)
    if k == "which":
        return item(tab + "%s pushed two carts with the same net force. Which cart's motion changed more?" % who, "the %d kg cart" % small,
                    ["the %d kg cart" % max(m1, m2), "Both changed the same.", "Neither changed."], "With the same force, less mass means a bigger change in motion.")
    if k == "rule":
        return item(tab + "What relationship does %s's data show?" % who, "With the same force, a smaller mass speeds up more.", ["With the same force, a larger mass speeds up more.", "Mass has no effect.", "Force has no effect."],
                    "Acceleration = force ÷ mass.")
    m3 = R.choice([m for m in [1, 2, 4, 5, 10] if m not in (m1, m2) and F % m == 0] or [0])
    if not m3 or not once(("fm", m3, F), 1):
        return None
    return item(tab + "If %s pushes a %d kg cart with the same %d N, what will its acceleration be?" % (who, m3, F), "%d m/s²" % (F // m3),
                ["%d m/s²" % (F * m3), "%d m/s²" % F, "%d m/s²" % (F // m3 + 2)], "a = F ÷ m = %d ÷ %d = %d m/s²." % (F, m3, F // m3))


def g_force():
    m = R.choice([2, 4, 5, 10])
    Fs = [10, 20, 40]
    who = P.next()[0]
    rows = [["%d N" % f, "%s m/s²" % (("%g" % (f / m)))] for f in Fs]
    tab = table(["Net force on a %d kg cart" % m, "Acceleration"], rows)
    k = R.choice(["show", "var", "new", "new", "new"])
    if k in ("show", "var") and not once(k):
        return None
    if k == "new":
        f = R.choice([f for f in [5, 15, 25, 30, 50, 60, 80] if f % m == 0] or [0])
        if not f or not once(("fm", m, f), 1):
            return None
        return item(tab + "Using %s's data, predict the acceleration of the %d kg cart with a net force of %d N." % (who, m, f), "%d m/s²" % (f // m),
                    ["%d m/s²" % (f * m), "%d m/s²" % f, "%d m/s²" % (f // m + m)], "a = F ÷ m = %d ÷ %d = %d m/s²." % (f, m, f // m))
    if k == "show":
        return item(tab + "What does %s's data show?" % who, "A bigger net force causes a bigger change in motion.", ["A bigger force causes a smaller change.", "Force does not matter.", "Mass changes with force."],
                    "Doubling the force doubles the acceleration.")
    return item(tab + "In %s's investigation, what variable was changed on purpose?" % who, "the net force", ["the mass of the cart", "the acceleration", "the type of cart"],
                "The mass stayed the same; only the force was changed.")


B1 = bank([
    ("What is net force?", "the total of all the forces acting on an object", ["the largest single force", "the force of gravity only", "the mass of an object"], "Add forces in the same direction; subtract opposite ones."),
    ("What does Newton's first law say?", "An object keeps doing what it is doing unless an unbalanced force acts on it.", ["Moving objects always slow down by themselves.", "Heavier objects fall faster.", "For every action there is a reaction."],
     "This is inertia."),
    ("A hockey puck slides on ice and slowly stops. Why?", "Friction is an unbalanced force acting against its motion.", ["It runs out of force.", "Ice pulls it backward.", "Gravity pushes it sideways."],
     "Without friction, it would keep sliding."),
    ("What does Newton's second law say?", "Acceleration depends on the net force and the mass: a = F ÷ m.", ["Force equals speed.", "Mass has no effect on motion.", "Objects need force to keep moving."],
     "More force, more acceleration; more mass, less acceleration."),
    ("What unit is used for force?", "newton (N)", ["kilogram (kg)", "meter (m)", "second (s)"], "1 N gives 1 kg an acceleration of 1 m/s²."),
    ("A car moves at a steady 60 km/h on a straight road. What is the net force?", "zero; the forces are balanced", ["a large forward force", "a large backward force", "it cannot be known"],
     "Steady speed in a straight line means balanced forces."),
    ("Why is it harder to start pushing a full shopping cart than an empty one?", "The full cart has more mass, so it needs more force to change its motion.", ["The full cart has less inertia.", "Empty carts have no mass.", "Gravity is stronger on full carts."],
     "More mass, more inertia."),
    ("In an investigation of force and motion, why change only one variable?", "so you know which variable caused the change", ["to make the test faster", "because it is required by law", "so the data is random"],
     "Fair tests change one variable at a time."),
])
B5 = bank([
    ("Ava pulls a cart with a spring scale at 5 N, 10 N and 15 N. What should she keep the same?", "the cart's mass and the surface", ["the force", "nothing", "the speed only"], "Only the force should change."),
    ("Leo adds bricks to a cart and pulls with the same force each time. What is he testing?", "how mass affects the change in motion", ["how force affects motion", "how color affects motion", "how friction disappears"],
     "Mass is the variable he changes."),
    ("Mia's cart moves at a steady speed while she pulls with 4 N. What is the friction force?", "4 N backward", ["0 N", "8 N backward", "4 N forward"], "Steady speed means balanced forces."),
    ("A rocket's engines push up with 30,000 N and gravity pulls down with 20,000 N. What happens?", "It accelerates upward with a net force of 10,000 N.", ["It falls.", "It stays still.", "It moves sideways."],
     "30,000 − 20,000 = 10,000 N up."),
    ("Why do seat belts matter when a car stops suddenly?", "Your body keeps moving forward because of inertia until a force stops it.", ["The car pushes you backward.", "Gravity gets stronger.", "Seat belts make the car stop."],
     "Newton's first law."),
])


def body():
    think = ("<p>The <b>net force</b> is the total of all forces on an object. Add forces in the same direction; subtract forces in opposite directions.</p>"
             + "<div class='qfig'>" + fpic(25, 10, "cart") + "</div>"
             + "<p>25 N right − 10 N left = <b>15 N to the right</b>. Unbalanced forces change motion in the direction of the net force.</p>"
             "<p><b>Newton's first law</b>: with no net force, an object stays at rest or keeps moving at the same speed in a straight line (inertia). "
             "<b>Newton's second law</b>: the change in motion (acceleration) depends on net force and mass, <b>a = F ÷ m</b>. More force → more change; more mass → less change.</p>")
    ex = [("Forces of 30 N right and 30 N left act on a box at rest. What happens?", ["Net force = 0."], "It stays at rest."),
          ("The same 20 N pushes a 2 kg cart and a 4 kg cart. Which accelerates more?", ["a = F ÷ m", "20 ÷ 2 = 10; 20 ÷ 4 = 5"], "the 2 kg cart")]
    mist = ["Thinking a moving object needs a net force to keep moving.",
            "Adding forces that point in opposite directions.",
            "Thinking more mass speeds up more with the same push."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Net force", B1 + [(g_net, 12)]),
        ("Balanced and unbalanced forces", [(g_net, 8), (g_motion, 12)]),
        ("Force and acceleration", [(g_force, 8), (g_mass, 12)]),
        ("Mass and motion", [(g_mass, 10), (g_motion, 6), (g_force, 4)]),
        ("Planning investigations", B5 + [g_mass, g_force, g_net, g_motion]),
    ])
    make("grade-8", "forces-and-motion", 2, "MS-PS2-2",
         "Plan an investigation to provide evidence that the change in an object's motion depends on the sum of the forces on the object and the mass of the object.",
         "Forces and Motion",
         "Grade 8 Forces and Motion Worksheets: Net Force, Inertia and Newton's Second Law",
         "Forces and Motion",
         "Free middle school science worksheets on forces and motion (NGSS MS-PS2-2): net force diagrams, balanced and unbalanced forces, inertia, and how force and mass affect acceleration. 100 practice questions with answers.",
         "Motion changes when the net force is not zero.",
         "A bigger net force causes a bigger change in motion; a bigger mass causes a smaller change (a = F ÷ m).",
         body(),
         [("How do you find net force?", "Add forces that point in the same direction and subtract forces that point in opposite directions."),
          ("What happens when the forces on an object are balanced?", "The object keeps doing what it was doing: it stays at rest or keeps moving at a steady speed in a straight line."),
          ("How do force and mass affect motion?", "A larger net force causes a larger acceleration. A larger mass causes a smaller acceleration for the same force.")],
         sets)


if __name__ == "__main__":
    main()
