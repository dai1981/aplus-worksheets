# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Maps of Land and Water (2-ESS2-2)
  python tools/gen_us_science_g2_maps_of_land_and_water.py
Develop a model to represent the shapes and kinds of land and bodies of water in an area.
Kinds of land (mountain, hill, plain, valley, island, beach, forest) and bodies of water (ocean, lake, river, pond);
reading a simple map with a key, finding features by letter, and comparing them.
Wrong answers come from real mistakes: "a lake and an ocean are the same", "an island is a body of water",
"a river does not move".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(20110)
R = U.R
P = People(R)
USED = {}
BLUE, LAND = "#9fd0f0", "#e7f0d2"


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def mountain(x, y, k=1.0):
    return "<path d='M%g %g L%g %g L%g %g Z' fill='#a98b6d' stroke='%s' stroke-width='1.5'/><path d='M%g %g L%g %g L%g %g Z' fill='#fff'/>" % (
        x - 18 * k, y + 14 * k, x, y - 16 * k, x + 18 * k, y + 14 * k, INK, x - 6 * k, y - 4 * k, x, y - 16 * k, x + 6 * k, y - 4 * k)


def tree(x, y, k=1.0):
    return "<rect x='%g' y='%g' width='%g' height='%g' fill='#8a5a2b'/><circle cx='%g' cy='%g' r='%g' fill='#4f9a4f' stroke='%s' stroke-width='1.2'/>" % (
        x - 2 * k, y, 4 * k, 9 * k, x, y - 4 * k, 8 * k, INK)


def town(x, y):
    return "".join("<rect x='%g' y='%g' width='10' height='9' fill='#e8893a' stroke='%s' stroke-width='1'/><path d='M%g %g l5 -6 l5 6 Z' fill='#b5462f'/>" % (
        x + dx - 5, y + dy, INK, x + dx - 5, y + dy) for dx, dy in [(-9, 0), (6, 0), (-2, 12)])


def hillf(x, y):
    return "<path d='M%g %g Q%g %g %g %g Z' fill='#b7d38f' stroke='%s' stroke-width='1.5'/>" % (x - 20, y + 10, x, y - 18, x + 20, y + 10, INK)


FEAT = {"ocean": "ocean", "lake": "lake", "river": "river", "mountains": "mountains", "forest": "forest", "town": "town", "island": "island", "hill": "hill", "beach": "beach"}
WATER = {"ocean", "lake", "river"}


def map_svg(labels=None, key=True, flip=False):
    """A map: ocean on one side with a beach and an island, a river from the mountains to the ocean, a lake, a forest, a hill and a town.
    labels: {feature: letter}. Returns svg and the feature positions."""
    W, H = 420, 260
    s = "<rect x='0' y='0' width='%d' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (W, H, LAND, INK)
    pos = {}
    s += "<path d='M300 0 Q280 70 296 130 Q312 200 290 260 L420 260 L420 0 Z' fill='%s'/>" % BLUE
    s += "<path d='M300 0 Q280 70 296 130 Q312 200 290 260' fill='none' stroke='#e6cf8f' stroke-width='9'/>"
    pos["beach"] = (290, 200)
    pos["ocean"] = (370, 70)
    s += "<ellipse cx='372' cy='190' rx='26' ry='16' fill='#e7f0d2' stroke='#c9a95a' stroke-width='3'/>" + tree(372, 190, 0.8)
    pos["island"] = (372, 190)
    for i, (x, y) in enumerate([(50, 50), (86, 40), (120, 56)]):
        s += mountain(x, y)
    pos["mountains"] = (86, 44)
    s += "<path d='M110 70 Q150 110 190 100 Q240 90 262 140 Q276 170 300 168' fill='none' stroke='%s' stroke-width='7' stroke-linecap='round'/>" % BLUE
    pos["river"] = (190, 100)
    s += "<ellipse cx='90' cy='190' rx='44' ry='24' fill='%s' stroke='#5aa6d6' stroke-width='2'/>" % BLUE
    pos["lake"] = (90, 190)
    for x, y in [(190, 170), (210, 180), (230, 168), (205, 200), (228, 196)]:
        s += tree(x, y)
    pos["forest"] = (212, 186)
    s += hillf(170, 40) + hillf(200, 46)
    pos["hill"] = (186, 38)
    s += town(150, 220)
    pos["town"] = (150, 230)
    if labels:
        LP = {"ocean": (385, 34), "lake": (152, 186), "river": (262, 140), "mountains": (86, 86), "forest": (256, 196), "town": (186, 236),
              "island": (372, 226), "hill": (236, 24), "beach": (297, 132)}
        for f, L in labels.items():
            x, y = LP[f]
            s += "<circle cx='%g' cy='%g' r='12' fill='#fff' stroke='%s' stroke-width='2'/>" % (x, y, INK) + text(x, y + 5, L, 14)
    return svg_wrap(W, H, s, "a map with mountains, a hill, a river, a lake, a forest, a town, a beach, an ocean and an island")


