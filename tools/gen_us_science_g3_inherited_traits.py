# -*- coding: utf-8 -*-
"""
US Grade 3 Science: Inherited Traits (3-LS3-1)
  python tools/gen_us_science_g3_inherited_traits.py
Plants and animals have traits inherited from their parents, and there is variation of these traits
among a group of similar organisms (siblings look alike but are not identical).
Inherited traits (eye color, fur color, petal color, leaf shape, ear shape) vs. traits that are learned
or caused by the environment (a scar, riding a bike, a short haircut, speaking a language).
Assessment boundary: no genetic mechanisms or prediction of traits.
Wrong answers come from real mistakes: "a puppy can inherit a trait neither parent family has",
"learned skills are inherited", "siblings are always exactly the same".
"""
from sci_common import Unit, item, bank, lesson, make, table, People

U = Unit(30107)
R = U.R
P = People(R)

INH = ["eye color", "the shape of your ears", "natural hair color", "freckles", "the color of a dog's fur", "the number of legs a spider has",
       "the shape of a maple leaf", "the color of a rose's petals", "a cat's long tail", "a zebra's stripes", "curly hair", "the shape of a bird's beak",
       "the size of an elephant's ears", "the color of a tiger's fur", "a giraffe's long neck"]
NOT_INH = ["riding a bike", "a scar on your knee", "speaking Spanish", "a short haircut", "reading a book", "a dog sitting when told to", "playing the piano",
           "a tan from the sun", "a broken branch on a tree", "a parrot saying “hello”", "pierced ears", "knowing how to swim", "a bird's broken wing", "a sunburn"]


def g_which():
    k = R.choice(["inh", "not"])
    p = P.next()
    if k == "inh":
        return item("%s makes a list of traits. Which one is inherited from parents?" % p[0], R.choice(INH), R.sample(NOT_INH, 3),
                    "Inherited traits are passed from parents to offspring. Skills and injuries are not inherited.")
    return item("%s makes a list. Which one is NOT an inherited trait?" % p[0], R.choice(NOT_INH), R.sample(INH, 3),
                "It is learned or caused by the environment, not passed down from parents.")


def g_classify():
    k = R.choice(["inh", "not"])
    x = R.choice(INH if k == "inh" else NOT_INH)
    return item("Is “%s” an inherited trait, or is it learned or caused by the environment?" % x,
                "inherited from parents" if k == "inh" else "learned or caused by the environment",
                ["learned or caused by the environment" if k == "inh" else "inherited from parents", "Both parents must teach it.", "It comes from the food only."],
                "%s is %s." % (x[0].upper() + x[1:], "passed down from parents" if k == "inh" else "not passed down from parents"))


PAIRS = [("dog", "puppies", "fur", ["black", "brown", "white", "spotted", "golden"]),
         ("cat", "kittens", "fur", ["gray", "orange", "black", "white", "striped"]),
         ("rabbit", "baby rabbits", "fur", ["white", "brown", "black", "gray"]),
         ("pea plant", "seedlings", "flowers", ["purple", "white"]),
         ("guinea pig", "babies", "fur", ["white", "brown", "black", "tan"]),
         ("horse", "foals", "coat", ["brown", "black", "white", "gray"])]


def g_offspring():
    an, kids, part, cols = R.choice([x for x in PAIRS if x[2] != "flowers"])
    a, b = R.sample(cols, 2)
    odd = R.choice(["green", "purple", "purple and green", "bright pink"])
    if odd in (a, b):
        return None
    p = P.next()
    return item("%s has a %s with %s %s and a %s with %s %s. They have %s. Which %s color would be most surprising?" % (p[0], an, a, part, an, b, part, kids, part),
                odd, [a, b, "a mix of %s and %s" % (a, b)],
                "Offspring inherit traits from their parents, so the %s will most likely have %s, %s or a mix like their parents." % (kids, a, b))


def g_var():
    an, kids, part, cols = R.choice(PAIRS[:3] + PAIRS[4:])
    p = P.next()
    n = R.randint(4, 7)
    counts = [R.randint(1, n - 1)]
    counts.append(n - counts[0])
    a, b = R.sample(cols, 2)
    rows = [[a, "%d" % counts[0]], [b, "%d" % counts[1]]]
    k = R.choice(["why", "total"])
    tab = table(["%s color" % part.capitalize(), "Number of %s" % kids], rows)
    if k == "why":
        return item(tab + "%s's %s had %d %s. Their %s colors are not all the same. Why?" % (p[0], an, n, kids, part),
                    "Offspring of the same parents can have variations in their traits.", ["Some of them are not really related.", "They chose their own colors.", "The food changed their colors."],
                    "Brothers and sisters look alike but are not exactly the same. This is variation.")
    return item(tab + "How many %s did %s's %s have in all?" % (kids, p[0], an), "%d" % n, ["%d" % counts[0], "%d" % counts[1], "%d" % (n + 1)],
                "%d + %d = %d." % (counts[0], counts[1], n))


