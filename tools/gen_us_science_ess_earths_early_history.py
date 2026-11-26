# -*- coding: utf-8 -*-
"""
US High School Earth and Space Science: Earth's Early History (HS-ESS1-6)
  python tools/gen_us_science_ess_earths_early_history.py
Apply scientific reasoning and evidence from ancient Earth materials, meteorites, and other planetary surfaces to
construct an account of Earth's formation and early history.
Radiometric dating (fraction left, parent : daughter ratios, half-lives), choosing a dating isotope, evidence from
meteorites, zircon crystals, Moon rocks and craters, and the order of early events.
Wrong answers come from real mistakes: "after two half-lives nothing is left", "carbon-14 dates dinosaur bones",
"Earth's oldest rocks show its exact age", "the Moon has no useful record".
"""
from sci_common import Unit, item, bank, lesson, make, table, People
from sci_phys import num, uniq, safe

U = Unit(90406)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ISO = [("uranium-238", "lead-206", 4.47, "billion"), ("potassium-40", "argon-40", 1.25, "billion"), ("uranium-235", "lead-207", 704, "million"),
       ("carbon-14", "nitrogen-14", 5730, "")]


@safe
def g_age():
    p, d, hl, u = R.choice(ISO)
    n = R.randint(1, 6)
    k = R.choice(["frac", "ratio"])
    if (p == "carbon-14" and k == "ratio") or (u == "billion" and hl * n > 4.6) or (u == "million" and hl * n > 4600) or not once(("ag", p, n, k)):
        return None
    left = 1 / 2 ** n
    age = hl * n
    unit = ("%s years" % u) if u else "years"
    g = "%s %s" % (num(age, 2), unit)
    w = ["%s %s" % (num(hl * 2 ** n, 2), unit), "%s %s" % (num(hl * (n + 1), 2), unit), "%s %s" % (num(hl / n, 2), unit), "%s %s" % (num(hl, 2), unit)]
    if k == "frac":
        return item("%s has 1/%d of its original %s left (half-life %s %s). How old is it?" % ("A piece of old wood" if p == "carbon-14" else "A mineral", 2 ** n, p, num(hl, 2), unit), g, uniq(g, w),
                    "1/%d = %d half-lives; %d × %s = %s %s." % (2 ** n, n, n, num(hl, 2), num(age, 2), unit))
    dd = 2 ** n - 1
    return item("A rock has %s and %s in a ratio of 1 : %d (half-life of %s: %s %s). How old is it? (Assume all the %s came from decay.)" % (p, d, dd, p, num(hl, 2), unit, d), g, uniq(g, w),
                "1 : %d means 1/%d is left → %d half-lives = %s %s." % (dd, 2 ** n, n, num(age, 2), unit))


@safe
def g_hl():
    n = R.randint(1, 5)
    k = R.choice(["left", "count", "daughter"])
    m0 = R.choice([16, 32, 64, 80, 96, 100, 128, 160, 200, 320])
    left = m0 / 2 ** n
    if left != round(left, 2) or not once(("hl", n, m0, k)):
        return None
    if k == "left":
        g = "%s g" % num(left, 2)
        return item("A sample starts with %d g of a radioactive parent. How much parent is left after %d half-lives?" % (m0, n), g,
                    uniq(g, ["%s g" % num(m0 / (2 * n), 2), "%s g" % num(m0 - left, 2), "0 g", "%s g" % num(left * 2, 2)]), "Halve %d times: %s g." % (n, num(left, 2)))
    if k == "count":
        g = str(n)
        return item("A sample had %d g of parent and now has %s g. How many half-lives have passed?" % (m0, num(left, 2)), g, uniq(g, [str(n + 1), str(n - 1) if n > 1 else "6", str(2 ** n), str(n * 2)]),
                    "%d → %s takes %d halvings." % (m0, num(left, 2), n))
    g = "%s g" % num(m0 - left, 2)
    return item("A rock started with %d g of parent isotope and no daughter. After %d half-lives, how much daughter isotope is there?" % (m0, n), g,
                uniq(g, ["%s g" % num(left, 2), "%d g" % m0, "0 g", "%s g" % num(m0 / 2, 2)]), "Daughter = original − parent left = %d − %s = %s g." % (m0, num(left, 2), num(m0 - left, 2)))


