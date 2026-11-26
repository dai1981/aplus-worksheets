# -*- coding: utf-8 -*-
"""
UK Year 2 science: Microhabitats (Living things and their habitats)
  python tools/gen_uk_science_y2_microhabitats.py
Identify and name a variety of plants and animals in microhabitats: minibeasts under logs and stones, in leaf
litter, in soil, on leaves and flowers; what conditions they like (dark, damp, cool); a woodlouse choice chamber;
and counting minibeasts in a minibeast hunt (tally charts and tables). Caring for minibeasts.
Wrong answers come from real mistakes: "minibeasts like hot, dry places", "a microhabitat is a tiny animal",
"woodlice are insects", "all minibeasts live in the same place".
"""
from uk_sci import Unit, item, bank, kid_lesson, make_uk, table, People, once
import sci_kids as K
from sci_phys import uniq

U = Unit(61203)
R = U.R
P = People(R)

WHERE = [("a woodlouse", "under a log or a stone"), ("an earthworm", "in the soil"), ("a centipede", "under a log or a stone"), ("a slug", "under a log or a stone"),
         ("a snail", "under a log or a stone"), ("a spider", "in a web in a hedge"), ("a ladybird", "on the leaves of a plant"), ("a bee", "on a flower"),
         ("a caterpillar", "on the leaves of a plant"), ("a beetle", "in the leaf litter"), ("an ant", "in a nest under a paving slab"), ("a butterfly", "on a flower")]
PLACES = sorted({x[1] for x in WHERE})


def g_where():
    a, w = R.choice(WHERE)
    if not once(("wh", a)):
        return None
    damp = {"under a log or a stone", "in the leaf litter", "in the soil"}
    pool = [x for x in PLACES if x not in damp] if w in damp else sorted(damp) + ["in a nest under a paving slab"]
    pool = [x for x in pool if x != w]
    return item("Where are you most likely to find %s?" % a, w, R.sample(pool, 3), "Minibeasts live in the microhabitat that gives them what they need.")


COND = [("under a log", "dark, damp and cool"), ("in the soil", "dark and damp"), ("in leaf litter", "damp and shady"), ("on a sunny path", "bright, dry and warm"),
        ("on top of a wall in the sun", "bright, dry and warm")]


def g_cond():
    p, c = R.choice(COND)
    k = R.random() < 0.5
    if not once(("co", p, k)):
        return None
    if k:
        return item("What is it usually like %s?" % p, c, [x for x in ["dark, damp and cool", "bright, dry and warm", "dark and damp", "damp and shady", "hot and sandy"] if x != c][:3],
                    "Microhabitats each have their own conditions.")
    a = "fewer" if "bright" in c else "lots of"
    return item("Would you find %s woodlice %s?" % ("many" if a == "lots of" else "many", p), "Yes, they like dark, damp places." if a == "lots of" else "No, woodlice dry out in bright, warm places.",
                ["No, woodlice dry out in bright, warm places." if a == "lots of" else "Yes, they like dark, damp places.", "Woodlice live only in ponds.", "Woodlice live only in trees."],
                "Woodlice need damp places to stop them drying out.")


def g_chamber():
    who = P.next()[0]
    pair = R.choice([("dark side", "light side"), ("damp side", "dry side")])
    tot = R.choice([10, 12, 15, 20])
    good = R.randint(tot - 4, tot - 1)
    bad = tot - good
    k = R.choice(["more", "like", "read", "read", "why"])
    if not once(("ch", pair, tot, good, k)) or (k == "why" and not once(("cw",), 3)) or (k in ("like", "more") and not once(("cl", pair, k), 2)):
        return None
    tab = table(["Side of the tray", "Woodlice after 10 minutes"], [[pair[0], str(good)], [pair[1], str(bad)]])
    intro = tab + "%s put %d woodlice in a tray with a %s and a %s. " % (who, tot, pair[0], pair[1])
    if k == "more":
        return item(intro + "Which side had more woodlice?", "the " + pair[0], ["the " + pair[1], "Both sides had the same.", "The woodlice left the tray."], "%d is more than %d." % (good, bad))
    if k == "like":
        lk = pair[0].split()[0]
        return item(intro + "What do the results show woodlice like?", "%s places" % lk, ["%s places" % pair[1].split()[0], "hot, sunny places", "places with no air"], "Most went to the %s." % pair[0])
    if k == "read":
        g = str(bad)
        return item(intro + "How many woodlice were on the %s?" % pair[1], g, uniq(g, [str(good), str(tot), str(bad + 2), str(max(0, bad - 1))]), "Read the table.")
    if k == "total":
        g = str(tot)
        return item(intro + "How many woodlice are there altogether?", g, uniq(g, [str(good), str(bad), str(tot + 2), str(good - bad)]), "%d + %d = %d." % (good, bad, tot))
    return item(intro + "Why should %s put the woodlice back under their log afterwards?" % who, "so they are back in the habitat they need", ["so they can dry out", "so they can be lost", "it does not matter"],
                "Always care for living things.")


