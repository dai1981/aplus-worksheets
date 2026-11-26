# -*- coding: utf-8 -*-
"""
UK Year 9 science (KS3 Physics): Work, Moments and Springs
  python tools/gen_uk_science_y9_work_and_moments.py
Work done = force × distance (in joules), moments as the turning effect of a force (moment = force × distance from the
pivot, in N m), the principle of moments and balanced see-saws, levers and simple machines (a bigger force but a smaller
movement), and forces stretching springs: extension directly proportional to force (Hooke's law) up to the limit.
Wrong answers come from real mistakes: "work = force + distance", "a longer spanner gives a smaller moment",
"the heavier child must sit further from the pivot", "a spring's length is the same as its extension".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
from sci_phys import uniq

U = Unit(61909)
R = U.R
P = People(R)
uk_sci.USED.clear()


def f(x):
    x = round(x, 2)
    return "{:,}".format(int(x)) if x == int(x) else "{:,}".format(x)


JOB = ["pushes a box", "pulls a sledge", "lifts a bag", "drags a suitcase", "pushes a trolley", "lifts a crate"]


def g_work():
    who = P.next()[0]
    j = R.choice(JOB)
    fo = R.choice([10, 20, 25, 40, 50, 80, 100, 150, 200])
    d = R.choice([0.5, 1, 1.5, 2, 3, 4, 5, 10])
    k = R.choice(["w", "w", "d"])
    if not once(("wo", j, fo, d, k)):
        return None
    w = fo * d
    if k == "w":
        g = "%s J" % f(w)
        return item("%s %s with a force of %s N for %s m. How much work is done?" % (who, j, f(fo), f(d)), g,
                    uniq(g, ["%s J" % f(fo + d), "%s J" % f(fo / d), "%s J" % f(fo), "%s J" % f(w * 10)]), "work done = force × distance = %s × %s = %s J." % (f(fo), f(d), f(w)))
    g = "%s m" % f(d)
    return item("%s does %s J of work moving a load with a force of %s N. How far does the load move?" % (who, f(w), f(fo)), g,
                uniq(g, ["%s m" % f(w * fo), "%s m" % f(w - fo) if w > fo else "%s m" % f(d * 2), "%s m" % f(fo), "%s m" % f(d * 10)]), "distance = work ÷ force = %s ÷ %s." % (f(w), f(fo)))


def g_moment():
    fo = R.choice([5, 10, 20, 25, 30, 40, 50, 60])
    d = R.choice([0.1, 0.2, 0.25, 0.3, 0.5, 1, 1.5, 2])
    o = R.choice(["a spanner", "a door handle", "a crowbar", "a wheelbarrow handle", "a lever"])
    if (o in ("a spanner", "a door handle") and d > 0.5) or not once(("mo", fo, d)):
        return None
    m = fo * d
    g = "%s N m" % f(m)
    return item("A force of %s N is applied to %s %s m from the pivot. What is the moment?" % (f(fo), o, f(d)), g,
                uniq(g, ["%s N m" % f(fo + d), "%s N m" % f(fo / d), "%s N m" % f(fo), "%s N m" % f(m * 10)]), "moment = force × distance from pivot = %s × %s." % (f(fo), f(d)))


def g_bal():
    a, b = P.next()[0], P.next()[0]
    w1 = R.choice([300, 400, 450, 500, 600])
    d1 = R.choice([1, 1.5, 2, 2.5, 3])
    w2 = R.choice([200, 250, 300, 400, 500, 600, 750])
    d2 = w1 * d1 / w2
    if w2 == w1 or d2 > 4 or d2 * 100 != int(d2 * 100) or not once(("ba", w1, d1, w2)):
        return None
    g = "%s m" % f(d2)
    return item("%s (weight %d N) sits %s m from the pivot of a see-saw. %s weighs %d N. How far from the pivot on the other side must %s sit to balance it?" % (a, w1, f(d1), b, w2, b), g,
                uniq(g, ["%s m" % f(d1), "%s m" % f(w2 * d1 / w1), "%s m" % f(d1 + 1), "%s m" % f(round(w1 / w2, 2))]),
                "Balanced: %d × %s = %d × d, so d = %s m. The lighter person sits further away." % (w1, f(d1), w2, f(d2)))


def g_hooke():
    who = P.next()[0]
    per = R.choice([1, 2, 3, 4, 5])
    nat = R.choice([5, 6, 8, 10, 12])
    forces = [0, 1, 2, 3, 4]
    ext = [x * per for x in forces]
    k = R.choice(["ext", "len", "pred", "pattern", "limit"])
    if not once(("ho", per, nat, k)) or not once(("ho", k), 2 if k in ("pattern", "limit") else 9):
        return None
    tab = table(["Force (N)", "Length of spring (cm)"], [[str(x), str(nat + e)] for x, e in zip(forces, ext)])
    intro = tab + "%s hung weights on a spring. " % who
    if k == "ext":
        g = "%d cm" % ext[3]
        return item(intro + "What is the extension when the force is 3 N?", g, uniq(g, ["%d cm" % (nat + ext[3]), "%d cm" % nat, "%d cm" % ext[2], "%d cm" % (ext[3] + 1)]), "extension = %d − %d = %d cm." % (nat + ext[3], nat, ext[3]))
    if k == "len":
        g = "%d cm" % nat
        return item(intro + "What is the natural (unstretched) length of the spring?", g, uniq(g, ["%d cm" % (nat + per), "0 cm", "%d cm" % per, "%d cm" % (nat + ext[4])]), "The length with no force.")
    if k == "pred":
        g = "%d cm" % (nat + 6 * per)
        return item(intro + "If the pattern continues, what will the length be with a force of 6 N?", g, uniq(g, ["%d cm" % (6 * per), "%d cm" % (nat + 5 * per), "%d cm" % (nat * 6), "%d cm" % (nat + 6)]), "Extension 6 × %d = %d cm, plus %d cm." % (per, 6 * per, nat))
    if k == "pattern":
        return item(intro + "What does the data show?", "The extension is directly proportional to the force.", ["The length doubles each time.", "The spring gets shorter.", "Force has no effect."], "Hooke's law.")
    return item("What happens if a spring is stretched past its limit of proportionality?", "It no longer obeys Hooke's law and may not return to its original length.", ["It gets shorter.", "It becomes a magnet.", "Nothing changes."], "Permanently stretched.")


B1 = bank([
    ("What is work done?", "the energy transferred when a force moves an object", ["the time taken for a job", "the mass of an object", "the force with no movement"], "Measured in joules."),
    ("Is work done when you push a wall that does not move?", "No, because the wall does not move.", ["Yes, lots of work.", "Yes, if you push hard.", "Only if it is a heavy wall."], "No distance moved."),
    ("What is a moment?", "the turning effect of a force", ["a short time", "a force in a straight line", "the mass of a lever"], "moment = force × distance."),
    ("Why is it easier to undo a nut with a long spanner?", "The longer distance gives a bigger moment for the same force.", ["A long spanner is lighter.", "It reduces the moment.", "It makes the nut smaller."], "Moment = force × distance."),
])
B5 = bank([
    ("What does a simple machine such as a lever do?", "It lets a small force move a large load, but the small force moves further.", ["It creates energy.", "It makes the load lighter.", "It reduces work to zero."], "Bigger force, smaller movement."),
    ("Why is a door handle placed far from the hinges?", "A larger distance gives a bigger moment, so it is easier to open.", ["It looks better.", "The hinge is weak.", "To make it harder."], "Moments."),
    ("What is the principle of moments?", "When balanced, the clockwise moments equal the anticlockwise moments.", ["All forces are equal.", "The pivot moves.", "Moments always add to zero force."], "Balance."),
    ("What is the difference between a spring's length and its extension?", "Extension is the increase in length from the natural length.", ["They are the same.", "Extension is the natural length.", "Length is always smaller."], "Subtract the natural length."),
    ("Why do springs in a car's suspension get squashed when people get in?", "The extra weight is a force that compresses them.", ["They get colder.", "The engine starts.", "Springs shrink with age."], "Forces deform objects."),
])


def body():
    think = ("<p><b>Forces can do work, turn things and stretch things.</b></p>"
             "<ul><li>work done (J) = force (N) × distance moved (m).</li>"
             "<li>moment (N m) = force (N) × distance from the pivot (m). Balanced: clockwise moments = anticlockwise moments.</li>"
             "<li>A spring's extension is proportional to the force (Hooke's law), up to its limit.</li></ul>")
    ex = [("50 N pushes 4 m. Work?", ["50 × 4"], "200 J"),
          ("20 N at 0.5 m from a pivot. Moment?", ["20 × 0.5"], "10 N m")]
    mist = ["Adding force and distance instead of multiplying.", "Thinking the heavier person sits further from the pivot.", "Mixing up length and extension."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Work done", B1[:2] + [(g_work, 18)]),
        ("Moments", B1[2:] + [(g_moment, 18)]),
        ("Balancing", [(g_bal, 16), (g_moment, 4)]),
        ("Springs", [(g_hooke, 16), (g_work, 4)]),
        ("Levers and machines", B5 + [(g_bal, 5), (g_hooke, 4), (g_moment, 3), (g_work, 3)]),
    ])
    make_ks3(9, "work-and-moments", 9, "Physics", "Forces",
             "Forces as pushes or pulls, arising from the interaction between two objects; using force arrows in diagrams; moment as the turning effect of a force; forces: associated with deforming objects; stretching and squashing – springs; with rubbing and friction between surfaces; forces measured in newtons, measurements of stretch or compression as force is changed; force-extension linear relation; Hooke's Law as a special case; work done and energy changes on deformation; simple machines give bigger force but at the expense of smaller movement (and vice versa): product of force and displacement unchanged.",
             "Work, Moments and Springs",
             "Year 9 Science: Work, Moments and Springs Worksheets (Levers, Hooke's Law)",
             "Work and Moments",
             "Free Year 9 science worksheets on work done, moments, balancing see-saws, levers and simple machines, and stretching springs with Hooke's law. 100 questions with answers.",
             "moment = force × distance from the pivot",
             "Work done = force × distance; extension is proportional to force.",
             body(),
             [("How do you calculate work done?", "Multiply the force by the distance moved in the direction of the force: work done = force × distance. The unit is the joule."),
              ("How do you balance a see-saw?", "The clockwise moment must equal the anticlockwise moment. A lighter person must sit further from the pivot than a heavier one."),
              ("What is Hooke's law?", "The extension of a spring is directly proportional to the force on it, as long as it is not stretched past its limit of proportionality.")],
             sets)


if __name__ == "__main__":
    main()
