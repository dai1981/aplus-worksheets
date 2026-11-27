# -*- coding: utf-8 -*-
"""
Australian Curriculum v9.0 Science, Year 5, AC9S5U03: light sources, light travelling in straight lines, and how we see.
  python tools/gen_au_science_y5_light_sources_and_how_light_travels.py
Reuses the UK Year 6 light makers (sources, transparent / translucent / opaque, how we see) with Australian names.
Own questions on straight-line evidence (light beams through dust, holes in cards, sunbeams through clouds).
Wrong answers come from real mistakes: thinking the Moon or a mirror is a light source, thinking light comes out of our eyes,
thinking light bends around corners on its own.
"""
from au_sci import AU, seed_of, make_au, tq, pool, limit

YEAR, SORT = 5, 5
U, R, P, src = AU(seed_of(YEAR, SORT))

T = "gen_uk_science_y6_how_light_travels"
S = "gen_uk_science_y6_how_we_see"
uk_src = limit(src(T, "g_src"), 9)
uk_srcyn = src(T, "g_srcyn")
uk_mat = src(T, "g_mat")
uk_def = limit(src(T, "g_def"), 3)
uk_speed = limit(src(T, "g_speed"), 3)
uk_b1 = src.B(T, "B1")
uk_b5 = src.B(T, "B5")
uk_dark = limit(src("gen_uk_science_y3_light_and_dark", "g_dark"), 2)
uk_why = src(S, "g_why")
uk_diag = limit(src(S, "g_diag"), 5)
uk_see1 = src.B(S, "B1")

LINE = [("Sunbeams shine through gaps in the clouds.", "The beams are straight lines."),
        ("A torch beam shines through smoke at a concert.", "The beam is a straight line."),
        ("Three cards with holes are lined up. You can see a candle through all three holes.", "Light only gets through when the holes are in a straight line."),
        ("One of the three cards is moved a little to the side.", "The light is blocked, because light cannot bend around the card."),
        ("Light shines through a gap in the curtains onto the floor.", "It makes a patch with straight edges."),
        ("A laser pointer is shone through misty air.", "You see a thin, straight line of light."),
        ("You cannot see around a corner without a mirror.", "Light travels in straight lines and does not bend around the corner."),
        ("An object blocks light from a torch and makes a shadow.", "Light travels in straight lines, so it cannot reach the space behind the object.")]


def g_line():
    s, a = R.choice(LINE)
    w = ["Light bends to go around objects.", "Light comes out of our eyes.", "Light spreads out in curves.", "Light only travels at night.",
         "Light moves in a zigzag."]
    return tq("%s What does this show about light?" % s, "Light travels in straight lines.", R.sample(w, 3), a)


POOL1 = pool(R, [
    ("Why is the Moon not a light source?", "It reflects light from the Sun.", ["It is too small.", "It is too far away.", "It only shines at night."], "The Moon makes no light of its own."),
    ("Which word describes a material that blocks all light?", "opaque", ["transparent", "translucent", "luminous"], "Wood, metal and cardboard are opaque."),
    ("Why do shadows have the same outline as the object?", "Light travels in straight lines past the edges of the object.", ["Light bends around the object.", "The object gives off dark light.", "Shadows are made of dust."], "The edges of the shadow line up with the edges of the object."),
    ("Which is the biggest natural light source for Earth?", "the Sun", ["the Moon", "lightning", "a firefly"], "The Sun is a star."),
    ("Which of these is an artificial (made by people) light source?", "a street light", ["the Sun", "lightning", "a glow-worm"], "People make street lights, torches and screens."),
    ("Which glows in caves in Australia and is a living light source?", "glow-worms", ["mirrors", "the Moon", "shiny rocks"], "Glow-worms make their own light."),
    ("How do we see a book in a lit room?", "Light from a lamp reflects off the book into our eyes.", ["Light comes out of our eyes onto the book.", "The book gives off its own light.", "We do not need light to see."], "Light travels from the source to the object to our eyes."),
    ("Why can't we see anything in a completely dark room?", "No light reflects into our eyes.", ["Our eyes stop working at night.", "Objects disappear in the dark.", "Darkness fills our eyes."], "We need light to see."),
    ("Which arrow shows how we see a tree on a sunny day?", "Sun → tree → eye", ["eye → tree → Sun", "eye → tree", "tree → Sun → eye"], "Light starts at the source."),
    ("Which material lets almost no light through?", "cardboard", ["clear glass", "clean water", "air"], "Cardboard is opaque."),
    ("Why do lighthouses have bright lamps on tall towers?", "Light travels in straight lines, so a high light can be seen far out at sea.", ["Light bends over hills.", "High light is warmer.", "Ships can hear the light."], "A tall tower stops hills and waves blocking the light."),
])
POOL5 = pool(R, [
    ("Mia lines up three cards with holes and looks at a torch. She can see the light. Then she moves the middle card. What will she see?", "no light", ["the same light", "brighter light", "two lights"], "The holes are no longer in a straight line."),
    ("Jack tests how much light passes through four materials using a light meter. Which result fits clear plastic?", "95% of the light passes through", ["0% passes through", "40% passes through", "the plastic makes its own light"], "Transparent materials let most light through."),
    ("Which is a fair way to compare how much light materials let through?", "same torch, same distance, same size piece of each material", ["a different torch for each material", "different distances for each material", "testing only one material"], "Change only the material."),
    ("A student says, 'I can see because light comes out of my eyes.' What evidence shows this is wrong?", "In a completely dark room you see nothing.", ["Eyes are round.", "Some people wear glasses.", "Eyes blink."], "If light came out of eyes, we could see in the dark."),
    ("Ruby's light meter shows 800 units with no cover, 600 with baking paper and 0 with cardboard. Which word fits baking paper?", "translucent", ["transparent", "opaque", "a light source"], "Some light passes through, but not all."),
    ("Why do cyclists wear bright clothes and use lights at night?", "so light from their lights and car headlights reaches drivers' eyes", ["so they can see in the dark without light", "to keep warm", "to make the road brighter for everyone"], "Drivers can only see what sends light into their eyes."),
])


