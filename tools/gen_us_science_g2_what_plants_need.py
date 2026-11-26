# -*- coding: utf-8 -*-
"""
US Grade 2 Science: What Plants Need to Grow (2-LS2-1)
  python tools/gen_us_science_g2_what_plants_need.py
Plan and conduct an investigation to determine if plants need sunlight and water to grow.
Fair tests (change one thing), reading height data, plants in the dark turn pale and weak, plants without water wilt.
Wrong answers come from real mistakes: "plants eat soil for food", "more water is always better", "change two things at once".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, bar_chart, svg_wrap, People
from ws_common import text, INK
import sci_kids as K

U = Unit(20105)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


COND = {"sun+water": ("in the sun with water", "grew tall and green"),
        "dark+water": ("in a dark closet with water", "grew pale, thin and weak"),
        "sun+dry": ("in the sun with no water", "wilted and dried up"),
        "dark+dry": ("in a dark closet with no water", "dried up and died")}


def setup_svg(conds):
    s = ""
    for i, c in enumerate(conds):
        x = 70 + i * 140
        if "sun" in c:
            s += K.icon("sun", x + 40, 26, 0.45)
        else:
            s += "<rect x='%d' y='8' width='120' height='118' fill='#3b3f4a' opacity='0.85'/>" % (x - 60)
        if "water" in c:
            s += K.icon("drop", x - 38, 34, 0.4)
        s += K.icon("plant", x, 84, 0.8)
        s += text(x, 146, "ABCD"[i], 16)
        s += text(x, 166, {"sun+water": "sun, water", "dark+water": "dark, water", "sun+dry": "sun, no water", "dark+dry": "dark, no water"}[c], 12, weight=400)
    return svg_wrap(140 * len(conds), 176, s, "plants in different places: " + "; ".join(COND[c][0] for c in conds))


def g_best():
    conds = R.sample(sorted(COND), 3)
    if "sun+water" not in conds:
        conds[R.randrange(3)] = "sun+water"
    if len(set(conds)) < 3 or not once(("b", tuple(conds))):
        return None
    who = P.next()[0]
    a = "ABCD"[conds.index("sun+water")]
    return item(fig(setup_svg(conds)) + "%s puts 3 bean plants in different places for 2 weeks. Which plant will grow best?" % who, "plant " + a,
                ["plant " + "ABCD"[i] for i, c in enumerate(conds) if c != "sun+water"] + ["They will all grow the same."], "Plants need both sunlight and water.")


def g_what():
    c = R.choice(["dark+water", "sun+dry", "dark+dry", "sun+water"])
    who = P.next()[0]
    if not once(("w", c), 2):
        return None
    where, res = COND[c]
    wrong = [COND[x][1] for x in COND if x != c]
    return item("%s keeps a plant %s for 2 weeks. What most likely happens?" % (who, where), "It " + res + ".", ["It " + w + "." for w in wrong],
                "Sunlight + water = healthy. No light = pale and weak. No water = wilted.")


def g_fair():
    who = P.next()[0]
    test = R.choice(["light", "water"])
    if not once(("f", test, who), 1) or not once(("f", test), 5):
        return None
    if test == "light":
        return item("%s wants to test if plants need light. Which is a fair test?" % who, "Two plants get the same water; one is in the sun and one is in the dark.",
                    ["One plant in the sun with water; one in the dark with no water.", "Two plants in the sun with the same water.", "Only one plant in the dark."],
                    "Change only one thing: the light.")
    return item("%s wants to test if plants need water. Which is a fair test?" % who, "Two plants in the sun; one gets water and one does not.",
                ["One plant in the sun with water; one in the dark with no water.", "Two plants in the dark with no water.", "One plant gets water and juice."],
                "Change only one thing: the water.")


def g_data():
    who = P.next()[0]
    plant = R.choice(["bean", "pea", "sunflower", "corn", "radish"])
    h = {"sun + water": R.choice([12, 14, 15, 16, 18]), "dark + water": R.choice([6, 7, 8, 9]), "sun + no water": R.choice([2, 3, 4])}
    labels = sorted(h)
    R.shuffle(labels)
    vals = [h[l] for l in labels]
    k = R.choice(["graph", "graph", "short", "diff", "diff", "conclude"])
    if not once(("d", plant, tuple(labels), tuple(vals), k)) or (k == "conclude" and not once("conc", 4)) or (k == "graph" and not once(("g", plant), 3)):
        return None
    if k == "graph":
        short = {"sun + water": "sun, water", "dark + water": "dark, water", "sun + no water": "sun, dry"}
        ch = bar_chart([short[l] for l in labels], vals, "height (cm)", "bar graph of %s plant heights after 3 weeks" % plant, ymax=21, step=3, w=360)
        a = labels[vals.index(max(vals))]
        return item(fig(ch) + "%s measured %s plants after 3 weeks (dry = no water). Which plant grew the tallest?" % (who, plant), a, [l for l in labels if l != a] + ["They are the same height."],
                    "The tallest bar: %s." % a)
    tab = table(["%s plant" % plant.capitalize(), "Height after 3 weeks"], [[l, "%d cm" % v] for l, v in zip(labels, vals)])
    if k == "short":
        a = labels[vals.index(min(vals))]
        return item(tab + "Which %s plant in %s's test is the shortest?" % (plant, who), a, [l for l in labels if l != a] + ["They are the same height."], "Without water the plant could not grow.")
    if k == "diff":
        x, y = sorted(R.sample(list(zip(labels, vals)), 2), key=lambda t: -t[1])
        return item(tab + "How much taller is the %s plant than the %s plant in %s's test?" % (x[0], y[0], who), "%d cm" % (x[1] - y[1]),
                    ["%d cm" % x[1], "%d cm" % (x[1] + y[1]), "%d cm" % (x[1] - y[1] + 2)], "%d − %d = %d cm." % (x[1], y[1], x[1] - y[1]))
    return item(tab + "What can %s conclude about %s plants?" % (who, plant), "They need both sunlight and water to grow well.", ["They grow best in the dark.", "They do not need water.", "Light and water do not matter."],
                "The plant with both grew the most.")


B1 = bank([
    ("What two things do plants need from this list?", "sunlight and water", ["candy and toys", "darkness and ice", "noise and wind only"], "Plants also need air and space."),
    ("Where do plants make their food?", "in their leaves, using sunlight", ["in the soil", "from rocks", "from people"], "Leaves use light to make food."),
    ("What happens to a plant with no water?", "It wilts and can die.", ["It grows faster.", "It turns blue.", "Nothing happens."], "Plants need water."),
    ("What happens to a plant kept in the dark?", "It grows pale, thin and weak.", ["It grows big and green.", "It turns into a tree.", "It makes flowers faster."], "Plants need light."),
    ("Which part of a plant takes in water?", "the roots", ["the flowers", "the leaves only", "the seeds"], "Roots drink water from the soil."),
    ("Can a plant get too much water?", "Yes. Too much water can rot the roots.", ["No, more is always better.", "Only cactus plants need water.", "Plants never need water."], "Just the right amount."),
    ("What is a fair test?", "a test where you change only one thing", ["a test where you change everything", "a test with no plants", "a guess"], "Keep everything else the same."),
    ("Why do leaves face the window in a classroom?", "They grow toward the light.", ["They like the view.", "Wind pushes them.", "They are cold."], "Plants bend toward light."),
])
B5 = bank([
    ("Ava's plant in a dark box is pale and tall but thin. What does it need?", "sunlight", ["more darkness", "candy", "a smaller pot"], "Pale plants need light."),
    ("Leo forgot to water his plant for 2 weeks. The leaves droop. What should he do?", "water it", ["put it in the dark", "paint the leaves", "cut the roots"], "Drooping means thirsty."),
    ("Mia uses 2 plants of the same kind, size and soil. Why?", "so only the thing she is testing is different", ["so they look pretty", "so the test is faster", "so they grow flowers"], "Fair test."),
    ("Kai's sun + water plant grew 15 cm. His dark + water plant grew 6 cm. How much more did the first one grow?", "9 cm", ["21 cm", "15 cm", "6 cm"], "15 − 6 = 9."),
    ("A plant on a windowsill leans toward the window. Which explains this?", "It grows toward the sunlight it needs.", ["It is falling over.", "It wants fresh air.", "The pot is too small."], "Plants need light."),
])


def body():
    pic = setup_svg(["sun+water", "dark+water", "sun+dry"])
    ex = [("A plant gets water but no light. What happens?", ["Plants need light."], "It grows pale and weak."),
          ("Test: do plants need water? What do you change?", ["Change one thing."], "only the water")]
    mist = ["Thinking plants get food from the soil. They make food with sunlight.",
            "Thinking more water is always better.",
            "Changing two things at once, so the test is not fair."]
    return kid_lesson(pic, "Plants need sunlight and water to grow.",
                      ["No light: pale and weak.", "No water: wilted.", "Test fairly: change only one thing."], ex, mist)


def main():
    sets = U.sets([
        ("What plants need", B1 + [(g_what, 4), (g_best, 4), (g_data, 4)]),
        ("Light and water", [(g_best, 8), (g_what, 4), (g_fair, 4), (g_data, 4)]),
        ("Fair tests", [(g_fair, 6), (g_best, 6), (g_data, 8)]),
        ("Reading plant data", [(g_data, 20)]),
        ("Plant scientists", B5 + [(g_data, 15)]),
    ])
    make("grade-2", "what-plants-need", 5, "2-LS2-1",
         "Plan and conduct an investigation to determine if plants need sunlight and water to grow.",
         "What Plants Need to Grow",
         "Grade 2 What Plants Need Worksheets: Sunlight, Water and Fair Tests",
         "What Plants Need",
         "Free grade 2 science worksheets on what plants need (NGSS 2-LS2-1): sunlight and water, fair tests and reading plant growth data. 100 picture questions with answers.",
         "Plants need sunlight and water.",
         "Test it fairly: change only one thing.",
         body(),
         [("What do plants need to grow?", "Sunlight, water, air and space. This unit tests sunlight and water."),
          ("How do you test if plants need light?", "Use two plants that are the same. Give both the same water. Put one in the sun and one in the dark."),
          ("Do plants eat soil?", "No. Plants make their own food in their leaves using sunlight, water and air.")],
         sets)


if __name__ == "__main__":
    main()
