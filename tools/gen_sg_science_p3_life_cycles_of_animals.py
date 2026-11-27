# -*- coding: utf-8 -*-
"""
Singapore Primary 3 science: Life cycles of animals (Cycles)
  python tools/gen_sg_science_p3_life_cycles_of_animals.py
Animals have different life cycles: four stages (egg, larva, pupa, adult) for the butterfly, mosquito and beetle,
three stages (egg, nymph, adult) for the cockroach and grasshopper, egg - tadpole - froglet - adult for the frog,
egg - chick - adult for the chicken. Some young look like their parents (nymph, chick), some do not (larva, tadpole).
Stopping mosquitoes from breeding (stagnant water) is Singapore's dengue prevention.
Wrong answers come from real mistakes: "a cockroach has a pupa stage", "a caterpillar is a different animal",
"a tadpole is a fish", "the pupa eats a lot".
"""
from sg_sci import Unit, item, bank, lesson, make_sg, table, People, once, use

U = Unit(63304)
R = U.R
P = People(R)
LC = use(U, "gen_uk_science_y5_life_cycles", drop=["gestation", "incubation", "human", "swan", "horse", "froglet"])

CYC = {"butterfly": ["egg", "caterpillar (larva)", "pupa", "adult butterfly"],
       "mosquito": ["egg", "larva", "pupa", "adult mosquito"],
       "mealworm beetle": ["egg", "larva (mealworm)", "pupa", "adult beetle"],
       "cockroach": ["egg", "nymph", "adult cockroach"],
       "grasshopper": ["egg", "nymph", "adult grasshopper"],
       "frog": ["egg", "tadpole", "young frog", "adult frog"],
       "chicken": ["egg", "chick", "adult chicken"]}
ALL = sorted({s for v in CYC.values() for s in v})
LIKE = {"cockroach": True, "grasshopper": True, "chicken": True, "butterfly": False, "mosquito": False, "mealworm beetle": False, "frog": False}


def a_(x):
    return ("an " if x[0] in "aeio" else "a ") + x


def g_next():
    an = R.choice(sorted(CYC))
    st = CYC[an]
    i = R.randrange(len(st) - 1)
    k = R.choice(["after", "before"])
    if k == "after":
        a, s0 = st[i + 1], st[i]
        q = "In the life cycle of %s, which stage comes after the %s?" % (a_(an), s0)
    else:
        a, s0 = st[i], st[i + 1]
        q = "In the life cycle of %s, which stage comes just before the %s?" % (a_(an), s0)
    if not once(("nx", an, k, i)):
        return None
    w = [x for x in st if x not in (a, s0)]
    pool = [x for x in ALL if x not in st and x.split(" (")[0] not in " ".join(st)]
    R.shuffle(pool)
    w = (w + pool)[:3]
    return item(q, a, w, "The life cycle of %s is: %s." % (a_(an), " → ".join(st)))


def g_count():
    an = R.choice(sorted(CYC))
    if not once(("ct", an)):
        return None
    n = len(CYC[an])
    return item("How many stages are there in the life cycle of %s?" % a_(an), str(n), [str(x) for x in (2, 3, 4, 5) if x != n],
                "%s: %s." % (an[0].upper() + an[1:], " → ".join(CYC[an])))


def g_has():
    k = R.choice(["pupa", "nymph", "larva", "tadpole"])
    yes = {"pupa": ["butterfly", "mosquito", "mealworm beetle"], "nymph": ["cockroach", "grasshopper"], "larva": ["butterfly", "mosquito", "mealworm beetle"],
           "tadpole": ["frog"]}[k]
    a = R.choice(yes)
    if not once(("hs", k, a)):
        return None
    no = [x for x in sorted(CYC) if x not in yes]
    return item("Which of these animals has a %s stage in its life cycle?" % k, a, R.sample(no, 3),
                "%s: %s." % (a[0].upper() + a[1:], " → ".join(CYC[a])))


def g_like():
    an = R.choice(sorted(CYC))
    if not once(("lk", an)):
        return None
    young = CYC[an][1].split(" (")[0]
    if LIKE[an]:
        return item("Does the young (%s) of %s look like its parent?" % (young, a_(an)), "Yes, it looks like a smaller adult.",
                    ["No, it looks completely different.", "No, it has no legs.", "Only after it becomes a pupa."],
                    "The %s looks like the adult but is smaller%s." % (young, " and has no wings" if an in ("cockroach", "grasshopper") else ""))
    return item("Does the young (%s) of %s look like its parent?" % (young, a_(an)), "No, it looks very different from the adult.",
                ["Yes, it is a smaller copy of the adult.", "Yes, but it has more legs.", "It has no young stage."],
                "The young changes a lot as it grows: %s." % " → ".join(CYC[an]))


