# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Balanced and Unbalanced Forces (3-PS2-1)
  python tools/gen_us_science_g3_balanced_and_unbalanced_forces.py
A force is a push or a pull. Balanced forces (equal and opposite) do not change an object's motion;
unbalanced forces make it start, stop, speed up, slow down or change direction.
Assessment boundary: qualitative only (equal / not equal; arrows of the same or different length),
one direction (left-right or up-down).
Wrong answers come from real mistakes: "balanced forces mean no forces", "a still object has no forces",
"the object moves toward the smaller force".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, line, text, arrow, circle, People, INK, BLUE, RED

U = Unit(30101)
R = U.R
P = People(R)
OBJ = ["box", "wagon", "desk", "sled", "toy car", "crate", "cart", "chair"]


def force_pic(left, right, obj="box", label=None):
    """Arrows pushing/pulling on a box: left = length of arrow pointing left, right = arrow pointing right (in units)."""
    W, H = 380, 110
    bx, by, bw, bh = 150, 35, 80, 50
    s = [line(10, by + bh, W - 10, by + bh, INK, 2), rect(bx, by, bw, bh, "#f6dcb4", INK, 2), text(bx + bw / 2, by + bh / 2 + 5, obj, 13, weight=400)]
    u = 22
    if right:
        s.append(arrow(bx + bw + 4, by + bh / 2, bx + bw + 18 + right * 20, by + bh / 2, BLUE, 4, 12))
    if left:
        s.append(arrow(bx - 4, by + bh / 2, bx - 18 - left * 20, by + bh / 2, RED, 4, 12))
    return svg_wrap(W, H, "".join(s), label or "a %s with force arrows" % obj)


def g_pic():
    obj = R.choice(OBJ)
    a = R.randint(1, 5)
    k = R.choice(["bal", "unbal"])
    b = a if k == "bal" else R.choice([x for x in range(1, 6) if x != a])
    pic = fig(force_pic(a, b, obj))
    q = R.choice(["kind", "move"])
    if q == "kind":
        if a == b:
            return item(pic + "Two forces act on a %s. The arrows are the same length. Are the forces balanced or unbalanced?" % obj, "balanced",
                        ["unbalanced", "There are no forces.", "Only the right force counts."], "Equal forces in opposite directions are balanced.")
        return item(pic + "Two forces act on a %s that is at rest. One arrow is longer. Are the forces balanced or unbalanced?" % obj, "unbalanced",
                    ["balanced", "There are no forces.", "They cancel each other out."], "The forces are not equal, so they are unbalanced.")
    if a == b:
        return item(pic + "The %s is at rest. What will happen?" % obj, "It will stay still.", ["It will move to the right.", "It will move to the left.", "It will move up."],
                    "Balanced forces do not change the motion of an object at rest.")
    d = "right" if b > a else "left"
    o = "left" if d == "right" else "right"
    return item(pic + "The %s is at rest. The arrows show two forces. What will happen?" % obj, "It will start to move to the %s." % d,
                ["It will start to move to the %s." % o, "It will stay still.", "It will move up into the air."],
                "The bigger force points to the %s, so the forces are unbalanced and the %s moves that way." % (d, obj))


def g_tug():
    a = R.randint(2, 6)
    b = R.choice([a] * 2 + [x for x in range(2, 7) if x != a])
    p = P.next()
    team1, team2 = R.sample(["Red Team", "Blue Team", "Green Team", "Gold Team"], 2)
    q = "In a tug-of-war, the %s has %d kids and the %s has %d kids. Every kid pulls equally hard. What happens to the rope?" % (team1, a, team2, b)
    if a == b:
        return item(q, "It does not move, because the pulls are balanced.", ["It moves toward the %s." % team1, "It moves toward the %s." % team2, "It breaks because there are no forces."],
                    "Equal pulls in opposite directions are balanced forces.")
    win = team1 if a > b else team2
    lose = team2 if win == team1 else team1
    return item(q, "It moves toward the %s." % win, ["It moves toward the %s." % lose, "It does not move.", "It moves straight up."],
                "The %s pulls with more force, so the forces are unbalanced." % win)


