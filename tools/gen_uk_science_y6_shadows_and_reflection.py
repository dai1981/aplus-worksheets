# -*- coding: utf-8 -*-
"""
UK Year 6 science: Shadows and Reflection (Light)
  python tools/gen_uk_science_y6_shadows_and_reflection.py
Why shadows have the same shape as the object, how shadow size changes with the distance from the light, shadows
from the Sun during the day, mirrors (angle in = angle out), mirror writing and periscopes.
Wrong answers come from real mistakes: "a shadow is a reflection", "moving the object away from the torch makes the
shadow bigger", "shadows are longest at midday", "mirrors make light bend round corners on their own".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once, fig
from uk_sci_pics import shadow_setup
from sci_phys import uniq

U = Unit(61612)
R = U.R
P = People(R)


def g_shd():
    who = P.next()[0]
    d = [10, 20, 30, 40, 50]
    start = R.choice([40, 44, 48, 50, 54, 60])
    drop = [R.choice([10, 12, 14]), R.choice([6, 7, 8]), R.choice([4, 5]), R.choice([2, 3])]
    h = [start]
    for x in drop:
        h.append(h[-1] - x)
    k = R.choice(["read", "read", "pattern", "measured", "changed", "same", "predict", "diff"])
    ri = R.randrange(5)
    if not once(("sh", k, ri if k == "read" else 0, tuple(h))) or (k in ("pattern", "measured", "changed", "same") and not once(("sk", k), 3)):
        return None
    tab = table(["Distance from torch to object (cm)", "Height of shadow on screen (cm)"], [[str(a), str(b)] for a, b in zip(d, h)])
    intro = fig(shadow_setup("distance", "torch, object and screen; the distance from torch to object changes")) + tab + "%s moved a toy closer to the screen and further from the torch. " % who
    if k == "read":
        g = "%d cm" % h[ri]
        return item(intro + "How tall was the shadow when the toy was %d cm from the torch?" % d[ri], g, uniq(g, ["%d cm" % x for x in h] + ["%d cm" % d[ri]]), "Read across from %d cm." % d[ri])
    if k == "pattern":
        return item(intro + "What pattern do the results show?", "The further the toy is from the torch, the smaller its shadow.",
                    ["The further the toy is from the torch, the bigger its shadow.", "The shadow stays the same size.", "The shadow changes shape."], "Closer to the light blocks more light: a bigger shadow.")
    if k == "measured":
        return item(intro + "What did %s measure?" % who, "the height of the shadow", ["the distance from the torch", "the brightness of the torch", "the colour of the toy"], "The measured variable is the result.")
    if k == "changed":
        return item(intro + "Which variable did %s change?" % who, "the distance from the torch to the toy", ["the height of the shadow", "the toy", "the torch"], "Only one variable is changed.")
    if k == "same":
        return item(intro + "Which should %s keep the same for a fair test?" % who, "the toy, the torch and where the screen is", ["the distance from the torch", "the shadow height", "nothing"], "Control variables stay the same.")
    if k == "predict":
        lo, hi = h[3], h[2]
        g = "between %d cm and %d cm" % (lo, hi)
        return item(intro + "Predict the shadow height when the toy is 35 cm from the torch.", g,
                    ["more than %d cm" % h[0], "less than %d cm" % h[4], "exactly %d cm" % h[4]], "35 cm is between 30 cm and 40 cm, so the height is between those two results.")
    dd = h[0] - h[4]
    g = "%d cm" % dd
    return item(intro + "How much smaller was the shadow at 50 cm than at 10 cm?", g, uniq(g, ["%d cm" % h[0], "%d cm" % h[4], "40 cm", "%d cm" % (dd + 4)]), "%d − %d = %d cm." % (h[0], h[4], dd))


SHAPE = [("a ball", "a circle"), ("a tin can standing upright, seen from the side", "a rectangle"), ("an ice cream cone held point down", "a triangle"),
         ("a coin facing the torch", "a circle"), ("a cube facing the torch", "a square"), ("a pair of scissors held open", "an X-like shape"),
         ("a hand with fingers spread", "a hand shape with spread fingers"), ("a book standing upright facing the torch", "a rectangle")]


def g_shape():
    o, s = R.choice(SHAPE)
    if not once(("sp", o)):
        return None
    w = [x for x in ["a circle", "a rectangle", "a triangle", "a square", "an X-like shape", "a hand shape with spread fingers"] if x != s]
    return item("A torch shines on %s. What shape is its shadow?" % o, s, R.sample(w, 3), "Light travels in straight lines, so the shadow has the same outline as the object.")


SUN = [("in the early morning", "long", "west"), ("at midday", "short", "north"), ("in the late afternoon", "long", "east")]


def g_sun():
    t, l, dr = R.choice(SUN)
    k = R.random() < 0.5
    if not once(("su", t, k)):
        return None
    if k:
        return item("In the UK, how long is a tree's shadow %s?" % t, l if l == "short" else "long", ["short" if l == "long" else "long", "there is no shadow", "the same length all day"],
                    "When the Sun is low, shadows are long; at midday it is highest, so shadows are shortest.")
    return item("In the UK, which way does a tree's shadow point %s?" % t, "towards the %s" % dr, ["towards the %s" % x for x in ("north", "south", "east", "west") if x != dr][:3],
                "Shadows point away from the Sun. The Sun rises in the east, is in the south at midday, and sets in the west.")


def g_mirror():
    a = R.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    if not once(("mi", a)):
        return None
    g = "%d°" % a
    return item("A ray of light hits a flat mirror at %d° to the normal (the line at right angles to the mirror). At what angle does it reflect?" % a, g,
                uniq(g, ["%d°" % (90 - a), "%d°" % (180 - a), "%d°" % (2 * a), "0°"]), "The angle of reflection equals the angle of incidence.")


WORD = ["AMBULANCE", "POLICE", "FIRE", "STOP", "EXIT"]


def g_peri():
    q, a, w, e = R.choice([
        ("How many mirrors does a simple periscope use?", "two", ["one", "three", "none"], "One at the top and one at the bottom."),
        ("At what angle are the mirrors in a periscope set?", "45°", ["90°", "10°", "180°"], "Each mirror turns the light through a right angle."),
        ("What does a periscope let you do?", "see over walls or crowds", ["see in total darkness", "make things bigger", "see through solid walls"], "Light is reflected twice."),
        ("Why is AMBULANCE written backwards on the front of ambulances?", "so drivers can read it the right way in their mirrors", ["so it looks interesting", "because it is a code", "so only nurses can read it"], "Mirrors reverse left and right."),
        ("You hold a book up to a mirror. What happens to the writing?", "It appears back to front (reversed left to right).", ["It appears upside down.", "It disappears.", "It looks the same."], "Mirror images are reversed."),
        ("Which surface reflects light best to give a clear image?", "a smooth, shiny mirror", ["a rough brick wall", "black velvet", "crumpled paper"], "Smooth surfaces reflect light evenly."),
        ("Why are mirrors placed at sharp bends on narrow roads?", "to let drivers see traffic coming round the bend", ["to make the road brighter at night", "to slow cars down", "to reflect sound"], "Reflection helps us see round corners."),
    ])
    if not once(("pe", q)):
        return None
    return item(q, a, w, e)


B1 = bank([
    ("What is a shadow?", "a dark area where light is blocked by an object", ["a reflection of the object", "a light source", "a kind of mirror"], "Opaque objects block light."),
    ("Why does a shadow have the same shape as the object?", "Light travels in straight lines, so the object blocks light in its own outline.", ["Shadows copy objects on purpose.", "Light bends round the object.", "Shadows are reflections."], "Straight lines of light."),
    ("Which kind of material makes the darkest shadow?", "opaque", ["transparent", "translucent", "reflective glass"], "No light gets through."),
    ("How do you make a shadow bigger with a torch?", "move the object closer to the torch", ["move the object further from the torch", "use a smaller object", "switch the torch off"], "Closer to the light: bigger shadow."),
    ("Why can't you see colour or detail in a shadow?", "A shadow is just an area with less light; it has no detail of its own.", ["Shadows are always black paint.", "Shadows are made of smoke.", "Shadows are reflections."], "It is the absence of light."),
    ("When is your shadow shortest on a sunny day in the UK?", "around midday", ["early in the morning", "late in the evening", "at night"], "The Sun is highest at midday."),
    ("What does a mirror do to light?", "reflects it", ["absorbs all of it", "makes new light", "lets it pass through"], "Light bounces off the smooth surface."),
    ("Which statement about reflection is true?", "The angle of reflection is equal to the angle of incidence.", ["Light always reflects straight back.", "Mirrors make light bend into curves.", "Only light sources can reflect."], "Angle in = angle out."),
])
B5 = bank([
    ("How could a shadow puppet show make one puppet look like a giant?", "move that puppet closer to the light", ["move it next to the screen", "use a weaker light", "turn the puppet around"], "Use the pattern."),
    ("Why do sundials work?", "The Sun's shadow moves in a regular way during the day.", ["Shadows are random.", "The Sun stays still.", "Shadows show the date only."], "The Earth turns."),
    ("Why are there two shadows when two lamps shine on one object?", "Each lamp's light is blocked separately, making one shadow each.", ["Shadows split in half.", "One lamp makes two shadows.", "Shadows reflect each other."], "One shadow per light source."),
    ("A pupil says shadows are reflections. How could you show they are not?", "A shadow has no colour or detail, but a reflection shows the object's colours.", ["Reflections and shadows are identical.", "Shadows are brighter.", "Shadows show your face."], "Compare them."),
    ("Why do drivers have mirrors on cars?", "to see behind them by reflecting light into their eyes", ["to make light", "to see in total darkness", "to keep the car cool"], "Reflection in use."),
])


def body():
    think = ("<p><b>Light travels in straight lines, so opaque objects make shadows with the same outline.</b></p>"
             "<ul><li>Move an object closer to the light and its shadow gets bigger; move it away and the shadow gets smaller.</li>"
             "<li>Outdoors, shadows are long in the morning and evening and shortest at midday. They point away from the Sun.</li>"
             "<li>Mirrors reflect light: the angle of reflection equals the angle of incidence. A periscope uses two mirrors at 45°.</li></ul>")
    ex = [("Shadow 50 cm at 10 cm, 20 cm at 40 cm. At 25 cm?", ["Between the 20 cm and 30 cm results"], "between those heights"),
          ("Ray hits a mirror at 35°. Reflected angle?", ["Angle in = angle out"], "35°")]
    mist = ["Thinking a shadow is a reflection.", "Thinking moving the object away from the light makes the shadow bigger.", "Thinking shadows are longest at midday."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Making shadows", B1 + [(g_shape, 8), (g_sun, 4)]),
        ("Shadows and mirrors", [(g_sun, 2), (g_mirror, 6), (g_peri, 4), (g_shd, 8)]),
        ("Shadow size", [(g_shd, 20)]),
        ("Mirrors and periscopes", [(g_mirror, 6), (g_peri, 3), (g_shd, 11)]),
        ("Investigating light", B5 + [(g_shd, 15)]),
    ])
    make_uk(6, "shadows-and-reflection", 12, "Light",
            "Use the idea that light travels in straight lines to explain why shadows have the same shape as the objects that cast them.",
            "Shadows and Reflection",
            "Year 6 Science: Shadows and Reflection Worksheets (Shadow Size, Mirrors, Periscopes)",
            "Shadows and Reflection",
            "Free Year 6 science worksheets on shadows and reflection: why shadows have the same shape as objects, shadow size investigations, shadows from the Sun, mirrors and periscopes. 100 questions with answers.",
            "Straight-line light makes same-shape shadows.",
            "Closer to the light, bigger shadow; mirrors reflect at equal angles.",
            body(),
            [("Why do shadows have the same shape as the object?", "Light travels in straight lines. An opaque object blocks the light, so the dark area behind it has the same outline as the object."),
             ("How can you change the size of a shadow?", "Move the object closer to the light to make the shadow bigger, or further from the light (closer to the screen) to make it smaller."),
             ("How does a periscope work?", "It has two mirrors at 45°. Light reflects off the top mirror down the tube, then off the bottom mirror into your eye.")],
            sets)


if __name__ == "__main__":
    main()
