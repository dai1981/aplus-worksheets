# -*- coding: utf-8 -*-
"""
UK Year 3 science: Magnets Attract and Repel (Forces and magnets)
  python tools/gen_uk_science_y3_magnets_attract_and_repel.py
Magnets have two poles; like poles repel and unlike poles attract (predicting with bar-magnet pictures); magnetic
force acts at a distance and through some materials; comparing the strength of magnets (paperclip tests); and uses of
magnets such as compasses.
Wrong answers come from real mistakes: "N attracts N", "bigger magnets are always stronger", "magnets attract all
metals", "magnetic force only works when touching".
"""
from uk_sci import Unit, item, bank, lesson, make_uk, table, fig, People, once
from uk_sci_pics import magnets, _bar
from sci_common import svg_wrap
from sci_phys import uniq

U = Unit(61313)
R = U.R
P = People(R)

POLE = {"N": "north pole", "S": "south pole"}


def g_pic():
    a = R.choice([("N", "S"), ("S", "N")])
    b = R.choice([("N", "S"), ("S", "N")])
    k = R.choice(["what", "why", "which"])
    if not once(("pc", a, b, k)):
        return None
    l, r = a[1], b[0]
    att = l != r
    pic = fig(magnets(a, b, "two bar magnets: the left one %s to %s, the right one %s to %s" % (a[0], a[1], b[0], b[1])))
    if k == "what":
        ans = "They attract (pull together)." if att else "They repel (push apart)."
        return item(pic + "The two magnets are pushed towards each other. What happens?", ans,
                    ["They repel (push apart)." if att else "They attract (pull together).", "Nothing happens.", "They both lose their magnetism."],
                    "Unlike poles attract; like poles repel.")
    if k == "why":
        ans = ("A %s faces a %s, and unlike poles attract." % (POLE[l], POLE[r])) if att else ("Two %ss face each other, and like poles repel." % POLE[l])
        w = ["Two %ss face each other, and like poles repel." % POLE[l], "A %s faces a %s, and unlike poles attract." % (POLE[l], POLE["S" if l == "N" else "N"]),
             "Magnets only work when they touch.", "The bigger magnet always wins."]
        return item(pic + "Explain what happens when these magnets are brought together.", ans, [x for x in w if x != ans][:3], "Look at the two ends that face each other.")
    ans = "the %s of the left magnet and the %s of the right magnet" % (POLE[l], POLE[r])
    w = ["the %s of the left magnet and the %s of the right magnet" % (POLE[x], POLE[y]) for x in "NS" for y in "NS" if (x, y) != (l, r)]
    return item(pic + "Which two poles are facing each other?", ans, w, "Look at the letters on the two inside ends.")


def g_txt():
    x, y = R.choice("NS"), R.choice("NS")
    k = R.choice(["near", "end"])
    if k == "near":
        if not once(("tn", x, y)):
            return None
        att = x != y
        ans = "They attract." if att else "They repel."
        return item("The %s of one magnet is brought near the %s of another magnet. What happens?" % (POLE[x], POLE[y]), ans,
                    ["They repel." if att else "They attract.", "Nothing happens.", "Both magnets break."], "Like poles repel; unlike poles attract.")
    act = R.choice(["attracts", "repels"])
    if not once(("te", x, act)):
        return None
    ans = POLE["S" if x == "N" else "N"] if act == "attracts" else POLE[x]
    return item("The %s of a magnet %s one end of another magnet. Which pole is that end?" % (POLE[x], act), "a " + ans,
                ["a " + (POLE["S"] if ans == POLE["N"] else POLE["N"]), "the middle of the magnet", "it could be either pole"], "Like poles repel; unlike poles attract.")


def row3(bars):
    s = []
    for i, (l, r) in enumerate(bars):
        _bar(10 + i * 140, 20, l, r, s, w=100)
    return svg_wrap(400, 74, "".join(s), "three bar magnets in a row")


def g_three():
    bars = [R.choice([("N", "S"), ("S", "N")]) for _ in range(3)]
    pair = R.choice([(0, 1), (1, 2)])
    if not once(("th", tuple(bars), pair)):
        return None
    l, r = bars[pair[0]][1], bars[pair[1]][0]
    att = l != r
    ans = "They attract." if att else "They repel."
    nm = ["the left magnet", "the middle magnet", "the right magnet"]
    return item(fig(row3(bars)) + "Three magnets are pushed together in this order. What happens between %s and %s?" % (nm[pair[0]], nm[pair[1]]), ans,
                ["They repel." if att else "They attract.", "Nothing happens.", "They swap places."], "Look at the two ends that face each other: like poles repel, unlike poles attract.")


