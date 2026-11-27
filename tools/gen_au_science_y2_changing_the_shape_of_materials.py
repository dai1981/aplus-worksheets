# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 2, AC9S2U03: materials can be changed physically by bending, twisting, stretching,
squashing and breaking, without becoming a different material; some go back to their shape and some do not.
  python tools/gen_au_science_y2_changing_the_shape_of_materials.py
Reuses the UK Year 2 changing the shape of materials makers with Australian names, plus own questions. Short sentences.
Wrong answers come from real mistakes: thinking a bent material becomes a new material, and thinking every material springs back.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once
import sci_kids as K

YEAR, SORT = 2, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

CS = "gen_uk_science_y2_changing_the_shape_of_materials"
c_act = src(CS, "g_act")
c_back = src(CS, "g_back")
c_band = limit(src(CS, "g_band"), 8)
c_can = src(CS, "g_can")
c_b1 = src.B(CS, "B1")
c_b5 = src.B(CS, "B5")

ACTS = [("bend", "a pipe cleaner", "it stays bent"), ("twist", "a piece of wire", "it stays twisted"), ("stretch", "a rubber band", "it goes back"),
        ("squash", "a sponge", "it goes back"), ("squash", "a ball of play dough", "it stays squashed"), ("stretch", "a balloon", "it goes back when you let go"),
        ("bend", "a plastic ruler", "it springs back"), ("twist", "a towel", "it can be untwisted"), ("fold", "a sheet of paper", "it keeps a crease"),
        ("roll", "a lump of clay into a snake", "it stays rolled")]


def g_acts():
    a, o, r = R.choice(ACTS)
    k = R.choice(["what", "after"])
    if not once(("ac", o, k)):
        return None
    if k == "what":
        return tq("Which action changes the shape of %s?" % o, a, [x for x in ["bend", "twist", "stretch", "squash", "fold", "roll"] if x != a][:3],
                  "Bending, twisting, stretching and squashing change shape.")
    return tq("You %s %s. What happens after you let go?" % (a, o), r, [x[2] for x in ACTS if x[2] != r][:3],
              "Some materials spring back; some keep their new shape.")


SAME = [("a cut-up apple", "still apple"), ("a crumpled piece of foil", "still foil"), ("a bent paperclip", "still metal"),
        ("broken chalk", "still chalk"), ("a twisted pipe cleaner", "still a pipe cleaner"), ("squashed play dough", "still play dough"),
        ("torn paper", "still paper"), ("a folded T-shirt", "still fabric")]


def g_same():
    o, a = R.choice(SAME)
    if not once(("sm", o)):
        return None
    return tq("Is %s still the same material?" % o, "yes, it is %s" % a, ["no, it is a new material", "no, it is now plastic", "no, it is now water"],
              "Changing shape does not change the material.")