B1 = bank([
    ("What is a trait?", "a feature of a living thing, like eye color or leaf shape", ["a kind of food", "a place where animals live", "a type of weather"],
     "Traits can be inherited or learned."),
    ("What is an inherited trait?", "a trait passed from parents to their offspring", ["a skill you learn at school", "a trait caused by an injury", "a trait that changes every day"],
     "Eye color and fur color are inherited."),
    ("Why do puppies look like their parents?", "They inherit traits from their parents.", ["They copy their parents on purpose.", "They eat the same food.", "They live in the same house."],
     "Offspring get traits from their parents."),
    ("Why do brothers and sisters look alike but not exactly the same?", "They get different mixes of traits from their parents.", ["They have different parents.", "Only one of them inherited traits.", "Traits come from friends."],
     "This is called variation."),
    ("Do plants inherit traits?", "Yes. Seeds grow into plants with traits like their parent plants.", ["No, only animals do.", "Only trees do.", "Only flowers do."],
     "A sunflower seed grows into a sunflower."),
    ("A dog learns to fetch a ball. Will its puppies know how to fetch without learning?", "No. Learned skills are not inherited.", ["Yes, always.", "Only if it is a big dog.", "Only the first puppy."],
     "Behaviors that are learned are not passed down."),
    ("What does variation mean?", "differences in traits among living things of the same kind", ["all living things are exactly the same", "a kind of food", "a place to live"],
     "No two dogs, even from the same litter, are exactly alike."),
    ("A mother cat has a scar on her ear. Will her kittens be born with scars?", "No. A scar is caused by an injury, not inherited.", ["Yes, all of them.", "Only the girls.", "Only the biggest kitten."],
     "Injuries are not passed down."),
])
B5 = bank([
    ("Ava plants seeds from a red tulip. What color flowers will most likely grow?", "red, like the parent plant", ["blue", "green", "no flowers ever"], "Plants inherit traits from their parents."),
    ("Leo compares the leaves of 10 oak trees. They have the same shape but different sizes. What does this show?", "Oak trees inherit leaf shape, and there is variation in size.", ["The trees are not oaks.", "Leaf shape is learned.", "Every tree is exactly the same."],
     "Similar shape is inherited; small differences are variation."),
    ("Mia's family all have curly hair, but her cousin straightens his hair. What will his children inherit?", "the trait for curly or straight hair from their parents, not his straightened style", ["straight hair because he straightens it", "no hair", "a haircut"],
     "A hairstyle is not inherited."),
    ("Noah sees a litter of 5 kittens: 2 gray, 2 black and 1 white. The mother is gray and the father is black. Where might the white come from?", "Traits can come from grandparents or the parents' family.", ["The kitten chose white.", "White kittens come from snow.", "It is not their kitten."],
     "Traits can be passed down from earlier generations."),
    ("Why do farmers choose seeds from their best plants?", "The new plants will likely inherit the good traits.", ["Best plants make no seeds.", "Seeds forget their parents.", "It makes the soil better."],
     "Offspring inherit traits from parents."),
])


def body():
    think = ("<p>A <b>trait</b> is a feature of a living thing. Many traits are <b>inherited</b>: they are passed from parents to their offspring. "
             "Eye color, fur color, ear shape, leaf shape and flower color are inherited.</p>"
             "<p>Offspring look like their parents but are not exactly the same. Even brothers and sisters are a little different. This is called <b>variation</b>.</p>"
             "<p>Some traits are <b>not inherited</b>: skills we learn (riding a bike) and changes from the environment (a scar or a sunburn).</p>")
    ex = [("A black dog and a brown dog have puppies. What color will the puppies most likely be?", ["Puppies inherit traits from their parents."], "black, brown or a mix"),
          ("Is speaking English inherited?", ["It must be learned."], "No, it is learned.")]
    mist = ["Thinking learned skills are inherited.",
            "Thinking offspring are exact copies of their parents.",
            "Thinking a scar or injury is passed to the young."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Traits from parents", B1 + [(g_which, 6), (g_classify, 6)]),
        ("Inherited or not?", [(g_classify, 12), (g_which, 8)]),
        ("Parents and offspring", [(g_offspring, 14), (g_classify, 6)]),
        ("Variation", [(g_var, 12), (g_offspring, 4), (g_which, 4)]),
        ("Using evidence", B5 + [g_var, g_offspring, g_which, g_classify]),
    ])
    make("grade-3", "inherited-traits", 7, "3-LS3-1",
         "Analyze and interpret data to provide evidence that plants and animals have traits inherited from parents and that variation of these traits exists in a group of similar organisms.",
         "Inherited Traits",
         "Grade 3 Inherited Traits Worksheets: Traits from Parents and Variation",
         "Inherited Traits",
         "Free Grade 3 science worksheets on inherited traits (NGSS 3-LS3-1): traits passed from parents to offspring, variation among siblings, and inherited vs. learned traits in plants and animals. 100 practice questions with answers.",
         "Offspring inherit traits from their parents.",
         "Young plants and animals look like their parents, but not exactly. Learned skills and injuries are not inherited.",
         body(),
         [("What is an inherited trait?", "It is a trait passed from parents to their offspring, like eye color, fur color or the shape of a leaf."),
          ("Why don't brothers and sisters look exactly the same?", "Each one gets a different mix of traits from the parents. These differences are called variation."),
          ("Are learned skills inherited?", "No. Skills like riding a bike or reading must be learned. They are not passed down.")],
         sets)


if __name__ == "__main__":
    main()