def g_change():
    rows = [("A soccer ball is sitting still. A player kicks it.", "It starts moving.", "unbalanced"),
            ("A rolling ball hits a wall.", "It stops or changes direction.", "unbalanced"),
            ("A book rests on a table.", "It stays still.", "balanced"),
            ("A wagon rolls on grass and friction slows it.", "It slows down.", "unbalanced"),
            ("A hockey puck is hit with a stick.", "It speeds up.", "unbalanced"),
            ("A lamp hangs from the ceiling by a chain.", "It stays still.", "balanced"),
            ("A kid stands still on a scale.", "The kid stays still.", "balanced"),
            ("A tennis ball is hit back over the net.", "It changes direction.", "unbalanced"),
            ("A bike rider squeezes the brakes.", "The bike slows down.", "unbalanced"),
            ("A picture hangs on a nail on the wall.", "It stays still.", "balanced"),
            ("A boat floats still on a calm lake.", "It stays still.", "balanced"),
            ("A girl pushes a swing.", "The swing starts moving.", "unbalanced")]
    s, what, k = R.choice(rows)
    return item("%s %s Are the forces balanced or unbalanced?" % (s, what), k,
                ["balanced" if k == "unbalanced" else "unbalanced", "There are no forces at all.", "Only gravity acts, so there is no answer."],
                "When motion changes (start, stop, speed up, slow down, turn), forces are unbalanced. When nothing changes, they are balanced.")


def g_still():
    things = [("a book on a shelf", "the shelf"), ("a cup on a table", "the table"), ("a ball on the floor", "the floor"), ("a cat sleeping on a rug", "the rug"),
              ("a lamp on a desk", "the desk"), ("a plant pot on a windowsill", "the windowsill"), ("a box on a bench", "the bench"), ("a laptop on a desk", "the desk"),
              ("a pumpkin on a porch", "the porch"), ("a bowl on a counter", "the counter"), ("a rock on the ground", "the ground"), ("a toy on a bed", "the bed")]
    t, under = R.choice(things)
    return item("%s%s is not moving. Which statement is true?" % (t[0].upper(), t[1:]),
                "Gravity pulls it down and %s pushes it up with an equal force." % under, ["No forces act on it.", "Only gravity acts on it.", "The forces on it are unbalanced."],
                "An object at rest still has forces on it. They are balanced.")


B1 = bank([
    ("What is a force?", "a push or a pull", ["a kind of energy you can eat", "the speed of an object", "the color of an object"], "Kicks, lifts and tugs are all forces."),
    ("Which is a pull?", "opening a drawer", ["kicking a ball", "pressing a doorbell", "pushing a cart"], "You pull a drawer toward you."),
    ("Which is a push?", "pressing a button", ["opening a door toward you", "dragging a sled behind you", "lifting a bag by its handle"], "Pressing moves something away from you."),
    ("What are balanced forces?", "equal forces in opposite directions", ["no forces at all", "two forces in the same direction", "one big force"], "Balanced forces cancel out."),
    ("What can unbalanced forces do to an object?", "start it, stop it, speed it up, slow it down or change its direction", ["only make it heavier", "nothing at all", "only change its color"],
     "Unbalanced forces change motion."),
    ("Which force pulls objects toward Earth?", "gravity", ["magnetism only", "friction", "a push from the wind"], "Gravity pulls everything down toward Earth."),
    ("Which force slows a sliding object?", "friction", ["gravity pulling up", "magnetism", "light"], "Friction acts where surfaces rub."),
    ("Two kids push a box from opposite sides with equal force. What happens?", "The box does not move.", ["The box moves left.", "The box moves right.", "The box flies up."], "The forces are balanced."),
])
B5 = bank([
    ("Ava pushes a toy car gently and then hard. Which push makes it move farther?", "the hard push", ["the gentle push", "They are the same.", "Neither push moves it."], "A bigger force changes motion more."),
    ("Leo hangs a weight from a spring. The spring stretches, then stops. Why does the weight stop moving?", "The spring pulls up with the same force as gravity pulls down.", ["Gravity stops working.", "The spring has no force.", "The weight gets lighter."],
     "The forces become balanced."),
    ("Mia wants to test how the size of a push changes how far a ball rolls. What should she change?", "only the size of the push", ["the ball and the push", "the floor and the ball", "nothing"],
     "Change one variable for a fair test."),
    ("A sled is sliding down a snowy hill. A friend pulls it from the bottom with a rope. What happens?", "The sled slows down.", ["The sled speeds up.", "Nothing changes.", "The sled moves uphill fast."],
     "The pull is opposite to the motion, so it slows the sled."),
    ("Noah pushes a heavy box but it does not move. Why?", "Friction pushes back with the same force, so the forces are balanced.", ["He used no force.", "There is no friction.", "Gravity pulls the box sideways."],
     "Balanced forces do not change motion."),
])