def g_order():
    an = R.choice([x for x in sorted(CYC) if len(CYC[x]) == 4])
    st = CYC[an]
    if not once(("or", an)):
        return None
    w = [[st[0], st[2], st[1], st[3]], [st[1], st[0], st[2], st[3]], [st[3], st[2], st[1], st[0]]]
    return item("Which shows the life cycle of %s in the correct order?" % a_(an), " → ".join(st), [" → ".join(x) for x in w],
                "Start with the egg and end with the adult.")


WHERE = [("Where does a mosquito lay its eggs?", "on the surface of still water", ["on leaves", "in the soil", "inside fruits"], "Mosquito larvae and pupae live in water."),
         ("Where does a frog lay its eggs?", "in water", ["on dry sand", "in a nest in a tree", "inside its body until they hatch"], "Tadpoles live in water."),
         ("Where does a butterfly usually lay its eggs?", "on the leaves of the plant its caterpillars eat", ["in water", "in the soil", "on the ground under stones"], "The caterpillars hatch on their food."),
         ("Where do mosquito larvae live?", "in water", ["on leaves", "in the soil", "on animals"], "They hang below the water surface to breathe."),
         ("Where do tadpoles live?", "in water", ["on land", "in trees", "in the soil"], "Tadpoles breathe through gills."),
         ("Where does a hen keep her eggs warm?", "in a nest, by sitting on them", ["in water", "under the soil", "on a leaf"], "The heat helps the chicks develop.")]


def g_where():
    q, a, w, e = R.choice(WHERE)
    if not once(("wh", q)):
        return None
    return item(q, a, w, e)


def g_table():
    an = R.choice(["butterfly", "mosquito", "mealworm beetle", "frog"])
    st = CYC[an]
    days = {"butterfly": [4, 14, 10, 14], "mosquito": [2, 7, 2, 14], "mealworm beetle": [10, 60, 14, 60], "frog": [7, 60, 30, 700]}[an]
    k = R.choice(["longest", "shortest", "total", "eats"])
    if not once(("tb", an, k)):
        return None
    tb = table(["Stage", "About how many days"], [[s, str(d)] for s, d in zip(st, days)])
    q0 = "The table shows the life cycle of %s.<br>%s" % (a_(an), tb)
    s = sorted(zip(days, st))
    if k == "longest":
        if s[-1][0] == s[-2][0]:
            return None
        return item(q0 + "Which stage lasts the longest?", s[-1][1], [x for _, x in s[:-1]], "Compare the number of days.")
    if k == "shortest":
        if s[0][0] == s[1][0]:
            return None
        return item(q0 + "Which stage lasts the shortest time?", s[0][1], [x for _, x in s[1:]], "Compare the number of days.")
    if k == "total":
        t = sum(days[:3])
        return item(q0 + "About how many days does it take from egg to adult?", str(t), [str(t + 10), str(sum(days)), str(days[1])],
                    "Add the days of the stages before the adult: %s = %d." % (" + ".join(str(d) for d in days[:3]), t))
    if an == "frog":
        return item(q0 + "Which stage lives only in water and breathes through gills?", "tadpole", ["egg", "young frog", "adult frog"],
                    "Tadpoles live in water and breathe through gills.")
    return item(q0 + "At which stage does the animal eat the most and grow fastest?", st[1], [st[0], st[2], st[3]],
                "The larva eats a lot. The pupa does not eat.")


