# -*- coding: utf-8 -*-
"""
UK Year 1 science: Carnivores, Herbivores and Omnivores (Animals, including humans)
  python tools/gen_uk_science_y1_carnivores_herbivores_and_omnivores.py
Identify and name a variety of common animals that are carnivores, herbivores and omnivores: what animals eat,
sorting animals by diet, teeth as clues, and a table of animals and their food.
Wrong answers come from real mistakes: "all big animals eat meat", "rabbits eat meat", "humans only eat plants",
"a herbivore eats herbs only".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K

U = Unit(61105)
R = U.R
P = People(R)

DIET = [("a rabbit", "grass and carrots", "herbivore"), ("a cow", "grass", "herbivore"), ("a sheep", "grass", "herbivore"), ("a horse", "grass and hay", "herbivore"),
        ("a giraffe", "leaves from tall trees", "herbivore"), ("an elephant", "grass, leaves and fruit", "herbivore"), ("a caterpillar", "leaves", "herbivore"), ("a deer", "grass and leaves", "herbivore"),
        ("a lion", "meat from other animals", "carnivore"), ("a tiger", "meat from other animals", "carnivore"), ("an owl", "mice and voles", "carnivore"), ("a shark", "fish and seals", "carnivore"),
        ("a spider", "flies and other insects", "carnivore"), ("a crocodile", "fish and other animals", "carnivore"), ("an eagle", "fish, rabbits and mice", "carnivore"), ("a cat", "meat and fish", "carnivore"),
        ("a human", "fruit, vegetables, bread, meat and fish", "omnivore"), ("a pig", "plants and small animals", "omnivore"), ("a bear", "fish, berries and honey", "omnivore"),
        ("a badger", "worms, berries and roots", "omnivore"), ("a hedgehog", "beetles, worms and berries", "omnivore"), ("a fox", "rabbits, mice and berries", "omnivore"),
        ("a chicken", "seeds, grain and insects", "omnivore"), ("a robin", "worms, insects and seeds", "omnivore")]
KIND = {"herbivore": "a herbivore (eats only plants)", "carnivore": "a carnivore (eats only animals)", "omnivore": "an omnivore (eats plants and animals)"}


def g_kind():
    a, f, k = R.choice(DIET)
    if not once(("ki", a)):
        return None
    return item("%s eats %s. What kind of animal is it?" % (a[0].upper() + a[1:], f), KIND[k], [KIND[x] for x in sorted(KIND) if x != k] + ["a plant"],
                "Herbivores eat plants, carnivores eat animals, omnivores eat both.")


def g_pick():
    k = R.choice(sorted(KIND))
    yes = [x[0] for x in DIET if x[2] == k]
    no = [x[0] for x in DIET if x[2] != k]
    a = R.choice(yes)
    if not once(("pk", a)):
        return None
    w = R.sample(no, 3)
    o = sorted([a] + w)
    return item("Which of these is %s: %s or %s?" % (KIND[k].split(" (")[0], ", ".join(o[:3]), o[3]), a, w, "Think about what each animal eats.")


def g_food():
    a, f, k = R.choice(DIET)
    if not once(("fo", a)):
        return None
    w = [x[1] for x in DIET if x[2] != k]
    return item("What does %s eat?" % a, f, R.sample(sorted(set(w)), 3), "Animals eat different foods.")


def g_table():
    who = P.next()[0]
    rows = R.sample(DIET, 5)
    k = R.choice(sorted(KIND))
    n = sum(1 for r in rows if r[2] == k)
    if n == 0 or not once(("tb", tuple(r[0] for r in rows), k)):
        return None
    tab = table(["Animal", "What it eats"], [[r[0], r[1]] for r in rows])
    g = str(n)
    plural = {"herbivore": "herbivores", "carnivore": "carnivores", "omnivore": "omnivores"}[k]
    return item(tab + "%s made a table of animals and their food. How many of these animals are %s?" % (who, plural), g, [str(x) for x in range(6) if x != n][:3],
                "%s eat %s." % (plural.capitalize(), {"herbivore": "only plants", "carnivore": "only other animals", "omnivore": "plants and animals"}[k]))


B1 = bank([
    ("What is a herbivore?", "an animal that eats only plants", ["an animal that eats only meat", "an animal that eats herbs only", "a plant that eats insects"], "Cows and rabbits."),
    ("What is a carnivore?", "an animal that eats only other animals", ["an animal that eats only plants", "a plant", "an animal that eats nothing"], "Lions and owls."),
    ("What is an omnivore?", "an animal that eats plants and animals", ["an animal that eats only grass", "an animal that eats only meat", "an animal that never eats"], "Humans and pigs."),
    ("What kind of animal is a human?", "an omnivore", ["a carnivore", "a herbivore", "a plant"], "We can eat plants and meat."),
    ("What does a rabbit eat?", "plants such as grass and carrots", ["meat", "fish", "insects"], "Rabbits are herbivores."),
    ("What does a lion eat?", "meat from other animals", ["grass", "leaves", "fruit"], "Lions are carnivores."),
    ("What kind of teeth do many carnivores have?", "sharp, pointed teeth for tearing meat", ["flat teeth for chewing grass", "no teeth", "soft teeth"], "Teeth are clues."),
    ("What kind of teeth do many herbivores have?", "flat teeth for chewing plants", ["long, sharp fangs", "no teeth at all", "teeth like a shark"], "Grinding grass."),
])
B5 = bank([
    ("Is an elephant a carnivore because it is big?", "No. Elephants eat only plants, so they are herbivores.", ["Yes, big animals eat meat.", "Yes, it eats lions.", "It is an omnivore."], "Size does not matter."),
    ("A pet cat is a carnivore. What should it be fed?", "cat food made from meat or fish", ["only lettuce", "only seeds", "sweets"], "Right food for the animal."),
    ("A hedgehog eats beetles and berries. Why is it an omnivore?", "It eats both animals and plants.", ["It eats only plants.", "It eats only meat.", "It eats nothing."], "Both."),
    ("How could you find out what a garden bird eats?", "Put out different foods and watch which it eats.", ["Guess.", "Look at its colour.", "Ask a friend to guess."], "Observe."),
    ("Some people choose not to eat meat. Does that make humans herbivores?", "No. Humans can eat both, so they are omnivores, even if some choose not to eat meat.", ["Yes, all humans are herbivores.", "Yes, humans are carnivores.", "Humans do not eat."], "What a body can eat."),
])


def body():
    pic = K.row(["rabbit", "cat", "bear"], words=["herbivore", "carnivore", "omnivore"], size=90, label="a rabbit is a herbivore, a cat is a carnivore and a bear is an omnivore")
    ex = [("A cow eats grass. It is a?", ["Only plants"], "herbivore"),
          ("A fox eats mice and berries. It is an?", ["Both"], "omnivore")]
    mist = ["Thinking all big animals eat meat.", "Thinking rabbits eat meat.", "Thinking humans only eat plants."]
    return kid_lesson(pic, "Animals eat different things.",
                      ["Herbivores eat only plants.", "Carnivores eat only other animals.", "Omnivores eat plants and animals."], ex, mist)


def main():
    sets = U.sets([
        ("What animals eat", B1 + [(g_food, 12)]),
        ("Herbivore, carnivore or omnivore?", [(g_kind, 14), (g_food, 6)]),
        ("Which one?", [(g_pick, 16), (g_kind, 4)]),
        ("Animal food table", [(g_table, 20)]),
        ("Thinking about food", B5 + [(g_table, 9), (g_pick, 6)]),
    ])
    make_uk(1, "carnivores-herbivores-and-omnivores", 5, "Animals, including humans",
            "Identify and name a variety of common animals that are carnivores, herbivores and omnivores.",
            "Carnivores, Herbivores, Omnivores",
            "Year 1 Science: Carnivores, Herbivores and Omnivores Worksheets",
            "What Animals Eat",
            "Free Year 1 science worksheets on carnivores, herbivores and omnivores: what animals eat, sorting animals by diet and teeth as clues. 100 questions with answers.",
            "Herbivores eat plants.",
            "Carnivores eat other animals. Omnivores eat both.",
            body(),
            [("What is the difference between a herbivore, a carnivore and an omnivore?", "Herbivores eat only plants, carnivores eat only other animals, and omnivores eat both plants and animals."),
             ("What are humans?", "Humans are omnivores, because our bodies can eat both plants and animals."),
             ("How can teeth help us tell?", "Sharp, pointed teeth are good for meat. Flat teeth are good for chewing plants.")],
            sets)


if __name__ == "__main__":
    main()
