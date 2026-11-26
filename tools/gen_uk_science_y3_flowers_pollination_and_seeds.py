# -*- coding: utf-8 -*-
"""
UK Year 3 science: Flowers, Pollination and Seeds (Plants)
  python tools/gen_uk_science_y3_flowers_pollination_and_seeds.py
The part flowers play in the life cycle of flowering plants: the life cycle from seed to seed, simple flower parts,
pollination by insects and wind, seed formation inside fruits, and seed dispersal.
Reuses the pollination-step, pollination-type and dispersal questions of the Year 5 reproduction unit (new seed) and
adds Year 3 questions on the life cycle, flower parts, fruits and seeds.
Wrong answers come from real mistakes: "flowers are only for decoration", "fruits have nothing to do with seeds",
"all seeds are spread by wind", "bees visit flowers to help the plant on purpose".
"""
import uk_sci
from uk_sci import Unit, item, bank, lesson, make_uk, People, once
import gen_uk_science_y5_reproduction_in_plants_and_animals as Y5

Y5.U = Unit(61304)
Y5.R = Y5.U.R
Y5.P = People(Y5.R)
uk_sci.USED.clear()
U, R, P = Y5.U, Y5.R, Y5.P

CYC = ["a seed", "germination (the seed starts to grow)", "a seedling", "an adult plant", "flowers", "pollination", "new seeds forming inside a fruit", "seed dispersal"]


def g_cycle():
    if R.random() < 0.55:
        i, j = sorted(R.sample(range(len(CYC)), 2))
        if j - i > 3 or not once(("cf", i, j)):
            return None
        a, b = CYC[i], CYC[j]
        o = [a, b] if R.random() < 0.5 else [b, a]
        return item("In the life cycle of a flowering plant, which comes first: %s or %s?" % tuple(o), a, [b, "They happen at the same time.", "Neither is part of the life cycle."],
                    "Seed → germination → seedling → adult plant → flowers → pollination → seeds in a fruit → dispersal.")
    i = R.randrange(len(CYC) - 1)
    k = R.random() < 0.5
    if not once(("cy", i, k)):
        return None
    if k:
        a = CYC[i + 1]
        return item("In the life cycle of a flowering plant, what comes after %s?" % CYC[i], a, R.sample([x for x in CYC if x not in (a, CYC[i])], 3),
                    "Seed → germination → seedling → adult plant → flowers → pollination → seeds in a fruit → dispersal.")
    a = CYC[i]
    return item("In the life cycle of a flowering plant, what comes just before %s?" % CYC[i + 1], a, R.sample([x for x in CYC if x not in (a, CYC[i + 1])], 3),
                "Seed → germination → seedling → adult plant → flowers → pollination → seeds in a fruit → dispersal.")


FP = [("the petals", "attract insects with their colour and scent"), ("the anthers", "make pollen"), ("the stigma", "catch pollen with its sticky top"),
      ("the ovary", "hold the tiny ovules that become seeds"), ("the sepals", "protect the flower while it is a bud"), ("the nectar", "give insects a sweet drink")]


def g_fpart():
    p, j = R.choice(FP)
    k = R.random() < 0.5
    if not once(("fp", p, k)):
        return None
    if k:
        return item("What is the job of %s of a flower?" % p, "to " + j, ["to " + x[1] for x in R.sample([x for x in FP if x[0] != p], 3)], "Each part of a flower helps make seeds.")
    return item("Which part of a flower has this job: to %s?" % j, p, R.sample([x[0] for x in FP if x[0] != p], 3), "Each part of a flower helps make seeds.")


