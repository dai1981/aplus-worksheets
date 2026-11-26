# -*- coding: utf-8 -*-
"""
UK Year 1 science: Garden and Wild Plants (Plants)
  python tools/gen_uk_science_y1_garden_and_wild_plants.py
Identify and name a variety of common wild and garden plants: wild flowers and weeds, garden flowers, describing
plants by their flowers and leaves, plants that sting or are poisonous, and counting plants found on a plant hunt.
Wrong answers come from real mistakes: "all flowers are planted by people", "dandelions are garden flowers",
"it is safe to eat any berry", "a weed is not a plant".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, bar_chart, fig, People, once
import sci_kids as K

U = Unit(61101)
R = U.R
P = People(R)

WILD = ["a daisy", "a dandelion", "a buttercup", "clover", "a stinging nettle", "a thistle", "cow parsley", "a wild poppy"]
GARD = ["a rose", "a sunflower", "a tulip", "a pansy", "lavender", "a sweet pea", "a geranium", "a marigold"]


def g_wild():
    k = R.random() < 0.5
    pool, other = (WILD, GARD) if k else (GARD, WILD)
    a = R.choice(pool)
    if not once(("wg", a)):
        return None
    w = R.sample(other, 3)
    o = sorted([a] + w)
    q = "Which of these is a wild plant" if k else "Which of these is usually planted in a garden"
    return item("%s: %s or %s?" % (q, ", ".join(o[:3]), o[3]), a, w, "Wild plants grow by themselves. Garden plants are usually planted by people.")


DESC = [("a small flower with white petals and a yellow middle", "a daisy"), ("a yellow flower that turns into a fluffy seed head", "a dandelion"),
        ("a shiny yellow flower shaped like a little cup", "a buttercup"), ("a plant with leaves that sting if you touch them", "a stinging nettle"),
        ("a prickly plant with a purple flower", "a thistle"), ("a very tall plant with a huge yellow flower", "a sunflower"),
        ("a flower with a sweet smell and thorns on its stem", "a rose"), ("a bright red flower often seen in fields", "a wild poppy"),
        ("a small plant with leaves in three round parts", "clover"), ("a plant with purple flowers that smell lovely", "lavender"),
        ("a plant with blue, bell-shaped flowers in woods in spring", "a bluebell"), ("a cup-shaped spring flower, often red or yellow, that grows from a bulb", "a tulip")]


def g_desc():
    d, a = R.choice(DESC)
    if not once(("de", a)):
        return None
    return item("Which plant is %s?" % d, a, R.sample([x[1] for x in DESC if x[1] != a], 3), "Look at the flowers and leaves to name a plant.")


SAFE = [("Which plant can sting your skin?", "a stinging nettle", ["a daisy", "a buttercup", "clover"]),
        ("What should you do if you find berries on a bush?", "Do not eat them, because some are poisonous.", ["Eat them all.", "Give them to a friend to eat.", "Taste one to check."]),
        ("Which leaf can help soothe a nettle sting?", "a dock leaf", ["a holly leaf", "a thistle leaf", "a rose leaf"]),
        ("Why should you wash your hands after touching plants on a nature walk?", "Some plants can irritate skin or are poisonous.", ["Plants make your hands grow.", "Plants are sticky only.", "There is no reason."]),
        ("Is it all right to pick lots of wild flowers?", "No. Leave them for insects and for others to enjoy.", ["Yes, pick them all.", "Yes, pull up the roots.", "Only bluebells."]),
        ("Which plant has prickles that can hurt your hands?", "a thistle", ["a daisy", "clover", "a tulip"])]


def g_safe():
    q, a, w = R.choice(SAFE)
    if not once(("sa", q)):
        return None
    return item(q, a, w, "Look at plants, but take care and do not eat them.")


FIELD = ["daisies", "dandelions", "buttercups", "clover", "thistles"]


def g_hunt():
    who = P.next()[0]
    f = R.sample(FIELD, 4)
    v = R.sample(range(1, 11), 4)
    k = R.choice(["most", "fewest", "read"])
    ri = R.randrange(4)
    if not once(("hu", tuple(f), tuple(v), k)):
        return None
    ch = bar_chart(f, v, "", "bar chart of wild flowers %s found on the school field" % who, ymax=10, step=2, w=340, title="Flowers found")
    intro = fig(ch) + "%s went on a plant hunt on the school field. " % who
    if k == "most":
        a = f[v.index(max(v))]
        return item(intro + "Which flower did %s find most of?" % who, a, [x for x in f if x != a], "The tallest bar.")
    if k == "fewest":
        a = f[v.index(min(v))]
        return item(intro + "Which flower did %s find fewest of?" % who, a, [x for x in f if x != a], "The shortest bar.")
    g = str(v[ri])
    return item(intro + "How many %s did %s find?" % (f[ri], who), g, [str(x) for x in v if x != v[ri]][:3], "Read the top of the bar.")


B1 = bank([
    ("What is a wild plant?", "a plant that grows by itself", ["a plant that people plant", "a plant made of plastic", "a plant in a shop"], "Daisies and dandelions."),
    ("What is a garden plant?", "a plant that people usually plant and look after", ["a plant that grows anywhere by itself", "a kind of tree only", "a weed"], "Roses and sunflowers."),
    ("What is a weed?", "a wild plant growing where people do not want it", ["a plant made of paper", "a garden flower", "a kind of tree"], "Dandelions in a lawn."),
    ("Which plant has a flower that becomes a 'clock' of fluffy seeds?", "a dandelion", ["a rose", "a tulip", "a daisy"], "Blow the seeds away."),
    ("Which flower has white petals and a yellow middle?", "a daisy", ["a poppy", "a buttercup", "a thistle"], "Common on lawns."),
    ("Where would you find bluebells in spring?", "in woods", ["in the sea", "in the desert", "on a roof"], "Carpets of blue."),
    ("Is grass a plant?", "Yes.", ["No, it is a rock.", "No, it is an animal.", "Only when it is long."], "Grass is a wild plant."),
    ("Which garden flower grows very tall and follows the sun when young?", "a sunflower", ["a daisy", "clover", "a buttercup"], "Huge yellow flowers."),
])
B4 = bank([
    ("Which plant often grows in cracks in the pavement?", "a dandelion", ["a sunflower", "a rose", "a tulip"], "Wild plants grow almost anywhere."),
    ("Which plant is often grown for its nice smell?", "lavender", ["a stinging nettle", "a thistle", "grass"], "Gardeners grow it."),
    ("Which red flower is worn to remember people in November?", "a poppy", ["a daisy", "a dandelion", "a bluebell"], "Remembrance."),
    ("Which part of a plant is often colourful to attract insects?", "the flower", ["the root", "the stem", "the seed"], "Petals."),
    ("Which plant has leaves in three round parts?", "clover", ["a rose", "a tulip", "a sunflower"], "Look closely at the leaves."),
    ("Which of these is a garden vegetable plant?", "a runner bean", ["a stinging nettle", "a thistle", "a dandelion"], "Grown to eat."),
    ("Where do garden plants often come from?", "seeds, bulbs or young plants bought or saved by people", ["they appear from nowhere", "they fall from clouds", "they are made of plastic"], "People plant them."),
    ("Can a plant be both wild and grown in gardens?", "Yes, some wild flowers like poppies are also planted in gardens.", ["No, never.", "Only trees.", "Only weeds."], "Some are both."),
])
B5 = bank([
    ("Why do bees like wild flowers?", "They get nectar and pollen from them.", ["Wild flowers are cold.", "Bees eat the leaves.", "Bees do not visit flowers."], "Food for insects."),
    ("How could you find out which wild flower is most common on the field?", "Count each kind of flower and record it in a tally chart.", ["Guess.", "Pick all the flowers.", "Look for one second."], "Count and record."),
    ("Why might a gardener pull up dandelions?", "They are weeds growing where the gardener does not want them.", ["They are poisonous to touch.", "They are not plants.", "They grow too slowly."], "Weeds."),
    ("Why should you not eat plants you find on a walk?", "Some plants are poisonous.", ["All plants taste bad.", "Plants are too big.", "Plants are not food ever."], "Stay safe."),
    ("How could you remember the plants you saw on a walk?", "Take photos or draw them and write their names.", ["Pull them all up.", "Forget them.", "Eat them."], "Record what you see."),
])


def body():
    pic = K.row(["flower", "plant", "tree"], words=["daisy", "dandelion", "oak tree"], size=90, label="a daisy, a dandelion and an oak tree")
    ex = [("A dandelion: wild or garden?", ["It grows by itself"], "wild"),
          ("Which plant stings?", ["Leaves with tiny hairs"], "a stinging nettle")]
    mist = ["Thinking all flowers are planted by people.", "Thinking a weed is not a plant.", "Thinking it is safe to eat any berry."]
    return kid_lesson(pic, "Some plants are wild. Some grow in gardens.",
                      ["Wild plants grow by themselves, like daisies and dandelions.", "Garden plants are planted by people, like roses.", "Look, but do not eat wild plants."], ex, mist)


def main():
    sets = U.sets([
        ("Wild or garden?", B1 + [(g_wild, 12)]),
        ("Name the plant", [(g_desc, 12), (g_wild, 4), (g_safe, 4)]),
        ("Plant hunt", [(g_hunt, 20)]),
        ("Plants around us", B4 + [(g_safe, 2), (g_hunt, 10)]),
        ("Thinking about plants", B5 + [(g_hunt, 15)]),
    ])
    make_uk(1, "garden-and-wild-plants", 1, "Plants",
            "Identify and name a variety of common wild and garden plants, including deciduous and evergreen trees.",
            "Garden and Wild Plants",
            "Year 1 Science: Garden and Wild Plants Worksheets (Naming Plants)",
            "Garden and Wild Plants",
            "Free Year 1 science worksheets on garden and wild plants: naming common flowers and weeds, plants that sting, and a plant hunt with a bar chart. 100 questions with answers.",
            "Wild plants grow by themselves.",
            "Garden plants are planted by people. Look, but do not eat wild plants.",
            body(),
            [("What is the difference between wild and garden plants?", "Wild plants grow by themselves, like daisies and dandelions. Garden plants are usually planted by people, like roses and sunflowers."),
             ("Which common wild plants should Year 1 know?", "Daisies, dandelions, buttercups, clover, stinging nettles, thistles and poppies."),
             ("Is it safe to touch wild plants?", "Look carefully. Stinging nettles sting and some berries are poisonous, so never eat wild plants and wash your hands afterwards.")],
            sets)


if __name__ == "__main__":
    main()