def g_letter():
    feats = R.sample(sorted(FEAT), 4)
    letters = dict(zip(feats, "ABCD"))
    target = R.choice(feats)
    who = P.next()[0]
    if not once(("l", tuple(feats), target)) or not once(("lt", target), 3):
        return None
    pic = fig(map_svg(letters))
    return item(pic + "%s made a map. Which letter shows the %s?" % (who, FEAT[target]), letters[target], [letters[f] for f in feats if f != target], "Find the %s on the map." % FEAT[target])


def g_name():
    feats = R.sample(sorted(FEAT), 4)
    letters = dict(zip(feats, "ABCD"))
    target = R.choice(feats)
    who = P.next()[0]
    if not once(("n", tuple(feats), target)) or not once(("nt", target), 3):
        return None
    pic = fig(map_svg(letters))
    return item(pic + "On %s's map, what is at letter %s?" % (who, letters[target]), FEAT[target], [FEAT[f] for f in feats if f != target], "Letter %s marks the %s." % (letters[target], FEAT[target]))


def g_water():
    feats = R.sample(sorted(FEAT), 4)
    w = [f for f in feats if f in WATER]
    who = P.next()[0]
    q = R.choice(["water", "land"])
    good = w if q == "water" else [f for f in feats if f not in WATER]
    if len(good) != 1 or not once(("w", tuple(feats), q)):
        return None
    letters = dict(zip(feats, "ABCD"))
    a = good[0]
    return item(fig(map_svg(letters)) + "On %s's map, which letter shows %s?" % (who, "a body of water" if q == "water" else "land, not water"), letters[a], [letters[f] for f in feats if f != a],
                "The %s is %s." % (FEAT[a], "water" if q == "water" else "land"))


DESC = [("land with water all around it", "an island", ["a lake", "a river", "a valley"]),
        ("water with land all around it", "a lake", ["an island", "an ocean", "a mountain"]),
        ("water that flows downhill to a lake or the ocean", "a river", ["a pond", "a lake", "a hill"]),
        ("a very big body of salty water", "an ocean", ["a pond", "a river", "a lake"]),
        ("very tall land with steep sides and a pointed top", "a mountain", ["a hill", "a plain", "a valley"]),
        ("raised land that is lower and rounder than a mountain", "a hill", ["a mountain", "a valley", "an island"]),
        ("flat land that goes on for a long way", "a plain", ["a mountain", "a hill", "a valley"]),
        ("low land between hills or mountains", "a valley", ["a plain", "a hill", "an island"]),
        ("sandy land next to the ocean or a lake", "a beach", ["a valley", "a mountain", "a river"]),
        ("a small, still body of water", "a pond", ["an ocean", "a river", "a mountain"])]


def g_desc():
    d, a, w = R.choice(DESC)
    who = P.next()[0]
    t = R.random() < 0.6
    if not once((d, t)):
        return None
    if t:
        return item("%s describes %s. What is it?" % (who, d), a, w, "%s is %s." % (a[0].upper() + a[1:], d))
    others = [x[0] for x in DESC if x[1] != a]
    return item("%s finds %s on a map. Which describes it?" % (who, a), d, R.sample(others, 3), "%s is %s." % (a[0].upper() + a[1:], d))


def g_kind():
    pool = [("ocean", "water"), ("lake", "water"), ("river", "water"), ("pond", "water"), ("mountain", "land"), ("hill", "land"), ("plain", "land"), ("valley", "land"),
            ("island", "land"), ("beach", "land")]
    a = R.sample(pool, 4)
    q = R.choice(["water", "land"])
    good = [x for x in a if x[1] == q]
    if len(good) != 1 or not once(("k", tuple(a), q)):
        return None
    who = P.next()[0]
    return item("%s sorts words: %s. Which one is %s?" % (who, ", ".join(x[0] for x in a), "a body of water" if q == "water" else "a kind of land"), good[0][0], [x[0] for x in a if x != good[0]],
                "%s is %s." % (good[0][0][0].upper() + good[0][0][1:], "water" if q == "water" else "land"))


REL = [("river", "flows from the mountains to the ocean"), ("lake", "is near the town"), ("island", "is in the ocean"), ("beach", "is between the land and the ocean"),
       ("forest", "is near the river"), ("mountains", "are where the river starts")]


