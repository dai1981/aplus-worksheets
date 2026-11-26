# -*- coding: utf-8 -*-
"""Class 10 Science, Unit III Natural Phenomena (NCERT chapters 9–10) and Unit IV Effects of Current (chapters 11–12): question makers.
New Cartesian sign convention as in NCERT: distances measured from the pole / optical centre, in the direction of incident light positive.
Mirror: 1/v + 1/u = 1/f, m = −v/u. Lens: 1/v − 1/u = 1/f, m = v/u, P = 1/f (f in metres)."""
from fractions import Fraction as F
from uk_alsci import nf, nq, tq, once_maker
from in_sci import pairs, name, _R, U, K

E_CH = 1.6e-19


def ch(xs):
    return _R[0].choice(xs)


def sg(x):
    """signed number with the NCERT minus sign: −15, +20"""
    x = F(x)
    s = str(abs(x.numerator)) if x.denominator == 1 else nf(abs(float(x)))
    return ("−" if x < 0 else "+") + s


def cm(x):
    return sg(x) + " cm"


# =================================================================== Chapter 9: light
def mirror_case():
    R = _R[0]
    for _ in range(200):
        kind = R.choice(["concave", "concave", "convex"])
        f = F(R.choice([10, 12, 15, 20, 24, 25, 30, 40]))
        f = -f if kind == "concave" else f
        u = -F(R.choice(range(5, 91, 5)))
        if 1 / f - 1 / u == 0:
            continue
        v = 1 / (1 / f - 1 / u)
        if v.denominator == 1 and abs(v) <= 240 and v != u:
            return kind, f, u, v
    return None


def lens_case():
    R = _R[0]
    for _ in range(200):
        kind = R.choice(["convex", "convex", "concave"])
        f = F(R.choice([10, 12, 15, 20, 24, 25, 30, 40]))
        f = -f if kind == "concave" else f
        u = -F(R.choice(range(5, 91, 5)))
        if 1 / f + 1 / u == 0:
            continue
        v = 1 / (1 / f + 1 / u)
        if v.denominator == 1 and abs(v) <= 240:
            return kind, f, u, v
    return None


def c_mirror(k=None):
    c = mirror_case()
    if not c:
        return None
    kind, f, u, v = c
    k = k or ch(["v", "f", "m", "nature"])
    m = -v / u
    if k == "v":
        alt = [-v, v * 2, v / 2, -u, f]
        alt = [x for x in alt if x != v and F(x).denominator == 1]
        return tq("An object is placed %d cm in front of a %s mirror of focal length %d cm. Where is the image? (Use 1/v + 1/u = 1/f.)" % (-u, kind, abs(f)), "v = %s" % cm(v),
                  ["v = %s" % cm(x) for x in alt], "u = %s, f = %s; 1/v = 1/f − 1/u, so v = <b>%s</b> (%s image)." % (cm(u), cm(f), cm(v), "real" if v < 0 else "virtual"))
    if k == "f":
        return tq("A %s mirror forms an image at v = %s for an object at u = %s. What is its focal length?" % (kind, cm(v), cm(u)), "f = %s" % cm(f),
                  ["f = %s" % cm(x) for x in [-f, f * 2, (u + v) / 2] if x != f], "1/f = 1/v + 1/u, so f = <b>%s</b>; the radius of curvature is %s." % (cm(f), cm(2 * f)))
    if k == "m":
        return tq("An object is %d cm in front of a %s mirror; the image is at v = %s. What is the magnification?" % (-u, kind, cm(v)), "m = %s" % sg(m),
                  ["m = %s" % sg(x) for x in [-m, v / u, 1 / m, -1 / m, m * 2] if x != m], "m = −v/u = −(%s)/(%s) = <b>%s</b>. Negative m means real and inverted." % (sg(v), sg(u), sg(m)))
    nat = ("real and inverted" if v < 0 else "virtual and erect") + (", enlarged" if abs(m) > 1 else ", diminished" if abs(m) < 1 else ", same size")
    opts = ["real and inverted, enlarged", "real and inverted, diminished", "real and inverted, same size", "virtual and erect, enlarged", "virtual and erect, diminished"]
    return tq("An object is %d cm in front of a %s mirror of focal length %d cm. Describe the image." % (-u, kind, abs(f)), nat, _R[0].sample([x for x in opts if x != nat], 3),
              "v = %s and m = %s: %s." % (cm(v), sg(m), nat))


def c_lens(k=None):
    c = lens_case()
    if not c:
        return None
    kind, f, u, v = c
    k = k or ch(["v", "f", "m", "P"])
    m = v / u
    if k == "v":
        return tq("An object is placed %d cm from a %s lens of focal length %d cm. Where is the image? (Use 1/v − 1/u = 1/f.)" % (-u, kind, abs(f)), "v = %s" % cm(v),
                  ["v = %s" % cm(x) for x in [-v, v * 2, f - u, -u] if x != v], "1/v = 1/f + 1/u, so v = <b>%s</b> (%s)." % (cm(v), "real, on the other side" if v > 0 else "virtual, on the same side as the object"))
    if k == "f":
        return tq("A %s lens forms an image at v = %s for an object at u = %s. What is its focal length?" % (kind, cm(v), cm(u)), "f = %s" % cm(f),
                  ["f = %s" % cm(x) for x in [-f, f * 2, f / 2, v - u] if x != f], "1/f = 1/v − 1/u, so f = <b>%s</b>." % cm(f))
    if k == "m":
        return tq("An object is %d cm from a %s lens; the image is at v = %s. What is the magnification?" % (-u, kind, cm(v)), "m = %s" % sg(m),
                  ["m = %s" % sg(x) for x in [-m, u / v, m * 2, -u / v] if x != m], "For a lens m = v/u = (%s)/(%s) = <b>%s</b>." % (sg(v), sg(u), sg(m)))
    P = 100 / f
    return nq("What is the power of a %s lens of focal length %d cm?" % (kind, abs(f)), float(P), [float(-P), float(1 / f), float(f / 100)], " D",
              "P = 1/f with f in metres: 1/(%s m) = <b>%s D</b>." % (sg(f / 100), sg(P) if P.denominator == 1 else nf(float(P))))


N_MED = [("water", 1.33), ("glass (crown)", 1.52), ("diamond", 2.42), ("kerosene", 1.44), ("alcohol", 1.36), ("ice", 1.31), ("turpentine oil", 1.47), ("rock salt", 1.54), ("ruby", 1.71), ("benzene", 1.50)]