USE = [("a 25,000-year-old mammoth bone", "carbon-14 (half-life 5,730 years)"), ("a 3.9-billion-year-old Moon rock", "uranium-238 (half-life 4.5 billion years)"),
       ("a 100-million-year-old volcanic ash layer", "potassium-40 (half-life 1.25 billion years)"), ("a 5,000-year-old wooden tool", "carbon-14 (half-life 5,730 years)"),
       ("a 4.4-billion-year-old zircon crystal", "uranium-238 (half-life 4.5 billion years)"), ("a 70-million-year-old lava flow", "potassium-40 (half-life 1.25 billion years)")]


@safe
def g_use():
    s, a = R.choice(USE)
    if not once(("us", s)):
        return None
    opts = ["carbon-14 (half-life 5,730 years)", "uranium-238 (half-life 4.5 billion years)", "potassium-40 (half-life 1.25 billion years)", "hydrogen-3 (half-life 12 years)"]
    return item("Which isotope is best for dating %s?" % s, a, [o for o in opts if o != a], "Choose a half-life close to the age: too short and nothing is left; too long and almost nothing has decayed.")


EV = [("Meteorites", "The solar system, including Earth, formed about 4.56 billion years ago."), ("Tiny zircon crystals from Australia (4.4 billion years old)", "Earth had solid crust and probably liquid water very early."),
      ("Heavily cratered surfaces on the Moon and Mercury", "The early solar system had many large impacts."), ("Moon rocks brought back by Apollo", "The Moon formed from material similar to Earth's, likely after a giant impact."),
      ("Banded iron formations about 2.5 billion years old", "Oxygen began to build up in the oceans and air."), ("Stromatolite fossils about 3.5 billion years old", "Simple microbial life existed very early.")]


@safe
def g_ev():
    s, a = R.choice(EV)
    k = R.random() < 0.6
    if not once(("ev", s, k)):
        return None
    if k:
        return item("What does this evidence tell us about early Earth: %s?" % s, a, R.sample([x[1] for x in EV if x[1] != a], 3), "Old materials record early events.")
    return item("Which evidence best supports this idea: “%s”" % a, s, R.sample([x[0] for x in EV if x[0] != s], 3), "Match the evidence to the claim.")


EVT = [("Earth forms", 4.56), ("the Moon forms after a giant impact", 4.5), ("the oldest zircon crystals form", 4.4), ("the Late Heavy Bombardment of impacts", 4.0),
       ("the first microbial fossils (stromatolites)", 3.5), ("oxygen begins to build up in the air", 2.4), ("the first animals appear", 0.6)]


@safe
def g_order():
    a, b = R.sample(EVT, 2)
    if not once(("or", tuple(sorted((a[0], b[0]))))):
        return None
    first, second = sorted([a, b])
    older = a if a[1] > b[1] else b
    newer = b if older is a else a
    return item("Which happened first: %s, or %s?" % (first[0], second[0]), older[0], [newer[0], "They happened at the same time.", "Neither has happened yet."],
                "%s: about %s billion years ago; %s: about %s billion years ago." % (older[0][0].upper() + older[0][1:], num(older[1], 2), newer[0], num(newer[1], 2)))


