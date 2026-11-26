# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Properties of Materials (2-PS1-1)
  python tools/gen_us_science_g2_properties_of_materials.py
Plan and conduct an investigation to describe and classify different kinds of materials by their observable
properties: color, texture (rough / smooth), hard / soft, bends / does not bend, shiny / dull, see-through,
floats / sinks, soaks up water / waterproof, solid / liquid.
Short sentences for 7-8 year olds, a picture in most questions.
Wrong answers come from real mistakes: "heavy things are always hard", "all metal floats", "see-through means soft".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, People
import sci_kids as K

U = Unit(20101)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# object picture, object words, material
OBJ = [("block", "a block", "wood"), ("spoon", "a spoon", "metal"), ("sock", "a sock", "cloth"), ("paper", "a sheet of paper", "paper"),
       ("glass", "a window", "glass"), ("rock", "a rock", "rock"), ("crayon", "a crayon", "wax"), ("ice", "an ice cube", "ice (frozen water)"),
       ("cup", "a plastic cup", "plastic"), ("ball", "a bouncy ball", "rubber")]

def g_what():
    pic, words, mat = R.choice(OBJ)
    who = P.next()[0]
    if not once(("w", pic)):
        return None
    wrong = [m for m in ["wood", "metal", "cloth", "paper", "glass", "rock", "plastic", "rubber"] if m != mat]
    R.shuffle(wrong)
    return item(fig(K.card(pic)) + "%s has %s. What is it made of?" % (who, words), mat, wrong[:3], "%s is made of %s." % (words[0].upper() + words[1:], mat))


# property -> (objects that clearly have it, objects that clearly do not)
YN = {"hard": ({"block", "spoon", "rock", "glass", "ice"}, {"sock", "paper"}),
      "soft": ({"sock"}, {"block", "spoon", "rock", "glass", "ice"}),
      "bends": ({"sock", "paper", "ball"}, {"block", "rock", "glass", "ice"}),
      "shiny": ({"spoon", "glass"}, {"sock", "paper", "block", "rock"}),
      "see-through": ({"glass", "ice"}, {"block", "spoon", "sock", "rock", "paper", "crayon", "ball"}),
      "rough": ({"rock"}, {"glass", "spoon", "cup", "ice"}),
      "floats": ({"block", "cup"}, {"spoon", "rock"}),
      "sinks": ({"spoon", "rock"}, {"block", "cup", "ball"}),
      "soaks up water": ({"sock", "paper"}, {"spoon", "glass", "cup", "rock", "ball", "crayon"}),
      "waterproof": ({"ball", "cup", "crayon"}, {"sock", "paper"}),
      "bouncy": ({"ball"}, {"block", "rock", "glass", "spoon", "ice"}),
      "melts in a warm room": ({"ice"}, {"block", "spoon", "rock", "glass", "sock"})}
ASK = {"hard": "Which one is hard?", "soft": "Which one is soft?", "bends": "Which one bends easily?", "shiny": "Which one is shiny?",
       "see-through": "Which one can you see through?", "rough": "Which one feels rough?",
       "floats": "Which one floats in water?", "sinks": "Which one sinks in water?", "soaks up water": "Which one soaks up water?",
       "waterproof": "Which one keeps water out (is waterproof)?", "bouncy": "Which one is bouncy?", "melts in a warm room": "Which one melts in a warm room?"}
BYPIC = {o[0]: o for o in OBJ}


def short(o):
    return o[1].split(" ", 1)[1]


def g_which():
    p = R.choice(sorted(YN))
    yes, no = YN[p]
    if len(no) < 3:
        return None
    a = BYPIC[R.choice(sorted(yes))]
    ws = [BYPIC[x] for x in R.sample(sorted(no), 3)]
    if not once(("p", p, a[0]), 2):
        return None
    who = P.next()[0]
    opts = [a] + ws
    R.shuffle(opts)
    L = "ABCD"
    pic = K.row([o[0] for o in opts], words=["%s. %s" % (L[i], short(o)) for i, o in enumerate(opts)], size=95)
    return item(fig(pic) + "%s sorts things. %s" % (who, ASK[p]), "%s (%s)" % (L[opts.index(a)], short(a)),
                ["%s (%s)" % (L[opts.index(o)], short(o)) for o in ws], "The %s: %s." % (short(a), p))


def g_true():
    pic, words, mat = R.choice(OBJ)
    ps = [p for p in YN if pic in YN[p][0]]
    ns = [p for p in YN if pic in YN[p][1]]
    if not ps or len(ns) < 3:
        return None
    p = R.choice(ps)
    if not once(("t", pic, p)):
        return None
    who = P.next()[0]
    what = words if mat in words or pic in ("rock", "paper") else "%s made of %s" % (words, mat)
    return item(fig(K.card(pic)) + "%s tests %s. Which word fits it?" % (who, what), p, R.sample(ns, 3),
                "It is %s." % p if p not in ("bends", "floats", "sinks", "soaks up water", "melts in a warm room") else "It %s." % p)


