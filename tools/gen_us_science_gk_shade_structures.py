# -*- coding: utf-8 -*-
"""
US Kindergarten Science: Building Shade (K-PS3-2)
  python tools/gen_us_science_gk_shade_structures.py
Use tools and materials to design and build a structure that will reduce the warming effect of sunlight on an area.
Umbrellas, tents, hats and shade sails; which roof material blocks sunlight (cardboard, thick cloth, foil) and which
does not (clear plastic, a net); testing with ice cubes under each shade.
Very short sentences for 5-6 year olds; almost every question has a picture.
Wrong answers come from real mistakes: "clear plastic makes good shade", "a tiny roof shades a big area", "the shade that melts ice fastest is best".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(9104)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ROOF = {"cardboard": ("#b8875a", 1.0, True), "thick cloth": ("#5a7fc0", 1.0, True), "foil": ("#c9ced6", 1.0, True), "wood": ("#8a5a2b", 1.0, True),
        "clear plastic": ("#dff1fb", 0.35, False), "a net": ("none", 1.0, False), "wax paper": ("#f4f1e8", 0.6, False)}


def shelter_svg(mat, x0=0, lab=None):
    col, op, good = ROOF[mat]
    s = "<line x1='%d' y1='40' x2='%d' y2='110' stroke='%s' stroke-width='3'/>" % (x0 + 40, x0 + 40, INK)
    s += "<line x1='%d' y1='40' x2='%d' y2='110' stroke='%s' stroke-width='3'/>" % (x0 + 140, x0 + 140, INK)
    if mat == "a net":
        s += "".join("<line x1='%d' y1='34' x2='%d' y2='44' stroke='%s'/>" % (x0 + 36 + i * 9, x0 + 44 + i * 9, INK) for i in range(12))
        s += "<rect x='%d' y='34' width='112' height='10' fill='none' stroke='%s'/>" % (x0 + 34, INK)
    else:
        s += "<rect x='%d' y='32' width='112' height='12' fill='%s' opacity='%s' stroke='%s' stroke-width='1.5'/>" % (x0 + 34, col, op, INK)
    if good:
        s += "<ellipse cx='%d' cy='112' rx='56' ry='7' fill='#6d8a5d' opacity='0.6'/>" % (x0 + 90)
    else:
        s += "<path d='M%d 44 L%d 112 L%d 112 L%d 44 Z' fill='#ffe98a' opacity='0.45'/>" % (x0 + 40, x0 + 40, x0 + 140, x0 + 140)
    s += K.icon("ice", x0 + 90, 102, 0.35)
    if lab:
        s += text(x0 + 90, 134, lab, 13)
    return s


def one_svg(mat, label=None):
    return svg_wrap(180, 140 if label else 120, K.icon("sun", 160, 16, 0.4) + shelter_svg(mat, 0, label), "a shade roof made of %s over an ice cube" % mat)


def g_mat():
    mat = R.choice(sorted(ROOF))
    good = ROOF[mat][2]
    who = P.next()[0]
    k = R.choice(["shade", "ice"])
    if not once((mat, k)):
        return None
    pic = fig(one_svg(mat))
    if k == "shade":
        return item(pic + "%s makes a roof of %s. Will it make good shade?" % (who, mat), "Yes. It blocks the sunlight." if good else "No. Sunlight gets through.",
                    ["No. Sunlight gets through." if good else "Yes. It blocks the sunlight.", "Yes. It makes it hotter.", "No. Roofs never help."], "Good shade blocks sunlight.")
    return item(pic + "An ice cube sits under %s's %s roof. Will the ice stay cool?" % (who, mat), "Yes, it stays cool longer." if good else "No, it melts fast.",
                ["No, it melts fast." if good else "Yes, it stays cool longer.", "It turns into a rock.", "It gets bigger."], "Blocking sunlight keeps it cool.")


def g_pick():
    goods = [m for m in ROOF if ROOF[m][2]]
    bads = [m for m in ROOF if not ROOF[m][2]]
    q = R.choice(["best", "worst"])
    if q == "best":
        ms = [R.choice(goods)] + R.sample(bads, 2)
    else:
        ms = R.sample(goods, 2) + [R.choice(bads)]
    R.shuffle(ms)
    if not once((tuple(ms), q)):
        return None
    who = P.next()[0]
    sv = K.icon("sun", 520, 16, 0.4) + "".join(shelter_svg(m, i * 180, "ABC"[i] + ". " + m) for i, m in enumerate(ms))
    pic = svg_wrap(540, 140, sv, "three shade roofs: " + ", ".join(ms))
    a = [m for m in ms if ROOF[m][2] == (q == "best")][0]
    i = ms.index(a)
    return item(fig(pic) + "%s builds 3 shades. Which one is %s?" % (who, "the best shade" if q == "best" else "the worst shade"), "%s (%s)" % ("ABC"[i], a),
                ["%s (%s)" % ("ABC"[j], m) for j, m in enumerate(ms) if j != i] + ["They are all the same."], "%s %s sunlight." % (a[0].upper() + a[1:], "blocks" if q == "best" else "lets in"))


def g_test():
    who = P.next()[0]
    ms = R.sample(sorted(ROOF), 3)
    vals = [R.randint(30, 50) if ROOF[m][2] else R.randint(10, 22) for m in ms]
    if len(set(vals)) < 3:
        return None
    k = R.choice(["best", "worst", "diff"])
    if not once((tuple(ms), k)) or not once(("k", k), 8):
        return None
    tab = table(["Shade roof", "Minutes until the ice melted"], [[m, str(v)] for m, v in zip(ms, vals)])
    if k == "best":
        a = ms[vals.index(max(vals))]
        return item(tab + "%s tested 3 shade roofs with ice. Which roof worked best?" % who, a, [m for m in ms if m != a] + ["They all worked the same."], "The ice lasted longest: %d minutes." % max(vals))
    if k == "worst":
        a = ms[vals.index(min(vals))]
        return item(tab + "%s tested 3 shade roofs with ice. Which roof worked worst?" % who, a, [m for m in ms if m != a] + ["They all worked the same."], "The ice melted fastest: %d minutes." % min(vals))
    x, y = sorted(zip(ms, vals), key=lambda t: -t[1])[0], sorted(zip(ms, vals), key=lambda t: t[1])[0]
    d = x[1] - y[1]
    return item(tab + "In %s's test, how many more minutes did the ice last under %s than under %s?" % (who, x[0], y[0]), str(d), [str(x[1]), str(x[1] + y[1]), str(d + 1)],
                "%d − %d = %d." % (x[1], y[1], d))


NEED = [("The playground slide gets too hot.", "a shade sail over the slide"), ("A dog sits in the hot sun all day.", "a doghouse or a shady roof"),
        ("The car seat is hot after lunch.", "a sunshade in the car window"), ("A small plant wilts in the hot sun.", "a little cloth shade over the plant"),
        ("Kids at the beach are too hot.", "a big beach umbrella"), ("The class garden bench is too hot to sit on.", "a roof over the bench"),
        ("A baby in a stroller is in bright sun.", "a stroller canopy"), ("The bike seat gets very hot.", "a cover or a shady spot for the bike")]


def g_need():
    p, a = R.choice(NEED)
    who = P.next()[0]
    if not once(p):
        return None
    w = R.sample([x[1] for x in NEED if x[1] != a], 2) + ["a fan pointed at the sun"]
    return item("%s sees a problem. %s What is a good solution?" % (who, p), a, w, "Shade blocks the sun's warming.")


FIX = [("Ava's shade is too small. Only part of the sandbox is cool.", "make the roof bigger", ["make the roof smaller", "use clear plastic", "take the roof off"]),
       ("Leo's clear plastic roof does not keep the ice cool.", "use cardboard or thick cloth", ["use more clear plastic", "use a net", "use no roof"]),
       ("Mia's shade falls over in the wind.", "make the poles stronger", ["make the roof clear", "use thinner poles", "take out the poles"]),
       ("Kai's net roof lets sunlight through the holes.", "use a cloth with no holes", ["use a bigger net", "cut more holes", "use no roof"]),
       ("Zoe's shade is in the wrong spot. The sun shines under it from the side.", "move or tilt it to block the sun", ["make it see-through", "paint it", "make it shorter"]),
       ("Sam's paper roof gets wet and falls apart in the rain.", "use a waterproof material", ["use more paper", "use tissue paper", "use a net"])]


def g_fix():
    p, a, w = R.choice(FIX)
    if not once(p):
        return None
    return item("%s How can it be improved?" % p, a, w, "Test, then improve.")


B1 = bank([
    ("What does shade do?", "blocks sunlight so it is cooler", ["makes more light", "makes things hotter", "makes rain"], "Shade keeps us cool."),
    ("Which makes good shade?", "a big umbrella", ["a clear window", "a fishing net", "a glass of water"], "It blocks the sun."),
    ("Why do people wear hats in the sun?", "to shade their face", ["to get hotter", "to see in the dark", "to stay wet"], "A hat is a little shade."),
    ("Which roof lets sunlight through?", "clear plastic", ["cardboard", "wood", "thick cloth"], "You can see through it."),
    ("Why do we test shades with ice?", "to see which shade keeps things coolest", ["to make ice", "to eat it", "to make the sun hot"], "The ice shows the warming."),
    ("Where would you put a shade for a sandbox?", "over the sandbox", ["far away from it", "under the sand", "inside the house"], "Shade the place you need."),
    ("Which shade is bigger and better for a picnic?", "a big tent", ["a tiny hat", "a small leaf", "a straw"], "Big area, big shade."),
    ("What do trees give us on sunny days?", "shade", ["more heat", "snow", "rain"], "Leaves block sunlight."),
])
B5 = bank([
    ("Ava's ice lasted 40 minutes under cardboard and 15 under clear plastic. Which roof was better?", "cardboard", ["clear plastic", "they were the same", "neither"], "Longer is better here."),
    ("Leo builds a shade with sticks and a towel. What does the towel do?", "blocks the sunlight", ["lets all the sunlight in", "makes it rain", "makes it hotter"], "The towel is the roof."),
    ("Mia's shade keeps 1 doll cool, but she has 3 dolls. What should she do?", "make the shade bigger", ["make it smaller", "take it away", "use a net"], "Shade more area."),
    ("Kai wants to test 2 shades fairly. What should be the same?", "the same ice cube size and the same sunny spot", ["a bigger ice cube for one", "one in the shade of a tree", "nothing"], "Fair test."),
    ("Why does a car windshield shade keep the seat cooler?", "It blocks the sunlight coming in.", ["It makes the car colder by blowing air.", "It makes light.", "It adds water."], "Blocking sunlight."),
])


def body():
    sv = K.icon("sun", 340, 16, 0.4) + shelter_svg("cardboard", 0, "cardboard: shade") + shelter_svg("clear plastic", 180, "clear plastic: no shade")
    pic = svg_wrap(360, 140, sv, "a cardboard roof makes shade over ice; a clear plastic roof does not")
    ex = [("Cardboard roof or clear plastic roof: which makes shade?", ["Cardboard blocks light."], "cardboard"),
          ("Ice lasts 40 minutes under shade A and 15 under shade B. Which is better?", ["Longer is better."], "shade A")]
    mist = ["Thinking clear plastic makes good shade.",
            "Thinking a tiny roof can shade a big area.",
            "Picking the shade where the ice melted fastest."]
    return kid_lesson(pic, "Block the sun to make shade.",
                      ["Block the sunlight with a roof.", "Use cardboard, wood or thick cloth.", "Test with ice. Then improve."], ex, mist)


def main():
    sets = U.sets([
        ("What is shade?", B1 + [(g_mat, 6), (g_need, 6)]),
        ("Roof materials", [(g_mat, 8), (g_pick, 8), (g_need, 2), (g_fix, 2)]),
        ("Which shade is best?", [(g_pick, 8), (g_test, 8), (g_fix, 4)]),
        ("Ice tests", [(g_test, 12), (g_pick, 8)]),
        ("Shade builders", B5 + [(g_pick, 11), (g_test, 4)]),
    ])
    make("kindergarten", "shade-structures", 4, "K-PS3-2",
         "Use tools and materials to design and build a structure that will reduce the warming effect of sunlight on an area.",
         "Building Shade",
         "Kindergarten Shade Worksheets: Build a Shade to Block the Sun",
         "Building Shade",
         "Free kindergarten science worksheets on building shade (NGSS K-PS3-2): roofs that block sunlight, testing shades with ice and improving a design. 100 picture questions with answers.",
         "Shade keeps things cool.",
         "A good roof blocks the sunlight. Test it with ice.",
         body(),
         [("What makes good shade?", "A roof that blocks sunlight, like cardboard, wood or thick cloth. Clear plastic and nets let sunlight through."),
          ("How can kids test a shade?", "Put the same ice cube under each shade in the same sunny spot and time how long it takes to melt."),
          ("How can a shade be improved?", "Make it bigger, use a material that blocks light, make the poles stronger or tilt it toward the sun.")],
         sets)


if __name__ == "__main__":
    main()
