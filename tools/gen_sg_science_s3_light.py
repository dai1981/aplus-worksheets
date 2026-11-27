# -*- coding: utf-8 -*-
"""
Singapore Secondary 3 O-Level Physics (6091), Topic 12: Light
  python tools/gen_sg_science_s3_light.py
Reflection (angle of incidence = angle of reflection) and the image in a plane mirror; refraction, refractive index
n = sin i ÷ sin r = c ÷ v; critical angle (sin c = 1 ÷ n) and total internal reflection, optical fibres; thin converging lenses:
focal point and focal length, the nature of the image for different object distances, and uses (magnifying glass, camera,
projector).
UK reflection makers are reused (Singapore names); the rest are written here.
Wrong answers come from real mistakes: "angles are measured from the mirror surface", "light bends away from the normal entering
glass", "n = sin r ÷ sin i", "total internal reflection happens going from air into glass", "a converging lens always makes a
real image".
"""
import math
from sg_ol import OL, seed_of, make_ol, item, nq, tq, nf, trim, rows, pool, upto, keep, ex

LV, SUBJ, SORT = 3, "Physics", 12
U, R, P, src = OL(seed_of(LV, SUBJ, SORT))
N = ex
uk_refl = src("gen_uk_science_y7_light", "g_refl")

deg = math.radians


def g_refl():
    i = R.choice([15, 20, 25, 30, 35, 40, 50, 55, 60, 65, 70])
    k = R.choice(["r", "glancing", "between"])
    if k == "r":
        return nq("A ray strikes a plane mirror. The angle between the ray and the normal is %d°. What is the angle of reflection?" % i, i, [90 - i, 2 * i, 180 - i], "°",
                  "Angle of reflection = angle of incidence = %d° (both measured from the normal)." % i)
    if k == "glancing":
        return nq("A ray strikes a plane mirror at %d° to the mirror surface. What is the angle of reflection?" % (90 - i), i, [90 - i, 2 * (90 - i), 180 - i], "°",
                  "Angle of incidence = 90° − %d° = %d° (from the normal), so the angle of reflection is %d°." % (90 - i, i, i))
    return nq("The angle of incidence on a plane mirror is %d°. What is the angle between the incident ray and the reflected ray?" % i, 2 * i, [i, 90 - i, 180 - 2 * i], "°",
              "The angle between them is i + r = %d° + %d° = %d°." % (i, i, 2 * i))


def g_mirror():
    d = R.choice([0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0])
    k = R.choice(["dist", "sep", "move"])
    who, pr, _ = P.next()
    if k == "dist":
        return nq("%s stands %s m in front of a plane mirror. How far is the image behind the mirror?" % (who, N(d)), d, [2 * d, d / 2, d + 1], " m", "The image is as far behind the mirror as the object is in front.")
    if k == "sep":
        return nq("%s stands %s m in front of a plane mirror. How far is %s from the image?" % (who, N(d), pr), 2 * d, [d, d / 2, 4 * d], " m",
                  "Image distance = %s m behind, so separation = %s + %s = %s m." % (N(d), N(d), N(d), N(2 * d)))
    m = R.choice([0.5, 1.0])
    return nq("%s stands %s m from a plane mirror and walks %s m towards it. How far is %s now from %s image?" % (who, N(d + m), N(m), pr, "her" if pr == "she" else "his"),
              2 * d, [2 * (d + m), d, 2 * (d + m) - m], " m", "New distance from mirror = %s m; image distance = %s m; separation = %s m." % (N(d), N(d), N(2 * d)))


MED = [("glass", 1.5), ("water", 1.33), ("perspex", 1.5), ("diamond", 2.42), ("crown glass", 1.52)]


