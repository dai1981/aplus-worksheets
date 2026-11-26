# -*- coding: utf-8 -*-
"""
UK Year 2 science: Animals and Their Young (Animals, including humans)
  python tools/gen_uk_science_y2_animals_and_their_young.py
Notice that animals, including humans, have offspring which grow into adults: names of baby animals, young that look
like their parents and young that do not (tadpoles, caterpillars), simple life cycles (frog, butterfly, chicken), and
how humans grow from baby to adult. Reuses the life-cycle step question of the Year 5 unit (new seed).
Wrong answers come from real mistakes: "a tadpole is a baby fish", "all babies look like their parents",
"a caterpillar is a kind of worm", "a puppy grows into a cat".
"""
import uk_sci
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import gen_uk_science_y5_life_cycles as L5
import sci_kids as K
from sci_phys import uniq

L5.U = Unit(61207)
L5.R = L5.U.R
L5.P = People(L5.R)
uk_sci.USED.clear()
U, R, P = L5.U, L5.R, L5.P
L5.CYC = {"frog": ["frogspawn (eggs)", "tadpole", "froglet", "adult frog"],
          "butterfly": ["egg", "caterpillar", "chrysalis", "adult butterfly"],
          "chicken": ["egg", "chick", "young chicken", "adult hen"],
          "human": ["baby", "child", "teenager", "adult"],
          "dog": ["puppy", "young dog", "adult dog", "old dog"]}

BABY = [("cat", "a kitten"), ("dog", "a puppy"), ("cow", "a calf"), ("sheep", "a lamb"), ("horse", "a foal"), ("hen", "a chick"), ("duck", "a duckling"),
        ("frog", "a tadpole"), ("butterfly", "a caterpillar"), ("pig", "a piglet"), ("goat", "a kid"), ("kangaroo", "a joey"), ("fox", "a cub"),
        ("goose", "a gosling"), ("owl", "an owlet"), ("swan", "a cygnet"), ("deer", "a fawn"), ("rabbit", "a kit")]


def g_baby():
    a, b = R.choice(BABY)
    k = R.random() < 0.5
    if not once(("ba", a, k)):
        return None
    if k:
        return item("What is a baby %s called?" % a, b, R.sample([x[1] for x in BABY if x[1] != b], 3), "Many baby animals have special names.")
    return item("What does %s grow up to be?" % b, "a " + a if a[0] not in "aeiou" else "an " + a, R.sample(["a " + x[0] if x[0][0] not in "aeiou" else "an " + x[0] for x in BABY if x[1] != b], 3),
                "Young animals grow into adults of the same kind.")


LIKE = [("a kitten", True), ("a puppy", True), ("a lamb", True), ("a foal", True), ("a calf", True), ("a piglet", True), ("a human baby", True),
        ("a tadpole", False), ("a caterpillar", False), ("a ladybird larva", False), ("a maggot (a young fly)", False), ("a mealworm (a young beetle)", False)]


def g_like():
    b, y = R.choice(LIKE)
    if not once(("li", b)):
        return None
    a = "Yes, it looks like a small adult." if y else "No, it looks very different and changes as it grows."
    return item("Does %s look like its parents?" % b, a, ["No, it looks very different and changes as it grows." if y else "Yes, it looks like a small adult.", "It does not have parents.", "It looks like a plant."],
                "Mammals look like small adults. Frogs and many insects change shape as they grow.")


HUM = ["baby", "toddler", "child", "teenager", "adult", "older adult"]


def g_human():
    i, j = sorted(R.sample(range(len(HUM)), 2))
    k = R.random() < 0.5
    if k:
        if not once(("hp", i, j)):
            return None
        a, b = HUM[i], HUM[j]
        o = [a, b] if R.random() < 0.5 else [b, a]
        return item("Which comes first as a person grows up: %s or %s?" % tuple(("a " if x[0] not in "aeiou" else "an ") + x for x in o), ("a " if a[0] not in "aeiou" else "an ") + a,
                    [("a " if b[0] not in "aeiou" else "an ") + b, "They happen at the same time.", "People do not change."], "Baby → toddler → child → teenager → adult → older adult.")
    i = R.randrange(len(HUM) - 1)
    if not once(("hn", i)):
        return None
    a = HUM[i + 1]
    return item("A person is a %s. What will they be next?" % HUM[i], ("a " if a[0] not in "aeiou" else "an ") + a,
                [("a " if x[0] not in "aeiou" else "an ") + x for x in R.sample([x for x in HUM if x not in (a, HUM[i])], 3)], "Baby → toddler → child → teenager → adult → older adult.")


