# -*- coding: utf-8 -*-
"""
UK Year 2 science: Seeds and Bulbs (Plants)
  python tools/gen_uk_science_y2_seeds_and_bulbs.py
Observe and describe how seeds and bulbs grow into mature plants: which plants grow from seeds and which from bulbs,
what seeds grow into, the order a bean grows (root, shoot, leaves, flowers, new seeds), and measuring a growing
bean plant week by week.
Wrong answers come from real mistakes: "the shoot grows before the root", "a bulb is a kind of seed", "an acorn grows
into a conker tree", "plants stop growing after a week".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
from sci_phys import uniq
import sci_kids as K

U = Unit(61205)
R = U.R
P = People(R)

SEED = ["a sunflower", "a runner bean", "a pea plant", "cress", "an oak tree", "a horse chestnut tree", "an apple tree", "a tomato plant", "a pumpkin plant", "a poppy", "a carrot", "a lettuce", "a marigold"]
BULB = ["a daffodil", "a tulip", "an onion", "garlic", "a snowdrop", "a bluebell", "a hyacinth"]


def g_sb():
    k = R.random() < 0.55
    p = R.choice(SEED if k else BULB)
    if not once(("sb", p)):
        return None
    a = "a seed" if k else "a bulb"
    return item("Does %s usually grow from a seed or from a bulb?" % p, a, ["a bulb" if k else "a seed", "a stone", "a leaf"], "Sunflowers and beans grow from seeds; daffodils and onions grow from bulbs.")


GROW = [("an acorn", "an oak tree"), ("a conker", "a horse chestnut tree"), ("an apple pip", "an apple tree"), ("a sunflower seed", "a sunflower"),
        ("a broad bean seed", "a bean plant"), ("a daffodil bulb", "a daffodil"), ("a tulip bulb", "a tulip"), ("an onion set (a small bulb)", "an onion plant"),
        ("a sycamore seed", "a sycamore tree"), ("a pumpkin seed", "a pumpkin plant")]


def g_into():
    s, p = R.choice(GROW)
    if not once(("in", s)):
        return None
    return item("What does %s grow into?" % s, p, R.sample([x[1] for x in GROW if x[1] != p], 3), "A seed or bulb grows into the same kind of plant it came from.")


STAGE = ["a seed", "a root grows down", "a shoot grows up", "leaves open", "flowers grow", "pods with new seeds form"]


def g_order():
    i = R.randrange(len(STAGE) - 1)
    k = R.random() < 0.5
    if not once(("or", i, k)):
        return None
    if k:
        a = STAGE[i + 1]
        return item("A bean grows. What happens after %s?" % STAGE[i].replace("a seed", "planting a seed"), a, R.sample([x for x in STAGE if x not in (a, STAGE[i])], 3),
                    "Seed → root → shoot → leaves → flowers → new seeds.")
    a = STAGE[i]
    return item("A bean grows. What happens just before %s?" % STAGE[i + 1], a if a != "a seed" else "a seed is planted", R.sample([x for x in STAGE[1:] if x not in (a, STAGE[i + 1])], 3),
                "Seed → root → shoot → leaves → flowers → new seeds.")


WEEK = [0, 1, 2, 3, 4]


def g_table():
    who = P.next()[0]
    step = R.choice([[0, 2, 5, 9, 14], [0, 1, 4, 8, 12], [0, 3, 6, 10, 15], [0, 2, 4, 7, 11], [0, 1, 3, 6, 10],
                         [0, 2, 6, 11, 17], [0, 1, 5, 10, 16], [0, 3, 7, 12, 18]])
    k = R.choice(["read", "read", "most", "diff", "pattern"])
    ri = R.randrange(1, 5)
    if not once(("tb", tuple(step), k, ri if k == "read" else 0)) or (k == "pattern" and not once(("tp",), 2)):
        return None
    tab = table(["Week", "Height of the bean plant (cm)"], [[str(w), str(h)] for w, h in zip(WEEK, step)])
    intro = tab + "%s measured a bean plant every week. " % who
    if k == "read":
        g = "%d cm" % step[ri]
        return item(intro + "How tall was the plant in week %d?" % ri, g, uniq(g, ["%d cm" % x for x in step if x] + ["%d cm" % ri]), "Read across from week %d." % ri)
    if k == "most":
        d = [step[i + 1] - step[i] for i in range(4)]
        j = d.index(max(d))
        if d.count(max(d)) > 1:
            return None
        a = "between week %d and week %d" % (j, j + 1)
        return item(intro + "When did the plant grow the most?", a, ["between week %d and week %d" % (x, x + 1) for x in range(4) if x != j][:3], "Find the biggest jump.")
    if k == "diff":
        g = "%d cm" % (step[4] - step[2])
        return item(intro + "How much did it grow from week 2 to week 4?", g, uniq(g, ["%d cm" % step[4], "%d cm" % step[2], "2 cm", "%d cm" % (step[4] + step[2])]), "%d − %d." % (step[4], step[2]))
    return item(intro + "What do the results show?", "The plant got taller every week.", ["The plant got shorter.", "The plant stayed the same.", "The plant stopped growing after week 1."], "The numbers keep going up.")


B1 = bank([
    ("What grows out of a seed first?", "a root", ["a flower", "a leaf", "a fruit"], "The root grows down, then the shoot grows up."),
    ("What is a bulb?", "a store of food under the ground that a new plant grows from", ["a kind of seed", "a flower", "a light bulb for plants"], "Daffodils and onions grow from bulbs."),
    ("What does a seed need to start growing?", "water and warmth", ["darkness and salt", "only sunlight", "nothing"], "Seeds start in damp, warm soil."),
    ("What is a seedling?", "a young plant that has just grown from a seed", ["a seed in a packet", "a fully grown tree", "a flower bud"], "It has its first leaves."),
    ("Which way does a root grow?", "down into the soil", ["up to the sky", "sideways only", "it does not grow"], "Roots grow down."),
    ("Which way does a shoot grow?", "up towards the light", ["down into the soil", "into the bulb", "it does not grow"], "Shoots grow up."),
    ("When are daffodil bulbs usually planted in the UK?", "in autumn, so they flower in spring", ["in summer, to flower the next day", "only in winter snow", "never"], "They wait underground."),
    ("What do flowers make so that new plants can grow?", "seeds", ["bulbs only", "roots", "soil"], "The life cycle starts again."),
])
B3 = bank([
    ("What does a bean need to start growing?", "water and warmth", ["light and salt", "a dark fridge", "nothing at all"], "Germination."),
    ("Why do beans grow well in a sunny window once they have leaves?", "Leaves need light to make food.", ["Light makes roots grow up.", "Beans like cold glass.", "Sunlight waters them."], "Leaves need light."),
    ("Where do a bean plant's new seeds grow?", "in pods", ["in the roots", "in the soil", "on the leaves"], "Like the bean you planted."),
    ("What happens to the bean seed after the plant has grown leaves?", "It shrivels, because its stored food has been used.", ["It grows bigger.", "It turns into a flower.", "It becomes a root."], "Food used up."),
    ("Which part of a bean plant holds it in the soil?", "the roots", ["the flowers", "the pods", "the leaves"], "Roots anchor the plant."),
    ("How long does a bean take to show a shoot?", "about a week or two", ["one minute", "ten years", "it never grows"], "It needs time."),
    ("What is it called when a seed starts to grow?", "germination", ["pollination", "evaporation", "reflection"], "The seed wakes up."),
    ("Which is the right order?", "seed, seedling, young plant, flowering plant", ["flowering plant, seed, seedling, young plant", "young plant, seed, flowering plant, seedling", "seedling, seed, flowering plant, young plant"], "From small to grown."),
])
B5 = bank([
    ("A bean is planted upside down. Which way will its root grow?", "down, because roots always grow downwards", ["up, out of the soil", "it will not grow", "sideways for ever"], "Roots sense gravity."),
    ("Why can a bulb start to grow without leaves?", "It has food stored inside it.", ["It eats soil.", "It does not need food.", "It uses its flower."], "Stored food."),
    ("How could you see a bean's root growing?", "Grow it in a clear jar with damp paper towel.", ["Grow it in a closed metal tin.", "Bury it very deep.", "Keep it dry in a drawer."], "Observe closely."),
    ("Why do gardeners plant seeds at different times of year?", "Different seeds need different warmth to start growing.", ["Seeds can only be planted on Mondays.", "All seeds grow best in snow.", "It does not matter when."], "Suitable temperature."),
    ("How could you show a sunflower grows taller over time?", "Measure its height every week and record it in a table.", ["Look at it once.", "Guess its height.", "Measure a different plant each week."], "Measure and record."),
])


def body():
    pic = K.row(["seed", "sprout", "plant"], words=["seed", "seedling", "plant"], size=90, label="a seed grows into a seedling, then a plant")
    ex = [("What grows first from a bean?", ["Down into the soil"], "a root"),
          ("Daffodil: seed or bulb?", ["Planted in autumn"], "a bulb")]
    mist = ["Thinking the shoot grows before the root.", "Thinking a bulb is a kind of seed.", "Thinking an acorn grows into a conker tree."]
    return kid_lesson(pic, "Seeds and bulbs grow into plants.",
                      ["A root grows down, then a shoot grows up.", "Leaves open, flowers grow, then new seeds form.", "Bulbs, like daffodils, have food stored inside."], ex, mist)


def main():
    sets = U.sets([
        ("Seeds and bulbs", B1 + [(g_sb, 12)]),
        ("What will it grow into?", [(g_into, 10), (g_sb, 5), (g_order, 5)]),
        ("How a bean grows", B3 + [(g_order, 5), (g_table, 7)]),
        ("Measuring growth", [(g_table, 20)]),
        ("Thinking about growing", B5 + [(g_table, 13), (g_sb, 2)]),
    ])
    make_uk(2, "seeds-and-bulbs", 5, "Plants",
            "Observe and describe how seeds and bulbs grow into mature plants.",
            "Seeds and Bulbs",
            "Year 2 Science: Seeds and Bulbs Worksheets (How Plants Grow)",
            "Seeds and Bulbs",
            "Free Year 2 science worksheets on seeds and bulbs: which plants grow from each, what seeds grow into, how a bean grows and measuring plant growth. 100 questions with answers.",
            "Seeds and bulbs grow into plants.",
            "Root first, then shoot, leaves, flowers and new seeds.",
            body(),
            [("How does a seed grow into a plant?", "With water and warmth, a root grows down and a shoot grows up. Leaves open, the plant grows taller, flowers grow and new seeds form."),
             ("What is the difference between a seed and a bulb?", "A seed is small and grows from a flower. A bulb is bigger and stores food underground. Daffodils, tulips and onions grow from bulbs."),
             ("What grows first from a seed?", "The root grows first, downwards into the soil. Then a shoot grows up towards the light.")],
            sets)


if __name__ == "__main__":
    main()
