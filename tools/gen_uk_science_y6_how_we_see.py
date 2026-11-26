# -*- coding: utf-8 -*-
"""
UK Year 6 science: How We See (Light)
  python tools/gen_uk_science_y6_how_we_see.py
We see things because light travels from a source into our eyes, or from a source to an object and then into our
eyes. Ray diagrams (drawn new each time), why we cannot see in total darkness, parts of the eye, and pupil size.
Wrong answers come from real mistakes: "light comes out of our eyes", "we can see in total darkness after a while",
"non-luminous objects give out light", "the pupil gets bigger in bright light".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once, fig
from uk_sci_pics import seeing
from sci_phys import uniq

U = Unit(61611)
R = U.R
P = People(R)

PAIRS = [("lamp", "book"), ("Sun", "tree"), ("torch", "cat"), ("candle", "cup"), ("lamp", "apple"), ("Sun", "football"), ("torch", "teddy bear"), ("lamp", "vase"), ("Sun", "flower"), ("candle", "mouse")]
OK = "It is correct: light travels from the source to the object, then into the eye."
CONF = [([("S", "O"), ("O", "E")], OK),
        ([("S", "O"), ("E", "O")], "The second arrow points the wrong way: light goes into the eye, not out of it."),
        ([("O", "E")], "It is missing the light travelling from the source to the object."),
        ([("S", "E")], "It shows the source being seen, not how light from the object reaches the eye."),
        ([("E", "O")], "Light does not come out of eyes, and the light from the source is missing.")]


def g_diag():
    src, obj = R.choice(PAIRS)
    i = R.randrange(len(CONF))
    rays, a = CONF[i]
    who = P.next()[0]
    if not once(("dg", src, obj, i)):
        return None
    w = [c for _, c in CONF if c != a]
    return item(fig(seeing(src, obj, rays, "diagram of how light might travel from a %s to a %s and an eye" % (src.lower(), obj))) +
                "%s drew this diagram to explain how we see the %s. Is it correct?" % (who, obj), a, R.sample(w, 3), "To see a non-luminous object, light must go from the source to the object and then into the eye.")


LUM = ["a lit candle", "the Sun at sunset", "a torch shining at you", "a computer screen", "a traffic light"]
NON = ["a book", "a red bus", "your friend's face", "the Moon", "a white wall", "a tree", "a cat", "a road sign"]


def g_why():
    k = R.random() < 0.4
    if k:
        a = R.choice(LUM)
        if not once(("wl", a)):
            return None
        return item("Why can you see %s?" % a, "Light travels from it straight into your eyes.", ["Light from your eyes lands on it.", "It reflects light from your eyes.", "It makes a sound you can see."],
                    "Light sources give out light that enters our eyes directly.")
    a = R.choice(NON)
    if not once(("wn", a)):
        return None
    return item("Why can you see %s?" % a, "Light from a source reflects off it into your eyes.", ["It gives out its own light.", "Light shines out of your eyes onto it.", "Your eyes can see without light."],
                "%s does not make light; it reflects light into our eyes." % (a[0].upper() + a[1:]))


EYE = [("the pupil", "the hole that lets light into the eye"), ("the iris", "the coloured part that changes the size of the pupil"),
       ("the lens", "focuses light onto the back of the eye"), ("the retina", "detects light at the back of the eye"),
       ("the optic nerve", "carries signals from the eye to the brain"), ("the cornea", "the clear front window of the eye")]


def g_eye():
    p, j = R.choice(EYE)
    k = R.random() < 0.5
    if not once(("ey", p, k)):
        return None
    if k:
        return item("Which description matches %s?" % p, j, R.sample([x[1] for x in EYE if x[0] != p], 3), "%s: %s." % (p[0].upper() + p[1:], j))
    return item("Which part of the eye is %s?" % j, p, R.sample([x[0] for x in EYE if x[0] != p], 3), "%s: %s." % (p[0].upper() + p[1:], j))


def g_pupil():
    who = P.next()[0]
    rows = [("in a dark room", R.choice([6, 7, 8])), ("in the classroom", R.choice([4, 5])), ("outside on a cloudy day", R.choice([3, 4])), ("in bright sunshine", 2)]
    if rows[1][1] <= rows[2][1]:
        return None
    k = R.choice(["big", "small", "read", "read", "why", "diff"])
    ri = R.randrange(4)
    if not once(("pu", k, ri if k == "read" else 0, tuple(v for _, v in rows))) or (k in ("big", "small", "why") and not once(("pk", k), 2)):
        return None
    tab = table(["Where", "Pupil width (mm)"], [[a, str(b)] for a, b in rows])
    intro = tab + "%s measured a friend's pupil in different light. " % who
    if k == "big":
        return item(intro + "Where was the pupil widest?", "in a dark room", ["in the classroom", "outside on a cloudy day", "in bright sunshine"], "Pupils open wide in dim light to let more light in.")
    if k == "small":
        return item(intro + "Where was the pupil narrowest?", "in bright sunshine", ["in a dark room", "in the classroom", "outside on a cloudy day"], "Pupils shrink in bright light to protect the eye.")
    if k == "read":
        a, b = rows[ri]
        g = "%d mm" % b
        return item(intro + "How wide was the pupil %s?" % a, g, uniq(g, ["%d mm" % v for _, v in rows] + ["%d mm" % (b + 1)]), "Read the row: %s." % a)
    if k == "diff":
        d = rows[0][1] - rows[3][1]
        g = "%d mm" % d
        return item(intro + "How much wider was the pupil in a dark room than in bright sunshine?", g, uniq(g, ["%d mm" % rows[0][1], "%d mm" % (rows[0][1] + 2), "%d mm" % (d + 1), "2 mm"]),
                    "%d − 2 = %d mm." % (rows[0][1], d))
    return item(intro + "What pattern does the table show?", "The brighter the light, the smaller the pupil.", ["The brighter the light, the bigger the pupil.", "The pupil never changes.", "Pupils only change in the dark."],
                "The iris controls how much light enters.")


B1 = bank([
    ("How do we see an object that is not a light source?", "Light from a source reflects off the object into our eyes.", ["Light comes out of our eyes.", "The object gives out its own light.", "We see without any light."], "Source → object → eye."),
    ("Can you see anything in a room with no light at all?", "No, because no light can reflect into your eyes.", ["Yes, after your eyes get used to it.", "Yes, if you stare hard.", "Only white objects."], "Total darkness means no light."),
    ("In a ray diagram, which way should the arrows point?", "in the direction light travels: from the source towards the eye", ["from the eye to the object", "both ways at once", "it does not matter"], "Light enters the eye."),
    ("What does 'luminous' mean?", "gives out its own light", ["reflects light well", "lets light through", "has no colour"], "The Sun is luminous."),
    ("Why can you see the Moon at night?", "Sunlight reflects off the Moon into your eyes.", ["The Moon makes its own light.", "Your eyes light up the Moon.", "Stars shine on it from behind."], "The Moon is non-luminous."),
    ("Which part of the eye lets light in?", "the pupil", ["the eyelash", "the eyebrow", "the optic nerve"], "The black circle in the middle."),
    ("Why do cats seem to see in very dim light?", "Their pupils open very wide and their eyes reflect light inside.", ["They give out light from their eyes.", "They do not need light.", "They see with their whiskers."], "They still need some light."),
    ("Why do we wear sunglasses in bright sun?", "to reduce the light entering our eyes and protect them", ["to see in the dark", "to make the Sun brighter", "to stop sound"], "Protect the eyes."),
])
B5 = bank([
    ("A pupil says, 'We see because light comes out of our eyes.' Which evidence shows this is wrong?", "We cannot see anything in a completely dark room.", ["We can see the Sun.", "Our eyes are round.", "We blink."], "If light came from eyes, we could see in the dark."),
    ("Why are road signs made with reflective paint?", "They reflect car headlights back to the driver's eyes.", ["They make their own light.", "They absorb all light.", "They glow in the dark forever."], "More light reaches the eyes."),
    ("How could you test which material is best for a reflective armband?", "Shine the same torch on each in a dark room and compare how bright they look from the same distance.", ["Wear them in the daytime only.", "Weigh them.", "Use a different torch for each."], "Fair test."),
    ("Why is it harder to read a book by moonlight than by a lamp?", "Less light reaches the book, so less is reflected into your eyes.", ["Moonlight is too fast.", "Books cannot reflect moonlight.", "The Moon is a light source."], "Amount of light."),
    ("Why do opticians shine a light into your eye?", "to see the pupil get smaller and check the eye is working", ["to make the eye grow", "to dry the eye", "to change eye colour"], "Pupil reflex."),
])


def body():
    think = ("<p><b>We see things when light enters our eyes.</b></p>"
             "<ul><li>Light sources (luminous): light travels straight from them into our eyes.</li>"
             "<li>Other objects: light from a source reflects off them and travels into our eyes.</li>"
             "<li>In ray diagrams, arrows go from the source, to the object, to the eye, never out of the eye. With no light at all, we see nothing.</li></ul>")
    ex = [("How do you see a book under a lamp?", ["Lamp → book", "Book → eye"], "light reflects off the book into your eye"),
          ("Dark room or bright sunshine: bigger pupil?", ["Pupils open to let in more light"], "dark room")]
    mist = ["Drawing arrows coming out of the eye.", "Thinking you can see in total darkness after a while.", "Thinking objects like the Moon give out their own light."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("How we see", B1 + [(g_why, 6), (g_eye, 6)]),
        ("Seeing objects", [(g_why, 4), (g_diag, 16)]),
        ("Ray diagrams", [(g_diag, 14), (g_why, 3), (g_eye, 3)]),
        ("The eye", [(g_eye, 3), (g_pupil, 17)]),
        ("Thinking about seeing", B5 + [(g_diag, 8), (g_pupil, 7)]),
    ])
    make_uk(6, "how-we-see", 11, "Light",
            "Use the idea that light travels in straight lines to explain that objects are seen because they give out or reflect light into the eye. "
            "Explain that we see things because light travels from light sources to our eyes or from light sources to objects and then to our eyes.",
            "How We See",
            "Year 6 Science: How We See Worksheets (Ray Diagrams, Reflection and the Eye)",
            "How We See",
            "Free Year 6 science worksheets on how we see: light travelling into the eye, ray diagrams, luminous and non-luminous objects, parts of the eye and pupil size. 100 questions with answers.",
            "We see when light enters our eyes.",
            "Light goes from a source, bounces off objects, and travels into the eye.",
            body(),
            [("How do we see things?", "Light from a light source either goes straight into our eyes, or reflects off an object and then travels into our eyes."),
             ("Which way should arrows point in a ray diagram?", "From the light source to the object and from the object to the eye, showing the direction light travels. Arrows never come out of the eye."),
             ("Why can't we see in total darkness?", "With no light, nothing can reflect into our eyes, so we cannot see anything at all.")],
            sets)


if __name__ == "__main__":
    main()
