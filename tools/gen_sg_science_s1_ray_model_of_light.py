# -*- coding: utf-8 -*-
"""
Singapore Secondary 1 science (Lower Secondary Science, Models): Ray Model of Light
  python tools/gen_sg_science_s1_ray_model_of_light.py
The ray model, reflection by smooth (regular) and rough (diffuse) surfaces, plane and curved mirrors and their uses,
images in a plane mirror, the law of reflection (angles measured from the normal), refraction caused by the change in the
speed of light, dispersion of white light by a prism, infrared and ultraviolet radiation, and light pollution.
UK KS3 light makers are reused for angles and the spectrum.
Wrong answers come from real mistakes: "angles are measured from the mirror", "light speeds up when it enters glass",
"the image in a plane mirror is upside down", "a rough surface does not reflect light".
"""
from sg_sci import item, bank, lesson
from sg_lss import Unit, luse, make_lss, seo, once, upto, People

U = Unit(64105)
R = U.R
P = People(R)
LI = luse(U, "gen_uk_science_y7_light", drop=[r"\bsound\b", r"thunder", r"filter", r"lit only"])


def g_ang():
    m = R.choice([10, 15, 20, 25, 30, 35, 40, 50, 55, 60, 65, 70, 75, 80])
    k = R.choice(["mirror", "normal"])
    if not once(("an", m, k)):
        return None
    if k == "mirror":
        a = 90 - m
        return item("A ray of light hits a plane mirror. The angle between the ray and the mirror surface is %d°. What is the angle of reflection?" % m, "%d°" % a,
                    ["%d°" % m, "%d°" % (2 * m), "%d°" % (180 - m)], "Angles are measured from the normal: 90° − %d° = %d°, and i = r." % (m, a))
    return item("The angle of reflection at a plane mirror is %d°. What is the angle between the reflected ray and the mirror surface?" % m, "%d°" % (90 - m),
                ["%d°" % m, "%d°" % (2 * m), "%d°" % (180 - m)], "The normal is at 90° to the mirror, so the angle is 90° − %d° = %d°." % (m, 90 - m))


IMG = [("upright (the same way up as the object)", "upside down"), ("the same size as the object", "larger than the object"),
       ("laterally inverted (left and right are swapped)", "not changed from left to right"), ("as far behind the mirror as the object is in front", "on the surface of the mirror"),
       ("virtual (it cannot be caught on a screen)", "real (it can be caught on a screen)")]


def g_img():
    a, w = R.choice(IMG)
    if not once(("im", a)):
        return None
    others = [x[1] for x in IMG if x[0] != a]
    return item("Which describes the image formed by a plane mirror?", "It is " + a + ".", ["It is " + w + "."] + ["It is " + x + "." for x in R.sample(others, 2)],
                "A plane mirror image is upright, the same size, laterally inverted, virtual and as far behind the mirror as the object is in front.")


def g_dist():
    d = R.choice([0.5, 1, 1.5, 2, 2.5, 3])
    nm, he, his = P.next()
    k = R.choice(["img", "gap", "walk"])
    if not once(("dt", d, k)):
        return None
    ds = ("%g" % d)
    if k == "img":
        return item("%s stands %s m in front of a plane mirror. How far behind the mirror is %s image?" % (nm, ds, his), "%s m" % ds,
                    ["%g m" % (2 * d), "%g m" % (d / 2), "0 m"], "The image is as far behind the mirror as the object is in front.")
    if k == "gap":
        return item("%s stands %s m in front of a plane mirror. How far is %s from %s image?" % (nm, ds, he, his), "%g m" % (2 * d),
                    ["%s m" % ds, "%g m" % (d / 2), "%g m" % (d + 1)], "%s m + %s m = %g m." % (ds, ds, 2 * d))
    s = R.choice([0.5, 1])
    return item("%s stands %s m in front of a plane mirror and walks %g m towards it. How far is %s from %s image now?" % (nm, ds, s, he, his) if d > s else None,
                "%g m" % (2 * (d - s)), ["%g m" % (d - s), "%g m" % (2 * d), "%g m" % (2 * d - s)], "New distance to the mirror = %g m, so image distance = 2 × %g = %g m." % (d - s, d - s, 2 * (d - s))) if d > s else None


USES = [("a car's side mirror", "a convex mirror", "It gives a wide field of view."), ("a mirror at a sharp bend in a road", "a convex mirror", "Drivers see more of the road."),
        ("a shop's security mirror", "a convex mirror", "It shows a large area of the shop."), ("a dentist's mirror for seeing teeth larger", "a concave mirror", "It gives a magnified image when held close."),
        ("the reflector behind a torch bulb", "a concave mirror", "It sends the light out as a strong beam."), ("a make-up mirror that magnifies", "a concave mirror", "Close objects look larger."),
        ("a dressing-table mirror", "a plane mirror", "It gives an image the same size as you."), ("a periscope", "two plane mirrors", "Each mirror turns the light through 90°.")]