COL = ["red", "blue", "green", "yellow", "orange", "purple"]


def g_train():
    a, b = R.sample(COL, 2)
    x, y = R.choice("NS"), R.choice("NS")
    if not once(("tr", a, b)) or not once(("tx", x, y), 4):
        return None
    att = x != y
    ans = "Yes, they join, because unlike poles attract." if att else "No, they push apart, because like poles repel."
    return item("Two toy train carriages join with magnets. The back of the %s carriage has a %s. The front of the %s carriage has a %s. Will they join?" % (a, POLE[x], b, POLE[y]), ans,
                ["No, they push apart, because like poles repel." if att else "Yes, they join, because unlike poles attract.", "Yes, any two magnets always join.", "No, magnets cannot join trains."],
                "Unlike poles attract; like poles repel.")




def g_strength():
    who = P.next()[0]
    kinds = R.sample(["bar magnet", "horseshoe magnet", "ring magnet", "button magnet", "wand magnet", "cylinder magnet"], 4)
    v = R.sample(range(2, 15), 4)
    k = R.choice(["most", "least", "read", "diff", "fair", "size"])
    ri = R.randrange(4)
    if not once(("st", tuple(kinds), tuple(v), k)) or (k in ("fair", "size") and not once(("sk", k), 3)):
        return None
    tab = table(["Magnet", "Paperclips held in a chain"], [[m, str(x)] for m, x in zip(kinds, v)])
    intro = tab + "%s tested how many paperclips each magnet could hold in a chain. " % who
    if k == "most":
        a = kinds[v.index(max(v))]
        return item(intro + "Which magnet was the strongest?", "the " + a, ["the " + x for x in kinds if x != a], "It held the most paperclips.")
    if k == "least":
        a = kinds[v.index(min(v))]
        return item(intro + "Which magnet was the weakest?", "the " + a, ["the " + x for x in kinds if x != a], "It held the fewest paperclips.")
    if k == "read":
        g = str(v[ri])
        return item(intro + "How many paperclips did the %s hold?" % kinds[ri], g, uniq(g, [str(x) for x in v] + [str(v[ri] + 2)]), "Read the row.")
    if k == "diff":
        d = max(v) - min(v)
        g = str(d)
        return item(intro + "How many more paperclips did the strongest magnet hold than the weakest?", g, uniq(g, [str(max(v)), str(min(v)), str(max(v) + min(v)), str(d + 1)]),
                    "%d − %d = %d." % (max(v), min(v), d))
    if k == "fair":
        return item(intro + "What should %s keep the same for a fair test?" % who, "the same kind and size of paperclips", ["the magnet being tested", "the number of paperclips held", "nothing at all"],
                    "Only the magnet changes.")
    return item(intro + "Why did %s count paperclips?" % who, "to measure each magnet's strength with a number", ["to make the magnets stronger", "to see which paperclip was heaviest", "to change the poles"],
                "Numbers make results easy to compare.")


USE = [("a compass", "A magnetic needle turns to point north."), ("a fridge door", "Magnets in the seal keep the door shut."), ("a scrapyard crane", "A huge magnet lifts old cars."),
       ("a recycling centre", "Magnets separate steel cans from aluminium cans."), ("a cupboard door catch", "A small magnet holds the door closed."),
       ("a fishing game for toddlers", "Magnets on the rods pick up the fish.")]


def g_use():
    u, h = R.choice(USE)
    k = R.random() < 0.5
    if not once(("us", u, k)):
        return None
    if k:
        return item("How is a magnet used in %s?" % u, h, R.sample([x[1] for x in USE if x[1] != h], 3), "Magnets are useful in many everyday things.")
    return item("Where is a magnet used like this: %s" % h[0].lower() + h[1:], u, R.sample([x[0] for x in USE if x[0] != u], 3), "Magnets are useful in many everyday things.")


