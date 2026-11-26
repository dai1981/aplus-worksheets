# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Choosing the Best Material (2-PS1-2)
  python tools/gen_us_science_g2_choosing_materials.py
Analyze data obtained from testing different materials to determine which materials have the properties that are
best suited for an intended purpose. Match a job to a property, read simple test results (pennies held, water soaked up,
minutes an ice cube lasted, how far a ball bounced).
Wrong answers come from real mistakes: "pick the prettiest material", "pick the biggest number even when smaller is better".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, bar_chart, People
import sci_kids as K

U = Unit(20102)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# job, best material, why, wrong materials, picture
JOBS = [("a raincoat", "plastic", "it keeps water out and bends", ["paper", "cotton cloth", "wood"], "rain"),
        ("a window", "glass", "you can see through it", ["wood", "metal", "cardboard"], "glass"),
        ("a cooking pot", "metal", "it is strong and does not burn or melt on the stove", ["plastic", "paper", "wax"], "hot"),
        ("a pillow", "soft cloth", "it is soft", ["rock", "metal", "glass"], None),
        ("a towel", "cotton cloth", "it soaks up water", ["plastic", "glass", "metal"], "drop"),
        ("a boat", "wood", "it floats", ["rock", "paper", "clay"], "block"),
        ("a bouncy ball", "rubber", "it bounces and bends", ["glass", "wood", "rock"], "ball"),
        ("a winter hat", "wool", "it is soft and keeps you warm", ["metal", "glass", "plastic wrap"], "snow"),
        ("a wall for a house", "brick", "it is hard and strong", ["paper", "cloth", "ice"], "house"),
        ("a mirror", "shiny glass", "it is smooth and shiny so it reflects", ["wood", "cloth", "rock"], "mirror"),
        ("a sun hat", "straw", "it is light and blocks the sun", ["metal", "glass", "rock"], "hat"),
        ("a fence post", "wood", "it is hard and strong", ["paper", "cloth", "ice"], None),
        ("a garden hose", "rubber", "it bends and keeps water in", ["glass", "paper", "wood"], "drop"),
        ("a lunch bag you can use again", "cloth", "it is strong and bends", ["glass", "ice", "rock"], "apple"),
        ("an umbrella", "waterproof nylon cloth", "it keeps rain off and folds up", ["paper", "cotton balls", "wood"], "umbrella"),
        ("a spoon for hot soup", "metal", "it does not melt or bend in hot soup", ["wax", "paper", "ice"], "spoon")]


def g_job():
    job, best, why, wrong, pic = R.choice(JOBS)
    who = P.next()[0]
    fg = fig(K.card(pic)) if pic else ""
    t = R.random() < 0.6
    if not once((job, t)):
        return None
    if t:
        return item(fg + "%s wants to make %s. Which material is best?" % (who, job), best, wrong, "%s is best because %s." % (best[0].upper() + best[1:], why))
    others = [j[2] for j in JOBS if j[2] != why and j[1] != best]
    return item(fg + "%s makes %s out of %s. Why is %s a good choice?" % (who, job, best, best), "Because " + why + ".",
                ["Because " + x + "." for x in R.sample(others, 2)] + ["Because it is the prettiest color."], "Choose a material by its properties, not its color.")


TESTS = [("pennies a paper bridge held", "the strongest", True, "paper bridge", [("copy paper", 4), ("cardboard", 20), ("tissue paper", 1), ("folded paper", 12)]),
         ("spoonfuls of water each towel soaked up", "soaks up the most water", True, "towel", [("paper towel", 6), ("cotton towel", 10), ("plastic wrap", 0), ("wax paper", 1)]),
         ("minutes an ice cube stayed frozen in each cup", "keeps ice cold the longest", True, "cup", [("foam cup", 40), ("metal cup", 15), ("glass cup", 20), ("paper cup", 25)]),
         ("drops of water that leaked through", "keeps water out best", False, "roof", [("cloth", 9), ("plastic", 0), ("paper", 12), ("felt", 7)]),
         ("centimeters a ball bounced", "is the bounciest", True, "ball", [("rubber", 60), ("wood", 15), ("clay", 2), ("cork", 25)]),
         ("minutes it took to dry", "dries the fastest", False, "shirt", [("thin cotton", 30), ("thick wool", 90), ("polyester", 20), ("denim", 70)])]