def c_refr(k=None):
    k = k or ch(["v", "n", "rel", "dense"])
    m, n = ch(N_MED)
    if k == "v":
        return nq("The refractive index of %s is %s. What is the speed of light in %s? (c = 3 × 10<sup>8</sup> m/s)" % (m, nf(n, 3), m), 3e8 / n, [3e8 * n, n / 3e8, 3e8 / n / 2], " m/s",
                  "v = c/n = 3 × 10<sup>8</sup> ÷ %s = <b>%s m/s</b>." % (nf(n, 3), nf(3e8 / n)))
    if k == "n":
        sp = 3e8 / n
        return nq("Light travels at %s m/s in %s. What is its refractive index? (c = 3 × 10<sup>8</sup> m/s)" % (nf(sp), m), n, [1 / n, n - 1, n * 3 / 2], "", "n = c/v = <b>%s</b>." % nf(n, 3), sf=3)
    if k == "dense":
        (a, x), (b, y) = _R[0].sample(N_MED, 2)
        if x == y:
            return None
        hi = a if x > y else b
        return tq("Refractive index of %s = %s and of %s = %s. In which does light travel faster?" % (a, nf(x, 3), b, nf(y, 3)), b if hi == a else a, [hi, "at the same speed in both", "it cannot be said"],
                  "Light is slower in the optically denser medium (higher refractive index).")
    (a, x), (b, y) = _R[0].sample(N_MED, 2)
    return nq("What is the refractive index of %s with respect to %s? (n of %s = %s, n of %s = %s)" % (a, b, a, nf(x, 3), b, nf(y, 3)), x / y, [y / x, x * y, x - y + 1 if x != y else 0.5], "",
              "n<sub>21</sub> = n<sub>2</sub>/n<sub>1</sub> = %s ÷ %s = <b>%s</b>." % (nf(x, 3), nf(y, 3), nf(x / y)))


CONCAVE_POS = [("beyond C", "between F and C; real, inverted and diminished"), ("at C", "at C; real, inverted and the same size"), ("between C and F", "beyond C; real, inverted and enlarged"),
               ("at F", "at infinity; real, inverted and highly enlarged"), ("between P and F", "behind the mirror; virtual, erect and enlarged"), ("at infinity", "at F; real, inverted and highly diminished")]
CONVEX_POS = [("at infinity", "at F; real, inverted and highly diminished"), ("beyond 2F₁", "between F₂ and 2F₂; real, inverted and diminished"), ("at 2F₁", "at 2F₂; real, inverted and the same size"),
              ("between F₁ and 2F₁", "beyond 2F₂; real, inverted and enlarged"), ("at F₁", "at infinity; real, inverted and highly enlarged"), ("between F₁ and O", "on the same side as the object; virtual, erect and enlarged")]
LIGHT = [("Which mirror is used as a rear-view mirror in vehicles?", "a convex mirror, because it gives a wider field of view with an erect image", ["a concave mirror", "a plane mirror only", "a concave lens"], "Its image is always virtual, erect and diminished."),
         ("Which mirror is used by dentists?", "a concave mirror, to see a large image of the teeth", ["a convex mirror", "a plane mirror", "a cylindrical mirror"], "The tooth is placed between P and F."),
         ("Which mirror is used in torches and headlights?", "a concave mirror, with the bulb at its focus", ["a convex mirror", "a plane mirror", "a convex lens"], "It gives a parallel beam."),
         ("What is the relation between focal length and radius of curvature?", "R = 2f", ["f = 2R", "R = f", "R = f²"], "f is half the radius of curvature."),
         ("What is the focal length of a plane mirror?", "infinity", ["zero", "1 m", "equal to the object distance"], "Its radius of curvature is infinite."),
         ("What does a negative magnification mean?", "the image is real and inverted", ["the image is virtual and erect", "the image is larger", "there is no image"], "Positive m means virtual and erect."),
         ("Why does a pencil look bent when partly dipped in water?", "light refracts as it passes from water into air", ["light reflects from the water", "water magnifies the pencil", "the pencil really bends"], "Refraction changes the direction of light."),
         ("What are the laws of refraction?", "the rays and normal are in one plane, and sin i / sin r is constant (Snell's law)", ["the angle of incidence equals the angle of reflection", "light always speeds up", "light travels in circles"], "The constant is the refractive index."),
         ("When light goes from air into glass, how does it bend?", "towards the normal", ["away from the normal", "it does not bend", "it reflects back"], "Glass is optically denser."),
         ("What happens to a ray of light that passes through a glass slab?", "it comes out parallel to the incident ray but shifted sideways", ["it comes out along the normal", "it stops inside", "it bends by 90°"], "The sideways shift is the lateral displacement."),
         ("What is the unit of the power of a lens?", "dioptre (D)", ["metre", "watt", "joule"], "1 D is the power of a lens of focal length 1 m."),
         ("What is the sign of the power of a concave lens?", "negative", ["positive", "zero", "it can be either"], "A concave lens has a negative focal length."),
         ("What is the total power of a +2.0 D lens in contact with a −0.5 D lens?", "+1.5 D", ["+2.5 D", "−1.5 D", "−2.5 D"], "Powers of lenses in contact add."),
         ("Which lens always gives a virtual, erect and diminished image?", "a concave lens", ["a convex lens", "a concave mirror", "a plane mirror"], "A convex mirror does too."),
         ("Where should an object be placed in front of a convex lens to get a real image of the same size?", "at 2F₁", ["at F₁", "between F₁ and O", "at infinity"], "The image forms at 2F₂."),
         ("Which ray goes undeviated through a lens?", "a ray through the optical centre", ["a ray parallel to the axis", "a ray through the focus", "every ray"], "A ray parallel to the axis passes through F after refraction."),
         ("Which ray is reflected back along its own path by a concave mirror?", "a ray through the centre of curvature", ["a ray through the focus", "a ray parallel to the axis", "a ray to the pole"], "It hits the mirror along the normal."),
         ("Why is a concave mirror used in solar furnaces?", "it concentrates sunlight at its focus, producing heat", ["it spreads light out", "it makes virtual images", "it absorbs light"], "Large concave mirrors are used."),
         ("What is the absolute refractive index of a medium?", "the speed of light in vacuum divided by its speed in the medium", ["the speed of light in the medium", "the angle of refraction", "the focal length of a lens"], "n = c/v.")]


# =================================================================== Chapter 10: the human eye and the colourful world
EYE = [("the cornea", "a thin transparent membrane where most of the refraction of light happens"), ("the iris", "a dark muscular diaphragm that controls the size of the pupil"),
       ("the pupil", "the opening that controls the amount of light entering the eye"), ("the eye lens", "fine-adjusting the focal length to focus images on the retina"),
       ("the ciliary muscles", "changing the curvature of the eye lens"), ("the retina", "a light-sensitive screen where the image is formed"),
       ("the optic nerve", "carrying electrical signals from the retina to the brain"), ("rods", "light-sensitive cells that respond to dim light"), ("cones", "cells that respond to colour")]
