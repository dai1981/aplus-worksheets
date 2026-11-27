# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 1, AC9S1U03: pushes and pulls - their strength and direction, and how they change the
speed, direction and shape of objects.
  python tools/gen_au_science_y1_pushes_and_pulls.py
Reuses the US Kindergarten pushes and pulls and changing speed and direction makers with Australian names, plus own questions on
changing shape (squashing, stretching, twisting). Short sentences.
Wrong answers come from real mistakes: thinking a bigger push makes things go a shorter way, and thinking only pushes change shape.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once
import sci_kids as K

YEAR, SORT = 1, 4
U, R, P, src = AU(seed_of(YEAR, SORT))

PP = "gen_us_science_gk_pushes_and_pulls"
SD = "gen_us_science_gk_changing_speed_and_direction"
p_pp = src(PP, "g_pp")
p_dir = src(PP, "g_dir")
p_strong = limit(src(PP, "g_strong"), 8)
p_data = limit(src(PP, "g_data"), 6)
p_b1 = src.B(PP, "B1")
p_b5 = src.B(PP, "B5")
s_change = src(SD, "g_change")
s_pick = limit(src(SD, "g_pick2"), 8)
s_test = src(SD, "g_test")
s_dist = src(SD, "g_dist")
s_wall = src(SD, "g_wall")
s_b5 = src.B(SD, "B5")

SHAPE = [("squash a ball of play dough", "push", "it gets flatter"), ("stretch a rubber band", "pull", "it gets longer"),
         ("squeeze a sponge", "push", "it gets smaller"), ("pull a piece of chewing gum", "pull", "it gets longer and thinner"),
         ("press a foot into wet sand", "push", "it makes a footprint"), ("pull a slinky", "pull", "it stretches out"),
         ("roll play dough into a snake", "push", "it gets long and thin"), ("pull a sock over a foot", "pull", "it stretches")]


def g_shape():
    act, f, res = R.choice(SHAPE)
    k = R.choice(["force", "result"])
    if not once(("sh", act, k)):
        return None
    if k == "force":
        return tq("You %s. Is this a push or a pull?" % act, "a %s" % f, ["a %s" % ("pull" if f == "push" else "push"), "neither", "a spin only"],
                  "Pushes and pulls can change the shape of things.")
    return tq("You %s. What happens to its shape?" % act, res, [x[2] for x in SHAPE if x[2] != res][:3], "Forces can change shape.")


POOL1 = pool(R, [
    ("What is a push?", "a force that moves something away from you", ["a force that moves something towards you", "a kind of light", "a sound"], "You push a swing away."),
    ("What is a pull?", "a force that moves something towards you", ["a force that moves something away", "a colour", "a smell"], "You pull a door open."),
    ("Kicking a footy is a…", "push", ["pull", "spin only", "sound"], "Your foot pushes the ball away."),
    ("Opening a drawer is a…", "pull", ["push", "bounce", "twist only"], "You pull it towards you."),
    ("What happens when you push a ball harder?", "it goes faster and further", ["it goes slower", "it stops", "it gets smaller"], "A stronger push gives more movement."),
    ("How can you change the direction of a rolling ball?", "push it from the side", ["look at it", "say stop", "clap"], "A push can change direction."),
    ("What does a magnet do to a steel paper clip?", "pulls it without touching", ["pushes it away always", "makes it hot", "nothing"], "Magnets can pull some metals."),
    ("What makes a dropped apple fall to the ground?", "the pull of gravity", ["a push from the wind only", "magnets", "light"], "Gravity pulls things down."),
    ("A cricket ball is hit by a bat. What changes?", "its direction and speed", ["its colour", "its name", "nothing"], "The bat pushes the ball."),
    ("Which needs a bigger push?", "a heavy box", ["an empty box", "a feather", "a balloon"], "Heavy things need bigger forces."),
])
POOL5 = pool(R, [
    ("Mia pushes a toy car gently, then hard. She measures how far it goes. What will she find?", "the hard push makes it go further", ["the gentle push goes further", "both the same", "the car does not move"], "Stronger pushes move things further."),
    ("Jack tests how far a car rolls on carpet and on tiles. What should he keep the same?", "the car and the push", ["the floor", "nothing", "the distance"], "Change one thing only."),
    ("Ruby pulls a box with a rope. It moves towards her. Which way was the force?", "towards Ruby", ["away from Ruby", "up only", "no force"], "A pull is towards you."),
    ("Kai rolls a ball into a wall. What happens?", "the wall pushes it back and it changes direction", ["the ball goes through the wall", "it speeds up", "nothing"], "A wall can change direction."),
    ("Ella squeezes a stress ball, then lets go. What happens?", "it goes back to its shape", ["it stays flat forever", "it melts", "it gets bigger"], "Some materials spring back."),
    ("Noah uses a measuring tape to see how far his paper plane flew after soft and hard throws. Why does he measure?", "to compare the results fairly", ["to make the plane fly", "to decorate it", "for no reason"], "Measuring helps us compare."),
])


def main():
    sets = U.sets([
        ("Push or pull?", [(POOL1, 6), (p_pp, 6), (p_b1, 4), (g_shape, 4)]),
        ("Strength and direction", [(p_dir, 6), (p_strong, 6), (POOL1, 3), (s_change, 3), (s_wall, 2)]),
        ("Changing speed and direction", [(s_pick, 6), (s_change, 4), (s_dist, 4), (POOL1, 2), (p_strong, 2), (s_wall, 2)]),
        ("Changing shape", [(g_shape, 12), (POOL1, 2), (POOL5, 2), (p_data, 4)]),
        ("Let's test it", [(POOL5, 4), (p_b5, 4), (s_b5, 4), (s_test, 4), (p_data, 2), (s_pick, 2)]),
    ])
    pic = K.row(["ball", "block", "dog", "drum"], words=["kick", "push", "pull", "tap"], size=80, label="kicking a ball, pushing a block, pulling a dog lead and tapping a drum")
    make_au(YEAR, "pushes-and-pulls", SORT, "AC9S1U03", "Physical sciences",
            "Describe pushes and pulls in terms of strength and direction and predict the effect of these forces on objects' motion "
            "and shape (summary of the Australian Curriculum v9.0 Science content description).",
            "Pushes and Pulls", "Pushes and pulls",
            "Free Year 1 science worksheets on pushes and pulls: strong and gentle forces, direction, changing speed and direction, "
            "and changing shape by squashing and stretching. 100 questions with answers.",
            "A push or pull makes things move.", "A bigger push or pull makes a bigger change. Forces can also change shape.",
            ("Pushes and pulls are forces.", ["A push moves things away from you.", "A pull moves things towards you.",
                                               "Forces can change speed, direction and shape."]),
            [("Opening a door towards you: push or pull?", ["it comes towards you"], "pull")],
            ["Thinking a bigger push makes things go a shorter way.", "Thinking only pushes can change shape (pulls stretch things)."],
            [("What is a force?", "A force is a push or a pull. Forces can start, stop, speed up, slow down or turn moving things."),
             ("How can forces change shape?", "Squashing, squeezing and pressing are pushes; stretching is a pull. Both can change an object's shape."),
             ("How can children explore forces?", "Push toy cars with different strengths, roll balls into walls and stretch rubber bands.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
