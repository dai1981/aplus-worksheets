# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Light and Seeing (1-PS4-2)
  python tools/gen_us_science_g1_light_and_seeing.py
Make observations to construct an evidence-based account that objects in darkness can be seen only when illuminated.
Light sources (sun, lamp, flashlight, fire, fireflies) give off light; other things are seen when light bounces off them.
A closed box, a dark closet, a cave. Very short sentences for 6-7 year olds, many pictures.
Wrong answers come from real mistakes: "cats see in total darkness", "the moon makes its own light", "eyes make light".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(10102)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


SRC = {"sun": True, "star": True, "flashlight": True, "moon": False, "mirror": False, "apple": False, "ball": False, "cup": False, "rock": False, "crayon": False}
NM = {"sun": "sun", "star": "star", "flashlight": "flashlight", "moon": "moon", "mirror": "mirror", "apple": "apple", "ball": "ball", "cup": "cup", "rock": "rock", "crayon": "crayon"}


def g_src():
    k = R.choice(sorted(SRC))
    who = P.next()[0]
    if not once(("s", k)):
        return None
    yes = SRC[k]
    if k == "moon":
        return item(fig(K.card("moon")) + "%s sees the moon shine at night. Does the moon make its own light?" % who, "No. It reflects light from the sun.",
                    ["Yes. It is a light source.", "Yes. It is a big lamp.", "No. It is dark, so we never see it."], "Sunlight bounces off the moon.")
    if k == "mirror":
        return item(fig(K.card("mirror")) + "%s's mirror looks bright. Is a mirror a light source?" % who, "No. It bounces light.",
                    ["Yes. It makes light.", "Yes. It is like the sun.", "No. It is always dark."], "Mirrors reflect light.")
    return item(fig(K.card(k)) + "%s looks at a %s. Does it give off its own light?" % (who, NM[k]), "yes" if yes else "no", ["no" if yes else "yes", "only on Tuesdays", "only when it is cold"],
                ("A %s is a light source." if yes else "A %s does not make light. We see it when light bounces off it.") % NM[k])


def g_pick():
    src = R.choice(["sun", "star", "flashlight"])
    others = R.sample([k for k in SRC if not SRC[k]], 3)
    kinds = [src] + others
    R.shuffle(kinds)
    if not once(("p", tuple(kinds))):
        return None
    L = "ABCD"
    who = P.next()[0]
    neg = R.random() < 0.3
    pic = K.row(kinds, words=["%s. %s" % (L[i], NM[k]) for i, k in enumerate(kinds)], size=90)
    a = "%s (%s)" % (L[kinds.index(src)], NM[src])
    return item(fig(pic) + "%s looks at these. Which one makes its own light?" % who, a, ["%s (%s)" % (L[i], NM[k]) for i, k in enumerate(kinds) if k != src],
                "A %s is a light source." % NM[src])


def box_svg(lit, thing):
    s = "<rect x='20' y='20' width='240' height='110' fill='%s' stroke='%s' stroke-width='2.5'/>" % ("#fff8d6" if lit else "#1f2430", INK)
    if lit:
        s += K.icon("flashlight", 60, 40, 0.6) + "<path d='M80 44 L240 30 L240 120 Z' fill='#ffe98a' opacity='0.55'/>"
        s += K.icon(thing, 190, 86, 0.8)
    s += "<circle cx='20' cy='75' r='6' fill='#000' stroke='%s'/>" % INK
    s += text(140, 150, "flashlight on" if lit else "lid closed, no light", 13, weight=400)
    return svg_wrap(280, 160, s, "a box with a peephole: %s" % ("a flashlight lights up a %s inside" % NM[thing] if lit else "dark inside"))


def g_box():
    lit = R.random() < 0.5
    thing = R.choice(["apple", "ball", "cup", "crayon"])
    who = P.next()[0]
    if not once(("b", lit, thing)):
        return None
    pic = fig(box_svg(lit, thing))
    if lit:
        return item(pic + "%s peeks in the hole. The flashlight is on. Can %s see the %s?" % (who, who, NM[thing]), "Yes. Light shines on it.",
                    ["No. Boxes are always dark.", "No. Eyes cannot see in boxes.", "Yes. The %s makes light." % NM[thing]], "Light bounces off the %s into our eyes." % NM[thing])
    return item(pic + "There is a %s in the dark box. %s peeks in. What does %s see?" % (NM[thing], who, who), "nothing; it is too dark",
                ["the %s, very clearly" % NM[thing], "the %s glowing" % NM[thing], "a rainbow"], "With no light, we cannot see.")


