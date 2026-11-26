# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Variation and Survival (3-LS4-2)
  python tools/gen_us_science_g3_variation_and_survival.py
Differences in characteristics among individuals of the same species can give advantages in surviving,
finding mates and reproducing: color that matches the background (camouflage), longer thorns,
faster legs, thicker fur, brighter feathers that attract mates, longer roots.
Students use data (how many of each kind survived) as evidence.
Wrong answers come from real mistakes: "every individual of a species is the same", "the animal changes
its color because it wants to", "the biggest always survives".
"""
from sci_common import Unit, item, bank, lesson, make, table, fig, bar_chart, People

U = Unit(30110)
R = U.R
P = People(R)

# (species, trait A, trait B, setting, which survives better, why)
CASES = [("moths", "light-colored", "dark-colored", "on dark, sooty tree trunks", 1, "Birds cannot see the dark moths as easily on the dark bark."),
         ("moths", "light-colored", "dark-colored", "on light, pale tree trunks", 0, "The light moths blend in with the pale bark."),
         ("beetles", "green", "brown", "on green leaves", 0, "Green beetles are hard for birds to see on green leaves."),
         ("mice", "brown", "white", "in a brown, dry field", 0, "Owls have a harder time spotting brown mice on brown ground."),
         ("rabbits", "white", "brown", "in snowy winter fields", 0, "White rabbits blend in with the snow."),
         ("cactuses", "short-spined", "long-spined", "in a desert with hungry animals", 1, "Animals avoid biting the plants with long spines."),
         ("deer", "slower", "faster", "where wolves hunt", 1, "Faster deer can run away from wolves."),
         ("foxes", "thin-furred", "thick-furred", "during a very cold winter", 1, "Thick fur keeps them warm."),
         ("sunflowers", "short-rooted", "long-rooted", "during a long dry summer", 1, "Longer roots can reach water deeper in the soil."),
         ("frogs", "bright green", "dull brown", "on a muddy pond bank", 1, "Brown frogs blend in with the mud."),
         ("lizards", "sandy-colored", "black", "on light desert sand", 0, "Sandy lizards are hard for hawks to see on the sand."),
         ("crabs", "red", "sand-colored", "on a sandy beach", 1, "Sand-colored crabs blend in with the beach.")]


def g_case():
    sp, a, b, setting, win, why = R.choice(CASES)
    p = P.next()
    t = [a, b]
    return item("%s studies %s living %s. Some are %s and some are %s. Which ones are more likely to survive?" % (p[0], sp, setting, a, b),
                "the %s %s" % (t[win], sp), ["the %s %s" % (t[1 - win], sp), "They survive equally well.", "Neither kind can survive."], why)


def g_data():
    sp, a, b, setting, win, why = R.choice(CASES)
    start = R.choice([20, 30, 40, 50])
    good = R.randint(start // 2 + 3, start - 2)
    bad = R.randint(2, start // 2 - 2)
    surv = [0, 0]
    surv[win], surv[1 - win] = good, bad
    t = [a, b]
    p = P.next()
    rows = [["%s %s" % (t[0], sp), "%d" % start, "%d" % surv[0]], ["%s %s" % (t[1], sp), "%d" % start, "%d" % surv[1]]]
    tab = table(["Kind", "At the start", "Still alive after one year"], rows)
    k = R.choice(["which", "claim", "num"])
    if k == "which":
        return item(tab + "Scientists counted %s living %s. Which kind survived better?" % (sp, setting), "the %s %s" % (t[win], sp),
                    ["the %s %s" % (t[1 - win], sp), "They survived the same.", "Neither survived."], "%d survived compared with %d." % (good, bad))
    if k == "claim":
        return item(tab + "%s reads this data about %s living %s. Which claim does it support?" % (p[0], sp, setting),
                    "Being %s gives these %s an advantage here." % (t[win], sp),
                    ["Being %s gives these %s an advantage here." % (t[1 - win], sp), "Color and body features do not matter.", "All the %s are exactly the same." % sp], why)
    return item(tab + "How many more %s %s than %s %s were still alive after one year?" % (t[win], sp, t[1 - win], sp), "%d" % (good - bad),
                ["%d" % good, "%d" % bad, "%d" % (good + bad)], "%d − %d = %d." % (good, bad, good - bad))


MATES = [("peacocks", "with bigger, brighter tail feathers", "Females choose males with bright tails, so these males have more young."),
         ("male cardinals", "with brighter red feathers", "Brighter males attract more mates."),
         ("frogs", "with louder calls", "Females find and choose males with louder calls."),
         ("male deer", "with larger antlers", "Larger antlers help males win contests and attract mates."),
         ("flowers", "with brighter petals", "More bees visit them, so they make more seeds."),
         ("flowers", "with a stronger smell", "More insects find them, so they make more seeds.")]


def g_mate():
    sp, trait, why = R.choice(MATES)
    p = P.next()
    seeds = "make more seeds" if sp == "flowers" else "have more young"
    return item("%s sees that some %s grow up %s. Why might these %s %s?" % (p[0], sp, trait, sp, seeds), why,
                ["They decided to grow them.", "All of them are exactly the same.", "It makes them hide from predators better."], why)


B1 = bank([
    ("What is variation?", "differences in traits among living things of the same kind", ["all members of a species are the same", "a kind of habitat", "a type of weather"],
     "No two rabbits are exactly alike."),
    ("What is camouflage?", "a color or pattern that helps a living thing blend in with its surroundings", ["a loud call", "a kind of food", "a sharp tooth"],
     "Blending in helps animals hide from predators."),
    ("Why can small differences help an animal survive?", "Some differences make it easier to find food, hide or stay warm.", ["Differences never matter.", "Animals choose their differences.", "Only big animals survive."],
     "Traits that help survival are an advantage."),
    ("A brown rabbit and a white rabbit live in a snowy place. Which is easier for a fox to see?", "the brown rabbit", ["the white rabbit", "They are equally easy to see.", "Neither can be seen."],
     "The white rabbit blends in."),
    ("Does an animal change its color because it wants to blend in?", "No. Animals are born with color differences, and some colors help more.", ["Yes, always.", "Only birds do.", "Only in winter."],
     "Variation is already there when the animals are born."),
    ("What does an advantage mean for a living thing?", "a trait that helps it survive or have young", ["a trait that hurts it", "a kind of home", "the color of its food"],
     "Advantages help individuals survive and reproduce."),
    ("Why do plants with longer roots survive dry summers better?", "Longer roots reach water deeper in the soil.", ["Long roots make rain.", "Short roots hold more water.", "Roots do not need water."],
     "The trait helps the plant get water."),
    ("Which trait could help a male bird find a mate?", "bright, colorful feathers", ["dull feathers that blend in", "a broken wing", "a quiet call nobody hears"],
     "Bright colors and songs attract mates."),
])
B5 = bank([
    ("Ava puts 20 green and 20 red paper bugs on green grass. Friends pick up as many as they can in 1 minute. Which color will most likely be left?", "green", ["red", "They will be left equally.", "neither"],
     "Green bugs blend in with green grass."),
    ("Leo's data shows more dark moths survived on dark trees. What should he do to check his result?", "repeat the count in other places and years", ["stop counting", "count only light moths", "paint the trees"],
     "More data makes evidence stronger."),
    ("Mia sees that most of the mice in a dark forest are dark brown. What is the best explanation?", "Dark mice were harder for owls to see, so more of them survived and had young.", ["Mice chose to be dark.", "Owls like dark mice.", "Light mice moved to the moon."],
     "Variation plus survival changes which traits are common."),
    ("Some sunflowers in a field grow taller than others. How might being taller help?", "Taller plants get more sunlight.", ["Taller plants need no water.", "Taller plants are invisible.", "Taller plants have no roots."],
     "More light means more food made."),
    ("Noah reads that cheetahs that run faster catch more food. What does this show?", "Running speed is an advantage for cheetahs.", ["Speed does not matter.", "Slow cheetahs catch more food.", "Cheetahs do not need food."],
     "Faster cheetahs survive better."),
])


def body():
    think = ("<p>Living things of the same kind are not all exactly alike. These differences are called <b>variation</b>.</p>"
             "<p>Some differences give an <b>advantage</b>: they help an individual <b>survive</b>, find a <b>mate</b> or have more young.</p>"
             "<ul><li><b>Camouflage</b>: colors that blend in help animals hide from predators.</li>"
             "<li>Longer spines, faster legs, thicker fur and longer roots help in some places.</li>"
             "<li>Brighter feathers or louder calls can help animals attract mates.</li></ul>"
             "<p>Which trait is best depends on the <b>environment</b>: white fur helps in snow but not in a brown field.</p>")
    ex = [("Green and brown beetles live on green leaves. Which survive better?", ["Green beetles blend in.", "Birds see brown ones more easily."], "the green beetles"),
          ("Why do some deer escape wolves better?", ["Some deer are faster."], "Faster deer can run away.")]
    mist = ["Thinking all members of a species are exactly the same.",
            "Thinking animals change their traits because they want to.",
            "Forgetting that the best trait depends on the environment."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Variation and advantages", B1 + [(g_case, 6), (g_mate, 6)]),
        ("Which ones survive?", [(g_case, 14), (g_mate, 6)]),
        ("Survival data", [(g_data, 16), (g_case, 4)]),
        ("Finding mates and having young", [(g_mate, 10), (g_data, 10)]),
        ("Investigations", B5 + [g_data, g_case, g_mate]),
    ])
    make("grade-3", "variation-and-survival", 10, "3-LS4-2",
         "Use evidence to construct an explanation for how the variations in characteristics among individuals of the same species may provide advantages in surviving, finding mates, and reproducing.",
         "Variation and Survival",
         "Grade 3 Variation Worksheets: How Differences Help Animals and Plants Survive",
         "Variation and Survival",
         "Free Grade 3 science worksheets on variation and survival (NGSS 3-LS4-2): camouflage, traits that give an advantage, attracting mates, and survival data tables. 100 practice questions with answers.",
         "Some differences help living things survive.",
         "Members of a species vary. A trait like camouflage or long roots can help some individuals survive and have young.",
         body(),
         [("What is variation?", "Variation means the differences in traits among members of the same species, like fur color or speed."),
          ("How can variation help an animal survive?", "A trait like camouflage, speed or thick fur can help it hide, escape or stay warm, so it is more likely to survive and have young."),
          ("Does the best trait depend on the environment?", "Yes. White fur helps a rabbit hide in snow, but brown fur is better in a brown field.")],
         sets)


if __name__ == "__main__":
    main()
