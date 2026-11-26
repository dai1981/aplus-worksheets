# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Light and Sound Waves (MS-PS4-2)
  python tools/gen_us_science_g8_light_and_sound_waves.py
Develop and use a model to describe that waves are reflected, absorbed, or transmitted through various materials.
Light: reflection (angle in = angle out), refraction when changing medium, transparent / translucent / opaque,
color from reflected light. Sound: a mechanical wave that needs a medium, faster in solids than in air,
echoes (reflection) and soundproofing (absorption). Light travels through a vacuum; sound does not.
Wrong answers come from real mistakes: "sound travels through space", "a red apple absorbs red light",
"sound is fastest in air", "light bends because it slows down only in air".
"""
from sci_common import Unit, item, bank, lesson, make, fig, svg_wrap, line, text, arrow, table, People, INK, BLUE, RED, GRAY

U = Unit(80109)
R = U.R
P = People(R)
USED = {}


def nm(x):
    return "{:,}".format(int(x)) if x == int(x) else "{:,.1f}".format(x)


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def mirror(ang):
    import math
    W, H = 360, 200
    cx, cy = 180, 170
    L = 140
    a = math.radians(ang)
    rr = 62 if ang >= 40 else 105
    x1, y1 = cx - L * math.sin(a), cy - L * math.cos(a)
    x2, y2 = cx + L * math.sin(a), cy - L * math.cos(a)
    s = [line(40, cy, 320, cy, INK, 4), line(cx, cy, cx, 20, GRAY, 1.5).replace("/>", " stroke-dasharray='5 4'/>"),
         arrow(x1, y1, cx - 3, cy - 3, RED, 3, 10), arrow(cx + 2, cy - 2, x2, y2, RED, 3, 10),
         text(cx - rr * math.sin(a / 2), cy - rr * math.cos(a / 2) + 5, "%d°" % ang, 14, col=RED), text(cx + rr * math.sin(a / 2), cy - rr * math.cos(a / 2) + 5, "?", 16, col=RED), text(cx, 16, "normal", 12, col=GRAY, weight=400),
         text(70, cy + 22, "mirror", 13, weight=400)]
    return svg_wrap(W, H, "".join(s), "a light ray hitting a mirror at %d degrees from the normal" % ang)


def g_reflect():
    ang = R.choice([20, 25, 30, 35, 40, 45, 50, 55, 60])
    who = P.next()[0]
    if not once(("m", ang)):
        return None
    return item(fig(mirror(ang)) + "In %s's ray model, light hits a flat mirror at %d° from the normal. What is the angle of reflection?" % (who, ang), "%d°" % ang,
                ["%d°" % (90 - ang) if 90 - ang != ang else "%d°" % (ang + 10), "%d°" % (180 - ang), "%d°" % (ang * 2)], "Angle of incidence = angle of reflection.")


MAT = {"transparent": ["clear window glass", "clean water in a glass", "a clear plastic bottle", "air", "a clear eyeglass lens"],
       "translucent": ["wax paper", "frosted glass", "a thin paper lampshade", "tissue paper", "a frosted shower door"],
       "opaque": ["a brick wall", "a wooden door", "aluminum foil", "a book", "a metal pan"]}


def g_mat():
    k = R.choice(sorted(MAT))
    m = R.choice(MAT[k])
    who = P.next()[0]
    t = R.random() < 0.5
    if not once(("mat", m, t)) or not once(("matx", m), 1 + (k != "transparent")):
        return None
    desc = {"transparent": "It transmits almost all light, so you can see clearly through it.", "translucent": "It transmits some light but scatters it, so things look blurry.",
            "opaque": "It transmits no light; light is reflected or absorbed."}
    if t:
        return item("%s shines a flashlight at %s. How is it best described?" % (who, m), k, [x for x in MAT if x != k] + ["magnetic"], desc[k])
    return item("%s shines a flashlight at %s. What happens to the light?" % (who, m), desc[k], [desc[x] for x in MAT if x != k] + ["The light is turned into sound."], "%s is %s." % (m[0].upper() + m[1:], k))


COL = [("red", "a red apple"), ("green", "a green leaf"), ("blue", "a blue shirt"), ("yellow", "a yellow banana"), ("white", "a white sheet of paper"), ("black", "a black backpack"), ("orange", "an orange carrot"), ("purple", "a purple grape")]


def g_color():
    c, obj = R.choice(COL)
    who = P.next()[0]
    if not once(("c", c)):
        return None
    if c == "white":
        a = "It reflects all colors of light."
    elif c == "black":
        a = "It absorbs all colors of light."
    else:
        a = "It reflects %s light and absorbs the other colors." % c
    w = ["It absorbs %s light and reflects the other colors." % (c if c not in ("white", "black") else "red"), "It makes its own %s light." % ("colored" if c in ("white", "black") else c),
         "It reflects all colors of light." if c != "white" else "It absorbs all colors of light."]
    return item("Why does %s look %s to %s in white sunlight?" % (obj, c, who), a, w, "We see the colors an object reflects.")


SPEED = [("air", 343), ("water", 1480), ("steel", 5960), ("wood", 3800)]


def g_sound():
    who = P.next()[0]
    k = R.choice(["fast", "slow", "echo", "time"])
    if k in ("fast", "slow"):
        if not once(k, 3):
            return None
        rows = [[m, "{:,} m/s".format(v)] for m, v in R.sample(SPEED, 4)]
        tab = table(["Material", "Speed of sound"], rows)
        a = "steel" if k == "fast" else "air"
        return item(tab + "In %s's data, through which material does sound travel %s?" % (who, "fastest" if k == "fast" else "slowest"), a, [m for m, _ in SPEED if m != a],
                    "Sound is fastest in solids, where particles are close together, and slowest in gases.")
    if k == "echo":
        t = R.choice([1, 2, 3, 4, 5, 6])
        if not once(("e", t)):
            return None
        d = 343 * t / 2
        return item("%s shouts toward a cliff and hears the echo %d s later. Sound travels at about 343 m/s in air. How far away is the cliff?" % (who, t), nm(d) + " m",
                    [nm(343 * t) + " m", nm(343 / t) + " m", nm(d / 2) + " m"], "The sound goes there and back: 343 × %d ÷ 2 = %s m." % (t, nm(d)))
    t = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
    if not once(("t", t)):
        return None
    d = 343 * t
    return item("%s sees lightning and hears thunder %d s later. About how far away was the lightning? (sound in air ≈ 343 m/s)" % (who, t), "about {:,} m".format(d),
                ["about {:,} m".format(d // 2 if t % 2 == 0 else d * 2), "about %d m" % (343 + t), "0 m, because light and sound arrive together"], "Light arrives almost instantly; sound takes %d s: 343 × %d." % (t, t))


WHAT = [("A sound wave hits a thick foam panel in a recording studio.", "absorbed"), ("Light passes through a clear window.", "transmitted"),
        ("Your voice bounces off a canyon wall.", "reflected"), ("Sunlight hits a black parking lot and warms it.", "absorbed"),
        ("Light bounces off a calm lake.", "reflected"), ("Sound travels through a wall to the next room.", "transmitted"),
        ("A heavy curtain makes a room quieter.", "absorbed"), ("A bat's call bounces off a moth.", "reflected"),
        ("Light shines through a glass of water.", "transmitted"), ("Ultrasound waves bounce off a baby inside the mother.", "reflected"),
        ("Sunlight warms a dark rock on the beach.", "absorbed"), ("You hear music from a car through its closed windows.", "transmitted"),
        ("A submarine's sonar ping bounces off the seafloor.", "reflected"), ("Egg-carton foam on a wall quiets a drum room.", "absorbed"),
        ("Light passes through a clear plastic water bottle.", "transmitted"), ("A bike reflector shines back at a car's headlights.", "reflected")]


REFR = [("A pencil in a glass of water looks broken at the water's surface.", "Light bends as it passes from water into air."),
        ("A glass prism spreads white light into a band of colors.", "Each color bends by a different amount in the glass."),
        ("A swimming pool looks shallower than it really is.", "Light from the bottom bends as it leaves the water."),
        ("A magnifying glass makes letters look bigger.", "The curved lens bends light rays toward each other."),
        ("Raindrops make a rainbow when the Sun is behind you.", "Sunlight bends and splits into colors inside the drops."),
        ("Eyeglasses help a person see clearly.", "The lenses bend light so it focuses on the back of the eye."),
        ("A fish in a pond is not exactly where it appears to be.", "Light bends at the water's surface, so the fish's image shifts."),
        ("A hot road looks wet in the distance on a summer day.", "Light bends as it passes through hot and cooler layers of air.")]


def g_refr():
    s, a = R.choice(REFR)
    who = P.next()[0]
    if not once(("rf", s)):
        return None
    w = ["Light is absorbed and disappears.", "Light reflects off a mirror at the same angle.", "Sound waves bend the light."]
    return item("%s notices: “%s” What explains this?" % (who, s), a, w, "This is refraction: light changes speed and direction when it enters a new material.")


def g_what():
    s, a = R.choice(WHAT)
    who = P.next()[0]
    if not once(("w", s)):
        return None
    return item("%s's model: “%s” Is the wave mainly reflected, absorbed or transmitted?" % (who, s), a, [x for x in ["reflected", "absorbed", "transmitted"] if x != a] + ["created"],
                "Waves can be reflected (bounce), absorbed (taken in, often as heat) or transmitted (pass through).")


B1 = bank([
    ("What three things can happen when a wave hits a material?", "It can be reflected, absorbed or transmitted.", ["It always disappears.", "It always speeds up.", "It turns into matter."], "Often a mix of all three."),
    ("Can sound travel through outer space?", "No. Sound needs a medium (matter) to travel through.", ["Yes, faster than on Earth.", "Yes, but only at night.", "Only near planets."], "Space is nearly empty."),
    ("Can light travel through outer space?", "Yes. Light does not need a medium.", ["No, it needs air.", "Only from the Moon.", "Only at night."], "Sunlight crosses empty space."),
    ("What is refraction?", "the bending of a wave as it passes from one material into another", ["a wave bouncing off a mirror", "a wave being absorbed", "a wave getting louder"], "It changes speed in the new material."),
    ("Why does a straw look bent in a glass of water?", "Light refracts as it passes from water into air.", ["The straw really bends.", "Water absorbs the straw.", "Air reflects all light."], "Light changes speed and direction."),
    ("Why does a black shirt get hotter in the sun than a white shirt?", "Black absorbs more light, which becomes thermal energy.", ["Black reflects more light.", "White absorbs more light.", "Color does not matter."], "Absorption warms."),
    ("Which is a mechanical wave?", "sound", ["light", "radio waves", "X-rays"], "Mechanical waves need a medium."),
    ("Why do rooms with carpets and curtains have fewer echoes?", "Soft materials absorb sound instead of reflecting it.", ["They make sound faster.", "They reflect all sound.", "They block light."], "Absorption reduces echoes."),
])
B4 = bank([
    ("Which material lets sound travel the fastest?", "a steel rail", ["air", "a vacuum", "helium gas"], "Solids carry sound fastest."),
    ("Why do astronauts on a spacewalk use radios to talk?", "Radio waves are light-like waves that can cross empty space; sound cannot.", ["Their voices are too quiet.", "Air in space is too thick.", "Radios make sound faster."],
     "Electromagnetic waves need no medium."),
    ("What is an echo?", "a sound wave reflected back to the listener", ["a sound absorbed by a wall", "light bouncing off a mirror", "a very loud sound"], "Echoes are reflections."),
    ("What happens to light when it enters glass from air?", "It slows down and can change direction.", ["It speeds up to infinity.", "It stops completely.", "It turns into sound."], "That is refraction."),
    ("Why is snow so bright on a sunny day?", "Snow reflects most of the light that hits it.", ["Snow makes its own light.", "Snow absorbs all light.", "Snow is transparent."], "White surfaces reflect."),
    ("Why do solar panels and solar cookers often look dark?", "Dark surfaces absorb more light energy.", ["Dark surfaces reflect more light.", "Dark colors are cheaper.", "Light cannot reach them."], "Absorption collects energy."),
    ("Which wave can travel through a vacuum?", "light", ["sound", "water waves", "a wave on a rope"], "Light needs no medium."),
    ("Why does a sound get fainter when you close a thick door?", "The door absorbs and reflects much of the sound, so less is transmitted.", ["The door makes the sound faster.", "Sound cannot travel through anything.", "The door makes light."],
     "Less sound passes through."),
    ("Light hits a mirror at 0° from the normal (straight on). Where does it go?", "straight back the way it came", ["along the mirror", "through the mirror", "it disappears"], "0° in, 0° out."),
    ("What is the normal line in a ray diagram?", "a line drawn perpendicular to the surface where the ray hits", ["the mirror itself", "the path of the light", "a line parallel to the mirror"], "Angles are measured from the normal."),
])
B5 = bank([
    ("Ava puts a ringing phone in a jar and pumps the air out. The sound gets fainter. What does this show?", "Sound needs a medium to travel.", ["Light needs air.", "Phones stop working in jars.", "Glass absorbs light."],
     "Less air, less sound."),
    ("Leo presses his ear to a desk and hears a tap louder than through the air. Why?", "Sound travels well through solids.", ["Desks make sound.", "Air blocks all sound.", "His ear is closer to light."], "Solids transmit sound well."),
    ("Mia shines a laser through water with a little milk in it. She sees the beam. Why?", "The milk particles scatter some of the light toward her eyes.", ["Milk makes light.", "Water absorbs all light.", "Lasers need milk."], "Scattering makes the beam visible."),
    ("A model shows a ray hitting a mirror at 30° and leaving at 30°. What law does this show?", "the law of reflection", ["the law of gravity", "Newton's first law", "conservation of mass"], "Angles are equal."),
    ("Why are concert halls designed with special wall shapes?", "to control how sound is reflected and absorbed", ["to make light brighter", "to stop all sound", "to make walls heavier"], "Engineers design for sound."),
])


def body():
    think = ("<p>When a wave reaches a new material, it can be <b>reflected</b> (bounce back), <b>absorbed</b> (taken in, often becoming heat) or <b>transmitted</b> (pass through). Often all three happen.</p>"
             "<ul><li><b>Light</b> travels even through empty space. A mirror reflects it at the same angle it hits (angle in = angle out). Light <b>refracts</b> (bends) when it moves into a new material. "
             "Materials are <b>transparent</b>, <b>translucent</b> or <b>opaque</b>. We see the colors an object <b>reflects</b>.</li>"
             "<li><b>Sound</b> needs a medium. It travels fastest in solids and slowest in gases. Echoes are reflected sound; soft materials absorb sound.</li></ul>")
    ex = [("A ray hits a mirror at 40° from the normal. Reflection angle?", ["Angle in = angle out."], "40°"),
          ("Why does a green leaf look green?", ["We see reflected colors."], "It reflects green light and absorbs the others.")]
    mist = ["Thinking sound can travel through empty space.",
            "Thinking a red object absorbs red light. It reflects red.",
            "Thinking sound is fastest in air. It is fastest in solids."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Reflect, absorb, transmit", B1 + [(g_what, 6), (g_mat, 6)]),
        ("Light and materials", [(g_mat, 8), (g_color, 8), (g_what, 4)]),
        ("Reflection and refraction", [(g_reflect, 8), (g_refr, 8), (g_what, 4)]),
        ("Sound waves", B4[:5] + [(g_sound, 15)]),
        ("Modeling waves", B5 + B4[5:] + [g_sound, g_reflect, g_what, g_mat]),
    ])
    make("grade-8", "light-and-sound-waves", 9, "MS-PS4-2",
         "Develop and use a model to describe that waves are reflected, absorbed, or transmitted through various materials.",
         "Light and Sound Waves",
         "Grade 8 Light and Sound Waves Worksheets: Reflection, Absorption, Transmission and Refraction",
         "Light and Sound Waves",
         "Free middle school science worksheets on light and sound waves (NGSS MS-PS4-2): reflection, absorption and transmission, transparent and opaque materials, color, refraction, echoes and the speed of sound. 100 practice questions with answers.",
         "Waves are reflected, absorbed or transmitted.",
         "Light can cross empty space and bends between materials. Sound needs matter and is fastest in solids.",
         body(),
         [("What happens when light hits an object?", "The light can be reflected, absorbed or transmitted. The colors that are reflected are the colors we see."),
          ("Why can't sound travel in space?", "Sound is a vibration of matter. Space has almost no matter, so there is nothing to carry the vibration."),
          ("What is the law of reflection?", "The angle at which light hits a flat surface equals the angle at which it bounces off, both measured from the normal line.")],
         sets)


if __name__ == "__main__":
    main()
