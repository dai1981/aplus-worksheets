# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Light and Materials (1-PS4-3)
  python tools/gen_us_science_g1_light_and_materials.py
Plan and conduct investigations to determine the effect of placing objects made with different materials in the path
of a beam of light. Clear (transparent) materials let all the light through, some (translucent) let a little through,
others (opaque) block it and make a dark shadow, and shiny (reflective) materials bounce it.
Very short sentences, many pictures.
Wrong answers come from real mistakes: "clear glass makes a dark shadow", "a mirror lets light through", "wax paper blocks all light".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(10103)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# material, kind: all / some / none / bounce
MAT = [("clear glass", "all"), ("clear plastic wrap", "all"), ("a glass of clean water", "all"), ("a clear plastic cup", "all"), ("a clear jar", "all"),
       ("wax paper", "some"), ("tissue paper", "some"), ("a white sheet", "some"), ("frosted glass", "some"), ("a thin paper plate", "some"), ("a cloudy plastic bag", "some"),
       ("cardboard", "none"), ("a wooden block", "none"), ("a book", "none"), ("a metal pan", "none"), ("a hand", "none"), ("a rock", "none"), ("a thick towel", "none"),
       ("a mirror", "bounce"), ("aluminum foil", "bounce"), ("a shiny spoon", "bounce")]
WORD = {"all": "lets all the light through", "some": "lets some light through", "none": "blocks the light", "bounce": "bounces the light back"}
NAME = {"all": "transparent (clear)", "some": "translucent", "none": "opaque", "bounce": "reflective (shiny)"}
WALL = {"all": "bright", "some": "dim", "none": "dark shadow", "bounce": "dark, because the light bounced back"}


def beam_svg(kind, label=True):
    s = K.icon("flashlight", 40, 70, 0.7) + "<path d='M62 66 L170 46 L170 94 L62 74 Z' fill='#ffe98a' opacity='0.7'/>"
    col = {"all": ("#dff1fb", 0.45), "some": ("#f4f1e8", 0.85), "none": ("#8a5a2b", 1), "bounce": ("#cfd6de", 1)}[kind]
    s += "<rect x='170' y='36' width='16' height='68' fill='%s' opacity='%s' stroke='%s' stroke-width='1.5'/>" % (col[0], col[1], INK)
    if kind == "bounce":
        s += "<path d='M170 50 L80 20 L80 34 L170 90 Z' fill='#ffe98a' opacity='0.5'/>"
    else:
        op = {"all": 0.7, "some": 0.3, "none": 0}[kind]
        if op:
            s += "<path d='M186 46 L290 30 L290 110 L186 94 Z' fill='#ffe98a' opacity='%s'/>" % op
    wall = {"all": "#fff3a6", "some": "#f3ecd0", "none": "#5d5d66", "bounce": "#6d6d75"}[kind]
    s += "<rect x='290' y='20' width='16' height='100' fill='%s' stroke='%s' stroke-width='1.5'/>" % (wall, INK)
    if label is True:
        s += text(178, 128, "?", 15) + text(298, 136, "wall", 12, weight=400)
    elif label:
        s += text(178, 128, label, 13) + text(298, 136, "wall", 12, weight=400)
    return svg_wrap(320, 140, s, "a flashlight shines at a material; the wall behind is %s" % WALL[kind])


def g_kind():
    m, k = R.choice(MAT)
    who = P.next()[0]
    t = R.random() < 0.55
    if not once((m, t)):
        return None
    if t:
        return item("%s shines a flashlight at %s. What happens to the light?" % (who, m), "It " + WORD[k] + ".", ["It " + WORD[x] + "." for x in WORD if x != k],
                    "%s %s." % (m[0].upper() + m[1:], WORD[k]))
    if k == "bounce":
        return item("%s shines a flashlight at %s. Where does most of the light go?" % (who, m), "It bounces back toward the flashlight side.", ["It goes through to the wall.", "It turns into sound.", "It goes into the floor."],
                    "%s is shiny. It reflects light." % (m[0].upper() + m[1:]))
    return item("%s holds %s in a beam of light. What will the wall behind it look like?" % (who, m), WALL[k], [WALL[x] for x in ("all", "some", "none") if x != k] + ["rainbow colored"],
                "%s %s." % (m[0].upper() + m[1:], WORD[k]))