PLACES = [("in a closet with the door shut", False), ("in a cave with no light", False), ("in a room at night with the lights off and no windows", False),
          ("on a sunny playground", True), ("in a room with a lamp on", True), ("in a tent with a flashlight on", True), ("in a dark basement with a candle lit", True),
          ("in a closed toy box", False), ("at a campsite next to a fire", True), ("in a sealed cardboard box", False)]
OBJS = ["a red ball", "a teddy bear", "a book", "a shoe", "a toy car", "a hat"]


def g_place():
    pl, lit = R.choice(PLACES)
    ob = R.choice(OBJS)
    who = P.next()[0]
    if not once(("pl", pl)):
        return None
    if lit:
        return item("%s puts %s %s. Can %s see it?" % (who, ob, pl, who), "Yes. There is light.", ["No. It is too dark.", "Only with eyes closed.", "No. It hides."],
                    "Light shines on it, so we can see it.")
    return item("%s puts %s %s. Can %s see it?" % (who, ob, pl, who), "No. There is no light.", ["Yes. Eyes make light.", "Yes, very clearly.", "Yes, if you look hard."],
                "We need light to see.")


HOW = [("How can Ava see her toy in a dark closet?", "turn on a light", ["close her eyes", "shut the door", "whisper"], "Light helps us see."),
       ("How can Leo read a book in a dark tent?", "use a flashlight", ["hold it closer", "close the tent", "shake the book"], "Add light."),
       ("How can Mia find her shoe under the bed?", "shine a flashlight under the bed", ["turn off the lamp", "close her eyes", "count to ten"], "Shine light on it."),
       ("How can Kai see a fish in a dark aquarium?", "turn on the aquarium light", ["tap the glass", "turn off the room lights", "shout"], "Light it up."),
       ("How can Sam see stairs at night?", "turn on the stair light", ["walk faster", "wear sunglasses", "close his eyes"], "Light shines on the stairs."),
       ("How can Zoe see bugs in a dark log?", "shine a light into the log", ["cover the log", "shake her head", "wait in the dark"], "Light bounces off the bugs.")]


def g_how():
    q, a, w, e = R.choice(HOW)
    if not once(q):
        return None
    return item(q, a, w, e)


TXT = [("a candle flame", True), ("lightning", True), ("a TV screen that is on", True), ("a firefly", True), ("a glow stick", True), ("a campfire", True),
       ("a spoon", False), ("a window", False), ("white paper", False), ("fresh snow", False), ("a shiny car", False), ("a lake", False), ("a bike reflector", False)]


def g_src2():
    t, yes = R.choice(TXT)
    who = P.next()[0]
    if not once(("t", t)):
        return None
    if yes:
        return item("%s sees %s in the dark. Is it a light source?" % (who, t), "Yes. It makes its own light.", ["No. It only reflects light.", "No. Nothing makes light.", "Yes, but only in the day."],
                    "%s gives off light." % (t[0].upper() + t[1:]))
    return item("%s sees %s shine. Is it a light source?" % (who, t), "No. Light bounces off it.", ["Yes. It makes its own light.", "Yes. It is like the sun.", "No. We can never see it."],
                "%s reflects light." % (t[0].upper() + t[1:]))


PATH = [("a lamp", "a book"), ("the sun", "a tree"), ("a flashlight", "a cat"), ("a candle", "a cake"), ("the sun", "a car"), ("a lamp", "a puzzle"),
        ("a flashlight", "a map"), ("the sun", "a flower"), ("a campfire", "a tent"), ("a lamp", "a doll")]


def g_path():
    src, ob = R.choice(PATH)
    who = P.next()[0]
    if not once((src, ob)):
        return None
    good = "%s → %s → eyes" % (src, ob)
    w = ["eyes → %s → %s" % (ob, src), "%s → %s → eyes" % (ob, src), "eyes → %s → %s" % (src, ob)]
    return item("%s sees %s lit by %s. How does the light travel?" % (who, ob, src), good, w, "Light goes from the source, bounces off %s, then into the eyes." % ob)


def g_more():
    a = R.choice([p for p in PLACES if p[1]])
    b = R.choice([p for p in PLACES if not p[1]])
    who = P.next()[0]
    if not once((a[0], b[0])) or not once(("m", a[0]), 2) or not once(("mb", b[0]), 2):
        return None
    x, y = (a, b) if R.random() < 0.5 else (b, a)
    return item("%s lost a toy. Where can %s see it: %s or %s?" % (who, who, x[0], y[0]), a[0], [b[0], "in both places", "in neither place"], "There is light %s." % a[0])


