# -*- coding: utf-8 -*-
"""
BC Kindergarten Math: Equal and Not Equal (BC Mathematics Curriculum, Kindergarten Content: Equality and inequality
as a balance)
  python3 tools/gen_cabc_math_k_equal_and_not_equal.py
Balanced and not balanced pan scales, which side has more, making a scale balance, equal and not equal groups,
and fair sharing stories (fish drying on racks, sharing with a friend). The balance pictures are the BC Grade 1
pan balances (dots in rows of 5).
Wrong answers come from real mistakes: thinking the side that is higher has more, giving the bigger number
instead of how many to add, and thinking a group is equal because it looks as wide.
"""
import random
from k_pics import two_groups_svg, lettered_groups_svg, name, KINDS
from bck_common import Kids, Cycle, mcq, letters, finish, make, fig, figure, lesson, collect, S
import gen_cabc_math_g1_equality as g1

R = random.Random(52701)
BLUE, RED = "#1f5fa8", "#c0392b"
POS = Cycle()


def bal(a, b):
    return g1.balance_svg([(a, BLUE)] if a else [], [(b, RED)] if b else [])


# ------------------------------------------------------------ set 1: balanced or not?
def one_bal(r):
    a = r.randint(1, 10)
    b = a if r.random() < 0.45 else r.randint(1, 10)
    right = "Balanced (equal)" if a == b else "Not balanced (not equal)"
    return mcq(fig(bal(a, b)) + "Is the scale balanced?", right, ["Not balanced (not equal)" if a == b else "Balanced (equal)", "We cannot tell", "Both sides are empty"],
               "Left: %d. Right: %d. %s" % (a, b, "The same number on each side, so the scale is level: <b>%s</b>." % right if a == b else "%d and %d are different, so one side goes down: <b>%s</b>." % (a, b, right)))


# ------------------------------------------------------------ set 2: which side has more?
def one_side(r):
    a, b = r.randint(1, 10), r.randint(1, 10)
    if a == b:
        return None
    side = "The left side" if a > b else "The right side"
    other = "The right side" if a > b else "The left side"
    kind = r.choice(["more", "down", "less"])
    if kind == "more":
        return mcq(fig(bal(a, b)) + "Which side has <b>more</b>?", side, [other, "They are the same", "We cannot tell"], "%d is more than %d. The side with more goes down: <b>%s</b>." % (max(a, b), min(a, b), side.lower()))
    if kind == "down":
        return mcq(fig(bal(a, b)) + "Why is one side lower?", "It has more", ["It has fewer", "Both sides are equal", "It is closer to the ground"], "The lower side has %d and the other has %d. <b>It has more</b>." % (max(a, b), min(a, b)))
    return mcq(fig(bal(a, b)) + "Which side has <b>fewer</b>?", other, [side, "They are the same", "We cannot tell"], "%d is fewer than %d. The side with fewer goes up: <b>%s</b>." % (min(a, b), max(a, b), other.lower()))


# ------------------------------------------------------------ set 3: make it balance
def one_fix(r):
    a, b = r.randint(1, 10), r.randint(1, 10)
    if a == b or abs(a - b) > 5:
        return None
    d = abs(a - b)
    lighter = "right" if a > b else "left"
    kind = r.choice(["add", "add", "remove"])
    if kind == "add":
        return mcq(fig(bal(a, b)) + "How many dots should you <b>add</b> to the %s side to make the scale balance?" % lighter, d, [max(a, b), min(a, b), d + 1, d - 1],
                   "%d and %d. Add <b>%d</b> to the %s side to make both sides %d." % (a, b, d, lighter, max(a, b)))
    heavier = "left" if a > b else "right"
    return mcq(fig(bal(a, b)) + "How many dots should you <b>take off</b> the %s side to make the scale balance?" % heavier, d, [max(a, b), min(a, b), d + 1, d - 1],
               "Take <b>%d</b> off the %s side. Then both sides have %d." % (d, heavier, min(a, b)))


# ------------------------------------------------------------ set 4: equal groups
def one_groups(r):
    kind = r.choice(["eq", "eq", "which"])
    k = r.choice(KINDS)
    if kind == "eq":
        a = r.randint(1, 10)
        b = a if r.random() < 0.5 else r.randint(1, 10)
        k2 = r.choice(KINDS)
        right = "Equal" if a == b else "Not equal"
        return mcq(fig(two_groups_svg(a, k, b, k2, "?")) + "Are the two groups equal or not equal?", right, ["Not equal" if a == b else "Equal", "We cannot tell", "Equal, because they look the same size"],
                   "%d %s and %d %s: <b>%s</b>." % (a, name(k, a), b, name(k2, b), right))
    n = r.randint(2, 9)
    vals = [n] + r.sample([v for v in range(1, 11) if v != n], 3)
    j = POS.next()
    vals[0], vals[j] = vals[j], vals[0]
    q = fig(lettered_groups_svg([(v, k) for v in vals])) + "Which group is <b>equal</b> to %d?" % n
    it = mcq(q, "ABCD"[j], [l for l in "ABCD" if l != "ABCD"[j]], "Count each group. Group <b>%s</b> has %d, so it is equal to %d." % ("ABCD"[j], n, n))
    return letters(it, "ABCD"[j])


