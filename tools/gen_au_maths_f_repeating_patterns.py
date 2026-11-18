# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Repeating Patterns (Australian Curriculum v9.0, AC9MFA01)
  python3 tools/gen_au_maths_f_repeating_patterns.py
What comes next in AB patterns, then AAB, ABB and ABC patterns, finding the part that repeats, finding a
missing piece in the middle, and the same pattern shown in different ways (colours, shapes, sounds, actions).
Wrong answers come from real mistakes: repeating the last thing again, starting the pattern over from the
wrong place, choosing the right shape in the wrong colour, and naming only part of the repeating unit.
"""
import random
from k_pics import name
from f_common import Kids, mcq, finish, make, fig, figure, mistakes, pattern_svg

R = random.Random(99701)
SH = [("shape", "circle", "red"), ("shape", "square", "blue"), ("shape", "triangle", "yellow"), ("shape", "circle", "green"),
      ("shape", "square", "red"), ("shape", "triangle", "blue"), ("shape", "rectangle", "green"), ("shape", "circle", "yellow")]
OB = [("obj", "apple"), ("obj", "star"), ("obj", "duck"), ("obj", "ball"), ("obj", "fish"), ("obj", "flower"), ("obj", "heart"), ("obj", "cup")]


def nm(it):
    return "%s %s" % (it[2], it[1]) if it[0] == "shape" else name(it[1], 1)


def build_pattern(unit, n):
    return [unit[i % len(unit)] for i in range(n)]


def wrong_next(unit, n, pool):
    nxt = unit[n % len(unit)]
    out = [nm(x) for x in unit if x != nxt]
    out.append(nm(unit[(n - 1) % len(unit)]))
    if nxt[0] == "shape":
        out.append("%s %s" % ([c for c in ["red", "blue", "yellow", "green"] if c != nxt[2]][0], nxt[1]))
        out.append("%s %s" % (nxt[2], [k for k in ["circle", "square", "triangle"] if k != nxt[1]][0]))
    out += [nm(p) for p in pool if p not in unit]
    return out


# ------------------------------------------------------------ set 1: AB patterns
def set_ab(rnd):
    its = []
    seen = set()
    while len(its) < 20:
        pool = SH if len(its) % 2 == 0 else OB
        unit = rnd.sample(pool, 2)
        n = rnd.choice([4, 5, 6, 7])
        key = (tuple(unit), n)
        if key in seen:
            continue
        seen.add(key)
        items = build_pattern(unit, n)
        q = fig(pattern_svg(items, 1)) + "What comes next?"
        ans = nm(unit[n % 2])
        its.append(mcq(q, ans, wrong_next(unit, n, pool), "The pattern is %s, %s, again and again. The last one is %s, so next is <b>%s</b>." % (nm(unit[0]), nm(unit[1]), nm(items[-1]), ans)))
    return {"title": "What comes next? (AB)", "items": its}


# ------------------------------------------------------------ set 2: AAB, ABB, ABC
def set_harder(rnd):
    its = []
    seen = set()
    kinds = ["AAB", "ABB", "ABC", "AAB", "ABB", "ABC", "ABC", "AABB"]
    while len(its) < 20:
        kind = kinds[len(its) % len(kinds)]
        pool = SH if len(its) % 2 == 0 else OB
        a, b, c = rnd.sample(pool, 3)
        unit = {"AAB": [a, a, b], "ABB": [a, b, b], "ABC": [a, b, c], "AABB": [a, a, b, b]}[kind]
        n = rnd.choice([len(unit) * 2, len(unit) * 2 + 1, len(unit) * 2 + 2])
        if n > 9:
            n = len(unit) * 2
        key = (tuple(unit), n)
        if key in seen:
            continue
        seen.add(key)
        items = build_pattern(unit, n)
        q = fig(pattern_svg(items, 1)) + "What comes next?"
        ans = nm(unit[n % len(unit)])
        its.append(mcq(q, ans, wrong_next(unit, n, pool), "The part that repeats is %s. Say it again and again to find the next one: <b>%s</b>." % (", ".join(nm(x) for x in unit), ans)))
    return {"title": "What comes next? (AAB, ABB, ABC)", "items": its}


# ------------------------------------------------------------ set 3: the repeating part
def set_unit(rnd):
    its = []
    seen = set()
    kinds = ["AB", "AAB", "ABB", "ABC", "AB", "ABC"]
    while len(its) < 20:
        kind = kinds[len(its) % len(kinds)]
        pool = SH if len(its) % 2 else OB
        a, b, c = rnd.sample(pool, 3)
        unit = {"AB": [a, b], "AAB": [a, a, b], "ABB": [a, b, b], "ABC": [a, b, c]}[kind]
        key = tuple(unit)
        if key in seen:
            continue
        seen.add(key)
        items = build_pattern(unit, len(unit) * 3)
        q = fig(pattern_svg(items)) + "Start at the beginning. Which part repeats again and again?"
        ans = ", ".join(nm(x) for x in unit)
        rots = [unit[k:] + unit[:k] for k in range(len(unit))]
        raw = [unit[:1], unit[:2], unit + unit[:1], [unit[0], unit[0]], unit[::-1], [unit[1]], unit[:2] + unit[:1], [unit[-1], unit[-1]]]
        cands = [", ".join(nm(x) for x in c) for c in raw if c not in rots and len(c) > 0]
        its.append(mcq(q, ans, cands, "Find the part that comes again and again. It is <b>%s</b>, and it repeats 3 times." % ans))
    return {"title": "The part that repeats", "items": its}


# ------------------------------------------------------------ set 4: missing piece
def set_missing(rnd):
    its = []
    seen = set()
    kinds = ["AB", "AAB", "ABC", "ABB"]
    while len(its) < 20:
        kind = kinds[len(its) % len(kinds)]
        pool = SH if len(its) % 2 == 0 else OB
        a, b, c = rnd.sample(pool, 3)
        unit = {"AB": [a, b], "AAB": [a, a, b], "ABB": [a, b, b], "ABC": [a, b, c]}[kind]
        n = len(unit) * 3 if len(unit) == 2 else len(unit) * 2 + 1
        items = build_pattern(unit, n)
        pos = rnd.randrange(1, n - 1)
        key = (tuple(unit), pos)
        if key in seen:
            continue
        seen.add(key)
        ans = nm(items[pos])
        show = items[:pos] + [("blank",)] + items[pos + 1:]
        q = fig(pattern_svg(show)) + "Which one is missing?"
        its.append(mcq(q, ans, wrong_next(unit, pos, pool), "The part that repeats is %s. Say it along the row: the gap is <b>%s</b>." % (", ".join(nm(x) for x in unit), ans)))
    return {"title": "Find the missing piece", "items": its}


# ------------------------------------------------------------ set 5: patterns in different ways
def set_ways(rnd):
    K = Kids(rnd)
    its = []
    acts = [("clap", "stamp"), ("jump", "sit"), ("pat", "clap"), ("hop", "hop", "turn"), ("clap", "clap", "stamp"), ("touch your head", "touch your toes"),
            ("stamp", "clap", "click"), ("wave", "nod")]
    for i, unit in enumerate(acts):
        kid = K.next()
        n = len(unit) * 2 + (1 if i % 2 else 0)
        seq = [unit[j % len(unit)] for j in range(n)]
        ans = unit[n % len(unit)]
        q = "%s makes a pattern: %s, … What comes next?" % (kid["n"], ", ".join(seq))
        wr = [u for u in dict.fromkeys(unit) if u != ans] + [seq[-1], "sing", "stop"]
        its.append(mcq(q, ans, wr, "The part that repeats is %s. Next is <b>%s</b>." % (", ".join(unit), ans)))
    # same pattern, different look
    pairs = [(["red", "blue"] * 3, "AB"), (["circle", "circle", "square"] * 2, "AAB"), (["big", "small", "small"] * 2, "ABB"),
             (["apple", "pear"] * 3, "AB"), (["red", "red", "yellow"] * 2, "AAB"), (["clap", "stamp", "stamp"] * 2, "ABB"),
             (["cat", "dog", "bird"] * 2, "ABC"), (["up", "down"] * 3, "AB"), (["1", "2", "3"] * 2, "ABC"), (["star", "star", "moon"] * 2, "AAB"),
             (["hop", "jump", "jump"] * 2, "ABB"), (["tick", "tock"] * 3, "AB")]
    same = {"AB": "green, yellow, green, yellow, green, yellow", "AAB": "dog, dog, cat, dog, dog, cat", "ABB": "red, blue, blue, red, blue, blue",
            "ABC": "circle, square, triangle, circle, square, triangle"}
    for seq, kind in pairs:
        q = "Which pattern is made the same way as <b>%s</b>?" % ", ".join(seq)
        ans = same[kind]
        wr = [v for k, v in same.items() if k != kind]
        its.append(mcq(q, ans, wr, "Both are %s patterns: the parts repeat in the same way. <b>%s</b>." % (
            {"AB": "one, then another, again and again", "AAB": "two the same, then one different", "ABB": "one, then two the same", "ABC": "three different things"}[kind], ans)))
    return {"title": "Patterns in different ways", "items": its}


def body():
    a, b = ("shape", "circle", "red"), ("shape", "square", "blue")
    c = ("obj", "star")
    return (
        "<h2>What is a repeating pattern?</h2>"
        "<p>A repeating pattern has a part that comes <b>again and again</b>. Find that part, then say it over and over to keep going.</p>"
        + figure(pattern_svg([a, b, a, b, a, b]), "red circle, blue square: AB, AB, AB.")
        + "<h2>Longer parts</h2><p>Some patterns repeat 3 things: two the same then one different (AAB), or three different things (ABC).</p>"
        + figure(pattern_svg([a, a, c, a, a, c]), "red circle, red circle, star: AAB, AAB.")
        + "<h2>Different ways</h2><p>Patterns can be colours, shapes, sounds or actions: clap, stamp, clap, stamp is an AB pattern too.</p>"
        + mistakes([["Repeating the last thing again", "Say the pattern from the start"],
                    ["Right shape, wrong colour", "Check both the shape and the colour"],
                    ["Naming only part of the repeating part", "Find where the pattern starts again"]]))


FAQ = [("What patterns do Foundation students learn?",
        "Repeating patterns: they recognise, copy and continue patterns made with colours, shapes, objects, sounds and actions (AC9MFA01)."),
       ("What do AB, AAB and ABC mean?",
        "They describe the part that repeats. AB is two things taking turns (red, blue). AAB is two the same then one different. ABC is three different things."),
       ("Why are patterns important in maths?",
        "Spotting what repeats is the start of algebra. It also helps with counting by 2s, 5s and 10s and with days of the week."),
       ("How can I make patterns at home?",
        "Thread beads, line up toys, or clap and stamp a rhythm. Ask your child to say what comes next and which part repeats.")]


def build():
    sets = [set_ab(R), set_harder(R), set_unit(R), set_missing(R), set_ways(R)]
    finish(sets, R, max_num=10)
    make("repeating-patterns", 7, "AC9MFA01", "Algebra",
         "Repeating Patterns: What Comes Next?",
         "Foundation Repeating Patterns Worksheets: AB, AAB and ABC Patterns (Free, with Answers)",
         "Repeating patterns",
         "Recognise, copy and continue repeating patterns represented in different ways.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on repeating patterns, matched to the Australian Curriculum (AC9MFA01): what comes next, AB, AAB and ABC patterns, the part that repeats, missing pieces, sounds and actions. 100 picture questions with answers.",
         "A repeating pattern has a part that comes again and again.",
         "Find the part that repeats, then say it over and over to keep going.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