B1 = bank([
    ("What is a life cycle?", "the stages an animal goes through from egg or birth to adult", ["the food an animal eats", "the place an animal lives", "how an animal moves"], "The adult then reproduces and the cycle starts again."),
    ("What is the stage of a butterfly between the caterpillar and the adult?", "pupa", ["nymph", "tadpole", "egg"], "Inside the pupa, the caterpillar changes into a butterfly."),
    ("What is a young cockroach called?", "a nymph", ["a larva", "a pupa", "a tadpole"], "A nymph looks like a small adult without wings."),
    ("What is a young frog that lives in water called?", "a tadpole", ["a nymph", "a larva", "a chick"], "Tadpoles have tails and gills."),
    ("Which animal has a three-stage life cycle?", "cockroach", ["butterfly", "mosquito", "mealworm beetle"], "Egg → nymph → adult."),
    ("Which animal has a four-stage life cycle?", "mosquito", ["cockroach", "grasshopper", "chicken"], "Egg → larva → pupa → adult."),
    ("Does a pupa eat?", "No. It does not eat or move much while it changes.", ["Yes, it eats more than the larva.", "Yes, it eats leaves.", "Only at night."], "The pupa uses food stored by the larva."),
    ("Which stage comes first in the life cycle of most animals?", "egg", ["adult", "pupa", "nymph"], "Many animals start life as an egg."),
])
B2 = bank([
    ("How is a caterpillar different from an adult butterfly?", "It has no wings and eats leaves.", ["It has wings.", "It lays eggs.", "It drinks nectar."], "The caterpillar changes completely inside the pupa."),
    ("How is a nymph different from an adult grasshopper?", "It is smaller and has no fully grown wings.", ["It has no legs.", "It lives in water.", "It looks completely different."], "A nymph looks like a small adult."),
    ("What happens to a tadpole as it grows into a frog?", "It grows legs and loses its tail.", ["It grows wings.", "It grows scales.", "It becomes a fish."], "It also starts to breathe through lungs."),
    ("Why does a nymph shed its skin (moult) several times?", "Its hard outer skin does not grow, so it sheds it to grow bigger.", ["It is too hot.", "It wants to change colour.", "It is turning into a pupa."], "Cockroach and grasshopper nymphs moult as they grow."),
    ("Which stage of a mosquito can fly?", "the adult", ["the egg", "the larva", "the pupa"], "Only adult mosquitoes have wings."),
    ("Which statement about a frog's life cycle is correct?", "Tadpoles live in water; adult frogs can live on land and in water.", ["Tadpoles live on land.", "Adult frogs breathe only through gills.", "Frogs give birth to young frogs."], "Frogs are amphibians."),
    ("A chick hatches from an egg. What does it grow into?", "an adult chicken", ["a duck", "a pupa", "a tadpole"], "Chick → adult chicken."),
    ("Which young animal looks most like its parent?", "a cockroach nymph", ["a butterfly caterpillar", "a mosquito larva", "a frog tadpole"], "Nymphs are small copies of the adult."),
])
B3 = bank([
    ("Why should we remove stagnant water from flower pot plates?", "Mosquitoes lay their eggs in still water.", ["Water makes flowers die.", "It attracts cockroaches.", "It makes the plants grow too fast."], "No still water means no place for mosquito larvae to grow."),
    ("Which disease in Singapore is spread by the Aedes mosquito?", "dengue fever", ["chickenpox", "the common cold", "food poisoning"], "Stopping mosquitoes from breeding helps prevent dengue."),
    ("Which action would best stop mosquitoes from breeding at home?", "turning over pails and changing the water in vases often", ["leaving water in buckets", "keeping the lights on", "watering plants more"], "Mosquito eggs need still water."),
    ("Why is breaking the life cycle at the larva stage useful for controlling mosquitoes?", "The larvae die before they can become adults and lay eggs.", ["Larvae bite people.", "Larvae fly away.", "Larvae eat the adults."], "Fewer adults means fewer eggs."),
    ("Why do some animals lay many eggs?", "Many eggs and young are eaten or die, so laying many helps some survive.", ["They cannot count.", "All of them always survive.", "Eggs are their food."], "Frogs and fish lay hundreds of eggs."),
    ("Which of these animals' young live in a different place from the adults?", "frog", ["chicken", "cockroach", "grasshopper"], "Tadpoles live in water; many adult frogs live on land."),
    ("Mealworms are fed to pet birds. Which stage of the beetle is a mealworm?", "larva", ["egg", "pupa", "adult"], "A mealworm is the larva of the mealworm beetle."),
])
B5 = bank([
    ("Siti kept mealworms in a container with oats. After three weeks, some stopped moving and turned pale and still. What stage were they?", "pupa", ["egg", "nymph", "adult"], "The mealworm (larva) becomes a pupa before the adult beetle."),
    ("Ravi saw tiny wriggling things in a pail of rainwater. What are they most likely?", "mosquito larvae", ["tadpoles", "cockroach nymphs", "caterpillars"], "Mosquito larvae wriggle in still water."),
    ("A pupil observed: egg → young that looks like the adult but has no wings → adult. Which animal could it be?", "a grasshopper", ["a butterfly", "a mosquito", "a frog"], "That is a three-stage life cycle with a nymph."),
    ("A pupil kept a caterpillar in a container with fresh leaves. Why did she add fresh leaves every day?", "Caterpillars need a lot of food to grow.", ["The pupa needs leaves to eat.", "The leaves keep the container dry.", "Butterflies lay eggs only on dry leaves."], "The larva stage eats the most."),
    ("A pupil changes the water in his vase every 3 days. A mosquito egg takes 2 days to hatch and the larva takes 7 days to become a pupa. Can adult mosquitoes come from the vase?", "No. The larvae are thrown away before they can become pupae.", ["Yes, the eggs hatch into adults straight away.", "Yes, because larvae can fly away.", "No, because mosquitoes do not lay eggs in water."], "Changing the water often breaks the life cycle."),
    ("Which observation shows that a butterfly's life cycle is complete?", "The adult butterfly lays eggs.", ["The caterpillar eats leaves.", "The pupa hangs from a twig.", "The egg is yellow."], "Laying eggs starts the cycle again."),
    ("Mei Ling saw frog eggs in a pond in March. What would she most likely see in the pond a few weeks later?", "tadpoles", ["chicks", "nymphs", "pupae"], "Frog eggs hatch into tadpoles."),
])


