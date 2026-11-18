# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Comparing Length, Mass, Capacity and Time (Australian Curriculum v9.0, AC9MFM01)
  python3 tools/gen_au_maths_f_comparing_length_mass_capacity.py
Longer and shorter (lined up at one end), taller and shorter, heavier and lighter on a pan balance, holds
more and holds less, and which events take a longer or shorter time.
Wrong answers come from real mistakes: comparing things that do not start at the same line, thinking the
higher side of a balance is heavier, thinking a taller container always holds more, and mixing up
'longest' with 'shortest'.
"""
import random
from k_pics import pencils_svg, towers_svg, balance_svg, name
from f_common import Kids, mcq, finish, make, fig, figure, mistakes, glasses_svg

R = random.Random(99801)
L4 = ["A", "B", "C", "D"]


def letter_q(svg, q, ans_i, n, e):
    ans = L4[ans_i]
    return mcq(fig(svg) + q, ans, [x for x in L4[:n] if x != ans] + ["They are all the same" if n > 2 else "They are the same", "We cannot tell"], e)


# ------------------------------------------------------------ set 1: longer and shorter
def set_length(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        n = rnd.choice([2, 3, 3, 4])
        ls = rnd.sample(range(3, 10), n)
        want = rnd.choice(["longest", "shortest"]) if n > 2 else rnd.choice(["longer", "shorter"])
        key = (tuple(ls), want)
        if key in seen:
            continue
        seen.add(key)
        i = ls.index(max(ls) if want in ("longest", "longer") else min(ls))
        trap = len(its) >= 14 and n >= 3
        offs = None
        if trap:
            offs = [0] * n
            j = ls.index(min(ls))
            offs[j] = max(ls) - min(ls) + 1          # the shortest pencil starts far to the right
            if want != "shortest":
                continue
        svg = pencils_svg(ls, offsets=offs)
        q = ("Which pencil is the <b>%s</b>?" if n > 2 else "Which pencil is <b>%s</b>?") % want
        e = ("Line them up at one end and look at the other end. Pencil <b>%s</b> is the %s." % (L4[i], want)) if not trap else \
            ("Pencil %s starts further along, but it is the smallest. Compare from the same starting line: <b>%s</b> is the shortest." % (L4[i], L4[i]))
        its.append(letter_q(svg, q, i, n, e))
    return {"title": "Longer and shorter", "items": its}


# ------------------------------------------------------------ set 2: taller and shorter
def set_height(rnd):
    its = []
    seen = set()
    while len(its) < 14:
        n = rnd.choice([2, 3, 4])
        hs = rnd.sample(range(2, 9), n)
        want = rnd.choice(["tallest", "shortest"]) if n > 2 else rnd.choice(["taller", "shorter"])
        key = (tuple(hs), want)
        if key in seen:
            continue
        seen.add(key)
        i = hs.index(max(hs) if want.startswith("tall") else min(hs))
        its.append(letter_q(towers_svg(hs), ("Which tower is the <b>%s</b>?" if n > 2 else "Which tower is <b>%s</b>?") % want, i, n,
                            "The towers stand on the same line. Tower <b>%s</b> is the %s (%d cubes)." % (L4[i], want, hs[i])))
    pairs = [("a giraffe", "a dog", "taller", 0), ("a cat", "a tree", "shorter", 0), ("a cup", "a door", "taller", 1),
             ("a baby", "a dad", "shorter", 0), ("a chair", "a house", "taller", 1), ("a horse", "a mouse", "shorter", 1)]
    for a, b, want, k in pairs:
        ans, other = (a, b) if k == 0 else (b, a)
        its.append(mcq("Which is usually <b>%s</b>: %s or %s?" % (want, a, b), ans.capitalize(), [other.capitalize(), "They are the same height", "We cannot tell"],
                       "Think of them standing side by side. <b>%s</b> is %s." % (ans.capitalize(), want)))
    return {"title": "Taller and shorter", "items": its}


# ------------------------------------------------------------ set 3: heavier and lighter
def set_mass(rnd):
    its = []
    plan = [("apple", 2, "ball", 1, "left"), ("duck", 1, "cup", 2, "right"), ("star", 3, "fish", 1, "left"), ("ball", 1, "apple", 1, "equal"),
            ("cup", 2, "flower", 2, "right"), ("fish", 2, "heart", 3, "left"), ("button", 3, "duck", 1, "right"), ("flower", 1, "star", 1, "equal"),
            ("heart", 2, "apple", 2, "left"), ("bug", 3, "ball", 2, "right"), ("apple", 1, "fish", 3, "right"), ("duck", 2, "button", 2, "equal")]
    for i, (ka, na, kb, nb, tilt) in enumerate(plan):
        A, B = "the " + name(ka, na), "the " + name(kb, nb)
        vA, vB = ("is" if na == 1 else "are"), ("is" if nb == 1 else "are")
        svg = balance_svg((ka, na), (kb, nb), tilt)
        if tilt == "equal":
            q = fig(svg) + "What does the balance show?"
            ans = "Both sides have the same mass"
            wr = ["%s %s heavier" % (A.capitalize(), vA), "%s %s heavier" % (B.capitalize(), vB), "%s %s lighter" % (A.capitalize(), vA)]
            e = "The balance is level, so both sides have <b>the same mass</b>."
        else:
            heavy, light = (A, B) if tilt == "left" else (B, A)
            if i % 2 == 0:
                q = fig(svg) + "Which side is <b>heavier</b>?"
                ans = heavy.capitalize()
                wr = [light.capitalize(), "Both sides have the same mass", "We cannot tell"]
                e = "The heavier side goes <b>down</b>. That side has <b>%s</b>." % heavy
            else:
                q = fig(svg) + "Which side is <b>lighter</b>?"
                ans = light.capitalize()
                wr = [heavy.capitalize(), "Both sides have the same mass", "We cannot tell"]
                e = "The lighter side goes <b>up</b>. That side has <b>%s</b>." % light
        its.append(mcq(q, ans, wr, e))
    things = [("a watermelon", "a grape", "heavier"), ("a feather", "a brick", "lighter"), ("a car", "a bike", "heavier"), ("a leaf", "a school bag", "lighter"),
              ("an elephant", "a dog", "heavier"), ("a pencil", "a book", "lighter"), ("a pumpkin", "a peanut", "heavier"), ("a balloon", "a ball of clay", "lighter")]
    for a, b, want in things:
        ans = a
        its.append(mcq("Which is usually <b>%s</b>: %s or %s?" % (want, a, b), ans.capitalize(), [b.capitalize(), "They are the same mass", "We cannot tell"],
                       "Think of holding one in each hand. <b>%s</b> is %s." % (ans.capitalize(), want)))
    o = its
    return {"title": "Heavier and lighter", "items": [o[0], o[12], o[1], o[13], o[2], o[14], o[3], o[15], o[4], o[16], o[5], o[17], o[6], o[18], o[7], o[19], o[8], o[9], o[10], o[11]]}


# ------------------------------------------------------------ set 4: holds more, holds less
def set_capacity(rnd):
    its = []
    seen = set()
    while len(its) < 10:
        n = rnd.choice([2, 3, 4])
        levs = rnd.sample([0.2, 0.35, 0.5, 0.65, 0.8, 0.95], n)
        want = rnd.choice(["most", "least"])
        key = (tuple(levs), want)
        if key in seen:
            continue
        seen.add(key)
        i = levs.index(max(levs) if want == "most" else min(levs))
        svg = glasses_svg([(46, 80, l) for l in levs])
        its.append(letter_q(svg, "The glasses are the same size. Which glass has the <b>%s</b> water?" % want, i, n,
                            "Same size glasses: the higher the water, the more water. Glass <b>%s</b> has the %s." % (L4[i], want)))
    shapes = [[(40, 90, 0), (90, 60, 0)], [(70, 70, 0), (40, 50, 0)], [(36, 100, 0), (100, 80, 0), (60, 60, 0)], [(50, 50, 0), (90, 90, 0)],
              [(90, 40, 0), (40, 40, 0)], [(60, 100, 0), (60, 60, 0), (60, 80, 0)], [(30, 90, 0), (110, 70, 0)], [(80, 60, 0), (80, 90, 0), (50, 40, 0)],
              [(100, 50, 0), (40, 60, 0)], [(46, 46, 0), (70, 90, 0), (90, 30, 0)]]
    for j, items in enumerate(shapes):
        vols = [w * w * h for w, h, _ in items]          # round containers: width x width x height
        want = "most" if j % 2 == 0 else "least"
        i = vols.index(max(vols) if want == "most" else min(vols))
        tallest = max(range(len(items)), key=lambda k: items[k][1])
        e = "Think about how much space is inside: both how wide and how tall. Container <b>%s</b> holds the %s." % (L4[i], want)
        if want == "most" and tallest != i:
            e += " The tallest one is thin, so it holds less."
        its.append(letter_q(glasses_svg(items), "These containers are round, like cups. Which one holds the <b>%s</b>?" % want, i, len(items), e))
    o = its
    return {"title": "Holds more, holds less", "items": [x for pair in zip(o[:10], o[10:]) for x in pair]}


# ------------------------------------------------------------ set 5: how long does it take?
def set_time(rnd):
    K = Kids(rnd)
    its = []
    pairs = [("brushing your teeth", "a night's sleep"), ("eating an apple", "blinking"), ("a school day", "tying your shoes"), ("clapping once", "watching a movie"),
             ("a holiday at the beach", "washing your hands"), ("sneezing", "eating lunch"), ("walking to the letterbox", "flying to another country"),
             ("a birthday party", "drinking a glass of water"), ("reading a picture book", "snapping your fingers"), ("growing a tree", "growing a bean sprout")]
    longer = {0: 1, 1: 0, 2: 0, 3: 1, 4: 0, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0}
    for i, (a, b) in enumerate(pairs):
        L = [a, b][longer[i]]
        S = [a, b][1 - longer[i]]
        if i % 2 == 0:
            q = "Which takes a <b>longer</b> time: %s or %s?" % (a, b)
            ans, oth = L, S
            e = "<b>%s</b> takes longer than %s." % (L.capitalize(), S)
        else:
            q = "Which takes a <b>shorter</b> time: %s or %s?" % (a, b)
            ans, oth = S, L
            e = "<b>%s</b> is quicker than %s." % (S.capitalize(), L)
        its.append(mcq(q, ans.capitalize(), [oth.capitalize(), "They take the same time", "We cannot tell"], e))
    races = [(8, 5), (4, 9), (6, 3), (7, 10), (5, 2), (3, 6), (9, 4), (2, 7), (10, 8), (6, 9)]
    for a, b in races:
        k1, k2 = K.next(), K.next()
        while k2["n"] == k1["n"]:
            k2 = K.next()
        q = "%s and %s run a race. %s counts %d claps to finish. %s counts %d claps. Who took <b>less time</b>?" % (k1["n"], k2["n"], k1["n"], a, k2["n"], b)
        w = k1["n"] if a < b else k2["n"]
        l = k2["n"] if a < b else k1["n"]
        its.append(mcq(q, w, [l, "They took the same time", "We cannot tell"], "Fewer claps means less time. %d claps is less than %d, so <b>%s</b> was quicker." % (min(a, b), max(a, b), w)))
    o = its
    return {"title": "Longer and shorter time", "items": [x for pair in zip(o[:10], o[10:]) for x in pair]}


def body():
    return (
        "<h2>Line them up</h2>"
        "<p>To compare length, line things up at <b>one end</b>, then look at the other end. The one that sticks out is <b>longer</b>.</p>"
        + figure(pencils_svg([7, 4, 5]), "Pencil A is the longest. Pencil B is the shortest.")
        + "<h2>Heavier and lighter</h2><p>On a pan balance, the <b>heavier</b> side goes <b>down</b>. The lighter side goes up. Level means the same mass.</p>"
        + figure(balance_svg(("apple", 2), ("ball", 1), "left"), "The apples are heavier.")
        + "<h2>Holds more</h2><p>For the same size glasses, the higher water is more. For different containers, think about how wide and how tall they are.</p>"
        + figure(glasses_svg([(46, 80, 0.3), (46, 80, 0.8)]), "Glass B has more water.")
        + "<h2>Longer time</h2><p>Some things take a long time (a night's sleep). Some take a short time (a clap).</p>"
        + mistakes([["Comparing things that do not start at the same line", "Line them up at one end first"],
                    ["Thinking the higher side of the balance is heavier", "Heavy goes down"],
                    ["Thinking a taller container always holds more", "Check how wide it is too"]]))


FAQ = [("What measuring do Foundation students learn?",
        "They compare objects and events directly: longer or shorter, heavier or lighter, holds more or less, and takes more or less time (AC9MFM01). They do not use rulers or units yet."),
       ("What is a direct comparison?",
        "Putting two things side by side, on a balance or one inside the other to see which is longer, heavier or holds more, without measuring with numbers."),
       ("Why does my child think a tall, thin glass holds more?",
        "Young children notice height first. Pour water from one container to the other to show which really holds more."),
       ("How can I practise at home?",
        "Compare shoes, spoons and toys by length; hold two fruits to feel which is heavier; pour water between cups in the bath.")]


def build():
    sets = [set_length(R), set_height(R), set_mass(R), set_capacity(R), set_time(R)]
    finish(sets, R, max_num=10)
    make("comparing-length-mass-and-capacity", 8, "AC9MFM01", "Measurement",
         "Comparing Length, Mass, Capacity and Time",
         "Foundation Measurement Worksheets: Longer, Heavier, Holds More, Takes Longer (Free, with Answers)",
         "Comparing and measuring",
         "Identify and compare attributes of objects and events, including length, capacity, mass and duration, using direct comparisons and communicating reasoning.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on comparing length, mass, capacity and time, matched to the Australian Curriculum (AC9MFM01): longer and shorter, heavier and lighter, holds more, takes longer. 100 picture questions with answers.",
         "Compare directly: line things up, use a balance, or pour.",
         "Heavy goes down on a balance. Line up at one end to compare length.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
