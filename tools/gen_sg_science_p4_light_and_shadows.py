# -*- coding: utf-8 -*-
"""
Singapore Primary 4 science: Light and shadows (Energy)
  python tools/gen_sg_science_p4_light_and_shadows.py
We see an object when it gives out light or reflects light into our eyes. Light sources (the Sun, a torch) and objects that
only reflect light (the Moon, a mirror). Materials are transparent, translucent or opaque. A shadow forms when an opaque
object blocks light; light travels in straight lines, and the shadow gets bigger as the object moves nearer the light.
UK Year 3 and Year 6 light questions are reused with Singapore names (no angles of reflection, no speed of light);
light-sensor experiments are written here.
Wrong answers come from real mistakes: "the Moon is a light source", "we see because light comes out of our eyes",
"a translucent object makes no shadow", "the shadow is bigger when the object is nearer the screen".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63404)
R = U.R
P = People(R)
D = ["winter", "snow", "bonfire", "UK", "normal"]
LD = use(U, "gen_uk_science_y3_light_and_dark", drop=D)
SH = use(U, "gen_uk_science_y3_shadows", drop=D)
LT = use(U, "gen_uk_science_y6_how_light_travels", drop=D)
SR = use(U, "gen_uk_science_y6_shadows_and_reflection", drop=D)


def g_sensor():
    mats = {"clear glass": (85, 95), "clear plastic": (80, 90), "frosted glass": (40, 55), "tracing paper": (30, 45), "tissue paper": (20, 35),
            "cardboard": (0, 0), "aluminium foil": (0, 0), "wood": (0, 0)}
    pick = R.sample(sorted(mats), 4)
    vals = [R.randint(*mats[m]) for m in pick]
    if len(set(vals)) < 4 and vals.count(0) < 2:
        return None
    if vals.count(0) > 1:
        return None
    k = R.choice(["opaque", "transparent", "translucent", "window", "var", "same"])
    if not once(("se", k, tuple(sorted(pick)))) or not once(("sen", k), 1 if k in ("var", "same") else 3):
        return None
    tb = table(["Material", "Light-sensor reading (units)"], [[m, str(v)] for m, v in zip(pick, vals)])
    q0 = "%s placed four materials of the same thickness, one at a time, between a torch and a light sensor.<br>%s" % (P.next()[0], tb)
    s = sorted(zip(vals, pick))
    if k == "opaque":
        if s[0][0] != 0:
            return None
        return item(q0 + "Which material is opaque?", s[0][1], [m for _, m in s[1:]], "An opaque material lets no light through, so the reading is 0.")
    if k == "transparent":
        if s[-1][0] < 75 or s[-2][0] >= 75:
            return None
        return item(q0 + "Which material is most likely transparent?", s[-1][1], [m for _, m in s[:-1]], "A transparent material lets most light through.")
    if k == "translucent":
        mid = [m for v, m in s if 15 <= v <= 60]
        if len(mid) != 1:
            return None
        return item(q0 + "Which material is translucent?", mid[0], [m for v, m in s if m != mid[0]], "A translucent material lets some light through.")
    if k == "window":
        return item(q0 + "Which material would be best for a window that people can see through clearly?", s[-1][1], [m for _, m in s[:-1]],
                    "It lets the most light through.")
    if k == "var":
        return item(q0 + "What did the light sensor measure?", "the amount of light passing through each material",
                    ["the thickness of each material", "the heat of the torch", "the colour of each material"], "A higher reading means more light passed through.")
    return item(q0 + "Why were the materials the same thickness?", "so that only the type of material was changed",
                ["so that the torch was brighter", "so that the sensor was warmer", "so that the readings were all 0"], "This makes the test fair.")


B1 = bank([
    ("How do we see an object that is not a light source, such as a book?", "Light from a light source reflects off the book into our eyes.", ["Light comes out of our eyes and hits the book.", "The book gives out its own light.", "We do not need light to see it."], "Light must enter our eyes."),
    ("Why is the Moon NOT a light source?", "It reflects light from the Sun.", ["It is too far away.", "It only shines at night.", "It is made of rock, so it glows."], "The Moon has no light of its own."),
    ("Which of these is a light source?", "a lit candle", ["a mirror", "the Moon", "a white wall"], "A light source gives out its own light."),
    ("What is an opaque material?", "a material that does not let light pass through", ["a material that lets all light through", "a material that lets some light through", "a material that gives out light"], "Wood and metal are opaque."),
    ("What is a translucent material?", "a material that lets some light pass through", ["a material that lets no light through", "a material that lets almost all light through", "a material that gives out light"], "Frosted glass and tracing paper are translucent."),
    ("Which shows that light travels in straight lines?", "Shadows have sharp edges with the same outline as the object.", ["Light can bend around corners.", "Light is bright.", "Light makes things warm."], "Light cannot bend round the object."),
])
B5 = bank([
    ("Why are the windows of HDB bathrooms often made of frosted glass?", "Frosted glass lets light in but people cannot see in clearly.", ["It lets no light in.", "It is transparent.", "It reflects all light."], "Frosted glass is translucent."),
    ("A shadow of a lamp post at a bus stop is longest at which time of the day?", "early morning or late afternoon", ["at noon", "at midnight", "it is the same all day"], "The Sun is low in the sky then."),
    ("Siti moved a torch further away from a toy, keeping the toy and the screen in place. What happened to the shadow?", "It became smaller.", ["It became bigger.", "It disappeared.", "It stayed the same."], "The toy blocks a smaller part of the light when the torch is far."),
    ("Why does a cardboard puppet in a shadow puppet show make a darker shadow than a tissue paper puppet?", "Cardboard is opaque, so it blocks all the light; tissue paper lets some through.", ["Cardboard gives out dark light.", "Tissue paper is opaque.", "Cardboard reflects all light into the screen."], "Opaque objects make darker shadows."),
    ("A pupil shone a torch at a mirror in a dark room and saw a bright spot on the wall. What does this show?", "Light reflects off shiny surfaces.", ["Mirrors are light sources.", "Light travels in curves.", "Walls give out light."], "The mirror reflected the torch's light."),
])


def body():
    think = ("<p><b>We see an object when light from it enters our eyes.</b> The light is either given out by the object (a light source) or reflected from it.</p>"
             "<ul><li><b>Transparent</b> materials let most light through; <b>translucent</b> materials let some light through; <b>opaque</b> materials let no light through.</li>"
             "<li>A <b>shadow</b> forms when an object blocks light. Light travels in straight lines, so the shadow has the outline of the object.</li>"
             "<li>The nearer the object is to the light, the bigger its shadow.</li></ul>")
    ex = [("Is the Moon a light source?", ["It does not give out its own light", "It reflects light from the Sun"], "No."),
          ("A toy is moved nearer a torch. What happens to its shadow?", ["It blocks more of the light", "The shadow gets bigger"], "It gets bigger.")]
    mist = ["Thinking the Moon and mirrors are light sources. They only reflect light.",
            "Thinking we see because light comes out of our eyes. Light must enter our eyes.",
            "Thinking translucent objects make no shadow. They make a lighter shadow.",
            "Thinking a shadow gets bigger when the object moves nearer the screen. It gets bigger when the object moves nearer the light."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Light sources and seeing", B1 + LD.B1 + [(LT.g_src, 3), (LT.g_srcyn, 3)]),
        ("Reflecting light", LD.BR + [(LD.g_refl, 4), (LD.g_dark, 4), (LT.g_src, 2), (SR.g_peri, 2)]),
        ("Transparent, translucent or opaque", LT.B1 + [(LT.g_mat, 5), (LT.g_def, 4), (g_sensor, 3)]),
        ("Shadows", SH.B1 + [(SH.g_side, 4), (SH.g_size, 3), (SR.g_shape, 3), (SR.g_shd, 2)]),
        ("PSLE-style investigations", B5 + SH.B5 + [(g_sensor, 5), (SR.g_shd, 5)]),
    ])
    make_sg(4, "light-and-shadows", 4, "Energy", "Energy forms and uses (Light)",
            "Recognise that an object can be seen when it reflects light or when it is a source of light. Recognise that a shadow is formed when light is "
            "completely or partially blocked by an object, and investigate how materials let light through (transparent, translucent, opaque) "
            "(summary of the MOE Primary Science Syllabus).",
            "Light and Shadows",
            "Primary 4 Science: Light and Shadows Worksheets (with Answers)",
            "Light and shadows",
            "Free Primary 4 science worksheets for Singapore pupils on light: light sources, how we see, transparent, translucent and opaque materials, and shadows. 100 questions with answers.",
            "We see things when light enters our eyes.",
            "A shadow forms when an object blocks light.",
            body(),
            [("Why is the Moon not a light source?", "The Moon does not give out its own light. It reflects light from the Sun."),
             ("What is the difference between translucent and opaque?", "A translucent material lets some light through, such as frosted glass. An opaque material lets no light through, such as wood or metal."),
             ("How can I make a shadow bigger?", "Move the object nearer to the light source, or move the light source nearer to the object.")],
            sets)


if __name__ == "__main__":
    main()