POOL1 = pool(R, [
    ("What does 'stretch' mean?", "pull something to make it longer", ["push it to make it flat", "turn it round", "break it"], "Rubber bands stretch."),
    ("What does 'twist' mean?", "turn the ends in opposite directions", ["make it longer", "make it hot", "paint it"], "You twist a lid off a jar."),
    ("Which material can be stretched and goes back?", "a rubber band", ["a glass", "a stone", "a wooden block"], "Rubber is elastic."),
    ("Which material breaks if you try to bend it?", "a dry biscuit", ["a rubber band", "a pipe cleaner", "a sock"], "Some materials are brittle."),
    ("What happens when you squash a ball of play dough?", "it changes shape and stays squashed", ["it turns into water", "it springs back", "it becomes metal"], "Play dough does not spring back."),
    ("Which can be folded?", "paper", ["a rock", "a glass", "a brick"], "Paper is bendy."),
    ("A potter shapes clay into a bowl. What kind of change is this?", "a change of shape; it is still clay", ["it is now a new material", "it disappears", "it becomes glass right away"], "Heating it in a kiln changes it later."),
    ("Why is a trampoline mat stretchy?", "so it bends down and springs back", ["so it breaks", "so it stays flat", "so it is heavy"], "Stretchy materials store energy."),
    ("Which action breaks a block of chocolate into pieces?", "snapping it", ["stretching it", "twisting it slowly", "bending it gently"], "Each piece is still chocolate."),
    ("Which is easier to bend?", "a thin wire", ["a thick metal bar", "a brick", "a glass jar"], "Thin things bend more easily."),
])
POOL5 = pool(R, [
    ("Mia hangs a toy on rubber bands of different thickness. Which band stretches most?", "the thinnest band", ["the thickest band", "all the same", "none"], "Thin bands stretch more."),
    ("Jack tests which materials spring back after squashing: a sponge, foil and play dough. Which spring back?", "only the sponge", ["all of them", "foil and play dough", "none of them"], "Sponges are springy."),
    ("Ruby bends a paperclip back and forth many times. What happens?", "it gets warm and may snap", ["it gets longer", "it turns to rubber", "nothing"], "Bending too often can break metal."),
    ("Kai pulls a rubber band and measures its length: 10 cm, then 15 cm, then 10 cm again. What does this show?", "it stretches and goes back", ["it breaks", "it shrinks forever", "it stays 15 cm"], "Rubber is elastic."),
    ("Ella wants to test how far rubber bands stretch fairly. What should she keep the same?", "the same weight on each band", ["the bands", "nothing", "the colour only"], "Only change one thing."),
    ("Noah twists a pipe cleaner into a shape. Then he untwists it. Is it a new material?", "no, it is still a pipe cleaner", ["yes, it is now wire", "yes, it is plastic", "it disappeared"], "Shape changes do not change materials."),
])


def main():
    sets = U.sets([
        ("Bend, twist, stretch and squash", [(g_acts, 8), (c_act, 6), (POOL1, 4), (c_b1, 2)]),
        ("Does it go back?", [(c_back, 6), (g_acts, 4), (c_can, 4), (POOL1, 3), (POOL5, 3)]),
        ("Still the same material", [(g_same, 8), (POOL1, 3), (c_can, 4), (c_b1, 3), (c_act, 2)]),
        ("Stretchy materials", [(c_band, 7), (g_acts, 4), (POOL1, 3), (POOL5, 3), (c_back, 3)]),
        ("Let's test it", [(c_b5, 4), (c_band, 1), (g_acts, 3), (g_same, 3), (c_can, 3), (c_act, 3), (POOL1, 3)]),
    ])
    pic = K.row(["paper", "sock", "ball", "block"], words=["fold", "stretch", "squash", "stack"], size=80, label="folding paper, stretching a sock, squashing a ball and stacking blocks")
    make_au(YEAR, "changing-the-shape-of-materials", SORT, "AC9S2U03", "Chemical sciences",
            "Recognise that materials can be changed physically without changing their material composition and explore the effect of "
            "different actions on materials including bending, twisting, stretching and breaking into smaller pieces "
            "(summary of the Australian Curriculum v9.0 Science content description).",
            "Changing the Shape of Materials", "Changing shape",
            "Free Year 2 science worksheets on changing the shape of materials: bending, twisting, stretching and squashing, materials "
            "that spring back, and why the material stays the same. 100 questions with answers.",
            "Changing shape, same material.", "Bending, twisting, stretching and squashing change the shape, not the material.",
            ("We can change the shape of materials.", ["Bend, twist, stretch, squash or fold.", "Rubber springs back; play dough does not.",
                                                       "It is still the same material."]),
            [("Bent paperclip: still metal?", ["only the shape changed"], "yes")],
            ["Thinking a bent or squashed object is a new material.", "Thinking all materials spring back."],
            [("What is a physical change?", "A physical change changes the shape or size of a material but not what it is made of."),
             ("Why do some materials spring back?", "Materials like rubber and sponge are elastic: they return to their shape after being stretched or squashed."),
             ("How can children explore this?", "Squash play dough, stretch rubber bands, fold paper and twist pipe cleaners, then talk about what changed.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
