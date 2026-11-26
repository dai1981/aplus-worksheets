# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Habitats and Biodiversity (2-LS4-1)
  python tools/gen_us_science_g2_habitats_and_biodiversity.py
Make observations of plants and animals to compare the diversity of life in different habitats.
Count kinds (not individuals) of living things in pictures, compare habitats with tally tables and bar graphs,
and match plants and animals to the habitat where they can live.
Wrong answers come from real mistakes: "count every animal instead of every kind", "more animals means more kinds",
"a fish can live in a desert".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, bar_chart, svg_wrap, People
from ws_common import text
import sci_kids as K

U = Unit(20107)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


BG = {"pond": ("#e6f3fc", "#cfe7b8"), "forest": ("#e6f3fc", "#b8d99a"), "meadow": ("#e6f3fc", "#d7ecbf")}
LIVES = {"pond": ["fish", "duck", "frog"], "forest": ["squirrel", "bird", "bear", "bug", "rabbit"],
         "meadow": ["bee", "butterfly", "rabbit", "bird", "bug"]}


def habitat_svg(where, counts, w=400, h=200, label=None):
    """counts: [(kind, n)] placed on a grid over a simple picture of the habitat"""
    sky, gr = BG[where]
    s = "<rect x='0' y='0' width='%d' height='%d' fill='%s'/>" % (w, h, sky)
    s += "<rect x='0' y='48' width='%d' height='%d' fill='%s'/>" % (w, h - 48, gr)
    if where == "pond":
        s += "<ellipse cx='%d' cy='%d' rx='%d' ry='%d' fill='#9fd0f0' stroke='#5aa6d6' stroke-width='2'/>" % (w / 2, h / 2 + 30, w / 2 - 14, h / 2 - 34)
    if where == "forest":
        for x in range(28, w, 62):
            s += "<g opacity='0.45'>%s</g>" % K.icon("tree", x, 34, 0.55)
    if where == "meadow":
        for x in range(20, w, 44):
            s += "<g opacity='0.6'>%s</g>" % K.icon("flower", x, 52, 0.3)
    cols = 5
    cells = [(44 + c * (w - 88) / (cols - 1), 92 + r * 52) for r in range(2) for c in range(cols)] + [(44 + c * (w - 88) / (cols - 1), 40) for c in range(cols)]
    things = [k for k, n in counts for _ in range(n)]
    R.shuffle(things)
    for (x, y), k in zip(cells, things):
        s += K.icon(k, x + R.randint(-5, 5), y + R.randint(-3, 3), 0.62)
    lab = label or "a %s with %s" % (where, ", ".join("%d %s" % (n, K.name(k) + ("" if n == 1 else "s")) for k, n in counts))
    return svg_wrap(w, h, s, lab)


ANIM = {"fish", "duck", "frog", "bug", "squirrel", "bird", "bear", "rabbit", "bee", "butterfly"}


def g_kinds():
    where = R.choice(sorted(BG))
    pool = [k for k in LIVES[where] if k in ANIM]
    m = R.randint(2, min(4, len(pool)))
    kinds = R.sample(pool, m)
    counts = [(k, R.randint(1, 4)) for k in kinds]
    total = sum(n for _, n in counts)
    if total > 10 or total == m or not once(("k", where, m, total)):
        return None
    who = P.next()[0]
    pic = fig(habitat_svg(where, counts))
    if R.random() < 0.6:
        return item(pic + "%s looks at a %s. How many different kinds of animals are there?" % (who, where), str(m), [str(x) for x in list(dict.fromkeys([total, m + 1, m - 1 if m > 2 else m + 2, m + 2, m + 3])) if x != m][:3],
                    "Count kinds, not animals: %s." % ", ".join(K.name(k) for k in kinds))
    return item(pic + "%s counts every animal %s the %s, one by one. How many animals are there in all?" % (who, "at" if where == "pond" else "in", where), str(total), [str(x) for x in list(dict.fromkeys([m, total + 1, total - 1, total + 2])) if x != total][:3],
                "Add them up: %s = %d." % (" + ".join(str(n) for _, n in counts), total))


def g_compare():
    a, b = R.sample(sorted(BG), 2)
    pa = [k for k in LIVES[a] if k in ANIM]
    pb = [k for k in LIVES[b] if k in ANIM]
    ma, mb = R.randint(1, len(pa)), R.randint(1, len(pb))
    if ma == mb or ma > 4 or mb > 4 :
        return None
    ka, kb = R.sample(pa, ma), R.sample(pb, mb)
    ca = [(k, R.randint(1, 3)) for k in ka]
    cb = [(k, R.randint(1, 3)) for k in kb]
    ta, tb = sum(n for _, n in ca), sum(n for _, n in cb)
    if ta > 10 or tb > 10 or not once(("c", a, b, ma, mb)):
        return None
    pic = habitat_svg(a, ca, 300, 170) + habitat_svg(b, cb, 300, 170)
    more = "A" if ma > mb else "B"
    who = P.next()[0]
    return item(fig(pic) + "%s compares habitat A (a %s) and habitat B (a %s). Which has more kinds of animals?" % (who, a, b), "habitat %s" % more,
                ["habitat %s" % ("B" if more == "A" else "A"), "They have the same number of kinds.", "Neither has animals."],
                "A has %d kinds; B has %d kinds." % (ma, mb))


