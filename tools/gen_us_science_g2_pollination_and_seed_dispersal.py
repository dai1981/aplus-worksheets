# -*- coding: utf-8 -*-
"""
US Grade 2 Science: Pollination and Seed Dispersal (2-LS2-2)
  python tools/gen_us_science_g2_pollination_and_seed_dispersal.py
Develop a simple model that mimics the function of an animal in dispersing seeds or pollinating plants.
Bees, butterflies and hummingbirds move pollen from flower to flower; animals carry seeds on fur, eat fruit and drop
the seeds, or bury nuts; wind and water also move seeds. Models: pipe cleaners, cotton balls, sticky tape, fuzzy socks.
Wrong answers come from real mistakes: "bees make flowers grow taller", "seeds spread by walking", "pollen is food for the plant".
"""
from sci_common import Unit, item, bank, kid_lesson, make, fig, table, People
import sci_kids as K

U = Unit(20106)
R = U.R
P = People(R)
USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


ANIMALS = [("bee", "a bee", "moves pollen from flower to flower", "pollination"),
           ("butterfly", "a butterfly", "moves pollen from flower to flower", "pollination"),
           ("bird", "a hummingbird", "moves pollen while drinking nectar", "pollination"),
           ("squirrel", "a squirrel", "buries acorns that grow into new trees", "seed dispersal"),
           ("dog", "a dog", "carries sticky seeds in its fur", "seed dispersal"),
           ("bird", "a robin", "eats berries and drops the seeds far away", "seed dispersal"),
           ("bear", "a bear", "eats berries and leaves the seeds in new places", "seed dispersal"),
           ("rabbit", "a rabbit", "carries burrs stuck in its fur", "seed dispersal")]


def g_job():
    pic, nm, how, job = R.choice(ANIMALS)
    who = P.next()[0]
    t = R.random() < 0.5
    if not once((nm, t)):
        return None
    if t:
        return item(fig(K.card(pic)) + "%s watches %s. %s %s. How is it helping plants?" % (who, nm, nm[0].upper() + nm[1:], how),
                    "It helps with " + job + ".", ["It helps with " + ("seed dispersal" if job == "pollination" else "pollination") + ".", "It makes the plant taller.", "It waters the plant."],
                    "Pollination moves pollen; seed dispersal moves seeds to new places.")
    w = [a[2] for a in ANIMALS if a[3] != job]
    w = list(dict.fromkeys(w))
    R.shuffle(w)
    return item(fig(K.card(pic)) + "%s sees %s near some plants. How can it help the plants?" % (who, nm), "It " + how + ".", ["It " + x + "." for x in w[:2]] + ["It paints the flowers."],
                "%s helps with %s." % (nm[0].upper() + nm[1:], job))


SEEDS = [("dandelion seeds with fluffy parachutes", "the wind"), ("maple seeds with wings", "the wind"), ("burrs with tiny hooks", "animal fur"),
         ("berries with seeds inside", "animals that eat them"), ("a coconut", "floating on water"), ("acorns", "squirrels that bury them"),
         ("sticky seeds on a stem", "animal fur"), ("cherries", "animals that eat them"), ("cottonwood seeds with fluff", "the wind"),
         ("seeds that float in a pond", "floating on water")]


def g_seed():
    s, a = R.choice(SEEDS)
    who = P.next()[0]
    if not once(("s", s)):
        return None
    w = sorted({x[1] for x in SEEDS if x[1] != a})
    return item("%s finds %s. What most likely carries these seeds to new places?" % (who, s), a, R.sample(w, 3), "The shape of a seed is a clue to how it travels.")


MODELS = [("a cotton ball on a stick, dabbed into chalk dust and then onto another paper flower", "a bee's fuzzy body picking up and moving pollen", "pollination", "bee"),
          ("a pipe cleaner pressed into powder and then onto a paper flower", "a bee's fuzzy body picking up and moving pollen", "pollination", "bee"),
          ("a fuzzy sock dragged through a pile of burrs", "an animal's fur picking up sticky seeds", "seed dispersal", "fur"),
          ("a piece of tape pressed onto seeds and walked across the room", "an animal's fur picking up sticky seeds", "seed dispersal", "fur"),
          ("a glove with velcro on the fingers touching seeds", "an animal's fur picking up sticky seeds", "seed dispersal", "fur"),
          ("a straw dipped in juice in a paper flower, with powder on the flower", "a hummingbird drinking nectar and getting pollen on its beak", "pollination", "hb"),
          ("a toy truck that picks up a seed and drops it in a new pot", "a squirrel carrying and burying a nut", "seed dispersal", "sq"),
          ("a spoon that digs a hole, drops in an acorn and covers it", "a squirrel carrying and burying a nut", "seed dispersal", "sq"),
          ("a fan blowing paper seeds with wings across a table", "wind spreading maple seeds", "seed dispersal", "wind"),
          ("a person blowing on a cotton-fluff seed across the floor", "wind spreading maple seeds", "seed dispersal", "wind"),
          ("a toy bird that 'eats' a bead from a paper berry and drops it in a new cup", "a bird eating berries and dropping the seeds far away", "seed dispersal", "eat")]


