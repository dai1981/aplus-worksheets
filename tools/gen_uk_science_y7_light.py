# -*- coding: utf-8 -*-
"""
UK Year 7 science (KS3 Physics): Light
  python tools/gen_uk_science_y7_light.py
Light waves travelling through a vacuum at 300,000 km/s; transmission, absorption and reflection; the law of reflection
and the normal; refraction at the boundary of glass and air; white light dispersed into a spectrum by a prism;
coloured filters and the colour of objects under coloured light; the eye and the pinhole camera; light vs sound.
Reuses the speed and material questions of the Year 6 unit (new seed).
Wrong answers come from real mistakes: "the angle of reflection is measured from the mirror", "a red filter turns
light red by adding red", "a blue object looks blue in red light", "light needs a medium".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_ks3, table, People, once
import gen_uk_science_y6_how_light_travels as L6
from sci_phys import uniq

L6.U = Unit(61712)
L6.R = L6.U.R
L6.P = People(L6.R)
uk_sci.USED.clear()
U, R, P = L6.U, L6.R, L6.P


def g_refl():
    i = R.choice(range(10, 81, 5))
    k = R.choice(["refl", "mirror", "total"])
    if not once(("re", i, k)):
        return None
    if k == "refl":
        g = "%d°" % i
        return item("A ray of light hits a plane mirror with an angle of incidence of %d°. What is the angle of reflection?" % i, g, uniq(g, ["%d°" % (90 - i), "%d°" % (180 - i), "%d°" % (2 * i), "90°"]),
                    "Law of reflection: angle of incidence = angle of reflection (both measured from the normal).")
    if k == "mirror":
        g = "%d°" % (90 - i)
        return item("A ray of light makes an angle of %d° with the surface of a mirror. What is the angle of incidence (measured from the normal)?" % i, g,
                    uniq(g, ["%d°" % i, "%d°" % (180 - i), "90°", "%d°" % (2 * i)]), "The normal is at 90° to the mirror, so 90° − %d° = %d°." % (i, 90 - i))
    g = "%d°" % (2 * i)
    return item("The angle of incidence is %d°. What is the angle between the incident ray and the reflected ray?" % i, g, uniq(g, ["%d°" % i, "%d°" % (90 - i), "%d°" % (180 - i), "90°"]),
                "Each ray makes %d° with the normal, so together %d°." % (i, 2 * i))


COLS = ["red", "green", "blue"]


def g_obj():
    obj = R.choice(["red", "green", "blue", "white", "black"])
    light = R.choice(["red", "green", "blue", "white"])
    if not once(("ob", obj, light)):
        return None
    if obj == "black":
        a = "black"
    elif obj == "white":
        a = light
    elif light == "white":
        a = obj
    else:
        a = obj if obj == light else "black"
    thing = R.choice(["T-shirt", "ball", "car", "book", "hat"])
    w = [x for x in ["red", "green", "blue", "white", "black"] if x != a]
    return item("A %s %s is lit only by %s light. What colour does it look?" % (obj, thing, light), a, R.sample(w, 3),
                "Objects reflect their own colour and absorb the others. If their colour is not in the light, they look black.")


def g_filter():
    k = R.random() < 0.5
    if k:
        f = R.choice(COLS)
        if not once(("fi", f)):
            return None
        return item("White light shines through a %s filter. What colour light comes out?" % f, f, [x for x in ["red", "green", "blue", "white", "black (no light)"] if x != f][:3],
                    "A filter lets its own colour through and absorbs the rest.")
    f1, f2 = R.sample(COLS, 2)
    if not once(("ff", f1, f2)):
        return None
    return item("White light passes through a %s filter and then a %s filter. What comes out?" % (f1, f2), "no light (it looks black)", [f1 + " light", f2 + " light", "white light"],
                "The first filter lets only %s through; the second absorbs %s." % (f1, f1))


SPEC = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]


def g_spec():
    i = R.randrange(len(SPEC) - 1)
    k = R.random() < 0.5
    if not once(("sp", i, k)):
        return None
    if k:
        a = SPEC[i + 1]
        return item("In the spectrum made by a prism, which colour comes after %s?" % SPEC[i], a, R.sample([x for x in SPEC if x not in (a, SPEC[i])], 3), "Red, orange, yellow, green, blue, indigo, violet.")
    a = SPEC[i]
    return item("In the spectrum made by a prism, which colour comes just before %s?" % SPEC[i + 1], a, R.sample([x for x in SPEC if x not in (a, SPEC[i + 1])], 3), "Red, orange, yellow, green, blue, indigo, violet.")


REFR = [("A ray of light goes from air into a glass block at an angle.", "It bends towards the normal."), ("A ray of light comes out of a glass block into air at an angle.", "It bends away from the normal."),
        ("A ray of light enters a glass block along the normal (at 90° to the surface).", "It goes straight on without bending."),
        ("A straw in a glass of water looks bent.", "Light from the straw refracts as it leaves the water."),
        ("A swimming pool looks shallower than it really is.", "Light refracts as it leaves the water."),
        ("A prism splits white light into colours.", "Different colours refract by different amounts.")]


def g_refr():
    s, a = R.choice(REFR)
    if not once(("rf", s)):
        return None
    return item("%s What happens or why?" % s, a, R.sample([x[1] for x in REFR if x[1] != a], 3), "Refraction is the bending of light when it changes speed going into a different material.")


B1 = bank([
    ("How fast does light travel in a vacuum?", "about 300,000 km per second", ["about 340 m per second", "about 300 km per hour", "it does not travel in a vacuum"], "Nothing travels faster."),
    ("What is the normal in a ray diagram?", "a line at 90° to the surface where the ray hits", ["the surface of the mirror", "the reflected ray", "the light source"], "Angles are measured from it."),
    ("What is the law of reflection?", "angle of incidence = angle of reflection", ["angle of incidence = 90°", "the reflected ray always goes back the same way", "light bends towards the mirror"], "For plane mirrors."),
    ("What is refraction?", "the bending of light as it passes from one material into another", ["light bouncing off a mirror", "light being absorbed", "light making a shadow"], "It changes speed."),
    ("What is white light made of?", "all the colours of the spectrum mixed together", ["only white", "only red and blue", "no colours"], "A prism separates them."),
    ("Why does a red apple look red in white light?", "It reflects red light and absorbs the other colours.", ["It makes red light.", "It absorbs red light.", "It is a light source."], "Coloured objects reflect their colour."),
    ("How is light different from sound?", "Light can travel through a vacuum; sound cannot.", ["Sound is faster.", "Light needs air.", "They are the same."], "Different waves."),
    ("What does the lens in the eye do?", "focuses light onto the retina", ["makes light", "stores pictures", "turns light into sound"], "Like a camera lens."),
])
B5 = bank([
    ("Why does a pinhole camera make an upside-down image?", "Light travels in straight lines, so rays cross over at the pinhole.", ["The pinhole is upside down.", "Light bends in a circle.", "The screen is curved."], "Straight lines."),
    ("Why do we see lightning before we hear thunder?", "Light travels far faster than sound.", ["Thunder happens later.", "Sound is faster than light.", "Our ears are slower."], "Speeds."),
    ("Why is a periscope made with two mirrors at 45°?", "Each mirror reflects the light through 90°, so it comes out parallel to where it went in.", ["Mirrors bend light like lenses.", "It makes the light faster.", "45° stops reflection."], "Law of reflection."),
    ("Why does the bottom of a swimming pool look closer than it is?", "Light from the bottom refracts as it leaves the water.", ["The water is magnified.", "Light reflects off the bottom twice.", "The pool really is shallow."], "Refraction."),
    ("Why are emergency vehicles often yellow with reflective strips?", "They reflect lots of light so they are easy to see.", ["Yellow absorbs all light.", "Reflective strips make light.", "It is cheaper."], "Reflection for safety."),
])


def body():
    think = ("<p><b>Light travels in straight lines at 300,000 km/s, even through a vacuum.</b></p>"
             "<ul><li>Reflection: angle of incidence = angle of reflection, measured from the normal.</li>"
             "<li>Refraction: light bends when it goes into a different material (towards the normal into glass).</li>"
             "<li>White light is a mix of colours. Filters let their own colour through; objects reflect their own colour.</li></ul>")
    ex = [("Angle of incidence 35°. Angle of reflection?", ["They are equal"], "35°"),
          ("A blue ball in red light?", ["No blue light to reflect"], "black")]
    mist = ["Measuring angles from the mirror instead of the normal.", "Thinking a red filter adds red to light.", "Thinking a blue object looks blue in red light."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("How light travels", B1 + [(L6.g_mat, 6), (L6.g_speed, 6)]),
        ("Reflection", [(g_refl, 20)]),
        ("Refraction and the spectrum", [(g_refr, 6), (g_spec, 10), (g_filter, 4)]),
        ("Colour", [(g_obj, 14), (g_filter, 6)]),
        ("Thinking about light", B5 + [(g_obj, 8), (g_refl, 7)]),
    ])
    make_ks3(7, "light", 12, "Physics", "Waves",
             "The similarities and differences between light waves and waves in matter; light waves travelling through a vacuum; speed of light; the transmission of light through materials: absorption, diffuse scattering and specular reflection at a surface; use of ray model to explain imaging in mirrors, the pinhole camera, the refraction of light and action of convex lens in focusing (qualitative); the human eye; colours and the different frequencies of light, white light and prisms (qualitative only); differential colour effects in absorption and diffuse reflection.",
             "Light",
             "Year 7 Science: Light Worksheets (Reflection, Refraction, Colour)",
             "Light",
             "Free Year 7 science worksheets on light: the speed of light, reflection and the law of reflection, refraction, the spectrum, coloured filters and coloured objects. 100 questions with answers.",
             "Light travels in straight lines.",
             "Angle of incidence = angle of reflection. Objects reflect their own colour.",
             body(),
             [("What is the law of reflection?", "The angle of incidence equals the angle of reflection. Both angles are measured from the normal, a line at 90° to the mirror."),
              ("What is refraction?", "Light bending as it passes from one material into another, because its speed changes. Going from air into glass, it bends towards the normal."),
              ("Why do objects look different colours in coloured light?", "An object reflects only its own colour of light. If that colour is not in the light shining on it, it absorbs everything and looks black.")],
             sets)


if __name__ == "__main__":
    main()
