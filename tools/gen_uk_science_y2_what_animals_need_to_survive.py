# -*- coding: utf-8 -*-
"""
UK Year 2 science: What Animals Need to Survive (Animals, including humans)
  python tools/gen_uk_science_y2_what_animals_need_to_survive.py
Find out about and describe the basic needs of animals, including humans, for survival (water, food and air): how
different animals get air, what pets need to be cared for, and which need is most urgent.
Wrong answers come from real mistakes: "fish do not need air", "animals only need food", "pets can look after
themselves", "plants and animals need sweets".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K

U = Unit(61208)
R = U.R
P = People(R)

NEED = ["water", "food", "air"]
NOT = ["toys", "a television", "sweets", "money", "a bicycle", "music", "a mobile phone", "fizzy drinks", "a party", "computer games"]


def g_need():
    a = R.choice(NEED)
    w = R.sample(NOT, 3)
    if not once(("nd", a), 5):
        return None
    o = sorted([a] + w)
    return item("What do all animals need to stay alive: %s or %s?" % (", ".join(o[:3]), o[3]), a, w, "All animals, including humans, need water, food and air.")


PET = [("a goldfish", "clean water, fish food and air in the water"), ("a hamster", "water, hamster food and a clean, airy cage"),
       ("a dog", "water, dog food, fresh air and walks"), ("a rabbit", "water, hay and vegetables, and a hutch with fresh air"),
       ("a cat", "water, cat food and a safe place to rest"), ("a budgie", "water, seeds and a clean cage"),
       ("a guinea pig", "water, hay and vegetables, and a clean hutch"), ("a pet snail", "damp leaves, water spray and air holes in its tank")]


def g_pet():
    a, n = R.choice(PET)
    if not once(("pe", a)):
        return None
    w = ["only toys and a bed", "nothing; pets look after themselves", "sweets and fizzy drinks"]
    return item("What does %s need to stay alive and healthy?" % a, n, w, "Pets need water, the right food and air, and someone to care for them.")


AIR = [("a fish", "with gills, from the water"), ("a human", "with lungs, by breathing in"), ("a whale", "with lungs, by coming up to the surface"),
       ("a dog", "with lungs, by breathing in"), ("a tadpole", "with gills, from the water"), ("a cat", "with lungs, by breathing in"),
       ("a bird", "with lungs, by breathing in")]


def g_air():
    a, h = R.choice(AIR)
    if not once(("ai", a)):
        return None
    w = [x for x in ["with gills, from the water", "with lungs, by breathing in", "with lungs, by coming up to the surface", "it does not need air",
                     "through its fur", "through its feet"] if x != h and not (h.startswith("with lungs") and x == "with lungs, by breathing in")]
    return item("How does %s get the air it needs?" % a, h, R.sample(w, 3), "All animals need air. Fish use gills; mammals and birds use lungs.")


ORDER = [("air", "a few minutes"), ("water", "a few days"), ("food", "a few weeks")]


def g_order():
    k = R.choice(["first", "longest", "how"])
    i = R.randrange(3)
    if not once(("or", k, i if k == "how" else 0)):
        return None
    if k == "first":
        return item("Which does a person need most urgently: food, water or air?", "air", ["food", "water", "toys"], "Without air we can live only a few minutes.")
    if k == "longest":
        return item("Which can a person live without for the longest: food, water or air?", "food", ["air", "water", "sleep for one minute"], "We can live a few weeks without food, but only days without water.")
    n, t = ORDER[i]
    return item("About how long can a person live without %s?" % n, t, [x[1] for x in ORDER if x[1] != t] + ["for ever"], "Air: minutes. Water: days. Food: weeks.")


SCEN = [("A goldfish bowl has not been cleaned for weeks.", "The fish may not get enough clean water and air."),
        ("A hamster's water bottle is empty.", "It needs fresh water every day."),
        ("A dog is left in a hot car with the windows shut.", "It can overheat and cannot get fresh air; this is dangerous."),
        ("A rabbit is given only sweets.", "Sweets are not its food; it needs hay and vegetables."),
        ("A pupil's lunchbox has no drink.", "People need water to stay healthy."),
        ("A cat's food bowl is empty for two days.", "It needs food every day.")]


def g_scen():
    s, a = R.choice(SCEN)
    if not once(("sc", s)):
        return None
    return item("%s Why is this a problem?" % s, a, R.sample([x[1] for x in SCEN if x[1] != a], 3), "Animals need water, food and air.")


PFOOD = [("a rabbit", "hay and fresh vegetables"), ("a goldfish", "fish flakes"), ("a dog", "dog food"), ("a cat", "cat food"), ("a budgie", "bird seed"),
         ("a hamster", "hamster mix with seeds and grains"), ("a tortoise", "leafy greens such as dandelion leaves"), ("a horse", "grass and hay")]
JUNK = ["chocolate", "crisps", "sweets", "fizzy drinks", "cake", "biscuits"]


def g_pfood():
    a, f = R.choice(PFOOD)
    if not once(("pf", a)):
        return None
    return item("Which is the best food for %s?" % a, f, R.sample(JUNK, 3), "Each animal needs the right kind of food.")


WILD = [("an owl", "by hunting mice and voles"), ("a squirrel", "by finding nuts and seeds"), ("a blackbird", "by pulling worms from the soil"),
        ("a hedgehog", "by eating beetles, worms and slugs"), ("a heron", "by catching fish in a river"), ("a deer", "by eating grass and leaves"),
        ("a fox", "by hunting rabbits and finding berries"), ("a bee", "by drinking nectar from flowers"), ("a spider", "by catching insects in its web"),
        ("a robin", "by eating insects, worms and seeds")]


def g_wild():
    a, h = R.choice(WILD)
    if not once(("wi", a)):
        return None
    return item("How does %s get its food in the wild?" % a, h, R.sample([x[1] for x in WILD if x[1] != h], 3), "Wild animals find their own food.")


def g_table():
    who = P.next()[0]
    kids = R.sample(["Ava", "Leo", "Isla", "Noah", "Ruby", "Kai", "Maya", "Theo"], 4)
    v = R.sample(range(2, 9), 4)
    k = R.choice(["most", "least", "read", "diff", "total"])
    ri, rj = R.sample(range(4), 2)
    if not once(("tb", tuple(kids), tuple(v), k)):
        return None
    tab = table(["Pupil", "Glasses of water drunk in a day"], [[n, str(x)] for n, x in zip(kids, v)])
    intro = tab + "%s's class counted how many glasses of water they drank in a day. " % who
    if k == "most":
        a = kids[v.index(max(v))]
        return item(intro + "Who drank the most water?", a, [x for x in kids if x != a], "The biggest number.")
    if k == "least":
        a = kids[v.index(min(v))]
        return item(intro + "Who drank the least water?", a, [x for x in kids if x != a], "The smallest number.")
    if k == "read":
        g = str(v[ri])
        return item(intro + "How many glasses did %s drink?" % kids[ri], g, [str(x) for x in v if x != v[ri]][:3], "Read the row.")
    if k == "diff":
        a, b = max(v[ri], v[rj]), min(v[ri], v[rj])
        hi, lo = (kids[ri], kids[rj]) if v[ri] > v[rj] else (kids[rj], kids[ri])
        g = str(a - b)
        w = list(dict.fromkeys([str(a), str(b), str(a + b), str(a - b + 1)]))
        return item(intro + "How many more glasses did %s drink than %s?" % (hi, lo), g, [x for x in w if x != g][:3], "%d − %d = %d." % (a, b, a - b))
    t = v[ri] + v[rj]
    g = str(t)
    w = list(dict.fromkeys([str(v[ri]), str(v[rj]), str(t + 1), str(t - 1)]))
    return item(intro + "How many glasses did %s and %s drink altogether?" % (kids[ri], kids[rj]), g, [x for x in w if x != g][:3], "%d + %d = %d." % (v[ri], v[rj], t))


B1 = bank([
    ("What are the three things all animals need to survive?", "water, food and air", ["toys, games and music", "sweets, crisps and fizzy drinks", "only food"], "Water, food, air."),
    ("Do humans need the same basic things as other animals?", "Yes. We need water, food and air too.", ["No, we need only toys.", "No, we need only sleep.", "No, humans are not animals."], "Humans are animals."),
    ("Why do we need food?", "to give us energy and help us grow", ["to keep our hair tidy", "to make us cold", "we do not need food"], "Food gives energy."),
    ("Why do we need water?", "Our bodies need it to work and stay healthy.", ["only to wash", "only to swim", "we do not need water"], "Drink plenty."),
    ("Do fish need air?", "Yes. They take it from the water with their gills.", ["No, never.", "Only at night.", "Only big fish."], "Gills, not lungs."),
    ("Where do wild animals get their water?", "from ponds, rivers, rain and the food they eat", ["from shops", "from taps only", "they never need water"], "Nature provides it."),
    ("Why do pets need people to look after them?", "They cannot get their own food and water in a cage or house.", ["Pets can go to the shop.", "They never get hungry.", "They make their own food."], "Caring for pets."),
    ("Which part of the body do we use to breathe?", "the lungs", ["the stomach", "the ears", "the bones"], "Air goes into the lungs."),
])
B5 = bank([
    ("Why should a pet's water be changed every day?", "so it stays clean and fresh", ["so the bowl looks shiny", "to make it colder", "pets do not drink"], "Clean water."),
    ("Why do fish tanks often have a pump that makes bubbles?", "It puts more air into the water for the fish.", ["It makes music.", "It feeds the fish.", "It keeps the fish dry."], "Fish need air too."),
    ("A pupil says plants and animals need exactly the same things. Is that right?", "Not quite: animals must eat food, but plants make their own.", ["Yes, exactly the same.", "No, animals need nothing.", "No, plants need sweets."], "Animals eat; plants make food."),
    ("Why do animals in the wild move to find water in a dry summer?", "They need water to survive.", ["They want a holiday.", "Water is not needed.", "They are looking for toys."], "Basic needs."),
    ("What should you check every day if you look after the class guinea pig?", "that it has food, fresh water and a clean hutch", ["that it has a new toy", "that it is watching TV", "nothing at all"], "Daily care."),
])


def body():
    pic = K.row(["drop", "apple", "cloud"], words=["water", "food", "air"], size=90, label="animals need water, food and air")
    ex = [("Which need is most urgent?", ["Minutes without it"], "air"),
          ("How does a fish get air?", ["From the water"], "with gills")]
    mist = ["Thinking fish do not need air.", "Thinking animals only need food.", "Thinking pets can look after themselves."]
    return kid_lesson(pic, "All animals need water, food and air.",
                      ["Humans are animals too.", "Fish take air from the water with gills.", "Pets need people to give them food and water."], ex, mist)


def main():
    sets = U.sets([
        ("Basic needs", B1 + [(g_need, 12)]),
        ("Getting air", [(g_air, 7), (g_order, 5), (g_scen, 6), (g_need, 2)]),
        ("Caring for animals", [(g_pet, 8), (g_pfood, 8), (g_wild, 4)]),
        ("Drinking water", [(g_table, 20)]),
        ("Thinking about needs", B5 + [(g_wild, 6), (g_table, 9)]),
    ])
    make_uk(2, "what-animals-need-to-survive", 8, "Animals, including humans",
            "Find out about and describe the basic needs of animals, including humans, for survival (water, food and air).",
            "What Animals Need to Survive",
            "Year 2 Science: What Animals Need Worksheets (Water, Food and Air)",
            "What Animals Need",
            "Free Year 2 science worksheets on what animals need to survive: water, food and air, how animals breathe, caring for pets and how wild animals find food. 100 questions with answers.",
            "Water, food and air.",
            "All animals, including humans, need these to stay alive.",
            body(),
            [("What do animals need to survive?", "All animals, including humans, need water, food and air."),
             ("Do fish need air?", "Yes. Fish take air from the water using their gills."),
             ("How do we look after a pet?", "Give it fresh water, the right food, a clean home with air, and check on it every day.")],
            sets)


if __name__ == "__main__":
    main()
