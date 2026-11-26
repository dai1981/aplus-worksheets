# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Stopping Wind and Water Erosion (2-ESS2-1)
  python tools/gen_us_science_g2_stopping_wind_and_water_erosion.py
Compare multiple solutions designed to slow or prevent wind or water from changing the shape of the land.
Plants and roots, rows of trees (windbreaks), sand fences, rock walls, sandbags and levees; testing models
(pour water on a sand hill, blow with a fan) and comparing how much sand is lost.
Wrong answers come from real mistakes: "a bigger number of cups lost is better", "pick the prettiest solution",
"plastic sheets are always best".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, bar_chart, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(20109)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# problem, best solution, why, other (wrong) solutions
PROB = [("Wind blows sand off a beach.", "plant beach grass", "the roots hold the sand", "wind"),
        ("Wind blows soil off a big farm field.", "plant a row of trees beside the field", "the trees slow the wind", "wind"),
        ("Wind piles sand onto a beach road.", "build a sand fence", "the fence slows the wind and traps sand", "wind"),
        ("Rain washes soil down a steep hill.", "plant grass on the hill", "the roots hold the soil", "water"),
        ("A river floods and washes away its banks.", "build a levee (a high bank of soil) along the river", "it keeps the water in the river", "water"),
        ("Waves wash away a sandy beach.", "put big rocks along the shore", "the rocks take the force of the waves", "water"),
        ("Rain washes a dirt path into a ditch.", "cover the path with wood chips", "the chips slow the water", "water"),
        ("Floodwater may wash into a house.", "stack sandbags by the door", "the bags block the water", "water"),
        ("Water runs fast down a steep garden.", "build flat steps (terraces) into the hill", "flat steps slow the water", "water"),
        ("Rain washes soil off a garden bed.", "cover the soil with straw", "the straw protects the soil", "water")]
SILLY = ["paint the ground", "put up a flag", "dig more holes", "take away all the plants", "use a fan to blow harder"]


def g_problem():
    p, sol, why, kind = R.choice(PROB)
    who = P.next()[0]
    t = R.random() < 0.6
    if not once((p, t)):
        return None
    if t:
        other = [x[1] for x in PROB if x[3] != kind]
        return item("%s sees a problem: %s What is a good solution?" % (who, p), sol, R.sample(other, 1) + R.sample(SILLY, 2), "%s: %s." % (sol[0].upper() + sol[1:], why))
    whys = sorted({x[2] for x in PROB if x[2] != why})
    return item("The problem: %s %s's plan: %s. How does this help?" % (p, who, sol), "It helps because " + why + ".", ["It helps because " + w + "." for w in R.sample(whys, 2)] + ["It makes the place look nice."],
                "Solutions slow wind or water.")


def g_cause():
    p, sol, why, kind = R.choice(PROB)
    who = P.next()[0]
    if not once(("c", p)):
        return None
    return item("%s reads: “%s” What is changing the land here?" % (who, p), kind, ["water" if kind == "wind" else "wind", "sunlight", "animals"], "This change is caused by %s." % kind)


COVERS = [("no cover (bare sand)", 8, 12), ("grass with roots", 1, 3), ("rocks", 2, 4), ("straw", 3, 5), ("craft sticks", 5, 7)]


def g_test():
    who = P.next()[0]
    rows = R.sample(COVERS, 4)
    if not any(r[0].startswith("no cover") for r in rows):
        rows[R.randrange(4)] = COVERS[0]
    vals = [R.randint(lo, hi) for _, lo, hi in rows]
    names = [r[0] for r in rows]
    if len(set(vals)) < 4 or len(set(names)) < 4:
        return None
    k = R.choice(["best", "worst", "diff", "diff", "graph"])
    if not once(("t", tuple(names), k)) or not once(("tk", k), 10):
        return None
    if k == "graph":
        short = [{"no cover (bare sand)": "bare", "grass with roots": "grass", "craft sticks": "sticks"}.get(n, n) for n in names]
        ch = bar_chart(short, vals, "spoons of sand washed away", "bar graph of sand washed away from model hills", ymax=12, step=2, w=330)
        a = short[vals.index(min(vals))]
        return item(fig(ch) + "%s poured the same water on 4 model sand hills. Which cover kept the most sand in place?" % who, a, [x for x in short if x != a],
                    "The shortest bar lost the least sand: %s." % a)
    tab = table(["Cover on the sand hill", "Spoons of sand washed away"], [[n, str(v)] for n, v in zip(names, vals)])
    if k == "best":
        a = names[vals.index(min(vals))]
        return item(tab + "%s poured the same water on each hill. Which cover worked best?" % who, a, [n for n in names if n != a], "Least sand washed away = best: %d spoons." % min(vals))
    if k == "worst":
        a = names[vals.index(max(vals))]
        return item(tab + "%s poured the same water on each hill. Which cover worked worst?" % who, a, [n for n in names if n != a], "Most sand washed away = worst: %d spoons." % max(vals))
    x, y = sorted(R.sample(list(zip(names, vals)), 2), key=lambda t: -t[1])
    d = x[1] - y[1]
    if d == 0:
        return None
    return item(tab + "In %s's test, how many more spoons of sand washed away with %s than with %s?" % (who, x[0], y[0]), str(d), [str(x[1]), str(x[1] + y[1]), str(d + 1)], "%d − %d = %d." % (x[1], y[1], d))


