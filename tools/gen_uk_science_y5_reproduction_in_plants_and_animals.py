# -*- coding: utf-8 -*-
"""
UK Year 5 science: Reproduction in Plants and Animals (Living things and their habitats)
  python tools/gen_uk_science_y5_reproduction_in_plants_and_animals.py
Sexual reproduction (two parents) and asexual reproduction (one parent: runners, bulbs, tubers, cuttings), the parts
of a flower, pollination by insects and wind, fertilisation, and seed dispersal.
Wrong answers come from real mistakes: "pollination and fertilisation are the same", "petals make the pollen",
"a strawberry runner needs two parents", "all seeds are spread by wind".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, People, once

U = Unit(61502)
R = U.R
P = People(R)

PART = [("the petals", "attract insects with colour and scent"), ("the anther", "make pollen"), ("the filament", "hold up the anther"),
        ("the stigma", "catch pollen on its sticky top"), ("the ovary", "hold the ovules that become seeds"),
        ("the sepals", "protect the flower when it is a bud"), ("the style", "join the stigma to the ovary"), ("the nectary", "make sweet nectar that insects drink")]


def g_part():
    p, j = R.choice(PART)
    k = R.random() < 0.5
    if not once(("pa", p, k)):
        return None
    if k:
        return item("What is the job of %s in a flower?" % p, "to " + j, ["to " + x[1] for x in R.sample([x for x in PART if x[0] != p], 3)], "The job of %s is to %s." % (p, j))
    return item("Which part of a flower has this job: to %s?" % j, p, R.sample([x[0] for x in PART if x[0] != p], 3), "The job of %s is to %s." % (p, j))


ASEX = [("Strawberry plants send out runners that grow new plants.", "runners"), ("A potato left in a dark cupboard grows shoots that become new plants.", "tubers"),
        ("Daffodils grow new bulbs beside the old bulb.", "bulbs"), ("A gardener plants a piece of stem cut from a geranium.", "cuttings"),
        ("A spider plant grows little plantlets on long stems.", "plantlets"), ("Garlic cloves are planted to grow new garlic.", "bulbs")]
SCEN = [("Pollen from one apple tree fertilises the flower of another.", "sexual"), ("A strawberry runner grows into a new plant.", "asexual"),
        ("A hen and a cockerel produce a fertilised egg.", "sexual"), ("A cutting from a willow tree grows roots in water.", "asexual"),
        ("A frog's eggs are fertilised by a male frog.", "sexual"), ("A potato tuber sprouts into a new plant.", "asexual"),
        ("Two rabbits have a litter of babies.", "sexual"), ("A daffodil bulb divides to make a new bulb.", "asexual"),
        ("A starfish arm that breaks off grows into a whole new starfish.", "asexual"), ("Bees carry pollen between sunflowers.", "sexual")]


def g_asex():
    s, a = R.choice(ASEX)
    if not once(("as", s)):
        return None
    return item("%s Which kind of asexual reproduction is this?" % s, a, R.sample([x for x in ["runners", "tubers", "bulbs", "cuttings", "plantlets"] if x != a], 3),
                "Asexual reproduction needs only one parent; the new plant is identical to it.")


def g_scen():
    s, a = R.choice(SCEN)
    if not once(("sc", s)):
        return None
    ans = "sexual reproduction (two parents)" if a == "sexual" else "asexual reproduction (one parent)"
    return item("%s Is this sexual or asexual reproduction?" % s, ans, ["asexual reproduction (one parent)" if a == "sexual" else "sexual reproduction (two parents)", "germination", "photosynthesis"],
                "Sexual reproduction joins cells from two parents; asexual needs one parent.")


DISP = [("a dandelion", "by the wind, with fluffy parachutes"), ("a sycamore", "by the wind, with wings that spin"), ("a burdock", "by animals, with hooks that stick to fur"),
        ("a blackberry", "by animals that eat the fruit and drop the seeds"), ("a coconut", "by water, floating to new places"), ("a pea plant", "by the pod bursting open"),
        ("an acorn", "by animals, such as squirrels that bury them"), ("a cherry", "by animals that eat the fruit and drop the seeds"),
        ("goosegrass (cleavers)", "by animals, with hooks that stick to fur"), ("gorse", "by the pod bursting open"), ("a water lily", "by water, floating to new places"),
        ("a thistle", "by the wind, with fluffy parachutes")]


def g_disp():
    p, d = R.choice(DISP)
    if not once(("di", p)):
        return None
    w = sorted({x[1] for x in DISP if x[1].split(",")[0] != d.split(",")[0]})
    return item("How are the seeds of %s usually dispersed?" % p, d, R.sample(w, 3), "Seeds are spread away from the parent so the new plants have space, light and water.")


STEPS = ["A bee visits a flower and pollen sticks to its body.", "The bee carries the pollen to another flower of the same kind.",
         "Pollen lands on the sticky stigma (pollination).", "The pollen joins with an ovule in the ovary (fertilisation).",
         "The ovule grows into a seed, and the ovary becomes a fruit.", "The seeds are dispersed and can grow into new plants."]


def g_step():
    i = R.randrange(len(STEPS) - 1)
    k = R.random() < 0.5
    if not once(("st", i, k)):
        return None
    if k:
        a = STEPS[i + 1]
        return item("\"%s\" What happens next?" % STEPS[i], a, R.sample([x for x in STEPS if x not in (a, STEPS[i])], 3), "Pollination → fertilisation → seed and fruit → dispersal.")
    a = STEPS[i]
    return item("\"%s\" What happened just before?" % STEPS[i + 1], a, R.sample([x for x in STEPS if x not in (a, STEPS[i + 1])], 3), "Pollination → fertilisation → seed and fruit → dispersal.")


POLL = [("bright, colourful petals", "insect-pollinated"), ("a sweet scent", "insect-pollinated"), ("sticky, spiky pollen", "insect-pollinated"),
        ("sweet nectar", "insect-pollinated"), ("anthers that hang outside the flower", "wind-pollinated"), ("huge amounts of light, smooth pollen", "wind-pollinated"),
        ("feathery stigmas", "wind-pollinated"), ("small, green petals or none at all", "wind-pollinated")]


def g_poll():
    f, a = R.choice(POLL)
    if not once(("po", f)):
        return None
    return item("A flower has %s. How is it most likely pollinated?" % f, "It is " + a + ".", ["It is " + ("wind-pollinated" if a == "insect-pollinated" else "insect-pollinated") + ".",
                "It does not need pollination.", "It is pollinated by water only."], "Insect flowers attract; wind flowers make lots of light pollen.")


CMP = [("needs only one parent", "asexual"), ("makes offspring identical to the parent", "asexual"), ("makes offspring that vary", "sexual"),
       ("needs pollination in flowering plants", "sexual"), ("happens with runners, bulbs and tubers", "asexual"), ("joins a male cell and a female cell", "sexual"),
       ("can make many copies quickly", "asexual"), ("helps a species cope with change over many generations", "sexual"), ("produces seeds in flowering plants", "sexual")]


def g_cmp():
    f, a = R.choice(CMP)
    if not once(("cm", f)):
        return None
    ans = "sexual reproduction" if a == "sexual" else "asexual reproduction"
    return item("Which kind of reproduction %s?" % f, ans, ["asexual reproduction" if a == "sexual" else "sexual reproduction", "both kinds equally", "neither kind"],
                "Sexual: two parents, offspring vary. Asexual: one parent, identical offspring.")


def g_disp2():
    p, d = R.choice(DISP)
    if not once(("d2", p)):
        return None
    w = R.sample([x[0] for x in DISP if x[1].split(",")[0] != d.split(",")[0]], 3)
    return item("Which plant's seeds are usually dispersed %s?" % d, p, w, "Match the seed or fruit to how it travels.")


def g_dist():
    who = P.next()[0]
    seed = R.choice(["sycamore", "dandelion", "ash", "lime"])
    xs = R.sample(range(40, 180, 5), 5)
    k = R.choice(["far", "near", "mean", "range"])
    if not once(("ds", tuple(xs), k)):
        return None
    tab = table(["Test", "Distance travelled (cm)"], [[str(i + 1), str(x)] for i, x in enumerate(xs)])
    intro = tab + "%s dropped a %s seed from the same height in front of a fan five times. " % (who, seed)
    from sci_phys import uniq, num
    if k == "far":
        g = "%d cm" % max(xs)
        return item(intro + "What was the furthest distance?", g, uniq(g, ["%d cm" % x for x in xs]), "Find the largest number.")
    if k == "near":
        g = "%d cm" % min(xs)
        return item(intro + "What was the shortest distance?", g, uniq(g, ["%d cm" % x for x in xs]), "Find the smallest number.")
    if k == "range":
        g = "%d cm" % (max(xs) - min(xs))
        return item(intro + "What is the range of the results (largest − smallest)?", g, uniq(g, ["%d cm" % max(xs), "%d cm" % min(xs), "%d cm" % (max(xs) + min(xs)), "%d cm" % (max(xs) - min(xs) + 10)]),
                    "%d − %d = %d cm." % (max(xs), min(xs), max(xs) - min(xs)))
    if sum(xs) % 5:
        return None
    m = sum(xs) // 5
    g = "%d cm" % m
    return item(intro + "What is the mean distance?", g, uniq(g, ["%d cm" % sum(xs), "%d cm" % (m + 5), "%d cm" % (m - 5), "%d cm" % sorted(xs)[2]]), "%d ÷ 5 = %d cm." % (sum(xs), m))


B1 = bank([
    ("What is reproduction?", "making new living things of the same kind", ["growing taller", "breathing", "moving around"], "A life process."),
    ("How many parents are needed for sexual reproduction?", "two", ["one", "none", "four"], "Male and female cells join."),
    ("How is the offspring of asexual reproduction different from sexual reproduction?", "It is identical to its one parent.", ["It has two parents.", "It is a different species.", "It is always smaller."], "Clones."),
    ("What is pollination?", "moving pollen from an anther to a stigma", ["a seed growing into a plant", "a plant making food", "a seed falling to the ground"], "Often by insects or wind."),
    ("What is fertilisation in a flower?", "pollen joining with an ovule to start a seed", ["a farmer adding manure", "a seed being blown away", "a petal falling off"], "After pollination."),
    ("Why do plants disperse their seeds?", "so new plants are not crowded and can get enough light, water and space", ["to make the parent plant grow", "to feed the wind", "because seeds are heavy"], "Less competition."),
    ("What is the male part of a flower called?", "the stamen (anther and filament)", ["the carpel", "the sepal", "the petal"], "It makes pollen."),
    ("What is the female part of a flower called?", "the carpel (stigma, style and ovary)", ["the stamen", "the sepal", "the anther"], "It makes ovules."),
])
B5 = bank([
    ("Why do gardeners grow new plants from cuttings?", "The new plants are identical to a parent plant they like.", ["Cuttings grow from seeds.", "Cuttings need two parents.", "Cuttings make different flowers."], "Asexual copies."),
    ("Why is it a problem if bee numbers fall?", "Fewer flowers would be pollinated, so fewer fruits and seeds would form.", ["There would be more honey.", "Plants would grow faster.", "Wind would stop."], "Pollinators matter."),
    ("How could you investigate which seed design falls most slowly?", "Drop model seeds with different wing sizes from the same height and time them.", ["Throw them as hard as possible.", "Drop them from different heights.", "Plant them all."], "Fair test."),
    ("Why might wind-pollinated plants cause hay fever?", "They release huge amounts of light pollen into the air.", ["They have bright petals.", "They make nectar.", "They have no pollen."], "Grass pollen."),
    ("Why does sexual reproduction help a species survive changes?", "Offspring vary, so some may suit new conditions.", ["Offspring are all identical.", "It is faster than asexual.", "It needs no parents."], "Variation."),
])


def body():
    think = ("<p><b>Plants and animals reproduce to make new living things of the same kind.</b></p>"
             "<ul><li>Sexual reproduction needs two parents; offspring vary. Asexual reproduction needs one parent; offspring are identical (runners, bulbs, tubers, cuttings).</li>"
             "<li>In a flower, the anther makes pollen and the stigma catches it. Pollination → fertilisation → seed and fruit.</li>"
             "<li>Seeds are dispersed by wind, animals, water or by bursting pods.</li></ul>")
    ex = [("Strawberry runner: how many parents?", ["The new plant grows from one plant"], "one: asexual"),
          ("Burdock seeds have hooks. Dispersed how?", ["Hooks catch on fur"], "by animals")]
    mist = ["Mixing up pollination and fertilisation.", "Thinking petals make the pollen.", "Thinking all seeds are spread by the wind."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Two kinds of reproduction", B1 + [(g_scen, 8), (g_asex, 4)]),
        ("Parts of a flower", [(g_part, 14), (g_poll, 6)]),
        ("Pollination and fertilisation", [(g_step, 10), (g_poll, 2), (g_cmp, 8)]),
        ("Seed dispersal", [(g_disp, 12), (g_disp2, 8)]),
        ("Thinking like a gardener", B5 + [(g_dist, 10), (g_asex, 2), (g_scen, 2), (g_part, 1)]),
    ])
    make_uk(5, "reproduction-in-plants-and-animals", 2, "Living things and their habitats",
            "Describe the life process of reproduction in some plants and animals.",
            "Reproduction in Plants and Animals",
            "Year 5 Science: Reproduction in Plants and Animals Worksheets (Flowers, Pollination, Seeds)",
            "Reproduction",
            "Free Year 5 science worksheets on reproduction in plants and animals: sexual and asexual reproduction, parts of a flower, pollination, fertilisation and seed dispersal. 100 questions with answers.",
            "Two parents or one: new life begins.",
            "Flowers are pollinated and fertilised to make seeds; runners and bulbs make copies.",
            body(),
            [("What is the difference between sexual and asexual reproduction?", "Sexual reproduction needs two parents and the offspring vary. Asexual reproduction needs one parent and the offspring are identical to it."),
             ("What is the difference between pollination and fertilisation?", "Pollination is pollen moving from an anther to a stigma. Fertilisation happens later, when the pollen joins with an ovule in the ovary to start a seed."),
             ("How are seeds dispersed?", "By the wind (dandelion, sycamore), by animals (burdock hooks, berries that are eaten), by water (coconut) or by pods bursting open (peas, gorse).")],
            sets)


if __name__ == "__main__":
    main()