DEFECT = [("myopia (near-sightedness)", "a concave lens"), ("hypermetropia (far-sightedness)", "a convex lens"), ("presbyopia with both near and distant vision problems", "a bifocal lens")]
SKY = [("Why does the sky look blue?", "air molecules scatter blue light much more than red light", ["the sea reflects blue light", "sunlight is blue", "the atmosphere absorbs red light only"], "Fine particles scatter shorter wavelengths more."),
       ("Why does the Sun look reddish at sunrise and sunset?", "light travels through more air, so most blue light is scattered away", ["the Sun is cooler then", "the clouds are red", "red light is absorbed"], "Red light reaches our eyes."),
       ("Why are danger signals red?", "red light is scattered least by fog and smoke, so it can be seen from far", ["red is the brightest colour", "red light is fastest", "red is easy to make"], "It has the longest wavelength of visible light."),
       ("Why do stars twinkle?", "atmospheric refraction keeps changing the apparent position and brightness of starlight", ["stars switch on and off", "stars move very fast", "clouds block them"], "Stars are point sources."),
       ("Why do planets not twinkle?", "they are close and act as extended sources, so changes average out", ["they do not give light", "they are made of rock", "they are too far"], "The total light reaching us stays almost the same."),
       ("Why do we see the Sun about 2 minutes before actual sunrise?", "atmospheric refraction bends sunlight towards us", ["the Earth spins faster in the morning", "light travels faster at dawn", "the Sun is closer in the morning"], "Sunset is delayed by about 2 minutes too."),
       ("What is dispersion of light?", "splitting of white light into its colours", ["bending of light at a surface", "reflection of light", "scattering of light by dust"], "A prism disperses white light into VIBGYOR."),
       ("Which colour bends the most in a prism?", "violet", ["red", "yellow", "green"], "Violet has the shortest wavelength; red bends the least."),
       ("How is a rainbow formed?", "water droplets in the air disperse sunlight by refraction, internal reflection and refraction again", ["by clouds reflecting light", "by the Sun's colours mixing", "by scattering of red light"], "It is always opposite the Sun."),
       ("What did Newton show with a second, inverted prism?", "the colours recombine to give white light", ["white light is a single colour", "red bends most", "prisms make colour"], "So white light is a mixture of colours."),
       ("What is the Tyndall effect?", "scattering of light by colloidal particles, making the path of a beam visible", ["bending of light in a prism", "reflection of light by a mirror", "absorption of light by water"], "Seen when sunlight enters a smoky room."),
       ("What is the near point of a normal eye?", "about 25 cm", ["about 1 m", "about 2 cm", "infinity"], "The far point is at infinity."),
       ("What is the power of accommodation of the eye?", "its ability to change the focal length of the eye lens", ["its ability to see colours", "its ability to see in the dark", "the size of the pupil"], "Ciliary muscles change the lens shape."),
       ("What causes a cataract?", "the eye lens becomes cloudy", ["the retina detaches", "the pupil closes", "the cornea becomes thin"], "It can be treated by surgery."),
       ("Why do we have two eyes instead of one?", "for a wider field of view and depth perception", ["to see colours", "to see at night", "to avoid myopia"], "Each eye sees a slightly different image."),
       ("Why is the colour of the clear sky black for an astronaut in space?", "there is no atmosphere to scatter sunlight", ["space is full of dust", "the Sun is dim in space", "blue light is absorbed"], "Scattering needs particles."),
       ("What happens to the pupil in dim light?", "it becomes larger to let in more light", ["it becomes smaller", "it closes", "it turns red"], "The iris controls its size."),
       ("Why does the sky look white on a hazy day?", "large particles scatter all colours about equally", ["the air is cold", "the Sun is white", "the clouds absorb blue"], "Very fine particles scatter mainly blue."),
       ("Why does the sun look flattened (oval) near the horizon?", "atmospheric refraction bends light from its lower edge more", ["the Sun changes shape", "clouds cover part of it", "the Earth is flat there"], "Refraction is larger near the horizon."),
       ("What is the spectrum of white light?", "the band of seven colours produced by dispersion", ["a single colour", "a shadow", "an image in a mirror"], "VIBGYOR: violet, indigo, blue, green, yellow, orange, red."),
       ("Why does a glass prism split white light but a glass slab does not?", "in a prism the faces are not parallel, so the colours stay separated", ["a slab is not made of glass", "a slab absorbs colour", "a prism reflects light"], "In a slab the colours recombine as they come out parallel."),
       ("What is atmospheric refraction?", "refraction of light by layers of air of different temperature and density", ["reflection from clouds", "scattering by dust", "absorption by ozone"], "Hot air is optically rarer than cooler air."),
       ("Why does an object seen through hot air above a fire seem to wobble?", "the refractive index of the hot air keeps changing", ["the object is moving", "smoke reflects light", "the fire bends the object"], "This is atmospheric refraction on a small scale."),
       ("What is the angle of deviation in a prism?", "the angle between the incident ray and the emergent ray", ["the angle of the prism", "the angle of incidence", "the angle of reflection"], "It depends on the colour of light."),
       ("What kind of light does an astronaut see from the Sun in space?", "white light, against a dark sky", ["blue light only", "red light only", "no light"], "There is no air to scatter it."),
       ("Why can we not see clearly an object closer than 25 cm?", "the eye lens cannot become any more curved", ["the retina is too far away", "the pupil closes", "the cornea is too thick"], "25 cm is the least distance of distinct vision."),
       ("What causes myopia?", "the eyeball is too long or the eye lens is too curved", ["the eyeball is too short", "the lens is too weak", "the pupil is too small"], "The image of a far object forms in front of the retina."),
       ("What causes hypermetropia?", "the eyeball is too short or the focal length of the eye lens is too long", ["the eyeball is too long", "the lens is too curved", "the retina is damaged"], "The image of a near object would form behind the retina.")]


PRISM = [("In white light passing through a prism, which colour bends the least?", "red"), ("Which colour lies between green and indigo in the spectrum?", "blue"),
         ("Which colour lies between orange and green in the spectrum?", "yellow"), ("Which colour of visible light has the shortest wavelength?", "violet"),
         ("Which colour of visible light has the longest wavelength?", "red"), ("Which colour lies between yellow and blue in the spectrum?", "green"),
         ("Which colour lies between red and yellow in the spectrum?", "orange"), ("Which colour lies between blue and violet in the spectrum?", "indigo"),
         ("Which colour is at the top (outer edge) of a primary rainbow?", "red"), ("Which colour is at the bottom (inner edge) of a primary rainbow?", "violet"),
         ("Which colour of light is scattered the most by air molecules?", "violet"), ("Which colour does a clear sky look to us at noon?", "blue")]