def hill(x, cover, k=1.0):
    s = "<path d='M%g %g Q%g %g %g %g Z' fill='#e3c58f' stroke='%s' stroke-width='2'/>" % (x - 80 * k, 120, x, 20, x + 80 * k, 120, INK)

    def top(t):
        return x - 80 * k + 160 * k * t, 120 * (1 - t) ** 2 + 40 * t * (1 - t) + 120 * t * t

    if cover == "grass":
        for i in range(1, 12):
            gx, gy = top(i / 12)
            s += "<path d='M%g %g l-4 -9 M%g %g l0 -11 M%g %g l4 -9' stroke='#3f8f3f' stroke-width='2' fill='none'/>" % (gx, gy, gx, gy, gx, gy)
    if cover == "rocks":
        for i in range(1, 8):
            gx, gy = top(i / 8)
            s += "<ellipse cx='%g' cy='%g' rx='8' ry='5.5' fill='#9a9a9a' stroke='%s' stroke-width='1.2'/>" % (gx, gy - 2, INK)
    for i in range(5):
        s += "<line x1='%g' y1='%g' x2='%g' y2='%g' stroke='#5aa6d6' stroke-width='2'/>" % (x - 40 + i * 20, 22, x - 46 + i * 20, 34)
    return s


def g_pic():
    who = P.next()[0]
    a, b = R.sample(["bare", R.choice(["grass", "rocks"])], 2)
    lab = {"bare": "bare sand", "grass": "grass", "rocks": "rocks"}
    pic = svg_wrap(400, 150, hill(100, a) + hill(300, b) + text(100, 142, "A: " + lab[a], 14) + text(300, 142, "B: " + lab[b], 14),
                   "two model hills in the rain: A with %s, B with %s" % (lab[a], lab[b]))
    order = {"bare": 0, "rocks": 1, "grass": 2}
    lose = "A" if order[a] < order[b] else "B"
    q = R.choice(["more", "less"])
    if not once(("p", a, b, q)):
        return None
    ans = lose if q == "more" else ("B" if lose == "A" else "A")
    return item(fig(pic) + "%s makes it rain on two model hills. Which hill will lose %s sand?" % (who, q), "hill " + ans, ["hill " + ("B" if ans == "A" else "A"), "Both lose the same.", "Neither loses any."],
                "Bare sand has nothing to protect it, so it washes away most.")


SOL = [("a stone wall", "very well", "a lot of money", "1 week"), ("grass", "well", "a little money", "a few months to grow"),
       ("sandbags", "well", "a little money", "1 day"), ("a row of trees", "very well", "a little money", "many years to grow"),
       ("a sand fence", "well", "a little money", "1 day")]


def g_choose():
    who = P.next()[0]
    a, b = R.sample(SOL, 2)
    need = R.choice(["fast", "cheap"])
    if need == "fast":
        fa = "day" in a[3] or "week" in a[3]
        fb = "day" in b[3] or "week" in b[3]
        if fa == fb or not once(("ch", a[0], b[0], need)):
            return None
        ans = a if fa else b
        oth = b if fa else a
        return item("%s's town needs to stop erosion <b>this week</b>. Choice 1: %s (%s). Choice 2: %s (%s). Which should they pick?" % (who, a[0], a[3].replace("1 day", "ready in 1 day").replace("1 week", "ready in 1 week"), b[0], b[3].replace("1 day", "ready in 1 day").replace("1 week", "ready in 1 week")),
                    ans[0], [oth[0], "Do nothing.", "Pick the prettier one."], "%s can be ready this week." % (ans[0][0].upper() + ans[0][1:]))
    ca, cb = a[2] == "a little money", b[2] == "a little money"
    if ca == cb or not once(("ch", a[0], b[0], need)):
        return None
    ans = a if ca else b
    oth = b if ca else a
    return item("%s's school has only a little money to stop soil washing away. Choice 1: %s (costs %s). Choice 2: %s (costs %s). Which is the better choice?" % (who, a[0], a[2], b[0], b[2]),
                ans[0], [oth[0], "Do nothing.", "Pick the biggest one."], "%s costs less." % (ans[0][0].upper() + ans[0][1:]))