PLACES = [("a pond", 6, 9), ("a forest", 7, 11), ("a parking lot", 1, 3), ("a meadow", 6, 10), ("a sandy desert", 2, 5), ("a school yard", 3, 5), ("a tide pool", 5, 8)]


def g_data():
    who = P.next()[0]
    rows = R.sample(PLACES, 3)
    vals = [R.randint(lo, hi) for _, lo, hi in rows]
    names = [r[0] for r in rows]
    if len(set(vals)) < 3:
        return None
    k = R.choice(["most", "least", "diff", "graph", "graph"])
    if not once(("d", tuple(names), k)) or (k == "graph" and not once("gr", 8)):
        return None
    if k == "graph":
        short = [n.replace("a ", "").replace("sandy ", "") for n in names]
        ch = bar_chart(short, vals, "kinds of living things", "bar graph of how many kinds of living things %s found in each place" % who, ymax=12, step=2, w=330)
        a = short[vals.index(max(vals))]
        return item(fig(ch) + "%s counted kinds of plants and animals in 3 places. Which place had the most kinds?" % who, a, [x for x in short if x != a] + ["They all had the same."],
                    "The tallest bar: %s." % a)
    tab = table(["Place", "Kinds of plants and animals"], [[n, str(v)] for n, v in zip(names, vals)])
    if k == "most":
        a = names[vals.index(max(vals))]
        return item(tab + "Which place in %s's table has the most kinds of living things?" % who, a, [n for n in names if n != a] + ["They are all the same."], "Biggest number: %d." % max(vals))
    if k == "least":
        a = names[vals.index(min(vals))]
        return item(tab + "Which place in %s's table has the fewest kinds of living things?" % who, a, [n for n in names if n != a] + ["They are all the same."], "Smallest number: %d." % min(vals))
    x, y = sorted(R.sample(list(zip(names, vals)), 2), key=lambda t: -t[1])
    d = x[1] - y[1]
    return item(tab + "In %s's table, how many more kinds were found in %s than in %s?" % (who, x[0], y[0]), str(d), [str(x[1]), str(x[1] + y[1]), str(d + 1)], "%d − %d = %d." % (x[1], y[1], d))


HOME = [("fish", "a pond", "It needs water to breathe."), ("duck", "a pond", "It swims and finds food in water."), ("frog", "a pond", "It lays eggs in water."),
        ("cactus", "a desert", "It stores water for dry times."), ("squirrel", "a forest", "It needs trees for nuts and nests."), ("bear", "a forest", "It finds food and shelter in the woods."),
        ("bee", "a meadow", "It needs flowers for nectar."), ("butterfly", "a meadow", "It drinks nectar from flowers."), ("tree", "a forest", "Many trees grow together in a forest.")]
HABS = ["a pond", "a desert", "a forest", "a meadow"]


def g_home():
    k, where, why = R.choice(HOME)
    who = P.next()[0]
    t = R.random() < 0.6
    if not once(("h", k, t)):
        return None
    if t:
        return item(fig(K.card(k)) + "%s finds a %s. Which habitat is the best home for it?" % (who, K.name(k)), where, [h for h in HABS if h != where],
                    why)
    if k == "tree":
        return None
    return item(fig(K.card(k)) + "Why does a %s live in %s, as %s learned?" % (K.name(k), where, who), why, R.sample([x[2] for x in HOME if x[2] != why and x[1] != where], 3), "Living things live where they can get what they need.")


TEXT = [("A camel", "a desert", ["an ocean", "a pond", "the Arctic"]), ("A polar bear", "the Arctic", ["a desert", "a rain forest", "a pond"]),
        ("A whale", "the ocean", ["a desert", "a forest", "a meadow"]), ("A monkey", "a rain forest", ["the Arctic", "a desert", "the ocean"]),
        ("A starfish", "the ocean", ["a desert", "a forest", "the Arctic"]), ("A penguin", "the icy Antarctic", ["a desert", "a rain forest", "a meadow"]),
        ("A lizard", "a desert", ["the ocean", "the Arctic", "a pond"]), ("A deer", "a forest", ["the ocean", "the Arctic", "a pond"])]