# ------------------------------------------------------------ set 5: fair sharing stories
def one_story(r):
    K = Kids(r)
    k = K.next()
    kind = r.choice(["rack", "rack", "share", "plates"])
    a, b = r.randint(1, 8), r.randint(1, 8)
    if kind == "rack":
        if a == b:
            q = "%s's grandpa hangs %d fish on one drying rack and %d fish on the other. Are the racks equal?" % (k["n"], a, b)
            return mcq(q, "Yes, they are equal", ["No, they are not equal", "We cannot tell", "One rack has 1 more"], "%d and %d are the same: <b>Yes, they are equal</b>." % (a, b))
        if abs(a - b) % 2 or abs(a - b) > 4:
            return None
        m = abs(a - b) // 2
        q = "%s's grandpa hangs %d fish on one drying rack and %d on the other. How many fish should he move to make the racks equal?" % (k["n"], max(a, b), min(a, b))
        return mcq(q, m, [abs(a - b), max(a, b), m + 1], "Move <b>%d</b> from %d to %d. Then both racks have %d." % (m, max(a, b), min(a, b), (a + b) // 2))
    if kind == "share":
        n = r.choice([2, 4, 6, 8, 10])
        what = r.choice(["berries", "stickers", "crackers", "shells", "grapes"])
        q = "%s shares %d %s fairly with a friend. Each gets the same number. How many does each get?" % (k["n"], n, what)
        return mcq(q, n // 2, [n, n // 2 + 1, n // 2 - 1 if n > 2 else 3], "Fair means equal shares. %d is %d and %d, so each gets <b>%d</b>." % (n, n // 2, n // 2, n // 2))
    if a == b:
        return None
    q = "One plate has %d crackers. Another plate has %d crackers. Is that fair?" % (a, b)
    return mcq(q, "No, the plates are not equal", ["Yes, the plates are equal", "Yes, because both are plates", "We cannot tell"], "%d and %d are different: <b>No, the plates are not equal</b>." % (a, b))


def build():
    sets = [S("Balanced or not?", collect(one_bal, 20, R)),
            S("Which side has more?", collect(one_side, 20, R)),
            S("Make it balance", collect(one_fix, 20, R)),
            S("Equal and not equal groups", collect(one_groups, 20, R)),
            S("Fair sharing stories", collect(one_story, 20, R))]
    finish(sets, R, max_num=10)
    body = lesson(
        "<ul><li>A pan scale is <b>balanced</b> (level) when both sides have the same amount. The sides are <b>equal</b>.</li>"
        "<li>When one side has more, that side goes <b>down</b>. The sides are <b>not equal</b>.</li>"
        "<li>To make a scale balance, add to the side with fewer, or take some off the side with more.</li></ul>",
        [figure(bal(4, 4), "4 and 4: balanced, equal."),
         figure(bal(6, 3), "6 and 3: the left side goes down. Add 3 to the right side to balance.")],
        [["Thinking the higher side has more", "The side with more is heavier and goes down."],
         ["Giving the bigger number for how many to add", "Find how many more the heavier side has."],
         ["Thinking groups are equal because they look as wide", "Count both groups."]])
    faq = [("What does equality as a balance mean?", "Two amounts are equal when a pan balance is level. If one side has more, it goes down and the amounts are not equal."),
           ("How can I show equal and not equal at home?", "Use a coat hanger with two cups, or line up two rows of toys and count each row."),
           ("What is fair sharing?", "Sharing so that everyone gets an equal amount, like putting the same number of fish on each drying rack."),
           ("Do Kindergarten children use the = sign?", "They start with the words equal and not equal and with balances. The = and ≠ symbols come in Grade 1.")]
    make("equal-and-not-equal", 7, "Patterning", "Equal and Not Equal: Balances and Fair Sharing", "Equal and not equal",
         "Equality and inequality as a balance: modeling equality as balanced and inequality as imbalanced using concrete and visual models; fish drying and sharing",
         "Free Kindergarten math worksheets on equal and not equal for the BC curriculum: pan balances, which side has more, making a balance, equal groups and fair sharing stories. 100 picture questions with answers.",
         "Equal amounts make a balance level.", "If one side has more, it goes down. Add to the lighter side or take from the heavier side to balance.",
         body, faq, sets)


if __name__ == "__main__":
    build()
