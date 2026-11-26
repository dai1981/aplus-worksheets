# -*- coding: utf-8 -*-
"""
UK Year 3 science: Shadows (Light)
  python tools/gen_uk_science_y3_shadows.py
Shadows are formed when the light from a light source is blocked by an opaque object; transparent, translucent and
opaque materials; which side a shadow falls on; how the size of a shadow changes as the object moves nearer to or
further from the light; shadow shapes; and shadows made by the Sun during the day. Investigation tables.
Reuses the shadow and material questions of the Year 6 light units (new seed) and adds Year 3 questions.
Wrong answers come from real mistakes: "a shadow is a reflection", "shadows point towards the light",
"moving away from the torch makes the shadow bigger", "transparent things make dark shadows".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, People, once
import gen_uk_science_y6_shadows_and_reflection as S6
import gen_uk_science_y6_how_light_travels as L6

U = Unit(61311)
R = U.R
P = People(R)
S6.U = L6.U = U
S6.R = L6.R = R
S6.P = L6.P = P
uk_sci.USED.clear()

OBJ = ["a teddy bear", "a vase", "a toy car", "a plastic dinosaur", "a cup", "a model house", "a football", "a doll", "a toy robot", "a wooden block",
       "a paper puppet", "a jug", "a lamp post", "a tree"]


def g_side():
    o = R.choice(OBJ)
    side = R.choice(["left", "right", "in front of", "behind"])
    if not once(("sd", o)):
        return None
    opp = {"left": "on the right of the object", "right": "on the left of the object", "in front of": "behind the object", "behind": "in front of the object"}
    src = "on the %s of" % side if side in ("left", "right") else side
    a = opp[side]
    if "tree" in o or "lamp" in o:
        q = "The Sun is shining from %s %s. Where is its shadow?" % (src.replace(" of", ""), o) if side in ("in front of", "behind") else "The Sun is %s %s. Where is its shadow?" % (src, o)
    else:
        q = "A torch is %s %s. Where is its shadow?" % (src, o)
    w = [x for x in opp.values() if x != a]
    return item(q, a, w, "A shadow forms on the opposite side of the object from the light.")


SIZE = [("moves the %s closer to the torch", "The shadow gets bigger."), ("moves the %s further from the torch", "The shadow gets smaller."),
        ("moves the torch closer to the %s", "The shadow gets bigger."), ("moves the torch further from the %s", "The shadow gets smaller.")]


def g_size():
    who = P.next()[0]
    act, a = R.choice(SIZE)
    o = R.choice(OBJ[:12])
    if not once(("sz", act, o)) or not once(("sa", act), 3):
        return None
    return item("%s is making shadows on a screen with %s. %s %s. What happens to the shadow?" % (who, o, who, act % o.split(" ", 1)[1]), a,
                [x for x in ["The shadow gets bigger.", "The shadow gets smaller.", "The shadow stays the same size.", "The shadow disappears."] if x != a],
                "The closer the object is to the light, the more light it blocks, so the shadow is bigger.")


B1 = bank([
    ("What is a shadow?", "a dark area where light is blocked by an object", ["a reflection of an object", "a light source", "a kind of mirror"], "Light cannot get through."),
    ("What do you need to make a shadow?", "a light source and an object that blocks light", ["only a mirror", "only darkness", "only water"], "And a surface for it to fall on."),
    ("Which kind of material makes the darkest shadow?", "an opaque material", ["a transparent material", "a translucent material", "a mirror"], "It blocks all the light."),
    ("Why does a window not make a dark shadow?", "Glass is transparent and lets light through.", ["Glass is opaque.", "Windows are light sources.", "Glass is too thin to exist."], "Light passes through."),
    ("Why does a shadow have the same outline as the object?", "Light travels in straight lines, so the object blocks a shape of light.", ["Shadows copy objects on purpose.", "Light bends around objects.", "Shadows are reflections."], "Straight lines."),
    ("Is a shadow a reflection?", "No. A shadow is where light is blocked, not bounced back.", ["Yes, it is a dark mirror image.", "Yes, in sunlight.", "Only on water."], "Different things."),
    ("Can you see your shadow in a completely dark room?", "No. A shadow needs a light source.", ["Yes, it is darker than the room.", "Yes, if you jump.", "Only at night."], "No light, no shadow."),
    ("What colour is a shadow?", "dark, because little or no light reaches it", ["the same colour as the object", "always blue", "bright white"], "It is an absence of light."),
])
B5 = bank([
    ("Why is a shadow from a translucent material lighter than one from an opaque material?", "Some light passes through translucent materials.", ["Translucent materials are light sources.", "Opaque materials let light through.", "They make the same shadow."], "Partly blocked."),
    ("How could you make the shadow of a puppet bigger on a screen?", "Move the puppet closer to the torch.", ["Move the puppet closer to the screen.", "Turn the torch off.", "Use a smaller screen."], "Closer to the light."),
    ("Why are shadows shortest at midday?", "The Sun is highest in the sky.", ["The Sun is lowest then.", "The Sun is behind the Moon.", "Shadows rest at midday."], "High Sun, short shadows."),
    ("How did people use shadows to tell the time long ago?", "with a sundial, whose shadow moves as the Sun moves across the sky", ["by measuring the Moon's shadow only", "with mirrors", "with candles"], "Sundials."),
    ("In a shadow puppet show, why must the puppets be opaque?", "so they block the light and make clear, dark shadows", ["so they reflect light", "so light passes through", "so the screen stays bright"], "Clear shapes."),
])


def body():
    think = ("<p><b>A shadow forms when an opaque object blocks light from a light source.</b></p>"
             "<ul><li>Opaque materials block all light; translucent let some through; transparent let almost all through.</li>"
             "<li>The shadow falls on the side away from the light and has the same outline as the object.</li>"
             "<li>The closer the object is to the light, the bigger the shadow.</li></ul>")
    ex = [("Torch on the left of a cup. Shadow?", ["Opposite side"], "on the right"),
          ("Move the toy nearer the torch. Shadow?", ["Blocks more light"], "bigger")]
    mist = ["Thinking a shadow is a reflection.", "Thinking shadows point towards the light.", "Thinking moving away from the torch makes the shadow bigger."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("What makes a shadow?", B1 + [(L6.g_mat, 8), (g_side, 4)]),
        ("Opaque, translucent, transparent", [(L6.g_mat, 8), (L6.g_def, 6), (S6.g_shape, 6)]),
        ("Where shadows fall", [(g_side, 6), (g_size, 8), (S6.g_sun, 6)]),
        ("Shadow investigation", [(S6.g_shd, 20)]),
        ("Thinking about shadows", B5 + [(S6.g_shd, 8), (g_size, 4), (g_side, 2), (L6.g_def, 1)]),
    ])
    make_uk(3, "shadows", 11, "Light",
            "Recognise that shadows are formed when the light from a light source is blocked by an opaque object. Find patterns in the way that the size of shadows change.",
            "Shadows",
            "Year 3 Science: Shadows Worksheets (Opaque, Translucent, Transparent)",
            "Shadows",
            "Free Year 3 science worksheets on shadows: how shadows form, opaque, translucent and transparent materials, shadow size and position, and shadows from the Sun. 100 questions with answers.",
            "Opaque objects block light.",
            "Closer to the light, bigger shadow.",
            body(),
            [("How is a shadow made?", "When an opaque object blocks light from a light source, a dark area forms behind it on the side away from the light. That is a shadow."),
             ("How can you change the size of a shadow?", "Move the object closer to the light to make the shadow bigger, or further from the light to make it smaller."),
             ("What is the difference between opaque, translucent and transparent?", "Opaque materials let no light through and make dark shadows. Translucent materials let some light through. Transparent materials let almost all light through.")],
            sets)


if __name__ == "__main__":
    main()