def g_table():
    who = P.next()[0]
    test = R.choice(["water", "float", "bend"])
    if test == "water":
        mats = [R.choice(["plastic", "rubber"])] + R.sample(["cloth", "paper", "cardboard", "felt", "a sponge"], 3)
        R.shuffle(mats)
        res = {m: ("soaked through" if m not in ("plastic", "rubber") else "stayed dry underneath") for m in mats}
        q, good = "Which material would make the best raincoat?", [m for m in mats if res[m] == "stayed dry underneath" and m in ("plastic", "rubber")]
        head = "Drop of water on top"
    elif test == "float":
        mats = [R.choice(["wood", "plastic", "cork"])] + R.sample(["metal", "rock", "glass", "clay"], 3)
        R.shuffle(mats)
        res = {m: ("floated" if m in ("wood", "plastic", "cork") else "sank") for m in mats}
        if None in res.values():
            return None
        q, good = "Which material would make the best toy boat?", [m for m in mats if res[m] == "floated"]
        head = "Put in a tub of water"
    else:
        mats = ["rubber"] + R.sample(["wood", "metal", "rock", "glass", "clay brick"], 3)
        R.shuffle(mats)
        res = {m: ("bent" if m == "rubber" else "did not bend") for m in mats}
        q, good = "Which material would make the best garden hose that can bend around corners?", [m for m in mats if res[m] == "bent"]
        head = "Tried to bend it"
    if len(good) != 1 or not once(("tab", test, tuple(sorted(mats)))):
        return None
    tab = table(["Material", head], [[m, res[m]] for m in mats])
    return item(tab + "%s did a test. %s" % (who, q), good[0], [m for m in mats if m != good[0]], "Look at the results. %s %s." % (good[0][0].upper() + good[0][1:], res[good[0]]))


B1 = bank([
    ("What is a property?", "something you can observe about a material, like color or how it feels", ["the name of a person", "the price of a toy", "the weather today"], "Properties: color, shape, hard or soft, and more."),
    ("Which sense do you use to find out if something is rough?", "touch", ["hearing", "taste", "smell"], "Feel it with your fingers."),
    ("Which word tells about color?", "red", ["soft", "bendy", "heavy"], "Red is a color."),
    ("Which is a texture word?", "bumpy", ["blue", "five", "loud"], "Texture is how something feels."),
    ("A window is see-through. What is it made of?", "glass", ["wood", "rock", "cloth"], "Light passes through glass."),
    ("Which is the best way to find out if a material floats?", "put it in water and watch", ["look at its color", "smell it", "guess"], "Test it."),
    ("Why do we sort materials by their properties?", "to choose the right material for a job", ["to make them heavier", "to change their color", "to make them melt"], "Properties help us choose."),
    ("Is something heavy always hard?", "No. A big pillow is heavy but soft.", ["Yes, always.", "Only metal is heavy.", "Heavy things are always soft."], "Heavy and hard are different properties."),
])
B5 = bank([
    ("Ava wants a cup that will not break if it falls. Which is best?", "plastic", ["glass", "paper", "ice"], "Plastic does not shatter."),
    ("Leo wants a blanket that is soft and warm. Which material is best?", "cloth", ["metal", "glass", "rock"], "Cloth is soft."),
    ("Mia wants to see inside a box without opening it. What should the lid be?", "clear plastic", ["wood", "metal", "cardboard"], "You can see through clear plastic."),
    ("Kai tests 4 balls by dropping them. Which property is he testing?", "how bouncy they are", ["their color", "their smell", "their taste"], "He watches how high they bounce."),
    ("Why are pots made of metal?", "Metal is strong and does not melt on the stove.", ["Metal is soft.", "Metal is see-through.", "Metal soaks up water."], "Choose the right property for the job."),
])


def body():
    pic = K.row(["block", "spoon", "sock", "glass"], words=["wood", "metal", "cloth", "glass"], size=90)
    ex = [("Which is see-through: wood, glass or a rock?", ["You can see through it."], "glass"),
          ("A sock is soft and bends. What is it made of?", ["Think about clothes."], "cloth")]
    mist = ["Thinking heavy things are always hard.",
            "Thinking all metal things float. Most metal sinks.",
            "Mixing up color words and texture words."]
    return kid_lesson(pic, "Every material has properties you can see and feel.",
                      ["Look: color, shiny or dull, see-through.", "Touch: hard or soft, rough or smooth, bends or not.",
                       "Test: does it float or sink? Does it soak up water?"], ex, mist)


def main():
    sets = U.sets([
        ("What is it made of?", B1 + [(g_what, 6), (g_true, 6)]),
        ("Hard, soft, rough and smooth", [(g_which, 10), (g_true, 10)]),
        ("Sorting materials", [(g_which, 12), (g_true, 8)]),
        ("Testing materials", [(g_table, 12), (g_which, 4), (g_what, 4)]),
        ("Choosing materials", B5 + [(g_table, 8), (g_which, 4), (g_true, 3)]),
    ])
    make("grade-2", "properties-of-materials", 1, "2-PS1-1",
         "Plan and conduct an investigation to describe and classify different kinds of materials by their observable properties.",
         "Properties of Materials",
         "Grade 2 Properties of Materials Worksheets: Hard, Soft, Floats, Sinks",
         "Properties of Materials",
         "Free grade 2 science worksheets on properties of materials (NGSS 2-PS1-1): hard and soft, rough and smooth, see-through, floats or sinks, and simple tests. 100 picture questions with answers.",
         "Materials have properties.",
         "Look, touch and test: hard or soft, floats or sinks.",
         body(),
         [("What are properties of materials?", "Things you can observe, like color, texture, hard or soft, see-through, and whether it floats or soaks up water."),
          ("How can kids test materials?", "Drop water on them, put them in water, try to bend them, and compare what happens."),
          ("Why do properties matter?", "They help us choose the best material for a job, like plastic for a raincoat.")],
         sets)


if __name__ == "__main__":
    main()
