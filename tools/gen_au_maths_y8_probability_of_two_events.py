# -*- coding: utf-8 -*-
"""
AU Year 8 Maths: Probability of Two Events (Australian Curriculum v9.0: AC9M8P02)
  python3 tools/gen_au_maths_y8_probability_of_two_events.py
Sample spaces for two dice and for a coin with a spinner, complementary events and tree diagrams,
Venn diagrams, two-way tables, and mutually exclusive events.
Wrong answers come from real mistakes: counting 2 + 5 and 5 + 2 as one outcome, using the wrong total,
forgetting that P(not A) = 1 − P(A), counting the overlap of a Venn diagram twice, and adding probabilities of
events that can happen together.
"""
import random
from fractions import Fraction as F
from au_hs import num, mcq, B, S, make, lesson, collect, QN, T, fr, table, svg_wrap, text, fig, INK, RED, BLUE, GREEN

R = random.Random(81801)


def pf(v):
    v = F(v)
    return "0" if v == 0 else "1" if v == 1 else fr(v.numerator, v.denominator)


def QP(q, ans, wrongs, e):
    ans = F(ans)
    cands = []
    for w in wrongs:
        if w is None:
            continue
        if isinstance(w, str):
            cands.append((w, w))
        else:
            w = F(w)
            if 0 <= w <= 1:
                cands.append((pf(w), pf(w)))
    for d in (F(1, ans.denominator), F(-1, ans.denominator), F(1, 2 * ans.denominator)):
        if 0 < ans + d <= 1:
            cands.append((pf(ans + d), pf(ans + d)))
    cands.append((pf(1 - ans), pf(1 - ans)))
    return mcq(q, (pf(ans), pf(ans)), cands, e)


