# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Heating and Cooling (2-PS1-4)
  python tools/gen_us_science_g2_heating_and_cooling.py
Construct an argument with evidence that some changes caused by heating or cooling can be reversed and some cannot.
Melting and freezing (ice, chocolate, butter, wax, crayons) can be undone; cooking an egg, baking, toasting and
burning cannot. Simple data on how fast ice melts in warm and cool places.
Wrong answers come from real mistakes: "a cooked egg turns raw again if you cool it", "melting makes the material
disappear", "freezing is caused by heating".
"""
from sci_common import Unit, item, bank, kid_lesson, make, table, fig, svg_wrap, arrow, People
from ws_common import text
import sci_kids as K

U = Unit(20104)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


# (change, heating or cooling, can be undone, how to undo or why not)
CH = [("An ice cube melts into water.", "heating", True, "Freeze the water and it turns back into ice."),
      ("Water freezes into ice in the freezer.", "cooling", True, "Warm the ice and it melts back into water."),
      ("Chocolate melts in a warm hand.", "heating", True, "Cool it and it gets hard again."),
      ("Melted chocolate hardens in the fridge.", "cooling", True, "Warm it and it melts again."),
      ("Butter melts in a hot pan.", "heating", True, "Cool it and it gets solid again."),
      ("A candle's wax melts near the flame.", "heating", True, "When it cools, the wax gets hard again."),
      ("A crayon melts in a hot car.", "heating", True, "When it cools, it is hard again (in a new shape)."),
      ("A puddle freezes on a cold night.", "cooling", True, "It melts again when the sun warms it."),
      ("An egg is cooked in a pan.", "heating", False, "A cooked egg can never become a raw egg again."),
      ("Bread is toasted.", "heating", False, "Toast cannot turn back into soft bread."),
      ("Cake batter is baked into a cake.", "heating", False, "A cake cannot turn back into batter."),
      ("Paper burns in a campfire.", "heating", False, "Ashes cannot turn back into paper."),
      ("Popcorn kernels pop.", "heating", False, "Popped corn cannot become a hard kernel again."),
      ("Wet clay is baked into a hard pot.", "heating", False, "Baked clay cannot become soft wet clay again."),
      ("Pancake batter cooks on a griddle.", "heating", False, "The pancake cannot turn back into runny batter."),
      ("A marshmallow gets toasted over a fire.", "heating", False, "The brown, crispy outside cannot turn back.")]


def g_undo():
    s, hc, rev, why = R.choice(CH)
    who = P.next()[0]
    if not once(("u", s)):
        return None
    if rev:
        return item("%s observes: “%s” Can this change be undone?" % (who, s), "Yes. " + why, ["No. It can never change back.", "No. The material is gone.", "Yes, but only by adding salt."], "Melting and freezing can be undone.")
    return item("%s observes: “%s” Can this change be undone?" % (who, s), "No. " + why, ["Yes. Just cool it down.", "Yes. Just put it in the freezer.", "Yes. Just wait a day."], "Some changes from heating make something new.")


def g_hc():
    s, hc, rev, why = R.choice(CH)
    who = P.next()[0]
    if not once(("h", s)):
        return None
    return item("%s observes: “%s” What caused this change?" % (who, s), hc, ["cooling" if hc == "heating" else "heating", "wind", "light only"],
                "Melting, cooking and baking come from heating. Freezing and hardening come from cooling.")


def pair_svg(a, b, word):
    s = K.icon(a, 60, 55, 0.9) + K.icon(b, 240, 55, 0.9) + arrow(110, 55, 190, 55, "#d9822b", 3, 10) + text(150, 40, word, 14)
    return svg_wrap(300, 110, s, "%s changing into %s" % (K.name(a), K.name(b)))


PAIRS = [("ice", "drop", "melts", "heating", True), ("drop", "ice", "freezes", "cooling", True), ("crayon", "puddle", "melts", "heating", True),
         ("snow", "drop", "melts", "heating", True), ("ice", "puddle", "melts", "heating", True), ("puddle", "ice", "freezes", "cooling", True)]
WORDS = {("crayon", "puddle"): ("a crayon", "a puddle of melted wax"), ("snow", "drop"): ("snow", "water"), ("ice", "puddle"): ("an ice cube", "a puddle"),
         ("puddle", "ice"): ("a puddle", "ice"), ("ice", "drop"): ("an ice cube", "water"), ("drop", "ice"): ("water", "an ice cube")}


def g_pic():
    who = P.next()[0]
    a, b, word, hc, rev = R.choice(PAIRS)
    wa, wb = WORDS[(a, b)]
    k = R.choice(["name", "cause", "back"])
    if not once(("p", a, b, k)):
        return None
    pic = fig(pair_svg(a, b, "?"))
    if k == "name":
        return item(pic + "%s draws %s changing into %s. What is this change called?" % (who, wa, wb),
                    "melting" if word == "melts" else "freezing", ["freezing" if word == "melts" else "melting", "burning", "cooking"], "Solid to liquid is melting; liquid to solid is freezing.")
    if k == "cause":
        return item(pic + "In %s's picture, %s changes into %s. Did heating or cooling cause it?" % (who, wa, wb), hc, ["cooling" if hc == "heating" else "heating", "pushing", "shaking"],
                    "Melting comes from heating; freezing comes from cooling.")
    return item(pic + "In %s's picture, %s changes into %s. How could you change it back?" % (who, wa, wb), "cool it down" if hc == "heating" else "warm it up",
                ["warm it up more" if hc == "heating" else "cool it down more", "it can never change back", "paint it"], "Melting and freezing can be undone.")


def g_melt():
    who = P.next()[0]
    places = [("in the sun", R.choice([10, 12, 15])), ("in the shade", R.choice([25, 30, 35])), ("in a cooler", R.choice([60, 75, 90])), ("on a warm stove", R.choice([3, 4, 5]))]
    rows = R.sample(places, 3)
    k = R.choice(["fast", "slow", "diff"])
    if not once(("m", tuple(r for r in rows), k)):
        return None
    tab = table(["Where the ice cube was", "Minutes to melt"], [[p, str(m)] for p, m in rows])
    if k == "fast":
        a = min(rows, key=lambda r: r[1])[0]
        return item(tab + "%s timed ice cubes. Where did the ice melt fastest?" % who, a, [r[0] for r in rows if r[0] != a] + ["They melted at the same time."], "Fewest minutes = fastest. More heat melts ice faster.")
    if k == "slow":
        a = max(rows, key=lambda r: r[1])[0]
        return item(tab + "%s timed ice cubes. Where did the ice melt slowest?" % who, a, [r[0] for r in rows if r[0] != a] + ["They melted at the same time."], "Most minutes = slowest. Less heat, slower melting.")
    a, b = sorted(R.sample(rows, 2), key=lambda r: -r[1])
    return item(tab + "In %s's test, how many more minutes did the ice %s take than the ice %s?" % (who, a[0], b[0]), str(a[1] - b[1]), [str(a[1]), str(a[1] + b[1]), str(a[1] - b[1] + 5)],
                "%d − %d = %d." % (a[1], b[1], a[1] - b[1]))


B1 = bank([
    ("What happens to ice when it is heated?", "It melts into water.", ["It turns into a rock.", "It gets bigger and harder.", "Nothing."], "Heating melts ice."),
    ("What happens to water in a freezer?", "It freezes into ice.", ["It boils.", "It disappears.", "It turns into juice."], "Cooling freezes water."),
    ("Can melted ice be turned back into ice?", "Yes. Put it in the freezer.", ["No, never.", "Only if you add sugar.", "Only in summer."], "This change can be undone."),
    ("Can a cooked egg turn back into a raw egg?", "No.", ["Yes, if you cool it.", "Yes, if you freeze it.", "Yes, after a day."], "Cooking makes a change that cannot be undone."),
    ("What is melting?", "a solid turning into a liquid", ["a liquid turning into a solid", "something burning", "something breaking"], "Ice to water."),
    ("What is freezing?", "a liquid turning into a solid", ["a solid turning into a liquid", "something cooking", "something drying"], "Water to ice."),
    ("Which change can NOT be undone?", "baking a cake", ["melting butter", "freezing juice", "melting chocolate"], "A cake cannot become batter again."),
    ("Which change CAN be undone?", "melting a crayon", ["toasting bread", "burning wood", "cooking an egg"], "Melted wax gets hard again when it cools."),
])
B5 = bank([
    ("Ava melts chocolate and pours it into a star mold. Then she cools it. What does she get?", "a hard chocolate star", ["chocolate milk", "a cake", "nothing"], "Cooling makes it hard in a new shape."),
    ("Leo says a toasted marshmallow will turn white again in the fridge. Is he right?", "No. Toasting cannot be undone.", ["Yes.", "Yes, if he waits an hour.", "Only if it is cold outside."], "Use evidence: it stays brown."),
    ("Mia freezes juice into a pop and then it melts in the sun. What is the juice like now?", "liquid juice again", ["ice forever", "a cake", "gone"], "Freezing and melting can go back and forth."),
    ("Why does a snowman melt in spring?", "The warm air and sun heat the snow.", ["The wind cools it.", "Rain freezes it.", "It gets too cold."], "Heating melts snow."),
    ("Kai cooks pancakes. Which evidence shows the change cannot be undone?", "Cooling the pancake does not make it runny batter again.", ["The pancake is round.", "The pan is hot.", "The batter was white."], "Try to undo it: it stays a pancake."),
])


def body():
    pic = pair_svg("ice", "drop", "heat")
    ex = [("Butter melts in a pan. Can it change back?", ["Cool it."], "Yes, it gets solid again."),
          ("Bread is toasted. Can it change back?", ["Cooling does not make soft bread."], "No.")]
    mist = ["Thinking a cooked egg can become raw if you cool it.",
            "Thinking melted things disappear. They are still there as a liquid.",
            "Mixing up melting (heating) and freezing (cooling)."]
    return kid_lesson(pic, "Heating and cooling can change things.",
                      ["Some changes can be undone: ice melts, water freezes.", "Some cannot: cooking, baking, burning.", "Test it: try to change it back."], ex, mist)


def main():
    sets = U.sets([
        ("Melting and freezing", B1 + [(g_pic, 6), (g_hc, 6)]),
        ("Heating or cooling?", [(g_hc, 10), (g_pic, 8), (g_melt, 2)]),
        ("Can it be undone?", [(g_undo, 16), (g_pic, 2), (g_melt, 2)]),
        ("Ice melting data", [(g_melt, 18), (g_pic, 2)]),
        ("Using evidence", B5 + [(g_melt, 8), (g_undo, 7)]),
    ])
    make("grade-2", "heating-and-cooling", 4, "2-PS1-4",
         "Construct an argument with evidence that some changes caused by heating or cooling can be reversed and some cannot.",
         "Heating and Cooling",
         "Grade 2 Heating and Cooling Worksheets: Changes You Can and Cannot Undo",
         "Heating and Cooling",
         "Free grade 2 science worksheets on heating and cooling (NGSS 2-PS1-4): melting and freezing, cooking and baking, and which changes can be undone. 100 picture questions with answers.",
         "Some changes can be undone.",
         "Melting and freezing go back and forth. Cooking and burning do not.",
         body(),
         [("Which changes can be undone?", "Melting and freezing: ice and water, chocolate, butter, wax and crayons can change back."),
          ("Which changes cannot be undone?", "Cooking an egg, baking a cake, toasting bread and burning paper make something new that cannot change back."),
          ("How can kids test it?", "Try to change it back by cooling or warming it, and observe what happens.")],
         sets)


if __name__ == "__main__":
    main()
