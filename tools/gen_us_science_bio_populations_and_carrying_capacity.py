# -*- coding: utf-8 -*-
"""
US High School Biology: Populations and Carrying Capacity (HS-LS2-1, HS-LS2-2)
  python tools/gen_us_science_bio_populations_and_carrying_capacity.py
Use mathematical and/or computational representations to support explanations of factors that affect carrying capacity
of ecosystems at different scales, and of factors affecting biodiversity and populations.
Population change (births, deaths, immigration, emigration), density, exponential and logistic growth, carrying capacity
from data, limiting factors (density-dependent and density-independent), and mark-recapture estimates.
Wrong answers come from real mistakes: "a population keeps growing forever", "a flood is density-dependent",
"multiplying instead of dividing in mark-recapture".
"""
from sci_common import Unit, item, bank, lesson, make, table, comma, People

U = Unit(90108)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ANIM = ["deer", "rabbits", "wolves", "trout", "sparrows", "squirrels", "elk", "frogs", "beetles", "mice"]


def g_change():
    a = R.choice(ANIM)
    n0 = R.randrange(200, 2000, 10)
    b, d, i, e = R.randint(20, 200), R.randint(20, 200), R.randint(0, 40), R.randint(0, 40)
    k = R.choice(["new", "change"])
    if not once((a, n0, b, d)):
        return None
    ch = b + i - d - e
    if k == "change":
        sg = lambda v: ("+" if v >= 0 else "−") + comma(abs(v))
        w = [v for v in dict.fromkeys([b - d + e - i, b + d + i + e, b - d, ch + 10, ch - 10]) if v != ch][:3]
        return item("A population of %s had %d births, %d deaths, %d animals move in and %d move out this year. What is the change in population?" % (a, b, d, i, e),
                    sg(ch), [sg(v) for v in w], "(births + moved in) − (deaths + moved out) = %d + %d − %d − %d = %d." % (b, i, d, e, ch))
    return item("There are %s %s. This year: %d births, %d deaths, %d move in, %d move out. How many next year?" % (comma(n0), a, b, d, i, e), comma(n0 + ch),
                [comma(n0 + b - d), comma(n0 + b + d + i + e), comma(n0 - ch)], "%s + %d = %s." % (comma(n0), ch, comma(n0 + ch)))


def g_density():
    a = R.choice(ANIM)
    area = R.choice([2, 4, 5, 8, 10, 20, 25, 50])
    per = R.randint(3, 60)
    n = area * per
    if not once((a, area, per)):
        return None
    return item("%s %s live in %d km². What is the population density?" % (comma(n), a, area), "%d per km²" % per, ["%s per km²" % comma(n * area), "%d per km²" % (per + area), "%d per km²" % (n - area)],
                "%s ÷ %d = %d." % (comma(n), area, per))


def g_double():
    t = R.choice([20, 30, 60])
    h = R.choice([2, 3, 4, 5, 6])
    start = R.choice([1, 10, 100])
    if not once((t, h, start)):
        return None
    n = h * 60 // t
    a = start * 2 ** n
    return item("%s bacteri%s double%s every %d minutes with unlimited food. How many after %d hours?" % (comma(start), "um" if start == 1 else "a", "s" if start == 1 else "", t, h),
                comma(a), [comma(start * 2 * n), comma(start * 2 ** (n - 1)), comma(start * n)], "%d doublings: %s × 2^%d = %s." % (n, comma(start), n, comma(a)))


