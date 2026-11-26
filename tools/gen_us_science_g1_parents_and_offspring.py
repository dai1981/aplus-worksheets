# -*- coding: utf-8 -*-
"""
US Grade 1 Science: Parents and Offspring (1-LS1-2)
  python tools/gen_us_science_g1_parents_and_offspring.py
Read texts and use media to determine patterns in behavior of parents and offspring that help offspring survive.
Parents feed, carry, protect, keep warm and teach their young; young animals cry, chirp and follow to get help.
Very short sentences, many pictures.
Wrong answers come from real mistakes: "babies cry for no reason", "all animal parents stay with their babies",
"a baby bird can find its own food right away".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, svg_wrap, People
from ws_common import text
import sci_kids as K

U = Unit(10106)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


NEEDS = {"food": "to get food", "warm": "to stay warm", "safe": "to stay safe", "learn": "to learn how to live on its own"}
ACTS = [("A mother bird brings worms to the nest.", "food", "bird"), ("A father penguin holds the egg on his feet.", "warm", None),
        ("A mother cat carries a kitten by its neck.", "safe", "cat"), ("Ducklings walk in a line behind their mother.", "safe", "duck"), ("A mother bear shows her cubs how to catch fish.", "learn", "bear"),
        ("A hen sits on her eggs.", "warm", "egg"), ("Elephants stand in a circle around a baby.", "safe", None),
        ("A mother dog licks her puppies clean and lets them drink milk.", "food", "dog"), ("A wolf mom brings meat to the den.", "food", None),
        ("Adult wolves teach pups to hunt.", "learn", None), ("A mother bird sits on her chicks at night.", "warm", "nest"),
        ("A mother deer hides her fawn in tall grass.", "safe", None), ("A mother cow lets her calf drink milk.", "food", None),
        ("A mother otter teaches her pup to swim.", "learn", None), ("A gorilla mom carries her baby on her back.", "safe", None)]


def g_why():
    s, need, pic = R.choice(ACTS)
    who = P.next()[0]
    if not once(s):
        return None
    fg = fig(K.card(pic)) if pic else ""
    return item(fg + "%s reads: “%s” How does this help the baby?" % (who, s), "It helps the baby %s." % NEEDS[need][3:], ["It helps the baby %s." % NEEDS[x][3:] for x in NEEDS if x != need and {x, need} != {"warm", "safe"}] + ["It does not help the baby."] * ({"warm", "safe"} & {need} and 1 or 0),
                "Parents help babies %s." % NEEDS[need][3:])


BABY = [("A baby bird opens its mouth wide and chirps.", "It is hungry and wants food."), ("A puppy whines when it is cold.", "It wants to be warm."),
        ("A kitten meows loudly when it is lost.", "It wants its mother to find it."), ("A baby cries in the night.", "It needs help from a parent."),
        ("A baby deer stays very still in the grass.", "It is hiding to stay safe."), ("A lamb bleats and runs to its mother.", "It wants milk or comfort."),
        ("A baby seal calls out on the ice.", "It wants its mother to find it."), ("Chicks peep and hide under the hen.", "They want to be warm and safe.")]


def g_baby():
    s, a = R.choice(BABY)
    who = P.next()[0]
    if not once(s):
        return None
    w = R.sample([x[1] for x in BABY if x[1] != a and x[1][:6] != a[:6]], 2) + ["It is playing a game."]
    return item("%s watches a video. %s Why?" % (who, s), a, w, "Babies use sounds and actions to get help.")


NAMES = [("cat", "kitten"), ("dog", "puppy"), ("bear", "cub"), ("duck", "duckling"), ("cow", "calf"), ("horse", "foal"), ("sheep", "lamb"),
         ("kangaroo", "joey"), ("deer", "fawn"), ("pig", "piglet"), ("frog", "tadpole"), ("goat", "kid"), ("hen", "chick"), ("swan", "cygnet")]


def g_name():
    a, b = R.choice(NAMES)
    who = P.next()[0]
    t = R.random() < 0.6
    if not once((a, t)):
        return None
    pic = fig(K.card(a)) if a in ("cat", "dog", "bear", "duck", "frog") else ""
    if t:
        return item(pic + "%s learns about a %s. What is its baby called?" % (who, a), "a " + b, ["a " + x[1] for x in R.sample([n for n in NAMES if n[1] != b], 3)], "A baby %s is a %s." % (a, b))
    return item("%s sees a %s. Who is its parent?" % (who, b), "a " + a, ["a " + x[0] for x in R.sample([n for n in NAMES if n[0] != a], 3)], "A %s grows up to be a %s." % (b, a))


SAME = [("Sea turtle mothers lay eggs in the sand and leave.", "The babies must find the ocean on their own."),
        ("Frogs lay many eggs in a pond and swim away.", "Many tadpoles hatch, and some survive."),
        ("Many fish lay lots of eggs and do not care for them.", "So many eggs means some babies survive."),
        ("Spiders often leave their egg sacs.", "Baby spiders take care of themselves.")]


def g_alone():
    s, a = R.choice(SAME)
    who = P.next()[0]
    if not once(s):
        return None
    return item("%s reads: “%s” What does this tell us?" % (who, s), a, ["All animal parents stay with their babies.", "The babies get fed by the parents.", "The babies never hatch."],
                "Some animals do not care for their young.")


def g_pick():
    acts = [("bird", "feeds worms to its chicks"), ("cat", "carries its kittens to safety"), ("duck", "leads its ducklings to water"),
            ("bear", "teaches its cubs to fish"), ("dog", "feeds its puppies milk")]
    kinds = R.sample(acts, 4)
    a = R.choice(kinds)
    if not once((tuple(k[0] for k in kinds), a[0])):
        return None
    L = "ABCD"
    who = P.next()[0]
    pic = K.row([k[0] for k in kinds], words=["%s. %s" % (L[i], k[0]) for i, k in enumerate(kinds)], size=90)
    return item(fig(pic) + "%s reads a book. Which parent %s?" % (who, a[1]), "%s (%s)" % (L[kinds.index(a)], a[0]),
                ["%s (%s)" % (L[i], k[0]) for i, k in enumerate(kinds) if k != a], "The %s %s." % (a[0], a[1]))


B1 = bank([
    ("Why do parents feed their babies?", "Babies cannot get food on their own yet.", ["Babies are never hungry.", "Food makes babies sleep forever.", "Parents are not hungry."], "Babies need help."),
    ("Why does a baby bird chirp loudly?", "to tell its parents it is hungry", ["to scare the parents", "to sing a song for fun", "to tell it is full"], "Chirping gets food."),
    ("How does a mother kangaroo keep her joey safe?", "in her pouch", ["in a nest", "under a rock", "in the water"], "The pouch is like a pocket."),
    ("Why do ducklings follow their mother?", "to stay safe and find food", ["to race her", "to get lost", "to sleep"], "Mom leads them."),
    ("Why does a hen sit on her eggs?", "to keep them warm", ["to break them", "to hide from them", "to cool them"], "Eggs need warmth."),
    ("What do human babies do when they need help?", "cry", ["fly", "dig", "bark"], "Crying tells parents."),
    ("Why do bear cubs stay with their mother?", "to learn how to find food and stay safe", ["to teach her", "to sleep alone", "to find a new mom"], "Cubs learn from mom."),
    ("What is an offspring?", "a baby or young animal", ["a kind of food", "a type of nest", "a grown-up animal only"], "Offspring are young."),
])
B5 = bank([
    ("Ava reads that a penguin dad holds the egg on his feet for weeks. Why?", "to keep the egg warm on the ice", ["to play catch", "to make it cold", "to hide it from mom"], "Ice is cold."),
    ("Leo sees a mother cat move her kittens to a new spot. Why might she do that?", "to keep them safe", ["to lose them", "to make them cold", "to make them hungry"], "Moving away from danger."),
    ("Mia's baby brother cries. What might he need?", "food, a clean diaper, or comfort", ["a toy car only", "nothing", "a bike"], "Crying asks for help."),
    ("Kai watches a video of wolves. Older wolves bring food to pups. What pattern is this?", "Parents feed their young.", ["Babies feed parents.", "Wolves never share.", "Pups hunt alone."], "Feeding helps survival."),
    ("Sam sees a robin chase a cat away from its nest. Why?", "to protect its chicks", ["to play tag", "to make friends with the cat", "to find a new nest"], "Parents protect."),
    ("Omar reads that elephant calves stay close to the herd. How does this help?", "The big elephants protect them.", ["They get lost.", "They run away.", "They get colder."], "The herd keeps calves safe."),
    ("Zoe learns sea turtles leave their eggs. How are they different from birds?", "Birds care for their chicks; sea turtles do not.", ["They are the same.", "Turtles feed babies worms.", "Birds leave eggs in sand."], "Not all parents stay."),
])


def body():
    pic = K.row(["bird", "nest", "cat", "duck"], words=["feeds", "keeps warm", "carries", "leads"], size=95)
    ex = [("A mother bird brings worms. How does it help?", ["Babies need food."], "The chick gets food."),
          ("A baby cries. Why?", ["It needs help."], "It tells the parent it needs something.")]
    mist = ["Thinking babies cry for no reason.",
            "Thinking all animal parents stay with their babies.",
            "Thinking baby birds can find food right away."]
    return kid_lesson(pic, "Parents help their babies live.",
                      ["Parents feed, carry, protect and teach.", "Babies cry and chirp to ask for help.", "Some animals, like sea turtles, leave their eggs."], ex, mist)


def main():
    sets = U.sets([
        ("Parents help babies", B1 + [(g_why, 6), (g_pick, 6)]),
        ("How parents help", [(g_why, 10), (g_pick, 6), (g_name, 4)]),
        ("Babies ask for help", [(g_baby, 8), (g_name, 8), (g_pick, 4)]),
        ("Baby animal names", [(g_name, 12), (g_alone, 4), (g_pick, 4)]),
        ("Animal families", B5 + [(g_pick, 9), (g_name, 4)]),
    ])
    make("grade-1", "parents-and-offspring", 6, "1-LS1-2",
         "Read texts and use media to determine patterns in behavior of parents and offspring that help offspring survive.",
         "Parents and Offspring",
         "Grade 1 Parents and Offspring Worksheets: How Animal Parents Help Their Babies",
         "Parents and Babies",
         "Free grade 1 science worksheets on parents and offspring (NGSS 1-LS1-2): how animal parents feed, protect and teach their young, and how babies ask for help. 100 picture questions with answers.",
         "Parents help babies live.",
         "Parents feed and protect. Babies cry or chirp for help.",
         body(),
         [("How do animal parents help their babies?", "They feed them, keep them warm, carry and protect them, and teach them to find food."),
          ("Why do babies cry or chirp?", "To tell parents they are hungry, cold, lost or need help."),
          ("Do all animal parents take care of their babies?", "No. Sea turtles, many fish and frogs lay eggs and leave. They lay many eggs, so some babies survive.")],
         sets)


if __name__ == "__main__":
    main()
