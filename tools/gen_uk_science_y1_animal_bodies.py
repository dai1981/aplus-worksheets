# -*- coding: utf-8 -*-
"""
UK Year 1 science: Animal Bodies (Animals, including humans)
  python tools/gen_uk_science_y1_animal_bodies.py
Describe and compare the structure of a variety of common animals (fish, amphibians, reptiles, birds and mammals,
including pets): body parts such as wings, fins, gills, beaks, tails, shells and whiskers, what each part is for,
counting legs, and comparing two animals.
Wrong answers come from real mistakes: "all animals have four legs", "fish breathe with lungs", "only birds have
tails", "a snake has tiny legs".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, People, once
from uk_ks1 import card, name
import sci_kids as K

U = Unit(61106)
R = U.R
P = People(R)

HAS = [("wings and feathers", ["a robin", "a duck", "an owl", "a penguin", "a swan", "a blackbird"], ["a cat", "a goldfish", "a snake", "a dog"]),
       ("fins and gills", ["a goldfish", "a shark", "a trout", "a salmon", "a cod"], ["a rabbit", "a robin", "a horse", "a mouse"]),
       ("a beak", ["a robin", "a duck", "a parrot", "an eagle", "a pelican", "a toucan"], ["a cat", "a frog", "a cow", "a lizard"]),
       ("a hard shell", ["a tortoise", "a snail", "a crab", "a turtle"], ["a rabbit", "a robin", "a dog", "a goldfish"]),
       ("whiskers", ["a cat", "a mouse", "a rabbit", "a seal", "a tiger", "a hamster"], ["a robin", "a snake", "a goldfish", "a frog"]),
       ("hooves", ["a horse", "a cow", "a sheep", "a goat", "a deer", "a pig"], ["a cat", "a robin", "a frog", "a snake"]),
       ("no legs", ["a snake", "a goldfish", "a worm", "a slug"], ["a dog", "a robin", "a frog", "a lizard"]),
       ("a long, bushy tail", ["a squirrel", "a fox"], ["a frog", "a robin", "a goldfish", "a snail"])]


def g_has():
    f, yes, no = R.choice(HAS)
    a = R.choice(yes)
    if not once(("ha", f, a)):
        return None
    w = R.sample(no, 3)
    o = sorted([a] + w)
    return item("Which of these animals has %s: %s or %s?" % (f, ", ".join(o[:3]), o[3]), a, w, "Look at each animal's body parts.")


JOB = [("fins", "to swim and steer in water"), ("wings", "to fly"), ("gills", "to breathe under water"), ("a beak", "to pick up and eat food"),
       ("whiskers", "to feel things in the dark"), ("a shell", "to protect a soft body"), ("webbed feet", "to swim, like a paddle"),
       ("sharp claws", "to grip, climb and catch food"), ("a long tail", "to balance"), ("big ears", "to hear well"),
       ("a long neck", "to reach leaves high in trees"), ("long back legs", "to jump a long way"), ("a trunk", "to pick up food and suck up water"),
       ("thick fur", "to keep warm in the cold")]


def g_job():
    p, j = R.choice(JOB)
    k = R.random() < 0.5
    if not once(("jo", p, k)):
        return None
    if k:
        return item("What does an animal use %s for?" % p, j, R.sample([x[1] for x in JOB if x[1] != j], 3), "Each body part helps the animal live.")
    return item("Which body part helps an animal %s?" % j[3:], p, R.sample([x[0] for x in JOB if x[0] != p], 3), "Each body part helps the animal live.")


LEGS = [("a bird", 2), ("a dog", 4), ("a spider", 8), ("an ant", 6), ("a snake", 0), ("a human", 2), ("a cat", 4), ("a beetle", 6), ("a frog", 4), ("a ladybird", 6),
        ("a duck", 2), ("a horse", 4), ("a goldfish", 0), ("a lizard", 4)]


def g_legs():
    a, n = R.choice(LEGS)
    if not once(("le", a)):
        return None
    return item("How many legs does %s have?" % a, str(n), [str(x) for x in (0, 2, 4, 6, 8) if x != n][:3] if n != 8 else ["2", "4", "6"],
                "Birds and humans have 2 legs, many mammals 4, insects 6, spiders 8, snakes and fish none.")


PAIRS = [("a cat", "a dog", "fur, four legs and a tail"), ("a robin", "a duck", "feathers, wings and a beak"), ("a goldfish", "a shark", "fins, gills and scales"),
         ("a frog", "a toad", "damp skin and back legs for jumping"), ("a snake", "a lizard", "dry, scaly skin"), ("a cow", "a horse", "hooves and fur"),
         ("a human", "a monkey", "hands that can grip"), ("an ant", "a beetle", "six legs")]


def g_both():
    a, b, f = R.choice(PAIRS)
    if not once(("bo", a)):
        return None
    return item("What do %s and %s both have?" % (a, b), f, R.sample([x[2] for x in PAIRS if x[2] != f], 3), "Compare the two animals' bodies.")


PIC = [("fish", "fins"), ("bird", "wings"), ("duck", "a beak"), ("cat", "whiskers"), ("rabbit", "long ears"), ("frog", "long back legs"), ("squirrel", "a bushy tail")]


def g_pic():
    k, p = R.choice(PIC)
    if not once(("pi", k)):
        return None
    w = [x[1] for x in PIC if x[1] != p and not ({x[1], p} <= {"wings", "a beak"})]
    return item(card(k) + "This is a %s. Which body part does it have?" % name(k), p, R.sample(w, 3), "Look closely at the picture.")


B1 = bank([
    ("Which body part do fish use to breathe?", "gills", ["lungs", "a beak", "feathers"], "Gills take air from water."),
    ("Which animals have feathers?", "birds", ["fish", "mammals", "reptiles"], "Only birds have feathers."),
    ("How many legs does an insect have?", "six", ["four", "eight", "two"], "Ants, bees, ladybirds."),
    ("How many legs does a spider have?", "eight", ["six", "four", "ten"], "Spiders are not insects."),
    ("Which body part do we use to see?", "eyes", ["ears", "nose", "tongue"], "Most animals have eyes."),
    ("What do many mammals have on their bodies?", "fur or hair", ["feathers", "fins", "shells"], "Cats, dogs, humans."),
    ("Which animal has no legs?", "a snake", ["a lizard", "a frog", "a dog"], "Snakes slide along."),
    ("What is a beak?", "the hard mouth of a bird", ["a kind of wing", "a fish's fin", "a cat's whisker"], "Birds eat with beaks."),
])
B3 = bank([
    ("Which animal has a long neck to reach high leaves?", "a giraffe", ["a pig", "a frog", "a goldfish"], "Body parts suit the animal."),
    ("What does a bird use its wings for?", "to fly", ["to swim under water like gills", "to dig", "to breathe"], "Most birds fly."),
    ("Which animal uses its trunk like a hand?", "an elephant", ["a horse", "a cat", "a duck"], "A trunk is a long nose."),
    ("Which of these has a tail?", "a dog", ["a human", "a snail", "an earthworm"], "Many mammals have tails."),
    ("Which body part does a cat use to smell?", "its nose", ["its tail", "its whiskers", "its paws"], "Noses smell."),
    ("What is the hard outside of a crab called?", "a shell", ["fur", "feathers", "a fin"], "It protects the crab."),
    ("What helps a frog jump far?", "long, strong back legs", ["a beak", "feathers", "a shell"], "Spring-like legs."),
    ("Which animals have scales?", "fish and reptiles", ["birds and mammals", "only cats", "only insects"], "Fish and snakes."),
])
B5 = bank([
    ("Why do ducks have webbed feet?", "They help them swim, like paddles.", ["To keep warm.", "To fly faster.", "To dig holes."], "Body parts suit how animals live."),
    ("Why does an owl have big eyes?", "to see in the dark when it hunts at night", ["to look pretty", "to hear better", "to swim"], "Night hunter."),
    ("How is a goldfish different from a cat?", "It has fins and gills instead of legs and lungs.", ["It has fur and whiskers.", "It has feathers.", "It is exactly the same."], "Compare structures."),
    ("Why does a tortoise have a shell?", "to protect its soft body", ["to swim faster", "to fly", "to stay cold"], "Protection."),
    ("How could you compare two pets' bodies?", "Look closely and list the body parts each one has.", ["Guess.", "Weigh only one.", "Look at their names."], "Observe and compare."),
])


def body():
    pic = K.row(["fish", "bird", "cat"], words=["fins", "wings", "whiskers"], size=90, label="a fish has fins, a bird has wings and a cat has whiskers")
    ex = [("A fish breathes with?", ["Under water"], "gills"),
          ("How many legs does a spider have?", ["More than an insect"], "eight")]
    mist = ["Thinking all animals have four legs.", "Thinking fish breathe with lungs.", "Thinking a snake has tiny legs."]
    return kid_lesson(pic, "Animals have different body parts.",
                      ["Fish have fins and gills. Birds have wings, feathers and a beak.", "Each body part helps the animal to live.", "We can compare animals by their body parts."], ex, mist)


def main():
    sets = U.sets([
        ("Body parts", B1 + [(g_pic, 7), (g_legs, 5)]),
        ("Which animal has it?", [(g_has, 14), (g_legs, 6)]),
        ("What is it for?", [(g_job, 16), (g_legs, 3), (g_has, 1)]),
        ("Comparing animals", [(g_both, 8), (g_has, 10), (g_job, 2)]),
        ("Thinking about bodies", B3 + B5 + [(g_has, 5), (g_job, 2)]),
    ])
    make_uk(1, "animal-bodies", 6, "Animals, including humans",
            "Describe and compare the structure of a variety of common animals (fish, amphibians, reptiles, birds and mammals, including pets).",
            "Animal Bodies",
            "Year 1 Science: Animal Bodies Worksheets (Wings, Fins, Legs and Tails)",
            "Animal Bodies",
            "Free Year 1 science worksheets on animal bodies: wings, fins, gills, beaks, shells and whiskers, what each part is for, counting legs and comparing animals. 100 questions with answers.",
            "Animals have different body parts.",
            "Each part helps the animal: fins to swim, wings to fly, gills to breathe.",
            body(),
            [("What body parts do animals have?", "Many have legs, eyes and a mouth. Fish have fins and gills, birds have wings and beaks, and many mammals have fur, whiskers and tails."),
             ("Why do animals have different body parts?", "Each part helps the animal live where it lives: fins to swim, wings to fly, webbed feet to paddle."),
             ("How many legs do animals have?", "Birds and humans have 2, many mammals 4, insects 6, spiders 8, and snakes and fish have none.")],
            sets)


if __name__ == "__main__":
    main()
