# -*- coding: utf-8 -*-
"""
India Class 10 Maths, NCERT Chapter 14: Probability (CBSE Unit VII Statistics and Probability)
  python3 tools/gen_in_maths_c10_probability.py
Classical probability P(E) = favourable outcomes ÷ total outcomes, sure and impossible events, complementary events
P(not E) = 1 − P(E), dice, coins and numbered discs, bags of balls and defective items, a well-shuffled deck of 52
playing cards, two coins and two dice, and problems.
Wrong answers come from real mistakes: favourable ÷ unfavourable, counting 4 kings and 4 hearts as 8 (king of hearts twice),
11 outcomes for the sum of two dice, 1 + P(E), and treating “at least one” as “exactly one”.
"""
import random, math
from fractions import Fraction as F
from in_common import num, S, make, lesson, mix, T, fv, People

R = random.Random(910014)
P = People(R)


def pf(v):
    v = F(v)
    return "%d/%d" % (v.numerator, v.denominator) if v.denominator != 1 else str(v.numerator)


def Tp(q, ans, wr, e):
    ws = []
    for w in wr:
        w = F(w)
        if w != ans and 0 <= w <= 1 and pf(w) not in ws:
            ws.append(pf(w))
    for extra in (1 - ans, ans / 2, F(1, 2), F(1, 4), F(1, 3)):
        if len(ws) >= 3:
            break
        if extra != ans and pf(extra) not in ws and 0 <= extra <= 1:
            ws.append(pf(extra))
    return T(q, pf(ans), ws[:3], e)


# ---------------------------------------------------------------- set 1: concepts
CONC = [
    ("The probability of an event that is certain to happen is", "1", ["0", "1/2", "−1"], "A sure event has probability 1."),
    ("The probability of an impossible event is", "0", ["1", "1/2", "−1"], "An impossible event has probability 0."),
    ("Which of these cannot be the probability of an event?", "−1.5", ["2/3", "0.7", "15%"], "Probabilities lie between 0 and 1, so −1.5 is impossible."),
    ("Which of these numbers cannot be a probability?", "1.2", ["0", "0.35", "1"], "A probability is never more than 1."),
    ("The sum of the probabilities of all the elementary events of an experiment is", "1", ["0", "1/2", "the number of outcomes"], "All the elementary events together are certain to happen."),
    ("If P(E) = 0.05, what is P(not E)?", "0.95", ["0.05", "1.05", "0.5"], "P(not E) = 1 − 0.05."),
    ("If P(E) = 0.62, what is P(not E)?", "0.38", ["0.62", "1.62", "0.48"], "P(not E) = 1 − 0.62."),
    ("If P(E) = 3/8, what is P(not E)?", "5/8", ["3/8", "8/3", "11/8"], "P(not E) = 1 − 3/8."),
    ("A player says: “A coin has two outcomes, so the probability of a head is 1/2.” Is this correct, and why?", "Yes, because the two outcomes are equally likely",
     ["No, because the coin can land on its edge", "Yes, because every event has probability 1/2", "No, because it depends on the last toss"], "The classical definition needs equally likely outcomes, which a fair coin gives."),
    ("A student says: “When I throw a die, I either get a 6 or not, so P(6) = 1/2.” Is this correct?", "No, because the two outcomes are not equally likely",
     ["Yes, there are two outcomes", "Yes, a die is fair", "No, because P(6) = 1/6 only on the first throw"], "“6” and “not 6” are not equally likely: P(6) = 1/6."),
    ("An event that has only one outcome of the experiment is called", "an elementary event", ["a sure event", "an impossible event", "a complementary event"], "An elementary event has exactly one outcome."),
    ("If E and not E are complementary events, P(E) + P(not E) =", "1", ["0", "1/2", "2"], "Complementary events together make a sure event."),
]


def one_conc(r):
    q, a, w, e = r.choice(CONC)
    return T(q if q.endswith("?") else q + " ___.", a, w, e + " <b>%s</b>." % a)


