# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Liquid Volume and Weight (TEKS 3.7D, 3.7E)
  python3 tools/gen_ustx_math_g3_liquid_volume_and_weight.py
Deciding whether to measure liquid volume (capacity) or weight, choosing customary and metric units (cups, quarts,
gallons, ounces, pounds, milliliters, liters, grams, kilograms) and tools, reading containers and scales (the US
Grade 3 makers, with "mass" said as "weight" as in the TEKS), and word problems.
Wrong answers come from real mistakes: measuring a liquid with a scale when the question asks how much it holds,
choosing a unit that is far too big or small, and reading a scale between marks as the next number.
"""
import random, re
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, run_many, adopt, example)
import gen_us_math_g3_mass_volume as usm

adopt(usm)
R = random.Random(61801)

CAP_Q = ["how much water a bathtub holds", "how much juice is in a pitcher", "how much milk fits in a glass", "how much gas a car's tank holds",
         "how much water is in a fish tank", "how much soup is in a pot", "how much lemonade is in a cooler", "how much medicine is in a spoon"]
WT_Q = ["how heavy a watermelon is", "how heavy a backpack is", "how heavy a bag of rice is", "how heavy a puppy is",
        "how heavy a box of books is", "how heavy an apple is", "how heavy a pumpkin is", "how heavy a pencil is"]


# ------------------------------------------------------------ set 1: capacity or weight?
def one_which(r):
    if r.random() < 0.5:
        what = r.choice(CAP_Q)
        right, other = "Liquid volume (capacity)", "Weight"
    else:
        what = r.choice(WT_Q)
        right, other = "Weight", "Liquid volume (capacity)"
    kind = r.choice(["meas", "tool"])
    if kind == "meas":
        return mcq("You want to know %s. What should you measure?" % what, right, [other, "Length", "Time"],
                   "You want to know %s, so measure <b>%s</b>." % ("how much it holds" if right != "Weight" else "how heavy it is", right.lower()))
    tool = "A measuring cup" if right != "Weight" else "A scale"
    return mcq("Which tool would you use to find %s?" % what, tool, ["A scale" if tool == "A measuring cup" else "A measuring cup", "A ruler", "A clock"],
               "<b>%s</b> measures %s." % (tool, "liquid volume" if right != "Weight" else "weight"))


# ------------------------------------------------------------ set 2: choose the unit
UNIT_Q = [("the water in a bathtub", "gallons", ["cups", "ounces", "pounds"]),
          ("the milk in a cereal bowl", "cups", ["gallons", "pounds", "yards"]),
          ("a bottle of shampoo", "milliliters", ["liters", "kilograms", "meters"]),
          ("the water in a swimming pool", "liters", ["milliliters", "grams", "centimeters"]),
          ("a pitcher of iced tea", "quarts", ["ounces", "pounds", "miles"]),
          ("a spoonful of honey", "milliliters", ["liters", "kilograms", "gallons"]),
          ("a bag of potatoes", "pounds", ["ounces", "gallons", "inches"]),
          ("a slice of bread", "ounces", ["pounds", "quarts", "feet"]),
          ("a pickup truck", "pounds", ["ounces", "cups", "liters"]),
          ("a paper clip", "grams", ["kilograms", "liters", "meters"]),
          ("a bicycle", "kilograms", ["grams", "milliliters", "centimeters"]),
          ("a strawberry", "grams", ["kilograms", "liters", "pounds"]),
          ("a large dog", "kilograms", ["grams", "liters", "meters"]),
          ("a jug of milk", "gallons", ["cups", "pounds", "ounces"]),
          ("a kitchen sink full of water", "gallons", ["cups", "ounces", "grams"]),
          ("a pencil", "grams", ["kilograms", "pounds", "liters"]),
          ("a glass of orange juice", "cups", ["gallons", "pounds", "liters"]),
          ("a watermelon", "pounds", ["ounces", "gallons", "cups"]),
          ("a bucket of paint", "liters", ["milliliters", "kilograms", "meters"]),
          ("a backpack full of books", "kilograms", ["grams", "liters", "milliliters"]),
          ("a baby bottle of milk", "ounces", ["gallons", "pounds", "miles"]),
          ("a cow", "pounds", ["ounces", "cups", "inches"])]


def one_unit(r):
    what, right, wrong = r.choice(UNIT_Q)
    kind = "weight" if right in ("pounds", "ounces", "grams", "kilograms") and "bottle" not in what else "liquid volume"
    return mcq("Which unit is best for the %s of %s?" % (kind, what), right, wrong,
               "<b>%s</b> fit%s the size of %s." % (right.capitalize(), "" if right.endswith("s") else "s", what))


def to_weight(it):
    for k in ("q", "e"):
        t = it[k]
        t = re.sub(r"has a mass of", "weighs", t)
        t = re.sub(r"\bmasses\b", "weights", t)
        t = re.sub(r"\bmass\b", "weight", t)
        t = re.sub(r"\bMass\b", "Weight", t)
        it[k] = t
    it["c"] = [re.sub(r"\bmass\b", "weight", c) for c in it["c"]]
    return it


# ------------------------------------------------------------ set 5: word problems
def one_story(r):
    k = Kid(r).next()
    kind = r.choice(["cups", "pounds", "liters", "kg", "gallons"])
    if kind == "cups":
        a, b = r.randint(2, 6), r.randint(2, 5)
        return mcq("%s pours %d cups of water into a pot. Then %s adds %d more cups. How many cups of water are in the pot?" % (k["n"], a, k["he"], b), "%d cups" % (a + b),
                   ["%d cups" % (a * b), "%d cups" % abs(a - b) if a != b else "%d cups" % (a + b + 2), "%d cups" % (a + b + 1)], "%d + %d = <b>%d cups</b>." % (a, b, a + b))
    if kind == "pounds":
        a, b = r.randint(12, 40), r.randint(3, 11)
        return mcq("A puppy weighs %d pounds. A cat weighs %d pounds. How much more does the puppy weigh?" % (a, b), "%d pounds" % (a - b),
                   ["%d pounds" % (a + b), "%d pounds" % (a - b + 10), "%d pounds" % (a - b - 1)], "%d − %d = <b>%d pounds</b>." % (a, b, a - b))
    if kind == "liters":
        n, l = r.randint(3, 9), r.randint(2, 8)
        return mcq("A cooler holds %d liters of lemonade. How many liters do %d coolers hold?" % (l, n), "%d liters" % (n * l),
                   ["%d liters" % (n + l), "%d liters" % (n * l - l), "%d liters" % (n * l + l)], "%d × %d = <b>%d liters</b>." % (n, l, n * l))
    if kind == "kg":
        t, n = r.choice([(12, 3), (20, 4), (18, 6), (24, 4), (30, 5), (16, 2), (21, 3), (35, 7)])
        return mcq("%d kilograms of rice are shared equally into %d bags. How many kilograms are in each bag?" % (t, n), "%d kilograms" % (t // n),
                   ["%d kilograms" % (t - n), "%d kilograms" % (t + n), "%d kilograms" % (t // n + 1)], "%d ÷ %d = <b>%d kilograms</b>." % (t, n, t // n))
    a, b = r.randint(10, 30), r.randint(5, 20)
    return mcq("A fish tank has %d gallons of water. %s adds %d gallons. Then %s takes out 3 gallons to clean it. How many gallons are in the tank now?" % (a, k["n"], b, k["he"]), "%d gallons" % (a + b - 3),
               ["%d gallons" % (a + b), "%d gallons" % (a + b + 3), "%d gallons" % (a - b - 3 if a - b - 3 > 0 else a + b - 13)], "%d + %d = %d. %d − 3 = <b>%d gallons</b>." % (a, b, a + b, a + b, a + b - 3))


def build():
    s3 = run_many(usm.set_container, "rnd", seed=191)
    s4 = [to_weight(it) for it in run_many(usm.set_scale, "rnd", seed=192, n=10)] + [to_weight(it) for it in run_many(usm.set_balance, "rnd", seed=193, n=10)]
    sets = [S("Liquid volume or weight?", collect(one_which, 20, R)),
            S("Choose the unit", collect(one_unit, 20, R)),
            S("Read liquid volume", s3),
            S("Read scales and balances", s4),
            S("Word problems", collect(one_story, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li><b>Liquid volume</b> (capacity) tells how much a container holds. Use a measuring cup or a marked container.</li>"
        "<li><b>Weight</b> tells how heavy something is. Use a scale or a pan balance.</li>"
        "<li>Customary units: cups, pints, quarts and gallons for liquid volume; ounces and pounds for weight.</li>"
        "<li>Metric units: milliliters and liters for liquid volume; grams and kilograms for weight.</li></ul>",
        [example("Which unit is best for the water in a bathtub?", ["A bathtub holds a lot of water.", "Cups and ounces are too small."], "gallons (or liters)"),
         example("Which tool tells how heavy a pumpkin is?", ["Heavy means weight.", "Weight is measured with a scale."], "a scale")],
        [["Using a scale to find how much a pitcher holds", "How much it holds is liquid volume: use a measuring cup."],
         ["Choosing a unit that is far too small or big", "Think: is it like a spoonful, a cup, or a bathtub?"],
         ["Reading the next number on a scale", "Count the marks between the numbers to find what each mark is worth."]])
    faq = [("What does TEKS 3.7D ask?", "Decide when it is appropriate to measure liquid volume (capacity) or weight."),
           ("What does TEKS 3.7E ask?", "Determine liquid volume or weight using appropriate units and tools, both customary (cups, quarts, gallons, ounces, pounds) and metric (milliliters, liters, grams, kilograms)."),
           ("What is the difference between liquid volume and weight?", "Liquid volume is how much a container holds. Weight is how heavy something is. A big balloon has a large volume but a small weight."),
           ("How do you read a scale?", "Find the numbers on each side of the pointer, then count what each small mark is worth.")]
    make("liquid-volume-and-weight", 18, "Geometry and Measurement", "3.7D, 3.7E",
         "3.7D determine when it is appropriate to use measurements of liquid volume (capacity) or weight; 3.7E determine liquid volume (capacity) or weight using appropriate units and tools",
         "Liquid Volume and Weight: Units and Tools", "Liquid Volume and Weight",
         "Free Grade 3 worksheets for Texas TEKS 3.7D and 3.7E: liquid volume or weight, customary and metric units, measuring cups and scales, reading containers and scales, and word problems. 100 questions with answers.",
         "Liquid volume is how much a container holds. Weight is how heavy something is.", "Use a measuring cup for liquid volume and a scale for weight. Choose a unit that fits the size.",
         body, faq, sets, seo_title="Grade 3 Liquid Volume and Weight Worksheets: Units and Tools (TEKS 3.7D, 3.7E)")


if __name__ == "__main__":
    build()
