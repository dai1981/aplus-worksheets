# -*- coding: utf-8 -*-
"""
India Class 11 Maths, NCERT Chapter 14: Probability (CBSE Unit V Statistics and Probability)
  python3 tools/gen_in_maths_c11_probability.py
Events and sample spaces (coins, dice, cards), complementary, mutually exclusive and exhaustive events, the axioms
(which assignments are valid), P(A ∪ B) = P(A) + P(B) − P(A ∩ B), P(not A), and 'and', 'or' and 'not' events
(own makers, SG Secondary 4 and US Geometry makers).
Wrong answers come from real mistakes: adding P(A) + P(B) for events that overlap, P(not A) = P(A) − 1, counting
the sample space of 3 coins as 6, and treating 'at least one' as 'exactly one'.
"""
import random, itertools
from fractions import Fraction as F
from in_sr import U, T2, use
from in_common import num, fv

R = random.Random(911114)
FX = [("P(A and B)", "P(A ∩ B)"), ("P(A or B)", "P(A ∪ B)"), ("A and B are", "A and B are")]
space = use(__import__("gen_sg_maths_s4_probability_of_combined_events"), "one_space", R, FX)
add = use(__import__("gen_us_math_ge_conditional_probability"), "one_add", R, FX)


def pv(x):
    return fv(x)


