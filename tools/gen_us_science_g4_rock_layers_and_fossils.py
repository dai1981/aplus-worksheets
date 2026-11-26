# -*- coding: utf-8 -*-
"""
US Grade 4 Science: Rock Layers and Fossils (4-ESS1-1)
  python tools/gen_us_science_g4_rock_layers_and_fossils.py
Patterns in rock formations and fossils in rock layers are evidence of changes in a landscape over time:
bottom layers are usually oldest (superposition), marine fossils show an area was once under water,
plant fossils show land, a canyon shows a river cut down through layers over a long time.
Assessment boundary: relative ages only, no absolute dating or rock-forming mechanisms.
Wrong answers come from real mistakes: "the top layer is the oldest", "fossils of fish mean the area
is a lake now", "a canyon formed in a few days".
"""
from sci_common import Unit, item, bank, lesson, make, fig, figure, svg_wrap, rect, line, circle, text, People, INK, BLUE, LEAF

U = Unit(40112)
R = U.R
P = People(R)
COLS = ["#e9d6a9", "#c9a26b", "#d9b98c", "#a88a6a", "#e2c79a", "#b99773"]
# fossil: (environment it shows, how to draw)
FOSSIL = {"seashell": "ocean", "fish": "water", "fern": "land", "dinosaur footprint": "land", "coral": "ocean", "tree leaf": "land", "clam": "ocean", "shark tooth": "ocean"}
ENV = {"ocean": "The area was once covered by ocean water.", "water": "The area was once covered by water.", "land": "The area was once dry land with plants or animals living on it."}