def main():
    sets = U.sets([
        ("Light sources", [(uk_src, 6), (uk_srcyn, 6), (POOL1, 5), (uk_b1, 3)]),
        ("Light travels in straight lines", [(g_line, 7), (uk_dark, 2), (POOL1, 4), (uk_speed, 2), (uk_b1, 3), (uk_why, 2)]),
        ("How we see", [(uk_why, 7), (uk_diag, 3), (uk_see1, 6), (POOL1, 2), (uk_b5, 2)]),
        ("Transparent, translucent and opaque", [(uk_mat, 10), (uk_def, 3), (uk_srcyn, 4), (uk_src, 1), (POOL1, 2)]),
        ("Investigations", [(POOL5, 6), (uk_b5, 3), (uk_diag, 2), (uk_mat, 5), (uk_speed, 1), (g_line, 1), (uk_src, 2)]),
    ])
    make_au(YEAR, "light-sources-and-how-light-travels", SORT, "AC9S5U03", "Physical sciences",
            "Describe how light travels from a source and how it interacts with objects and materials to form shadows and images "
            "(summary of the Australian Curriculum v9.0 Science content description).",
            "Light Sources and How Light Travels", "Light sources",
            "Free Year 5 science worksheets on light sources, how light travels in straight lines, how we see, and transparent, translucent "
            "and opaque materials. 100 questions with answers.",
            "Light travels in straight lines.", "We see when light from a source reaches our eyes, directly or after reflecting.",
            "<p><b>Light travels in straight lines from a source.</b></p><ul>"
            "<li>A light source gives off its own light: the Sun, a torch, a fire, a glow-worm. The Moon and mirrors only reflect light.</li>"
            "<li>We see an object when light from a source bounces off it and travels into our eyes.</li>"
            "<li>Transparent materials let most light through, translucent materials let some through, and opaque materials block it.</li></ul>",
            [("Is the Moon a light source?", ["it does not make light", "it reflects sunlight"], "no"),
             ("Cards with holes in a line, then one is moved. Why does the light disappear?", ["light travels in straight lines", "it cannot bend around the card"], "the light is blocked")],
            ["Thinking the Moon, a mirror or a reflector is a light source.", "Drawing arrows from the eye to the object (light goes into the eye).",
             "Mixing up translucent (some light gets through) and transparent (almost all gets through)."],
            [("How do we know light travels in straight lines?", "Beams of sunlight and torch beams in smoke are straight, shadows form behind objects, and you can only see a light through holes in cards when the holes are lined up."),
             ("Is the Moon a light source?", "No. The Moon reflects light from the Sun. Light sources, such as the Sun, a torch or a glow-worm, give off their own light."),
             ("What is the difference between transparent, translucent and opaque?", "Transparent materials such as clear glass let almost all light through. Translucent materials such as baking paper let some light through. Opaque materials such as wood block light.")],
            sets)


if __name__ == "__main__":
    main()