def g_use():
    u, a, e = R.choice(USES)
    if not once(("us", u)):
        return None
    return item("Which kind of reflecting surface is used in %s?" % u, a, [x for x in ["a convex mirror", "a concave mirror", "a plane mirror", "two plane mirrors", "a glass prism"] if x != a][:3], e)


REFR = [("A ray of light passes from air into a glass block at an angle.", "It slows down and bends towards the normal."),
        ("A ray of light passes from water into air at an angle.", "It speeds up and bends away from the normal."),
        ("A ray of light enters a glass block along the normal.", "It slows down but does not bend."),
        ("A ray of light passes from air into water at an angle.", "It slows down and bends towards the normal."),
        ("A ray of light leaves a glass block into air at an angle.", "It speeds up and bends away from the normal.")]
RALL = ["It slows down and bends towards the normal.", "It speeds up and bends away from the normal.", "It slows down but does not bend.", "It speeds up and bends towards the normal.", "It slows down and bends away from the normal."]


def g_refr():
    s, a = R.choice(REFR)
    if not once(("rf", s)):
        return None
    return item(s + " What happens to the light?", a, R.sample([x for x in RALL if x != a], 3), "Light changes speed when it enters a different medium, so it bends (refracts) unless it travels along the normal.")


EFF = [("A swimming pool looks shallower than it really is.", "refraction"), ("A straw in a glass of water looks bent.", "refraction"),
       ("A rainbow forms when sunlight passes through raindrops.", "dispersion"), ("A prism splits white light into seven colours.", "dispersion"),
       ("You can see your face in a still pond.", "regular reflection"), ("You can read a book from any angle under a lamp.", "diffuse reflection"),
       ("A coin at the bottom of a cup of water looks higher than it is.", "refraction"), ("A sheet of paper does not give a clear image of your face.", "diffuse reflection"),
       ("A smooth, polished metal tray shows a clear image.", "regular reflection")]


def g_eff():
    s, a = R.choice(EFF)
    if not once(("ef", s)):
        return None
    return item(s + " Which effect of light explains this?", a, [x for x in ["refraction", "dispersion", "regular reflection", "diffuse reflection"] if x != a], "This is an example of %s." % a)


EM = [("infrared", "is given out by warm objects and is used in TV remote controls and thermal cameras"), ("ultraviolet", "can cause sunburn and skin cancer, but helps the skin make vitamin D"),
      ("ultraviolet", "is used to kill germs in water treatment, such as for NEWater"), ("infrared", "is felt as heat from the Sun and from a radiant heater"),
      ("visible light", "is the only part of the spectrum our eyes can detect")]


def g_em():
    a, d = R.choice(EM)
    if not once(("em", d)):
        return None
    return item("Which radiation %s?" % d, a, [x for x in ["infrared", "ultraviolet", "visible light", "sound"] if x != a][:3], "Infrared, visible light and ultraviolet are parts of the electromagnetic spectrum.")


B1 = bank([
    ("What does a ray in a ray diagram represent?", "the path along which light travels", ["the speed of light", "the colour of light", "the brightness of light"], "Rays are straight lines with arrows."),
    ("Why do we see objects that do not give out their own light?", "Light from a source reflects off them into our eyes.", ["Our eyes send out light.", "They absorb all light.", "Light bends around them."], "Most objects are seen by reflected light."),
    ("What is the difference between regular and diffuse reflection?", "A smooth surface reflects parallel rays in one direction; a rough surface scatters them in many directions.", ["Only smooth surfaces reflect light.", "Rough surfaces make clear images.", "There is no difference."], "Both follow the law of reflection at each point."),
    ("What is the law of reflection?", "The angle of incidence equals the angle of reflection, both measured from the normal.", ["The angle of incidence is twice the angle of reflection.", "Angles are measured from the mirror.", "Light always reflects at 90°."], "The incident ray, the reflected ray and the normal lie in the same plane."),
    ("Why does light refract when it enters glass from air?", "Its speed changes as it enters a different medium.", ["Glass is a light source.", "Glass reflects all light.", "Light gets heavier."], "Light travels more slowly in glass than in air."),
    ("What is dispersion?", "the splitting of white light into its colours by a prism", ["the bouncing of light off a mirror", "the dimming of light at night", "the bending of a ray along the normal"], "Different colours refract by different amounts."),
    ("Which colour is bent the most by a prism?", "violet", ["red", "green", "yellow"], "Red is bent the least."),
    ("What is light pollution?", "too much artificial light at night, which affects people, animals and our view of the stars", ["light that has been dirtied", "sunlight in the day", "light from fireflies"], "Bright lights can confuse turtles and migrating birds."),
])
B5 = bank([
    ("Why are the words AMBULANCE written backwards on the front of an ambulance?", "Drivers in front see the word correctly in their rear-view mirrors.", ["To make the word shorter.", "Because of refraction.", "Because the mirror is curved."], "A plane mirror laterally inverts the image."),
    ("A torch shines on a white wall and on a mirror. Why can a person standing to the side see the spot on the wall but not on the mirror?", "The wall scatters light in all directions; the mirror reflects it in one direction.", ["The wall gives out its own light.", "The mirror absorbs all the light.", "Light cannot reach the mirror."], "This is diffuse versus regular reflection."),
    ("A fisherman aims his spear below where a fish appears to be. Why?", "Light from the fish refracts at the water surface, so the fish is deeper than it looks.", ["Fish always swim down.", "Light travels in curves.", "The water reflects all light."], "Refraction makes objects in water look shallower."),
    ("Why are sunscreens with UV protection recommended for outdoor activities in Singapore?", "Ultraviolet radiation from the Sun can damage the skin.", ["Infrared makes the skin cold.", "Visible light causes cancer.", "Sunlight has no harmful rays."], "Singapore has a high UV index on most days."),
    ("A student measures an angle of incidence of 35° and an angle of reflection of 36°. What is the best explanation?", "a small error in measuring the angles", ["the law of reflection is wrong", "the mirror absorbed light", "the ray refracted"], "Repeating the measurement reduces errors."),
    ("A ray passes through a rectangular glass block at an angle. How does the ray that comes out compare with the ray that went in?", "It is parallel to the incoming ray but shifted sideways.", ["It is at 90° to it.", "It goes back the way it came.", "It is split into colours."], "It bends towards the normal on entering and away on leaving."),
])