def draw_fossil(kind, x, y):
    if kind in ("seashell", "clam"):
        return ("<path d='M%d %d Q%d %d %d %d Z' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x - 10, y + 5, x, y - 12, x + 10, y + 5, INK)
                + line(x, y + 5, x, y - 5, INK, 1) + line(x - 5, y + 5, x - 3, y - 3, INK, 1) + line(x + 5, y + 5, x + 3, y - 3, INK, 1))
    if kind == "fish":
        return ("<path d='M%d %d Q%d %d %d %d Q%d %d %d %d Z' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x - 14, y, x - 2, y - 8, x + 8, y, x - 2, y + 8, x - 14, y, INK)
                + "<path d='M%d %d L%d %d L%d %d Z' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x + 8, y, x + 16, y - 6, x + 16, y + 6, INK))
    if kind in ("fern", "tree leaf"):
        s = line(x - 14, y + 6, x + 14, y - 6, LEAF, 2)
        for t in range(-2, 3):
            cx, cy = x + 6 * t, y - 2.5 * t
            s += line(cx, cy, cx - 3, cy - 7, LEAF, 1.5) + line(cx, cy, cx + 3, cy + 7, LEAF, 1.5)
        return s
    if kind == "dinosaur footprint":
        return "".join("<path d='M%d %d L%d %d' stroke='%s' stroke-width='3' stroke-linecap='round'/>" % (x, y + 6, x + dx, y - 6, INK) for dx in (-7, 0, 7)) + circle(x, y + 6, 3, INK, INK, 0)
    if kind == "coral":
        return "".join(line(x, y + 8, x + dx, y - 6, "#c0504d", 2.5) for dx in (-8, -3, 3, 8))
    if kind == "shark tooth":
        return "<path d='M%d %d L%d %d L%d %d Z' fill='#fff' stroke='%s' stroke-width='1.5'/>" % (x - 7, y + 6, x, y - 9, x + 7, y + 6, INK)
    return ""


def layers(fossils, label="rock layers with fossils", letters=True, river=False):
    """fossils: list from bottom to top, one per layer (None = no fossil)."""
    n = len(fossils)
    h = 42
    W = 320
    top = 10
    s = []
    for i in range(n):
        y = top + (n - 1 - i) * h
        s.append(rect(10, y, W - 60, h, COLS[i % len(COLS)], INK, 1.5))
        if letters:
            s.append(text(W - 34, y + h / 2 + 6, "ABCDEF"[n - 1 - i], 16))
        if fossils[i]:
            fx, fy = 60 + 50 * (i % 3), y + h / 2
            s.append("<g transform='translate(%d %d) scale(1.6) translate(%d %d)'>%s</g>" % (fx, fy, -fx, -fy, draw_fossil(fossils[i], fx, fy)))
    if river:
        s.append("<path d='M120 %d L150 %d L170 %d L200 %d Z' fill='#fff' stroke='none'/>" % (top - 1, top + n * h - 20, top + n * h - 20, top - 1))
        s.append(line(120, top, 150, top + n * h - 20, INK, 1.5) + line(200, top, 170, top + n * h - 20, INK, 1.5))
        s.append(rect(150, top + n * h - 26, 20, 6, BLUE, BLUE, 0))
    return svg_wrap(W, top + n * h + 10, "".join(s), label).replace("<svg ", "<svg data-pf='lg' ", 1)


def g_oldest():
    n = R.choice([3, 4, 5])
    fs = [R.choice(sorted(FOSSIL)) if R.random() < 0.6 else None for _ in range(n)]
    L = "ABCDEF"[:n]
    k = R.choice(["oldest", "youngest", "pair", "pair", "fossil"])
    if k == "pair":
        x, y = sorted(R.sample(L, 2))
        q = R.choice(["older", "younger"])
        a = (y if q == "older" else x)
        return item(fig(layers(fs)) + "The rock layers have not been turned over. Which layer is %s, layer %s or layer %s?" % (q, x, y), "layer " + a,
                    ["layer " + (x if a == y else y), "They are the same age.", "You cannot tell from layers."],
                    "Layer %s is lower than layer %s, so it is older." % (y, x))
    if k == "fossil":
        idx = [i for i in range(n) if fs[i]]
        if len(idx) < 2 or len({fs[i] for i in idx}) < len(idx):
            return None
        i, j = sorted(R.sample(idx, 2))
        return item(fig(layers(fs)) + "Which fossil is older: the %s or the %s?" % (fs[j], fs[i]) if R.random() < 0.5 else fig(layers(fs)) + "Which fossil is older: the %s or the %s?" % (fs[i], fs[j]),
                    "the " + fs[i], ["the " + fs[j], "They are the same age.", "the one closer to the top"],
                    "The %s is in a lower layer, so it is older." % fs[i])
    if k == "oldest":
        a = L[-1]
        w = [x for x in L if x != a]
        return item(fig(layers(fs)) + "The rock layers have not been turned over. Which layer is the oldest?", a, R.sample(w, min(3, len(w))) if len(w) >= 3 else w + ["All are the same age."],
                    "Layers form one on top of another, so the bottom layer (%s) formed first and is the oldest." % a)
    a = L[0]
    w = [x for x in L if x != a]
    return item(fig(layers(fs)) + "The rock layers have not been turned over. Which layer formed most recently?", a, R.sample(w, 3) if len(w) >= 3 else w + ["All are the same age."],
                "The top layer (%s) formed last, so it is the youngest." % a)


def g_env():
    n = R.choice([3, 4])
    fs = [None] * n
    i = R.randrange(n)
    f = R.choice(sorted(FOSSIL))
    fs[i] = f
    L = "ABCDEF"[n - 1 - i]
    env = FOSSIL[f]
    w = [ENV[e] for e in ENV if e != env and not {e, env} <= {"ocean", "water"}] + ["The area has always looked the same.", "The area was always covered by ice."]
    return item(fig(layers(fs)) + "Layer %s has a %s fossil. What does this tell you about the area when layer %s formed?" % (L, f, L), ENV[env], R.sample(w, 3),
                "A %s fossil is evidence that %s" % (f, ENV[env][0].lower() + ENV[env][1:]))


def g_change():
    a, b = R.sample(["ocean", "land"], 2) if R.random() < 0.5 else ("ocean", "land")
    low = R.choice([f for f in FOSSIL if FOSSIL[f] == a])
    high = R.choice([f for f in FOSSIL if FOSSIL[f] == b])
    fs = [low, None, high]
    word = {"ocean": "covered by ocean", "land": "dry land"}
    return item(fig(layers(fs)) + "The bottom layer has a %s fossil. The top layer has a %s fossil. How did this area change over time?" % (low, high),
                "It was %s first and later became %s." % (word[a], word[b]), ["It was %s first and later became %s." % (word[b], word[a]), "It never changed.", "Both layers formed on the same day."],
                "Bottom layers are older. The %s (older) shows %s; the %s (younger) shows %s." % (low, word[a], high, word[b]))


def g_canyon():
    n = 4
    fs = [R.choice(sorted(FOSSIL)) for _ in range(n)]
    k = R.choice(["what", "oldest", "time"])
    pic = fig(layers(fs, "a canyon cut through rock layers with a river at the bottom", letters=False, river=True))
    if k == "what":
        return item(pic + "A river runs at the bottom of this canyon. What most likely made the canyon?", "The river wore away the rock over a very long time.",
                    ["An earthquake made it in one day.", "People dug it with shovels.", "The rock layers grew upward around the river."], "Moving water slowly erodes rock and cuts deeper over millions of years.")
    if k == "oldest":
        return item(pic + "In the canyon walls, where are the oldest rock layers?", "at the bottom, near the river", ["at the top of the walls", "in the middle only", "All layers are the same age."],
                    "Layers at the bottom formed first.")
    return item(pic + "The walls show the same rock layers on both sides of the canyon. What does this show?", "The layers were once connected before the river cut through them.",
                ["The two sides formed in different places.", "Each side formed on a different day.", "The river made the layers."], "Matching layers are evidence that the river cut down through one landscape.")


B1 = bank([
    ("What is a fossil?", "the remains or traces of a living thing from long ago, preserved in rock", ["a kind of shiny mineral", "a rock that is still being formed", "a living animal in a cave"],
     "Shells, bones, leaves and footprints can all become fossils."),
    ("In rock layers that have not been moved, which layer is usually the oldest?", "the bottom layer", ["the top layer", "the middle layer", "the thickest layer"],
     "Each new layer forms on top of the older ones."),
    ("A fossil of a fern is found in rock. What does it show about the area long ago?", "It was land where plants grew.", ["It was the bottom of the ocean.", "It was covered by ice.", "It was a volcano."],
     "Ferns grow on land."),
    ("Fossil seashells are found on top of a mountain. What does this show?", "The rock formed under the ocean and was later pushed up.", ["Birds carried the shells up.", "The mountain is under water now.", "Shells grow on mountains."],
     "The landscape changed over a very long time."),
    ("Rock layers are like a stack of newspapers left on a porch every day. Which paper is the oldest?", "the one at the bottom", ["the one on top", "the one in the middle", "They are all the same age."],
     "The first paper was put down first, just like the bottom rock layer."),
    ("Which kind of fossil shows an area was once covered by water?", "a fish fossil", ["a fern fossil", "a dinosaur footprint", "a fossil tree leaf"], "Fish live in water."),
    ("How long does it take for thick rock layers and canyons to form?", "a very long time, thousands to millions of years", ["about one day", "about one week", "one school year"],
     "Changes in landscapes are slow."),
    ("What is a pattern in rock layers?", "the same order of layers repeating in different places", ["the color of the sky above them", "a drawing made by people", "the weather on one day"],
     "Matching patterns help scientists compare places."),
])
B5 = bank([
    ("Ava finds a fossil fish in a layer and a fossil fern in the layer just above it. Which happened first?", "The area was under water.", ["The area had ferns.", "Both at the same time.", "You cannot tell."],
     "The lower layer is older."),
    ("Leo sees the same three layers in two cliffs across a valley. What can he conclude?", "The layers were once connected, and the valley was carved later.", ["The cliffs formed in different places.", "The valley is older than the layers.", "The layers are different ages on each side."],
     "Matching patterns show the layers formed together."),
    ("Why do scientists say the Grand Canyon took millions of years to form?", "The Colorado River wears away rock very slowly.", ["People measured it with a ruler.", "It formed after one big storm.", "The rock grew upward."],
     "Slow erosion over a long time cut the canyon."),
    ("Mia models rock layers with colored sand in a jar. Which color did she pour first?", "the color at the bottom", ["the color on top", "the color in the middle", "the brightest color"],
     "The first layer poured ends up on the bottom."),
    ("A fossil of a palm tree is found in rock in a cold, snowy place. What does this suggest?", "The area once had a warm climate.", ["Palm trees grow in snow.", "The fossil is from today.", "The area was always cold."],
     "Fossils show how environments changed."),
])


def body():
    think = ("<p>Rock layers form one on top of another, so in layers that have not been turned over, the <b>bottom layer is the oldest</b> and the <b>top layer is the youngest</b>.</p>"
             "<p><b>Fossils</b> in the layers tell us what the area was like when each layer formed: seashells and fish mean it was under water; ferns and footprints mean it was land.</p>"
             + figure(layers(["seashell", None, "fern"]), "The bottom layer (C) has a seashell, so the area was once ocean. The top layer (A) has a fern, so it later became land.")
             + "<p>A <b>canyon</b> shows that a river cut down through the layers over a very long time.</p>")
    ex = [("A fish fossil is in a lower layer and a leaf fossil is in a higher layer. How did the area change?", ["Lower layers are older.", "Fish → water; leaf → land."], "It was under water, then it became land."),
          ("Which layer of a canyon wall is the oldest?", ["Layers form from the bottom up."], "the bottom layer")]
    mist = ["Thinking the top layer is the oldest.",
            "Thinking a sea fossil means the area is ocean today. It tells about the past.",
            "Thinking canyons form quickly. They take a very long time."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Fossils and rock layers", B1 + [(g_oldest, 6), (g_env, 6)]),
        ("Oldest and youngest layers", [(g_oldest, 12), (g_env, 8)]),
        ("What fossils tell us", [(g_env, 10), (g_change, 10)]),
        ("Canyons and changing landscapes", [(g_canyon, 8), (g_change, 6), (g_oldest, 6)]),
        ("Using evidence", B5 + [g_change, g_env, g_canyon, g_oldest]),
    ])
    make("grade-4", "rock-layers-and-fossils", 12, "4-ESS1-1",
         "Identify evidence from patterns in rock formations and fossils in rock layers to support an explanation for changes in a landscape over time.",
         "Rock Layers and Fossils",
         "Grade 4 Rock Layers and Fossils Worksheets: Oldest Layers and Changing Landscapes",
         "Rock Layers and Fossils",
         "Free Grade 4 science worksheets on rock layers and fossils (NGSS 4-ESS1-1): oldest and youngest layers, what fossils show about past environments, and how canyons form over time. 100 practice questions with answers.",
         "In rock layers, the bottom layer is the oldest.",
         "Fossils in each layer show what the area was like long ago, like ocean (seashells) or land (ferns).",
         body(),
         [("Which rock layer is the oldest?", "In layers that have not been turned over, the bottom layer is the oldest because each new layer forms on top."),
          ("What can fossils tell us?", "They show what lived in an area long ago, so they tell us whether the area was ocean, a lake or dry land."),
          ("Why are there seashell fossils on mountains?", "The rock formed under the ocean long ago and was slowly pushed up to form the mountains.")],
         sets)


if __name__ == "__main__":
    main()
