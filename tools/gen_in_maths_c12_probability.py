# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 13: Probability (CBSE Unit VI Probability)
  python3 tools/gen_in_maths_c12_probability.py
Conditional probability P(A|B) = P(A ∩ B)/P(B), conditional probability with dice, coins and two-way tables, the
multiplication theorem (drawing with and without replacement), independent events, the theorem of total probability
and Bayes' theorem (own makers, US Geometry and SG Secondary 4 makers).
Wrong answers come from real mistakes: P(A ∩ B)/P(A) for P(A|B), P(A)P(B) for events that are not independent,
replacing the first card when it is not replaced, adding the probabilities from the bags without weighting them,
and giving P(B|A) for Bayes' P(A|B).
"""
import random, itertools
from fractions import Fraction as F
from in_sr import U, T2, use
from in_common import num, fv

R = random.Random(912113)
FX = [("P(A and B)", "P(A ∩ B)"), ("P(A or B)", "P(A ∪ B)"), ("P(B | A)", "P(B|A)"), ("P(A | B)", "P(A|B)"), ("9th class", "Class 9"), ("10th class", "Class 10")]
cond = use(__import__("gen_us_math_ge_conditional_probability"), "one_cond", R, FX)
ind = use(__import__("gen_us_math_ge_conditional_probability"), "one_ind", R, FX)
table_ = use(__import__("gen_us_math_ge_conditional_probability"), "one_table", R, FX)
draw = use(__import__("gen_us_math_ge_conditional_probability"), "one_draw", R, FX)
without = use(__import__("gen_sg_maths_s4_probability_of_combined_events"), "one_without", R, FX)


def one_cp(r):
    a, b = F(r.randint(2, 9), 10), F(r.randint(2, 9), 10)
    i = F(r.randint(1, 9), 20)
    if i > min(a, b) or a + b - i > 1:
        return None
    k = r.choice(["ab", "ba", "union"])
    if k == "ab":
        return T2("P(A) = %s, P(B) = %s and P(A ∩ B) = %s. Find P(A|B)." % (num(a), num(b), num(i)), fv(i / b), [fv(i / a) if i / a != i / b else fv(i), fv(i * b) if i * b != i / b else fv(a * b), fv(a)],
                  "P(A|B) = P(A ∩ B) ÷ P(B) = %s ÷ %s = <b>%s</b>." % (num(i), num(b), fv(i / b)))
    if k == "ba":
        return T2("P(A) = %s, P(B) = %s and P(A ∩ B) = %s. Find P(B|A)." % (num(a), num(b), num(i)), fv(i / a), [fv(i / b) if i / a != i / b else fv(i), fv(i * a) if i * a != i / a else fv(a * b), fv(b)],
                  "P(B|A) = P(A ∩ B) ÷ P(A) = %s ÷ %s = <b>%s</b>." % (num(i), num(a), fv(i / a)))
    u = a + b - i
    return T2("P(A) = %s, P(B) = %s and P(A|B) = %s. Find P(A ∪ B)." % (num(a), num(b), fv(i / b)), num(u), [num(a + b) if a + b <= 1 else num(u + F(1, 10)), num(1 - u), num(a + b - i / b) if 0 <= a + b - i / b <= 1 and a + b - i / b != u else num(u - F(1, 20))],
              "P(A ∩ B) = P(B) × P(A|B) = %s, so P(A ∪ B) = %s + %s − %s = <b>%s</b>." % (num(i), num(a), num(b), num(i), num(u)))


DIE_EV = [("the sum is %d", lambda o, k: o[0] + o[1] == k, [6, 7, 8, 9, 10]), ("the sum is at least %d", lambda o, k: o[0] + o[1] >= k, [9, 10, 11]),
          ("a %d appears on at least one die", lambda o, k: k in o, [4, 5, 6]), ("both dice show the same number", lambda o, k: o[0] == o[1], [0])]
GIVEN = [("the first die shows %d", lambda o, k: o[0] == k, [2, 3, 4, 5, 6]), ("the sum is even", lambda o, k: (o[0] + o[1]) % 2 == 0, [0]),
         ("the first die shows an odd number", lambda o, k: o[0] % 2 == 1, [0]), ("the sum is more than %d", lambda o, k: o[0] + o[1] > k, [6, 7, 8])]


def one_dice(r):
    (ta, fa, ka), (tb, fb, kb) = r.choice(DIE_EV), r.choice(GIVEN)
    k1, k2 = r.choice(ka), r.choice(kb)
    outs = list(itertools.product(range(1, 7), repeat=2))
    B = [o for o in outs if fb(o, k2)]
    AB = [o for o in B if fa(o, k1)]
    if not B or not AB or len(AB) == len(B):
        return None
    p = F(len(AB), len(B))
    pa = F(sum(1 for o in outs if fa(o, k1)), 36)
    A_ = ta % k1 if "%d" in ta else ta
    B_ = tb % k2 if "%d" in tb else tb
    return T2("Two dice are thrown. Find the probability that %s, given that %s." % (A_, B_), fv(p), [fv(pa) if pa != p else fv(F(len(AB), 36)), fv(F(len(AB), 36)) if F(len(AB), 36) not in (p, pa) else fv(1 - p), fv(F(len(B), 36))],
              "Given %s, there are %d equally likely outcomes, and %d of them have %s: <b>%s</b>." % (B_, len(B), len(AB), A_, fv(p)))


BAGS = [("red", "black"), ("white", "black"), ("red", "blue"), ("green", "yellow")]


def one_total(r):
    c1, c2 = r.choice(BAGS)
    a1, b1 = r.randint(1, 8), r.randint(1, 8)
    a2, b2 = r.randint(1, 8), r.randint(1, 8)
    if a1 * (a2 + b2) == a2 * (a1 + b1):
        return None
    pb = F(1, 2)
    p1, p2 = F(a1, a1 + b1), F(a2, a2 + b2)
    tot = pb * p1 + pb * p2
    k = r.choice(["total", "bayes"])
    setup = "Bag I has %d %s and %d %s balls; bag II has %d %s and %d %s balls. A bag is chosen at random and a ball is drawn from it." % (a1, c1, b1, c2, a2, c1, b2, c2)
    if k == "total":
        return T2(setup + " Find the probability that the ball is %s." % c1, fv(tot), [fv(p1 + p2) if p1 + p2 <= 1 else fv(F(a1 + a2, a1 + b1 + a2 + b2)) if F(a1 + a2, a1 + b1 + a2 + b2) != tot else fv(p1 * p2), fv(p1 * p2), fv(F(a1 + a2, a1 + b1 + a2 + b2)) if F(a1 + a2, a1 + b1 + a2 + b2) != tot else fv(tot / 2)],
                  "Total probability: ½ × %s + ½ × %s = <b>%s</b>." % (fv(p1), fv(p2), fv(tot)))
    post = pb * p1 / tot
    return T2(setup + " The ball is %s. Find the probability that it came from bag I." % c1, fv(post), [fv(p1), fv(pb * p1), fv(1 - post)],
              "Bayes' theorem: P(I|%s) = (½ × %s) ÷ (½ × %s + ½ × %s) = <b>%s</b>." % (c1, fv(p1), fv(p1), fv(p2), fv(post)))


def one_factory(r):
    sh = r.choice([(50, 30, 20), (40, 35, 25), (60, 25, 15), (25, 35, 40), (30, 50, 20)])
    df = [r.choice([1, 2, 3, 4, 5]) for _ in range(3)]
    tot = sum(F(s, 100) * F(d, 100) for s, d in zip(sh, df))
    j = r.randrange(3)
    post = F(sh[j], 100) * F(df[j], 100) / tot
    names = ["A", "B", "C"]
    setup = "Machines A, B and C make %d%%, %d%% and %d%% of the bolts in a factory, and %d%%, %d%% and %d%% of their bolts are defective." % (*sh, *df)
    if r.random() < 0.5:
        return T2(setup + " A bolt is picked at random. Find the probability that it is defective.", fv(tot), [fv(F(sum(df), 300)), fv(F(sum(df), 100)), fv(tot * 2)],
                  "P(D) = Σ P(machine) × P(D|machine) = <b>%s</b>." % fv(tot))
    return T2(setup + " A bolt picked at random is defective. Find the probability that machine %s made it." % names[j], fv(post), [fv(F(df[j], 100)), fv(F(sh[j], 100)), fv(1 - post)],
              "Bayes: P(%s|D) = (%s × %s) ÷ P(D) = <b>%s</b>." % (names[j], fv(F(sh[j], 100)), fv(F(df[j], 100)), fv(post)))


def one_ind2(r):
    a, b = F(r.randint(1, 9), 10), F(r.randint(1, 9), 10)
    k = r.choice(["and", "or", "neither", "check"])
    if k == "and":
        return T2("A and B are independent, with P(A) = %s and P(B) = %s. Find P(A ∩ B)." % (num(a), num(b)), num(a * b), [num(a + b) if a + b <= 1 else num(a * b + F(1, 10)), num(min(a, b)), num(abs(a - b)) if a != b and abs(a - b) != a * b else num(1 - a * b)],
                  "For independent events P(A ∩ B) = P(A)P(B) = <b>%s</b>." % num(a * b))
    if k == "or":
        u = a + b - a * b
        return T2("A and B are independent, with P(A) = %s and P(B) = %s. Find P(A ∪ B)." % (num(a), num(b)), num(u), [num(a + b) if a + b <= 1 else num(u - F(1, 100)), num(a * b), num(1 - a * b) if 1 - a * b != u else num(u + F(1, 100))],
                  "P(A ∪ B) = P(A) + P(B) − P(A)P(B) = <b>%s</b>." % num(u))
    if k == "neither":
        v = (1 - a) * (1 - b)
        return T2("A and B are independent, with P(A) = %s and P(B) = %s. Find the probability that neither happens." % (num(a), num(b)), num(v),
                  [num(1 - a * b), num(1 - a - b) if a + b <= 1 and 1 - a - b != v else num(v + F(1, 100)), num(a * b) if a * b != v else num(v - F(1, 100))],
                  "P(A′ ∩ B′) = P(A′)P(B′) = %s × %s = <b>%s</b>." % (num(1 - a), num(1 - b), num(v)))
    i = a * b if r.random() < 0.5 else a * b + F(r.choice([1, -1]), 100)
    if i <= 0:
        return None
    yes = i == a * b
    return T2("P(A) = %s, P(B) = %s and P(A ∩ B) = %s. Are A and B independent?" % (num(a), num(b), num(i)), "Yes" if yes else "No",
              ["No" if yes else "Yes", "Only if they are mutually exclusive", "It cannot be decided"],
              "P(A)P(B) = %s, which %s P(A ∩ B), so <b>%s</b>." % (num(a * b), "equals" if yes else "is not equal to", "they are independent" if yes else "they are not independent"))


U(12, 13, "probability", 13, "Pr", "Probability: Conditional Probability, Independent Events and Bayes' Theorem", "probability",
  "Conditional probability, multiplication theorem on probability, independent events, total probability, Bayes' theorem (summary of the CBSE syllabus)",
  "Class 12 Probability worksheet (NCERT Chapter 13): conditional probability, the multiplication theorem, independent events, total probability and Bayes' theorem. 100 questions with answers.",
  "P(A|B) = P(A ∩ B) ÷ P(B).", "Independent: P(A ∩ B) = P(A)P(B).",
  "<ul><li><b>Conditional probability</b>: P(A|B) = P(A ∩ B) ÷ P(B), the probability of A when we know B has happened.</li>"
  "<li><b>Multiplication theorem</b>: P(A ∩ B) = P(A)P(B|A). Without replacement, the second draw has one fewer item.</li>"
  "<li>A and B are <b>independent</b> if P(A ∩ B) = P(A)P(B), so P(A|B) = P(A).</li>"
  "<li><b>Total probability</b>: P(A) = Σ P(E<sub>i</sub>)P(A|E<sub>i</sub>). <b>Bayes' theorem</b>: P(E<sub>i</sub>|A) = P(E<sub>i</sub>)P(A|E<sub>i</sub>) ÷ Σ P(E<sub>j</sub>)P(A|E<sub>j</sub>).</li></ul>",
  [("A die is thrown. Find P(a 2 | the number is even).", ["Given even: {2, 4, 6}", "One of these three is 2"], "1/3")],
  ["Dividing by P(A) instead of P(B) for P(A|B).", "Multiplying P(A)P(B) for events that are not independent.", "Weighting both bags as 1 when each is chosen with probability ½."],
  [("Are mutually exclusive events independent?", "No (unless one has probability 0). If A happens, B cannot, so knowing A changes P(B)."),
   ("When is Bayes' theorem used?", "To find the probability of a cause (which bag, which machine) after seeing the result.")],
  [("Conditional probability", [(one_cp, 12), (cond, 8)]),
   ("Dice and tables", [(one_dice, 12), (table_, 8)]),
   ("Multiplication theorem", [(draw, 10), (without, 10)]),
   ("Independent events", [(one_ind2, 14), (ind, 6)]),
   ("Total probability and Bayes' theorem", [(one_total, 12), (one_factory, 8)])], 912113)