def g_rel():
    f, r = R.choice(REL)
    who = P.next()[0]
    if not once(("r", f)):
        return None
    pic = fig(map_svg())
    return item(pic + "Look at %s's map. Which is true about the %s?" % (who, f), "The %s %s." % (f, r), ["The %s %s %s." % (f, "are" if f == "mountains" else "is", x) for x in R.sample([y for y in ["in the middle of the lake", "on top of the mountains", "inside the town", "under the ocean"] if f not in y], 3)],
                "Look closely at the map.")


B1 = bank([
    ("What is a map?", "a drawing that shows where things are", ["a kind of book of stories", "a picture of a person", "a list of numbers"], "Maps are models of a place."),
    ("What color usually shows water on a map?", "blue", ["red", "brown", "black"], "Blue means water."),
    ("What does a map key tell you?", "what the symbols on the map mean", ["what time it is", "who drew the map", "how old the map is"], "Read the key first."),
    ("Which is a body of water?", "a lake", ["a hill", "a mountain", "a valley"], "Lakes are water."),
    ("Which is a kind of land?", "a mountain", ["a river", "an ocean", "a pond"], "Mountains are land."),
    ("Is ocean water salty or fresh?", "salty", ["fresh", "sweet", "there is no water"], "Oceans are salty."),
    ("Is most lake and river water salty or fresh?", "fresh", ["salty", "sweet", "frozen all year"], "Most lakes and rivers are fresh water."),
    ("Which body of water is the biggest?", "an ocean", ["a pond", "a lake", "a river"], "Oceans are huge."),
])
B5 = bank([
    ("Ava's map has a blue line from the mountains to the sea. What does it most likely show?", "a river", ["a road", "a lake", "an island"], "Rivers flow downhill."),
    ("Leo says an island is a body of water. Is he right?", "No. An island is land with water around it.", ["Yes.", "Yes, a small one.", "No, an island is a mountain."], "The island is the land."),
    ("Mia makes a clay model: a bowl of water with clay all around it. What did she model?", "a lake", ["an island", "a river", "a mountain"], "Water with land around it."),
    ("Kai's model has a lump of clay in the middle of a pan of water. What did he model?", "an island", ["a lake", "a pond", "a river"], "Land with water around it."),
    ("Why do people make maps?", "to show the shapes and kinds of land and water in a place", ["to make art only", "to count animals", "to tell the time"], "Maps are models."),
])


def body():
    pic = map_svg({"mountains": "1", "river": "2", "lake": "3", "ocean": "4"})
    ex = [("On the map, what is at 3?", ["Water with land all around."], "a lake"),
          ("Is an island land or water?", ["It has water around it."], "land")]
    mist = ["Thinking a lake and an ocean are the same. Oceans are huge and salty.",
            "Thinking an island is water. It is land.",
            "Thinking a hill and a mountain are the same. Mountains are taller."]
    return kid_lesson(pic, "A map is a model of land and water.",
                      ["Blue = water: ocean, lake, river.", "Land: mountain, hill, island, beach.", "Use the key to read the map."], ex, mist)


def main():
    sets = U.sets([
        ("Land and water", B1 + [(g_kind, 6), (g_desc, 6)]),
        ("Kinds of land and water", [(g_desc, 12), (g_kind, 8)]),
        ("Reading a map", [(g_letter, 10), (g_name, 10)]),
        ("Map detective", [(g_water, 8), (g_name, 6), (g_letter, 6)]),
        ("Making models", B5 + [(g_rel, 5), (g_water, 5), (g_desc, 5)]),
    ])
    make("grade-2", "maps-of-land-and-water", 10, "2-ESS2-2",
         "Develop a model to represent the shapes and kinds of land and bodies of water in an area.",
         "Maps of Land and Water",
         "Grade 2 Maps of Land and Water Worksheets: Landforms and Bodies of Water",
         "Land and Water Maps",
         "Free grade 2 science worksheets on maps of land and water (NGSS 2-ESS2-2): mountains, hills, islands, lakes, rivers and oceans, and reading a simple map. 100 picture questions with answers.",
         "A map shows land and water.",
         "Blue is water. Use the key to find mountains, lakes and rivers.",
         body(),
         [("What are kinds of land?", "Mountains, hills, plains, valleys, islands and beaches."),
          ("What are bodies of water?", "Oceans, lakes, rivers and ponds. Oceans are salty; most lakes and rivers are fresh water."),
          ("How can kids model land and water?", "Draw a map with a key, or build a model with clay and water in a pan.")],
         sets)


if __name__ == "__main__":
    main()