WIRE = [("which wire usually has red (or brown) insulation?", "the live wire"), ("which wire usually has black (or blue) insulation?", "the neutral wire"),
        ("which wire usually has green insulation?", "the earth wire"), ("which wire is at 220 V?", "the live wire"), ("which wire is at zero potential?", "the neutral wire"),
        ("which wire is connected to a metal plate deep in the ground?", "the earth wire"), ("in which wire is the fuse or switch placed?", "the live wire"),
        ("which wire is joined to the metal body of an appliance?", "the earth wire"), ("which device cuts off the current on overload instead of a fuse wire?", "a miniature circuit breaker (MCB)"),
        ("what current rating is the separate circuit for geysers and air coolers?", "15 A"), ("what current rating is the circuit for bulbs and fans?", "5 A")]


def c_eye(k=None):
    k = k or ch(["myopia", "hyper", "defect", "far", "fl"])
    if k == "far":
        P = ch([-0.25, -0.4, -0.5, -0.8, -1.0, -1.25, -2.0, -2.5, -4.0, -5.0])
        return nq("A myopic person is prescribed a lens of power %s D. What is the far point of the uncorrected eye?" % nf(P, 3), -100 / P, [100 / P * -1 * 2, -P * 100, -1 / P], " cm",
                  "f = 1/P = %s m, so the far point is <b>%s cm</b> from the eye." % (nf(1 / P, 3), nf(-100 / P)))
    if k == "fl":
        P = ch([-4.0, -2.5, -2.0, -1.25, -0.5, 0.5, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]) 
        f = 100 / P
        return nq("An optician prescribes a lens of power %s%s D. What is its focal length?" % ("+" if P > 0 else "", nf(P, 3)), f, [-f, P * 100 if abs(P) < 1 else f / 10, 1 / P], " cm",
                  "f = 1/P = %s m = <b>%s cm</b> (%s lens)." % (nf(1 / P, 3), nf(f), "convex" if P > 0 else "concave"))
    if k == "defect":
        d, l = ch(DEFECT)
        return tq("Which lens corrects %s?" % d, l, [x for x in ["a concave lens", "a convex lens", "a bifocal lens", "a cylindrical lens"] if x != l][:3], "Myopia: concave; hypermetropia: convex; presbyopia with both problems: bifocal.")
    if k == "myopia":
        d = ch([0.4, 0.5, 0.6, 0.75, 0.8, 1.0, 1.2, 1.25, 1.5, 2.0, 2.5, 4.0, 5.0])
        P = -1 / d
        return nq("The far point of a myopic eye is %s m. What is the power of the lens needed to correct it?" % nf(d, 3), P, [-P, d, -d], " D",
                  "The lens must make distant objects seem to be at %s m: f = −%s m, P = 1/f = <b>%s D</b> (concave)." % (nf(d, 3), nf(d, 3), nf(P)), sf=3)
    N = ch([30, 40, 50, 60, 75, 80, 100, 120, 125, 150, 200])
    f = 1 / (1 / F(-N) - 1 / F(-25))
    P = 100 / f
    return nq("The near point of a hypermetropic eye is %d cm. What power of lens lets it read at 25 cm?" % N, float(P), [float(-P), float(100 / F(N)), float(100 / F(25))], " D",
              "u = −25 cm, v = −%d cm: 1/f = 1/v − 1/u, f = %s cm, P = 100/f = <b>%s D</b> (convex)." % (N, nf(float(f)), nf(float(P))), sf=3)


# =================================================================== Chapter 11: electricity
def c_elec(k=None):
    R = _R[0]
    k = k or ch(["ohm", "charge", "electrons", "work", "series", "parallel", "rho", "power", "kwh", "heat"])
    if k == "ohm":
        v = ch([1.5, 3, 4.5, 6, 9, 12, 24, 220])
        r = ch([2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 50, 100, 220, 440])
        w = ch(["I", "R", "V"])
        I = v / r
        if w == "I":
            return nq("A %s V battery is connected across a %d Ω resistor. What current flows?" % (nf(v, 3), r), I, [v * r, r / v, I * 2], " A", "I = V/R = %s ÷ %d = <b>%s A</b>." % (nf(v, 3), r, nf(I)))
        if w == "R":
            return nq("A current of %s A flows when %s V is applied across a conductor. What is its resistance?" % (nf(I), nf(v, 3)), r, [v * I, I / v, r * 2], " Ω", "R = V/I = <b>%s Ω</b>." % nf(r))
        return nq("What potential difference is needed to drive %s A through a %d Ω resistor?" % (nf(I), r), v, [I / r, r / I, v / 2], " V", "V = IR = <b>%s V</b>." % nf(v, 3))
    if k == "charge":
        I, t = ch([0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 4.0, 5.0]), ch([10, 20, 30, 60, 120, 300, 600])
        return nq("A current of %s A flows for %d s. How much charge passes?" % (nf(I, 2), t), I * t, [I / t, t / I, I * t / 60], " C", "Q = It = <b>%s C</b>." % nf(I * t))
    if k == "electrons":
        Q = ch([1, 2, 5, 8, 10, 16, 20])
        return nq("How many electrons make up a charge of %d C? (e = 1.6 × 10<sup>−19</sup> C)" % Q, Q / E_CH, [Q * E_CH, E_CH / Q, Q / E_CH / 10], "", "n = Q/e = %d ÷ 1.6 × 10<sup>−19</sup> = <b>%s</b>." % (Q, nf(Q / E_CH)))
    if k == "work":
        Q, V = ch([2, 4, 5, 10, 12, 20, 50]), ch([1.5, 3, 6, 9, 12, 220])
        return nq("How much work is done in moving %d C of charge across a potential difference of %s V?" % (Q, nf(V, 3)), Q * V, [Q / V, V / Q, Q + V], " J", "W = QV = <b>%s J</b>." % nf(Q * V))
    if k in ("series", "parallel"):
        rs = sorted(R.sample([2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60], ch([2, 3])))
        ser = sum(rs)
        par = 1 / sum(F(1, x) for x in rs)
        txt = ", ".join("%d Ω" % x for x in rs)
        if k == "series":
            return nq("Resistors of %s are joined in series. What is the total resistance?" % txt, ser, [float(par), ser / len(rs), max(rs)], " Ω", "In series R = R₁ + R₂ + … = <b>%d Ω</b>." % ser)
        if par.denominator > 12:
            return None
        return nq("Resistors of %s are joined in parallel. What is the total resistance?" % txt, float(par), [ser, float(sum(F(1, x) for x in rs)), min(rs)], " Ω",
                  "1/R = %s, so R = <b>%s Ω</b> (less than the smallest resistor)." % (" + ".join("1/%d" % x for x in rs), nf(float(par))))
    if k == "rho":
        rho, mat = ch([(1.72e-8, "copper"), (2.82e-8, "aluminium"), (1.0e-6, "nichrome"), (1.60e-8, "silver"), (10.0e-8, "iron")])
        L, A = ch([1, 2, 5, 10, 50, 100]), ch([1e-6, 2e-6, 5e-7, 1e-7, 4e-6])
        return nq("A %s wire (ρ = %s Ω m) is %d m long with a cross-sectional area of %s m². What is its resistance?" % (mat, nf(rho), L, nf(A)), rho * L / A, [rho * A / L, rho / (L * A), L / (rho * A) / 1e12], " Ω",
                  "R = ρL/A = <b>%s Ω</b>." % nf(rho * L / A))
    if k == "power":
        V = ch([12, 110, 220, 230])
        I = ch([0.1, 0.25, 0.5, 1, 2, 4, 5])
        w = ch(["P", "I"])
        if w == "P":
            return nq("An appliance draws %s A from a %d V supply. What is its power?" % (nf(I, 2), V), V * I, [V / I, I / V, V * I * I], " W", "P = VI = <b>%s W</b>." % nf(V * I))
        P = ch([40, 60, 100, 500, 1000, 1500, 2000])
        return nq("A %s W electric appliance runs on 220 V. What current does it draw?" % "{:,}".format(P), P / 220, [220 / P, P / 2200, P / 220 * 2], " A", "I = P/V = %s ÷ 220 = <b>%s A</b>." % ("{:,}".format(P), nf(P / 220)))
    if k == "kwh":
        P, h, d, rate = ch([100, 200, 250, 400, 500, 1000, 1500, 2000]), ch([2, 3, 4, 5, 6, 8, 10]), ch([10, 15, 20, 30]), ch([5, 6, 7, 8])
        e = P * h * d / 1000
        nm = name()
        return _rupee(nq("%s uses a %s W appliance for %d hours a day for %d days. Electricity costs ₹%d per unit (kWh). What is the cost?" % (nm, "{:,}".format(P), h, d, rate), e * rate,
                         [P * h * d * rate / 100, e, P * h * rate / 1000, e * rate * 10], "", "Energy = %s W × %d h × %d days = %s kWh; cost = %s × ₹%d = <b>₹%s</b>." % ("{:,}".format(P), h, d, nf(e), nf(e), rate, nf(e * rate))))
    I, Rr, t = ch([0.5, 1, 2, 3, 4, 5]), ch([2, 4, 5, 10, 20, 50]), ch([10, 30, 60, 120, 300])
    return nq("A current of %s A flows through a %d Ω resistor for %d s. How much heat is produced?" % (nf(I, 2), Rr, t), I * I * Rr * t, [I * Rr * t, I * Rr * Rr * t, I * I * Rr], " J",
              "H = I²Rt = %s² × %d × %d = <b>%s J</b>." % (nf(I, 2), Rr, t, nf(I * I * Rr * t)))