def body():
    think = ("<p><b>Light travels in straight lines, shown as rays. It reflects off surfaces and refracts when its speed changes.</b></p>"
             "<ul><li>Law of reflection: <b>angle of incidence = angle of reflection</b>, both measured from the <b>normal</b>.</li>"
             "<li>Plane mirror image: upright, same size, laterally inverted, virtual, as far behind the mirror as the object is in front.</li>"
             "<li>Light <b>slows down</b> entering glass or water and bends towards the normal; it speeds up and bends away when it leaves.</li>"
             "<li>A prism splits white light into colours: <b>dispersion</b>. Infrared and ultraviolet are invisible radiation.</li></ul>")
    ex = [("A ray makes 30° with the mirror surface. Angle of reflection?", ["Angle of incidence = 90° − 30° = 60°"], "60°"),
          ("You stand 2 m from a plane mirror. How far are you from your image?", ["The image is 2 m behind the mirror"], "4 m")]
    mist = ["Measuring angles from the mirror instead of the normal.", "Saying light speeds up when it enters glass. It slows down.",
            "Saying a plane mirror image is upside down. It is upright but laterally inverted.", "Thinking rough surfaces do not reflect. They reflect diffusely."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Reflection", B1[:4] + [(g_eff, 4), (g_use, 6), (LI.g_refl, 3), (g_ang, 3)]),
        ("The law of reflection", [(g_ang, 10), (LI.g_refl, 6), (g_img, 4)]),
        ("Plane mirror images", [(g_img, 4), (g_dist, 10), (g_use, 2), (g_eff, 4)]),
        ("Refraction and dispersion", B1[4:7] + [(g_refr, 5), (LI.g_spec, 6), (g_eff, 3), (g_em, 3)]),
        ("Exam-style questions", B5 + B1[7:] + LI.B5 + [(g_em, 2), (g_dist, 2), (g_ang, 3)]),
    ])
    make_lss(1, "ray-model-of-light", 5, "Models", "Ray Model of Light",
             "Describe the ray model of light; describe reflection by smooth and rough surfaces and the uses of plane and curved mirrors; investigate the image formed by a plane mirror "
             "and that the angle of incidence equals the angle of reflection; explain refraction as caused by a change in the speed of light and describe the dispersion of white light by a prism; "
             "recognise effects of infrared and ultraviolet radiation and light pollution (summary of the MOE Lower Secondary Science Syllabus).",
             "Ray Model of Light: Reflection and Refraction", seo(1, "Reflection and Refraction of Light"), "Ray model of light",
             "Free Secondary 1 science worksheets for Singapore students on the ray model of light: the law of reflection, plane mirror images, curved mirrors, refraction and dispersion. With answers.",
             "Angle of incidence = angle of reflection.", "Measure both angles from the normal.",
             body(),
             [("Why are angles measured from the normal?", "The normal is a line at 90° to the surface. Measuring from it makes the law of reflection the same for every surface."),
              ("Why does a straw look bent in water?", "Light from the straw refracts as it leaves the water, so the part in the water appears higher than it is."),
              ("What is lateral inversion?", "Left and right are swapped in a plane mirror image.")],
             sets)


if __name__ == "__main__":
    main()