def body():
    think = ("<p><b>A life cycle is the stages an animal goes through as it grows into an adult that can reproduce.</b></p>"
             "<ul><li><b>Four stages</b>: egg → larva → pupa → adult (butterfly, mosquito, beetle). The larva looks very different from the adult.</li>"
             "<li><b>Three stages</b>: egg → nymph → adult (cockroach, grasshopper). The nymph looks like a small adult without wings.</li>"
             "<li>Frog: egg → tadpole → young frog → adult frog. Chicken: egg → chick → adult.</li></ul>")
    ex = [("Which stage comes after the larva in a mosquito's life cycle?", ["Egg → larva → pupa → adult", "The pupa comes next"], "The pupa."),
          ("Why should we not leave water in pails at home?", ["Mosquitoes lay eggs in still water", "Larvae grow there"], "To stop mosquitoes from breeding.")]
    mist = ["Thinking a cockroach has a pupa stage. It has egg, nymph and adult only.",
            "Thinking a caterpillar is a different kind of animal. It is the larva of a butterfly.",
            "Thinking a tadpole is a fish. It is a young frog.",
            "Thinking the pupa eats a lot. It does not eat while it changes."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Stages of a life cycle", B1 + [(g_next, 5), (g_count, 4), (g_has, 3)]),
        ("Young and adults", B2 + [(g_like, 5), (g_next, 4), (g_where, 3)]),
        ("Three or four stages", [(g_order, 3), (g_has, 5), (g_count, 3), (g_next, 4), (LC.g_next, 3), (LC.g_stage, 2)]),
        ("Life cycles around us", B3 + [(g_where, 3), (g_table, 4), (LC.g_feat, 2), (g_like, 2), (g_has, 2)]),
        ("PSLE-style observations", B5 + [(g_table, 6), (LC.g_next, 3), (g_order, 2), (g_where, 2)]),
    ])
    make_sg(3, "life-cycles-of-animals", 4, "Cycles", "Cycles in plants and animals (Life cycles of animals)",
            "Show an understanding that different animals have different life cycles: some have three stages (egg, nymph, adult) and some have four stages "
            "(egg, larva, pupa, adult); frogs and chickens also go through stages as they grow. Observe that young animals may or may not resemble their parents "
            "(summary of the MOE Primary Science Syllabus).",
            "Life Cycles of Animals",
            "Primary 3 Science: Life Cycles of Animals Worksheets (with Answers)",
            "Life cycles of animals",
            "Free Primary 3 science worksheets for Singapore pupils on life cycles of animals: butterfly, mosquito, beetle, cockroach, grasshopper, frog and chicken, larva, pupa and nymph. 100 questions with answers.",
            "Animals grow through stages to become adults.",
            "Egg, larva, pupa, adult; or egg, nymph, adult.",
            body(),
            [("What is the difference between a larva and a nymph?", "A larva looks very different from the adult and later becomes a pupa. A nymph looks like a small adult without wings and has no pupa stage."),
             ("Which animals have a four-stage life cycle?", "The butterfly, mosquito and mealworm beetle: egg, larva, pupa and adult."),
             ("Why do we remove stagnant water in Singapore?", "Mosquitoes lay eggs in still water. Removing it stops the larvae from growing into adults, which helps to prevent dengue.")],
            sets)


if __name__ == "__main__":
    main()