def _rupee(it):
    """put ₹ in front of the numbers of a cost question"""
    if not it:
        return None
    it["c"] = ["₹" + c for c in it["c"]]
    return it


ELEC = [("What is the SI unit of electric current?", "ampere", ["volt", "ohm", "coulomb"], "1 A = 1 C/s."),
        ("How is an ammeter connected in a circuit?", "in series", ["in parallel", "across the cell only", "it is not connected"], "It measures the current through the circuit."),
        ("How is a voltmeter connected?", "in parallel across the component", ["in series", "to the earth", "inside the battery"], "It measures potential difference."),
        ("What does Ohm's law state?", "the current is proportional to the potential difference, if temperature stays the same", ["current is proportional to resistance", "voltage is always zero", "resistance increases with current"], "V = IR."),
        ("On which factors does the resistance of a wire depend?", "length, area of cross-section and material", ["only its colour", "only the voltage", "only its mass"], "R = ρL/A."),
        ("What happens to the resistance of a wire if its length is doubled?", "it doubles", ["it halves", "it stays the same", "it becomes four times"], "R is proportional to L."),
        ("What happens to the resistance if the area of cross-section is doubled?", "it halves", ["it doubles", "it stays the same", "it becomes four times"], "R is inversely proportional to A."),
        ("Why is tungsten used for bulb filaments?", "it has a very high melting point and glows when hot", ["it is a poor conductor of heat", "it is cheap", "it does not get hot"], "Bulbs are filled with nitrogen or argon to protect it."),
        ("Why is nichrome used in electric heaters?", "it has a high resistivity and does not oxidise easily when hot", ["it has very low resistance", "it is a good insulator", "it melts easily"], "Alloys have higher resistivity than pure metals."),
        ("Why are household appliances connected in parallel?", "each gets the full voltage and can be switched on or off separately", ["the total resistance increases", "they share the voltage", "it uses less wire"], "One fault does not stop the others."),
        ("What is the commercial unit of electrical energy?", "kilowatt hour (kWh), also called a unit", ["joule", "watt", "volt"], "1 kWh = 3.6 × 10⁶ J."),
        ("How many joules are in 1 kWh?", "3.6 × 10⁶ J", ["1,000 J", "3,600 J", "36,000 J"], "1,000 W × 3,600 s."),
        ("What is the function of a fuse?", "it melts and breaks the circuit when too much current flows", ["it increases the current", "it stores charge", "it measures voltage"], "It works by the heating effect of current."),
        ("What is 1 volt?", "the potential difference when 1 joule of work moves 1 coulomb of charge", ["1 coulomb per second", "1 joule per second", "1 ampere per ohm"], "V = W/Q."),
        ("What is 1 ohm?", "the resistance when a potential difference of 1 V drives a current of 1 A", ["1 volt per second", "1 coulomb per ampere", "1 watt per ampere"], "R = V/I."),
        ("Which is a good conductor of electricity?", "copper", ["glass", "rubber", "dry wood"], "Insulators have very high resistivity."),
        ("What happens to the total resistance when more resistors are added in parallel?", "it decreases", ["it increases", "it stays the same", "it becomes infinite"], "There are more paths for the current."),
        ("Which electrical quantity is the same in all resistors joined in series?", "the current", ["the potential difference", "the power", "the resistance"], "In parallel, the potential difference is the same."),
        ("What is the SI unit of resistivity?", "ohm metre (Ω m)", ["ohm", "ohm per metre", "volt metre"], "ρ = RA/L."),
        ("Does the resistivity of a wire change if it is cut in half?", "no, resistivity depends only on the material and temperature", ["yes, it halves", "yes, it doubles", "yes, it becomes zero"], "Resistance halves, but resistivity stays the same."),
        ("Why are copper and aluminium used for electrical transmission lines?", "they have low resistivity", ["they have high resistivity", "they are magnetic", "they are insulators"], "Less energy is lost as heat."),
        ("What is the SI unit of electric power?", "watt", ["joule", "kilowatt hour", "volt"], "1 W = 1 J/s = 1 V × 1 A."),
        ("What is the direction of conventional current?", "from the positive terminal to the negative terminal, outside the cell", ["the same as the flow of electrons", "from negative to positive", "in both directions"], "Electrons flow the opposite way."),
        ("What is an electric circuit?", "a continuous and closed path for electric current", ["a battery alone", "an open switch", "a single wire end"], "Current flows only in a closed circuit."),
        ("Which device keeps a potential difference across a conductor?", "a cell or battery", ["an ammeter", "a voltmeter", "a fuse"], "The chemical action in the cell does work on the charges."),
        ("What happens to the heat produced in a resistor if the current is doubled?", "it becomes four times", ["it doubles", "it halves", "it stays the same"], "H = I²Rt."),
        ("Why does the cord of a heater not glow while the element does?", "the cord has very low resistance, so little heat is produced", ["the cord carries less current", "the cord is cooled by air", "the element is closer to the socket"], "The same current flows through both.")]


