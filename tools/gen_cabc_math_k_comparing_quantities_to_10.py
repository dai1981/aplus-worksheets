# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Comparing Quantities to 10 (BC Mathematics Curriculum, Kindergarten Content: Ways to make 5 —
comparing quantities, 1-10)
  python3 tools/gen_cabc_math_k_comparing_quantities_to_10.py
Matching one to one to see more, fewer or the same, finding the group with the most or fewest, how many more,
comparing numbers to 10, and comparing in stories.
Wrong answers come from real mistakes: thinking the longer row has more, mixing up more and fewer, and giving
the bigger number instead of the difference.
"""
import random
from k_pics import match_svg, two_groups_svg, lettered_groups_svg, cards_svg, name, KINDS
from bck_common import Kids, Cycle, mcq, letters, finish, make, fig, figure, lesson, collect, S

R = random.Random(52301)


def near(n, lo=0, hi=10):
    return [x for x in [n + 1, n - 1, n + 2, n - 2, n + 3] if lo <= x <= hi and x != n]


# ------------------------------------------------------------ set 1: more, fewer or the same
def one_match(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    k1, k2 = r.sample(KINDS, 2)
    sp1, sp2 = (34, 34) if r.random() < 0.5 else ((46, 30) if a < b else (30, 46))
    pic = fig(match_svg([(a, k1, "", sp1), (b, k2, "", sp2)]))
    if a == b:
        q = pic + "Are there more %s, more %s, or the same number?" % (name(k1), name(k2))
        return mcq(q, "The same number", ["More %s" % name(k1), "More %s" % name(k2), "We cannot tell"], "Match them one to one. Nothing is left over, so there is <b>the same number</b> of each.")
    more = k1 if a > b else k2
    less = k2 if a > b else k1
    if r.random() < 0.5:
        q = pic + "Are there more %s or more %s?" % (name(k1), name(k2))
        return mcq(q, "More %s" % name(more), ["More %s" % name(less), "The same number", "We cannot tell"],
                   "Match them one to one. Some %s are left over, so there are <b>more %s</b>. A longer row does not always mean more." % (name(more), name(more)))
    q = pic + "Which are <b>fewer</b>: the %s or the %s?" % (name(k1), name(k2))
    return mcq(q, "The %s" % name(less), ["The %s" % name(more), "They are the same", "We cannot tell"],
               "%d is less than %d. Fewer means not as many: <b>the %s</b>." % (min(a, b), max(a, b), name(less)))


# ------------------------------------------------------------ set 2: the most and the fewest
POS = Cycle()


def one_most(r):
    vals = r.sample(range(1, 11), 4)
    k = r.choice(KINDS)
    word = r.choice(["most", "fewest"])
    target = max(vals) if word == "most" else min(vals)
    i, j = vals.index(target), POS.next()
    vals[i], vals[j] = vals[j], vals[i]
    letter = "ABCD"[vals.index(target)]
    q = fig(lettered_groups_svg([(v, k) for v in vals])) + "Which group has the <b>%s</b> %s?" % (word, name(k))
    it = mcq(q, letter, [l for l in "ABCD" if l != letter], "Count each group: %s. Group <b>%s</b> has the %s (%d)." % (", ".join("%s has %d" % (L, v) for L, v in zip("ABCD", vals)), letter, word, target))
    return letters(it, letter)


# ------------------------------------------------------------ set 3: how many more?
def one_diff(r):
    a, b = r.randint(1, 10), r.randint(1, 10)
    if a == b or abs(a - b) > 5:
        return None
    k1, k2 = r.sample(KINDS, 2)
    big, small = (k1, k2) if a > b else (k2, k1)
    q = fig(match_svg([(a, k1, "", 34), (b, k2, "", 34)])) + "How many more %s than %s are there?" % (name(big), name(small))
    d = abs(a - b)
    return mcq(q, d, [max(a, b), min(a, b), d + 1, d - 1], "Match them one to one. <b>%d</b> %s %s left over." % (d, name(big, d), "is" if d == 1 else "are"))


# ------------------------------------------------------------ set 4: comparing numbers
def one_num(r):
    a, b = r.sample(range(0, 11), 2)
    kind = r.choice(["bigger", "smaller", "order", "order"])
    if kind == "bigger":
        return mcq(fig(cards_svg([str(a), str(b)])) + "Which number is <b>bigger</b>?", max(a, b), [min(a, b), "They are the same", max(a, b) + 1 if max(a, b) < 10 else min(a, b) + 1 if min(a, b) + 1 != max(a, b) else 0], "When we count, %d comes after %d, so <b>%d</b> is bigger." % (max(a, b), min(a, b), max(a, b)), allow_zero=True)
    if kind == "smaller":
        return mcq(fig(cards_svg([str(a), str(b)])) + "Which number is <b>smaller</b>?", min(a, b), [max(a, b), "They are the same", min(a, b) + 1 if min(a, b) + 1 != max(a, b) else max(a, b) - 2], "When we count, %d comes before %d, so <b>%d</b> is smaller." % (min(a, b), max(a, b), min(a, b)), allow_zero=True)
    t = r.sample(range(0, 11), 3)
    srt = sorted(t)
    ans = ", ".join(map(str, srt))
    wr = [", ".join(map(str, srt[::-1])), ", ".join(map(str, t)) if t != srt else ", ".join(map(str, [srt[1], srt[0], srt[2]])), ", ".join(map(str, [srt[0], srt[2], srt[1]]))]
    return mcq(fig(cards_svg([str(x) for x in t])) + "Put the numbers in order, <b>smallest first</b>.", ans, wr, "Start with the smallest: <b>%s</b>." % ans, allow_zero=True)


# ------------------------------------------------------------ set 5: stories
def one_story(r):
    K = Kids(r)
    p1 = K.next()
    p2 = K.next()
    a, b = r.randint(1, 10), r.randint(1, 10)
    if a == b:
        return None
    what = r.choice(["shells", "stickers", "rocks", "cones", "berries", "leaves"])
    kind = r.choice(["who", "who", "diff", "same"])
    if kind == "who":
        return mcq("%s has %d %s. %s has %d %s. Who has <b>more</b>?" % (p1["n"], a, what, p2["n"], b, what), p1["n"] if a > b else p2["n"], [p2["n"] if a > b else p1["n"], "They have the same", "We cannot tell"],
                   "%d is more than %d, so <b>%s</b> has more." % (max(a, b), min(a, b), p1["n"] if a > b else p2["n"]))
    if kind == "diff":
        if abs(a - b) > 5:
            return None
        return mcq("%s has %d %s. %s has %d %s. How many more does %s have?" % (p1["n"], a, what, p2["n"], b, what, p1["n"] if a > b else p2["n"]), abs(a - b), [max(a, b), min(a, b), abs(a - b) + 1],
                   "Line them up and match. %d is <b>%d</b> more than %d." % (max(a, b), abs(a - b), min(a, b)))
    c = r.randint(2, 9)
    return mcq("%s has %d %s. %s has %d. How many more does %s need to have the same as %s?" % (p1["n"], c, what, p2["n"], c - 1, p2["n"], p1["n"]), 1, [c, c - 1, 2],
               "%d is 1 more than %d, so %s needs <b>1</b> more." % (c, c - 1, p2["n"]))


def build():
    sets = [S("More, fewer or the same", collect(one_match, 20, R)),
            S("The most and the fewest", collect(one_most, 20, R)),
            S("How many more?", collect(one_diff, 20, R)),
            S("Bigger and smaller numbers", collect(one_num, 20, R)),
            S("Comparing in stories", collect(one_story, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li>Line up two groups and <b>match them one to one</b>. The group with some left over has <b>more</b>.</li>"
        "<li>The other group has <b>fewer</b>. If nothing is left over, they are <b>the same</b>.</li>"
        "<li>When we count, a bigger number comes later: 7 is more than 4.</li></ul>",
        [figure(match_svg([(6, "apple", "", 34), (4, "star", "", 34)]), "Match one to one: 2 apples are left over. There are 2 more apples than stars."),
         figure(cards_svg(["3", "8"]), "8 comes after 3 when we count, so 8 is bigger.")],
        [["Thinking the longer row has more", "Match one to one, or count both rows."],
         ["Mixing up more and fewer", "More means the group with extra. Fewer means not as many."],
         ["Giving the bigger number for how many more", "Count only the ones left over after matching."]])
    faq = [("How do Kindergarten children compare quantities?", "They line up two groups and match them one to one, or count both groups and compare the numbers up to 10."),
           ("What is the difference between more and fewer?", "More is the group with extra left over after matching. Fewer is the group that runs out first."),
           ("Why match one to one?", "Spreading things out can make a row look longer. Matching shows which group really has more."),
           ("How can I practise at home?", "Put out two small piles of toys, line them up side by side, and ask which pile has more and how many more.")]
    make("comparing-quantities-to-10", 3, "Number", "Comparing Quantities to 10: More, Fewer and the Same", "Comparing quantities to 10",
         "Comparing quantities, 1-10",
         "Free Kindergarten math worksheets on comparing quantities to 10 for the BC curriculum: match one to one, more, fewer, the same, most and fewest, how many more, and bigger and smaller numbers. 100 picture questions with answers.",
         "Match one to one: the group with some left over has more.", "If nothing is left over, the groups are the same. A longer row does not always have more.",
         body, faq, sets)


if __name__ == "__main__":
    build()
