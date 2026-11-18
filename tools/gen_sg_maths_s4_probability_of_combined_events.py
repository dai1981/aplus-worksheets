# -*- coding: utf-8 -*-
"""
SG Secondary 4 Maths: Probability of Combined Events (MOE syllabus S2: possibility diagrams and tree diagrams;
addition and multiplication of probabilities for mutually exclusive and independent events)
  python3 tools/gen_sg_maths_s4_probability_of_combined_events.py
Possibility diagrams for two dice, coins and spinners, the addition rule for mutually exclusive events, the
multiplication rule for independent events, tree diagrams with and without replacement, and problems.
Set 1 reuses the UK Year 8 dice maker.
Wrong answers come from real mistakes: adding when the events happen together, multiplying when either one will
do, forgetting the second branch order (red then blue or blue then red), and not reducing the total when an
item is not replaced.
"""
import random
from fractions import Fraction as F
from sg_sec import num, S, make, lesson, collect, T, fr, fig, svg_wrap, text, line, People, adopt
import gen_uk_maths_y8_probability_of_combined_events as uk

R = random.Random(840800)
adopt(uk, R)
P = People(R)
QP, pf = uk.QP, uk.pf


def pt(v):
    """plain fraction text for use inside SVG"""
    v = F(v)
    return "%d/%d" % (v.numerator, v.denominator) if v.denominator != 1 else str(v.numerator)


def tree_svg(p1, labels, p2=None, label="tree diagram"):
    """two-stage tree; p1: probabilities of first stage (2 branches), p2: list of the 2 second-stage pairs"""
    p2 = p2 or [p1, p1]
    W, H = 340, 230
    s = []
    x0, x1, x2 = 20, 130, 260
    ys1 = [65, 165]
    ys2 = [[30, 100], [130, 200]]
    for i in range(2):
        s.append(line(x0, 115, x1, ys1[i], "#2b2b2b", 2))
        s.append(text((x0 + x1) / 2 - 6, (115 + ys1[i]) / 2 + (-10 if i == 0 else 18), p1[i], 13, col="#1f6fd1"))
        s.append(text(x1 + 18, ys1[i] + 5, labels[i], 13))
        for j in range(2):
            s.append(line(x1 + 40, ys1[i], x2, ys2[i][j], "#2b2b2b", 2))
            s.append(text((x1 + 40 + x2) / 2 - 4, (ys1[i] + ys2[i][j]) / 2 + (-8 if j == 0 else 16), p2[i][j], 13, col="#1f6fd1"))
            s.append(text(x2 + 30, ys2[i][j] + 5, labels[j], 13))
    return fig(svg_wrap(W, H, "".join(s), label))


def bag(r):
    a, b = r.randint(2, 7), r.randint(2, 7)
    cols = r.choice([("red", "blue"), ("green", "yellow"), ("black", "white"), ("orange", "purple")])
    return a, b, cols


# ------------------------------------------------------------ set 1: possibility diagrams
def one_space(r):
    return uk.one_dice(r) if r.random() < 0.7 else uk.one_coin_spinner(r)