def g_test():
    what, goal, bigger, thing, rows = R.choice(TESTS)
    who = P.next()[0]
    sc = R.choice([1, 2]) if "pennies" in what or "spoonfuls" in what else 1
    rows = [(m, v * sc) for m, v in rows]
    k = R.choice(["best", "worst", "diff", "diff"])
    if k != "diff" and not once((what, sc, k)):
        return None
    tab = table(["Material", what[0].upper() + what[1:]], [[m, str(v)] for m, v in rows])
    key = (lambda r: r[1]) if bigger else (lambda r: -r[1])
    best = max(rows, key=key)
    worst = min(rows, key=key)
    if k == "best":
        return item(tab + "%s tested materials for a %s. Which material %s?" % (who, thing, goal), best[0], [r[0] for r in rows if r != best],
                    "Look for the %s number: %s %s." % ("biggest" if bigger else "smallest", best[0], best[1]))
    if k == "worst":
        return item(tab + "%s tested materials for a %s. Which material would be the worst choice?" % (who, thing), worst[0], [r[0] for r in rows if r != worst],
                    "The %s number is the worst result here: %s %s." % ("smallest" if bigger else "biggest", worst[0], worst[1]))
    a, b = sorted(R.sample(rows, 2), key=lambda r: -r[1])
    if a[1] == b[1] or not once((what, sc, a[0], b[0])):
        return None
    d = a[1] - b[1]
    unit = what.split(" ")[0]
    return item(tab + "Look at %s's test. How many more %s for %s than for %s?" % (who, unit, a[0], b[0]), str(d), [str(a[1]), str(a[1] + b[1]), str(d + 1)], "%d − %d = %d." % (a[1], b[1], d))


def g_graph():
    who = P.next()[0]
    good = R.choice(["plastic", "foil"])
    low = R.sample(["paper", "cloth", "felt", "paper towel"], 2)
    mats = [good, "wax paper"] + low
    vals = [R.randint(10, 12), R.randint(6, 8)] + R.sample(range(1, 5), 2)
    z = list(zip(mats, vals))
    R.shuffle(z)
    mats, vals = [a for a, _ in z], [b for _, b in z]
    if not once(("gr", tuple(mats), tuple(vals))):
        return None
    if R.random() < 0.4:
        ch = bar_chart(mats, vals, "drops held", "bar graph of how many drops of water each material held before leaking", ymax=12, step=2, w=300)
        worst = mats[vals.index(min(vals))]
        return item(fig(ch) + "%s tested how many water drops each material held before leaking. Which material leaked first?" % who, worst,
                    [m for m in mats if m != worst], "The shortest bar held the fewest drops: %s." % worst)
    ch = bar_chart(mats, vals, "drops held", "bar graph of how many drops of water each material held before leaking", ymax=12, step=2, w=300)
    best = mats[vals.index(max(vals))]
    return item(fig(ch) + "%s tested which material holds the most water drops before leaking. Which material should %s use for a cup?" % (who, who), best,
                [m for m in mats if m != best], "The tallest bar held the most drops: %s." % best)