def body():
    think = ("<p>A <b>force</b> is a push or a pull. Forces have a size and a direction. We show them with arrows: a longer arrow means a bigger force.</p>"
             "<p><b>Balanced forces</b> are equal and opposite. They do not change how an object moves. <b>Unbalanced forces</b> are not equal. "
             "They make an object start, stop, speed up, slow down or change direction.</p>"
             + figure(force_pic(2, 4), "The push to the right is bigger, so the box moves to the right."))
    ex = [("In a tug-of-war, both teams pull equally hard. What happens?", ["The pulls are equal and opposite.", "The forces are balanced."], "The rope does not move."),
          ("A ball at rest is kicked. Are the forces balanced?", ["The ball starts moving.", "Motion changed."], "No, they are unbalanced.")]
    mist = ["Thinking an object at rest has no forces. The forces are balanced.",
            "Thinking the object moves toward the smaller force. It moves in the direction of the bigger force.",
            "Saying “balanced” means there are no forces."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Pushes and pulls", B1 + [(g_pic, 6), (g_still, 6)]),
        ("Balanced or unbalanced?", [(g_pic, 12), (g_change, 8)]),
        ("Tug-of-war", [(g_tug, 12), (g_pic, 8)]),
        ("Forces change motion", [(g_change, 12), (g_tug, 4), (g_still, 4)]),
        ("Force investigations", B5 + [g_pic, g_tug, g_change]),
    ])
    make("grade-3", "balanced-and-unbalanced-forces", 1, "3-PS2-1",
         "Plan and conduct an investigation to provide evidence of the effects of balanced and unbalanced forces on the motion of an object.",
         "Balanced and Unbalanced Forces",
         "Grade 3 Forces Worksheets: Balanced and Unbalanced Forces, Pushes and Pulls",
         "Balanced and Unbalanced Forces",
         "Free Grade 3 science worksheets on balanced and unbalanced forces (NGSS 3-PS2-1): pushes and pulls, force arrows, tug-of-war and how forces change motion. 100 practice questions with answers.",
         "Unbalanced forces change motion. Balanced forces do not.",
         "A force is a push or a pull. Equal and opposite forces are balanced, so the object keeps doing what it was doing.",
         body(),
         [("What is the difference between balanced and unbalanced forces?", "Balanced forces are equal and opposite and do not change motion. Unbalanced forces are not equal and make an object start, stop, speed up, slow down or turn."),
          ("Are there forces on an object that is not moving?", "Yes. Gravity pulls it down and the floor or table pushes it up. The forces are balanced."),
          ("Which way does an object move when forces are unbalanced?", "It moves in the direction of the bigger force.")],
         sets)


if __name__ == "__main__":
    main()
