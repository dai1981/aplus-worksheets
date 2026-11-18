# -*- coding: utf-8 -*-
"""
AU Foundation Maths: Sharing and Grouping (Australian Curriculum v9.0, AC9MFN06)
  python3 tools/gen_au_maths_f_sharing_and_grouping.py
Share equally between 2, 3 or 4, decide whether a share is fair, make equal groups, count the things in
equal groups, and sharing and grouping stories (sometimes with one left over).
Wrong answers come from real mistakes: giving the total instead of each share, giving the number of groups
instead of the number in each group, and calling unequal shares fair.
"""
import random
from k_pics import row_svg, groups_svg, name, KINDS
from f_common import Kids, mcq, finish, make, fig, figure, mistakes

R = random.Random(99601)
YES = "Yes, each group has the same number"


# ------------------------------------------------------------ set 1: share equally
def set_share(rnd):
    K = Kids(rnd)
    its = []
    plan = [(4, 2), (6, 2), (2, 2), (8, 2), (10, 2), (6, 3), (3, 3), (9, 3), (12, 3), (4, 4), (8, 4), (12, 4),
            (12, 2), (14, 2), (15, 3), (16, 4), (18, 3), (20, 4), (16, 2), (20, 2)]
    for i, (t, p) in enumerate(plan):
        k = KINDS[i % len(KINDS)]
        kid = K.next()
        each = t // p
        who = {2: "2 friends", 3: "3 friends", 4: "4 friends"}[p]
        q = fig(row_svg(t, k)) + "%s shares %d %s equally between %s. How many does each friend get?" % (kid["n"], t, name(k), who)
        its.append(mcq(q, each, [t, p, each + 1, each - 1, each + 2, each + 3],
                       "Give one to each friend, again and again, until none are left. Each friend gets <b>%d</b>. Check: %s make %d." % (each, " and ".join([str(each)] * p), t)))
    return {"title": "Share equally", "items": its}


# ------------------------------------------------------------ set 2: fair or not?
def set_fair(rnd):
    its = []
    plan = [((3, 3), True), ((4, 2), False), ((2, 2, 2), True), ((5, 4), False), ((4, 4), True), ((3, 2, 3), False),
            ((5, 5), True), ((1, 1, 1), True), ((6, 5), False), ((2, 3, 2), False), ((3, 3, 3), True), ((4, 4, 3), False),
            ((2, 2, 2, 2), True), ((1, 2), False), ((6, 6), True), ((3, 3, 3, 2), False), ((4, 4, 4), True), ((5, 3), False),
            ((2, 2), True), ((2, 1, 2, 2), False)]
    for i, (g, fair) in enumerate(plan):
        k = KINDS[(i * 3) % len(KINDS)]
        q = fig(groups_svg([(n, k) for n in g])) + "Are the %s shared equally?" % name(k)
        if fair:
            right = YES
            wr = ["No, one group has more", "No, the groups are too small", "We cannot tell"]
            e = "Every group has %d. The share is fair. <b>Yes</b>." % g[0]
        else:
            right = "No, the groups are not the same"
            wr = [YES, "Yes, all the %s are shared" % name(k), "We cannot tell"]
            e = "The groups have %s. They are not the same, so it is <b>not</b> fair." % ", ".join(str(n) for n in g)
        its.append(mcq(q, right, wr, e))
    return {"title": "Is it fair?", "items": its}


# ------------------------------------------------------------ set 3: make equal groups
def set_groups(rnd):
    its = []
    plan = [(4, 2), (6, 2), (8, 2), (10, 2), (6, 3), (9, 3), (12, 3), (10, 5), (15, 5), (20, 5),
            (12, 2), (8, 4), (12, 4), (16, 4), (14, 2), (18, 3), (20, 10), (16, 2), (15, 3), (20, 4)]
    for i, (t, size) in enumerate(plan):
        k = KINDS[(i + 2) % len(KINDS)]
        g = t // size
        q = fig(row_svg(t, k)) + "Put the %d %s into groups of %d. How many groups?" % (t, name(k), size)
        its.append(mcq(q, g, [t, size, g + 1, g - 1, g + 2, g + 3],
                       "Circle %d at a time: %s. That is <b>%d</b> groups." % (size, ", ".join(str(size * j) for j in range(1, g + 1)), g)))
    return {"title": "Make equal groups", "items": its}


# ------------------------------------------------------------ set 4: count equal groups
def set_count(rnd):
    its = []
    plan = [(2, 2), (3, 2), (2, 3), (4, 2), (2, 5), (3, 3), (5, 2), (2, 4), (3, 4), (4, 3),
            (3, 5), (2, 10), (4, 4), (5, 3), (2, 6), (4, 5), (6, 2), (3, 6), (5, 4), (2, 7)]
    for i, (g, size) in enumerate(plan):
        k = KINDS[(i + 5) % len(KINDS)]
        q = fig(groups_svg([(size, k)] * g)) + "There are %d groups of %d %s. How many %s altogether?" % (g, size, name(k), name(k))
        t = g * size
        how = ", ".join(str(size * j) for j in range(1, g + 1)) if size in (2, 5, 10) else " and ".join([str(size)] * g)
        its.append(mcq(q, t, [g + size, g, size, t + 1, t - 1, t + 2],
                       ("Count by %ds: %s. There are <b>%d</b>." % (size, how, t)) if size in (2, 5, 10) else ("%s make <b>%d</b>." % (how, t))))
    return {"title": "Count the groups", "items": its}