def g_logistic():
    a = R.choice(ANIM)
    K = R.randrange(300, 1200, 50)
    years = [0, 2, 4, 6, 8, 10, 12]
    fr = [0.05, 0.15, 0.4, 0.75, 0.93, 0.99, 1.0]
    vals = [int(round(K * f / 10.0)) * 10 for f in fr]
    vals[-2] = K - R.choice([10, 20])
    vals[-1] = K + R.choice([-10, 0, 10])
    k = R.choice(["K", "fast", "why", "ahead"])
    if not once((a, K, k)):
        return None
    tab = table(["Year", "Number of %s" % a], [[str(y), comma(v)] for y, v in zip(years, vals)])
    if k == "K":
        return item(tab + "About what is the carrying capacity for these %s?" % a, "about %s" % comma(K), ["about %s" % comma(vals[3]), "about %s" % comma(2 * K), "about %s" % comma(vals[1])],
                    "The population levels off near %s." % comma(K))
    if k == "fast":
        return item(tab + "Between which years did the %s population grow fastest?" % a, "years 4 to 6", ["years 0 to 2", "years 10 to 12", "years 8 to 10"],
                    "The biggest jump: %s to %s." % (comma(vals[2]), comma(vals[3])))
    if k == "why":
        return item(tab + "Why did the %s population stop growing?" % a, "Limited resources like food and space reached the carrying capacity.", ["The animals stopped having young.", "Populations always stop at 12 years.", "They became a new species."],
                    "Logistic growth levels off.")
    return item(tab + "If nothing changes, what will the %s population most likely be in year 20?" % a, "about %s" % comma(K), ["about %s" % comma(2 * K), "about %s" % comma(4 * K), "zero"],
                "It stays near the carrying capacity.")


FACT = [("disease spreading through a crowded herd", "density-dependent"), ("competition for food", "density-dependent"), ("predators eating more prey when prey are common", "density-dependent"),
        ("parasites passing easily between crowded animals", "density-dependent"), ("a forest fire", "density-independent"), ("a flood", "density-independent"),
        ("a sudden hard freeze", "density-independent"), ("a drought", "density-independent"), ("a volcanic eruption", "density-independent"), ("lack of nesting space", "density-dependent")]


def g_fact():
    s, k = R.choice(FACT)
    if not once(s):
        return None
    return item("Is %s a density-dependent or density-independent limiting factor?" % s, k, ["density-independent" if k == "density-dependent" else "density-dependent", "not a limiting factor", "a biotic increase"],
                "Density-dependent factors get stronger as the population gets crowded.")