def g_model():
    m, what, job, grp = R.choice(MODELS)
    who = P.next()[0]
    t = R.random() < 0.5
    if not once((m, t)):
        return None
    if t:
        w = sorted({x[1] for x in MODELS if x[3] != grp})
        return item("%s builds a model: %s. What does the model act like?" % (who, m), what, R.sample(w, 3), "A model copies how something works.")
    return item("%s builds a model: %s. Does it model pollination or seed dispersal?" % (who, m), job,
                ["seed dispersal" if job == "pollination" else "pollination", "photosynthesis", "melting"], "Pollen moves between flowers; seeds move to new places.")


def g_pick():
    who = P.next()[0]
    kinds = R.sample(["bee", "butterfly", "squirrel", "dog", "rabbit", "bear"], 4)
    ask = R.choice(["pollen", "seeds"])
    good = [k for k in kinds if k in ("bee", "butterfly")]
    if len(good) != 1 or not once(("pk", tuple(kinds), ask)) or not once("pkall", 22):
        return None
    L = "ABCD"
    a = good[0]
    pic = K.row(kinds, words=["%s. %s" % (L[i], k) for i, k in enumerate(kinds)], size=90)
    return item(fig(pic) + "%s looks at these animals. Which one moves %s from flower to flower?" % (who, ask) if ask == "pollen" else
                fig(pic) + "%s looks at these animals. Which one is NOT likely to carry seeds in its fur or bury them?" % who,
                "%s (%s)" % (L[kinds.index(a)], a), ["%s (%s)" % (L[i], k) for i, k in enumerate(kinds) if k != a],
                "Bees and butterflies visit flowers. Furry animals and squirrels move seeds.")


TOOLS = [("cotton ball", 18, 26), ("pipe cleaner", 14, 22), ("feather", 9, 15), ("smooth plastic bead", 0, 3), ("glass marble", 0, 2), ("fuzzy pom-pom", 20, 30)]


def g_test():
    who = P.next()[0]
    rows = R.sample(TOOLS, 4)
    vals = [R.randint(lo, hi) for _, lo, hi in rows]
    if len(set(vals)) < 4:
        return None
    names = [r[0] for r in rows]
    k = R.choice(["best", "worst", "diff", "why", "cmp"])
    if not once(("t", tuple(names), k)) or not once(("tk", k), 3 if k == "why" else 9):
        return None
    tab = table(["Model bee body", "Specks of chalk picked up"], [[n, str(v)] for n, v in zip(names, vals)])
    b, w = names[vals.index(max(vals))], names[vals.index(min(vals))]
    if k == "best":
        return item(tab + "%s tested model bee bodies. Which one moves pollen most like a real bee?" % who, b, [n for n in names if n != b], "Most chalk picked up: %s. Real bees are fuzzy." % b)
    if k == "worst":
        return item(tab + "%s tested model bee bodies. Which one is the worst model of a bee?" % who, w, [n for n in names if n != w], "Fewest specks: %s. Smooth things do not hold pollen." % w)
    if k == "diff":
        x, y = sorted(R.sample(list(zip(names, vals)), 2), key=lambda t: -t[1])
        d = x[1] - y[1]
        return item(tab + "In %s's test, how many more specks did the %s pick up than the %s?" % (who, x[0], y[0]), str(d), [str(x[1]), str(x[1] + y[1]), str(d + 2)], "%d − %d = %d." % (x[1], y[1], d))
    if k == "cmp":
        x, y = R.sample(list(zip(names, vals)), 2)
        a = "more" if x[1] > y[1] else "fewer"
        return item(tab + "In %s's test, did the %s pick up more or fewer specks than the %s?" % (who, x[0], y[0]), a + " (%d and %d)" % (x[1], y[1]),
                    [("fewer" if a == "more" else "more") + " (%d and %d)" % (x[1], y[1]), "the same", "none at all"], "Compare %d and %d." % (x[1], y[1]))
    return item(tab + "In %s's test, why did the %s pick up the most chalk?" % (who, b), "It is fuzzy, like a bee's body.", ["It is the heaviest.", "It is the prettiest color.", "It is smooth and shiny."],
                "Fuzzy hairs catch pollen.")