def g_beam():
    k = R.choice(list(WORD))
    who = P.next()[0]
    q = R.choice(["mat", "what"])
    if not once((k, q), 2):
        return None
    pic = fig(beam_svg(k))
    if q == "what":
        return item(pic + "%s puts something in the light. Look at the wall. What does the thing do?" % who, "It " + WORD[k] + ".", ["It " + WORD[x] + "." for x in WORD if x != k],
                    "The wall is %s." % WALL[k])
    good = R.choice([m for m, x in MAT if x == k])
    bad = [R.choice([m for m, x in MAT if x == y]) for y in WORD if y != k]
    if not once(("bm", good)):
        return None
    return item(pic + "Look at the wall in %s's test. What could the thing be?" % who, good, bad, "It %s." % WORD[k])


def g_word():
    k = R.choice(list(WORD))
    who = P.next()[0]
    t = R.random() < 0.5
    if not once((k, t), 2):
        return None
    if t:
        return item("%s's material %s. Which word fits?" % (who, WORD[k]), NAME[k], [NAME[x] for x in NAME if x != k], "%s means it %s." % (NAME[k].split(" ")[0].capitalize(), WORD[k]))
    m = R.choice([m for m, x in MAT if x == k])
    if not once(("w", m)):
        return None
    return item("%s tests %s. Which word fits it?" % (who, m), NAME[k], [NAME[x] for x in NAME if x != k], "%s %s." % (m[0].upper() + m[1:], WORD[k]))


USES = [("a window so you can see outside", "clear glass", "all"), ("curtains to make a bedroom dark", "thick cloth", "none"),
        ("a lampshade that glows softly", "thin paper", "some"), ("a sign that shines at night when car lights hit it", "a shiny reflector", "bounce"),
        ("a box to keep film in the dark", "cardboard", "none"), ("a fish tank so you can see the fish", "clear plastic", "all"),
        ("a bathroom window that lets light in but hides you", "frosted glass", "some"), ("a hat that shades your face", "thick straw", "none")]
CHOICE = {"all": "clear plastic", "some": "tissue paper", "none": "cardboard", "bounce": "aluminum foil"}


def g_use():
    job, best, k = R.choice(USES)
    who = P.next()[0]
    if not once(job):
        return None
    w = [CHOICE[x] for x in CHOICE if x != k]
    return item("%s wants to make %s. Which material is best?" % (who, job), best, w, "It needs a material that %s." % WORD[k])


def g_shadow():
    who = P.next()[0]
    ms = [R.choice([m for m, x in MAT if x == y]) for y in ("all", "some", "none")]
    R.shuffle(ms)
    q = R.choice(["dark", "none"])
    if not once((tuple(ms), q)):
        return None
    kinds = {m: x for m, x in MAT}
    if q == "dark":
        a = [m for m in ms if kinds[m] == "none"][0]
        return item("%s makes shadows with %s, %s and %s. Which makes the darkest shadow?" % (who, ms[0], ms[1], ms[2]), a, [m for m in ms if m != a] + ["They are all the same."],
                    "%s blocks all the light." % (a[0].upper() + a[1:]))
    a = [m for m in ms if kinds[m] == "all"][0]
    return item("%s shines light on %s, %s and %s. Which makes almost no shadow?" % (who, ms[0], ms[1], ms[2]), a, [m for m in ms if m != a] + ["They all make dark shadows."],
                "%s lets the light through." % (a[0].upper() + a[1:]))


