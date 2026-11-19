# -*- coding: utf-8 -*-
"""
Texas Kindergarten Math: 3D Solids: Cylinders, Cones, Spheres and Cubes (TEKS K.6B, K.6C, K.6E)
  python3 tools/gen_ustx_math_gk_solids_3d.py
Naming and finding solids (the US Kindergarten makers), and solids in the real world, flat faces,
roll, stack or slide, and flat or solid (own makers).
Wrong answers come from real mistakes: mixing up a circle and a sphere, and a square and a cube.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_gk_2d_and_3d_shapes as sh
adopt(sh)
tx_common.GRADE = "kindergarten"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


USED = {}


def pick(r, pool, tag):
    """Each pool item is used once, so no question repeats with only a name changed."""
    if tag not in USED:
        USED[tag] = list(pool)
        r.shuffle(USED[tag])
    if not USED[tag]:
        raise AssertionError("pool used up")
    return USED[tag].pop()

FACE = [("a can of soup", "circle"), ("a cereal box", "rectangle"), ("a number cube", "square"), ("an ice cream cone", "circle"), ("a tissue box", "rectangle"),
        ("a wooden block shaped like a cube", "square"), ("a drum", "circle"), ("a shoe box", "rectangle"), ("a party hat", "circle"), ("a glue stick", "circle"),
        ("a juice box", "rectangle"), ("an ice cube", "square"), ("a paper towel roll", "circle"), ("a box of crackers", "rectangle"), ("a cup", "circle"),
        ("a toy block shaped like a cube", "square"), ("a pizza box", "square"), ("a candle", "circle")]
SHAPES = ["circle", "triangle", "rectangle", "square"]
REAL = [("a basketball", "sphere"), ("an ice cream cone", "cone"), ("a can of beans", "cylinder"), ("a number cube", "cube"), ("a globe", "sphere"), ("a party hat", "cone"),
        ("a drum", "cylinder"), ("a sugar cube", "cube"), ("a marble", "sphere"), ("a traffic cone", "cone"), ("a candle", "cylinder"), ("a toy block", "cube"),
        ("an orange", "sphere"), ("a paper towel roll", "cylinder"), ("a game die", "cube"), ("a funnel", "cone")]
SOLIDS = ["sphere", "cube", "cone", "cylinder"]


def one_real(r):
    obj, s = pick(r, REAL, "real")
    k = Kid(r).next()
    return mcq("%s sees %s. What solid shape is it like?" % (k["n"], obj), "A " + s, ["A " + x for x in SOLIDS if x != s], "%s is shaped like <b>a %s</b>." % (obj[0].upper() + obj[1:], s))


def one_face(r):
    obj, shp = pick(r, FACE, "face")
    k = Kid(r).next()
    return mcq("%s traces around the bottom of %s. What flat shape does %s draw?" % (k["n"], obj, k["he"]), "A " + shp, ["A " + x for x in SHAPES if x != shp],
               "The flat face on the bottom of %s is <b>a %s</b>." % (obj, shp))


MOVE = [("a ball", "roll", "It is a sphere, round all over"), ("a box", "stack", "It has flat faces"), ("a can", "roll and stack", "It is a cylinder with flat faces and a curved side"),
        ("a block", "stack", "It is a cube with flat faces"), ("an orange", "roll", "It is round like a sphere"), ("a cereal box", "stack", "It has flat faces"),
        ("a paper towel roll", "roll and stack", "It is a cylinder"), ("a marble", "roll", "It is a sphere"), ("a drum", "roll and stack", "It is a cylinder"),
        ("a number cube", "stack", "It is a cube"), ("a globe", "roll", "It is a sphere"), ("a soup can", "roll and stack", "It is a cylinder")]
ANS = ["Roll", "Stack", "Roll and stack", "Neither"]


def one_move(r):
    obj, a, why = pick(r, MOVE, "move")
    k = Kid(r).next()
    right = a[0].upper() + a[1:]
    return mcq("%s plays with %s. Can it roll, stack, or both?" % (k["n"], obj), right, [x for x in ANS if x != right], "%s. It can <b>%s</b>." % (why, a))


FLAT = [("a drawing of a circle", "flat"), ("a ball", "solid"), ("a paper triangle", "flat"), ("a soup can", "solid"), ("a sticker shaped like a square", "flat"), ("a block", "solid"),
        ("a paper rectangle", "flat"), ("an orange", "solid"), ("a picture of a star", "flat"), ("a box", "solid"), ("a drawing of a square", "flat"), ("a cone", "solid"),
        ("a paper heart", "flat"), ("a marble", "solid"), ("a drawing of a triangle", "flat"), ("a toy truck", "solid"), ("a sticker shaped like a circle", "flat"), ("a cup", "solid"),
        ("a paper square", "flat"), ("a globe", "solid")]


def one_flat(r):
    obj, kind = pick(r, FLAT, "flat")
    k = Kid(r).next()
    return mcq("%s holds %s. Is it a flat shape or a solid?" % (k["n"], obj), "A " + kind + (" shape" if kind == "flat" else ""), ["A " + ("solid" if kind == "flat" else "flat shape"), "Both", "Neither"],
               "%s is <b>%s</b>." % (obj[0].upper() + obj[1:], "flat" if kind == "flat" else "a solid"))


def build():
    sets, R = build_sets([
        ("Name the solid shape", [("run", sh.set_solid, ("rnd", sh.Kids), 20)]),
        ("Solids in the real world", [("collect", one_real, 16), ("collect", one_move, 4)]),
        ("Flat faces of solids", [("collect", one_face, 18), ("collect", one_move, 2)]),
        ("Flat or solid?", [("collect", one_flat, 20)]),
        ("Find the shape; roll or stack", [("run", sh.set_find, ("rnd", sh.Kids), 14), ("collect", one_move, 6)]),
    ], 69013)
    finish(sets, R)
    body = lesson('<ul><li><b>Solids</b> are not flat: sphere, cube, cone, cylinder.</li><li>A <b>sphere</b> is a ball. A <b>cube</b> has 6 square faces.</li><li>A <b>cylinder</b> is like a can. A <b>cone</b> is like an ice cream cone.</li><li>The flat faces of solids are 2D shapes: a can has circle faces.</li></ul>',
        [example("A can of soup", ["2 flat circle faces"], "cylinder")],
        [['Mixing up a circle and a sphere', 'A circle is flat; a sphere is a ball.'], ['Mixing up a square and a cube', 'A square is one face of a cube.'], ['Thinking a turned cone is something else', 'Turning does not change the solid.']])
    faq = [('What does TEKS K.6B ask?', 'Identify three-dimensional solids, including cylinders, cones, spheres, and cubes, in the real world.'), ('What does TEKS K.6C ask?', 'Identify two-dimensional components of three-dimensional objects.'), ('Which solids can roll?', 'Spheres, cylinders and cones.'), ('What flat shape is on a cube?', 'A square.')]
    make('3d-solids', 13, 'Geometry and Measurement', 'K.6B, K.6C, K.6E',
         'K.6B identify three-dimensional solids, including cylinders, cones, spheres, and cubes, in the real world; K.6C identify two-dimensional components of three-dimensional objects; K.6E classify and sort a variety of regular and irregular two- and three-dimensional figures regardless of orientation or size',
         '3D Solids: Cylinders, Cones, Spheres and Cubes', '3D Solids',
         'Free kindergarten 3D solid worksheets for Texas TEKS K.6B, K.6C and K.6E: spheres, cubes, cones and cylinders in the real world, flat faces, and flat or solid. 100 questions with answers.',
         'Solids are not flat: sphere, cube, cone, cylinder.', 'A can is a cylinder with circle faces.',
         body, faq, sets, seo_title='Kindergarten 3D Solids Worksheets (TEKS K.6B)')


if __name__ == "__main__":
    build()