B1 = bank([
    ("Why do we test materials?", "to find out which one works best for a job", ["to make them a new color", "to break all of them", "to make them heavier"], "Testing gives us data."),
    ("A coat should keep rain out. Which property matters most?", "waterproof", ["shiny", "pretty color", "heavy"], "Keep water out."),
    ("A towel should dry you. Which property matters most?", "soaks up water", ["waterproof", "see-through", "hard"], "It must soak up water."),
    ("Which material is best for a window?", "glass", ["wood", "brick", "metal"], "Glass is see-through."),
    ("A bridge must hold heavy trucks. Which property matters most?", "strong", ["soft", "see-through", "bendy"], "Strong materials hold weight."),
    ("Why are tires made of rubber?", "Rubber bends and grips the road.", ["Rubber is see-through.", "Rubber soaks up water.", "Rubber melts in the sun."], "Bends and grips."),
    ("Which is a fair test of paper towels?", "Use the same amount of water for each towel.", ["Use more water for one towel.", "Test only one towel.", "Guess which is best."], "Keep things the same."),
    ("What is data?", "information we collect, like numbers from a test", ["a kind of material", "a tool for cutting", "a type of weather"], "Data helps us decide."),
])
B5 = bank([
    ("Ava's paper bridge held 4 pennies. Her cardboard bridge held 20. Which is stronger?", "the cardboard bridge", ["the paper bridge", "they are the same", "neither held pennies"], "20 is more than 4."),
    ("Leo wants a cup that keeps cocoa hot. A foam cup stayed hot 30 minutes, a metal cup 10 minutes. Which should he use?", "the foam cup", ["the metal cup", "either one is the same", "a paper bag"], "Longer is better here."),
    ("Mia's shirt test: cotton dried in 30 minutes, wool in 90. Which dried faster?", "cotton", ["wool", "they dried at the same time", "neither dried"], "Fewer minutes means faster."),
    ("A roof test: plastic leaked 0 drops, cloth leaked 9. Which is best for a roof?", "plastic", ["cloth", "both are the same", "neither"], "0 drops leaked."),
    ("Why should Kai test each material the same way?", "so the test is fair", ["so it takes longer", "so one material wins", "so he can skip some"], "A fair test compares fairly."),
])


def body():
    pic = K.row(["umbrella", "drop", "house", "ball"], words=["keeps rain out", "soaks up water", "strong", "bouncy"], size=95)
    ex = [("Best material for a raincoat: paper, cloth or plastic?", ["A raincoat must keep water out."], "plastic"),
          ("Bridge test: paper held 4 pennies, cardboard held 20. Strongest?", ["Bigger number = held more."], "cardboard")]
    mist = ["Choosing a material because of its color.",
            "Always picking the biggest number. Sometimes smaller is better, like fewer drops leaking.",
            "Testing materials in different ways, so the test is not fair."]
    return kid_lesson(pic, "Pick the material whose properties fit the job.",
                      ["Think: what must it do?", "Test the materials the same way.", "Use the data to choose."], ex, mist)


def main():
    sets = U.sets([
        ("Matching materials to jobs", B1 + [(g_job, 12)]),
        ("Why this material?", [(g_job, 16), (g_graph, 4)]),
        ("Reading test results", [(g_test, 16), (g_graph, 4)]),
        ("Comparing data", [(g_test, 14), (g_job, 4), (g_graph, 2)]),
        ("Engineer choices", B5 + [(g_test, 8), (g_job, 4), (g_graph, 3)]),
    ])
    make("grade-2", "choosing-materials", 2, "2-PS1-2",
         "Analyze data obtained from testing different materials to determine which materials have the properties that are best suited for an intended purpose.",
         "Choosing the Best Material",
         "Grade 2 Choosing Materials Worksheets: Test Materials and Pick the Best",
         "Choosing Materials",
         "Free grade 2 science worksheets on choosing materials (NGSS 2-PS1-2): match materials to jobs, read simple test results and pick the best material. 100 picture questions with answers.",
         "Match the material to the job.",
         "Test materials, then use the data to pick the best one.",
         body(),
         [("How do you choose the best material?", "Think about what the object must do, test the materials the same way, and pick the one with the best results."),
          ("Why is a fair test important?", "If every material is tested the same way, you can trust the results."),
          ("Is a bigger number always better?", "No. For leaks or drying time, a smaller number is better.")],
         sets)


if __name__ == "__main__":
    main()