B1 = bank([
    ("What is pollen?", "a yellow powder in flowers that helps make seeds", ["plant food", "a kind of water", "a type of leaf"], "Flowers need pollen to make seeds."),
    ("What is pollination?", "moving pollen from one flower to another", ["planting a seed", "watering a plant", "cutting a flower"], "Animals and wind can do it."),
    ("Why do bees visit flowers?", "to drink nectar, and they carry pollen while they do", ["to sleep", "to make the flowers taller", "to eat the leaves"], "Bees help flowers make seeds."),
    ("What is seed dispersal?", "seeds moving away from the parent plant", ["seeds growing roots", "flowers opening", "leaves falling"], "Seeds travel to new places."),
    ("Why is it good for seeds to travel?", "They have more room, light and water to grow.", ["They grow better under the parent plant.", "They get colder.", "They turn into flowers."], "Less crowding."),
    ("How do seeds with hooks travel?", "They stick to animal fur.", ["They swim.", "They fly with wings.", "They walk."], "Hooks grab fur."),
    ("How do fluffy dandelion seeds travel?", "The wind blows them.", ["They roll.", "Fish carry them.", "They dig."], "Fluff catches the wind."),
    ("What is a model?", "something we make to show how a real thing works", ["a real animal", "a type of seed", "a flower"], "Models help us explain."),
])
B5 = bank([
    ("Ava rubs a cotton ball on a paper flower with chalk, then on another flower. What does the chalk stand for?", "pollen", ["water", "seeds", "soil"], "Chalk dust is like pollen."),
    ("Leo walks through a field in fuzzy socks. Later he finds seeds stuck to them. What animal job did his socks copy?", "carrying seeds in fur", ["making honey", "eating leaves", "drinking nectar"], "Socks act like fur."),
    ("Mia's model bee has a smooth plastic body. Pollen does not stick. What should she change?", "add fuzzy material so pollen sticks", ["make it heavier", "paint it blue", "make it bigger"], "Real bees are fuzzy."),
    ("A tree's seeds fall straight down. What might happen to the young plants?", "They are crowded and compete for light and water.", ["They grow faster.", "They get more light.", "Nothing changes."], "Spreading out helps."),
    ("If there were no bees, what could happen to some fruit farms?", "Fewer flowers would make fruit.", ["More fruit would grow.", "Trees would grow taller.", "Nothing would change."], "Pollinators help make fruit."),
])


def body():
    pic = K.row(["bee", "flower", "squirrel", "tree"], words=["moves pollen", "flower", "moves seeds", "new tree"], size=95)
    ex = [("A bee drinks nectar and gets pollen on its body. Then it visits another flower. What happens?", ["It moves pollen."], "pollination"),
          ("A burr sticks to a dog's fur and falls off far away. What happens?", ["The seed moves."], "seed dispersal")]
    mist = ["Thinking bees make flowers grow taller. They move pollen.",
            "Thinking pollen is food for the plant.",
            "Mixing up pollination (pollen) and seed dispersal (seeds)."]
    return kid_lesson(pic, "Animals help plants make and spread seeds.",
                      ["Pollination: bees and birds move pollen.", "Seed dispersal: fur, eating, burying, wind, water.", "A model shows how it works."], ex, mist)


def main():
    sets = U.sets([
        ("Pollen and seeds", B1 + [(g_job, 6), (g_seed, 6)]),
        ("Animal helpers", [(g_job, 10), (g_pick, 10)]),
        ("How seeds travel", [(g_seed, 4), (g_pick, 6), (g_model, 6), (g_job, 4)]),
        ("Making models", [(g_model, 12), (g_test, 8)]),
        ("Testing models", B5 + [(g_test, 12), (g_pick, 3)]),
    ])
    make("grade-2", "pollination-and-seed-dispersal", 6, "2-LS2-2",
         "Develop a simple model that mimics the function of an animal in dispersing seeds or pollinating plants.",
         "Pollination and Seed Dispersal",
         "Grade 2 Pollination and Seed Dispersal Worksheets: How Animals Help Plants",
         "Pollination and Seeds",
         "Free grade 2 science worksheets on pollination and seed dispersal (NGSS 2-LS2-2): how bees move pollen, how seeds travel, and simple models. 100 picture questions with answers.",
         "Animals help plants.",
         "Bees move pollen. Animals, wind and water move seeds.",
         body(),
         [("What is pollination?", "Moving pollen from flower to flower so the plant can make seeds. Bees, butterflies and hummingbirds do this."),
          ("How do seeds travel?", "On animal fur, inside animals that eat fruit, buried by squirrels, blown by wind or floating on water."),
          ("What model can kids make?", "A cotton ball or pipe cleaner bee that picks up chalk pollen, or a fuzzy sock that picks up seeds.")],
         sets)


if __name__ == "__main__":
    main()