# ---------------------------------------------------------------- set 2: dice, coins and numbered discs
def one_die(r):
    kind = r.choice(["die", "die", "die", "disc", "disc"])
    if kind == "die":
        ev = r.choice([("a prime number", [2, 3, 5]), ("an even number", [2, 4, 6]), ("a number greater than 4", [5, 6]), ("a number less than 3", [1, 2]),
                       ("a multiple of 3", [3, 6]), ("a number between 2 and 6", [3, 4, 5]), ("8", []), ("a number less than 7", [1, 2, 3, 4, 5, 6]), ("a factor of 6", [1, 2, 3, 6])])
        p = F(len(ev[1]), 6)
        return Tp("A die is thrown once. What is the probability of getting %s?" % ev[0], p, [F(len(ev[1]), 6 - len(ev[1])) if len(ev[1]) < 6 else F(1, 6), F(1, 6), 1 - p],
                  "Outcomes: 1 to 6. Favourable: %s. P = %d/6 = <b>%s</b>." % (", ".join(map(str, ev[1])) or "none", len(ev[1]), pf(p)))
    n = r.choice([20, 25, 30, 50, 90, 100])
    ev = r.choice(["prime", "square", "even", "mult5", "two-digit"])
    nums = range(1, n + 1)
    if ev == "prime":
        fav = [k for k in nums if k > 1 and all(k % d for d in range(2, int(k ** 0.5) + 1))]
        txt = "a prime number"
    elif ev == "square":
        fav = [k for k in nums if int(math.isqrt(k)) ** 2 == k]
        txt = "a perfect square"
    elif ev == "even":
        fav = [k for k in nums if k % 2 == 0]
        txt = "an even number"
    elif ev == "mult5":
        fav = [k for k in nums if k % 5 == 0]
        txt = "a multiple of 5"
    else:
        fav = [k for k in nums if 10 <= k <= 99]
        txt = "a two-digit number"
    p = F(len(fav), n)
    return Tp("A box has %d discs numbered 1 to %d. One disc is drawn at random. Find the probability that it shows %s." % (n, n, txt), p,
              [F(len(fav), n - len(fav)) if n > len(fav) else F(1, n), 1 - p, F(len(fav) + 1, n)],
              "There are %d such numbers out of %d. P = <b>%s</b>." % (len(fav), n, pf(p)))