def one_ss(r):
    k = r.choice(["coins", "dice_coin", "count"])
    if k == "coins":
        n = r.choice([2, 3, 4])
        ev = r.choice(["exactly one head", "at least one head", "no head", "at least two heads", "exactly two heads", "at most one head"])
        outs = list(itertools.product("HT", repeat=n))
        cnt = {"exactly one head": lambda o: o.count("H") == 1, "at least one head": lambda o: o.count("H") >= 1, "no head": lambda o: o.count("H") == 0,
               "at least two heads": lambda o: o.count("H") >= 2, "exactly two heads": lambda o: o.count("H") == 2, "at most one head": lambda o: o.count("H") <= 1}[ev]
        m = sum(1 for o in outs if cnt(o))
        p = F(m, 2 ** n)
        alt = {"at least one head": "exactly one head", "exactly one head": "at least one head", "at least two heads": "exactly two heads", "exactly two heads": "at least two heads",
               "no head": "at most one head", "at most one head": "no head"}[ev]
        pa = F(sum(1 for o in outs if {"exactly one head": lambda o: o.count("H") == 1, "at least one head": lambda o: o.count("H") >= 1, "no head": lambda o: o.count("H") == 0,
               "at least two heads": lambda o: o.count("H") >= 2, "exactly two heads": lambda o: o.count("H") == 2, "at most one head": lambda o: o.count("H") <= 1}[alt](o)), 2 ** n)
        return T2("%d coins are tossed. Find the probability of getting %s." % (n, ev), pv(p), [pv(pa) if pa != p else pv(1 - p), pv(F(m, 2 * n)) if F(m, 2 * n) not in (p, pa) and m <= 2 * n else pv(F(1, 2 ** n)), pv(1 - p) if 1 - p not in (p,) else "1"],
                  "There are 2<sup>%d</sup> = %d equally likely outcomes, and %d of them have %s: <b>%s</b>." % (n, 2 ** n, m, ev, pv(p)))
    if k == "dice_coin":
        return T2("A die is thrown and a coin is tossed. How many outcomes are in the sample space?", "12", ["8", "6", "36"],
                  "6 outcomes for the die × 2 for the coin = <b>12</b>: {1H, 1T, 2H, …, 6T}.")
    n = r.choice([2, 3])
    return T2("How many outcomes are there when a die is thrown %d times?" % n, str(6 ** n), [str(6 * n), str(2 ** n * 3), str(6 ** n // 2)],
              "Each throw has 6 outcomes: 6<sup>%d</sup> = <b>%d</b>." % (n, 6 ** n))


def one_cards(r):
    ev = r.choice([("a king", 4), ("a red card", 26), ("a spade", 13), ("a face card", 12), ("an ace", 4), ("a red king", 2), ("a black face card", 6),
                   ("the queen of hearts", 1), ("a card that is not a heart", 39), ("a number card from 2 to 10", 36), ("a diamond or a club", 26),
                   ("a heart", 13), ("a card that is not an ace", 48), ("a red ace", 2), ("a black king", 2), ("a 7", 4), ("a black card", 26), ("a club face card", 3)])
    name, m = ev
    p = F(m, 52)
    cands = []
    for w in [F(m, 13), 1 - p, F(m, 26), F(1, 52), F(m + 4, 52), F(1, m), F(m - 1, 52)]:
        if 0 < w <= 1 and w != p and w not in cands:
            cands.append(w)
    return T2("A card is drawn at random from a well-shuffled pack of 52 cards. Find the probability that it is %s." % name, pv(p), [pv(w) for w in cands[:3]],
              "%d of the 52 cards are %s, so P = %d/52 = <b>%s</b>." % (m, name.replace("a ", "").replace("an ", "").replace("the ", ""), m, pv(p)))


def one_union(r):
    a, b = F(r.randint(2, 7), 10), F(r.randint(2, 7), 10)
    i = F(r.randint(1, min(int(a * 10), int(b * 10)) - 0), 10)
    if a + b - i > 1 or i >= min(a, b) + F(1, 100) and False:
        return None
    if i > min(a, b):
        return None
    u = a + b - i
    k = r.choice(["u", "i", "not", "only"])
    if k == "u":
        return T2("P(A) = %s, P(B) = %s and P(A ∩ B) = %s. Find P(A ∪ B)." % (num(a), num(b), num(i)), num(u), [num(a + b) if a + b <= 1 else num(u + F(1, 10)), num(a * b), num(a + b - 2 * i) if a + b - 2 * i != u else num(u - F(1, 10))],
                  "P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = %s + %s − %s = <b>%s</b>." % (num(a), num(b), num(i), num(u)))
    if k == "i":
        return T2("P(A) = %s, P(B) = %s and P(A ∪ B) = %s. Find P(A ∩ B)." % (num(a), num(b), num(u)), num(i), [num(a * b) if a * b != i else num(i + F(1, 10)), num(u - a), num(a + b + u - 1) if 0 <= a + b + u - 1 <= 1 and a + b + u - 1 != i else num(i + F(2, 10))],
                  "P(A ∩ B) = P(A) + P(B) − P(A ∪ B) = <b>%s</b>." % num(i))
    if k == "not":
        return T2("P(A) = %s, P(B) = %s and P(A ∩ B) = %s. Find P(not A and not B)." % (num(a), num(b), num(i)), num(1 - u), [num(1 - a - b) if a + b <= 1 else num(1 - u + F(1, 10)), num(u), num((1 - a) * (1 - b)) if (1 - a) * (1 - b) != 1 - u else num(1 - i)],
                  "P(A′ ∩ B′) = 1 − P(A ∪ B) = 1 − %s = <b>%s</b>." % (num(u), num(1 - u)))
    return T2("P(A) = %s and P(A ∩ B) = %s. Find P(A but not B)." % (num(a), num(i)), num(a - i), [num(a), num(a + i) if a + i <= 1 else num(i), num(1 - i)],
              "P(A ∩ B′) = P(A) − P(A ∩ B) = <b>%s</b>." % num(a - i))


def one_axiom(r):
    good = [F(1, 4)] * 4
    sets = []
    while len(sets) < 4:
        k = len(sets)
        ps = [F(r.randint(1, 5), 10) for _ in range(3)]
        if k == 0:
            last = 1 - sum(ps)
            if last < 0:
                continue
            ps.append(last)
        elif k == 1:
            last = 1 - sum(ps) + F(1, 10)
            ps.append(last)
            if last < 0:
                continue
        elif k == 2:
            ps.append(F(-1, 10))
            ps[0] = 1 - ps[1] - ps[2] - ps[3]
            if ps[0] <= 0 or ps[0] > 1:
                continue
        else:
            ps[0] = F(11, 10)
            ps.append(1 - sum(ps))
        sets.append(ps)
    show = lambda ps: ", ".join(num(p) for p in ps)
    return T2("A sample space has four outcomes. Which assignment of probabilities to them is valid?", show(sets[0]), [show(s) for s in sets[1:]],
              "Each probability must be between 0 and 1 and they must add up to 1. Only <b>%s</b> does this." % show(sets[0]))


def one_events(r):
    k = r.choice(["me", "exh", "comp"])
    if k == "me":
        return T2("A die is thrown. A: an even number, B: an odd number, C: a number less than 3. Which pair is mutually exclusive?", "A and B",
                  ["A and C", "B and C", "A, B and C together"], "A ∩ B = φ, but A ∩ C = {2} and B ∩ C = {1}. So <b>A and B</b> are mutually exclusive.")
    if k == "comp":
        n = r.choice([3, 4, 5, 6])
        return T2("A die is thrown. A is the event 'a number less than %d'. What is A′?" % n, "{%s}" % ", ".join(map(str, range(n, 7))),
                  ["{%s}" % ", ".join(map(str, range(1, n))), "{%s}" % ", ".join(map(str, range(n + 1, 7))) if n < 6 else "φ", "{%s}" % ", ".join(map(str, range(1, n + 1)))],
                  "A = {%s}, so A′ = S − A = <b>{%s}</b>." % (", ".join(map(str, range(1, n))), ", ".join(map(str, range(n, 7)))))
    p = F(r.randint(1, 9), 10)
    q = F(r.randint(1, 9), 10)
    if p + q != 1:
        return T2("P(E) = %s. Find P(not E)." % num(p), num(1 - p), [num(p), num(p - 1) if p != 1 else "0", num(1 + p) if 1 + p <= 2 else "1"],
                  "P(E′) = 1 − P(E) = <b>%s</b>." % num(1 - p))
    return None


U(11, 14, "probability", 14, "VII", "Probability: Events, Axioms and the Addition Rule", "probability",
  "Events: occurrence of events, 'not', 'and' and 'or' events, exhaustive events, mutually exclusive events; axiomatic (set theoretic) probability, connections with other theories studied in earlier classes; probability of an event, probability of 'not', 'and' and 'or' events (summary of the CBSE syllabus)",
  "Class 11 Probability worksheet (NCERT Chapter 14): sample spaces, coins, dice and cards, complementary and mutually exclusive events, axioms and P(A ∪ B). 100 questions with answers.",
  "P(A ∪ B) = P(A) + P(B) − P(A ∩ B).", "P(not A) = 1 − P(A).",
  "<ul><li>The <b>sample space</b> S is the set of all outcomes. An <b>event</b> is a subset of S.</li>"
  "<li>Axioms: 0 ≤ P(E) ≤ 1, P(S) = 1, and probabilities of outcomes add up to 1.</li>"
  "<li>A and B are <b>mutually exclusive</b> if A ∩ B = φ; then P(A ∪ B) = P(A) + P(B).</li>"
  "<li>In general P(A ∪ B) = P(A) + P(B) − P(A ∩ B), and P(A′) = 1 − P(A).</li></ul>",
  [("3 coins are tossed. Find P(at least one head).", ["8 outcomes; only TTT has no head", "1 − 1/8"], "7/8")],
  ["Adding P(A) + P(B) when A and B overlap.", "Taking 6 outcomes for 3 coins (there are 8).", "Treating 'at least one' as 'exactly one'."],
  [("What are exhaustive events?", "Events whose union is the whole sample space."), ("Can a probability be more than 1?", "No. 0 ≤ P(E) ≤ 1.")],
  [("Sample spaces and coins", [(one_ss, 12), (space, 8)]),
   ("Dice and cards", [(one_cards, 10), (space, 10)]),
   ("Events and axioms", [(one_events, 10), (one_axiom, 1), (add, 9)]),
   ("Addition rule", [(one_union, 20)]),
   ("Mixed problems", [(one_union, 8), (add, 8), (space, 4)])], 911114)