# ------------------------------------------------------------ set 5: stories
def set_story(rnd):
    K = Kids(rnd)
    its = []
    stories = [
        ("{n} has 6 strawberries to share equally with a friend. How many does each of them get?", 3, [6, 2, 4]),
        ("There are 8 children. They make pairs (groups of 2) for a game. How many pairs?", 4, [8, 2, 6]),
        ("{n} puts 10 toy cars into 2 equal rows. How many cars are in each row?", 5, [10, 2, 4]),
        ("3 friends share 9 biscuits equally. How many biscuits does each friend get?", 3, [9, 6, 4]),
        ("{n} has 12 eggs. {He} puts them into egg cups, 1 in each. How many egg cups does {he} need?", 12, [6, 1, 11]),
        ("4 children share 8 pencils equally. How many pencils does each child get?", 2, [8, 4, 3]),
        ("There are 6 socks. How many pairs of socks is that?", 3, [6, 2, 4]),
        ("{n} shares 7 grapes between 2 plates. Each plate gets the same, and 1 is left over. How many are on each plate?", 3, [4, 7, 2]),
        ("{n} has 15 stickers. {He} puts 5 on each page. How many pages does {he} fill?", 3, [5, 15, 4]),
        ("There are 10 fingers on two hands. How many fingers on each hand?", 5, [10, 2, 4]),
        ("{n} shares 4 slices of pizza equally with 3 friends, so 4 people share. How many slices does each person get?", 1, [4, 3, 2]),
        ("There are 9 players. They make 3 equal teams. How many players in each team?", 3, [9, 6, 4]),
        ("{n} has 20 beads. {He} makes groups of 10. How many groups?", 2, [10, 20, 3]),
        ("Two children share 12 blocks equally. How many blocks does each child get?", 6, [12, 2, 5]),
        ("{n} puts 8 shoes in pairs. How many pairs?", 4, [8, 2, 6]),
        ("{n} has 5 lollies to share equally between 2 friends. How many does each friend get, and how many are left over?", "2 each, 1 left over", ["5 each, 0 left over", "3 each, 0 left over", "2 each, 0 left over"]),
        ("There are 3 cars. Each car has 4 wheels. How many wheels?", 12, [7, 4, 3]),
        ("{n} shares 10 marbles equally between 5 friends. How many marbles does each friend get?", 2, [10, 5, 3]),
        ("There are 4 plates with 2 sausages on each plate. How many sausages?", 8, [6, 4, 2]),
        ("{n} has 7 apples to share equally with 7 friends. How many does each friend get?", 1, [7, 14, 2]),
    ]
    for t, ans, wr in stories:
        kid = K.next()
        q = t.format(n=kid["n"], He=kid["He"], he=kid["he"])
        if isinstance(ans, str):
            e = "Give one each, then one each again: 2 each. 1 lolly is left over, so it cannot be shared fairly. <b>%s</b>." % ans
        elif "share" in t or "equal" in t or "each hand" in t:
            e = "Share them out one at a time until none are left. The answer is <b>%d</b>." % ans
        else:
            e = "Make or count the equal groups. The answer is <b>%d</b>." % ans
        its.append(mcq(q, ans, wr, e))
    return {"title": "Sharing and grouping stories", "items": its}


def body():
    return (
        "<h2>Share equally</h2>"
        "<p>To share <b>equally</b> (fairly), give one to each person, again and again, until none are left. Everyone gets the same.</p>"
        + figure(groups_svg([(3, "apple"), (3, "apple")]), "6 apples shared equally between 2: 3 each.")
        + "<h2>Fair or not fair?</h2><p>If one group has more, the share is not fair.</p>"
        + figure(groups_svg([(4, "star"), (2, "star")]), "4 and 2 are not the same. Not fair.")
        + "<h2>Equal groups</h2><p>Put things into groups of the same size. Count the groups, or count all the things.</p>"
        + figure(groups_svg([(2, "duck")] * 4), "4 groups of 2: 2, 4, 6, 8. There are 8 ducks.")
        + mistakes([["Giving the total instead of each share", "Count what one person gets"],
                    ["Counting the groups when the question asks how many in each", "Read the question again: each or groups?"],
                    ["Calling a share fair when one group has more", "Count each group and compare"]]))


FAQ = [("What do Foundation students learn about sharing and grouping?",
        "They act out equal sharing and grouping with real objects and use counting or subitising (AC9MFN06). This is the start of division and multiplication, without any signs."),
       ("What does sharing equally mean?",
        "Everyone gets the same amount. A good way is to deal the things out one at a time, like cards, until none are left."),
       ("What if there is one left over?",
        "Then the things cannot be shared equally. Talking about the left-over one is a great early idea about remainders."),
       ("How can I practise at home?",
        "Share snacks between family members, sort socks into pairs, or put toy cars into equal rows. Ask: Is it fair? How do you know?")]


def build():
    sets = [set_share(R), set_fair(R), set_groups(R), set_count(R), set_story(R)]
    finish(sets, R, max_num=22)
    make("sharing-and-grouping", 6, "AC9MFN06", "Number",
         "Sharing and Grouping: Equal Shares and Equal Groups",
         "Foundation Sharing and Grouping Worksheets: Fair Shares and Equal Groups (Free, with Answers)",
         "Sharing and grouping",
         "Represent practical situations that involve equal sharing and grouping with physical and virtual materials and use counting or subitising strategies.",
         "Free Foundation (Prep, Kindergarten) maths worksheets on sharing and grouping, matched to the Australian Curriculum (AC9MFN06): share equally, fair or not fair, make equal groups and count groups. 100 picture questions with answers.",
         "Sharing equally means everyone gets the same.",
         "Deal things out one at a time. Equal groups all have the same number.",
         body(), FAQ, sets)


if __name__ == "__main__":
    build()
