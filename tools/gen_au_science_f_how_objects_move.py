# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Foundation, AC9SFU02: how objects move (roll, slide, bounce, spin, fall) and how size, shape
and material change the way they move.
  python tools/gen_au_science_f_how_objects_move.py
Reuses the US Kindergarten pushes and pulls and changing speed and direction makers with Australian names, plus own questions
on rolling and sliding. Very short sentences.
Wrong answers come from real mistakes: thinking a cube rolls like a ball, thinking heavy things always move faster, and thinking
objects move by themselves.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit, once
import sci_kids as K

YEAR, SORT = 0, 3
U, R, P, src = AU(seed_of(YEAR, SORT))

PP = "gen_us_science_gk_pushes_and_pulls"
SD = "gen_us_science_gk_changing_speed_and_direction"
p_pp = src(PP, "g_pp")
p_dir = src(PP, "g_dir")
p_strong = limit(src(PP, "g_strong"), 6)
p_b1 = src.B(PP, "B1")
p_b5 = src.B(PP, "B5")
s_change = src(SD, "g_change")
s_surf = src(SD, "g_surf")
s_ramp = src(SD, "g_ramp")
s_pick = limit(src(SD, "g_pick2"), 6)
s_b1 = src.B(SD, "B1")

MOVE = {"roll": ["a ball", "a marble", "an orange", "a wheel", "a tin can on its side"],
        "slide": ["a book", "a box", "a block", "an ice cube"],
        "bounce": ["a tennis ball", "a basketball", "a rubber ball"],
        "spin": ["a top", "a fidget spinner", "a pinwheel"]}


def g_move():
    k = R.choice(sorted(MOVE))
    o = R.choice(MOVE[k])
    if not once(("mv", o)):
        return None
    return tq("How does %s move best?" % o, "it can %s" % k, ["it can %s" % x for x in sorted(MOVE) if x != k][:3],
              "Round things roll. Flat things slide.")


SHAPE = [("Which shape rolls best?", "a ball", ["a cube", "a book", "a brick"], "Round shapes roll."),
         ("Which shape slides but does not roll?", "a box", ["a ball", "a marble", "a wheel"], "Flat sides slide."),
         ("Which ball bounces highest?", "a rubber ball", ["a ball of wet clay", "a ball of wool", "a beanbag"], "Rubber is springy."),
         ("Which will slide further on the floor?", "a smooth plastic box", ["a box with a rough mat on it", "a box with carpet under it", "a box on sand"], "Smooth things slide further."),
         ("Which car will roll further?", "a car on a smooth floor", ["a car on thick carpet", "a car on grass", "a car on sand"], "Rough surfaces slow things down."),
         ("Which is easier to roll down a slide?", "a round ball", ["a square block", "a flat book", "a sock"], "Round things roll easily."),
         ("What makes a ball start to roll?", "a push", ["nothing", "the colour", "the size only"], "Objects need a push or pull to move."),
         ("Which ball will roll further if you push both the same?", "a small hard ball on the footpath", ["a big soft ball on long grass", "a ball of clay", "a flat ball"], "Hard balls on smooth ground roll far.")]


def main():
    POOL1 = pool(R, SHAPE + [
        ("What do we call it when something moves round and round on the spot?", "spinning", ["rolling", "sliding", "falling"], "A top spins."),
        ("What happens to a ball when you let go of it?", "it falls down", ["it floats up", "it stays in the air", "it disappears"], "Things fall to the ground."),
        ("A ball rolls down a ramp. How can you make it go faster?", "make the ramp steeper", ["make the ramp flat", "paint the ball", "put sand on the ramp"], "Steeper ramps make things go faster."),
        ("Which one can roll and slide?", "a can of food", ["a cube", "a brick", "a book"], "On its side it rolls; on its end it slides."),
    ])
    POOL5 = pool(R, [
        ("Mia rolls a ball on grass and on concrete. Where does it roll further?", "on concrete", ["on grass", "the same", "it does not roll"], "Smooth ground lets it roll far."),
        ("Jack drops a tennis ball and a ball of play dough. Which one bounces?", "the tennis ball", ["the play dough", "both", "neither"], "Some materials bounce."),
        ("Ruby tests which toy rolls down a ramp. Which will roll?", "a toy car with wheels", ["a wooden block", "a book", "a box"], "Wheels help things roll."),
        ("Kai pushes a box gently and then hard. Which push moves it further?", "the hard push", ["the gentle push", "both the same", "neither"], "A bigger push moves things further."),
        ("Ella rolls a marble and a basketball down the same ramp. What should she keep the same?", "the ramp", ["the balls", "nothing", "the colour"], "Only change one thing."),
        ("Noah slides a block on a tray of ice and on carpet. Where does it slide further?", "on ice", ["on carpet", "the same", "it cannot slide"], "Ice is slippery."),
    ])
    sets = U.sets([
        ("Ways things move", [(g_move, 10), (POOL1, 6), (p_b1, 4)]),
        ("Pushes and pulls", [(p_pp, 6), (p_dir, 5), (p_strong, 5), (POOL1, 2), (s_b1, 2)]),
        ("Shape and size", [(POOL1, 5), (g_move, 3), (s_pick, 5), (s_change, 4), (p_strong, 3)]),
        ("Surfaces and ramps", [(s_surf, 6), (s_ramp, 6), (POOL1, 2), (s_change, 3), (s_pick, 3)]),
        ("Let's test it", [(POOL5, 6), (p_b5, 4), (s_b1, 3), (s_ramp, 2), (s_surf, 2), (g_move, 3)]),
    ])
    pic = K.row(["ball", "block", "ball", "rain"], words=["roll", "slide", "bounce", "fall"], size=80, label="a ball rolls, a block slides, a ball bounces, rain falls")
    make_au(YEAR, "how-objects-move", SORT, "AC9SFU02", "Physical sciences",
            "Describe how objects move and how factors including their size, shape or material influence their movement "
            "(Australian Curriculum v9.0 Science content description).",
            "How Objects Move", "How objects move",
            "Free Foundation science worksheets on how objects move: rolling, sliding, bouncing and spinning, pushes and pulls, "
            "and how shape, size, material and surfaces change movement. 100 questions with answers.",
            "Round things roll. Flat things slide.", "A push or pull makes things move. Shape, size and material change how they move.",
            ("Things move in different ways.", ["Balls roll. Boxes slide.", "Rubber balls bounce. Tops spin.",
                                                "A push or a pull makes things move."]),
            [("Which rolls: a ball or a book?", ["a ball is round"], "a ball")],
            ["Thinking a cube can roll like a ball.", "Thinking things move without a push or pull."],
            [("What makes things move?", "A push or a pull. Gravity also pulls things down when they fall."),
             ("Why do some things roll and others slide?", "Round things roll. Things with flat sides slide."),
             ("How can children explore movement at home?", "Roll different balls down a ramp, slide toys on different floors and see which ones bounce.")],
            sets, pic=pic)


if __name__ == "__main__":
    main()
