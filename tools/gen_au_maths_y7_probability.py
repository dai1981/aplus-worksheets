# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Probability (Australian Curriculum v9.0: AC9M7P01)
  python3 tools/gen_au_maths_y7_probability.py
The language and 0 to 1 scale of chance, sample spaces for single-stage events, probabilities of single events,
complementary events, predicting relative frequencies, and comparing experimental results with predictions.
Wrong answers come from real mistakes: writing a ratio instead of a probability, using the wrong total,
forgetting that probabilities add to 1, and thinking a coin is "due" a tail.
"""
import random
from fractions import Fraction as F
from math import gcd
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, fr, frac, table, People

R = random.Random(72101)
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
    ("rolling a 7 on an ordinary die", "Impossible", "0"),
    ("the sun rising tomorrow", "Certain", "1"),
    ("getting heads when you flip a fair coin", "Even chance", "0.5"),
    ("rolling a number less than 7 on an ordinary die", "Certain", "1"),
    ("picking a red card from a normal pack of cards", "Even chance", "0.5"),
    ("rolling a 6 on an ordinary die", "Unlikely", "1/6"),
    ("rolling a number greater than 1 on an ordinary die", "Likely", "5/6"),
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
        q = "A fair six-sided die is rolled. What is the probability of getting %s?" % B(ev)
        e = "%d of the 6 outcomes work, so P = %s%s." % (n, fr(n, 6), " = <b>%s</b>" % pf(ans) if ans.denominator != 6 else "")
        if ans.denominator == 6:
            e = "%d of the 6 outcomes work, so P = <b>%s</b>." % (n, pf(ans))
        return QP(q, ans, [F(1, n) if n > 1 else F(1, 2), F(n, 10), "%d : %d" % (n, 6 - n)], e)
    if kind == "spinner":
        n = r.choice([5, 8, 10])
        k = r.randint(1, n - 1)
        col = r.choice(["red", "blue", "green"])
        ans = F(k, n)
        q = "A fair spinner has %d equal sections. %d of them %s %s. What is the probability of landing on %s?" % (n, k, "is" if k == 1 else "are", col, B(col))
        e = "%d out of %d equal sections: <b>%s</b>." % (k, n, pf(ans))
        return QP(q, ans, [F(1, k) if k > 1 else F(1, 2), "%d : %d" % (k, n - k), F(n - k, n)], e)
    evs = [("a heart", F(13, 52)), ("a king", F(4, 52)), ("a red card", F(26, 52)), ("the ace of spades", F(1, 52)), ("a picture card (jack, queen or king)", F(12, 52))]
    ev, ans = r.choice(evs)
    q = "A card is picked at random from a normal pack of 52 cards. What is the probability it is %s?" % B(ev)
    e = "There %s %d such card%s out of 52: %s = <b>%s</b>." % ("is" if ans * 52 == 1 else "are", ans * 52, "" if ans * 52 == 1 else "s", fr(int(ans * 52), 52), pf(ans))
    if ans * 52 == 1:
        e = "There is only 1 such card out of 52: <b>%s</b>." % pf(ans)
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


# ------------------------------------------------------------ set 4: sample spaces and predicted frequencies
WORDS = ["AUSTRALIA", "KANGAROO", "BRISBANE", "PROBABILITY", "MATHEMATICS", "ADELAIDE", "WOMBAT", "PLATYPUS"]


def one_space(r):
    kind = r.randint(0, 3)
    if kind == 0:
        n = r.choice([4, 5, 6, 8, 10, 12])
        q = "A spinner is numbered 1 to %d. What is the sample space?" % n
        right = "{" + ", ".join(str(i) for i in range(1, n + 1)) + "}"
        wr = ["{" + ", ".join(str(i) for i in range(0, n + 1)) + "}", "{" + ", ".join(str(i) for i in range(1, n)) + "}", "{%d}" % n]
        return T(q, right, wr, "The sample space lists every possible outcome: <b>%s</b>." % right)
    if kind == 1:
        w = r.choice(WORDS)
        letter = r.choice(sorted(set(w)))
        c = w.count(letter)
        ans = F(c, len(w))
        q = "The letters of the word %s are written on cards and one card is picked at random. What is P(%s)?" % (B(w), letter)
        e = "There are %d letters and %d %s%s: <b>%s</b>." % (len(w), c, letter, "s" if c > 1 else "", pf(ans))
        return QP(q, ans, [F(1, len(set(w))), F(c, len(w) - c) if len(w) - c > c else None, F(1, len(w)) if c > 1 else F(2, len(w))], e)
    if kind == 2:
        n = r.choice([60, 120, 300, 600, 90, 240])
        ev, p = r.choice([("a 6", F(1, 6)), ("an even number", F(1, 2)), ("a number greater than 4", F(1, 3)), ("a 1 or a 2", F(1, 3))])
        ans = n * p
        q = "A fair six-sided die is rolled %d times. How many times would you expect to get %s?" % (n, B(ev))
        e = "Expected number = probability × number of trials = %s × %d = <b>%s</b>." % (pf(p), n, num(ans))
        return QN(q, ans, [n // 6 if p != F(1, 6) else n // 2, F(n, 2) if p != F(1, 2) else F(n, 3), n * p / 2], e)
    n = r.choice([50, 80, 100, 200, 400])
    k, tot = r.choice([(1, 4), (3, 4), (2, 5), (1, 5), (3, 10), (1, 8)])
    col = r.choice(["red", "blue", "green", "yellow"])
    ans = F(n * k, tot)
    if ans.denominator != 1:
        return None
    q = "A fair spinner has %d equal sections and %d %s %s. It is spun %d times. About how many times would you expect %s?" % (
        tot, k, "is" if k == 1 else "are", col, n, col)
    return QN(q, ans, [k * n // 10 if k * n // 10 != ans else ans + 5, n - ans, F(n, tot)], "P(%s) = %s, so expect %s × %d = <b>%s</b> times." % (col, pf(F(k, tot)), pf(F(k, tot)), n, num(ans)))


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
        ("A spinner landed on red 30 times out of 200 spins. How many reds would you expect in 1000 spins?", "150", ["300", "30", "130"], "0.15 × 1000 = <b>150</b>."),
        ("Cooper says, “I rolled a die 6 times and never got a 6, so the die is unfair.” Is he right?", "No, 6 rolls is not enough to tell", ["Yes, it must be unfair", "Yes, he should get exactly one 6", "No, a 6 is impossible"],
         "With only 6 rolls, results vary a lot. <b>Many more trials</b> are needed to judge whether a die is fair."),
        ("Which estimate of the probability of heads is most reliable?", "520 heads in 1000 flips", ["6 heads in 10 flips", "2 heads in 3 flips", "26 heads in 50 flips"],
         "More trials give a more reliable estimate: <b>520 heads in 1000 flips</b>."),
        ("The probability of winning a game is 0.35. Zara plays 40 times. How many times should she expect to win?", "14", ["35", "26", "4"], "0.35 × 40 = <b>14</b>."),
        ("A bag has red and blue sweets only. P(red) = 3/8. There are 24 sweets. How many are blue?", "15", ["9", "8", "16"], "Red = 3/8 × 24 = 9, so blue = 24 − 9 = <b>15</b>."),
        ("A bag has 5 red and some blue counters. P(red) = 1/4. How many blue counters are there?", "15", ["20", "4", "1"], "If 5 is a quarter, there are 20 counters in total, so 20 − 5 = <b>15</b> blue."),
        ("The letters of the word MATHEMATICS are put in a bag. One is taken at random. What is P(M)?", fr(2, 11), [fr(1, 11), fr(2, 9), fr(1, 2)], "There are 11 letters and 2 Ms: <b>2/11</b>.".replace("2/11", fr(2, 11))),
        ("A fair spinner has numbers 1 to 5. What is the probability of NOT getting a 2?", fr(4, 5), [fr(1, 5), fr(2, 5), fr(3, 5)], "4 of the 5 numbers are not 2: <b>4/5</b>.".replace("4/5", fr(4, 5))),
        ("Which of these cannot be a probability?", "1.2", ["0.95", fr(7, 8), "0"], "Probabilities are between 0 and 1. <b>1.2</b> is more than 1."),
        ("In a class of 30, 12 students have a pet. A student is picked at random. What is the probability they do not have a pet?", fr(3, 5), [fr(2, 5), fr(12, 30), fr(1, 2)], "18 out of 30 have no pet: 18/30 = <b>3/5</b>.".replace("3/5", fr(3, 5))),
        ("P(snow) = 0.08. What is the probability of no snow, as a percentage?", "92%", ["8%", "0.92%", "20%"], "1 − 0.08 = 0.92 = <b>92%</b>."),
        ("A weather app says the chance of rain is 70%. Which statement is correct?", "Rain is likely but not certain", ["It will definitely rain", "It will rain for 70% of the day", "Rain is unlikely"], "70% is closer to 1 than to 0: <b>rain is likely but not certain</b>."),
        ("A fair coin has landed on heads 5 times in a row. What is the probability of heads next time?", fr(1, 2), ["Less than 1/2", "More than 1/2", "0"], "A coin has no memory. Each flip is still <b>1/2</b>.".replace("1/2</b>", fr(1, 2) + "</b>")),
        ("A die is thrown 120 times. Which result is closest to what you would expect?", "About 20 sixes", ["Exactly 20 sixes", "About 60 sixes", "No sixes"], "1/6 × 120 = 20, but real results vary, so <b>about 20 sixes</b>."),
        ("Ruby picks a sock from a drawer with 4 black, 3 white and 5 grey socks. Which colour is she least likely to pick?", "White", ["Black", "Grey", "They are equally likely"], "White has the fewest (3 out of 12): <b>white</b>."),
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
         ("A die is rolled 300 times. How many 6s would you expect?", ["1/6 × 300."], "50")],
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
    make(7, "probability", 21, "AC9M7P01",
         "Probability: Chance, Sample Spaces and Relative Frequency",
         "Year 7 Probability Worksheets: Probability Scale, Sample Spaces, Single Events and Experiments (Free, Answer Key)",
         "Probability",
         "identify the sample space for single-stage events; assign probabilities to the outcomes of these events and predict relative frequencies for related events",
         "Free Year 7 maths worksheets on probability for the Australian Curriculum (AC9M7P01): the 0 to 1 scale, sample spaces, "
         "probabilities of single events, complementary events, expected frequencies and experiments. 100 questions with an answer key.",
         "P(event) = favourable outcomes ÷ total outcomes, from 0 (impossible) to 1 (certain).",
         "Expected number = probability × number of trials. P(not A) = 1 − P(A).",
         body(),
         [("What is the probability scale?", "A line from 0 to 1. 0 means impossible, 0.5 means an even chance and 1 means certain."),
          ("How do I find the probability of something not happening?", "Subtract the probability that it happens from 1. If P(rain) = 0.3, then P(no rain) = 0.7."),
          ("What is relative frequency?", "The fraction of trials in which something happened in an experiment. It is an estimate of the probability, and more trials give a better estimate."),
          ("What is a sample space?", "The list of every possible outcome. For a six-sided die it is {1, 2, 3, 4, 5, 6}.")],
         sets, R)


if __name__ == "__main__":
    main()