# =================================================================== Chapter 12: magnetic effects of electric current
DIRS = {"east": (1, 0, 0), "west": (-1, 0, 0), "north": (0, 1, 0), "south": (0, -1, 0), "upwards": (0, 0, 1), "downwards": (0, 0, -1)}


def c_flem(k=None):
    R = _R[0]
    a, b = R.sample(sorted(DIRS), 2)
    va, vb = DIRS[a], DIRS[b]
    cr = (va[1] * vb[2] - va[2] * vb[1], va[2] * vb[0] - va[0] * vb[2], va[0] * vb[1] - va[1] * vb[0])
    if cr == (0, 0, 0):
        return None
    f = next(n for n, v in DIRS.items() if v == cr)
    opp = next(n for n, v in DIRS.items() if v == tuple(-x for x in cr))
    w = k or R.choice(["force", "force", "current", "field"])
    ah = lambda d: d.replace("upwards", "top").replace("downwards", "bottom")
    if w == "current":
        return tq("A wire in a magnetic field pointing %s feels a force %s. By Fleming's left-hand rule, which way does the current flow?" % (b, f), "towards the " + ah(a),
                  ["towards the " + ah(x) for x in DIRS if x not in (a, b, f)], "Forefinger: field (%s); thumb: force (%s); middle finger: current, towards the <b>%s</b>." % (b, f, ah(a)))
    if w == "field":
        return tq("A current flows towards the %s in a wire that feels a force %s. By Fleming's left-hand rule, which way does the magnetic field point?" % (ah(a), f), b,
                  [x for x in DIRS if x not in (a, b, f)], "Middle finger: current (%s); thumb: force (%s); forefinger: field (<b>%s</b>)." % (a, f, b))
    return tq("A wire carries a current towards the %s in a magnetic field pointing %s. Using Fleming's left-hand rule, which way is the force on the wire?" % (a.replace("upwards", "top").replace("downwards", "bottom"), b), f,
              [opp, a, b], "Forefinger: field (%s); middle finger: current (%s); thumb: force (<b>%s</b>)." % (b, a, f))


def c_fuse(k=None):
    P = ch([40, 60, 100, 150, 200, 250, 300, 400, 500, 600, 750, 800, 1000, 1100, 1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000])
    I = P / 220
    fuses = [1, 3, 5, 10, 15]
    best = next((x for x in fuses if x >= I * 1.1), None)
    if not best:
        return None
    return tq("An appliance rated %s W, 220 V is used at home. Which fuse is most suitable: 1 A, 3 A, 5 A, 10 A or 15 A?" % "{:,}".format(P), "%d A" % best,
              ["%d A" % x for x in fuses if x != best][:3] if best > 3 else ["%d A" % x for x in fuses if x != best][-3:], "I = P/V = %s A, so choose the smallest fuse a little above this: <b>%d A</b>." % (nf(I), best))


MAG = [("What is a magnetic field line?", "a curve along which a free north pole would move", ["a line of electric current", "a line of equal temperature", "a wire"], "Field lines go from N to S outside a magnet."),
       ("Why do two magnetic field lines never cross?", "there would be two directions of the field at one point, which is impossible", ["they repel each other", "they are too weak", "they always cross at the poles"], "The field has one direction at each point."),
       ("Where is the magnetic field of a bar magnet strongest?", "near the poles, where field lines are closest", ["at the middle", "far away", "it is the same everywhere"], "Crowded lines mean a stronger field."),
       ("Who discovered that a current-carrying wire deflects a compass needle?", "Hans Christian Oersted", ["Michael Faraday", "Isaac Newton", "Georg Ohm"], "This showed that electricity and magnetism are linked."),
       ("What is the shape of the field lines around a straight current-carrying wire?", "concentric circles around the wire", ["straight lines parallel to the wire", "spirals", "no field forms"], "Use the right-hand thumb rule for the direction."),
       ("What does the right-hand thumb rule give?", "the direction of the magnetic field around a current-carrying wire", ["the direction of the force on a wire", "the size of the current", "the voltage"], "Thumb along the current; fingers curl in the field direction."),
       ("How does the field around a straight wire change as you move away from it?", "it becomes weaker", ["it becomes stronger", "it stays the same", "it reverses"], "Field strength falls with distance."),
       ("What happens to the field when the current in a wire is increased?", "it becomes stronger", ["it becomes weaker", "it disappears", "it reverses"], "Field strength depends on current."),
       ("What is a solenoid?", "a coil of many circular turns of insulated wire", ["a straight wire", "a bar magnet", "a battery"], "Its field is like that of a bar magnet."),
       ("What is the field like inside a long solenoid?", "uniform, with parallel straight field lines", ["zero", "circular", "random"], "It is used to make electromagnets."),
       ("What is an electromagnet?", "a soft iron core inside a solenoid that is magnetic only when current flows", ["a permanent magnet", "a battery", "a copper wire"], "Electromagnets can be switched on and off."),
       ("When is the force on a current-carrying conductor in a magnetic field the largest?", "when the current is at right angles to the field", ["when the current is parallel to the field", "when there is no current", "when the wire is copper"], "There is no force when they are parallel."),
       ("Which rule gives the direction of the force on a current-carrying conductor in a magnetic field?", "Fleming's left-hand rule", ["the right-hand thumb rule", "Ohm's law", "Snell's law"], "First finger field, second finger current, thumb motion."),
       ("What colour is the live wire in Indian domestic wiring?", "red (or brown)", ["green", "black only", "blue only"], "Neutral is black (or blue) and earth is green."),
       ("What is the potential difference between the live and neutral wires in Indian homes?", "220 V", ["110 V", "12 V", "440 V"], "The supply is alternating current at 50 Hz."),
       ("Why is the metal body of an appliance earthed?", "so that any leaked current flows to the earth and does not shock the user", ["to make it heavier", "to save electricity", "to make it work faster"], "The earth wire has low resistance."),
       ("What is a short circuit?", "the live and neutral wires touch, so a very large current flows", ["the circuit is switched off", "a fuse is added", "a wire is very long"], "It can cause fires; fuses and MCBs protect against it."),
       ("What is overloading?", "too many appliances on one socket draw too much current", ["using a fuse", "using thick wires", "switching off lights"], "It overheats wires."),
       ("What is the frequency of AC supply in India?", "50 Hz", ["60 Hz", "100 Hz", "220 Hz"], "AC changes direction 100 times a second."),
       ("Why is a separate circuit used for high-power appliances such as geysers?", "it has a higher current rating (15 A)", ["it uses less energy", "it needs no fuse", "it has no earth wire"], "Lights and fans use a 5 A circuit."),
       ("Which device is used in homes in place of a fuse in many new buildings?", "a miniature circuit breaker (MCB)", ["a voltmeter", "a solenoid", "a transformer"], "It switches off automatically on overload."),
       ("What is the direction of magnetic field lines inside a bar magnet?", "from the south pole to the north pole", ["from north to south", "there are no lines inside", "in circles"], "Field lines are closed loops."),
       ("What does a compass needle show near a magnet?", "the direction of the magnetic field at that point", ["the strength of the current", "the voltage", "the temperature"], "Its north end points along the field."),
       ("How can you make a solenoid's magnetic field stronger?", "use more turns, a larger current or a soft iron core", ["use fewer turns", "use a smaller current", "use a plastic core"], "This is how strong electromagnets are made."),
       ("What is the field like at the centre of a circular loop of current?", "the field lines are nearly straight and the field is stronger than at the edge", ["there is no field", "the field is circular only", "the field is weakest there"], "More turns give a stronger field."),
       ("Which device uses the force on a current-carrying coil in a magnetic field?", "an electric motor", ["a fuse", "a bulb", "a resistor"], "The coil rotates."),
       ("What is the main advantage of AC over DC?", "it can be sent over long distances with less loss of energy", ["it is always safer", "it never changes direction", "it needs no wires"], "Its voltage can be changed easily by transformers."),
       ("Which sources give direct current (DC)?", "cells and batteries", ["power stations' AC generators", "household sockets", "lightning"], "DC flows in one direction only."),
       ("How many times does AC at 50 Hz change direction each second?", "100 times", ["50 times", "25 times", "220 times"], "It reverses twice in each cycle."),
       ("What happens if the direction of the current in a conductor in a magnetic field is reversed?", "the force on it reverses", ["the force doubles", "the force stops", "the field disappears"], "Reversing the field also reverses the force."),
       ("What is the magnetic field outside a long solenoid like?", "like the field of a bar magnet", ["zero everywhere", "circular", "uniform and strong"], "One end acts as a north pole and the other as a south pole.")]