B1 = bank([
    ("What happens when light hits clear glass?", "It goes through.", ["It stops.", "It turns dark.", "It bounces back like a mirror."], "Clear glass is transparent."),
    ("What does a mirror do to light?", "bounces it back", ["lets it all through", "soaks it up like a towel", "makes it louder"], "Mirrors reflect light."),
    ("Which makes a dark shadow?", "a book", ["clear glass", "clear plastic wrap", "a glass of water"], "A book blocks the light."),
    ("Which lets some light through?", "wax paper", ["a wooden block", "a metal pan", "clear glass"], "Wax paper is translucent."),
    ("What is a shadow?", "a dark place where light is blocked", ["a kind of light", "a mirror", "a color"], "Something blocks the light."),
    ("Which word means 'blocks all light'?", "opaque", ["transparent", "translucent", "reflective"], "Opaque things make shadows."),
    ("Which word means 'lets all light through'?", "transparent", ["opaque", "translucent", "reflective"], "Like clear glass."),
    ("Which word means 'shiny, bounces light'?", "reflective", ["opaque", "transparent", "translucent"], "Like a mirror."),
])
B5 = bank([
    ("Ava puts tissue paper in a flashlight beam. The wall is a little bright. Why?", "Tissue paper lets some light through.", ["It blocks all light.", "It makes light.", "It is a mirror."], "Translucent."),
    ("Leo's wall has a dark shadow. What did he put in the beam?", "a wooden block", ["clear plastic wrap", "a window", "a glass of water"], "Opaque."),
    ("Mia shines a flashlight at a mirror. Where does the light go?", "It bounces back.", ["Through the mirror.", "It disappears.", "Into the mirror forever."], "Reflective."),
    ("Kai tests 4 materials. How should he hold the flashlight?", "at the same spot for each one", ["closer for some", "off for some", "far away for one"], "Keep the test fair."),
    ("Zoe wants a curtain to keep sunlight out. Which test result is best?", "The wall stays dark.", ["The wall is bright.", "The wall is dim.", "The light bounces off the wall."], "Opaque blocks light."),
])


def body():
    pic = "<div style='display:flex;gap:10px;flex-wrap:wrap'>%s%s%s</div>" % (beam_svg("all", "clear glass"), beam_svg("some", "wax paper"), beam_svg("none", "cardboard"))
    ex = [("Light hits clear plastic wrap. What happens?", ["It is clear."], "It goes through."),
          ("Light hits cardboard. What is on the wall?", ["Cardboard blocks light."], "a dark shadow")]
    mist = ["Thinking clear glass makes a dark shadow.",
            "Thinking a mirror lets light through. It bounces light.",
            "Thinking wax paper blocks all light. It lets some through."]
    return kid_lesson(pic, "Shine a light. What happens?",
                      ["Clear: all light goes through.", "Wax paper: some light goes through.", "Cardboard: blocks light. Mirror: bounces light."], ex, mist)


def main():
    sets = U.sets([
        ("What does light do?", B1 + [(g_kind, 8), (g_beam, 4)]),
        ("Through or blocked?", [(g_kind, 12), (g_beam, 8)]),
        ("Light words", [(g_word, 12), (g_kind, 8)]),
        ("Shadows", [(g_shadow, 12), (g_use, 4), (g_beam, 4)]),
        ("Light testers", B5 + [(g_use, 4), (g_shadow, 4), (g_word, 4), (g_kind, 3)]),
    ])
    make("grade-1", "light-and-materials", 3, "1-PS4-3",
         "Plan and conduct investigations to determine the effect of placing objects made with different materials in the path of a beam of light.",
         "Light and Materials",
         "Grade 1 Light and Materials Worksheets: Transparent, Translucent, Opaque and Reflective",
         "Light and Materials",
         "Free grade 1 science worksheets on light and materials (NGSS 1-PS4-3): what happens when light hits glass, wax paper, cardboard and mirrors, and how shadows form. 100 picture questions with answers.",
         "Some things let light through.",
         "Clear things let light through. Others block it or bounce it.",
         body(),
         [("What are transparent, translucent and opaque?", "Transparent things let all light through, translucent things let some through, and opaque things block it."),
          ("What does a mirror do?", "A mirror is reflective. It bounces light back."),
          ("How can kids test this?", "Shine a flashlight at each material and look at the wall behind it: bright, dim or a dark shadow.")],
         sets)


if __name__ == "__main__":
    main()