B1 = bank([
    ("What is erosion?", "wind or water moving soil, sand or rock to a new place", ["plants growing", "snow melting", "rocks getting bigger"], "Erosion changes the shape of land."),
    ("How do plant roots help stop erosion?", "They hold the soil in place.", ["They make the soil wet.", "They push the soil away.", "They eat the soil."], "Roots grip the soil."),
    ("What can slow down strong wind on a farm?", "a row of trees", ["a puddle", "a bare field", "a hole"], "Trees block wind."),
    ("What is a levee?", "a high bank that keeps a river from flooding", ["a kind of boat", "a type of fish", "a bridge"], "It holds water in."),
    ("Why do people put sandbags by doors in a flood?", "to block the water", ["to make the water warmer", "to feed fish", "to make it dry faster"], "Sandbags stop water."),
    ("Which land will erode the most in heavy rain?", "a bare hill with no plants", ["a hill covered in grass", "a hill with rocks on it", "a flat field with grass"], "Nothing holds bare soil."),
    ("Why do we test more than one solution?", "to find out which one works best", ["to waste water", "to make a mess", "because one is always enough"], "Compare solutions."),
    ("What does a sand fence do on a beach?", "It slows the wind so sand stays.", ["It makes waves bigger.", "It heats the sand.", "It keeps fish in."], "Slower wind drops sand."),
])
B5 = bank([
    ("Ava's bare hill lost 10 spoons of sand. Her grass hill lost 2. Which solution worked better?", "grass", ["bare sand", "they worked the same", "neither"], "2 is less than 10."),
    ("Leo used more water on one hill than the other. What is wrong with his test?", "It is not fair; use the same water.", ["Nothing is wrong.", "He needs more sand.", "He should use juice."], "Change only the cover."),
    ("Mia's rocks lost 3 spoons and her straw lost 5. How many fewer did the rocks lose?", "2", ["8", "3", "5"], "5 − 3 = 2."),
    ("A town picks trees to block wind. What is a downside?", "Trees take many years to grow.", ["Trees cost nothing at all.", "Trees make the wind stronger.", "Trees wash away."], "Every solution has trade-offs."),
    ("Kai wants to stop wind from blowing a sandbox. Which is a good, cheap idea?", "put up a small fence or cover", ["blow on it with a fan", "pour water and leave", "take out all the sand"], "Slow the wind."),
])


def body():
    pic = svg_wrap(400, 150, hill(100, "bare") + hill(300, "grass") + text(100, 142, "bare: loses sand", 14) + text(300, 142, "grass: holds sand", 14),
                   "a bare hill and a grassy hill in the rain")
    ex = [("Rain washes soil off a hill. What can help?", ["Roots hold soil."], "plant grass"),
          ("Test: bare hill lost 9 spoons, rocks lost 3. Which works better?", ["Less sand lost is better."], "rocks")]
    mist = ["Picking the bigger number. Less sand lost is better.",
            "Testing hills with different amounts of water.",
            "Forgetting cost and time. Some solutions take years."]
    return kid_lesson(pic, "We can slow down wind and water.",
                      ["Plants and trees: roots hold soil, trees block wind.", "Walls, fences, rocks and sandbags.", "Test solutions and compare."], ex, mist)


def main():
    sets = U.sets([
        ("Wind and water", B1 + [(g_cause, 6), (g_problem, 6)]),
        ("Choosing a solution", [(g_problem, 10), (g_pic, 4), (g_cause, 4)]),
        ("Model hills", [(g_test, 14), (g_pic, 2), (g_problem, 4)]),
        ("Comparing solutions", [(g_test, 10), (g_choose, 8), (g_pic, 2)]),
        ("Erosion engineers", B5 + [(g_test, 6), (g_choose, 4)]),
    ])
    make("grade-2", "stopping-wind-and-water-erosion", 9, "2-ESS2-1",
         "Compare multiple solutions designed to slow or prevent wind or water from changing the shape of the land.",
         "Stopping Wind and Water Erosion",
         "Grade 2 Erosion Worksheets: Compare Ways to Stop Wind and Water Changing the Land",
         "Stopping Erosion",
         "Free grade 2 science worksheets on stopping erosion (NGSS 2-ESS2-1): plants, fences, walls and sandbags, model hill tests and comparing solutions. 100 questions with answers.",
         "Slow the wind. Slow the water.",
         "Plants, fences and walls help. Test them to find the best.",
         body(),
         [("What is erosion?", "Wind or water moving soil, sand or rock away, changing the shape of the land."),
          ("How can we stop erosion?", "Plant grass and trees, build fences, walls and levees, put down rocks or sandbags."),
          ("How do kids test solutions?", "Build small sand hills, cover each one differently, pour the same water on each and measure the sand that washes away.")],
         sets)


if __name__ == "__main__":
    main()