def UNITS10c():
    NP, EC = "Natural Phenomena", "Effects of Current"
    b = {n: once_maker(v) for n, v in [("light", LIGHT), ("sky", SKY), ("elec", ELEC), ("mag", MAG)]}
    cpos = pairs(CONCAVE_POS, "An object is placed %s in front of a concave mirror. Where is the image and what is it like?", "For a concave mirror, where must the object be for the image to be %s?")
    lpos = pairs(CONVEX_POS, "An object is placed %s in front of a convex lens. Where is the image and what is it like?", "For a convex lens, where must the object be for the image to be %s?")
    prism = pairs(PRISM, "%s", None)
    wire = pairs(WIRE, "In domestic wiring in India, %s", None)
    eye = pairs(EYE, "What is the job of %s?", "Which part of the eye does this: %s?")
    return [
        U(9, "light-reflection-and-refraction", 9, NP,
          "Reflection of light by curved surfaces; images formed by spherical mirrors, centre of curvature, principal axis, principal focus, focal length, mirror formula (derivation not required), magnification. Refraction; laws of refraction, refractive index. Refraction of light by spherical lens; image formed by spherical lenses; lens formula (derivation not required); magnification. Power of a lens.",
          "Light – Reflection and Refraction", "light: reflection and refraction",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 9: concave and convex mirrors, the mirror and lens formulas, magnification, refractive index and the power of a lens. 100 questions with answers.",
          "Mirror: 1/v + 1/u = 1/f. Lens: 1/v − 1/u = 1/f.", "Measure from the pole; with the light is +, against it is −.",
          "<p>Use the New Cartesian sign convention: distances are measured from the pole (mirror) or optical centre (lens); distances in the direction of incident light are positive, against it negative. Objects are on the left, so u is negative. A concave mirror and a concave lens have negative focal lengths; a convex mirror and a convex lens have positive ones.</p>"
          "<p>Mirror formula 1/v + 1/u = 1/f, magnification m = −v/u. Lens formula 1/v − 1/u = 1/f, magnification m = v/u. Negative m means a real, inverted image. Power of a lens P = 1/f (f in metres), in dioptres. Refractive index n = c/v.</p>",
          [("Object at 30 cm from a concave mirror, f = 20 cm. Image?", ["u = −30, f = −20", "1/v = −1/20 + 1/30 = −1/60"], "v = −60 cm (real, inverted, enlarged)"),
           ("Power of a convex lens of focal length 25 cm?", ["f = +0.25 m", "P = 1/0.25"], "+4 D")],
          ["Forgetting that u is negative.", "Using the mirror formula for a lens.", "Leaving f in centimetres when finding power."],
          [("What is the New Cartesian sign convention?", "Distances are measured from the pole or optical centre; distances in the direction of incident light and heights above the axis are positive."),
           ("What does the power of a lens tell us?", "How strongly it converges or diverges light: P = 1/f in dioptres; convex lenses have positive power.")],
          lambda: [("Images in mirrors", [(cpos, 10), (b["light"], 6), (K(c_mirror, "nature"), 4)]), ("The mirror formula", [(K(c_mirror, "v", "f", "m"), 14), (K(c_mirror, "nature"), 6)]),
                   ("Refraction and refractive index", [(c_refr, 14), (b["light"], 6)]), ("Lenses and the lens formula", [(lpos, 8), (K(c_lens, "v", "f", "m"), 12)]),
                   ("Power and mixed problems", [(K(c_lens, "P"), 8), (K(c_lens, "v", "m"), 6), (K(c_mirror, "v", "m"), 6)])]),
        U(10, "the-human-eye-and-the-colourful-world", 10, NP,
          "Functioning of a lens in the human eye, defects of vision and their corrections, applications of spherical mirrors and lenses. Refraction of light through a prism, dispersion of light, scattering of light, applications in daily life.",
          "The Human Eye and the Colourful World", "the human eye and the colourful world",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 10: parts of the eye, accommodation, myopia and hypermetropia with lens powers, dispersion, atmospheric refraction and scattering of light. 100 questions with answers.",
          "Myopia: concave lens. Hypermetropia: convex lens.", "Blue light scatters most; red least.",
          "<p>The eye lens focuses images on the retina; ciliary muscles change its focal length (accommodation). The near point of a normal eye is about 25 cm and the far point is infinity. A myopic eye cannot see far objects (corrected by a concave lens); a hypermetropic eye cannot see near objects (corrected by a convex lens).</p>"
          "<p>A prism disperses white light into seven colours (VIBGYOR) because each colour bends by a different amount. Atmospheric refraction makes stars twinkle and gives an early sunrise. Scattering by air molecules makes the sky blue and the rising and setting Sun red.</p>",
          [("Far point of a myopic eye is 2 m. Lens power?", ["f = −2 m", "P = 1/f"], "−0.5 D"),
           ("Why is the sky blue?", ["air scatters short wavelengths most"], "blue light is scattered most")],
          ["Using a convex lens for myopia.", "Saying red light scatters most.", "Thinking planets twinkle like stars."],
          [("What is accommodation?", "The ability of the eye lens to change its focal length so that both near and far objects are seen clearly."),
           ("Why does the Sun look red at sunset?", "Sunlight passes through more air, so blue light is scattered away and mostly red light reaches us.")],
          lambda: [("Parts of the eye", [(eye, 15), (b["sky"], 5)]), ("Defects of vision", [(K(c_eye, "defect"), 3), (K(c_eye, "myopia"), 9), (K(c_eye, "hyper"), 7), (eye, 1)]),
                   ("Dispersion and the prism", [(prism, 10), (b["sky"], 8), (K(c_eye, "far"), 2)]),
                   ("Scattering and atmospheric refraction", [(b["sky"], 12), (prism, 1), (K(c_eye, "far"), 3), (K(c_eye, "myopia"), 2), (K(c_eye, "hyper"), 2)]),
                   ("Mixed problems", [(K(c_eye, "fl"), 12), (K(c_lens, "P"), 4), (b["sky"], 2), (K(c_eye, "far"), 2)])]),
        U(11, "electricity", 11, EC,
          "Electric current, potential difference and electric current. Ohm's law; resistance, resistivity, factors on which the resistance of a conductor depends. Series combination of resistors, parallel combination of resistors and its applications in daily life. Heating effect of electric current and its applications in daily life. Electric power, interrelation between P, V, I and R.",
          "Electricity", "electricity",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 11: current and charge, Ohm's law, resistivity, series and parallel resistors, electric power, heating effect and the cost of electricity in kWh. 100 questions with answers.",
          "V = IR, Q = It, P = VI.", "Series: R = R₁ + R₂. Parallel: 1/R = 1/R₁ + 1/R₂.",
          "<p>Current is the rate of flow of charge (I = Q/t, in amperes). Potential difference is work done per unit charge (V = W/Q, in volts). Ohm's law: V = IR. The resistance of a wire is R = ρL/A, where ρ is the resistivity of the material.</p>"
          "<p>In series, resistances add; in parallel, 1/R = 1/R₁ + 1/R₂ + … and the total is less than the smallest. Power P = VI = I²R = V²/R; heat H = I²Rt. Electrical energy is sold in kilowatt hours (units): energy = power (kW) × time (h).</p>",
          [("12 V across 4 Ω. Current?", ["I = V/R"], "3 A"),
           ("A 1,000 W heater runs 2 h a day for 30 days at ₹6 per unit. Cost?", ["1 kW × 2 h × 30 = 60 kWh", "60 × ₹6"], "₹360")],
          ["Adding resistances in parallel.", "Using watts instead of kilowatts for kWh.", "Connecting an ammeter in parallel."],
          [("Why are appliances in a house connected in parallel?", "Each gets the full 220 V, has its own switch, and one failing does not stop the others."),
           ("What is 1 kWh?", "The energy used by a 1,000 W appliance in one hour: 3.6 × 10⁶ J.")],
          lambda: [("Charge, current and potential difference", [(K(c_elec, "charge", "electrons", "work"), 14), (b["elec"], 6)]), ("Ohm's law", [(K(c_elec, "ohm"), 20)]),
                   ("Resistors in series and parallel", [(K(c_elec, "series", "parallel"), 16), (K(c_elec, "rho"), 4)]), ("Power and heating", [(K(c_elec, "power", "heat"), 14), (b["elec"], 6)]),
                   ("Energy and cost", [(K(c_elec, "kwh"), 14), (b["elec"], 6)])]),
        U(12, "magnetic-effects-of-electric-current", 12, EC,
          "Magnetic effects of current: magnetic field, field lines, field due to a current carrying conductor, field due to current carrying coil or solenoid; force on current carrying conductor, Fleming's left hand rule, direct current, alternating current: frequency of AC, advantage of AC over DC, domestic electric circuits.",
          "Magnetic Effects of Electric Current", "magnetic effects of electric current",
          "Free CBSE Class 10 Science worksheets for NCERT Chapter 12: magnetic field lines, the right-hand thumb rule, solenoids and electromagnets, Fleming's left-hand rule, fuses and domestic electric circuits. 100 questions with answers.",
          "A current makes a magnetic field around it.", "Fleming's left hand: Field, Current, thrust (Motion).",
          "<p>A current-carrying wire has a magnetic field of concentric circles around it; the right-hand thumb rule gives its direction. A solenoid behaves like a bar magnet, and with a soft iron core it makes an electromagnet.</p>"
          "<p>A current-carrying conductor in a magnetic field feels a force, largest when the current is at right angles to the field. Fleming's left-hand rule: forefinger along the field, middle finger along the current, thumb gives the force. Homes in India get 220 V AC at 50 Hz with live, neutral and earth wires, protected by fuses or MCBs.</p>",
          [("Current east, field north. Force?", ["forefinger north, middle finger east"], "upwards"),
           ("A 2,000 W, 220 V geyser. Fuse?", ["I = 2,000/220 ≈ 9.1 A"], "10 A")],
          ["Using the right hand for the force on a conductor.", "Choosing a fuse far bigger than the current needed.", "Mixing up the colours of live, neutral and earth wires."],
          [("Why does a fuse protect a circuit?", "Its thin wire melts when the current is too large, breaking the circuit before wires overheat."),
           ("What is the difference between AC and DC?", "DC flows in one direction; AC reverses direction periodically (50 times a second in India, so 50 Hz).")],
          lambda: [("Magnetic field lines", [(b["mag"], 20)]), ("Fleming's left-hand rule", [(c_flem, 20)]), ("Fuses and current", [(c_fuse, 10), (K(c_elec, "power"), 10)]),
                   ("Domestic circuits", [(wire, 9), (c_fuse, 6), (b["mag"], 5)]), ("Mixed problems", [(c_flem, 6), (K(c_elec, "heat"), 8), (K(c_elec, "kwh"), 6)])]),
    ]
