# -*- coding: utf-8 -*-
"""
UK Year 6 science: How Light Travels (Light)
  python tools/gen_uk_science_y6_how_light_travels.py
Light sources and reflectors, light travels in straight lines, transparent, translucent and opaque materials,
the speed of light, and seeing lightning before hearing thunder (about 3 seconds per kilometre).
Wrong answers come from real mistakes: "the Moon is a light source", "light can bend round corners in air",
"translucent means you can see clearly through it", "thunder and lightning happen at different times".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61610)
R = U.R
P = People(R)

SRC = ["the Sun", "a candle flame", "a torch that is switched on", "a lit bulb", "a firefly", "a flash of lightning", "a glowing computer screen", "a campfire", "a star"]
NOT = ["the Moon", "a mirror", "a bicycle reflector", "a cat's eye reflector on a road", "a sheet of white paper", "a shiny spoon", "the planet Venus", "a high-visibility jacket"]


def g_src():
    k = R.random() < 0.5
    if k:
        a = R.choice(SRC)
        w = R.sample(NOT, 3)
        if not once(("s", a), 3):
            return None
        o = sorted([a] + w)
        return item("Which of these is a light source: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "A light source gives out its own light. The others only reflect light.")
    a = R.choice(NOT)
    w = R.sample(SRC, 3)
    if not once(("n", a), 3):
        return None
    o = sorted([a] + w)
    return item("Which of these is NOT a light source: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "%s does not make its own light; it reflects light." % (a[0].upper() + a[1:]))


def g_srcyn():
    a = R.choice(SRC + NOT)
    if not once(("yn", a)):
        return None
    src = a in SRC
    ans = "a light source" if src else "not a light source: it reflects light"
    return item("Is %s a light source?" % a, ans, ["not a light source: it reflects light" if src else "a light source", "a light source only at night", "a sound source"],
                "Sources give out light; everything else is seen because it reflects light.")


MAT = {"transparent": ["clear glass", "cling film", "clean water", "a clear plastic bottle", "air", "a glass window", "a clear swimming pool"],
       "translucent": ["tracing paper", "frosted glass", "tissue paper", "greaseproof paper", "a thin cotton sheet", "a lampshade", "a plastic milk bottle"],
       "opaque": ["wood", "cardboard", "a brick", "aluminium foil", "a metal tray", "a book", "a stone wall", "a coin"]}
DEF = {"transparent": "lets almost all light through, so you can see clearly through it",
       "translucent": "lets some light through, but you cannot see clearly through it",
       "opaque": "lets no light through and makes a dark shadow"}


def g_mat():
    t = R.choice(sorted(MAT))
    m = R.choice(MAT[t])
    if not once(("ma", m)):
        return None
    return item("Is %s transparent, translucent or opaque?" % m, t, [x for x in sorted(MAT) if x != t] + ["a light source"], "%s %s." % (m[0].upper() + m[1:], DEF[t]))


def g_def():
    t = R.choice(sorted(MAT))
    k = R.random() < 0.5
    if k:
        if not once(("dt", t)):
            return None
        return item("A material %s. Which word describes it?" % DEF[t], t, [x for x in sorted(MAT) if x != t] + ["reflective"], "Transparent, translucent, opaque.")
    a = R.choice(MAT["opaque"])
    if not once(("dk", a)):
        return None
    tl = R.sample(MAT["translucent"], 2)
    return item("Which material would make the darkest shadow?", a, [R.choice(MAT["transparent"])] + tl,
                "Opaque materials block all the light.")


def g_speed():
    k = R.choice(["dist", "sun"])
    if k == "dist":
        n = R.choice([2, 3, 4, 5, 6, 10])
        if not once(("sd", n)):
            return None
        a = "%s km" % format(300000 * n, ",")
        return item("Light travels about 300,000 km every second. How far does it travel in %d seconds?" % n, a,
                    uniq(a, ["%s km" % format(300000 // n, ","), "%s km" % format(300000 + n, ","), "%s km" % format(30000 * n, ","), "%s km" % format(3000000 * n, ",")]),
                    "300,000 × %d = %s km." % (n, format(300000 * n, ",")))
    m = R.choice([2, 3, 4, 5])
    if not once(("ss", m)):
        return None
    a = "%d minutes" % (8 * m)
    return item("Light from the Sun takes about 8 minutes to reach Earth. If a planet were %d times as far from the Sun as Earth, about how long would sunlight take to reach it?" % m, a,
                uniq(a, ["%d minutes" % (8 + m), "8 seconds", "%d minutes" % (8 * m * 2), "%d hours" % (8 * m)]), "Twice as far takes twice as long, and so on.")


def g_storm():
    who = P.next()[0]
    s = R.choice([3, 6, 9, 12, 15, 18, 21, 24])
    km = s // 3
    if not once(("st", s)):
        return None
    a = "about %d km" % km
    return item("%s sees lightning and counts %d seconds before hearing the thunder. Sound travels about 1 km every 3 seconds. How far away is the storm?" % (who, s), a,
                uniq(a, ["about %d km" % (s * 3), "about %d km" % s, "about %d km" % (km + 3), "0 km, it is overhead"]), "%d ÷ 3 = %d km. We see the flash first because light is much faster than sound." % (s, km))


B1 = bank([
    ("How does light travel?", "in straight lines", ["in curves around corners", "in circles", "only downwards"], "Rays of light are straight."),
    ("What is a light source?", "something that gives out its own light", ["anything shiny", "anything white", "anything that is warm"], "The Moon only reflects sunlight."),
    ("Why does the Moon look bright at night?", "It reflects light from the Sun.", ["It makes its own light.", "It is on fire.", "It is a star."], "The Moon is not a light source."),
    ("Three cards with holes are lined up so you can see a torch through them. One card is moved. What happens?", "You can no longer see the torch.", ["The light bends to reach you.", "The torch gets brighter.", "Nothing changes."], "Light travels in straight lines."),
    ("Why should you never look directly at the Sun?", "Its light is so strong it can damage your eyes.", ["It is too far away to see.", "It is not a light source.", "It makes you sneeze."], "Safety."),
    ("Which travels faster: light or sound?", "light", ["sound", "they travel at the same speed", "neither moves"], "Light is about a million times faster."),
    ("What is darkness?", "the absence of light", ["a kind of light", "a gas", "a colour of light"], "No light reaching our eyes."),
    ("Why do we see lightning before we hear thunder?", "Light travels much faster than sound.", ["Lightning happens first.", "Thunder is quieter.", "Sound travels faster."], "They happen at the same time."),
])
B5 = bank([
    ("How could you show that light travels in straight lines using a hose pipe and a torch?", "Shine the torch through a straight pipe and then a bent pipe and compare.", ["Fill the pipe with water.", "Use a pipe in the dark only.", "Shake the torch."], "Straight pipe: light gets through."),
    ("Why do car headlights make beams with sharp edges in fog?", "Light travels in straight lines, so the beam edges are straight.", ["Fog bends light into circles.", "Headlights make sound.", "Fog is a light source."], "Rays are straight."),
    ("Why are curtains made of thick, opaque fabric in bedrooms?", "to block light so it is dark for sleeping", ["to let in more light", "to make the room translucent", "to reflect sound"], "Opaque blocks light."),
    ("A window is made of frosted glass. Why?", "It lets light in but people outside cannot see clearly in.", ["It blocks all light.", "It is a light source.", "It is cheaper than wood."], "Translucent."),
    ("Which would be best for testing which materials let light through?", "Shine the same torch at the same distance through each material onto a light sensor.", ["Use different torches for each.", "Hold materials at different distances.", "Test in sunlight that keeps changing."], "Fair test."),
])


def body():
    think = ("<p><b>Light travels from a source in straight lines.</b></p>"
             "<ul><li>Light sources give out their own light (the Sun, a flame, a lit bulb). The Moon and mirrors only reflect light.</li>"
             "<li>Transparent materials let light through; translucent let some through; opaque let none through.</li>"
             "<li>Light is very fast: about 300,000 km per second. That is why we see lightning before we hear thunder (about 3 seconds per km).</li></ul>")
    ex = [("Is the Moon a light source?", ["It does not make its own light"], "No, it reflects sunlight."),
          ("Thunder 12 seconds after lightning. Distance?", ["12 ÷ 3"], "about 4 km")]
    mist = ["Thinking the Moon or a mirror is a light source.", "Thinking light can bend around corners on its own.", "Mixing up translucent (some light) and transparent (clear)."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Light sources", B1 + [(g_src, 8), (g_srcyn, 4)]),
        ("Sources and reflectors", [(g_srcyn, 12), (g_src, 8)]),
        ("Letting light through", [(g_mat, 16), (g_def, 4)]),
        ("The speed of light", [(g_speed, 10), (g_storm, 8), (g_def, 2)]),
        ("Investigating light", B5 + [(g_src, 6), (g_mat, 6), (g_def, 3)]),
    ])
    make_uk(6, "how-light-travels", 10, "Light",
            "Recognise that light appears to travel in straight lines.",
            "How Light Travels",
            "Year 6 Science: How Light Travels Worksheets (Light Sources, Straight Lines, Opaque)",
            "How Light Travels",
            "Free Year 6 science worksheets on how light travels: light sources and reflectors, straight lines, transparent, translucent and opaque materials, and the speed of light. 100 questions with answers.",
            "Light travels in straight lines.",
            "It comes from a source and goes straight until something reflects or blocks it.",
            body(),
            [("How does light travel?", "Light travels in straight lines from its source until it hits something that reflects it, lets it through or blocks it."),
             ("Is the Moon a light source?", "No. The Moon does not make its own light. We see it because it reflects light from the Sun."),
             ("What is the difference between transparent, translucent and opaque?", "Transparent materials let light through clearly, translucent materials let some light through but blur the view, and opaque materials let no light through.")],
            sets)


if __name__ == "__main__":
    main()