def g_mark():
    a = R.choice(ANIM[:6] + ["turtles", "butterflies"])
    M = R.randint(20, 80)
    C = R.randint(20, 80)
    Rr = R.choice([x for x in range(2, 21) if (M * C) % x == 0] or [0])
    if not Rr or not once((a, M, C, Rr)):
        return None
    N = M * C // Rr
    return item("Scientists mark %d %s and release them. Later they catch %d, and %d are marked. Estimate the population (N = marked × caught ÷ recaptured)." % (M, a, C, Rr),
                comma(N), [comma(M * C), comma(M + C), comma(M * Rr // max(1, C) if M * Rr // max(1, C) else M + C + Rr)], "%d × %d ÷ %d = %s." % (M, C, Rr, comma(N)))


B1 = bank([
    ("What is carrying capacity?", "the largest population an environment can support over time", ["the fastest a population can grow", "the number of babies born each year", "the smallest population possible"], "Limited by resources."),
    ("What shape does exponential growth make on a graph?", "a J-shaped curve", ["an S-shaped curve", "a flat line", "a straight downward line"], "Unlimited resources."),
    ("What shape does logistic growth make?", "an S-shaped curve that levels off", ["a J-shaped curve that never stops", "a circle", "a zigzag"], "It reaches carrying capacity."),
    ("What is a limiting factor?", "something that keeps a population from growing larger", ["a factor that always helps growth", "a type of predator only", "a kind of DNA"], "Food, water, space, disease..."),
    ("Which two things increase a population?", "births and immigration", ["deaths and emigration", "births and deaths", "immigration and emigration"], "Coming in or being born."),
    ("What is emigration?", "individuals leaving a population", ["individuals entering a population", "being born", "dying of disease"], "Exit = emigrate."),
    ("Why can't a population grow exponentially forever?", "Resources run out.", ["Animals get bored.", "Genes stop working.", "The sun stops shining."], "Limits slow growth."),
    ("What happens if a population goes above carrying capacity?", "It usually falls back as resources run short.", ["It keeps growing forever.", "It becomes a new species.", "Nothing changes."], "Overshoot and decline."),
])
B5 = bank([
    ("Deer had no predators after wolves were removed. Their population grew, then crashed. Why?", "They ate too much food and went above carrying capacity.", ["Wolves came back that day.", "Deer stopped breeding for no reason.", "The weather got warmer."], "Overshoot."),
    ("Ecologists count 45 snails in a 1 m² quadrat and the field is 200 m². Estimate the snails in the field.", "9,000", ["245", "4,500", "200"], "45 × 200 = 9,000."),
    ("A new predator enters a lake. What is the likely effect on the carrying capacity for its prey?", "It decreases.", ["It increases.", "It stays the same forever.", "It doubles."], "More deaths."),
    ("More rain makes more grass in a park. What happens to the carrying capacity for rabbits?", "It increases.", ["It decreases.", "It drops to zero.", "It cannot change."], "More food."),
    ("A computer model of a fish population levels off at 5,000. What does 5,000 represent?", "the carrying capacity", ["the birth rate", "the starting population", "the number of predators"], "The plateau."),
])


def body():
    think = ("<p><b>Populations grow until limits stop them.</b></p>"
             "<ul><li>Change = (births + immigration) − (deaths + emigration).</li><li>With unlimited resources: exponential (J-curve). With limits: logistic (S-curve) up to the carrying capacity.</li>"
             "<li>Density-dependent limits (food, disease, predators) grow stronger when crowded; density-independent ones (fire, flood) do not.</li></ul>")
    ex = [("500 rabbits; 120 births, 80 deaths, 10 in, 20 out. Next year?", ["(120 + 10) − (80 + 20) = 30"], "530"),
          ("Mark 40, catch 50, 10 marked. N?", ["40 × 50 ÷ 10"], "200")]
    mist = ["Thinking a population keeps growing forever.", "Calling a flood density-dependent. It affects any population size.", "Multiplying all three numbers in mark-recapture."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Population basics", B1 + [(g_change, 6), (g_density, 6)]),
        ("Population math", [(g_change, 10), (g_density, 6), (g_double, 4)]),
        ("Growth curves", [(g_logistic, 12), (g_double, 8)]),
        ("Limiting factors", [(g_fact, 10), (g_mark, 10)]),
        ("Ecology models", B5 + [(g_logistic, 6), (g_mark, 5), (g_double, 4)]),
    ])
    make("biology", "populations-and-carrying-capacity", 8, "HS-LS2-1, HS-LS2-2",
         "Use mathematical and/or computational representations to support explanations of factors that affect carrying capacity of ecosystems at different scales. "
         "Use mathematical representations to support and revise explanations based on evidence about factors affecting biodiversity and populations in ecosystems of different scales.",
         "Populations and Carrying Capacity",
         "Carrying Capacity Worksheets: Population Growth, Limiting Factors (High School Biology)",
         "Populations",
         "Free high school biology worksheets on populations (NGSS HS-LS2-1, HS-LS2-2): population change, density, exponential and logistic growth, carrying capacity and mark-recapture. 100 questions with answers.",
         "Populations grow until limits stop them.",
         "The carrying capacity is the largest population the environment can support.",
         body(),
         [("What is carrying capacity?", "The largest population an environment can support over time, set by food, water, space and other limits."),
          ("What is the difference between exponential and logistic growth?", "Exponential growth speeds up without limit (J-curve). Logistic growth slows and levels off at the carrying capacity (S-curve)."),
          ("How does mark-recapture work?", "Mark some animals, release them, catch a second sample and use N = marked × caught ÷ recaptured.")],
         sets)


if __name__ == "__main__":
    main()