def g_snell():
    k = R.choice(["n", "r", "i", "v", "vn"])
    m_, n = R.choice(MED)
    i = R.choice([20, 25, 30, 35, 40, 45, 50, 55, 60, 70])
    r = math.degrees(math.asin(math.sin(deg(i)) / n))
    if k == "n":
        rr = round(r)
        nn = math.sin(deg(i)) / math.sin(deg(rr))
        return nq("A ray of light enters a block from air with an angle of incidence of %d° and an angle of refraction of %d°. What is the refractive index?" % (i, rr), nn,
                  [math.sin(deg(rr)) / math.sin(deg(i)), i / rr, math.sin(deg(i - rr))], "", "n = sin i ÷ sin r = sin %d° ÷ sin %d° = %s." % (i, rr, nf(nn)))
    if k == "r":
        return nq("Light passes from air into %s (refractive index %s) at an angle of incidence of %d°. What is the angle of refraction?" % (m_, N(n), i), r,
                  [i / n, math.degrees(math.asin(min(1, math.sin(deg(i)) * n / 2.5))) + 5, i - r], "°", "sin r = sin %d° ÷ %s, so r = %s°." % (i, N(n), nf(r)), sf=3)
    if k == "i":
        rr = R.choice([15, 20, 25, 30, 35])
        ii = math.degrees(math.asin(min(1, math.sin(deg(rr)) * n)))
        if math.sin(deg(rr)) * n >= 1:
            return None
        return nq("A ray enters %s (refractive index %s) from air and is refracted at %d° to the normal. What was the angle of incidence?" % (m_, N(n), rr), ii,
                  [rr * n, rr / n, 90 - ii], "°", "sin i = n × sin r = %s × sin %d°, so i = %s°." % (N(n), rr, nf(ii)))
    if k == "v":
        return nq("The refractive index of %s is %s. What is the speed of light in %s? (speed of light in air = 3.0 × 10⁸ m/s)" % (m_, N(n), m_), 3e8 / n, [3e8 * n, 3e8, 3e8 / n / 2], " m/s",
                  "v = c ÷ n = 3.0 × 10⁸ ÷ %s = %s m/s." % (N(n), nf(3e8 / n)))
    v = R.choice([2.0e8, 2.25e8, 1.24e8, 1.97e8])
    return nq("Light travels at %s m/s in a material. What is its refractive index? (c = 3.0 × 10⁸ m/s)" % nf(v), 3e8 / v, [v / 3e8, 3e8 - v, 3e8 / v / 2], "",
              "n = c ÷ v = 3.0 × 10⁸ ÷ %s = %s." % (nf(v), nf(3e8 / v)))


def g_crit():
    m_, n = R.choice(MED + [("an optical fibre core", 1.6), ("a plastic", 1.4)])
    c = math.degrees(math.asin(1 / n))
    k = R.choice(["c", "n", "tir"])
    if k == "c":
        return nq("The refractive index of %s is %s. What is its critical angle?" % (m_, N(n)), c, [90 - c, math.degrees(math.asin(1 / n / 2)), n * 30], "°",
                  "sin c = 1 ÷ n = 1 ÷ %s, so c = %s°." % (N(n), nf(c)))
    if k == "n":
        cc = R.choice([35, 40, 42, 45, 48, 50])
        nn = 1 / math.sin(deg(cc))
        return nq("A transparent material has a critical angle of %d°. What is its refractive index?" % cc, nn, [math.sin(deg(cc)), 1 / math.cos(deg(cc)), cc / 30], "",
                  "n = 1 ÷ sin c = 1 ÷ sin %d° = %s." % (cc, nf(nn)))
    a = R.choice([30, 35, 40, 45, 50, 55, 60, 65])
    tir = a > c
    return tq("Light travels inside %s (critical angle %s°) and hits the surface with air at %d° to the normal. What happens?" % (m_, nf(c), a),
              "It is totally internally reflected." if tir else "Most of it is refracted out into the air, bending away from the normal.",
              ["It is totally internally reflected." if not tir else "Most of it is refracted out into the air, bending away from the normal.",
               "It passes straight through without bending.", "It is absorbed completely."],
              "Total internal reflection happens only when light goes from a denser medium to a less dense one and the angle of incidence is greater than the critical angle.")


LENS = [("beyond 2F", "real, inverted and diminished, between F and 2F on the other side", "a camera"),
        ("at 2F", "real, inverted and the same size, at 2F on the other side", "a photocopier making a same-size copy"),
        ("between F and 2F", "real, inverted and magnified, beyond 2F on the other side", "a projector"),
        ("at F", "no clear image: the rays come out parallel (image at infinity)", "a spotlight making a parallel beam"),
        ("between F and the lens", "virtual, upright and magnified, on the same side as the object", "a magnifying glass")]


def g_lens():
    pos, img, use = R.choice(LENS)
    k = R.choice(["img", "use", "pos"])
    if k == "img":
        return tq("An object is placed %s in front of a thin converging lens. What image is formed?" % pos, img, [x[1] for x in LENS if x[1] != img][:3],
                  "Object %s: image %s. Used in %s." % (pos, img, use))
    if k == "use":
        return tq("Which device uses a converging lens with the object %s?" % pos, use, [x[2] for x in LENS if x[2] != use][:3], "Object %s: image %s." % (pos, img))
    return tq("Where must the object be placed for a converging lens to give an image that is %s?" % img, pos, [x[0] for x in LENS if x[0] != pos][:3], "Object %s: image %s." % (pos, img))


