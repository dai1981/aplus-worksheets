# -*- coding: utf-8 -*-
"""
US Kindergarten Science: Where Plants and Animals Live (K-ESS3-1)
  python tools/gen_us_science_gk_where_plants_and_animals_live.py
Use a model to represent the relationship between the needs of different plants and animals (including humans) and the
places they live. Fish need water, so they live in ponds; deer eat leaves, so they live in forests; cactuses need little
water, so they grow in deserts; people build homes near food and water.
Very short sentences for 5-6 year olds; almost every question has a picture.
Wrong answers come from real mistakes: "a fish can live in a tree", "animals live anywhere", "plants live where it is dark".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(9108)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ZONES = {"pond": ("#9fd0f0", "water"), "forest": ("#b8d99a", "trees"), "desert": ("#ecd29a", "sand"), "meadow": ("#d7ecbf", "grass and flowers")}
LIVE = {"fish": ("pond", "it needs water to live"), "duck": ("pond", "it swims and finds food in water"), "frog": ("pond", "it lays eggs in water"),
        "squirrel": ("forest", "it eats nuts and lives in trees"), "bear": ("forest", "it finds food and a den in the woods"), "bird": ("forest", "it builds nests in trees"),
        "bee": ("meadow", "it needs flowers"), "butterfly": ("meadow", "it drinks nectar from flowers"), "rabbit": ("meadow", "it eats grass"),
        "cactus": ("desert", "it needs only a little water"), "tree": ("forest", "it grows with many other trees"), "flower": ("meadow", "it needs lots of sun")}


def zones_svg(order):
    s = ""
    for i, z in enumerate(order):
        x = i * 120
        col, _ = ZONES[z]
        s += "<rect x='%d' y='0' width='116' height='110' fill='%s' stroke='%s' stroke-width='1.4'/>" % (x, col, INK)
        deco = {"pond": "<ellipse cx='%d' cy='60' rx='40' ry='18' fill='#5aa6d6' opacity='0.5'/>" % (x + 58),
                "forest": K.icon("tree", x + 40, 52, 0.45) + K.icon("tree", x + 80, 58, 0.45),
                "desert": K.icon("cactus", x + 58, 60, 0.45),
                "meadow": K.icon("flower", x + 36, 72, 0.35) + K.icon("flower", x + 80, 66, 0.35)}[z]
        s += deco + text(x + 58, 130, "%s: %s" % ("ABCD"[i], z), 13)
    return svg_wrap(120 * len(order), 140, s, "a model with places: " + ", ".join("%s %s" % ("ABCD"[i], z) for i, z in enumerate(order)))


def g_model():
    k = R.choice(sorted(LIVE))
    place = LIVE[k][0]
    order = R.sample(sorted(ZONES), 3)
    if place not in order:
        order[R.randrange(3)] = place
    if len(set(order)) < 3 or not once((k, tuple(order))) or not once(("m", k), 3):
        return None
    who = P.next()[0]
    i = order.index(place)
    pic = fig(K.card(k)) + fig(zones_svg(order))
    return item(pic + "%s is making a model. Where should the %s go?" % (who, K.name(k)), "%s (%s)" % ("ABC"[i], place), ["%s (%s)" % ("ABC"[j], z) for j, z in enumerate(order) if j != i] + ["anywhere"],
                "%s lives in a %s because %s." % ("A " + K.name(k), place, LIVE[k][1]))


def g_why():
    k = R.choice(sorted(LIVE))
    place, why = LIVE[k]
    who = P.next()[0]
    if not once(("w", k)):
        return None
    w = R.sample([LIVE[x][1] for x in LIVE if LIVE[x][0] != place], 3)
    return item(fig(K.card(k)) + "%s asks: why does a %s live in a %s?" % (who, K.name(k), place),
                "because " + why, ["because " + x for x in w], "Living things live where they get what they need.")


def g_where():
    k = R.choice(sorted(LIVE))
    place = LIVE[k][0]
    who = P.next()[0]
    if not once(("p", k)):
        return None
    return item(fig(K.card(k)) + "%s sees a %s. Where does it live?" % (who, K.name(k)), "in a " + place, ["in a " + z for z in ZONES if z != place], "A %s lives in a %s because %s." % (K.name(k), place, LIVE[k][1]))


def g_pick():
    place = R.choice(["pond", "forest", "meadow"])
    good = [k for k in LIVE if LIVE[k][0] == place and k not in ("tree", "flower")]
    a = R.choice(good)
    bad = R.sample([k for k in LIVE if LIVE[k][0] != place and k not in ("tree", "flower", "cactus") and k != "bird" and not (place in ("forest", "meadow") and k == "rabbit")], 3)
    kinds = [a] + bad
    R.shuffle(kinds)
    if not once((place, tuple(kinds))) or not once(("pk", a), 4):
        return None
    L = "ABCD"
    who = P.next()[0]
    pic = K.row(kinds, words=["%s. %s" % (L[i], K.name(k)) for i, k in enumerate(kinds)], size=90)
    return item(fig(pic) + "%s is making a %s model. Which animal belongs there?" % (who, place), "%s (%s)" % (L[kinds.index(a)], K.name(a)),
                ["%s (%s)" % (L[i], K.name(k)) for i, k in enumerate(kinds) if k != a], "A %s lives in a %s." % (K.name(a), place))


PEOPLE = [("People build towns near rivers.", "to get water"), ("Farmers live near their fields.", "to grow food"), ("People build houses with roofs.", "to stay dry and safe"),
          ("People in cold places build warm homes.", "to stay warm"), ("Fishing towns are by the sea.", "to catch fish for food"), ("People put screens on windows.", "to keep bugs out")]


def g_people():
    s, a = R.choice(PEOPLE)
    who = P.next()[0]
    if not once(s):
        return None
    return item("%s learns: %s Why?" % (who, s), a, R.sample([x[1] for x in PEOPLE if x[1] != a], 3), "People live where they can meet their needs.")


B1 = bank([
    ("Where does a fish live?", "in water", ["in a tree", "in the sand", "in the sky"], "Fish need water."),
    ("Why does a squirrel live in a forest?", "Trees give it nuts and a home.", ["It likes the sand.", "It needs to swim.", "It is cold there."], "Food and shelter."),
    ("Where does a cactus grow?", "in a desert", ["in a pond", "in the ocean", "under the snow"], "It needs little water."),
    ("Do all animals live in the same place?", "No. They live where they get what they need.", ["Yes, all in one place.", "Yes, in houses.", "Yes, in water."], "Needs match places."),
    ("What do people need from the place they live?", "food, water and shelter", ["only toys", "only TV", "only snow"], "People have needs too."),
    ("Where does a bee find food?", "in a meadow with flowers", ["in a desert with no flowers", "in the ocean", "in a cave"], "Bees need flowers."),
    ("What is a model?", "a small picture or copy that shows how something works", ["a real animal", "a type of tree", "a snack"], "Models help us explain."),
    ("Why does a duck live by a pond?", "It swims and finds food in the water.", ["It eats sand.", "It lives in trees.", "It hates water."], "Ponds meet its needs."),
])
B5 = bank([
    ("Ava puts a toy fish in the desert part of her model. What should she fix?", "move it to the water", ["keep it in the sand", "put it in a tree", "nothing"], "Fish need water."),
    ("Leo's model forest has trees and a squirrel. What else could live there?", "a bird in a nest", ["a whale", "a cactus", "a camel"], "Forests have nests."),
    ("Mia asks why there are no frogs in the desert. Why?", "Frogs need water to lay eggs.", ["Frogs love sand.", "Frogs are too big.", "Frogs live in clouds."], "Needs match places."),
    ("Kai sees deer at the edge of the woods. What are they looking for?", "leaves and grass to eat", ["sand to eat", "snow to drink", "toys"], "Deer eat plants."),
    ("Why do people build cities by rivers?", "The river gives water.", ["Rivers are loud.", "Rivers are cold.", "There is no reason."], "Water is a need."),
])


def body():
    pic = zones_svg(["pond", "forest", "desert"])
    ex = [("Where should a fish go in the model?", ["Fish need water."], "the pond"),
          ("Why does a squirrel live in a forest?", ["Trees give food and a home."], "nuts and trees")]
    mist = ["Thinking a fish can live in a tree.",
            "Thinking animals can live anywhere.",
            "Thinking plants grow well where it is dark."]
    return kid_lesson(pic, "Living things live where their needs are met.",
                      ["Fish: water. Squirrels: trees.", "Bees: flowers. Cactus: desert.", "People live near food and water."], ex, mist)


def main():
    sets = U.sets([
        ("Homes for living things", B1 + [(g_where, 6), (g_pick, 6)]),
        ("Making a model", [(g_model, 10), (g_where, 6), (g_pick, 4)]),
        ("Why do they live there?", [(g_why, 12), (g_people, 6), (g_pick, 2)]),
        ("Model builders", [(g_model, 12), (g_pick, 8)]),
        ("Habitat helpers", B5 + [(g_model, 10), (g_pick, 5)]),
    ])
    make("kindergarten", "where-plants-and-animals-live", 8, "K-ESS3-1",
         "Use a model to represent the relationship between the needs of different plants and animals (including humans) and the places they live.",
         "Where Plants and Animals Live",
         "Kindergarten Habitat Worksheets: Where Plants and Animals Live and Why",
         "Where Living Things Live",
         "Free kindergarten science worksheets on where plants and animals live (NGSS K-ESS3-1): ponds, forests, meadows and deserts, and why each living thing lives there. 100 picture questions with answers.",
         "Living things live where needs are met.",
         "Fish live in water. Squirrels live in trees.",
         body(),
         [("Why do animals live in different places?", "Each place gives them what they need: food, water and shelter."),
          ("Where do plants grow?", "Where they get the light and water they need. A cactus needs little water, so it grows in the desert."),
          ("How can kids make a model?", "Draw or build a pond, a forest and a meadow, then place each animal where it can meet its needs.")],
         sets)


if __name__ == "__main__":
    main()