def g_weigh():
    who = P.next()[0]
    w = [R.choice([3, 4]), R.choice([9, 10, 11]), R.choice([18, 20, 22]), R.choice([30, 35, 40]), R.choice([55, 60, 65])]
    ages = ["newborn", "1 year", "5 years", "10 years", "adult"]
    k = R.choice(["read", "pattern", "diff"])
    ri = R.randrange(5)
    if not once(("we", tuple(w), k, ri if k == "read" else 0)) or (k == "pattern" and not once(("wp",), 2)):
        return None
    tab = table(["Age", "Typical mass (kg)"], [[a, str(x)] for a, x in zip(ages, w)])
    intro = tab + "%s found out how a person's mass changes as they grow. " % who
    if k == "read":
        g = "%d kg" % w[ri]
        who_ = {0: "a newborn baby", 4: "an adult"}.get(ri, "a child aged " + ages[ri])
        return item(intro + "What is the typical mass of %s?" % who_, g, uniq(g, ["%d kg" % x for x in w]), "Read the row.")
    if k == "pattern":
        return item(intro + "What does the table show?", "People get heavier as they grow up.", ["People get lighter as they grow.", "People stay the same mass.", "Babies are the heaviest."], "The numbers go up.")
    d = w[3] - w[1]
    g = "%d kg" % d
    return item(intro + "How much heavier is a 10-year-old than a 1-year-old?", g, uniq(g, ["%d kg" % w[3], "%d kg" % w[1], "%d kg" % (w[3] + w[1]), "%d kg" % (d + 5)]), "%d − %d = %d kg." % (w[3], w[1], d))


B1 = bank([
    ("What are offspring?", "the young (babies) of a living thing", ["the oldest animals", "the food animals eat", "the home of an animal"], "Animals have offspring."),
    ("What does a caterpillar grow into?", "a butterfly", ["a worm", "a snake", "a bird"], "It changes inside a chrysalis."),
    ("What does a tadpole grow into?", "a frog", ["a fish", "a newt only", "a snail"], "Tadpoles grow legs."),
    ("What hatches out of a hen's egg?", "a chick", ["a duckling", "a kitten", "a tadpole"], "It grows into a hen or a cockerel."),
    ("Which animals give birth to live babies and feed them milk?", "mammals, such as cows and humans", ["birds", "fish", "insects"], "Mammals feed milk."),
    ("Which animals lay eggs with hard shells?", "birds", ["cows", "dogs", "horses"], "Hens, ducks and robins."),
    ("What does a puppy grow into?", "a dog", ["a cat", "a fox", "a wolf cub"], "Young grow into adults of the same kind."),
    ("Do all animals have babies that look like them?", "No. Tadpoles and caterpillars look very different from their parents.", ["Yes, always.", "Only birds do.", "No animals do."], "Some change shape."),
])
B5 = bank([
    ("Why do baby birds stay in the nest at first?", "They cannot fly or find food yet, so their parents feed them.", ["They are too big.", "Nests are warm only in winter.", "They are asleep for a year."], "Parents care for young."),
    ("How do human babies need looking after?", "They need milk, warmth, sleep and someone to care for them.", ["They can look after themselves.", "They only need toys.", "They need nothing."], "Adults care for babies."),
    ("Why does a frog lay so many eggs?", "Many eggs and tadpoles are eaten, so only a few grow into frogs.", ["Frogs like counting.", "Every egg always becomes a frog.", "Eggs are too small to see."], "Lots of offspring."),
    ("How could you find out how a baby changes as it grows?", "Look at photos of the same person at different ages.", ["Look at one photo only.", "Guess.", "Ask a pet."], "Compare over time."),
    ("Which grows the most in one year: a newborn baby or an adult?", "a newborn baby", ["an adult", "both the same", "neither grows"], "Adults have stopped growing taller."),
])


def body():
    pic = K.row(["egg", "bird", "bird"], words=["egg", "chick", "hen"], size=90, label="an egg hatches into a chick, which grows into a hen")
    ex = [("A baby sheep is called?", ["A young sheep"], "a lamb"),
          ("What does a tadpole grow into?", ["It grows legs"], "a frog")]
    mist = ["Thinking a tadpole is a baby fish.", "Thinking all babies look like their parents.", "Thinking a caterpillar is a kind of worm."]
    return kid_lesson(pic, "Animals have young that grow into adults.",
                      ["A kitten grows into a cat; a lamb grows into a sheep.", "Some young look very different, like tadpoles and caterpillars.", "People grow from baby to child to adult."], ex, mist)


def main():
    sets = U.sets([
        ("Baby animals", B1 + [(g_baby, 12)]),
        ("Who grows into what?", [(g_baby, 14), (g_like, 6)]),
        ("Life cycles", [(L5.g_next, 14), (g_like, 6)]),
        ("Growing up", [(g_human, 12), (g_weigh, 8)]),
        ("Caring for young", B5 + [(g_weigh, 6), (g_human, 5), (g_baby, 4)]),
    ])
    make_uk(2, "animals-and-their-young", 7, "Animals, including humans",
            "Notice that animals, including humans, have offspring which grow into adults.",
            "Animals and Their Young",
            "Year 2 Science: Animals and Their Young Worksheets (Offspring and Life Cycles)",
            "Animals and Their Young",
            "Free Year 2 science worksheets on animals and their young: baby animal names, young that look like their parents or change, simple life cycles and how people grow. 100 questions with answers.",
            "Young animals grow into adults.",
            "A lamb grows into a sheep. A tadpole changes into a frog.",
            body(),
            [("What are offspring?", "Offspring are the young of a living thing. Kittens are the offspring of cats."),
             ("Do all babies look like their parents?", "No. Kittens and lambs look like small adults, but tadpoles and caterpillars look very different and change as they grow."),
             ("How do people grow?", "A person grows from a baby to a toddler, a child, a teenager and then an adult.")],
            sets)


if __name__ == "__main__":
    main()