B1 = bank([
    ("What is the main job of a flower?", "to make seeds", ["to make food from sunlight", "to take in water", "to hold the plant up"], "Seeds grow into new plants."),
    ("What is pollen?", "a fine powder made by flowers that is needed to make seeds", ["a kind of soil", "a sweet drink for insects", "the seed of a plant"], "Often yellow."),
    ("Which animals carry pollen from flower to flower?", "insects such as bees and butterflies", ["worms", "fish", "snails only"], "Pollen sticks to their bodies."),
    ("Why do bees visit flowers?", "to drink nectar and collect pollen for food", ["to help the plant on purpose", "to sleep", "to lay eggs in every flower"], "The plant gets pollinated as a side effect."),
    ("What does a seed grow into?", "a new plant", ["a flower petal", "a rock", "an insect"], "The life cycle starts again."),
    ("What is germination?", "when a seed starts to grow", ["when a flower opens", "when a leaf falls", "when pollen is made"], "A root and shoot appear."),
    ("Where are the seeds of an apple?", "inside the fruit, in the core", ["on the leaves", "in the roots", "in the stalk"], "The fruit protects the seeds."),
    ("What does pollination mean?", "moving pollen from one flower to another of the same kind", ["a seed falling off a tree", "a plant drinking water", "a leaf making food"], "Needed before seeds form."),
    ("What is a seedling?", "a young plant that has just grown from a seed", ["a seed that has not started growing", "a flower bud", "a fully grown tree"], "It has its first leaves."),
    ("Which grows first from a germinating seed?", "a tiny root", ["a flower", "a fruit", "new seeds"], "The root grows down, then a shoot grows up."),
])
B3 = bank([
    ("Is a tomato a fruit?", "Yes. It grows from a flower and has seeds inside.", ["No, it is a root.", "No, it is a leaf.", "No, fruits must be sweet."], "Scientists call anything with seeds from a flower a fruit."),
    ("What grows into a fruit after pollination?", "the ovary of the flower", ["the petals", "the roots", "the leaves"], "The ovary swells around the seeds."),
    ("What happens to the petals after a flower is pollinated?", "They wither and fall off.", ["They turn into roots.", "They become seeds.", "They grow bigger."], "Their job is done."),
    ("Which of these is a seed?", "an acorn", ["a tulip petal", "an oak leaf", "a carrot root"], "It can grow into an oak tree."),
    ("How many seeds does a pea pod usually have?", "several, in a row", ["none", "exactly one hundred", "only half a seed"], "Each pea is a seed."),
    ("Why are many fruits sweet and colourful?", "so animals eat them and spread the seeds", ["to scare animals away", "to keep the seeds cold", "to stop the seeds growing"], "Animals carry the seeds away."),
    ("What does a seed need to start growing?", "water and warmth", ["darkness and salt", "only sunlight", "nothing at all"], "Germination."),
    ("Why does a dandelion seed have a fluffy top?", "so the wind can carry it far away", ["to keep it warm", "to attract bees", "to make it heavy"], "A tiny parachute."),
])
B5 = bank([
    ("A gardener puts a net over a strawberry plant so no insects reach the flowers. What will happen?", "Few or no strawberries will grow.", ["More strawberries will grow.", "The plant will grow taller.", "The flowers will turn into leaves."], "No pollination, no fruit."),
    ("Why is it good for a plant that its seeds land far away from it?", "The new plants will not have to share light, water and space with the parent.", ["The parent wants to be alone.", "Seeds grow only in rivers.", "It makes the parent plant grow faster."], "Less crowding."),
    ("Why do some farmers keep beehives near their apple trees?", "The bees pollinate the apple flowers, so more apples grow.", ["Bees eat the apples.", "Bees keep the trees warm.", "Bees water the trees."], "Pollinators help crops."),
    ("Grass flowers are small and green. How are they pollinated?", "by the wind", ["by bees attracted to bright colours", "by water", "they are never pollinated"], "No need to attract insects."),
    ("Why do some plants make thousands of seeds?", "Many seeds are eaten or land in poor places, so only a few grow.", ["Every seed always grows.", "Seeds are too small to grow.", "Plants like to be crowded."], "More chances."),
])


def body():
    think = ("<p><b>Flowers make seeds, and seeds grow into new plants.</b></p>"
             "<ul><li>Insects or the wind carry pollen from flower to flower: this is pollination.</li>"
             "<li>After pollination, seeds form inside a fruit.</li>"
             "<li>Seeds are spread (dispersed) by wind, water, animals or by bursting pods, then grow into new plants.</li></ul>")
    ex = [("What comes after pollination?", ["Pollen reaches the flower"], "seeds form inside a fruit"),
          ("Dandelion seeds travel how?", ["Fluffy parachutes"], "by the wind")]
    mist = ["Thinking flowers are only for decoration.", "Thinking fruits have nothing to do with seeds.", "Thinking all seeds are spread by the wind."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Flowers and seeds", B1 + [(g_cycle, 7), (g_fpart, 3)]),
        ("Pollination", [(g_fpart, 6), (Y5.g_poll, 5), (Y5.g_step, 7), (g_cycle, 2)]),
        ("Seeds and fruits", B3 + [(Y5.g_disp, 6), (Y5.g_disp2, 6)]),
        ("The life cycle", [(g_cycle, 14), (Y5.g_disp2, 3), (Y5.g_step, 2), (Y5.g_disp, 1)]),
        ("Thinking about seeds", B5 + [(g_cycle, 6), (Y5.g_poll, 2), (g_fpart, 2), (Y5.g_disp, 3), (Y5.g_disp2, 2)]),
    ])
    make_uk(3, "flowers-pollination-and-seeds", 4, "Plants",
            "Explore the part that flowers play in the life cycle of flowering plants, including pollination, seed formation and seed dispersal.",
            "Flowers, Pollination and Seeds",
            "Year 3 Science: Flowers, Pollination and Seeds Worksheets (Plant Life Cycle)",
            "Flowers and Seeds",
            "Free Year 3 science worksheets on flowers and the plant life cycle: pollination by insects and wind, seeds and fruits, and how seeds are dispersed. 100 questions with answers.",
            "Flowers make seeds.",
            "Pollination, then seeds in a fruit, then dispersal.",
            body(),
            [("Why do plants have flowers?", "Flowers make seeds. Pollen from one flower reaches another, and then seeds form inside a fruit."),
             ("What is pollination?", "Pollination is moving pollen from one flower to another of the same kind. Insects such as bees and the wind do this."),
             ("How are seeds dispersed?", "Seeds are spread by the wind (dandelions, sycamores), by animals (blackberries, burdock), by water (coconuts) or by pods that burst open (peas).")],
            sets)


if __name__ == "__main__":
    main()
