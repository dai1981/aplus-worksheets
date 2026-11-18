# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Counting and Comparing Collections (Australian Curriculum v9.0, AC9MFN03)
  python3 tools/gen_au_maths_f_counting_and_comparing.py
Count collections to 20, compare two rows by matching one to one (more, fewer, the same), find the group
with the most or fewest, find how many more, and explain who has more in stories.
Wrong answers come from real mistakes: judging by how long a row looks, mixing up more and fewer, counting
one thing twice, and answering with the bigger number instead of how many more.
"""
import random
from k_pics import row_svg, match_svg, lettered_groups_svg, scatter_svg, name, KINDS, CELL
from f_common import Kids, mcq, finish, make, fig, figure, mistakes

R = random.Random(99301)
SAME = "The same number"


# ------------------------------------------------------------ set 1: count to 20
def set_count(rnd):
    its = []
    plan = [(11, "apple"), (14, "star"), (12, "duck"), (16, "ball"), (13, "fish"), (18, "flower"), (15, "heart"), (20, "cup"),
            (17, "bug"), (19, "button"), (12, "star"), (15, "apple"), (13, "ball"), (16, "duck"), (11, "heart"), (14, "fish"),
            (19, "flower"), (17, "cup"), (20, "bug"), (18, "button")]
    for i, (n, k) in enumerate(plan):
        svg = row_svg(n, k) if i < 10 or n > 16 else scatter_svg(n, k, 1300 + i)
        q = fig(svg) + "How many %s?" % name(k)
        tip = "The first row has 10. Count on from 10: %s. " % ", ".join(str(v) for v in range(11, n + 1)) if svg.count("in rows") and n > 10 else "Touch each one once as you count. "
        its.append(mcq(q, n, [n - 1, n + 1, n - 10, n + 2], tip + "There are <b>%d</b>." % n))
    return {"title": "Counting to 20", "items": its}


# ------------------------------------------------------------ set 2: more, fewer or the same
def set_rows(rnd):
    its = []
    plan = [(5, 3, "apple", "cup"), (4, 4, "duck", "fish"), (2, 6, "star", "heart"), (7, 5, "ball", "flower"), (6, 6, "bug", "button"),
            (3, 7, "cup", "apple"), (8, 6, "fish", "duck"), (5, 5, "heart", "star"), (9, 7, "flower", "ball"), (4, 8, "button", "bug"),
            (10, 7, "apple", "star"), (6, 9, "duck", "cup"), (8, 8, "ball", "heart")]
    for i, (a, b, ka, kb) in enumerate(plan):
        A, B = name(ka), name(kb)
        svg = match_svg([(a, ka, "", 0), (b, kb, "", 0)])
        if i % 2 == 0:
            q = fig(svg) + "Are there more %s or more %s?" % (A, B)
            ans = SAME if a == b else ("More " + A if a > b else "More " + B)
            ch = ["More " + A, "More " + B, SAME, "We cannot tell"]
        else:
            q = fig(svg) + "Are there fewer %s or fewer %s?" % (A, B)
            ans = SAME if a == b else ("Fewer " + A if a < b else "Fewer " + B)
            ch = ["Fewer " + A, "Fewer " + B, SAME, "We cannot tell"]
        if a == b:
            e = "Match them one to one. None are left over: <b>the same number</b> (%d each)." % a
        else:
            big = A if a > b else B
            e = "Match them one to one. Some %s have no partner, so there are more %s. <b>%s</b>." % (big, big, ans)
        its.append(mcq(q, ans, [c for c in ch if c != ans], e))
    for a, b, ka, kb in [(4, 6, "duck", "apple"), (5, 7, "star", "cup"), (3, 5, "ball", "fish"), (6, 6, "flower", "heart"),
                         (5, 8, "heart", "button"), (7, 7, "cup", "duck"), (4, 5, "bug", "star")]:
        A, B = name(ka), name(kb)
        sp = int(CELL * b / a + 6) if a < b else CELL + 22
        svg = match_svg([(a, ka, "", sp), (b, kb, "", 0)])
        q = fig(svg) + "The %s are spread out. Are there more %s or more %s?" % (A, A, B)
        ans = SAME if a == b else "More " + B
        e = ("Do not look at how long the row is. Count: %d %s and %d %s. " % (a, A, b, B)) + ("<b>The same number</b>." if a == b else "<b>More %s</b>." % B)
        its.append(mcq(q, ans, [c for c in ["More " + A, "More " + B, SAME, "We cannot tell"] if c != ans], e))
    return {"title": "More, fewer or the same", "items": its}


# ------------------------------------------------------------ set 3: most and fewest
def set_most(rnd):
    its = []
    for i in range(20):
        k = KINDS[i % len(KINDS)]
        lo = 3 if i < 10 else 8
        vals = rnd.sample(range(lo, lo + 8), 4)
        want = "most" if i % 2 == 0 else "fewest"
        t = max(vals) if want == "most" else min(vals)
        letter = "ABCD"[vals.index(t)]
        q = fig(lettered_groups_svg([(v, k) for v in vals])) + "Which box has the <b>%s</b> %s?" % (want, name(k))
        e = "Count each box: %s. %d is the %s, so box <b>%s</b>." % (", ".join("%s has %d" % ("ABCD"[j], v) for j, v in enumerate(vals)), t,
                                                                   "biggest number" if want == "most" else "smallest number", letter)
        its.append(mcq(q, "Box " + letter, ["Box " + x for x in "ABCD" if x != letter], e))
    return {"title": "The most and the fewest", "items": its}


# ------------------------------------------------------------ set 4: how many more?
def set_diff(rnd):
    its = []
    plan = [(5, 3, "apple", "cup"), (6, 4, "duck", "fish"), (7, 6, "star", "heart"), (4, 1, "ball", "flower"), (8, 5, "bug", "button"),
            (6, 3, "cup", "apple"), (9, 7, "fish", "duck"), (5, 4, "heart", "star"), (10, 8, "flower", "ball"), (7, 3, "button", "bug"),
            (3, 6, "apple", "star"), (2, 5, "duck", "cup"), (4, 8, "ball", "heart"), (6, 7, "fish", "flower"), (5, 9, "bug", "apple"),
            (3, 4, "star", "duck"), (1, 4, "cup", "ball"), (6, 10, "heart", "fish"), (7, 9, "flower", "bug"), (2, 6, "button", "star")]
    for i, (a, b, ka, kb) in enumerate(plan):
        A, B = name(ka), name(kb)
        svg = match_svg([(a, ka, "", 0), (b, kb, "", 0)])
        d = abs(a - b)
        if a > b:
            q = fig(svg) + "How many more %s than %s?" % (A, B)
            e = "Match them. %d %s have no partner, so there %s <b>%d</b> more %s." % (d, name(ka, d), "is" if d == 1 else "are", d, name(ka, d))
        else:
            q = fig(svg) + "How many fewer %s than %s?" % (A, B)
            e = "Match them. %d %s have no partner, so there %s <b>%d</b> fewer %s." % (d, name(kb, d), "is" if d == 1 else "are", d, name(ka, d))
        if d == 1:
            e = e.replace("have no partner", "has no partner")
        its.append(mcq(q, d, [max(a, b), min(a, b), d + 1, d + 2], e))
    return {"title": "How many more? How many fewer?", "items": its}


# ------------------------------------------------------------ set 5: who has more?
THINGS = ["stickers", "shells", "marbles", "pencils", "leaves", "blocks", "beads", "cards"]


def set_story(rnd):
    K = Kids(rnd)
    its = []
    plan = [(12, 15), (9, 6), (14, 14), (11, 17), (20, 18), (8, 13), (16, 10), (7, 7), (13, 19), (18, 12),
            (5, 9), (15, 11), (17, 20), (10, 10), (19, 14), (6, 16), (12, 8), (11, 11), (4, 14), (20, 15)]
    for i, (a, b) in enumerate(plan):
        k1, k2 = K.next(), K.next()
        while k2["n"] == k1["n"]:
            k2 = K.next()
        th = THINGS[i % len(THINGS)]
        if i % 2 == 0:
            q = "%s has %d %s. %s has %d %s. Who has more? How do you know?" % (k1["n"], a, th, k2["n"], b, th)
            if a == b:
                ans = "Neither. They both have %d" % a
                wr = ["%s, because %s name comes first" % (k1["n"], k1["his"]), "%s, because %d is more" % (k2["n"], b + 1), "We cannot tell without the %s" % th]
            else:
                w, l, wn, ln = (k1["n"], k2["n"], a, b) if a > b else (k2["n"], k1["n"], b, a)
                ans = "%s, because %d comes after %d when we count" % (w, wn, ln)
                wr = ["%s, because %d comes after %d when we count" % (l, wn, ln), "%s, because %d is the first number" % (l, ln), "They have the same number"]
        else:
            q = "%s has %d %s. %s has %d %s. Who has fewer? How do you know?" % (k1["n"], a, th, k2["n"], b, th)
            if a == b:
                ans = "Neither. They both have %d" % a
                wr = ["%s, because %s name comes first" % (k1["n"], k1["his"]), "%s, because %d is less" % (k2["n"], b - 1), "We cannot tell without the %s" % th]
            else:
                w, l, wn, ln = (k1["n"], k2["n"], a, b) if a < b else (k2["n"], k1["n"], b, a)
                ans = "%s, because %d comes before %d when we count" % (w, wn, ln)
                wr = ["%s, because %d comes before %d when we count" % (l, wn, ln), "%s, because %d is the bigger number" % (l, ln), "They have the same number"]
        e = ("They both have %d, so <b>neither</b> has more or fewer." % a) if a == b else "<b>%s</b>." % ans
        its.append(mcq(q, ans, wr, e))
    return {"title": "Who has more? Explain", "items": its}


def body():
    return (
        "<h2>Count to 20</h2>"
        "<p>Touch each thing once. When there are more than 10, count the first 10, then <b>count on</b>: 11, 12, 13 …</p>"
        + figure(row_svg(13, "star"), "10 in the first row, then 11, 12, 13. There are 13 stars.")
        + "<h2>Match one to one</h2><p>Line up two groups. The group with things left over has <b>more</b>. The other has <b>fewer</b>. "
        "If nothing is left over, they are <b>the same</b>.</p>"
        + figure(match_svg([(6, "apple", "", 0), (4, "cup", "", 0)]), "2 apples have no cup: 2 more apples than cups.")
        + "<h2>Explain your thinking</h2><p>Say why: 15 comes after 12 when we count, so 15 is more.</p>"
        + mistakes([["Thinking a longer row has more", "Match or count both rows"],
                    ["Mixing up more and fewer", "More has some left over"],
                    ["Answering 7 for 'how many more' when there are 7 and 5", "Count only the ones left over: 2"]]))


FAQ = [("What does quantify and compare collections mean?",
        "It means counting how many are in a group and saying which group has more, fewer or the same. Foundation students do this for collections up to at least 20 (AC9MFN03)."),
       ("Why does my child think a spread-out row has more?",
        "Young children often judge by length. Match the two rows one to one or count both to show the number stays the same."),
       ("How can my child explain which group has more?",
        "Encourage sentences like: There are 2 left over, so there are more apples, or 15 comes after 12 when we count, so 15 is more."),
       ("What can we count at home?",
        "Count pegs, shells, socks or toy cars up to 20, then compare two piles. Ask: Which has more? How do you know?")]


def build():
    sets = [set_count(R), set_rows(R), set_most(R), set_diff(R), set_story(R)]
    finish(sets, R, max_num=22)
    make("counting-and-comparing-collections", 3, "AC9MFN03", "Number",
         "Counting and Comparing Collections to 20",
         "Foundation Counting and Comparing Worksheets: More, Fewer, the Same to 20 (Free, with Answers)",
         "Counting and comparing",
         "Quantify and compare collections to at least 20 using counting and explain or demonstrate reasoning.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on counting and comparing collections to 20, matched to the Australian Curriculum (AC9MFN03): count on past 10, match one to one, more, fewer, the same, most and fewest. 100 picture questions with answers.",
         "Match one to one: the group with some left over has more.",
         "Count each thing once. A longer row is not always more. Say how you know.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