# ---------------------------------------------------------------- set 3: bags, items, people
def one_bag(r):
    kind = r.choice(["balls", "balls", "balls", "bulbs", "pens"])
    if kind == "balls":
        cols = r.sample(["red", "blue", "green", "white", "black", "yellow"], 3)
        ns = [r.randint(2, 12) for _ in cols]
        t = sum(ns)
        want = r.choice(["one", "not", "either"])
        desc = ", ".join("%d %s" % (n, c) for n, c in zip(ns[:-1], cols[:-1])) + " and %d %s" % (ns[-1], cols[-1])
        if want == "one":
            p = F(ns[0], t)
            return Tp("A bag contains %s balls. One ball is drawn at random. What is the probability that it is %s?" % (desc, cols[0]), p,
                      [F(ns[0], t - ns[0]), F(1, 3), F(ns[0] + 1, t)], "%d %s out of %d balls: P = <b>%s</b>." % (ns[0], cols[0], t, pf(p)))
        if want == "not":
            p = F(t - ns[1], t)
            return Tp("A bag contains %s balls. One ball is drawn at random. What is the probability that it is not %s?" % (desc, cols[1]), p,
                      [F(ns[1], t), F(t - ns[1], ns[1]) if t - ns[1] < ns[1] else F(ns[0], t), F(2, 3)], "P(not %s) = 1 − %d/%d = <b>%s</b>." % (cols[1], ns[1], t, pf(p)))
        p = F(ns[0] + ns[2], t)
        return Tp("A bag contains %s balls. One ball is drawn at random. What is the probability that it is %s or %s?" % (desc, cols[0], cols[2]), p,
                  [F(ns[0] * ns[2], t * t), F(ns[0], t), F(2, 3)], "(%d + %d)/%d = <b>%s</b>." % (ns[0], ns[2], t, pf(p)))
    if kind == "bulbs":
        t = r.choice([20, 24, 25, 40, 50, 100, 144])
        d = r.randint(2, t // 4)
        p = F(t - d, t)
        return Tp("A lot of %d bulbs contains %d defective ones. One bulb is drawn at random. What is the probability that it is not defective?" % (t, d), p,
                  [F(d, t), F(t - d, d) if t - d < d else F(d, t - d), F(t - d - 1, t)], "Good bulbs: %d − %d = %d. P = %d/%d = <b>%s</b>." % (t, d, t - d, t - d, t, pf(p)))
    t = r.choice([96, 132, 144, 120, 60])
    d = r.choice([12, 6, 8, 10])
    p = F(t, t + d)
    name, he, his = P.next()
    return Tp("%d good pens are mixed with %d defective pens. %s takes out one pen at random. What is the probability that %s can buy it (it is good)?" % (t, d, name, he), p,
              [F(d, t + d), F(t, d) if t < d else F(d, t), F(t - d, t + d)], "Good pens %d out of %d. P = <b>%s</b>." % (t, t + d, pf(p)))


# ---------------------------------------------------------------- set 4: playing cards
CARDS = [
    ("a king", 4), ("a red card", 26), ("a face card", 12), ("a spade", 13), ("the queen of diamonds", 1), ("an ace", 4),
    ("a red face card", 6), ("a black king", 2), ("the jack of hearts", 1), ("a card that is not a face card", 40),
    ("a red queen", 2), ("a black card", 26), ("a club", 13), ("an ace of spades", 1), ("a card that is not an ace", 48),
    ("a face card of hearts", 3), ("a numbered card from 2 to 10", 36), ("a heart or a diamond", 26),
]


def one_card(r):
    if r.random() < 0.8:
        txt, k = r.choice(CARDS)
        p = F(k, 52)
        return Tp("One card is drawn from a well-shuffled deck of 52 playing cards. Find the probability that it is %s." % txt, p,
                  [F(k, 52 - k), F(1, 13) if p != F(1, 13) else F(1, 26), F(k, 13) if k <= 13 else F(1, 2)],
                  "There are %d such cards in 52. P = %d/52 = <b>%s</b>." % (k, k, pf(p)))
    k = r.choice(["kh", "qr", "as"])
    t, n, e = {"kh": ("a king or a heart", 16, "4 kings + 13 hearts − 1 (king of hearts counted twice) = 16"),
               "qr": ("a queen or a red card", 28, "4 queens + 26 red − 2 red queens = 28"),
               "as": ("an ace or a spade", 16, "4 aces + 13 spades − 1 (ace of spades) = 16")}[k]
    p = F(n, 52)
    wrong = F(n + (1 if k != "qr" else 2), 52)
    return Tp("One card is drawn from a well-shuffled deck of 52 cards. Find the probability that it is %s." % t, p, [wrong, F(1, 52), F(n, 26) if n < 26 else F(1, 2)],
              "%s. P = %d/52 = <b>%s</b>." % (e, n, pf(p)))


# ---------------------------------------------------------------- set 5: two coins, two dice, problems
def one_two(r):
    kind = r.choice(["coins", "dice", "dice", "dice", "lottery", "game"])
    if kind == "coins":
        n = r.choice([2, 3])
        ev = r.choice(["at least one head", "exactly one head", "no head", "two heads"]) if n == 2 else r.choice(["at least one head", "exactly two heads", "no tail", "at most one head"])
        outs = [""]
        for _ in range(n):
            outs = [o + c for o in outs for c in "HT"]
        test = {"at least one head": lambda o: "H" in o, "exactly one head": lambda o: o.count("H") == 1, "no head": lambda o: "H" not in o,
                "two heads": lambda o: o.count("H") == 2, "exactly two heads": lambda o: o.count("H") == 2, "no tail": lambda o: "T" not in o, "at most one head": lambda o: o.count("H") <= 1}[ev]
        fav = [o for o in outs if test(o)]
        p = F(len(fav), len(outs))
        return Tp("%s coins are tossed together. Find the probability of getting %s." % ("Two" if n == 2 else "Three", ev), p,
                  [F(len(fav), n + 1), F(len(fav) - 1, len(outs)) if fav else F(1, len(outs)), 1 - p],
                  "Outcomes: %s. Favourable: %s. P = <b>%s</b>." % (", ".join(outs), ", ".join(fav) or "none", pf(p)))
    if kind == "dice":
        ev = r.choice(["sum 8", "sum 7", "sum 10", "doublet", "sum 13", "sum at most 4", "product 6", "sum 2", "same number"])
        outs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
        test = {"sum 8": lambda a, b: a + b == 8, "sum 7": lambda a, b: a + b == 7, "sum 10": lambda a, b: a + b == 10, "doublet": lambda a, b: a == b,
                "sum 13": lambda a, b: a + b == 13, "sum at most 4": lambda a, b: a + b <= 4, "product 6": lambda a, b: a * b == 6, "sum 2": lambda a, b: a + b == 2,
                "same number": lambda a, b: a == b}[ev]
        txt = {"sum 8": "a sum of 8", "sum 7": "a sum of 7", "sum 10": "a sum of 10", "doublet": "a doublet (the same number on both)", "sum 13": "a sum of 13",
               "sum at most 4": "a sum of at most 4", "product 6": "a product of 6", "sum 2": "a sum of 2", "same number": "the same number on each die"}[ev]
        if ev == "same number":
            return None
        k = sum(1 for a, b in outs if test(a, b))
        p = F(k, 36)
        return Tp("Two dice are thrown at the same time. Find the probability of getting %s." % txt, p, [F(k, 11) if k <= 11 else F(1, 11), F(k + 1, 36), F(k, 12) if k <= 12 else F(1, 12)],
                  "There are 36 equally likely outcomes, and %d of them give %s. P = %d/36 = <b>%s</b>." % (k, txt, k, pf(p)))
    if kind == "lottery":
        t = r.choice([500, 1000, 2000, 5000])
        w = r.choice([2, 5, 10, 20, 25])
        p = F(w, t)
        name, he, his = P.next()
        return Tp("In a lucky draw there are %s tickets, of which %d carry a prize. %s buys one ticket. What is the probability that %s wins a prize?" % (num(t), w, name, he), p,
                  [F(t - w, t), F(1, w), F(w, t - w)], "%d prize tickets out of %s: P = <b>%s</b>." % (w, num(t), pf(p)))
    name, he, his = P.next()
    s = r.choice([("a piggy bank has 100 coins of 50 paise, 50 coins of ₹1, 20 coins of ₹2 and 10 coins of ₹5", "a 50 paise coin", F(100, 180), "100 of the 180 coins"),
                  ("a jar has 24 marbles, some green and some blue; the probability of a green marble is 2/3", "a blue marble", F(1, 3), "P(blue) = 1 − 2/3"),
                  ("a game has an arrow that stops on one of 8 equal sectors numbered 1 to 8", "an odd number", F(1, 2), "1, 3, 5, 7: 4 of 8"),
                  ("a game has an arrow that stops on one of 8 equal sectors numbered 1 to 8", "a number greater than 2", F(6, 8), "3 to 8: 6 of 8"),
                  ("the 12 children in a group include 5 girls", "a boy", F(7, 12), "7 boys of 12"),
                  ("in a class of 40 students, 15 come to school by bus", "a student who does not come by bus", F(25, 40), "25 of 40")])
    return Tp("%s. One is chosen at random. What is the probability of %s?" % (s[0][0].upper() + s[0][1:], s[1]), s[2], [1 - s[2], s[2] / 2, F(1, 4)],
              "%s: P = <b>%s</b>." % (s[3], pf(s[2])))


def main():
    seen = set()
    sets = [
        S("Probability: the basic ideas", mix(R, [(one_conc, 11), (one_die, 9)], seen)),
        S("Dice and numbered discs", mix(R, [(one_die, 20)], seen)),
        S("Bags, bulbs and pens", mix(R, [(one_bag, 20)], seen)),
        S("Playing cards", mix(R, [(one_card, 20)], seen)),
        S("Two coins, two dice and problems", mix(R, [(one_two, 20)], seen)),
    ]
    body = lesson(
        "<p>When all outcomes are <b>equally likely</b>, P(E) = number of favourable outcomes ÷ total number of outcomes.</p>"
        "<p>0 ≤ P(E) ≤ 1. A sure event has probability 1, an impossible event 0. <b>P(not E) = 1 − P(E)</b>.</p>"
        "<p>A deck has 52 cards: 4 suits (spades, clubs black; hearts, diamonds red) of 13 cards. Face cards are jacks, queens and kings (12 in all). Two dice give 36 outcomes.</p>",
        [("A die is thrown. Find P(prime number).", ["Primes: 2, 3, 5", "3 out of 6"], "1/2"),
         ("Two dice are thrown. Find P(sum = 8).", ["(2,6), (3,5), (4,4), (5,3), (6,2)", "5 out of 36"], "5/36")],
        ["Dividing favourable by unfavourable outcomes. Divide by the total.",
         "Counting a card twice (the king of hearts is a king and a heart).",
         "Taking the 11 possible sums of two dice as equally likely. Use the 36 ordered pairs."])
    faq = [
        ("What is the formula for probability in Class 10?", "P(E) = number of outcomes favourable to E ÷ number of all possible outcomes, when the outcomes are equally likely."),
        ("What are complementary events?", "E and not E. Exactly one of them happens, so P(E) + P(not E) = 1."),
        ("How many face cards are there in a deck of 52 cards?", "12: a jack, a queen and a king in each of the 4 suits."),
        ("How many outcomes are there when two dice are thrown?", "36, because each of the 6 outcomes of the first die can pair with each of the 6 outcomes of the second."),
    ]
    make(10, "probability", 14, "VII", 14, "Probability: Classical Probability", "probability",
         "Classical definition of probability; simple problems on finding the probability of an event (summary of the CBSE syllabus)",
         "Class 10 Probability worksheet (NCERT Chapter 14): sure and impossible events, complementary events, dice, coins, bags, playing cards and two dice. 100 questions with answers.",
         "P(E) = favourable outcomes ÷ total outcomes", "P(not E) = 1 − P(E)",
         body, faq, sets, R)


if __name__ == "__main__":
    main()
