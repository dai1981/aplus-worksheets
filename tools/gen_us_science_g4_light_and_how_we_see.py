# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Light and How We See (4-PS4-2)
  python tools/gen_us_science_g4_light_and_how_we_see.py
An object can be seen when light reflects from its surface and enters the eye.
Model: light source -> object -> eye. Mirrors reflect light; we see the moon by reflected sunlight.
Assessment boundary: no specific colors reflected, no how the eye/brain makes an image.
Wrong answers come from real mistakes: "light comes out of the eyes", "we can see in total darkness
if our eyes adjust", "the moon makes its own light".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, line, circle, rect, text, arrow, sun, classifier, People, INK, BLUE, RED, SUN

U = Unit(40107)
R = U.R
P = People(R)
OBJ = ["a ball", "a book", "an apple", "a cat", "a toy car", "a flower", "a shoe", "a cup", "a teddy bear", "a backpack"]


def lamp(x, y):
    return (rect(x - 4, y + 10, 8, 30, "#999", INK, 1.5) + rect(x - 16, y + 40, 32, 6, "#999", INK, 1.5)
            + "<path d='M%d %d L%d %d L%d %d L%d %d Z' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x - 18, y + 12, x - 10, y - 8, x + 10, y - 8, x + 18, y + 12, SUN, INK))


def eye(x, y, flip=False):
    d = -1 if flip else 1
    return ("<path d='M%d %d Q%d %d %d %d Q%d %d %d %d Z' fill='#fff' stroke='%s' stroke-width='2'/>" % (x - 16 * d, y, x, y - 13, x + 16 * d, y, x, y + 13, x - 16 * d, y, INK)
            + circle(x + 3 * d, y, 6, BLUE, INK, 1) + circle(x + 3 * d, y, 2.5, INK, INK, 0))


def thing(x, y):
    return circle(x, y, 16, RED, INK, 2)


def path_pic(kind, tag, inner=False):
    """Lamp at left, object (red ball) at right, eye at bottom-left. kind: right, fromeye, direct, backward."""
    W, H = 200, 150
    L, O, E = (35, 30), (165, 40), (55, 125)
    s = [lamp(*L), thing(*O), eye(*E)]
    if kind == "right":
        s += [arrow(58, 32, 144, 38, ORANGE_, 2.5, 9), arrow(150, 54, 76, 118, ORANGE_, 2.5, 9)]
    elif kind == "fromeye":
        s += [arrow(58, 32, 144, 38, ORANGE_, 2.5, 9), arrow(76, 118, 150, 54, ORANGE_, 2.5, 9)]
    elif kind == "direct":
        s += [arrow(40, 70, 52, 108, ORANGE_, 2.5, 9)]
    else:
        s += [arrow(144, 38, 58, 32, ORANGE_, 2.5, 9), arrow(150, 54, 76, 118, ORANGE_, 2.5, 9)]
    s.append(text(12, 145, tag, 18, "start"))
    if inner:
        return "".join(s)
    return svg_wrap(W, H, "".join(s), "diagram %s" % tag)


ORANGE_ = "#d9822b"
EXPL = {"right": "Light goes from the lamp to the object, bounces off (reflects) and enters the eye.",
        "fromeye": "Light does not come out of our eyes.", "direct": "This only shows light reaching the eye from the lamp, not from the object.",
        "backward": "Light comes from the lamp, not from the object to the lamp."}


def g_paths():
    kinds = ["right", "fromeye", "direct", "backward"]
    R.shuffle(kinds)
    tags = "ABCD"
    g = "".join("<g transform='translate(%d %d)'>%s</g>" % (210 * (i % 2), 160 * (i // 2), path_pic(k, t, True)) for i, (k, t) in enumerate(zip(kinds, tags)))
    g += line(205, 0, 205, 310, "#ccc", 1) + line(0, 155, 410, 155, "#ccc", 1)
    pics = svg_wrap(410, 310, g, "four light path diagrams A, B, C and D").replace("<svg ", "<svg data-pf='lg' ", 1)
    lab = dict(zip(kinds, tags))
    o = R.choice(OBJ)
    return item("<div class='qfig'>%s</div>" % pics + "The red circle is %s in a room lit by a lamp. Which diagram shows how a person sees %s?" % (o, "the " + o.split(" ", 1)[1]),
                lab["right"], [lab[k] for k in kinds if k != "right"], EXPL["right"] + " Diagram %s shows light coming out of the eye, which is wrong." % lab["fromeye"])


def g_one():
    k = R.choice(["right", "fromeye", "backward"])
    pic = fig(path_pic(k, ""))
    o = R.choice(OBJ)
    ok = k == "right"
    return item(pic + "A student drew this model to show how a person sees %s (the red circle) next to a lamp. Is the model correct?" % o,
                "Yes. Light goes from the lamp to the object and reflects into the eye." if ok else
                ("No. The arrow should go from the object to the eye, not out of the eye." if k == "fromeye" else "No. The light should start at the lamp, not at the object."),
                ["Yes. Light comes out of the eye to see the object.", "No. Light does not reflect off objects.", "No. You cannot see objects that are lit."] if ok else
                ["Yes. It shows the light correctly.", "No. There should be no lamp.", "No. Light only travels in curves."],
                EXPL[k] if not ok else EXPL["right"])


SRC = {"a source of light": ["the sun", "a flashlight that is on", "a candle flame", "a lamp that is on", "a firefly glowing", "a campfire", "a lit TV screen", "a star"],
       "not a source of light": ["the moon", "a mirror", "a book", "a white wall", "a bicycle reflector", "a spoon", "a window", "a cloud"]}
s_which, s_what = classifier(R, SRC, "Which of these is {k}?", "Is {x} a source of light, or does it only reflect light?",
                             {"a source of light": "It makes its own light.", "not a source of light": "It does not make light; we see it because light reflects off it."})


def g_dark():
    o = R.choice(OBJ)
    the = "the " + o.split(" ", 1)[1]
    p = P.next()
    place = R.choice(["a closet with the door shut", "a room with no windows and the lights off", "a cave far from the opening", "a box with the lid closed"])
    return item("%s and %s are in %s. There is no light at all. Can %s see %s?" % (p[0], o, place, p[1], the),
                "No. No light can reflect off %s into %s eyes." % (the, p[2]),
                ["Yes, after %s eyes adjust for a long time." % p[2], "Yes, if %s looks very hard." % p[1], "Yes, because %s eyes send out light." % p[2]],
                "We need light to reflect off an object and enter our eyes. In total darkness, there is nothing to see.")


def g_mirror():
    p = P.next()
    pos = "her" if p[1] == "she" else "his"
    k = R.choice(["see", "flash", "angle", "car"])
    if k == "see":
        return item("%s looks in a mirror and sees %s own face. What path does the light take?" % (p[0], pos),
                    "from %s face to the mirror, then back into %s eyes" % (pos, pos), ["from %s eyes to the mirror and back" % pos, "from the mirror to the ceiling", "light goes straight through the mirror"],
                    "Light from the room reflects off the face, bounces off the mirror and enters the eyes.")
    if k == "flash":
        return item("%s shines a flashlight at a mirror on the wall. What happens to the light?" % p[0], "It reflects (bounces) off the mirror.",
                    ["It is all trapped inside the mirror.", "It passes through the wall.", "It turns into sound."], "Smooth, shiny surfaces like mirrors reflect light well.")
    if k == "angle":
        return item("%s wants to see around a corner of a hallway. Which tool would help?" % p[0], "a mirror placed at the corner",
                    ["a black cloth", "a sheet of cardboard", "a brick"], "A mirror reflects light from around the corner into the eye.")
    return item("Why does a car have side mirrors?", "They reflect light from cars behind into the driver's eyes.", ["They make light for driving at night.", "They keep the car cool.", "They make the car faster."],
                "The driver sees what is behind by reflected light.")


B1 = bank([
    ("How do we see an object that does not make its own light?", "Light reflects off the object and enters our eyes.", ["Our eyes send out light to the object.", "The object makes light when we look.", "Sound bounces off the object."],
     "Light source → object → eye."),
    ("Does light come out of our eyes when we look at something?", "No. Light goes into our eyes.", ["Yes, always.", "Only in the dark.", "Only when we blink."],
     "Eyes take in light; they do not send it out."),
    ("Why can we see the moon at night?", "Sunlight reflects off the moon and travels to our eyes.", ["The moon makes its own light.", "Street lights shine on the moon.", "Our eyes light up the moon."],
     "The moon is not a light source. It reflects light from the sun."),
    ("What does reflect mean?", "to bounce off a surface", ["to be made by an object", "to disappear", "to get hotter"], "Light reflects off surfaces like walls, books and mirrors."),
    ("Which surface reflects light best?", "a smooth mirror", ["a black rug", "a dark sweater", "a pile of dirt"], "Smooth, shiny surfaces reflect most light."),
    ("Why is it hard to see in a dim room?", "Only a little light reflects off objects into our eyes.", ["Our eyes stop working.", "Objects disappear.", "Light flows out of our eyes."],
     "Less light means less reflected light reaching our eyes."),
    ("A bike reflector shines at night when car lights hit it. Why?", "It reflects the car's light back toward the driver.", ["It has a battery.", "It makes its own light.", "It is hot."],
     "Reflectors do not make light; they bounce it back."),
    ("In which direction does light travel?", "in straight lines until it hits something", ["only in circles", "only up", "it does not move"], "That is why shadows form."),
])
B5 = bank([
    ("Ava puts a toy in a shoebox with the lid closed and looks through a small hole. She cannot see the toy. Then she opens a second hole to let light in. What happens?", "She can see the toy.", ["She still cannot see it.", "The toy makes light.", "Her eyes give off light."],
     "Light enters through the second hole, reflects off the toy and comes out to her eye."),
    ("Leo says the moon makes its own light because it glows at night. Which fact shows he is wrong?", "The moon's lit side always faces the sun.", ["The moon is round.", "The moon is far away.", "The moon has craters."],
     "The bright part is the part that sunlight is hitting."),
    ("Why do safety vests have shiny strips?", "The strips reflect light from car headlights so drivers can see the worker.", ["The strips make light.", "The strips keep the worker warm.", "The strips are just for decoration."],
     "Reflected light enters the driver's eyes."),
    ("Mia shines a flashlight on a red ball in a dark room. Her friend can now see the ball. What is the best model?", "flashlight → ball → friend's eye", ["friend's eye → ball → flashlight", "ball → flashlight → eye", "flashlight → friend's eye only"],
     "The ball reflects the flashlight's light into the eye."),
    ("Which pair of objects are both sources of light?", "the sun and a lit candle", ["the moon and a mirror", "a book and the sun", "a mirror and a lamp that is off"],
     "Sources make their own light."),
    ("Noah uses two mirrors to make a periscope. What does it let him do?", "see over a wall by reflecting light twice", ["make light in the dark", "hear sounds better", "see through the wall"],
     "Each mirror reflects light toward the next, and then into his eye."),
])


def body():
    think = ("<p>We see an object when <b>light reflects</b> (bounces) off it and <b>enters our eyes</b>. "
             "Light comes from a <b>source</b>, like the sun or a lamp. Our eyes do not send out light.</p>"
             + figure(path_pic("right", ""), "Lamp → object → eye.")
             + "<p>Most things, like books, walls and the moon, do not make their own light. We see them because they reflect light. "
             "Smooth, shiny surfaces like mirrors reflect light very well. In total darkness we cannot see anything, because no light can reach our eyes.</p>")
    ex = [("How do you see a book on your desk?", ["The lamp or sun lights the book.", "Light reflects off the book.", "The light enters your eyes."], "light source → book → eye"),
          ("Why can we see the moon?", ["The moon does not make light.", "It reflects sunlight."], "Sunlight reflects off the moon into our eyes.")]
    mist = ["Drawing arrows from the eye to the object. Light goes into the eye.",
            "Thinking the moon makes its own light.",
            "Thinking eyes can see in total darkness after they adjust."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("How we see", B1 + [(g_one, 4), (g_dark, 4), (g_paths, 4)]),
        ("Modeling light paths", [(g_paths, 8), (g_one, 8), (g_dark, 4)]),
        ("Sources and reflectors", [(s_which, 8), (s_what, 8), (g_mirror, 4)]),
        ("Mirrors and reflection", [(g_mirror, 8), (s_what, 6), (g_one, 6)]),
        ("Investigations", B5 + [g_paths, g_dark, g_mirror, s_which]),
    ])
    make("grade-4", "light-and-how-we-see", 7, "4-PS4-2",
         "Develop a model to describe that light reflecting from objects and entering the eye allows objects to be seen.",
         "Light and How We See",
         "Grade 4 Light Worksheets: How We See Objects, Reflection and Light Sources",
         "Light and Seeing",
         "Free Grade 4 science worksheets on light and how we see (NGSS 4-PS4-2): light reflecting off objects into the eye, light sources and reflectors, mirrors, the moon and light path models. 100 practice questions with answers.",
         "We see things when light reflects off them into our eyes.",
         "Light goes from a source, like the sun or a lamp, to an object, and then bounces into our eyes. Eyes do not send out light.",
         body(),
         [("How do we see objects?", "Light from a source like the sun or a lamp reflects off the object and enters our eyes."),
          ("Does the moon make its own light?", "No. The moon reflects sunlight. That is why the lit part of the moon always faces the sun."),
          ("Can you see in total darkness?", "No. Without light, no light can reflect off objects into your eyes.")],
         sets)


if __name__ == "__main__":
    main()
