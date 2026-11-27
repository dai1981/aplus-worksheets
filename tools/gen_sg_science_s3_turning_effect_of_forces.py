# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 4: Turning Effect of Forces
  python tools/gen_sg_science_s3_turning_effect_of_forces.py
Moment of a force = force × perpendicular distance from the pivot (N m), the principle of moments for a body in equilibrium,
balancing beams and see-saws (including the weight of a uniform beam acting at its centre), centre of gravity and stability.
UK moment makers are reused (Singapore names); beam questions draw their own SVG.
Wrong answers come from real mistakes: "moment = force ÷ distance", "using the distance along a slanting line instead of the
perpendicular distance", "forgetting to change cm into m", "a lower centre of gravity makes an object less stable".
"""
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, fig, ex
from sci_common import svg_wrap, text, line, rect, BLUE, RED, INK

LV, SUBJ, SORT = 3, "Physics", 4
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex

uk_mom = src("gen_uk_science_y9_work_and_moments", "g_moment")
uk_bal = src("gen_uk_science_y9_work_and_moments", "g_bal")


def beam_svg(left, right, L=2.0):
    """left/right: [(distance from pivot in m, label)]; pivot in the middle of a beam of length L"""
    W, H = 440, 165
    x0, y = 220, 70
    sc = 190 / (L / 2)
    s = [rect(x0 - 200, y - 6, 400, 12, fill="#e8d9b5", sw=1.5),
         "<path d='M%d %d L%d %d L%d %d Z' fill='#888'/>" % (x0, y + 6, x0 - 16, y + 34, x0 + 16, y + 34)]
    for side, items in ((-1, left), (1, right)):
        for d, lab in items:
            x = x0 + side * d * sc
            s.append(line(x, y - 6, x, y - 34, col=RED, w=2.5) + "<path d='M%.1f %d L%.1f %d L%.1f %d Z' fill='%s'/>" % (x - 6, y - 14, x + 6, y - 14, x, y - 4, RED))
            s.append(text(x, y - 40, lab, fs=14, col=RED))
            s.append(line(x0, y + 46 + (12 if side > 0 else 0), x, y + 46 + (12 if side > 0 else 0), col=BLUE, w=1.5) + text((x0 + x) / 2, y + 42 + (12 if side > 0 else 0), N(d) + " m", fs=12, col=BLUE, weight=400))
    s.append(text(x0, y + 82, "pivot", fs=12, weight=400))
    return svg_wrap(W, H, "".join(s), "beam balanced on a pivot").replace("<svg ", "<svg data-pf='lg' ", 1)


def g_moment():
    k = R.choice(["M", "F", "d", "cm"])
    F = R.choice([5, 8, 10, 12, 20, 25, 40, 50, 60, 80, 150, 200])
    d = R.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.2, 1.5, 2])
    M = F * d
    what = R.choice(["a spanner", "a door handle", "a crowbar", "a wheelbarrow handle", "a tap handle"])
    if k == "M":
        return nq("A force of %d N acts at right angles on %s, %s m from the pivot. What is the moment of the force?" % (F, what, N(d)), M, [F / d, d / F, F + d], " N m",
                  "Moment = F × d = %d × %s = %s N m." % (F, N(d), N(M)))
    if k == "F":
        return nq("A moment of %s N m is needed to turn %s. The force is applied %s m from the pivot. What force is needed?" % (N(M), what, N(d)), F, [M * d, d / M, M - d], " N",
                  "F = moment ÷ d = %s ÷ %s = %d N." % (N(M), N(d), F))
    if k == "d":
        return nq("A force of %d N gives a moment of %s N m about a pivot. How far from the pivot does it act?" % (F, N(M)), d, [M * F, F / M, M - F if M > F else F - M], " m",
                  "d = moment ÷ F = %s ÷ %d = %s m." % (N(M), F, N(d)))
    dc = int(round(d * 100))
    return nq("A force of %d N acts at right angles to %s at a distance of %d cm from the pivot. What is the moment in N m?" % (F, what, dc), M, [F * dc, F * dc / 10, F / d], " N m",
              "Change cm to m first: %d cm = %s m. Moment = %d × %s = %s N m." % (dc, N(d), F, N(d), N(M)))


def g_beam():
    """two weights on a light beam: find the unknown force or distance"""
    L = 2.0
    while True:
        d1 = R.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0])
        F1 = R.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
        d2 = R.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0])
        F2 = F1 * d1 / d2
        if d1 != d2 and F2 == int(F2) and F2 <= 50:
            break
    k = R.choice(["F", "d"])
    if k == "F":
        svg = beam_svg([(d1, "%d N" % F1)], [(d2, "F")], L)
        return nq(fig(svg) + "The light beam is balanced. What is the force F?", int(F2), [F1 * d2 / d1, F1, F1 * d1 * d2], " N",
                  "Clockwise moment = anticlockwise moment: F × %s = %d × %s, so F = %d N." % (N(d2), F1, N(d1), int(F2)))
    svg = beam_svg([(d1, "%d N" % F1)], [(d2, "%d N" % F2)], L)
    svg = svg.replace(">%s m</text>" % N(d2), ">x</text>")
    return nq(fig(svg) + "The light beam is balanced. What is the distance x of the %d N weight from the pivot?" % F2, d2, [d1 * F2 / F1, d1, F1 * d1], " m",
              "%d × x = %d × %s, so x = %s ÷ %d = %s m." % (F2, F1, N(d1), N(F1 * d1), F2, N(d2)))


def g_seesaw():
    a, b = R.sample(P.pool, 2)
    wa = R.choice([300, 350, 400, 450, 500, 550, 600])
    da = R.choice([1.0, 1.2, 1.5, 1.6, 2.0])
    wb = R.choice([x for x in (300, 400, 450, 500, 600, 750, 800) if x != wa])
    db = wa * da / wb
    if db > 2.5 or abs(db * 100 - round(db * 100)) > 1e-9:
        return None
    return nq("%s (weight %d N) sits %s m from the pivot of a see-saw. Where must %s (weight %d N) sit on the other side to balance it?" % (a[0], wa, N(da), b[0], wb), db,
              [wb * da / wa, da, wa / wb], " m", "%d × %s = %d × d, so d = %s ÷ %d = %s m." % (wa, N(da), wb, N(wa * da), wb, N(db)))


def g_uniform():
    """uniform beam pivoted off-centre, balanced by a weight hanging from the short end"""
    L = R.choice([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    p = round(R.choice([0.1, 0.2, 0.25, 0.3, 0.4]) * L, 2)
    Wb = R.choice([20, 30, 40, 50, 60, 80, 100, 120, 150, 200])
    dW = round(L / 2 - p, 2)
    F = Wb * dW / p
    if F != int(F) or F > 1000:
        return None
    what = "plank" if L >= 3 else "beam"
    if R.random() < 0.5:
        return nq("A uniform %s %s m long weighs %d N. It is pivoted %s m from one end. What weight must hang from that end to keep it horizontal?" % (what, N(L), Wb, N(p)),
                  int(F), [Wb * p / dW, Wb, Wb * L / p], " N",
                  "The %s's weight acts at its centre, %s m from the pivot. W × %s = %d × %s, so W = %d N." % (what, N(dW), N(p), Wb, N(dW), int(F)))
    return nq("A uniform %s %s m long is pivoted %s m from one end. It balances horizontally when a %d N weight hangs from that end. What is the weight of the %s?" % (what, N(L), N(p), int(F), what),
              Wb, [int(F) * dW / p, int(F), int(F) * p], " N",
              "Its weight W acts at the centre, %s m from the pivot. W × %s = %d × %s, so W = %d N." % (N(dW), N(dW), int(F), N(p), Wb))


STAB = [("a racing car with a low, wide body", "very stable: low centre of gravity and wide base"),
        ("a bus with many passengers standing on the upper deck", "less stable: the centre of gravity is raised"),
        ("a tall, narrow vase", "less stable: high centre of gravity and narrow base"),
        ("a table lamp with a heavy base", "more stable: the heavy base lowers the centre of gravity"),
        ("a cone standing on its base", "stable: low centre of gravity and wide base"),
        ("a cone balanced on its tip", "unstable: any small tilt makes it fall")]
g_stab = rows(R, STAB, "Which statement best describes the stability of %s?")

POOL1 = pool(R, [
    ("What is the moment of a force?", "the force × the perpendicular distance from the pivot to the line of action of the force", ["the force × the time it acts", "the force ÷ the distance from the pivot", "the force × the speed"], "Moment is measured in N m."),
    ("What is the SI unit of moment?", "N m", ["N/m", "J/s", "kg m"], "Newton metre."),
    ("State the principle of moments.", "For a body in equilibrium, the sum of clockwise moments about any point equals the sum of anticlockwise moments about that point.",
     ["The forces on each side are always equal.", "The heavier side always goes down.", "Moments only act on moving objects."], "Also, the resultant force must be zero."),
    ("Why is a door handle placed far from the hinges?", "A larger distance gives a larger moment for the same force.", ["It looks better.", "It reduces the door's weight.", "It makes the moment smaller."], "Moment = F × d."),
    ("Why is a long spanner easier to use than a short one?", "The same force gives a larger moment because the distance is larger.", ["It is lighter.", "It reduces friction.", "It needs a larger force."], "A longer lever arm gives more turning effect."),
    ("What is the centre of gravity of an object?", "the point where the whole weight of the object appears to act", ["the middle of its base", "the heaviest part of it", "the point where it touches the ground"], "For a uniform object it is at the centre."),
    ("How can you find the centre of gravity of a flat irregular card?", "Hang it freely from two points and draw a plumb line from each; the lines cross at the centre of gravity.", ["Weigh it twice.", "Measure its longest side and halve it.", "Balance it on a spring balance."], "The plumb-line method."),
    ("What two conditions must be met for an object to be in equilibrium?", "The resultant force is zero and the resultant moment is zero.", ["Only the forces must balance.", "Only the moments must balance.", "It must be at the same height."], "No acceleration and no turning."),
    ("Where does the weight of a uniform metre rule act?", "at the 50 cm mark", ["at the 0 cm mark", "at the 100 cm mark", "at the 25 cm mark"], "At its centre."),
    ("Which change makes an object more stable?", "lowering its centre of gravity and widening its base", ["raising its centre of gravity", "making its base narrower", "adding weight to the top"], "The weight's line of action stays inside the base for a larger tilt."),
])
POOL5 = pool(R, [
    ("A 30 N force pushes a door 0.8 m from the hinges at an angle, not at right angles. Why is the moment less than 24 N m?", "The perpendicular distance from the hinge to the line of the force is less than 0.8 m.",
     ["The force is smaller.", "Moments do not depend on angle.", "The door is heavier."], "Only the perpendicular distance counts."),
    ("When does a tilted object topple over?", "when the line of action of its weight falls outside its base", ["as soon as it is tilted", "when its weight increases", "when its base is wide"], "The weight then gives a moment that turns it further."),
    ("Why do double-decker buses carry heavy items low down?", "to keep the centre of gravity low so the bus is stable when it leans", ["to make the bus faster", "to reduce friction", "to increase the moment of the driver"], "A low centre of gravity resists toppling."),
    ("A uniform 2.0 m plank weighs 80 N and rests on a pivot at its centre. What weight at one end keeps it balanced?", "0 N: it already balances", ["80 N", "40 N", "160 N"], "Its weight acts through the pivot, so it gives no moment."),
    ("A wheelbarrow carries a 400 N load 0.5 m from the wheel. The handles are 1.6 m from the wheel. What upward force at the handles lifts it? (ignore the barrow's weight)", "125 N",
     ["400 N", "1280 N", "200 N"], "F × 1.6 = 400 × 0.5, so F = 125 N."),
    ("A pair of scissors cuts card more easily near the pivot. Why?", "For the same force at the handles, the force on the card is larger near the pivot.", ["The blades are sharper there.", "There is less friction there.", "The moment is smaller there."], "Moment at the handle = moment at the card."),
    ("A beam is in equilibrium. The anticlockwise moment about the pivot is 45 N m. What is the clockwise moment?", "45 N m", ["0 N m", "90 N m", "22.5 N m"], "Principle of moments."),
    ("Two children of equal weight sit on a see-saw. One sits 2 m from the pivot. Where must the other sit to balance?", "2 m from the pivot on the other side", ["1 m on the other side", "4 m on the other side", "at the pivot"], "Equal weights need equal distances."),
    ("A tall bookshelf is fixed to the wall with a bracket. Why?", "It has a high centre of gravity and could topple if pulled.", ["To make it lighter.", "To lower its mass.", "To increase its base area."], "The bracket stops it turning."),
    ("A 12 N force at 0.25 m from a pivot balances a force F at 0.75 m on the other side. What is F?", "4 N", ["36 N", "3 N", "12 N"], "F × 0.75 = 12 × 0.25 = 3 N m, so F = 4 N."),
])


def main():
    sets = U.sets([
        ("Moment of a force", [POOL1, (g_moment, 10), (uk_mom, 4)]),
        ("Principle of moments", [(g_beam, 8), (g_seesaw, 6), (uk_bal, 4), POOL1]),
        ("Calculating moments", [(g_moment, 7), (g_beam, 5), (g_uniform, 5), (uk_mom, 3)]),
        ("Centre of gravity and stability", [(g_stab, 6), POOL1, (POOL5, 6), (g_uniform, 3)]),
        ("Exam-style questions", [(POOL5, 9), (g_uniform, 4), (g_seesaw, 3), (g_beam, 4)]),
    ])
    make_ol(LV, SUBJ, "turning-effect-of-forces", SORT, "Turning Effect of Forces",
            "Describe the moment of a force in terms of its turning effect and relate this to everyday examples; recall and apply moment = force × perpendicular distance "
            "from the pivot; state the principle of moments for a body in equilibrium and apply it to new situations; show understanding that the weight of a body may be "
            "taken as acting at its centre of gravity; describe qualitatively the effect of the position of the centre of gravity on the stability of objects (summary of "
            "the Singapore-Cambridge O-Level Physics 6091 syllabus).",
            "Turning Effect of Forces", "Moments",
            "Free Secondary 3 O-Level Physics worksheets on the turning effect of forces: moments, the principle of moments, balanced beams and see-saws, centre of gravity "
            "and stability. 100 questions with answers.",
            "Moment = force × perpendicular distance", "In equilibrium: clockwise moments = anticlockwise moments.",
            "<p><b>A moment is the turning effect of a force.</b></p><ul>"
            "<li>Moment = F × d, where d is the perpendicular distance from the pivot to the line of the force (N m). Change cm into m first.</li>"
            "<li>Principle of moments: in equilibrium, total clockwise moment = total anticlockwise moment about any point, and the resultant force is zero.</li>"
            "<li>A uniform object's weight acts at its centre (its centre of gravity). A low centre of gravity and a wide base make an object stable.</li></ul>",
            [("40 N at 0.3 m from a pivot balances F at 0.6 m. F?", ["F × 0.6 = 40 × 0.3 = 12"], "20 N"),
             ("A 15 N force acts 20 cm from a nut. Moment?", ["20 cm = 0.20 m", "15 × 0.20"], "3 N m")],
            ["Dividing force by distance. Moment = force × distance.", "Forgetting to change cm into m when the answer is in N m.",
             "Using the slanting distance instead of the perpendicular distance.", "Forgetting the weight of a uniform beam, which acts at its centre."],
            [("How do you use the principle of moments?", "Take moments about the pivot. Add all the clockwise moments and all the anticlockwise moments, set them equal and solve for the unknown."),
             ("What makes an object stable?", "A low centre of gravity and a wide base, so the line of action of the weight stays inside the base when it is tilted."),
             ("Where does the weight of a uniform beam act?", "At its centre. Include it as a force at the middle of the beam when you take moments.")],
            sets)


if __name__ == "__main__":
    main()