def g_text():
    a, h, w = R.choice(TEXT)
    who = P.next()[0]
    if not once(("t", a)):
        return None
    return item("%s reads about %s. Where does it live?" % (who, a.lower()), h, w, "%s gets what it needs in %s." % (a, h))


B1 = bank([
    ("What is a habitat?", "the place where a plant or animal lives", ["a kind of food", "a type of weather", "a baby animal"], "It gives food, water and shelter."),
    ("What does a habitat give an animal?", "food, water and shelter", ["toys", "money", "only sunshine"], "Living things need these."),
    ("What does 'kinds of animals' mean?", "different types, like ducks and frogs", ["how many animals in all", "how big the animals are", "the animals' colors"], "Count types, not each animal."),
    ("Which habitat usually has more kinds of living things?", "a forest", ["a parking lot", "a sidewalk", "an empty room"], "Forests have many plants and animals."),
    ("Which animal lives in water?", "a fish", ["a squirrel", "a camel", "a rabbit"], "Fish need water."),
    ("Where would you find a cactus?", "in a desert", ["in a pond", "in the ocean", "in the Arctic"], "Cactuses store water."),
    ("How can you learn which plants and animals live in a place?", "observe and count them", ["guess", "close your eyes", "ask a rock"], "Look and record."),
    ("Why do different habitats have different animals?", "Each animal needs certain things to live.", ["Animals pick places by color.", "All animals can live anywhere.", "Habitats are all the same."], "Needs match the habitat."),
])
B5 = bank([
    ("Ava saw 10 ducks at the pond. Leo saw 2 ducks, 3 frogs and 1 fish. Who saw more kinds of animals?", "Leo", ["Ava", "They saw the same.", "Neither"], "Leo saw 3 kinds; Ava saw 1."),
    ("Mia wants to compare 2 habitats fairly. What should she do?", "Look for the same amount of time in each place.", ["Look in one place for 1 minute and the other for 1 hour.", "Only look at one place.", "Guess the numbers."], "Keep the test fair."),
    ("A tally table: forest |||| ||, parking lot ||. How many more kinds in the forest?", "5", ["7", "2", "9"], "7 − 2 = 5."),
    ("Kai sees a fish flopping on a dry sidewalk. Why is this bad for the fish?", "Fish need water to live.", ["Fish like sidewalks.", "Fish need sand.", "Fish need snow."], "Its habitat is water."),
    ("Why might a pond have more kinds of living things than a sandbox?", "A pond has water, plants and food for many animals.", ["A pond is smaller.", "A sandbox has more water.", "Animals do not like water."], "More needs met, more kinds."),
])


def body():
    pic = habitat_svg("pond", [("fish", 3), ("duck", 2), ("frog", 1)], label="a pond with 3 fish, 2 ducks and 1 frog")
    ex = [("The pond has 3 fish, 2 ducks and 1 frog. How many kinds of animals?", ["fish, duck, frog"], "3 kinds"),
          ("A forest has 9 kinds. A parking lot has 2. Which has more?", ["9 is more than 2."], "the forest")]
    mist = ["Counting every animal instead of every kind.",
            "Thinking more animals always means more kinds.",
            "Thinking any animal can live anywhere."]
    return kid_lesson(pic, "Different places have different living things.",
                      ["A habitat gives food, water and shelter.", "Count the kinds: fish, duck, frog = 3.", "Compare places to see which has more kinds."], ex, mist)


def main():
    sets = U.sets([
        ("Habitats", B1 + [(g_home, 6), (g_text, 6)]),
        ("Counting kinds", [(g_kinds, 14), (g_home, 6)]),
        ("Who lives where?", [(g_home, 6), (g_text, 2), (g_kinds, 6), (g_compare, 6)]),
        ("Comparing habitats", [(g_compare, 10), (g_data, 10)]),
        ("Habitat scientists", B5 + [(g_data, 10), (g_compare, 5)]),
    ])
    make("grade-2", "habitats-and-biodiversity", 7, "2-LS4-1",
         "Make observations of plants and animals to compare the diversity of life in different habitats.",
         "Habitats and Living Things",
         "Grade 2 Habitats Worksheets: Compare the Living Things in Different Places",
         "Habitats",
         "Free grade 2 science worksheets on habitats and biodiversity (NGSS 2-LS4-1): count kinds of plants and animals, compare habitats and read simple data. 100 picture questions with answers.",
         "Different places, different life.",
         "Count the kinds of plants and animals to compare habitats.",
         body(),
         [("What is biodiversity?", "The number of different kinds of living things in a place. A forest has many kinds; a parking lot has few."),
          ("How do you compare habitats?", "Observe each place for the same time, count the kinds of plants and animals, and compare the numbers."),
          ("Kinds or animals?", "Count kinds. 5 ducks are 1 kind. 1 duck, 1 frog and 1 fish are 3 kinds.")],
         sets)


if __name__ == "__main__":
    main()
