# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Subitising to 5 (Australian Curriculum v9.0, AC9MFN02)
  python3 tools/gen_au_maths_f_subitising.py
See how many at a glance (without counting one by one): dot cubes, ten-frames, small scattered groups,
two small parts that make a whole, and finding the group that shows a number.
Wrong answers come from real mistakes: one more or one less after a rushed look, seeing 5 as 4 when it is
spread out, and counting only one of the two parts.
"""
import random
from k_pics import dice_svg, tenframe_svg, scatter_svg, lettered_groups_svg, two_groups_svg, row_svg, name, KINDS
from f_common import Kids, mcq, finish, make, fig, figure, mistakes

R = random.Random(99201)
LOOK = "Look quickly. "


def near(n):
    return [n + 1, n - 1, n + 2, n - 2, n + 3]


# ------------------------------------------------------------ set 1: dot cubes
def set_dice(rnd):
    K = Kids(rnd)
    combos = [(n, p) for p in range(4) for n in [1, 2, 3, 4, 5]]
    order = [0, 6, 12, 18, 4, 1, 7, 13, 19, 10, 2, 8, 14, 15, 11, 3, 9, 5, 16, 17]
    its = []
    for idx in order:
        n, p = combos[idx]
        if p == 0:
            q = fig(dice_svg([n])) + LOOK + "How many dots?"
        elif p == 1:
            q = fig(dice_svg([n])) + "Which number does the dot cube show?"
        elif p == 2:
            k = K.next()
            q = fig(dice_svg([n])) + "%s rolls the dot cube. What number did %s roll?" % (k["n"], k["he"])
        else:
            q = fig(dice_svg([n])) + "How many dots are on this dot cube?"
        shape_tip = {1: "one dot in the middle", 2: "two dots on a slant", 3: "three dots in a line", 4: "four dots, one in each corner",
                     5: "four corners and one in the middle"}[n]
        its.append(mcq(q, n, near(n), "The pattern is %s. You can see <b>%d</b> without counting." % (shape_tip, n)))
    return {"title": "Dot cubes", "items": its}


# ------------------------------------------------------------ set 2: ten-frames
def set_frames(rnd):
    its = []
    kinds = ["dot"] * 5 + ["apple", "star", "ball", "heart", "flower", "duck", "fish", "cup", "bug", "button"] + ["dot"] * 5
    nums = [1, 2, 3, 4, 5, 3, 1, 4, 2, 5, 4, 2, 5, 1, 3, 2, 4, 1, 5, 3]
    for i in range(20):
        n = nums[i]
        k = kinds[i]
        q = fig(tenframe_svg(n, kind=k)) + ("How many %s are in the ten-frame?" % name(k) if k != "dot" else LOOK + "How many dots are in the ten-frame?")
        if i >= 15:
            q = fig(tenframe_svg(n, kind=k)) + "How many empty boxes are in the top row?"
            ans = 5 - n
            if ans == 0:
                its.append(mcq(q, 0, [1, 5, 4], "The top row has 5 boxes and all 5 are full. There are <b>0</b> empty boxes.", allow_zero=True))
            else:
                its.append(mcq(q, ans, [n, 5, ans + 1, ans - 1], "The top row has 5 boxes. %d %s full, so <b>%d</b> %s empty." % (n, "is" if n == 1 else "are", ans, "is" if ans == 1 else "are"), allow_zero=True))
            continue
        e = "The top row of a ten-frame holds 5. %s" % ("The whole top row is full: <b>5</b>." if n == 5 else "%d of the 5 boxes %s full: <b>%d</b>." % (n, "is" if n == 1 else "are", n))
        its.append(mcq(q, n, near(n), e))
    seen = set()
    for it in its:
        assert it["q"] + "".join(sorted(it["c"])) not in seen
        seen.add(it["q"] + "".join(sorted(it["c"])))
    return {"title": "Ten-frames", "items": its}


# ------------------------------------------------------------ set 3: small groups
def set_groups(rnd):
    its = []
    plan = [(2, "apple"), (4, "star"), (3, "duck"), (5, "ball"), (1, "fish"), (3, "flower"), (5, "heart"), (4, "cup"),
            (2, "bug"), (5, "button"), (4, "apple"), (3, "star"), (1, "duck"), (5, "fish"), (2, "flower"), (4, "bug"),
            (3, "ball"), (5, "cup"), (2, "heart"), (4, "button")]
    for i, (n, k) in enumerate(plan):
        svg = scatter_svg(n, k, 900 + i) if i % 3 else row_svg(n, k)
        q = fig(svg) + LOOK + "How many %s?" % name(k)
        e = "Small groups up to 5 can be seen all at once. There %s <b>%d</b> %s." % ("is" if n == 1 else "are", n, name(k, n))
        its.append(mcq(q, n, near(n), e))
    return {"title": "Small groups", "items": its}


# ------------------------------------------------------------ set 4: two parts
def set_parts(rnd):
    its = []
    pairs = [(1, 1), (2, 1), (1, 3), (2, 2), (3, 2), (1, 4), (2, 3), (4, 1), (3, 1), (1, 2)]
    for i, (a, b) in enumerate(pairs):
        q = fig(dice_svg([a, b])) + "How many dots on the two dot cubes altogether?"
        t = a + b
        its.append(mcq(q, t, [a, b, t + 1, t - 1, t + 2], "See %d and %d. Together that is <b>%d</b>." % (a, b, t)))
    kinds = ["apple", "star", "duck", "ball", "flower", "heart", "fish", "cup", "bug", "button"]
    for i, (a, b) in enumerate([(2, 2), (3, 1), (1, 4), (2, 3), (3, 2), (4, 1), (1, 2), (2, 1), (1, 3), (1, 1)]):
        k = kinds[i]
        q = fig(two_groups_svg(a, k, b, k, "and")) + "How many %s altogether?" % name(k)
        t = a + b
        its.append(mcq(q, t, [a, b, t + 1, t - 1, t + 2], "See %d and %d. %d and %d make <b>%d</b>." % (a, b, a, b, t)))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14], o[5], o[15], o[6], o[16], o[7], o[17], o[8], o[18], o[9], o[19]]
    return {"title": "Two parts at a glance", "items": order}


# ------------------------------------------------------------ set 5: find the group
def set_find(rnd):
    K = Kids(rnd)
    its = []
    kinds = KINDS
    for i in range(20):
        k = kinds[i % len(kinds)]
        target = [3, 4, 2, 5, 1][i % 5]
        others = [v for v in [1, 2, 3, 4, 5] if v != target]
        rnd.shuffle(others)
        vals = others[:3] + [target]
        rnd.shuffle(vals)
        letter = "ABCD"[vals.index(target)]
        if i < 12:
            q = fig(lettered_groups_svg([(v, k) for v in vals])) + "Which box has <b>%d</b> %s?" % (target, name(k, target))
            e = "Box %s has %d %s. You can see it without counting." % (letter, target, name(k, target))
            its.append(mcq(q, "Box " + letter, ["Box " + x for x in "ABCD" if x != letter], e))
        else:
            kid = K.next()
            q = fig(lettered_groups_svg([(v, k) for v in vals])) + "%s rolls a %d on a dot cube. Which box has the same number of %s?" % (kid["n"], target, name(k))
            e = "%d dots and %d %s are the same number. That is box <b>%s</b>." % (target, target, name(k, target), letter)
            its.append(mcq(q, "Box " + letter, ["Box " + x for x in "ABCD" if x != letter], e))
    return {"title": "Find the group", "items": its}


def body():
    return (
        "<h2>See it without counting</h2>"
        "<p><b>Subitising</b> means looking at a small group and knowing how many straight away, without counting one by one. "
        "Children learn to do this for groups up to 5.</p>"
        + figure(dice_svg([3, 4, 5]), "Dot cube patterns: 3, 4 and 5.")
        + "<h2>Use a ten-frame</h2><p>The top row of a ten-frame holds 5. If the whole top row is full, there are 5.</p>"
        + figure(tenframe_svg(4), "4: one box in the top row is empty.")
        + "<h2>Two small parts</h2><p>Bigger groups can be seen as two small parts: see 2 and 3, and know it is 5.</p>"
        + figure(dice_svg([2, 3]), "2 and 3 make 5.")
        + mistakes([["Guessing after a very quick look", "Look at the pattern, then check by counting"],
                    ["Thinking spread-out things are more", "Spreading out does not change how many"],
                    ["Counting only one part", "Say both parts, then how many altogether"]]))


FAQ = [("What is subitising?",
        "Subitising is seeing how many are in a small group at a glance, without counting. The Australian Curriculum (AC9MFN02) asks Foundation students to subitise collections up to 5."),
       ("Why is subitising important?",
        "It builds number sense. Children who can see 3 and 2 quickly can later see 5, add small numbers in their heads and use ten-frames."),
       ("How can I help my child subitise at home?",
        "Play games with a dot cube, dominoes or playing cards. Flash a small group of blocks for a second and ask: How many did you see? How did you see it?"),
       ("Should my child still count to check?",
        "Yes. Seeing the amount first and then counting to check is a good habit. Over time the counting will be needed less.")]


def build():
    sets = [set_dice(R), set_frames(R), set_groups(R), set_parts(R), set_find(R)]
    finish(sets, R, max_num=8)
    make("subitising-to-5", 2, "AC9MFN02", "Number",
         "Subitising: See How Many at a Glance",
         "Foundation Subitising Worksheets: Dot Cubes, Ten-Frames and Small Groups to 5 (Free, with Answers)",
         "Subitising to 5",
         "Recognise and name the number of objects within a collection up to 5 using subitising.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on subitising to 5, matched to the Australian Curriculum (AC9MFN02): dot cubes, ten-frames, small groups and two parts at a glance. 100 picture questions with answers.",
         "Small groups up to 5 can be seen all at once, without counting.",
         "Learn the dot cube patterns. On a ten-frame, a full top row is 5. See 2 and 3 and know it is 5.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