B1 = bank([
    ("What are the two ends of a magnet called?", "poles: a north pole and a south pole", ["tops and bottoms", "plus and minus", "heads and tails"], "N and S."),
    ("What happens when two north poles are pushed together?", "They repel (push apart).", ["They attract.", "Nothing.", "They stick for ever."], "Like poles repel."),
    ("What happens when a north pole and a south pole are brought together?", "They attract (pull together).", ["They repel.", "Nothing happens.", "They melt."], "Unlike poles attract."),
    ("Where is a bar magnet strongest?", "at its poles (the ends)", ["in the middle", "it is the same everywhere", "only on top"], "Paperclips cling to the ends."),
    ("Does a magnet have to touch a paperclip to pull it?", "No. Magnetic force can act at a distance.", ["Yes, always.", "Only on Tuesdays.", "Only if the paperclip is big."], "A non-contact force."),
    ("Can a magnet attract a paperclip through a sheet of paper?", "Yes. Magnetic force passes through paper.", ["No, paper blocks magnetism.", "Only wet paper.", "Only coloured paper."], "Try it!"),
    ("What does repel mean?", "push away", ["pull together", "stick to", "light up"], "Like poles repel."),
    ("What does attract mean?", "pull towards", ["push away", "break apart", "fall down"], "Unlike poles attract."),
])
B5 = bank([
    ("How could you find which end of an unlabelled magnet is north?", "Bring it near the north pole of a labelled magnet: the end that is repelled is north.", ["Look at its colour.", "Weigh it.", "Smell it."], "Use repulsion to test."),
    ("Why does a compass needle point north?", "The needle is a magnet and the Earth acts like a giant magnet.", ["The wind blows it.", "North is downhill.", "It is broken."], "The Earth's magnetism."),
    ("Ring magnets are put on a pencil and one floats above another. Why?", "Like poles face each other and repel.", ["They are glued.", "Unlike poles repel.", "Gravity is switched off."], "Floating magnets."),
    ("How could you test whether magnetism passes through water?", "Put a paperclip in a cup of water and move a magnet along the outside of the cup.", ["Throw the magnet in the sea.", "Freeze the magnet.", "Hold the magnet far from the cup."], "Test through materials."),
    ("A magnet is dropped many times and becomes weaker. Why should magnets be stored carefully?", "Knocks and heat can weaken them.", ["They grow stronger when dropped.", "They never change.", "They turn into plastic."], "Look after magnets."),
])


def body():
    think = ("<p><b>Magnets have a north pole and a south pole.</b></p>"
             "<ul><li>Like poles repel (N and N, S and S). Unlike poles attract (N and S).</li>"
             "<li>Magnetic force acts at a distance, even through paper or water.</li>"
             "<li>Test strength with paperclips; bigger magnets are not always stronger.</li></ul>")
    ex = [("N near N?", ["Like poles"], "repel"),
          ("S near N?", ["Unlike poles"], "attract")]
    mist = ["Thinking a north pole attracts a north pole.", "Thinking bigger magnets are always stronger.", "Thinking magnets must touch to work."]
    return lesson(think, ex, mist)


def main():
    sets = U.sets([
        ("Poles", B1 + [(g_txt, 6), (g_train, 6)]),
        ("Attract or repel?", [(g_pic, 8), (g_three, 8), (g_use, 4)]),
        ("Magnet strength", [(g_strength, 20)]),
        ("Using magnets", [(g_use, 8), (g_three, 6), (g_train, 6)]),
        ("Thinking about magnets", B5 + [(g_strength, 9), (g_pic, 4), (g_txt, 2)]),
    ])
    make_uk(3, "magnets-attract-and-repel", 13, "Forces and magnets",
            "Observe how magnets attract or repel each other and attract some materials and not others. Describe magnets as having two poles. "
            "Predict whether two magnets will attract or repel each other, depending on which poles are facing.",
            "Magnets Attract and Repel",
            "Year 3 Science: Magnets Worksheets (North and South Poles, Attract and Repel)",
            "Attract and Repel",
            "Free Year 3 science worksheets on magnets: north and south poles, attract and repel, predicting with bar magnets, magnet strength tests and uses of magnets. 100 questions with answers.",
            "Like poles repel; unlike poles attract.",
            "Magnetic force works at a distance.",
            body(),
            [("When do magnets attract or repel?", "Unlike poles (north and south) attract. Like poles (north and north, or south and south) repel."),
             ("Do magnets have to touch to work?", "No. Magnetic force is a non-contact force. It acts across a gap and even through paper, card or water."),
             ("How can you test which magnet is strongest?", "Count how many paperclips each magnet can hold in a chain, using the same paperclips each time. The one that holds the most is the strongest.")],
            sets)


if __name__ == "__main__":
    main()
