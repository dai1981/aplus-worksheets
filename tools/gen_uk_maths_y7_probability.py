# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Probability (KS3 Probability)
  python3 tools/gen_uk_maths_y7_probability.py
The probability scale, probabilities of single events as fractions, decimals and percentages,
P(not A) = 1 − P(A), sample spaces for two events, expected outcomes and relative frequency.
Wrong answers come from real mistakes: writing odds (3 : 5) instead of a probability, using the wrong total,
forgetting that probabilities add to 1, and counting 2 + 5 and 5 + 2 as one outcome.
"""
import random
from fractions import Fraction as F
from math import gcd
from uk_ks3 import num, mcq, B, S, make, lesson, collect, QN, T, fr, frac, table, People

R = random.Random(72001)
P = People(R)


def pf(v):
    v = F(v)
    if v == 0:
        return "0"
    if v == 1:
        return "1"
    return fr(v.numerator, v.denominator)


def QP(q, ans, wrongs, e):
    ans = F(ans)
    cands = []
    for w in wrongs:
        if w is None:
            continue
        if isinstance(w, str):
            cands.append((w, w))
        elif 0 <= F(w) <= 1 or True:
            cands.append((pf(w), pf(w)))
    for d in (F(1, ans.denominator or 1),):
        if 0 < ans + d <= 1:
            cands.append((pf(ans + d), pf(ans + d)))
        if 0 <= ans - d:
            cands.append((pf(ans - d), pf(ans - d)))
    cands.append((pf(1 - ans), pf(1 - ans)))
    return mcq(q, (pf(ans), pf(ans)), cands, e)


# ------------------------------------------------------------ set 1: probability scale
EVENTS = [
    ("rolling a 7 on an ordinary dice", "Impossible", "0"),
    ("the sun rising tomorrow", "Certain", "1"),
    ("getting heads when you flip a fair coin", "Even chance", "0.5"),
    ("rolling a number less than 7 on an ordinary dice", "Certain", "1"),
    ("picking a red card from a normal pack of cards", "Even chance", "0.5"),
    ("rolling a 6 on an ordinary dice", "Unlikely", "1/6"),
    ("rolling a number greater than 1 on an ordinary dice", "Likely", "5/6"),
    ("picking a blue ball from a bag of 9 red balls and 1 blue ball", "Unlikely", "0.1"),
    ("picking a red ball from a bag of 9 red balls and 1 blue ball", "Likely", "0.9"),
    ("picking a green ball from a bag of only red balls", "Impossible", "0"),
    ("a fair spinner with 4 equal sections numbered 1 to 4 landing on an even number", "Even chance", "0.5"),
    ("it being Monday the day after a Sunday", "Certain", "1"),
]


def one_scale(r):
    ev, word, val = r.choice(EVENTS)
    words = ["Impossible", "Unlikely", "Even chance", "Likely", "Certain"]
    if r.random() < 0.6:
        q = "How likely is %s?" % B(ev)
        return T(q, word, [w for w in words if w != word][:3] if word != "Impossible" else ["Unlikely", "Even chance", "Certain"],
                 "%s: <b>%s</b>." % (ev[0].upper() + ev[1:], word.lower()))
    if val in ("0", "1", "0.5"):
        wr = [x for x in ["0", "0.5", "1", "2", "−1"] if x != val][:3]
    else:
        wr = ["0", "1", "0.5"] if val not in ("0.9",) else ["0.1", "0", "9"]
    sval = val if "/" not in val else fr(*val.split("/"))
    q = "Which number best describes the probability of %s?" % B(ev)
    e = "Probabilities go from 0 (impossible) to 1 (certain). %s: <b>%s</b>." % (ev[0].upper() + ev[1:], sval)
    return T(q, sval, wr, e)


# ------------------------------------------------------------ set 2: single events
def one_single(r):
    kind = r.choice(["bag", "bag", "dice", "spinner", "cards"])
    if kind == "bag":
        cols = r.sample(["red", "blue", "green", "yellow", "white"], 3)
        ns = [r.randint(2, 9) for _ in cols]
        k = r.randrange(3)
        tot = sum(ns)
        ans = F(ns[k], tot)
        q = "A bag has %s counters. One counter is taken at random. What is the probability it is %s?" % (
            ", ".join("%d %s" % (n, c) for n, c in zip(ns[:-1], cols[:-1])) + " and %d %s" % (ns[-1], cols[-1]), B(cols[k]))
        e = "There are %d counters and %d are %s: P(%s) = %s%s." % (tot, ns[k], cols[k], cols[k], fr(ns[k], tot),
                                                                   " = <b>%s</b>" % pf(ans) if gcd(ns[k], tot) > 1 else "" if True else "")
        if gcd(ns[k], tot) == 1:
            e = "There are %d counters and %d are %s: P(%s) = <b>%s</b>." % (tot, ns[k], cols[k], cols[k], pf(ans))
        odds = "%d : %d" % (ns[k], tot - ns[k])
        wrong_total = F(ns[k], tot - ns[k]) if tot - ns[k] > ns[k] else None
        return QP(q, ans, [odds, wrong_total, F(1, 3), F(ns[k], 10) if tot != 10 else None], e)
    if kind == "dice":
        evs = [("an even number", 3), ("a number greater than 4", 2), ("a 3", 1), ("a prime number", 3), ("a multiple of 3", 2),
               ("a number less than 3", 2), ("a square number", 2), ("a factor of 6", 4)]
        ev, n = r.choice(evs)
        ans = F(n, 6)
        q = "A fair six-sided dice is rolled. What is the probability of getting %s?" % B(ev)
        e = "%d of the 6 outcomes work, so P = %s%s." % (n, fr(n, 6), " = <b>%s</b>" % pf(ans) if ans.denominator != 6 else "")
        if ans.denominator == 6:
            e = "%d of the 6 outcomes work, so P = <b>%s</b>." % (n, pf(ans))
        return QP(q, ans, [F(1, n) if n > 1 else F(1, 2), F(n, 10), "%d : %d" % (n, 6 - n)], e)
    if kind == "spinner":
        n = r.choice([5, 8, 10])
        k = r.randint(1, n - 1)
        col = r.choice(["red", "blue", "green"])
        ans = F(k, n)
        q = "A fair spinner has %d equal sections. %d of them are %s. What is the probability of landing on %s?" % (n, k, col, B(col))
        e = "%d out of %d equal sections: <b>%s</b>." % (k, n, pf(ans))
        return QP(q, ans, [F(1, k) if k > 1 else F(1, 2), "%d : %d" % (k, n - k), F(n - k, n)], e)
    evs = [("a heart", F(13, 52)), ("a king", F(4, 52)), ("a red card", F(26, 52)), ("the ace of spades", F(1, 52)), ("a picture card (jack, queen or king)", F(12, 52))]
    ev, ans = r.choice(evs)
    q = "A card is picked at random from a normal pack of 52 cards. What is the probability it is %s?" % B(ev)
    e = "There are %d such cards out of 52: %s = <b>%s</b>." % (ans * 52, fr(int(ans * 52), 52), pf(ans))
    return QP(q, ans, [F(1, 4) if ans != F(1, 4) else F(1, 13), F(1, 52) if ans != F(1, 52) else F(1, 4), F(int(ans * 52), 100)], e)


# ------------------------------------------------------------ set 3: not happening, decimals and percentages
def one_not(r):
    kind = r.randint(0, 2)
    if kind == 0:
        p = F(r.randint(1, 19), 20) if r.random() < 0.5 else F(r.randint(1, 9), 10)
        q = "The probability that it rains tomorrow is %s. What is the probability that it does %s rain?" % (B(num(p)), B("not"))
        e = "The probabilities add up to 1: 1 − %s = <b>%s</b>." % (num(p), num(1 - p))
        return QN(q, 1 - p, [p, 100 - p * 100 if False else F(1) - p + F(1, 10), -p if False else p + F(1, 10)], e)
    if kind == 1:
        pc = r.choice([15, 25, 35, 40, 62, 73, 8])
        q = "The probability of a train being late is %d%%. What is the probability it is %s late?" % (pc, B("not"))
        right = "%d%%" % (100 - pc)
        return T(q, right, ["%d%%" % pc, "%d%%" % (100 - pc + 10), "%s%%" % num(F(100, pc)) if F(100, pc).denominator == 1 else "%d%%" % (pc + 50)],
                 "100%% − %d%% = <b>%s</b>." % (pc, right))
    a, b = F(r.randint(1, 4), 10), F(r.randint(1, 4), 10)
    c = 1 - a - b
    if c <= 0:
        return None
    q = "A spinner can land on red, blue or green. P(red) = %s and P(blue) = %s. What is P(green)?" % (num(a), num(b))
    e = "All the probabilities add up to 1: 1 − %s − %s = <b>%s</b>." % (num(a), num(b), num(c))
    return QN(q, c, [a + b, 1 - a, F(1, 3)], e, near=(F(1, 10), F(-1, 10)))


# ------------------------------------------------------------ set 4: sample spaces and expected outcomes
def one_space(r):
    kind = r.randint(0, 3)
    if kind == 0:
        tgt = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == tgt)
        ans = F(ways, 36)
        q = "Two fair dice are rolled and the scores are added. What is the probability of a total of %s?" % B(str(tgt))
        pairs = ", ".join("(%d, %d)" % (a, b) for a in range(1, 7) for b in range(1, 7) if a + b == tgt)
        e = "There are 36 outcomes. A total of %d comes from %s: %d way%s, so P = %s." % (
            tgt, pairs, ways, "" if ways == 1 else "s", fr(ways, 36) if ans.denominator == 36 else fr(ways, 36) + " = " + pf(ans))
        e = e[:-1].rsplit("= ", 1)[0] + "= <b>%s</b>." % pf(ans)
        return QP(q, ans, [F(1, 11), F(ways, 12), F((ways + 1) // 2 if ways > 1 else 1, 21)], e)
    if kind == 1:
        q = "A coin is flipped and a fair dice is rolled. How many possible outcomes are there?"
        return QN(q, 12, [8, 6, 2], "2 outcomes for the coin × 6 for the dice = <b>12</b>.")
    if kind == 2:
        n = r.choice([60, 120, 300, 600])
        ev, p = r.choice([("a 6", F(1, 6)), ("an even number", F(1, 2)), ("a number greater than 4", F(1, 3))])
        ans = n * p
        q = "A fair dice is rolled %d times. How many times would you expect to get %s?" % (n, B(ev))
        e = "Expected number = probability × number of trials = %s × %d = <b>%s</b>." % (pf(p), n, num(ans))
        return QN(q, ans, [n // 6 if p != F(1, 6) else n // 2, F(n, 2) if p != F(1, 2) else F(n, 3), n * p / 2], e)
    flips = r.choice([3, 2])
    if flips == 2:
        q = "Two coins are flipped. What is the probability of getting one head and one tail?"
        return QP(q, F(1, 2), [F(1, 3), F(1, 4), F(2, 3)], "Outcomes: HH, HT, TH, TT. Two of the four work (HT and TH): <b>1/2</b>.".replace("1/2", pf(F(1, 2))))
    q = "Three coins are flipped. What is the probability of getting three heads?"
    return QP(q, F(1, 8), [F(1, 3), F(1, 6), F(3, 8)], "There are 2 × 2 × 2 = 8 outcomes and only HHH works: <b>%s</b>." % pf(F(1, 8)))


# ------------------------------------------------------------ set 5: experiments and problems
def problems():
    its = []
    for heads, n in [(18, 50), (34, 80), (27, 60), (45, 100)]:
        rf = F(heads, n)
        q = "A coin is flipped %d times and lands on heads %d times. What is the relative frequency of heads?" % (n, heads)
        e = "Relative frequency = %d ÷ %d = <b>%s</b>." % (heads, n, num(rf))
        its.append(QN(q, rf, [F(heads, 100) if n != 100 else F(heads, 50), F(1, 2), F(n - heads, n)], e, near=(F(1, 10), F(-1, 10))))
    data = [
        ("A spinner landed on red 30 times out of 200 spins. Estimate the probability of red.", "0.15", ["0.3", "30", "0.85"], "30 ÷ 200 = <b>0.15</b>."),
        ("A spinner landed on red 30 times out of 200 spins. How many reds would you expect in 1,000 spins?", "150", ["300", "30", "130"], "0.15 × 1,000 = <b>150</b>."),
        ("Mo says, “I rolled a dice 6 times and never got a 6, so the dice is unfair.” Is he right?", "No, 6 rolls is not enough to tell", ["Yes, it must be unfair", "Yes, he should get exactly one 6", "No, a 6 is impossible"],
         "With only 6 rolls, results vary a lot. <b>Many more trials</b> are needed to judge whether a dice is fair."),
        ("Which estimate of the probability of heads is most reliable?", "520 heads in 1,000 flips", ["6 heads in 10 flips", "2 heads in 3 flips", "26 heads in 50 flips"],
         "More trials give a more reliable estimate: <b>520 heads in 1,000 flips</b>."),
        ("The probability of winning a game is 0.35. Kai plays 40 times. How many times should he expect to win?", "14", ["35", "26", "4"], "0.35 × 40 = <b>14</b>."),
        ("A bag has red and blue sweets only. P(red) = 3/8. There are 24 sweets. How many are blue?", "15", ["9", "8", "16"], "Red = 3/8 × 24 = 9, so blue = 24 − 9 = <b>15</b>."),
        ("A bag has 5 red and some blue counters. P(red) = 1/4. How many blue counters are there?", "15", ["20", "4", "1"], "If 5 is a quarter, there are 20 counters in total, so 20 − 5 = <b>15</b> blue."),
        ("The letters of the word MATHEMATICS are put in a bag. One is taken at random. What is P(M)?", fr(2, 11), [fr(1, 11), fr(2, 9), fr(1, 2)], "There are 11 letters and 2 Ms: <b>2/11</b>.".replace("2/11", fr(2, 11))),
        ("A fair spinner has numbers 1 to 5. What is the probability of NOT getting a 2?", fr(4, 5), [fr(1, 5), fr(2, 5), fr(3, 5)], "4 of the 5 numbers are not 2: <b>4/5</b>.".replace("4/5", fr(4, 5))),
        ("Which of these cannot be a probability?", "1.2", ["0.95", fr(7, 8), "0"], "Probabilities are between 0 and 1. <b>1.2</b> is more than 1."),
        ("In a class of 30, 12 pupils have a pet. A pupil is picked at random. What is the probability they do not have a pet?", fr(3, 5), [fr(2, 5), fr(12, 30), fr(1, 2)], "18 out of 30 have no pet: 18/30 = <b>3/5</b>.".replace("3/5", fr(3, 5))),
        ("P(snow) = 0.08. What is the probability of no snow, as a percentage?", "92%", ["8%", "0.92%", "20%"], "1 − 0.08 = 0.92 = <b>92%</b>."),
        ("Two fair dice are rolled. What is the most likely total?", "7", ["12", "6", "All totals are equally likely"], "7 can be made in 6 ways, more than any other total: <b>7</b>."),
        ("A fair coin has landed on heads 5 times in a row. What is the probability of heads next time?", fr(1, 2), ["Less than 1/2", "More than 1/2", "0"], "A coin has no memory. Each flip is still <b>1/2</b>.".replace("1/2</b>", fr(1, 2) + "</b>")),
        ("A dice is thrown 120 times. Which result is closest to what you would expect?", "About 20 sixes", ["Exactly 20 sixes", "About 60 sixes", "No sixes"], "1/6 × 120 = 20, but real results vary, so <b>about 20 sixes</b>."),
        ("Ella picks a sock from a drawer with 4 black, 3 white and 5 grey socks. Which colour is she least likely to pick?", "White", ["Black", "Grey", "They are equally likely"], "White has the fewest (3 out of 12): <b>white</b>."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    return its


def body():
    return lesson(
        "<p>Probability measures how likely something is, from <b>0</b> (impossible) to <b>1</b> (certain). "
        "Write it as a fraction, decimal or percentage.</p>"
        "<p>When all outcomes are equally likely: P(event) = number of ways it can happen ÷ total number of outcomes. "
        "The probability of something <b>not</b> happening is 1 − P(it happens).</p>"
        "<p>From an experiment, the <b>relative frequency</b> = number of times it happened ÷ number of trials.</p>",
        [("A bag has 3 red and 5 blue counters. Find P(red).", ["8 counters, 3 are red."], "3/8"),
         ("P(late) = 0.15. Find P(not late).", ["1 − 0.15."], "0.85"),
         ("A dice is rolled 300 times. How many 6s would you expect?", ["1/6 × 300."], "50")],
        ["Writing a ratio such as 3 : 5 instead of a probability. It should be 3/8.",
         "Using the wrong total: with 3 red and 5 blue, the total is 8, not 5.",
         "Forgetting that all the probabilities add up to 1.",
         "Thinking a coin “is due” a tail after several heads. Each flip is independent."])


def main():
    sets = [S("The probability scale", collect(one_scale, 20, R)),
            S("Probability of a single event", collect(one_single, 20, R)),
            S("Probability of not happening", collect(one_not, 20, R)),
            S("Sample spaces and expected outcomes", collect(one_space, 20, R)),
            S("Experiments and problems", problems())]
    make(7, "probability", 20, "P",
         "Probability: The Probability Scale, Single Events and Experiments",
         "Year 7 Probability Worksheets: Probability Scale, P(not A), Sample Spaces and Relative Frequency",
         "Probability",
         "Record, describe and analyse the frequency of outcomes of simple probability experiments involving randomness, "
         "fairness, equally and unequally likely outcomes, using appropriate language and the 0-1 probability scale; "
         "understand that the probabilities of all possible outcomes sum to 1; enumerate sets and unions/intersections of "
         "sets systematically, using tables, grids and Venn diagrams; generate theoretical sample spaces for single and "
         "combined events with equally likely, mutually exclusive outcomes and use these to calculate theoretical probabilities.",
         "Free Year 7 probability worksheets: the 0 to 1 probability scale, probabilities of single events, P(not A), "
         "sample spaces for dice and coins, expected outcomes and relative frequency. 100 questions with answers.",
         "P(event) = ways it can happen ÷ total outcomes. Probabilities go from 0 to 1.",
         "P(not A) = 1 − P(A). Expected number = probability × number of trials.",
         body(),
         [("What is the probability scale?", "A line from 0 to 1. 0 means impossible, 0.5 means an even chance and 1 means certain."),
          ("How do I find the probability of something not happening?", "Subtract the probability that it happens from 1. If P(rain) = 0.3, then P(no rain) = 0.7."),
          ("What is relative frequency?", "The fraction of trials in which something happened in an experiment. It is an estimate of the probability, and more trials give a better estimate."),
          ("How many outcomes are there when two dice are rolled?", "6 × 6 = 36. A sample space grid helps you count them.")],
         sets, R)


if __name__ == "__main__":
    main()
