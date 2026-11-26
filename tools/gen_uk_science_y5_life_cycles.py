# -*- coding: utf-8 -*-
"""
UK Year 5 science: Life Cycles (Living things and their habitats)
  python tools/gen_uk_science_y5_life_cycles.py
The life cycles of a mammal, an amphibian, an insect (complete and incomplete metamorphosis) and a bird; the order of
stages, how the cycles differ, and gestation and incubation times.
Wrong answers come from real mistakes: "all animals lay eggs", "a tadpole is a fish", "a caterpillar is a different
animal from a butterfly", "every insect has a pupa stage".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once
from sci_phys import uniq

U = Unit(61501)
R = U.R
P = People(R)

CYC = {"frog": ["frogspawn (eggs)", "tadpole", "froglet", "adult frog"],
       "butterfly": ["egg", "caterpillar (larva)", "chrysalis (pupa)", "adult butterfly"],
       "chicken": ["egg", "chick", "young chicken", "adult hen"],
       "human": ["baby", "child", "teenager", "adult"],
       "ladybird": ["egg", "larva", "pupa", "adult ladybird"],
       "grasshopper": ["egg", "nymph", "larger nymph", "adult grasshopper"],
       "dog": ["puppy", "young dog", "adult dog", "old dog"]}
GROUP = {"frog": "amphibian", "butterfly": "insect", "chicken": "bird", "human": "mammal", "ladybird": "insect", "grasshopper": "insect", "dog": "mammal"}


def g_next():
    a = R.choice(sorted(CYC))
    st = CYC[a]
    i = R.randrange(len(st) - 1)
    k = R.random() < 0.5
    if not once(("nx", a, i, k)):
        return None
    if k:
        ans = st[i + 1]
        return item("In the life cycle of a %s, which stage comes after the %s?" % (a, st[i]), ans, [x for x in st if x not in (ans, st[i])] + [R.choice(["pupa", "seed", "spore"]) if a not in ("butterfly", "ladybird") else "seed"],
                    "%s life cycle: %s." % (a.capitalize(), " → ".join(st)))
    ans = st[i]
    return item("In the life cycle of a %s, which stage comes just before the %s?" % (a, st[i + 1]), ans, [x for x in st if x not in (ans, st[i + 1])] + ["seed"],
                "%s life cycle: %s." % (a.capitalize(), " → ".join(st)))


def g_stage():
    a = R.choice(sorted(CYC))
    s = R.choice(CYC[a][:-1])
    if s == "egg" or not once(("sg", a, s)):
        return None
    w = R.sample([x for x in CYC if x != a and s not in CYC[x]], 3)
    return item("Which animal has %s \"%s\" stage in its life cycle?" % ("an" if s[0] in "aeiou" else "a", s), a, w, "%s life cycle: %s." % (a.capitalize(), " → ".join(CYC[a])))


def g_group():
    a = R.choice(sorted(GROUP))
    if not once(("gp", a)):
        return None
    g = GROUP[a]
    return item("A %s's life cycle is typical of which group?" % a, g + "s", [x + "s" for x in ["mammal", "amphibian", "insect", "bird"] if x != g],
                "%s is %s." % (("A " + a) if a != "human" else "A human", ("an " if g[0] in "aeiou" else "a ") + g))


FEAT = [("lay eggs with hard shells and keep them warm", "birds"), ("give birth to live young and feed them milk", "mammals"),
        ("lay jelly-covered eggs in water; the young live in water and breathe with gills", "amphibians"),
        ("change completely from larva to pupa to adult", "insects such as butterflies"), ("have young that look like small versions of the adult", "mammals and birds"),
        ("change from a water-living young to a land-living adult", "amphibians")]


def g_feat():
    f, g = R.choice(FEAT)
    if not once(("ft", f)):
        return None
    opts = ["birds", "mammals", "amphibians", "insects such as butterflies", "mammals and birds"]
    return item("Which animals %s?" % f, g, R.sample([x for x in opts if x != g and not (g == "mammals and birds" and x in ("mammals", "birds")) and not (g in ("mammals", "birds") and x == "mammals and birds")], 3),
                "Life cycles differ between groups of animals.")


TIME = [("an elephant", 22, "months"), ("a human", 9, "months"), ("a cat", 2, "months"), ("a dog", 2, "months"), ("a horse", 11, "months"), ("a blue whale", 11, "months"),
        ("a chicken egg", 21, "days"), ("a duck egg", 28, "days"), ("a robin egg", 13, "days"), ("a swan egg", 35, "days")]


def g_time():
    a, b = R.sample(TIME, 2)
    if a[2] != b[2] or a[1] == b[1]:
        return None
    k = R.random() < 0.5
    if not once(("tm", tuple(sorted((a[0], b[0]))), k)):
        return None
    word = "gestation (time growing inside the mother)" if a[2] == "months" else "incubation (time inside the egg)"
    if k:
        d = abs(a[1] - b[1])
        g = "%d %s" % (d, a[2])
        return item("The %s of %s is about %d %s and of %s about %d %s. What is the difference?" % (word, a[0], a[1], a[2], b[0], b[1], b[2]), g,
                    uniq(g, ["%d %s" % (a[1] + b[1], a[2]), "%d %s" % (max(a[1], b[1]), a[2]), "%d %s" % (d + 2, a[2]), "%d %s" % (d, "weeks")]), "%d − %d = %d." % (max(a[1], b[1]), min(a[1], b[1]), d))
    big = a if a[1] > b[1] else b
    return item("Which takes longer: the %s of %s (about %d %s) or of %s (about %d %s)?" % (word, a[0], a[1], a[2], b[0], b[1], b[2]), big[0],
                [(b if big is a else a)[0], "They take the same time.", "Neither has a life cycle."], "Compare the numbers.")


B1 = bank([
    ("What is a life cycle?", "the stages a living thing goes through from birth to adult and producing young", ["the way an animal moves", "a type of bicycle race", "the food chain an animal is in"], "Born, grow, reproduce, die."),
    ("What is metamorphosis?", "a big change in body shape during the life cycle", ["a type of egg", "an animal's habitat", "a kind of food"], "Tadpole to frog, caterpillar to butterfly."),
    ("Which stage of a butterfly's life cycle is the pupa?", "the chrysalis", ["the egg", "the caterpillar", "the adult"], "Inside, the body is rebuilt."),
    ("Do all animals lay eggs?", "No. Most mammals give birth to live young.", ["Yes, every animal does.", "Only mammals lay eggs.", "No animals lay eggs."], "Mammals feed young on milk."),
    ("Is a tadpole a fish?", "No. It is a young frog, an amphibian.", ["Yes, it is a fish.", "It is an insect.", "It is a plant."], "It grows legs and lungs."),
    ("Which insects do NOT have a pupa stage?", "grasshoppers, which grow from nymphs", ["butterflies", "ladybirds", "bees"], "Incomplete metamorphosis."),
    ("Who was a naturalist famous for watching animals in the wild, such as chimpanzees?", "Jane Goodall", ["Isaac Newton", "Mary Anning", "Alexander Fleming"], "She studied chimpanzees in Tanzania."),
    ("Which British naturalist presents wildlife programmes and has filmed many life cycles?", "David Attenborough", ["William Harvey", "Charles Babbage", "Isambard Kingdom Brunel"], "Life on Earth and Planet Earth."),
])
B5 = bank([
    ("Why do many frogs lay thousands of eggs?", "Most eggs and tadpoles are eaten, so laying many means some survive.", ["Frogs cannot count.", "All of them always survive.", "Eggs are their food."], "Survival in numbers."),
    ("Why do birds sit on their eggs?", "to keep them warm so the chicks can develop", ["to hide them from the sun", "to make them harder", "to cool them down"], "Incubation."),
    ("How is a mammal's life cycle different from a butterfly's?", "A mammal's young look like small adults; a butterfly changes completely.", ["They are exactly the same.", "Mammals have a pupa stage.", "Butterflies feed young milk."], "Metamorphosis vs. growth."),
    ("Why do larger mammals usually have longer gestation periods?", "Their young take longer to grow big and developed enough to be born.", ["They are lazy.", "They have more eggs.", "Gestation is always 9 months."], "Size and development."),
    ("How could you study the life cycle of a butterfly in class?", "keep caterpillars in a butterfly habitat and record changes each day", ["catch adult butterflies only", "read about fish", "draw it once without looking"], "Observe over time."),
])


def body():
    think = ("<p><b>All living things have a life cycle, but the stages differ.</b></p>"
             "<ul><li>Mammal: born live, fed on milk, grows into an adult. Bird: hard-shelled egg kept warm, chick, adult.</li>"
             "<li>Amphibian: jelly eggs in water → tadpole → froglet → adult (metamorphosis).</li>"
             "<li>Insect: egg → larva → pupa → adult (complete), or egg → nymph → adult (incomplete).</li></ul>")
    ex = [("After the caterpillar comes?", ["Egg → caterpillar → chrysalis → butterfly"], "the chrysalis (pupa)"),
          ("Elephant 22 months, human 9 months. Difference?", ["22 − 9"], "13 months")]
    mist = ["Thinking all animals lay eggs.", "Thinking a tadpole is a fish.", "Thinking every insect has a pupa stage."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Life cycles", B1 + [(g_group, 6), (g_feat, 6)]),
        ("Stages in order", [(g_next, 14), (g_stage, 6)]),
        ("Comparing life cycles", [(g_stage, 10), (g_next, 6), (g_group, 1), (g_time, 3)]),
        ("Growing times", [(g_time, 16), (g_next, 4)]),
        ("Thinking like a naturalist", B5 + [(g_time, 8), (g_next, 4), (g_stage, 3)]),
    ])
    make_uk(5, "life-cycles", 1, "Living things and their habitats",
            "Describe the differences in the life cycles of a mammal, an amphibian, an insect and a bird.",
            "Life Cycles",
            "Year 5 Science: Life Cycles Worksheets (Mammal, Amphibian, Insect and Bird)",
            "Life Cycles",
            "Free Year 5 science worksheets on life cycles: mammals, amphibians, insects and birds, metamorphosis, the order of stages and gestation times. 100 questions with answers.",
            "Every animal has a life cycle.",
            "Mammals, birds, amphibians and insects grow up in different ways.",
            body(),
            [("How are life cycles different?", "Mammals give birth to live young; birds lay hard-shelled eggs; amphibians start as tadpoles in water; many insects change completely from larva to pupa to adult."),
             ("What is metamorphosis?", "A big change in body shape during the life cycle, such as a tadpole turning into a frog or a caterpillar turning into a butterfly."),
             ("What is a gestation period?", "The time a baby mammal grows inside its mother, from about 2 months for a cat to about 22 months for an elephant.")],
            sets)


if __name__ == "__main__":
    main()