def g_hunt():
    who = P.next()[0]
    mb = R.sample(["woodlice", "worms", "spiders", "slugs", "beetles", "centipedes", "snails", "ants"], 4)
    v = R.sample(range(1, 13), 4)
    k = R.choice(["most", "least", "read", "sum"])
    ri, rj = R.sample(range(4), 2)
    if not once(("hu", tuple(mb), tuple(v), k)):
        return None
    tab = table(["Minibeast", "Number found"], [[m, str(x)] for m, x in zip(mb, v)])
    intro = tab + "%s went on a minibeast hunt in the school garden. " % who
    if k == "most":
        a = mb[v.index(max(v))]
        return item(intro + "Which minibeast did %s find most of?" % who, a, [x for x in mb if x != a], "The biggest number.")
    if k == "least":
        a = mb[v.index(min(v))]
        return item(intro + "Which minibeast did %s find fewest of?" % who, a, [x for x in mb if x != a], "The smallest number.")
    if k == "read":
        g = str(v[ri])
        return item(intro + "How many %s did %s find?" % (mb[ri], who), g, uniq(g, [str(x) for x in v] + [str(v[ri] + 1)]), "Read the table.")
    s = v[ri] + v[rj]
    g = str(s)
    return item(intro + "How many %s and %s were found altogether?" % (mb[ri], mb[rj]), g, uniq(g, [str(v[ri]), str(v[rj]), str(s + 1), str(abs(v[ri] - v[rj]))]), "%d + %d = %d." % (v[ri], v[rj], s))


B1 = bank([
    ("What is a microhabitat?", "a very small habitat, like the space under a log", ["a tiny animal", "a big forest", "a kind of plant"], "Micro means very small."),
    ("Which of these is a microhabitat?", "under a stone", ["the whole ocean", "a desert", "the Arctic"], "Very small places."),
    ("What are minibeasts?", "small animals such as insects, worms, snails and spiders", ["baby farm animals", "small plants", "tiny rocks"], "Mini means small."),
    ("Why do woodlice live under logs?", "It is dark and damp there, and they need damp to stop drying out.", ["They like hot sun.", "Logs are warm and dry.", "They eat logs only."], "Damp and dark."),
    ("How many legs does an insect have?", "six", ["eight", "four", "none"], "Ants, beetles and ladybirds are insects."),
    ("How many legs does a spider have?", "eight", ["six", "four", "ten"], "Spiders are not insects."),
    ("What do earthworms eat?", "dead leaves and bits of plants in the soil", ["other worms", "stones", "birds"], "They help make soil."),
    ("Which tool helps you look closely at a minibeast?", "a magnifying glass", ["a hammer", "a ruler", "a torch only"], "Look closely, do not touch roughly."),
])
B5 = bank([
    ("How should you treat minibeasts on a minibeast hunt?", "gently, and put them back where you found them", ["keep them in a jar for ever", "squash them", "take them home"], "Care for living things."),
    ("Why should you put a log back the way you found it?", "Minibeasts living under it need it as their home.", ["So it looks tidy.", "Logs are heavy.", "It does not matter."], "Protect microhabitats."),
    ("Why are there more minibeasts under a log than on a sunny path?", "Under the log it is dark, damp and has food.", ["The path is damp and dark.", "Minibeasts like hot paths.", "There are none under logs."], "Conditions matter."),
    ("How could you make a fair test of whether woodlice prefer dark or light?", "Put the same woodlice in a tray with one dark side and one light side, and count after the same time.", ["Use different trays at different times.", "Count only once without a tray.", "Use only one woodlouse."], "Fair test."),
    ("Is a woodlouse an insect?", "No. It has 14 legs, so it is not an insect.", ["Yes, it has six legs.", "Yes, it is a beetle.", "No, it is a worm."], "Count the legs."),
])


def body():
    pic = K.scene([("worm", 80, 130, 0.6), ("leaf", 200, 120, 0.6), ("bug", 300, 120, 0.6), ("rock", 140, 140, 0.55)], label="a garden with a worm, leaves, a ladybird and a stone")
    ex = [("Woodlice live where?", ["Dark and damp"], "under logs and stones"),
          ("A spider has how many legs?", ["Not an insect"], "eight")]
    mist = ["Thinking a microhabitat is a tiny animal.", "Thinking minibeasts like hot, dry places.", "Thinking woodlice are insects."]
    return kid_lesson(pic, "A microhabitat is a very small habitat.",
                      ["Under a log, in leaf litter or in the soil.", "Many minibeasts like dark, damp places.", "Look gently and put them back."], ex, mist)


def main():
    sets = U.sets([
        ("Tiny habitats", B1 + [(g_where, 12)]),
        ("Where do they live?", [(g_cond, 8), (g_hunt, 12)]),
        ("Minibeast hunt", [(g_hunt, 12), (g_cond, 2), (g_chamber, 6)]),
        ("Woodlouse test", [(g_chamber, 20)]),
        ("Caring for minibeasts", B5 + [(g_chamber, 8), (g_hunt, 7)]),
    ])
    make_uk(2, "microhabitats", 3, "Living things and their habitats",
            "Identify that most living things live in habitats to which they are suited and describe how different habitats provide for the basic needs of different kinds of animals and plants. "
            "Identify and name a variety of plants and animals in their habitats, including microhabitats.",
            "Microhabitats",
            "Year 2 Science: Microhabitats Worksheets (Minibeasts Under Logs and Stones)",
            "Microhabitats",
            "Free Year 2 science worksheets on microhabitats: minibeasts under logs and stones, in leaf litter and soil, the woodlouse test and a minibeast hunt. 100 questions with answers.",
            "A microhabitat is a tiny habitat.",
            "Many minibeasts like dark, damp places such as under a log.",
            body(),
            [("What is a microhabitat?", "A very small habitat, such as the space under a log or a stone, a pile of leaves, or a crack in a wall."),
             ("Why do woodlice like logs?", "Under a log it is dark, damp and cool, and there are rotting plants to eat. Woodlice dry out in hot, bright places."),
             ("How do I go on a minibeast hunt?", "Gently lift logs and stones, look with a magnifying glass, record what you find, and put everything back carefully.")],
            sets)


if __name__ == "__main__":
    main()