B1 = bank([
    ("What do we need to see things?", "light", ["sound", "wind", "darkness"], "No light, no seeing."),
    ("Which is a light source?", "a lamp", ["a book", "a rock", "a sock"], "A lamp makes light."),
    ("Can you see in a room with no light at all?", "no", ["yes, clearly", "only colors", "yes, if you squint"], "We need light."),
    ("Where does daytime light come from?", "the sun", ["the moon", "a mirror", "the clouds"], "The sun is our biggest light source."),
    ("Why can we see a book in a lit room?", "Light bounces off it into our eyes.", ["The book makes light.", "Our eyes make light.", "Books glow."], "Light bounces."),
    ("Which one makes its own light?", "a campfire", ["a spoon", "a pillow", "a window"], "Fire gives off light."),
    ("Does the moon make light?", "No. It reflects the sun's light.", ["Yes.", "Yes, it is a lamp.", "Only in winter."], "The moon is lit by the sun."),
    ("Which bug makes its own light?", "a firefly", ["an ant", "a ladybug", "a bee"], "Fireflies glow."),
])
B5 = bank([
    ("Ava looks in a closed box with a peephole. She sees nothing. Then she opens the lid. Now she sees a toy. Why?", "Light came in.", ["The toy moved.", "The toy started to glow.", "Her eyes got bigger."], "Light makes seeing possible."),
    ("Leo says cats can see in total darkness. Is he right?", "No. Cats need a little light too.", ["Yes.", "Yes, cats make light.", "No, cats cannot see at all."], "All eyes need light."),
    ("Mia turns off the lamp in a room with no windows. What can she see?", "nothing", ["everything", "only red things", "her toys glowing"], "No light, no seeing."),
    ("Kai shines a flashlight on a wall. Is the wall a light source?", "No. The wall reflects the light.", ["Yes.", "Yes, walls glow.", "Only white walls."], "Only the flashlight makes light."),
    ("Which is the best evidence that we need light to see?", "In a dark box we see nothing; with light we see the toy.", ["Toys are fun.", "Boxes are brown.", "Lamps are tall."], "Test with and without light."),
])


def body():
    pic = "<div style='display:flex;gap:12px;flex-wrap:wrap'>%s%s</div>" % (box_svg(False, "ball"), box_svg(True, "ball"))
    ex = [("A toy is in a dark box. Can you see it?", ["There is no light."], "no"),
          ("A flashlight shines in the box. Can you see the toy?", ["Light bounces off the toy."], "yes")]
    mist = ["Thinking eyes make light.",
            "Thinking the moon makes its own light.",
            "Thinking some animals see in total darkness."]
    return kid_lesson(pic, "Is there light? Then we can see.",
                      ["No light: we see nothing.", "Light sources make light: sun, lamp, fire.", "Light bounces off things into our eyes."], ex, mist)


def main():
    sets = U.sets([
        ("Light sources", B1 + [(g_src, 6), (g_pick, 6)]),
        ("Light or no light?", [(g_place, 10), (g_box, 4), (g_src, 4), (g_src2, 2)]),
        ("The dark box", [(g_box, 4), (g_pick, 6), (g_how, 6), (g_src2, 4)]),
        ("How we see", [(g_path, 10), (g_src2, 7), (g_more, 3)]),
        ("Light scientists", B5 + [(g_more, 8), (g_pick, 7)]),
    ])
    make("grade-1", "light-and-seeing", 2, "1-PS4-2",
         "Make observations to construct an evidence-based account that objects in darkness can be seen only when illuminated.",
         "Light and Seeing",
         "Grade 1 Light and Seeing Worksheets: We Need Light to See",
         "Light and Seeing",
         "Free grade 1 science worksheets on light and seeing (NGSS 1-PS4-2): light sources, dark boxes and how light helps us see. 100 picture questions with answers.",
         "We need light to see.",
         "Light comes from a source and bounces off things into our eyes.",
         body(),
         [("Why can't we see in the dark?", "We see things when light bounces off them into our eyes. With no light, nothing bounces."),
          ("What is a light source?", "Something that makes its own light, like the sun, a lamp, a flashlight, fire or a firefly."),
          ("Does the moon make light?", "No. The moon reflects light from the sun.")],
         sets)


if __name__ == "__main__":
    main()
