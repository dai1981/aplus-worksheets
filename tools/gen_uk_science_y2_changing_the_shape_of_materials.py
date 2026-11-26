# -*- coding: utf-8 -*-
"""
UK Year 2 science: Changing the Shape of Materials (Uses of everyday materials)
  python tools/gen_uk_science_y2_changing_the_shape_of_materials.py
Find out how the shapes of solid objects made from some materials can be changed by squashing, bending, twisting and
stretching: naming the action, which objects can change shape, which go back to their shape, and an elastic-band
stretching test with results to read.
Wrong answers come from real mistakes: "all materials can be stretched", "squashed things always spring back",
"twisting and bending are the same", "a brick can be squashed with your hands".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
from sci_phys import uniq
import sci_kids as K

U = Unit(61211)
R = U.R
P = People(R)

ACT = [("pressing a ball of modelling clay flat", "squashing"), ("pressing a sponge in your hand", "squashing"), ("standing on an empty drinks can", "squashing"),
       ("making a snowball by pressing snow together", "squashing"), ("folding a piece of paper in half", "bending"), ("curving a pipe cleaner into a U", "bending"),
       ("making a straw into an L shape", "bending"), ("curving a ruler made of thin plastic", "bending"), ("wringing out a wet cloth", "twisting"),
       ("turning the ends of a sweet wrapper in opposite directions", "twisting"), ("turning a pipe cleaner round and round a pencil", "twisting"),
       ("making a balloon animal by turning the balloon", "twisting"), ("pulling an elastic band longer", "stretching"), ("pulling a spring apart", "stretching"),
       ("pulling a pair of tights over your legs", "stretching"), ("rolling dough out longer and thinner", "stretching")]
WORDS = ["squashing", "bending", "twisting", "stretching"]


def g_act():
    a, w = R.choice(ACT)
    if not once(("ac", a)):
        return None
    return item("Is %s squashing, bending, twisting or stretching?" % a, w, [x for x in WORDS if x != w], "Squash: press. Bend: curve. Twist: turn. Stretch: pull longer.")


CAN = [("a sponge", "squashed", True), ("a brick", "squashed with your hands", False), ("an elastic band", "stretched", True), ("a glass marble", "stretched", False),
       ("a pipe cleaner", "bent", True), ("a stone", "bent with your hands", False), ("a towel", "twisted", True), ("a metal spoon", "stretched with your hands", False),
       ("modelling clay", "squashed", True), ("a pair of tights", "stretched", True), ("a wooden block", "squashed with your hands", False), ("a paperclip", "bent", True),
       ("a balloon", "stretched", True), ("a china plate", "bent", False), ("kitchen foil", "twisted", True), ("a rock", "twisted with your hands", False)]


def g_can():
    o, v, y = R.choice(CAN)
    if not once(("ca", o)):
        return None
    return item("Can %s be %s?" % (o, v), "Yes." if y else "No, it is too hard or stiff.", ["No, it is too hard or stiff." if y else "Yes.", "Only when it is wet.", "Only on a hot day."],
                "Some materials can change shape easily; hard, stiff ones cannot.")


BACK = [("A sponge is squashed.", True), ("An elastic band is stretched and let go.", True), ("A spring is stretched a little and let go.", True),
        ("A ball of modelling clay is squashed.", False), ("A sheet of foil is scrunched up.", False), ("A drinks can is crushed.", False),
        ("Someone lies on a pillow and then gets up.", True), ("A paperclip is bent open.", False), ("A bouncy ball is squeezed.", True), ("A pipe cleaner is twisted.", False)]


def g_back():
    o, y = R.choice(BACK)
    if not once(("bk", o)):
        return None
    return item("%s Does it go back to its old shape by itself?" % o, "Yes, it springs back." if y else "No, it stays in its new shape.",
                ["No, it stays in its new shape." if y else "Yes, it springs back.", "It disappears.", "It turns into a liquid."], "Some materials spring back; others stay changed.")


def g_band():
    who = P.next()[0]
    st = R.choice([2, 3, 4])
    L0 = R.choice([8, 10, 12])
    v = [L0 + st * i for i in range(5)]
    k = R.choice(["read", "read", "pattern", "diff", "predict"])
    ri = R.randrange(1, 5)
    if not once(("bd", L0, st, k, ri if k == "read" else 0)) or (k == "pattern" and not once(("bp",), 2)):
        return None
    tab = table(["Marbles in the cup", "Length of the elastic band (cm)"], [[str(i), str(x)] for i, x in enumerate(v)])
    intro = tab + "%s hung a cup on an elastic band and added marbles one at a time. " % who
    if k == "read":
        g = "%d cm" % v[ri]
        return item(intro + "How long was the band with %d marble%s?" % (ri, "" if ri == 1 else "s"), g, uniq(g, ["%d cm" % x for x in v] + ["%d cm" % ri]), "Read across the row.")
    if k == "pattern":
        return item(intro + "What happened as more marbles were added?", "The band stretched longer.", ["The band got shorter.", "The band stayed the same.", "The band twisted."], "More pull, more stretch.")
    if k == "diff":
        d = v[4] - v[0]
        g = "%d cm" % d
        return item(intro + "How much longer was the band with 4 marbles than with none?", g, uniq(g, ["%d cm" % v[4], "%d cm" % v[0], "4 cm", "%d cm" % (d + st)]), "%d − %d = %d cm." % (v[4], v[0], d))
    g = "%d cm" % (v[4] + st)
    return item(intro + "If the pattern carries on, how long will it be with 5 marbles?", g, uniq(g, ["%d cm" % v[4], "%d cm" % (v[4] + 1), "5 cm", "%d cm" % (v[4] + 2 * st)]),
                "Each marble adds %d cm." % st)


B1 = bank([
    ("What does squash mean?", "press something to make it flatter or smaller", ["pull it longer", "turn it round", "curve it"], "Like pressing clay."),
    ("What does stretch mean?", "pull something to make it longer", ["press it flat", "turn it", "fold it"], "Like an elastic band."),
    ("What does twist mean?", "turn the ends in opposite directions", ["press it flat", "pull it longer", "make it see-through"], "Like wringing a cloth."),
    ("What does bend mean?", "make something curved or folded", ["make it longer", "make it melt", "make it disappear"], "Like a pipe cleaner."),
    ("Which material can be stretched easily?", "an elastic band", ["a brick", "a glass", "a stone"], "Elastic materials stretch."),
    ("Which material can be squashed easily?", "a sponge", ["a rock", "a brick", "a metal spoon"], "Soft materials squash."),
    ("Can you squash a brick with your hands?", "No, it is too hard.", ["Yes, easily.", "Only when it is cold.", "Only red bricks."], "Hard materials keep their shape."),
    ("What do we use to change the shape of a solid object?", "a push or a pull", ["only light", "only sound", "only water"], "Squash, bend, twist, stretch."),
])
B5 = bank([
    ("Why are elastic bands useful for holding things together?", "They stretch round things and pull back tight.", ["They are see-through.", "They are very hard.", "They melt when stretched."], "Stretchy and springy."),
    ("Why is modelling clay good for making models?", "It can be squashed and shaped and keeps its new shape.", ["It springs back at once.", "It cannot change shape.", "It is see-through."], "Keeps its shape."),
    ("Why are trampolines made with springs?", "Springs stretch and then spring back, so you bounce.", ["Springs are soft like clay.", "Springs stay stretched.", "Springs are waterproof."], "Stretch and spring back."),
    ("How could you test which elastic band stretches the most?", "Hang the same weight on each band and measure how long each gets.", ["Use a different weight on each.", "Look at their colours.", "Stretch only one band."], "Fair test."),
    ("Why should you not stretch an elastic band too far?", "It can snap.", ["It turns into a spring.", "It becomes metal.", "It never changes."], "Materials have limits."),
])


def body():
    pic = K.row(["ball", "cube", "sock"], words=["squash", "bend", "stretch"], size=90, label="materials can be squashed, bent, twisted or stretched")
    ex = [("Wringing out a wet cloth?", ["Ends turn opposite ways"], "twisting"),
          ("Does clay spring back after squashing?", ["It keeps its new shape"], "No")]
    mist = ["Thinking all materials can be stretched.", "Thinking squashed things always spring back.", "Thinking twisting and bending are the same."]
    return kid_lesson(pic, "Pushes and pulls can change an object's shape.",
                      ["Squash, bend, twist and stretch.", "Soft or bendy materials change shape easily; hard ones do not.", "Some spring back; some stay in their new shape."], ex, mist)


def main():
    sets = U.sets([
        ("Squash, bend, twist, stretch", B1 + [(g_act, 12)]),
        ("Which action?", [(g_act, 3), (g_can, 12), (g_back, 5)]),
        ("Spring back or stay?", [(g_back, 5), (g_can, 3), (g_band, 12)]),
        ("Stretching test", [(g_band, 20)]),
        ("Thinking about shapes", B5 + [(g_band, 15)]),
    ])
    make_uk(2, "changing-the-shape-of-materials", 11, "Uses of everyday materials",
            "Find out how the shapes of solid objects made from some materials can be changed by squashing, bending, twisting and stretching.",
            "Squashing, Bending, Twisting, Stretching",
            "Year 2 Science: Changing the Shape of Materials Worksheets (Squash, Bend, Twist, Stretch)",
            "Changing Shape",
            "Free Year 2 science worksheets on changing the shape of materials: squashing, bending, twisting and stretching, which materials spring back and an elastic band test. 100 questions with answers.",
            "Squash, bend, twist, stretch.",
            "Some materials spring back; others keep their new shape.",
            body(),
            [("How can we change the shape of an object?", "By squashing, bending, twisting or stretching it with a push or a pull."),
             ("Which materials change shape easily?", "Soft or bendy materials such as sponge, modelling clay, elastic bands and pipe cleaners. Hard materials such as brick, stone and glass do not."),
             ("Do things go back to their old shape?", "Some do, like a sponge or an elastic band. Others, like modelling clay or crushed foil, stay in their new shape.")],
            sets)


if __name__ == "__main__":
    main()