# ------------------------------------------------------------ set 1: two dice sample space
def one_dice(r):
    op = r.choice(["sum", "sum", "product", "difference"])
    f = {"sum": lambda a, b: a + b, "product": lambda a, b: a * b, "difference": lambda a, b: abs(a - b)}[op]
    vals = [f(a, b) for a in range(1, 7) for b in range(1, 7)]
    kind = r.random()
    if kind < 0.5:
        t = r.choice(sorted(set(vals)))
        cnt = vals.count(t)
        ev = "a %s of %d" % (op, t) if op != "difference" else "a difference of %d" % t
    else:
        cond = r.choice(["more than", "less than", "even", "a multiple of 3"])
        if cond in ("more than", "less than"):
            t = r.choice(sorted(set(vals))[2:-2])
            cnt = sum(1 for v in vals if (v > t if cond == "more than" else v < t))
            ev = "a %s %s %d" % (op, cond, t)
        elif cond == "even":
            cnt = sum(1 for v in vals if v % 2 == 0)
            ev = "an even %s" % op
        else:
            cnt = sum(1 for v in vals if v % 3 == 0)
            ev = "a %s that is a multiple of 3" % op
    if cnt == 0:
        return None
    ans = F(cnt, 36)
    q = "Two fair dice are rolled and the scores are %s. What is the probability of %s?" % (
        {"sum": "added", "product": "multiplied", "difference": "subtracted (larger − smaller)"}[op], B(ev))
    e = "Draw a 6 × 6 sample space: 36 equally likely outcomes. %d of them %s %s, so P = %s%s." % (
        cnt, "gives" if cnt == 1 else "give", ev, fr(cnt, 36), (" = <b>%s</b>" % pf(ans)) if ans.denominator != 36 else "")
    if ans.denominator == 36:
        e = e[:-1] + "" if False else e.replace("P = %s." % fr(cnt, 36), "P = <b>%s</b>." % pf(ans))
    distinct = len(set(vals))
    return QP(q, ans, [F(cnt, distinct) if cnt < distinct else None, F(cnt, 12), F((cnt + 1) // 2, 21)], e)


def one_coin_spinner(r):
    n = r.choice([3, 4, 5])
    cols = ["red", "blue", "green", "yellow", "white"][:n]
    target = r.choice(cols)
    side = r.choice(["heads", "tails"])
    total = 2 * n
    if r.random() < 0.5:
        q = "A coin is flipped and a fair spinner with %d equal sections (%s) is spun. What is the probability of %s and %s?" % (n, ", ".join(cols), side, B(target))
        ans = F(1, total)
        e = "There are 2 × %d = %d equally likely outcomes, and only one is (%s, %s): <b>%s</b>." % (n, total, side, target, pf(ans))
        return QP(q, ans, [F(1, 2) + F(1, n), F(2, total), F(1, n)], e)
    q = "A coin is flipped and a fair spinner with %d equal sections (%s) is spun. How many outcomes are possible?" % (n, ", ".join(cols))
    return QN(q, total, [n + 2, n, 2 ** n if 2 ** n != total else n * 3], "2 outcomes for the coin × %d for the spinner = <b>%d</b>." % (n, total))


# ------------------------------------------------------------ set 2: listing outcomes
def one_list(r):
    kind = r.randint(0, 3)
    if kind == 0:
        mains, sides = r.randint(2, 5), r.randint(2, 4)
        drinks = r.randint(2, 4)
        q = "A café offers %d main courses, %d side dishes and %d drinks. How many different meals of one main, one side and one drink are there?" % (mains, sides, drinks)
        ans = mains * sides * drinks
        return QN(q, ans, [mains + sides + drinks, mains * sides, ans * 2], "Multiply the number of choices: %d × %d × %d = <b>%d</b>." % (mains, sides, drinks, ans))
    if kind == 1:
        n = r.randint(2, 4)
        q = "%d coins are flipped. How many different outcomes are there (such as HHT)?" % n
        return QN(q, 2 ** n, [2 * n, n + 1, n * n if n * n != 2 ** n else 2 ** n + 2], "Each coin has 2 outcomes: 2<sup>%d</sup> = <b>%d</b>." % (n, 2 ** n))
    if kind == 2:
        letters = r.choice(["ABC", "XYZ", "PQR"])
        q = "How many different ways can the letters %s be arranged in a row?" % B(letters)
        return QN(q, 6, [3, 9, 27], "3 choices for the first letter, 2 for the second, 1 for the last: 3 × 2 × 1 = <b>6</b>.")
    digits = r.choice([[1, 2, 3], [2, 5, 7], [4, 6, 8]])
    q = "Two-digit numbers are made from the cards %s, using two different cards. How many numbers can be made?" % B(", ".join(str(d) for d in digits))
    return QN(q, 6, [3, 9, 8], "Listing: %s. That is <b>6</b>." % ", ".join(str(a) + str(b) for a in digits for b in digits if a != b))


# ------------------------------------------------------------ set 2: complementary events and tree diagrams
def one_comp(r):
    kind = r.choice(["dec", "pct", "frac", "count"])
    if kind == "dec":
        p = F(r.randint(5, 95), 100)
        ev = r.choice([("it rains in Darwin on a day in March", "it does not rain"), ("a bus is late", "the bus is not late"),
                       ("a seed germinates", "it does not germinate"), ("a netball goal shooter scores from a shot", "she misses")])
        q = "The probability that %s is %s. What is the probability that %s?" % (ev[0], num(p), ev[1])
        return QN(q, 1 - p, [p, 1 + p if 1 + p < 2 else None, 100 - p * 100 if False else 1 - p + F(1, 10)], "Complementary events add to 1: 1 − %s = <b>%s</b>." % (num(p), num(1 - p)), near=(F(1, 10), F(-1, 10)))
    if kind == "pct":
        p = r.randint(3, 97)
        q = "A weather forecast gives a %d%% chance of rain tomorrow. What is the chance it does not rain?" % p
        return QN(q, 100 - p, [p, 100 + p if False else 50, 1 - F(p, 100) if False else 100 - p + 10], "The chances add to 100%%: 100%% − %d%% = <b>%d%%</b>." % (p, 100 - p), unit="%", near=(5, -5))
    if kind == "frac":
        d = r.choice([5, 6, 8, 9, 10, 12, 20])
        k = r.randint(1, d - 1)
        p = F(k, d)
        q = "The probability of picking a green marble from a bag is %s. What is the probability of NOT picking a green marble?" % fr(p.numerator, p.denominator)
        right = 1 - p
        wr = [p, F(d - k, d + k), F(1, d)]
        cands = [(fr(w.numerator, w.denominator), w) for w in wr if w != right and 0 < w < 1]
        return mcq(q, (fr(right.numerator, right.denominator), right), cands + [("1", F(1))], "P(not green) = 1 − %s = <b>%s</b>." % (fr(p.numerator, p.denominator), fr(right.numerator, right.denominator)))
    tot = r.choice([20, 25, 30, 40, 50])
    k = r.randint(2, tot - 2)
    q = "A class of %d students has %d who play a musical instrument. A student is chosen at random. What is the probability that the student does NOT play an instrument?" % (tot, k)
    right = F(tot - k, tot)
    wr = [F(k, tot), F(tot - k, k) if tot - k < k else F(1, tot), F(1, 2) if right != F(1, 2) else F(1, 3)]
    cands = [(fr(w.numerator, w.denominator), w) for w in wr if w != right and 0 < w < 1]
    return mcq(q, (fr(right.numerator, right.denominator), right), cands + [(fr(k, tot - k) if k < tot - k else "1", "x")],
               "%d − %d = %d students do not play, so the probability is <b>%s</b>." % (tot, k, tot - k, fr(right.numerator, right.denominator)))


def tree_svg():
    s = ["<line x1='20' y1='110' x2='120' y2='50' stroke='%s' stroke-width='2'/>" % INK,
         "<line x1='20' y1='110' x2='120' y2='170' stroke='%s' stroke-width='2'/>" % INK,
         "<line x1='140' y1='50' x2='240' y2='20' stroke='%s' stroke-width='2'/>" % INK,
         "<line x1='140' y1='50' x2='240' y2='80' stroke='%s' stroke-width='2'/>" % INK,
         "<line x1='140' y1='170' x2='240' y2='140' stroke='%s' stroke-width='2'/>" % INK,
         "<line x1='140' y1='170' x2='240' y2='200' stroke='%s' stroke-width='2'/>" % INK,
         text(130, 55, "H", 16), text(130, 175, "T", 16), text(252, 25, "H", 16), text(252, 85, "T", 16), text(252, 145, "H", 16), text(252, 205, "T", 16),
         text(60, 72, "½", 15, col=RED), text(60, 158, "½", 15, col=RED), text(190, 26, "½", 15, col=RED), text(190, 80, "½", 15, col=RED),
         text(190, 146, "½", 15, col=RED), text(190, 200, "½", 15, col=RED),
         text(300, 25, "HH", 15), text(300, 85, "HT", 15), text(300, 145, "TH", 15), text(300, 205, "TT", 15)]
    return svg_wrap(340, 220, "".join(s), "tree diagram for two coin flips")


def trees():
    tv = fig(tree_svg())
    data = [
        ("The tree diagram shows two flips of a fair coin. How many outcomes are there?%s" % tv, "4", ["2", "3", "6"], "HH, HT, TH and TT: <b>4</b> outcomes."),
        ("The tree diagram shows two flips of a fair coin. What is P(two heads)?%s" % tv, fr(1, 4), [fr(1, 2), fr(1, 3), fr(2, 4)], "1 of the 4 outcomes: ½ × ½ = <b>¼</b>."),
        ("The tree diagram shows two flips of a fair coin. What is P(one head and one tail)?%s" % tv, fr(1, 2), [fr(1, 4), fr(1, 3), fr(3, 4)], "HT and TH: 2 of the 4 outcomes = <b>½</b>."),
        ("The tree diagram shows two flips of a fair coin. What is P(at least one tail)?%s" % tv, fr(3, 4), [fr(1, 4), fr(1, 2), fr(2, 3)], "Every outcome except HH: 1 − ¼ = <b>¾</b>."),
        ("A coin is flipped and a fair die is rolled. How many outcomes are there?", "12", ["8", "6", "2"], "2 × 6 = <b>12</b> outcomes."),
        ("A family has two children. Assuming boys and girls are equally likely, what is the probability that both are girls?", fr(1, 4), [fr(1, 2), fr(1, 3), fr(2, 3)], "GG is 1 of 4 outcomes (BB, BG, GB, GG): <b>¼</b>."),
        ("P(it rains on Saturday) = 0.3 and the weather on Sunday does not depend on Saturday, with P(rain) = 0.3. What is P(no rain on either day)?", "0.49", ["0.4", "0.7", "0.09"], "P(no rain) = 0.7 each day: 0.7 × 0.7 = <b>0.49</b>."),
        ("A spinner has 3 equal parts: red, blue and yellow. It is spun twice. How many outcomes are on the tree diagram?", "9", ["6", "3", "5"], "3 × 3 = <b>9</b> outcomes."),
    ]
    return [T(q, a, w, e) for q, a, w, e in data]


# ------------------------------------------------------------ set 3: Venn diagrams
def venn_svg(a_only, both, b_only, outside, la, lb):
    s = ["<rect x='6' y='6' width='328' height='178' rx='6' fill='none' stroke='%s' stroke-width='2'/>" % INK,
         "<circle cx='130' cy='98' r='70' fill='rgba(31,95,168,0.12)' stroke='%s' stroke-width='2.5'/>" % BLUE,
         "<circle cx='210' cy='98' r='70' fill='rgba(192,57,43,0.10)' stroke='%s' stroke-width='2.5'/>" % RED,
         text(100, 104, str(a_only), 18), text(170, 104, str(both), 18), text(240, 104, str(b_only), 18), text(310, 170, str(outside), 18),
         text(80, 30, la, 14, col=BLUE), text(262, 30, lb, 14, col=RED)]
    return svg_wrap(340, 190, "".join(s), "Venn diagram")


def one_venn(r):
    a_only, both, b_only, out = r.randint(2, 15), r.randint(1, 9), r.randint(2, 15), r.randint(1, 10)
    tot = a_only + both + b_only + out
    la, lb = r.choice([("Football", "Tennis"), ("Cats", "Dogs"), ("Maths", "Art"), ("Swimming", "Cycling")])
    svg = venn_svg(a_only, both, b_only, out, la, lb)
    kind = r.randint(0, 3)
    if kind == 0:
        cnt, ev = both, "like both %s and %s" % (la.lower(), lb.lower())
        wr = [F(both, a_only + both + b_only), F(a_only + both, tot), F(both + b_only, tot)]
    elif kind == 1:
        cnt, ev = a_only + both + b_only, "like %s or %s (or both)" % (la.lower(), lb.lower())
        wr = [F(a_only + 2 * both + b_only, tot) if a_only + 2 * both + b_only <= tot else None, F(a_only + b_only, tot), F(cnt, tot - out)]
    elif kind == 2:
        cnt, ev = a_only + both, "like %s" % la.lower()
        wr = [F(a_only, tot), F(a_only + both, tot - out), F(both, tot)]
    else:
        cnt, ev = out, "like neither"
        wr = [F(out, tot - out), F(a_only + b_only, tot), F(both, tot)]
    ans = F(cnt, tot)
    q = "The Venn diagram shows what %d students like. A student is chosen at random. What is the probability they %s?%s" % (tot, B(ev), fig(svg))
    e = "Count the numbers in the right regions: %d out of %d. P = <b>%s</b>." % (cnt, tot, pf(ans))
    return QP(q, ans, wr, e)


# ------------------------------------------------------------ set 4: two-way tables
def one_twoway(r):
    a, b, c, d = [r.randint(3, 25) for _ in range(4)]
    rows, cols = r.choice([(("Boys", "Girls"), ("Walk", "Bus")), (("Year 7", "Year 8"), ("Lunch from home", "Canteen lunch")),
                           (("Adults", "Children"), ("Left-handed", "Right-handed")), (("Boys", "Girls"), ("Football", "Netball"))])
    tot = a + b + c + d
    tbl = table(["", cols[0], cols[1], "Total"], [[rows[0], str(a), str(b), str(a + b)], [rows[1], str(c), str(d), str(c + d)], ["Total", str(a + c), str(b + d), str(tot)]])
    kind = r.randint(0, 2)
    if kind == 0:
        cnt, den, ev = a, tot, "is in the “%s” row and the “%s” column" % (rows[0], cols[0])
        wr = [F(a, a + b), F(a, a + c), F(a + c, tot)]
    elif kind == 1:
        cnt, den, ev = b + d, tot, "is in the “%s” column" % cols[1]
        wr = [F(b, tot), F(d, tot), F(b + d, b + d + a)]
    else:
        cnt, den, ev = c, c + d, "is in the “%s” column, if you already know they are in the “%s” row" % (cols[0], rows[1])
        wr = [F(c, tot), F(c, a + c), F(d, c + d)]
    ans = F(cnt, den)
    q = "A person is chosen at random from the table. What is the probability that the person %s?%s" % (ev, tbl)
    e = "%d out of %d: <b>%s</b>." % (cnt, den, pf(ans))
    return QP(q, ans, wr, e)


# ------------------------------------------------------------ set 5: mutually exclusive events and problems
def problems():
    its = []
    data = [
        ("A spinner can land on red, blue or green. P(red) = 0.3 and P(blue) = 0.45. What is P(red or blue)?", "0.75", ["0.135", "0.25", "0.15"], "Red and blue cannot happen together, so add: 0.3 + 0.45 = <b>0.75</b>."),
        ("A spinner can land on red, blue or green. P(red) = 0.3 and P(blue) = 0.45. What is P(green)?", "0.25", ["0.75", "0.15", "0.55"], "1 − 0.3 − 0.45 = <b>0.25</b>."),
        ("A bag has 3 red, 5 blue and 2 green counters. What is P(red or green)?", fr(1, 2), [fr(5, 10) + " … no", fr(6, 100), fr(3, 10)], "3 + 2 = 5 out of 10 = <b>1/2</b>.".replace("1/2", fr(1, 2))),
        ("Which pair of events are mutually exclusive when one die is rolled?", "Getting a 2 and getting an odd number", ["Getting a 2 and getting an even number", "Getting a 6 and getting a number more than 4", "Getting a 3 and getting a prime"],
         "A 2 is never odd, so <b>getting a 2 and getting an odd number</b> cannot happen together."),
        ("When one card is picked from a normal pack, why can you NOT add P(heart) and P(king) to find P(heart or king)?", "The king of hearts would be counted twice", ["Because there are 52 cards", "Because hearts are red", "You can add them"],
         "The events overlap: the king of hearts is in both, so adding counts it <b>twice</b>. (The answer is 16/52.)"),
        ("Two fair coins are flipped. What is the probability of at least one head?", fr(3, 4), [fr(1, 2), fr(1, 4), fr(2, 3)], "HH, HT, TH, TT: 3 of the 4 have a head: <b>3/4</b>.".replace("3/4", fr(3, 4))),
        ("Two fair dice are rolled. What is the probability that both show a 6?", fr(1, 36), [fr(1, 6), fr(2, 12), fr(1, 12)], "Only (6, 6) out of 36 outcomes: <b>1/36</b>.".replace("1/36", fr(1, 36))),
        ("Two fair dice are rolled. What is the probability of a double (both the same)?", fr(1, 6), [fr(1, 36), fr(1, 12), fr(1, 2)], "(1,1), (2,2), … (6,6): 6 out of 36 = <b>1/6</b>.".replace("1/6", fr(1, 6))),
        ("A fair die is rolled and a coin is flipped 60 times. How many times would you expect a 6 and a head?", "5", ["10", "30", "12"], "P(6 and head) = 1/12. 1/12 × 60 = <b>5</b>."),
        ("In a class, 18 students have a sister, 12 have a brother, 5 have both and 3 have neither. How many students are in the class?", "28", ["38", "33", "30"], "Sister only 13, both 5, brother only 7, neither 3: 13 + 5 + 7 + 3 = <b>28</b>."),
        ("The probability that Leo is late is 0.2. The probability that he is on time is 0.7. What is the probability that he is early?", "0.1", ["0.9", "0.5", "0.14"], "The three outcomes add up to 1: 1 − 0.2 − 0.7 = <b>0.1</b>."),
        ("Which of these is NOT a possible list of probabilities for three outcomes that cover everything?", "0.5, 0.4, 0.2", ["0.5, 0.3, 0.2", "0.1, 0.1, 0.8", "0.25, 0.25, 0.5"], "0.5 + 0.4 + 0.2 = 1.1, which is more than 1: <b>0.5, 0.4, 0.2</b>."),
        ("A menu has 4 starters and 6 mains. How many starter-and-main pairs are possible?", "24", ["10", "46", "12"], "4 × 6 = <b>24</b>."),
        ("A 4-digit PIN uses the digits 0–9 and digits can repeat. How many PINs are possible?", "10 000", ["40", "9999", "5040"], "10 × 10 × 10 × 10 = <b>10 000</b>."),
        ("A spinner numbered 1 to 4 is spun twice and the scores are added. What is the most likely total?", "5", ["4", "8", "All totals are equally likely"], "Totals 2–8. 5 can be made 4 ways (1+4, 2+3, 3+2, 4+1), more than any other: <b>5</b>."),
        ("A spinner numbered 1 to 4 is spun twice and the scores are added. What is P(total = 5)?", fr(1, 4), [fr(1, 7), fr(4, 8), fr(1, 16)], "4 of the 16 outcomes give 5: <b>1/4</b>.".replace("1/4", fr(1, 4))),
    ]
    for q, a, w, e in data:
        if "… no" in w[0]:
            w = [fr(5, 8), fr(6, 100), fr(3, 10)]
        its.append(T(q, a, w, e))
    tb = table(["+", "1", "2", "3"], [["1", "2", "3", "4"], ["2", "3", "4", "5"], ["3", "4", "5", "6"]])
    its.append(T("Two spinners numbered 1 to 3 are spun and the scores added. The sample space is shown. What is P(total = 4)?%s" % tb, fr(1, 3), [fr(1, 9), fr(4, 9), fr(1, 5)],
                 "3 of the 9 outcomes are 4: 3/9 = <b>1/3</b>.".replace("1/3", fr(1, 3))))
    its.append(T("Two spinners numbered 1 to 3 are spun and the scores added. The sample space is shown. What is P(total is even)?%s" % tb, fr(5, 9), [fr(4, 9), fr(1, 2), fr(3, 5)],
                 "Even totals: 2, 4, 4, 4, 6 — that is 5 of the 9 outcomes: <b>5/9</b>.".replace("5/9", fr(5, 9))))
    vs = venn_svg(7, 4, 6, 3, "Hockey", "Netball")
    its.append(T("The Venn diagram shows which sports 20 students play. How many play exactly one sport?%s" % fig(vs), "13", ["17", "4", "11"], "Hockey only 7 + netball only 6 = <b>13</b>."))
    its.append(T("The Venn diagram shows which sports 20 students play. A student who plays hockey is chosen. What is the probability they also play netball?%s" % fig(vs), fr(4, 11), [fr(4, 20), fr(4, 10), fr(7, 11)],
                 "11 play hockey and 4 of them also play netball: <b>4/11</b>.".replace("4/11", fr(4, 11))))
    return its


def body():
    return lesson(
        "<p>When two things happen, list all the equally likely outcomes in a <b>sample space</b> (a grid or a list). "
        "P(event) = number of outcomes that work ÷ total number of outcomes.</p>"
        "<p>In a <b>Venn diagram</b>, the overlap is in both groups — count it once. Two events are <b>mutually exclusive</b> "
        "if they cannot happen together; then P(A or B) = P(A) + P(B).</p>"
        + table(["+", "1", "2", "3", "4", "5", "6"], [[str(a)] + [str(a + b) for b in range(1, 7)] for a in range(1, 7)]),
        [("Two dice are rolled. Find P(total of 9).", ["(3,6), (4,5), (5,4), (6,3): 4 ways.", "4 out of 36."], fr(1, 9)),
         ("P(red) = 0.2, P(blue) = 0.5 on a spinner. Find P(red or blue).", ["Mutually exclusive, so add."], "0.7")],
        ["Counting 4 + 5 and 5 + 4 as one outcome — they are different.",
         "Using 11 possible totals as the denominator for two dice instead of 36 outcomes.",
         "Counting the overlap in a Venn diagram twice.",
         "Adding probabilities of events that can happen at the same time."])


def main():
    sets = [S("Sample spaces", collect(one_dice, 14, R) + collect(one_coin_spinner, 6, R)),
            S("Complementary events and tree diagrams", collect(one_comp, 12, R) + trees()),
            S("Venn diagrams", collect(one_venn, 20, R)),
            S("Two-way tables", collect(one_twoway, 20, R)),
            S("Mutually exclusive events and problems", problems())]
    make(8, "probability-of-two-events", 18, "AC9M8P02",
         "Probability of Two Events: Sample Spaces, Tree Diagrams, Venn Diagrams and Two-Way Tables",
         "Year 8 Probability Worksheets: Two-Way Tables, Venn Diagrams, Tree Diagrams and Complementary Events (Free, Answer Key)",
         "Probability of two events",
         "determine all possible combinations for 2 events, using two-way tables, tree diagrams and Venn diagrams, and use these "
         "to determine probabilities of specific outcomes in practical situations",
         "Free Year 8 maths worksheets on probability for the Australian Curriculum (AC9M8P02, AC9M8P01): sample spaces for two dice, "
         "complementary events, tree diagrams, Venn diagrams and two-way tables. 100 questions with an answer key.",
         "List every equally likely outcome in a sample space, then count the ones that work.",
         "Count the overlap of a Venn diagram once. Add probabilities only for mutually exclusive events.",
         body(),
         [("What is a sample space diagram?", "A table or list of every possible outcome. For two dice it is a 6 × 6 grid with 36 outcomes."),
          ("How do I find probabilities from a Venn diagram?", "Add the numbers in the regions you need and divide by the total of all the numbers, including the ones outside the circles."),
          ("What does mutually exclusive mean?", "The events cannot happen at the same time, such as rolling a 2 and rolling a 5 with one die."),
          ("What are complementary events?", "Two events where exactly one must happen, such as rain and no rain. Their probabilities add to 1, so P(not A) = 1 − P(A)."),
          ("How do I count combinations?", "Multiply the number of choices for each part. 3 mains and 4 drinks give 3 × 4 = 12 meals.")],
         sets, R)


if __name__ == "__main__":
    main()