def g_fl():
    f = R.choice([5, 8, 10, 12, 15, 20, 25])
    u = R.choice([1.5, 2, 3, 4, 0.5, 0.8]) * f
    pos = "beyond 2F" if u > 2 * f else "at 2F" if u == 2 * f else "between F and 2F" if u > f else "at F" if u == f else "between F and the lens"
    img = next(x[1] for x in LENS if x[0] == pos)
    return tq("A converging lens has a focal length of %d cm. An object is %s cm from it. What kind of image is formed?" % (f, N(u)), img, [x[1] for x in LENS if x[1] != img][:3],
              "2F is at %d cm, so the object is %s." % (2 * f, pos))


POOL1 = pool(R, [
    ("State the laws of reflection.", "The angle of incidence equals the angle of reflection, and the incident ray, reflected ray and normal lie in the same plane.",
     ["The angle of incidence is twice the angle of reflection.", "Light always reflects at 90°.", "Only the angles of rough surfaces are equal."], "Angles are measured from the normal."),
    ("Describe the image in a plane mirror.", "virtual, upright, the same size and laterally inverted, as far behind the mirror as the object is in front",
     ["real and inverted", "virtual and magnified", "real, upright and smaller"], "It cannot be formed on a screen."),
    ("What is refraction?", "the bending of light as it passes from one medium to another because its speed changes", ["the bouncing of light off a surface", "the splitting of light into colours only", "the absorption of light"], "Light slows down in glass."),
    ("When light enters glass from air at an angle, which way does it bend?", "towards the normal", ["away from the normal", "it does not bend", "along the surface"], "It slows down."),
    ("When light leaves glass into air at an angle, which way does it bend?", "away from the normal", ["towards the normal", "it does not bend", "back into the glass always"], "It speeds up."),
    ("A ray enters a glass block along the normal (angle of incidence 0°). What happens?", "It passes straight through without bending, though it slows down.", ["It bends towards the normal.", "It is totally internally reflected.", "It stops."], "No change in direction."),
    ("What is the critical angle?", "the angle of incidence in the denser medium for which the angle of refraction is 90°", ["the angle at which light reflects from a mirror", "the angle of refraction in glass", "the largest possible angle of incidence"], "sin c = 1 ÷ n."),
    ("What two conditions are needed for total internal reflection?", "Light must travel from a denser to a less dense medium, and the angle of incidence must be greater than the critical angle.",
     ["Light must go from air into glass at any angle.", "The angle of incidence must be zero.", "The surface must be a mirror."], "Used in optical fibres."),
    ("What is the principal focus (F) of a converging lens?", "the point where rays parallel to the principal axis meet after passing through the lens", ["the centre of the lens", "the point where the image is always formed", "twice the focal length"], "Its distance from the lens is the focal length."),
    ("What is the focal length of a lens?", "the distance between the optical centre of the lens and the principal focus", ["the thickness of the lens", "the distance from the object to the image", "the diameter of the lens"], "A thicker converging lens has a shorter focal length."),
])
POOL5 = pool(R, [
    ("Why does a swimming pool look shallower than it really is?", "Light from the bottom bends away from the normal as it leaves the water, so the bottom appears higher.",
     ["Light bends towards the normal leaving water.", "Water magnifies objects.", "Light reflects off the surface."], "This is apparent depth."),
    ("How does an optical fibre carry light around corners?", "by repeated total internal reflection inside the core", ["by refraction out of the fibre", "by absorbing and re-emitting light", "by reflecting from a metal coating"], "The core is denser than the cladding."),
    ("Why are optical fibres used for internet cables in Singapore?", "They carry large amounts of data as light pulses with little loss and no electrical interference.", ["They are made of copper.", "They carry sound waves.", "They need no light."], "Also used in endoscopes."),
    ("Why do prisms in binoculars use total internal reflection instead of mirrors?", "Total internal reflection reflects almost all the light, so the image is brighter.", ["Mirrors are too heavy only.", "Prisms refract light into colours.", "Mirrors produce real images."], "No silvering to wear away."),
    ("A magnifying glass shows a larger, upright image of an insect. Where is the insect?", "between the lens and its principal focus", ["beyond 2F", "at 2F", "exactly at F"], "The image is virtual."),
    ("Which type of image can be caught on a screen?", "a real image", ["a virtual image", "any image", "only the image in a plane mirror"], "Real rays meet at a real image."),
    ("The refractive index of glass is 1.5. What does this tell you?", "Light travels 1.5 times faster in air than in glass.", ["Light travels 1.5 times faster in glass.", "Glass bends light by 1.5°.", "Glass reflects 1.5 times more light."], "n = c ÷ v."),
    ("Why does a diamond sparkle?", "It has a large refractive index and small critical angle (about 24°), so light is totally internally reflected many times.", ["It produces light.", "It absorbs all light.", "It has a very large critical angle."], "Light escapes only from certain faces."),
    ("A ray hits the inside of a glass block (critical angle 42°) at 30° to the normal. What happens?", "Most of the light is refracted out into the air.", ["It is totally internally reflected.", "It stops.", "It is refracted towards the normal."], "30° is less than 42°."),
    ("Why do the letters AMBULANCE appear reversed on the front of an ambulance?", "Drivers see them the right way round in their rear-view mirror because a plane mirror gives lateral inversion.",
     ["To make it look modern.", "Because light reverses in glass.", "So that pedestrians can read it easily."], "Left and right are swapped in a mirror image."),
])