B1 = bank([
    ("How old is Earth?", "about 4.6 billion years", ["about 6,000 years", "about 46 million years", "about 13.8 billion years"], "From meteorites and Moon rocks."),
    ("Why are meteorites used to find Earth's age?", "They formed with the solar system and have not been changed by plate tectonics or erosion.", ["They are from other galaxies.", "They are very young.", "They contain no isotopes."], "Unchanged material."),
    ("Why are Earth's oldest rocks younger than Earth itself?", "Early crust was melted, eroded or recycled by plate tectonics.", ["Rocks formed later than Earth on purpose.", "Old rocks float to space.", "Rocks cannot be dated."], "Recycling."),
    ("What is radiometric dating?", "finding an age from how much of a radioactive isotope has decayed", ["counting tree rings only", "measuring rock color", "guessing from size"], "Uses half-lives."),
    ("After one half-life, how much of the parent isotope is left?", "one half", ["none", "one quarter", "all of it"], "Halves each time."),
    ("Why does the Moon keep a better record of early impacts than Earth?", "It has no plate tectonics, liquid water or weather to erase craters.", ["The Moon is older than the solar system.", "The Moon has more volcanoes.", "Earth had no impacts."], "Preserved surface."),
    ("Why can't carbon-14 date dinosaur fossils?", "Its half-life is too short; almost none is left after millions of years.", ["Dinosaurs had no carbon.", "Carbon-14 never decays.", "It only dates rocks from space."], "Choose the right isotope."),
    ("What does a zircon crystal 4.4 billion years old tell us?", "Earth had solid crust very early in its history.", ["Earth formed 4.4 million years ago.", "There was no crust until recently.", "Zircons come from the Moon."], "Hadean evidence."),
])
B5 = bank([
    ("Why do scientists date the same rock with two different isotope systems?", "If both give the same age, the result is more reliable.", ["To get two different ages.", "One isotope is always wrong.", "To use up the sample."], "Cross-checking."),
    ("Moon rocks and Earth rocks have very similar oxygen isotopes. What does this suggest?", "The Moon formed from material closely related to Earth's.", ["The Moon came from Mars.", "The Moon is made of ice.", "Earth formed from the Moon."], "Giant-impact model."),
    ("A student says Earth is 4.0 billion years old because that is the age of its oldest rocks. What is the best reply?", "Meteorites and lunar samples show Earth formed earlier, about 4.56 billion years ago.", ["The student is exactly right.", "Earth is 13.8 billion years old.", "Rocks cannot be dated."], "Evaluate the evidence."),
    ("Why do impact craters on Mars help us understand early Earth?", "Mars preserves an older surface, showing how many impacts happened in the early solar system.", ["Mars is Earth's moon.", "Mars has plate tectonics.", "Craters form from volcanoes only."], "Other planetary surfaces."),
    ("A lava layer is dated at 50 million years and a fossil lies just below it. What can you conclude?", "The fossil is older than 50 million years.", ["The fossil is younger.", "They are the same age exactly.", "Nothing can be concluded."], "Superposition + dating."),
])


def body():
    think = ("<p><b>Old materials and other worlds record Earth's early history.</b></p>"
             "<ul><li>Radiometric dating: after n half-lives, (1/2)<sup>n</sup> of the parent is left. Parent : daughter 1 : 1 → 1 half-life; 1 : 3 → 2; 1 : 7 → 3.</li>"
             "<li>Meteorites date the solar system (~4.56 billion years). Zircons, Moon rocks and craters show early crust, a giant impact and heavy bombardment.</li>"
             "<li>Choose an isotope whose half-life fits the age you want to measure.</li></ul>")
    ex = [("1/4 of potassium-40 left (half-life 1.25 billion years)?", ["2 half-lives", "2 × 1.25"], "2.5 billion years"),
          ("Parent : daughter = 1 : 3?", ["1/4 left = 2 half-lives"], "2 half-lives")]
    mist = ["Thinking nothing is left after two half-lives.", "Using carbon-14 to date dinosaur bones.", "Thinking the oldest rocks give Earth's exact age."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Earth's beginnings", B1 + [(g_order, 8), (g_ev, 4)]),
        ("Half-lives", [(g_hl, 17), (g_use, 3)]),
        ("Radiometric dating", [(g_age, 16), (g_hl, 4)]),
        ("Evidence from rocks and space", [(g_ev, 6), (g_order, 10), (g_use, 2), (g_age, 2)]),
        ("Building the story", B5 + [(g_age, 8), (g_hl, 7)]),
    ])
    make("earth-and-space-science", "earths-early-history", 6, "HS-ESS1-6",
         "Apply scientific reasoning and evidence from ancient Earth materials, meteorites, and other planetary surfaces to construct an account of Earth's formation and early history.",
         "Earth's Early History",
         "Earth's History Worksheets: Radiometric Dating, Meteorites and Early Earth (Earth Science)",
         "Earth's Early History",
         "Free high school Earth and space science worksheets on Earth's early history (NGSS HS-ESS1-6): radiometric dating, half-lives, meteorites, zircons, Moon rocks and craters. 100 questions with answers.",
         "Earth is about 4.6 billion years old.",
         "Meteorites, zircons and Moon rocks, dated by radioactive decay, tell Earth's early story.",
         body(),
         [("How do scientists know Earth's age?", "Radiometric dating of meteorites and Moon rocks, which formed with the solar system and were not recycled, gives about 4.56 billion years."),
          ("How does radiometric dating work?", "A radioactive parent isotope decays into a daughter at a known half-life. The fraction of parent left tells how many half-lives have passed."),
          ("Why use different isotopes for different ages?", "The half-life should be similar to the age being measured so a measurable amount of parent and daughter remains.")],
         sets)


if __name__ == "__main__":
    main()