# ------------------------------------------------------------ set 2: addition and multiplication rules
def one_rules(r):
    kind = r.choice(["or", "or", "and", "and", "not"])
    if kind == "or":
        n = r.choice([10, 12, 15, 20, 25])
        a, b = r.sample(range(1, n // 2), 2)
        nm = r.choice([("a red sweet", "a green sweet"), ("a fiction book", "a comic"), ("a gold coin", "a silver coin")])
        q = "A box holds %d items. P(%s) = %s and P(%s) = %s. One item is picked at random. Find P(%s or %s)." % (n, nm[0], pf(F(a, n)), nm[1], pf(F(b, n)), nm[0], nm[1])
        return QP(q, F(a + b, n), [F(a * b, n * n), F(a, n), 1 - F(a + b, n)], "The events are mutually exclusive (one item cannot be both), so add: %s + %s = <b>%s</b>." % (pf(F(a, n)), pf(F(b, n)), pf(F(a + b, n))))
    if kind == "and":
        p1 = F(r.randint(1, 5), r.choice([6, 8, 10]))
        p2 = F(r.randint(1, 4), r.choice([5, 6, 10]))
        if p1 >= 1 or p2 >= 1:
            return None
        ev = r.choice([("it rains on Monday", "the bus is late on Tuesday"), ("Ahmad wins his game", "Siti wins her game"), ("a light is red at the first junction", "a light is red at the second junction")])
        q = "P(%s) = %s and P(%s) = %s. The events are independent. Find the probability that both happen." % (ev[0], pf(p1), ev[1], pf(p2))
        return QP(q, p1 * p2, [p1 + p2 if p1 + p2 <= 1 else None, (1 - p1) * (1 - p2), p1 * (1 - p2)], "Independent events: multiply. %s × %s = <b>%s</b>." % (pf(p1), pf(p2), pf(p1 * p2)))
    p1 = F(r.randint(1, 4), r.choice([5, 6, 8]))
    p2 = F(r.randint(1, 4), r.choice([5, 6, 8]))
    if p1 >= 1 or p2 >= 1:
        return None
    q = "Two archers each shoot once. The probabilities of hitting the target are %s and %s, independently. Find the probability that neither hits." % (pf(p1), pf(p2))
    ans = (1 - p1) * (1 - p2)
    return QP(q, ans, [1 - p1 * p2, p1 * p2, 1 - p1 - p2 if 1 - p1 - p2 >= 0 else None], "P(miss) = %s and %s. Multiply: %s × %s = <b>%s</b>." % (pf(1 - p1), pf(1 - p2), pf(1 - p1), pf(1 - p2), pf(ans)))


# ------------------------------------------------------------ set 3: tree diagrams with replacement
def one_with(r):
    a, b, cols = bag(r)
    n = a + b
    pa, pb = F(a, n), F(b, n)
    pic = tree_svg([pt(pa), pt(pb)], [cols[0][0].upper(), cols[1][0].upper()], label="tree diagram for two picks with replacement")
    pre = "A bag has %d %s and %d %s balls. A ball is taken at random, its colour noted, and then it is replaced. A second ball is taken.%s" % (a, cols[0], b, cols[1], pic)
    kind = r.choice(["both", "both2", "diff", "atleast"])
    if kind == "both":
        return QP(pre + " Find the probability that both are %s." % cols[0], pa * pa, [pa + pa if pa + pa <= 1 else None, pa * F(a - 1, n - 1), pa], "Multiply along the branches: %s × %s = <b>%s</b>." % (pf(pa), pf(pa), pf(pa * pa)))
    if kind == "both2":
        return QP(pre + " Find the probability that both are %s." % cols[1], pb * pb, [pb * F(b - 1, n - 1), pb, 2 * pb * pb if 2 * pb * pb <= 1 else None], "Multiply along the branches: %s × %s = <b>%s</b>." % (pf(pb), pf(pb), pf(pb * pb)))
    if kind == "diff":
        ans = 2 * pa * pb
        return QP(pre + " Find the probability that the two balls are different colours.", ans, [pa * pb, pa + pb if pa + pb < 1 else None, 1 - pa * pb],
                  "Two paths: %s then %s, or %s then %s. %s × %s + %s × %s = <b>%s</b>." % (cols[0], cols[1], cols[1], cols[0], pf(pa), pf(pb), pf(pb), pf(pa), pf(ans)))
    ans = 1 - pb * pb
    return QP(pre + " Find the probability that at least one ball is %s." % cols[0], ans, [pa * pa, 2 * pa * pb, pb * pb], "P(at least one %s) = 1 − P(no %s) = 1 − %s × %s = <b>%s</b>." % (cols[0], cols[0], pf(pb), pf(pb), pf(ans)))


# ------------------------------------------------------------ set 4: tree diagrams without replacement
def one_without(r):
    a, b, cols = bag(r)
    n = a + b
    pa, pb = F(a, n), F(b, n)
    p2 = [[pt(F(a - 1, n - 1)), pt(F(b, n - 1))], [pt(F(a, n - 1)), pt(F(b - 1, n - 1))]]
    pic = tree_svg([pt(pa), pt(pb)], [cols[0][0].upper(), cols[1][0].upper()], p2, label="tree diagram for two picks without replacement")
    pre = "A box has %d %s and %d %s pens. Two pens are taken at random, one after the other, without replacement.%s" % (a, cols[0], b, cols[1], pic)
    kind = r.choice(["both", "both", "diff", "same"])
    if kind == "both":
        ans = pa * F(a - 1, n - 1)
        return QP(pre + " Find the probability that both are %s." % cols[0], ans, [pa * pa, F(a - 1, n - 1), pa * F(a, n - 1)],
                  "After one %s pen is taken there are %d %s pens out of %d. %s × %s = <b>%s</b>." % (cols[0], a - 1, cols[0], n - 1, pf(pa), pf(F(a - 1, n - 1)), pf(ans)))
    if kind == "diff":
        ans = pa * F(b, n - 1) + pb * F(a, n - 1)
        return QP(pre + " Find the probability that the pens are different colours.", ans, [2 * pa * pb, pa * F(b, n - 1), 1 - pa * F(a - 1, n - 1)],
                  "%s × %s + %s × %s = <b>%s</b>." % (pf(pa), pf(F(b, n - 1)), pf(pb), pf(F(a, n - 1)), pf(ans)))
    ans = pa * F(a - 1, n - 1) + pb * F(b - 1, n - 1)
    return QP(pre + " Find the probability that both pens are the same colour.", ans, [pa * pa + pb * pb, pa * F(a - 1, n - 1), 1 - ans + F(1, n * (n - 1))],
              "Both %s or both %s: %s × %s + %s × %s = <b>%s</b>." % (cols[0], cols[1], pf(pa), pf(F(a - 1, n - 1)), pf(pb), pf(F(b - 1, n - 1)), pf(ans)))


# ------------------------------------------------------------ set 5: problems
def one_prob(r):
    kind = r.choice(["late", "late", "cards", "exam", "dice"])
    nm, he, his = P.next()
    if kind == "late":
        pr = F(r.randint(1, 4), 10)
        pl_r = F(r.randint(4, 8), 10)
        pl_n = F(r.randint(1, 3), 10)
        ans = pr * pl_r + (1 - pr) * pl_n
        q = ("The probability that it rains on a school day is %s. If it rains, the probability that %s is late is %s; if it does not rain, it is %s. "
             "Find the probability that %s is late." % (pf(pr), nm, pf(pl_r), pf(pl_n), nm))
        return QP(q, ans, [pr * pl_r, pl_r + pl_n if pl_r + pl_n <= 1 else None, pr * pl_r * (1 - pr) * pl_n], "Two paths: rain and late, or no rain and late. %s × %s + %s × %s = <b>%s</b>." % (
            pf(pr), pf(pl_r), pf(1 - pr), pf(pl_n), pf(ans)))
    if kind == "cards":
        n = r.choice([8, 10, 12])
        k = r.randint(2, n // 2)
        ans = F(k, n) * F(k - 1, n - 1)
        q = "A pack has %d cards, and %d of them are picture cards. Two cards are drawn without replacement. Find the probability that both are picture cards." % (n, k)
        return QP(q, ans, [F(k, n) ** 2, F(k, n) * F(k, n - 1), F(k - 1, n - 1)], "%s × %s = <b>%s</b>. The second fraction has one fewer card of each." % (pf(F(k, n)), pf(F(k - 1, n - 1)), pf(ans)))
    if kind == "exam":
        p1 = F(r.randint(5, 9), 10)
        p2 = F(r.randint(4, 9), 10)
        ans = p1 * (1 - p2) + (1 - p1) * p2
        q = "The probability that %s passes Paper 1 is %s and Paper 2 is %s, independently. Find the probability that %s passes exactly one paper." % (nm, pf(p1), pf(p2), he)
        return QP(q, ans, [p1 * p2, 1 - p1 * p2, p1 * (1 - p2)], "Pass 1 and fail 2, or fail 1 and pass 2: %s × %s + %s × %s = <b>%s</b>." % (pf(p1), pf(1 - p2), pf(1 - p1), pf(p2), pf(ans)))
    t = r.choice([2, 3])
    ans = 1 - F(5, 6) ** t
    q = "A fair die is rolled %d times. Find the probability of getting at least one six." % t
    return QP(q, ans, [F(t, 6), F(1, 6) ** t, F(5, 6) ** t], "P(no six) = (%s)<sup>%d</sup> = %s. P(at least one six) = 1 − %s = <b>%s</b>." % (pf(F(5, 6)), t, pf(F(5, 6) ** t), pf(F(5, 6) ** t), pf(ans)))


def build():
    sets = [S("Possibility diagrams", collect(one_space, 20, R)),
            S("Adding and multiplying probabilities", collect(one_rules, 20, R)),
            S("Tree diagrams with replacement", collect(one_with, 20, R)),
            S("Tree diagrams without replacement", collect(one_without, 20, R)),
            S("Problems", collect(one_prob, 20, R))]
    for s in sets:
        for it in s["items"]:
            for k in ("q", "e"):
                it[k] = it[k].replace("sample space diagram", "possibility diagram").replace("sample space", "possibility diagram").replace(" 1 of them give ", " 1 of them gives ")
    body = lesson(
        "<ul><li>A <b>possibility diagram</b> lists every equally likely outcome, for example the 36 outcomes for two dice.</li>"
        "<li><b>Mutually exclusive</b> events cannot happen together: P(A or B) = P(A) + P(B).</li>"
        "<li><b>Independent</b> events do not affect each other: P(A and B) = P(A) × P(B).</li>"
        "<li>On a <b>tree diagram</b>, multiply along the branches and add the results of different paths. Without replacement, the second-stage fractions have one fewer item.</li></ul>",
        [("A bag has 3 red and 2 blue balls. Two are taken without replacement. Find P(both red).", ["P(red first) = 3/5", "P(red second) = 2/4"], fr(3, 10)),
         ("A coin is tossed and a die is rolled. Find P(head and a six).", ["Independent: multiply", "½ × ⅙"], fr(1, 12))],
        ["Adding when both events must happen (multiply instead).",
         "Forgetting one of the paths, such as red then blue as well as blue then red.",
         "Keeping the same total for the second pick when the item is not replaced.",
         "Working out 'at least one' the long way and missing a case. Use 1 − P(none)."])
    faq = [("When do you add probabilities and when do you multiply?", "Add for 'or' when the events are mutually exclusive. Multiply for 'and' when the events are independent (or along the branches of a tree diagram)."),
           ("What is a possibility diagram?", "A table or list that shows every possible outcome of two events, such as two dice, so you can count the outcomes you want."),
           ("How does 'without replacement' change a tree diagram?", "After the first pick there is one fewer item in total and one fewer of the colour picked, so the second-stage probabilities change."),
           ("How do you find P(at least one)?", "Use 1 − P(none). It is usually quicker than adding all the cases with one or more.")]
    make(4, "probability-of-combined-events", 8, "S2",
         "Probability of Combined Events: Possibility and Tree Diagrams",
         "", "Probability of combined events", "",
         "Free Secondary 4 maths worksheets on probability of combined events: possibility diagrams, mutually exclusive and independent events, tree diagrams with and without replacement, and problems. 100 questions with answers.",
         "Multiply along the branches; add the paths you want.",
         "Mutually exclusive: P(A or B) = P(A) + P(B). Independent: P(A and B) = P(A) × P(B).",
         body, faq, sets, R)


if __name__ == "__main__":
    build()