def main():
    sets = U.sets([
        ("Reflection and plane mirrors", [(g_refl, 7), (g_mirror, 5), (uk_refl, 3), POOL1]),
        ("Refraction and refractive index", [(g_snell, 12), POOL1, (POOL5, 2)]),
        ("Critical angle and total internal reflection", [(g_crit, 11), POOL1, (POOL5, 4)]),
        ("Converging lenses", [(g_lens, 9), (g_fl, 7), POOL1]),
        ("Exam-style questions", [(POOL5, 8), (g_snell, 4), (g_crit, 3), (g_fl, 3), (g_mirror, 2)]),
    ])
    make_ol(LV, SUBJ, "light", SORT, "Light",
            "Recall and use the laws of reflection and describe the image in a plane mirror; describe refraction and recall and apply refractive index n = sin i ÷ sin r "
            "and n = speed of light in a vacuum ÷ speed of light in the medium; define critical angle, recall and apply sin c = 1 ÷ n and describe total internal reflection "
            "and its use in optical fibres; describe the action of a thin converging lens, define focal length and principal focus, draw ray diagrams and state the nature "
            "of the image formed for different object distances, including uses such as a magnifying glass, camera and projector (summary of the Singapore-Cambridge "
            "O-Level Physics 6091 syllabus).",
            "Light", "Light",
            "Free Secondary 3 O-Level Physics worksheets on light: reflection, plane mirrors, refraction, refractive index, critical angle, total internal reflection, optical "
            "fibres and converging lenses. 100 questions with answers.",
            "n = sin i ÷ sin r = c ÷ v", "sin c = 1 ÷ n; angles are measured from the normal.",
            "<p><b>Light reflects with equal angles and refracts when its speed changes.</b></p><ul>"
            "<li>Reflection: i = r, measured from the normal. A plane mirror gives a virtual, upright, same-size, laterally inverted image.</li>"
            "<li>Refraction: n = sin i ÷ sin r = c ÷ v. Light bends towards the normal entering a denser medium.</li>"
            "<li>Total internal reflection: from denser to less dense medium, with i greater than the critical angle c, where sin c = 1 ÷ n.</li>"
            "<li>Converging lens: object beyond 2F gives a real, diminished image (camera); between F and 2F gives a real, magnified image (projector); inside F gives a virtual, magnified image (magnifying glass).</li></ul>",
            [("i = 40°, r = 25°. n?", ["n = sin 40° ÷ sin 25° = 0.643 ÷ 0.423"], "1.52"),
             ("n = 1.5. Critical angle?", ["sin c = 1 ÷ 1.5 = 0.667"], "41.8°")],
            ["Measuring angles from the surface instead of the normal.", "Writing n = sin r ÷ sin i (the answer becomes less than 1).",
             "Saying total internal reflection happens when light goes from air into glass.", "Thinking a converging lens always forms a real image."],
            [("How do you calculate refractive index?", "Use n = sin i ÷ sin r for light entering the medium from air, or n = c ÷ v using the speeds of light."),
             ("When does total internal reflection happen?", "When light travels from a denser medium towards a less dense one and the angle of incidence is larger than the critical angle."),
             ("What image does a magnifying glass form?", "When the object is closer than the principal focus, a converging lens forms a virtual, upright, magnified image on the same side as the object.")],
            sets)


if __name__ == "__main__":
    main()
