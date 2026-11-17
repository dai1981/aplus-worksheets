# -*- coding: utf-8 -*-
"""
US Geometry: Conditional Probability and Independence (Common Core S-CP.A.3, S-CP.A.2, S-CP.A.4, S-CP.B.7)
  python3 tools/gen_us_math_ge_conditional_probability.py
The Addition Rule and complements, independent events, the conditional probability formula, two-way tables,
and drawing with and without replacement.
Wrong answers come from real mistakes: adding P(A) and P(B) without subtracting the overlap, dividing by the
wrong total in a two-way table, mixing up P(A | B) and P(B | A), and keeping the same total when drawing
without replacement.
"""
import random
from fractions import Fraction as F
from us_hs import B, S, make, lesson, collect, T, num, MINUS, fr, People

R = random.Random(94301)


def pf(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    return fr(v.numerator, v.denominator)


def pc(v):
    """percent or decimal with up to 2 places"""
    return num(v)


def opts(right, wr):
    out = []
    for w in wr:
        if w is None:
            continue
        w = F(w)
        if w <= 0 or w > 1 or w == right:
            continue
        if pf(w) not in out:
            out.append(pf(w))
    k = 1
    while len(out) < 3:
        for cand in (right + F(1, 10 * k), right - F(1, 10 * k), right / 2, (1 + right) / 2):
            if 0 < cand < 1 and cand != right and pf(cand) not in out:
                out.append(pf(cand))
                break
        k += 1
    return out[:3]


# ------------------------------------------------------------ set 1: addition rule and complements
def one_add(r):
    kind = r.choice(["or", "or", "or_dec", "comp", "mutex", "card"])
    if kind in ("or", "or_dec"):
        a, b = F(r.randint(2, 7), 10), F(r.randint(2, 7), 10)
        both = F(r.randint(1, min(int(a * 10), int(b * 10)) - 0), 10) if min(a, b) > F(1, 10) else F(1, 10)
        if a + b - both > 1 or both >= min(a, b):
            return None
        q = "P(A) = %s, P(B) = %s and P(A and B) = %s. Find P(A or B)." % (pc(a), pc(b), pc(both))
        ans = a + b - both
        wr = [a + b, a * b, a + b - 2 * both, both]
        return T(q, pc(ans), [pc(w) for w in dict.fromkeys(wr) if w != ans and 0 < w <= 1][:3] + ([pc(ans + F(1, 10))] if len({w for w in wr if w != ans and 0 < w <= 1}) < 3 else []),
                 "Addition Rule: P(A or B) = P(A) + P(B) %s P(A and B) = %s + %s %s %s = <b>%s</b>. Subtract the overlap so it is not counted twice." % (
                     MINUS, pc(a), pc(b), MINUS, pc(both), pc(ans)))
    if kind == "comp":
        p = F(r.randint(1, 19), 20)
        q = "The probability that it rains tomorrow is %s. What is the probability that it does not rain?" % pc(p)
        return T(q, pc(1 - p), [pc(p), pc(1 - p / 2) if 1 - p / 2 != 1 - p else pc(p / 2), pc(abs(F(1, 2) - p)) if abs(F(1, 2) - p) not in (p, 1 - p) and p != F(1, 2) else pc(F(1, 20))],
                 "Complement: P(not A) = 1 %s P(A) = 1 %s %s = <b>%s</b>." % (MINUS, MINUS, pc(p), pc(1 - p)))
    if kind == "mutex":
        a, b = F(r.randint(1, 5), 10), F(r.randint(1, 4), 10)
        q = "Events A and B are mutually exclusive (they cannot both happen). P(A) = %s and P(B) = %s. Find P(A or B)." % (pc(a), pc(b))
        ans = a + b
        return T(q, pc(ans), [pc(w) for w in dict.fromkeys([a * b, abs(a - b) if a != b else a / 2, a + b - a * b]) if w != ans][:3],
                 "Mutually exclusive events have no overlap, so P(A and B) = 0 and P(A or B) = %s + %s = <b>%s</b>." % (pc(a), pc(b), pc(ans)))
    items = [("One card is drawn from a standard 52-card deck. What is the probability it is a heart or a king?", F(16, 52), [F(17, 52), F(13, 52) * F(4, 52), F(4, 52)],
              "13 hearts + 4 kings %s 1 king of hearts (counted twice) = 16 cards. 16/52 = <b>%s</b>." % (MINUS, pf(F(16, 52)))),
             ("One card is drawn from a standard 52-card deck. What is the probability it is red or a face card (J, Q, K)?", F(32, 52), [F(38, 52), F(26, 52), F(12, 52)],
              "26 red + 12 face cards %s 6 red face cards = 32. 32/52 = <b>%s</b>." % (MINUS, pf(F(32, 52)))),
             ("A number cube is rolled. What is the probability of an even number or a number greater than 4?", F(4, 6), [F(5, 6), F(3, 6), F(1, 6)],
              "Even: 2, 4, 6. Greater than 4: 5, 6. Together: 2, 4, 5, 6, which is 4 outcomes. 4/6 = <b>%s</b>." % pf(F(4, 6))),
             ("A number cube is rolled. What is the probability of a number less than 3 or a 6?", F(3, 6), [F(2, 6), F(4, 6), F(1, 6)],
              "Outcomes 1, 2 and 6: 3/6 = <b>%s</b>. These events cannot happen together." % pf(F(1, 2)))]
    q, ans, wr, e = r.choice(items)
    return T(q, pf(ans), opts(ans, wr), e)


# ------------------------------------------------------------ set 2: independent events
def one_ind(r):
    kind = r.choice(["mult", "mult", "test", "test", "dice"])
    if kind == "mult":
        a, b = F(r.randint(1, 9), 10), F(r.randint(1, 9), 10)
        q = "A and B are independent. P(A) = %s and P(B) = %s. Find P(A and B)." % (pc(a), pc(b))
        ans = a * b
        return T(q, pc(ans), [pc(w) for w in dict.fromkeys([a + b if a + b <= 1 else a + b - 1 + F(1, 100), a + b - a * b, min(a, b)]) if w != ans][:3],
                 "For independent events, multiply: P(A and B) = %s × %s = <b>%s</b>." % (pc(a), pc(b), pc(ans)))
    if kind == "test":
        a, b = F(r.randint(2, 8), 10), F(r.randint(2, 8), 10)
        ind = r.random() < 0.5
        both = a * b if ind else a * b + r.choice([F(1, 50), F(-1, 50), F(3, 100), F(-3, 100)])
        if both <= 0 or both >= min(a, b):
            return None
        q = "P(A) = %s, P(B) = %s and P(A and B) = %s. Are A and B independent?" % (pc(a), pc(b), pc(both))
        right = "Yes, because P(A) × P(B) = P(A and B)" if ind else "No, because P(A) × P(B) ≠ P(A and B)"
        return T(q, right, [x for x in ["Yes, because P(A) × P(B) = P(A and B)", "No, because P(A) × P(B) ≠ P(A and B)",
                                        "Yes, because P(A) + P(B) &lt; 1", "No, because P(A) ≠ P(B)"] if x != right],
                 "P(A) × P(B) = %s × %s = %s, which %s P(A and B) = %s. <b>%s</b>." % (pc(a), pc(b), pc(a * b), "equals" if ind else "does not equal", pc(both), right))
    items = [("Two number cubes are rolled. What is the probability that both show a 6?", F(1, 36), [F(1, 6), F(2, 6), F(1, 12)], "Independent: 1/6 × 1/6 = <b>1/36</b>."),
             ("A coin is flipped and a number cube is rolled. What is the probability of heads and a number less than 3?", F(1, 6), [F(1, 2), F(1, 3), F(5, 6)], "½ × 2/6 = 2/12 = <b>1/6</b>."),
             ("A coin is flipped three times. What is the probability of three heads?", F(1, 8), [F(3, 8), F(1, 6), F(1, 2)], "½ × ½ × ½ = <b>1/8</b>."),
             ("A spinner has 4 equal sections: red, blue, green, yellow. It is spun twice. What is the probability of red both times?", F(1, 16), [F(1, 8), F(1, 4), F(1, 2)],
              "Independent spins: ¼ × ¼ = <b>1/16</b>."),
             ("Two number cubes are rolled. What is the probability that neither shows a 1?", F(25, 36), [F(5, 6), F(1, 36), F(11, 36)], "P(not 1) = 5/6 on each cube: 5/6 × 5/6 = <b>25/36</b>.")]
    q, ans, wr, e = r.choice(items)
    return T(q, pf(ans), opts(ans, wr), e.replace("1/36", pf(F(1, 36))))


# ------------------------------------------------------------ set 3: conditional probability formula
def one_cond(r):
    a = F(r.randint(2, 9), 10)
    both = F(r.randint(1, int(a * 10) - 1), 10) if a > F(1, 10) else None
    if both is None:
        return None
    kind = r.choice(["given", "given", "back", "words"])
    if kind == "given":
        q = "P(A) = %s and P(A and B) = %s. Find P(B | A)." % (pc(a), pc(both))
        ans = both / a
        if num(ans) is None:
            return T(q, pf(ans), opts(ans, [both * a, a - both, both]), "P(B | A) = P(A and B) ÷ P(A) = %s ÷ %s = <b>%s</b>." % (pc(both), pc(a), pf(ans)))
        return T(q, pc(ans), [pc(w) for w in dict.fromkeys([both * a, a - both, both, ans / 2]) if w != ans and num(w)][:3],
                 "P(B | A) = P(A and B) ÷ P(A) = %s ÷ %s = <b>%s</b>." % (pc(both), pc(a), pc(ans)))
    if kind == "back":
        bg = F(r.randint(1, 9), 10)
        q = "P(A) = %s and P(B | A) = %s. Find P(A and B)." % (pc(a), pc(bg))
        ans = a * bg
        return T(q, pc(ans), [pc(w) for w in dict.fromkeys([a + bg if a + bg <= 1 else bg / 2, bg / a if bg < a else a / 2, abs(a - bg) if a != bg else a / 4]) if w != ans and num(w)][:3] +
                 ([pc(ans + F(1, 10))] if len({w for w in [a + bg if a + bg <= 1 else bg / 2, bg / a if bg < a else a / 2, abs(a - bg) if a != bg else a / 4] if w != ans and num(w)}) < 3 else []),
                 "P(A and B) = P(A) × P(B | A) = %s × %s = <b>%s</b>." % (pc(a), pc(bg), pc(ans)))
    pp = People(r)
    nm, he, his = pp.next()
    pa, pab = r.choice([(F(3, 5), F(3, 10)), (F(4, 5), F(2, 5)), (F(1, 2), F(1, 5)), (F(7, 10), F(7, 20)), (F(3, 4), F(1, 2)), (F(2, 5), F(1, 10))])
    q = ("At a school, %s of students take the bus, and %s of students take the bus and live more than 5 miles away. "
         "What is the probability that a student who takes the bus lives more than 5 miles away?" % (pc(pa * 100) + "%", pc(pab * 100) + "%"))
    ans = pab / pa
    right = pc(ans * 100) + "%"
    return T(q, right, [pc(w * 100) + "%" for w in dict.fromkeys([pab, pa * pab, pa - pab]) if w != ans][:3],
             "P(far | bus) = P(far and bus) ÷ P(bus) = %s ÷ %s = <b>%s</b>." % (pc(pab), pc(pa), right))


# ------------------------------------------------------------ set 4: two-way tables
SCEN = [("Grade", ["9th grade", "10th grade"], "Activity", ["Sports", "Music"]),
        ("Pet", ["Has a dog", "No dog"], "Pet", ["Has a cat", "No cat"]),
        ("Lunch", ["Brings lunch", "Buys lunch"], "Snack", ["Likes apples", "Likes chips"]),
        ("Device", ["Phone", "Tablet"], "Use", ["Games", "Video"])]


def one_table(r):
    _, rows, _, cols = r.choice(SCEN)
    v = [[r.randint(8, 45) for _ in range(2)] for _ in range(2)]
    rt = [sum(x) for x in v]
    ct = [v[0][j] + v[1][j] for j in range(2)]
    tot = sum(rt)
    tbl = ("<div class='sn-tw'><table class='sn-table'><thead><tr><th></th><th>%s</th><th>%s</th><th>Total</th></tr></thead><tbody>"
           "<tr><th>%s</th><td>%d</td><td>%d</td><td>%d</td></tr><tr><th>%s</th><td>%d</td><td>%d</td><td>%d</td></tr>"
           "<tr><th>Total</th><td>%d</td><td>%d</td><td>%d</td></tr></tbody></table></div>" % (
               cols[0], cols[1], rows[0], v[0][0], v[0][1], rt[0], rows[1], v[1][0], v[1][1], rt[1], ct[0], ct[1], tot))
    i, j = r.randint(0, 1), r.randint(0, 1)
    kind = r.choice(["row", "col", "and", "row", "col"])
    if kind == "row":
        q = "A person is chosen at random from the table. Find P(%s | %s).%s" % (cols[j], rows[i], tbl)
        ans = F(v[i][j], rt[i])
        e = "Given %s, use only that row: %d out of %d. <b>%s</b>." % (rows[i], v[i][j], rt[i], pf(ans))
        wr = [F(v[i][j], ct[j]), F(v[i][j], tot), F(rt[i], tot)]
    elif kind == "col":
        q = "A person is chosen at random from the table. Find P(%s | %s).%s" % (rows[i], cols[j], tbl)
        ans = F(v[i][j], ct[j])
        e = "Given %s, use only that column: %d out of %d. <b>%s</b>." % (cols[j], v[i][j], ct[j], pf(ans))
        wr = [F(v[i][j], rt[i]), F(v[i][j], tot), F(ct[j], tot)]
    else:
        q = "A person is chosen at random from the table. Find P(%s and %s).%s" % (rows[i], cols[j], tbl)
        ans = F(v[i][j], tot)
        e = "Both conditions: the cell has %d people out of %d in all. <b>%s</b>." % (v[i][j], tot, pf(ans))
        wr = [F(v[i][j], rt[i]), F(v[i][j], ct[j]), F(rt[i] + ct[j] - v[i][j], tot)]
    if rows[0] == "Has a dog" and kind:
        pass
    return T(q, pf(ans), opts(ans, wr), e)


# ------------------------------------------------------------ set 5: with and without replacement
def one_draw(r):
    pp = People(r)
    nm, he, his = pp.next()
    a, b = r.randint(2, 8), r.randint(2, 8)
    col1, col2 = r.choice([("red", "blue"), ("green", "yellow"), ("black", "white"), ("orange", "purple")])
    tot = a + b
    kind = r.choice(["without", "without", "with", "mixed", "second"])
    if kind == "without":
        q = "A bag has %d %s marbles and %d %s marbles. %s takes two marbles without replacement. What is the probability both are %s?" % (a, col1, b, col2, nm, col1)
        ans = F(a, tot) * F(a - 1, tot - 1)
        if ans == 0:
            return None
        return T(q, pf(ans), opts(ans, [F(a, tot) ** 2, F(a, tot) * F(a, tot - 1), F(a - 1, tot - 1)]),
                 "First %s: %d/%d. One %s is gone, so the second is %d/%d. %s × %s = <b>%s</b>." % (
                     col1, a, tot, col1, a - 1, tot - 1, pf(F(a, tot)), pf(F(a - 1, tot - 1)), pf(ans)))
    if kind == "with":
        q = "A bag has %d %s marbles and %d %s marbles. %s takes a marble, puts it back, and takes another. What is the probability both are %s?" % (a, col1, b, col2, nm, col2)
        ans = F(b, tot) ** 2
        return T(q, pf(ans), opts(ans, [F(b, tot) * F(b - 1, tot - 1), F(2 * b, tot) if 2 * b < tot else F(b, 2 * tot), F(b, tot)]),
                 "With replacement the draws are independent: %s × %s = <b>%s</b>." % (pf(F(b, tot)), pf(F(b, tot)), pf(ans)))
    if kind == "mixed":
        q = "A bag has %d %s marbles and %d %s marbles. Two are drawn without replacement. What is the probability the first is %s and the second is %s?" % (a, col1, b, col2, col1, col2)
        ans = F(a, tot) * F(b, tot - 1)
        return T(q, pf(ans), opts(ans, [F(a, tot) * F(b, tot), 2 * ans if 2 * ans < 1 else ans / 2, F(a * b, tot)]),
                 "%d/%d × %d/%d = <b>%s</b>. The total drops to %d for the second draw." % (a, tot, b, tot - 1, pf(ans), tot - 1))
    q = "A bag has %d %s marbles and %d %s marbles. The first marble drawn is %s and is not replaced. What is the probability that the second is %s?" % (a, col1, b, col2, col1, col1)
    ans = F(a - 1, tot - 1)
    if ans == 0:
        return None
    return T(q, pf(ans), opts(ans, [F(a, tot), F(a - 1, tot), F(a, tot - 1)]),
             "This is P(second %s | first %s). After one %s is removed, %d of the %d marbles left are %s: <b>%s</b>." % (col1, col1, col1, a - 1, tot - 1, col1, pf(ans)))


def build():
    sets = [S("Addition Rule and complements", collect(one_add, 20, R)),
            S("Independent events", collect(one_ind, 20, R)),
            S("Conditional probability", collect(one_cond, 20, R)),
            S("Two-way tables", collect(one_table, 20, R)),
            S("With and without replacement", collect(one_draw, 20, R))]
    body = lesson(
        "<ul><li><b>Complement</b>: P(not A) = 1 %s P(A).</li>"
        "<li><b>Addition Rule</b>: P(A or B) = P(A) + P(B) %s P(A and B). Subtract the overlap so it is not counted twice.</li>"
        "<li><b>Conditional probability</b>: P(B | A) means the probability of B <b>given</b> A. P(B | A) = P(A and B) ÷ P(A). In a two-way table, use only the row or column you are given.</li>"
        "<li><b>Independent</b> events do not affect each other: P(A and B) = P(A) × P(B), and P(B | A) = P(B).</li></ul>"
        "<p>Drawing <b>without replacement</b> changes the second probability, because one item is gone.</p>" % (MINUS, MINUS),
        [("P(A) = 0.5, P(B) = 0.4 and P(A and B) = 0.2. Are A and B independent?", ["0.5 × 0.4 = 0.2", "This equals P(A and B)"], "Yes"),
         ("A bag has 3 red and 2 blue marbles. Two are drawn without replacement. Find P(both red).", ["3/5 × 2/4"], "3/10")],
        ["Adding P(A) and P(B) without subtracting P(A and B).",
         "Dividing by the grand total when the question says \"given\". Divide by the row or column total.",
         "Mixing up P(A | B) and P(B | A).",
         "Keeping the same total for the second draw without replacement."])
    faq = [("What is conditional probability?", "The probability of an event given that another event has happened. P(B | A) = P(A and B) ÷ P(A)."),
           ("How do you know if two events are independent?", "Check whether P(A and B) = P(A) × P(B), or whether P(B | A) = P(B). If so, they are independent."),
           ("What is the Addition Rule in probability?", "P(A or B) = P(A) + P(B) − P(A and B). For mutually exclusive events, P(A and B) = 0."),
           ("How do you find a conditional probability from a two-way table?", "Use only the row or column for the given condition, and divide the cell count by that row or column total.")]
    make("conditional-probability", 23, "S-CP.A.3",
         "Conditional Probability and Independence",
         "Conditional Probability Worksheet: Independence and Two-Way Tables (Geometry, S-CP) | 100 Questions",
         "Conditional Probability",
         "Understand the conditional probability of A given B as P(A and B)/P(B), and interpret independence of A and B as saying that the conditional probability of A given B is the same as the probability of A, and the conditional probability of B given A is the same as the probability of B.",
         "Free worksheet on conditional probability: the Addition Rule, independent events, P(B | A), two-way tables and drawing without replacement. 100 questions with answers.",
         "P(B | A) = P(A and B) ÷ P(A).",
         "Independent events: P(A and B) = P(A) × P(B). Without replacement, the total goes down.",
         body, faq, sets, R, domain="Probability", grade="geometry")


if __name__ == "__main__":
    build()
