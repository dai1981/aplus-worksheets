# -*- coding: utf-8 -*-
"""
US Grade 8 Science: Natural Selection (MS-LS4-4, MS-LS4-6)
  python tools/gen_us_science_g8_natural_selection.py
Construct an explanation based on evidence that describes how genetic variations of traits in a population increase
some individuals' probability of surviving and reproducing in a specific environment; use mathematical representations
to support explanations of how natural selection may lead to increases and decreases of specific traits in populations
over time. Variation, overproduction, competition, survival and reproduction, inheritance; percent of a population.
Wrong answers come from real mistakes: "individuals change their traits because they need to", "the strongest always
survive", "a trait that helps in one place helps everywhere", "natural selection happens to one animal in its lifetime".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People, comma

U = Unit(80116)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


SCEN = [("beach mice", "light-colored fur", "dark fur", "on white sand dunes where owls hunt by sight"),
        ("peppered moths", "dark wings", "light wings", "on soot-covered tree trunks where birds hunt"),
        ("rock pocket mice", "dark fur", "light fur", "on black lava rock where hawks hunt"),
        ("bacteria", "resistance to an antibiotic", "no resistance", "in a patient taking that antibiotic"),
        ("insects", "resistance to a pesticide", "no resistance", "in fields sprayed with that pesticide"),
        ("finches", "large, strong beaks", "small beaks", "on an island where a drought leaves only hard seeds"),
        ("rabbits", "white winter fur", "brown winter fur", "in a snowy forest with foxes"),
        ("lizards", "longer legs", "shorter legs", "on an island with wide tree trunks and open ground"),
        ("giraffes", "longer necks", "shorter necks", "where lower leaves are eaten and higher leaves remain"),
        ("fish", "duller colors", "bright colors", "in a stream with many predators")]


def g_which():
    org, good, bad, env = R.choice(SCEN)
    who = P.next()[0]
    t = R.choice(["which", "why", "future"])
    if not once((org, t)):
        return None
    if t == "which":
        return item("%s studies a population of %s with %s or %s %s. Which individuals are most likely to survive and reproduce?" % (who, org, good, bad, env), "those with " + good,
                    ["those with " + bad, "all of them equally", "only the oldest ones"], "The trait that helps in this environment is %s." % good)
    if t == "why":
        return item("%s studies %s %s. Why do individuals with %s leave more offspring?" % (who, org, env, good), "Their trait helps them survive long enough to reproduce and pass it on.",
                    ["They decided to change their trait.", "They are always the strongest.", "Their trait appeared because they needed it."], "Natural selection acts on traits that already vary.")
    return item("%s predicts how %s %s will change over many generations. What is most likely?" % (who, org, env), "The percent with %s will increase." % good,
                ["The percent with %s will increase." % bad, "Every individual will change its trait during its life.", "The traits will stay exactly the same."], "Helpful heritable traits become more common.")


def g_pct():
    who = P.next()[0]
    org, good, bad, env = R.choice(SCEN[:3] + SCEN[5:8])
    tot = R.choice([200, 400, 500, 800, 1000])
    p1 = R.choice([10, 20, 25, 30, 40])
    p2 = p1 + R.choice([20, 25, 30, 40])
    if p2 >= 100:
        return None
    k = R.choice(["count", "change", "trend"])
    if not once((org, tot, p1, p2, k)):
        return None
    rows = [["Generation 1", "%d%%" % p1], ["Generation 10", "%d%%" % p2]]
    tab = table(["%s population" % org.capitalize(), "Percent with %s" % good], rows)
    if k == "count":
        n = tot * p2 // 100
        if tot * p2 % 100:
            return None
        return item(tab + "In %s's data, generation 10 has %s %s. How many have %s?" % (who, comma(tot), org, good), comma(n), [comma(tot * p1 // 100), comma(tot - n), comma(p2)],
                    "%d%% of %s = %s." % (p2, comma(tot), comma(n)))
    if k == "change":
        return item(tab + "By how many percentage points did %s with %s increase in %s's data?" % (org, good, who), "%d percentage points" % (p2 - p1),
                    ["%d percentage points" % p2, "%d percentage points" % (p1 + p2), "%d percentage points" % p1], "%d − %d = %d." % (p2, p1, p2 - p1))
    return item(tab + "These %s live %s. What best explains %s's data?" % (org, env, who), "%s helped more individuals survive and reproduce, so the trait became more common." % good.capitalize(),
                ["Individuals grew %s because they wanted to." % good, "The environment had no effect.", "%s became more common by chance only." % bad.capitalize()],
                "Natural selection increases helpful traits over generations.")


def g_graph():
    who = P.next()[0]
    org, good, bad, env = R.choice(SCEN[:3] + SCEN[5:7])
    start = R.choice([10, 15, 20])
    step = R.choice([10, 15, 20])
    vals = [min(start + step * i, 95) for i in range(5)]
    if not once((org, start, step)):
        return None
    ch = bar_chart(["1", "5", "10", "15", "20"], vals, "% with " + good, "bar graph of the percent of %s with %s over 20 generations" % (org, good), ymax=100, step=20, w=320)
    k = R.choice(["trend", "read"])
    if k == "trend":
        return item(fig(ch) + "%s graphed %s %s (x-axis: generation). What does the graph show?" % (who, org, env), "%s became more common over time." % good.capitalize(),
                    ["%s became less common over time." % good.capitalize(), "The population stayed the same.", "Each animal changed its trait during its life."],
                    "The bars rise across generations.")
    return item(fig(ch) + "Using %s's graph, by how many percentage points did %s rise from generation 1 to generation 10?" % (who, good), "%d" % (vals[2] - vals[0]),
                ["%d" % vals[2], "%d" % (vals[4] - vals[0]), "%d" % (vals[1] - vals[0])], "%d − %d = %d." % (vals[2], vals[0], vals[2] - vals[0]))


B1 = bank([
    ("What is natural selection?", "Individuals with helpful inherited traits survive and reproduce more, so those traits become more common.", ["Individuals change their traits when they need to.", "Only the biggest animals survive.", "Humans choose which animals breed."],
     "Darwin's idea."),
    ("What must be true about a trait for natural selection to act on it?", "It varies among individuals and can be inherited.", ["It is learned during life.", "Every individual has the same version.", "It appears only in adults."], "Variation + inheritance."),
    ("Does natural selection change an individual during its life?", "No. It changes the makeup of a population over generations.", ["Yes, very quickly.", "Yes, only in summer.", "Only in plants."], "Populations evolve; individuals do not."),
    ("Why do most species produce more offspring than can survive?", "Limited food and space create competition, so only some survive.", ["They want large families.", "Every offspring survives.", "It makes the environment bigger."], "Overproduction leads to competition."),
    ("What does 'fitness' mean in natural selection?", "how well an organism survives and reproduces in its environment", ["how fast it can run", "how big its muscles are", "how much it exercises"], "Reproduction is what counts."),
    ("A trait helps a mouse hide on dark rocks. Would it help on white sand?", "No. A trait that helps in one environment may hurt in another.", ["Yes, everywhere.", "Only at night.", "Traits never matter."], "Selection depends on the environment."),
    ("Where do new trait variations come from?", "mutations and the mixing of genes in sexual reproduction", ["the animal's wishes", "exercise", "learning"], "Variation must already exist."),
    ("Why are antibiotic-resistant bacteria a growing problem?", "Antibiotics kill non-resistant bacteria, so resistant ones survive and multiply.", ["Bacteria choose to become resistant.", "Antibiotics make bacteria stronger.", "Resistance is learned."],
     "Natural selection in action."),
])
B5 = bank([
    ("Ava says giraffes stretched their necks and passed longer necks to babies. What is a better explanation?", "Giraffes with longer necks reached more food, survived and reproduced more.", ["She is right.", "Necks grow from exercise.", "Giraffes chose to have long necks."],
     "Traits are inherited, not stretched."),
    ("Leo's island finch data: average beak depth rose from 9.2 mm to 9.8 mm after a drought. How much did it increase?", "0.6 mm", ["9.8 mm", "19 mm", "1.6 mm"], "9.8 − 9.2 = 0.6 mm."),
    ("Mia models selection by removing beads that do not match the background. What happens to bead colors after several rounds?", "Colors that match the background become more common.", ["All colors stay equal.", "Matching colors disappear.", "New colors appear from nowhere."],
     "Camouflage is selected."),
    ("After pollution was cleaned up, light peppered moths increased again. Why?", "Light moths were camouflaged on clean bark again.", ["Moths decided to be light.", "Dark moths moved away.", "Pollution does not affect moths."],
     "Selection follows the environment."),
    ("A population of 500 beetles is 30% green. How many beetles are green?", "150", ["30", "350", "170"], "0.30 × 500 = 150."),
])


def body():
    think = ("<p><b>Natural selection</b> works like this:</p><ol><li><b>Variation</b>: individuals have different inherited traits.</li>"
             "<li><b>Overproduction and competition</b>: more offspring are born than can survive.</li>"
             "<li><b>Selection</b>: individuals with traits that help in <b>that environment</b> survive and reproduce more.</li>"
             "<li><b>Inheritance</b>: they pass the helpful traits on, so the <b>percent</b> of the population with the trait <b>increases over generations</b>.</li></ol>"
             "<p>Individuals do not change their traits because they need to. A trait that helps in one place may hurt in another.</p>")
    ex = [("Dark moths go from 10% to 70% on sooty trees. Change?", ["70 − 10"], "60 percentage points"),
          ("Why did dark moths increase?", ["Camouflage from birds."], "They survived and reproduced more.")]
    mist = ["Thinking individuals change their traits because they need to.",
            "Thinking the strongest always survive. Fitness means surviving and reproducing.",
            "Thinking a helpful trait helps in every environment."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("How natural selection works", B1 + [(g_which, 12)]),
        ("Traits and environments", [(g_which, 14), (g_pct, 6)]),
        ("Population data", [(g_pct, 14), (g_graph, 6)]),
        ("Graphs of change", [(g_graph, 10), (g_pct, 10)]),
        ("Explaining with math", B5 + [g_pct, g_graph, g_which]),
    ])
    make("grade-8", "natural-selection", 16, "MS-LS4-4",
         "Construct an explanation based on evidence that describes how genetic variations of traits in a population increase some individuals' probability of surviving and reproducing in a specific environment.",
         "Natural Selection",
         "Grade 8 Natural Selection Worksheets: Variation, Survival, Adaptation and Population Data",
         "Natural Selection",
         "Free middle school science worksheets on natural selection (NGSS MS-LS4-4, MS-LS4-6): variation, competition, survival and reproduction, and using percentages and graphs to show how traits change in populations. 100 practice questions with answers.",
         "Helpful inherited traits become more common.",
         "Individuals with traits that fit their environment survive and reproduce more, so those traits increase over generations.",
         body(),
         [("How does natural selection work?", "Individuals vary in inherited traits. Those with traits that help in their environment survive and reproduce more, so the traits become more common over generations."),
          ("Do animals change their traits because they need to?", "No. Traits vary because of genes. Natural selection changes how common each trait is in a population over many generations."),
          ("How can math show natural selection?", "By tracking the percent of a population with a trait over generations, using tables and graphs to see whether it increases or decreases.")],
         sets)


if __name__ == "__main__":
    main()
