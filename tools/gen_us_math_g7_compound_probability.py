# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Compound Probability (7.SP.C.8)
  python tools/gen_us_math_g7_compound_probability.py
Sample spaces with lists, tables and tree diagrams; probabilities of compound events; simulations.
Wrong answers come from real mistakes: adding the outcomes instead of multiplying (3 shirts and 4 pants
-> 7 outfits), adding probabilities of independent events instead of multiplying, counting HT and TH
as one outcome, and using the wrong total.
"""
import random
from fractions import Fraction as F
from ws_common import (mcq, balance, B, table, example, write_unit, fr)

R = random.Random(71601)
UPDATED = "2026-11-09"


def pf(v):
    v = F(v)
    if v == 0:
        return "0"
    if v == 1:
        return "1"
    return fr(v.numerator, v.denominator)


def mcp(q, v, ws, e):
    v = F(v)
    d = v.denominator
    cands = [(pf(w), F(w)) for w in list(ws) + [v + F(1, d), v - F(1, d), v * 2, v / 2, 1 - v, v * 3, v + F(2, d)] if 0 < F(w) <= 1 and F(w) != v]
    return mcq(q, (pf(v), v), cands, e)


def mcn(q, v, ws, e):
    cands = [(str(w), w) for w in list(ws) + [v + 1, v - 1, v * 2] if w > 0 and w != v]
    return mcq(q, (str(v), v), cands, e)


# ------------------------------------------------------------ set 1: counting outcomes
def set_count():
    its = []
    cases = [("You flip a coin and roll a number cube.", 2, 6), ("You choose a shirt (3 colors) and pants (4 colors).", 3, 4),
             ("You spin a spinner with 5 equal parts and flip a coin.", 5, 2), ("You pick a sandwich (4 kinds) and a drink (3 kinds).", 4, 3),
             ("You roll two number cubes.", 6, 6), ("You pick a letter from A, B, C and a number from 1 to 5.", 3, 5),
             ("You choose a size (small, medium, large) and a flavor (6 flavors).", 3, 6), ("You flip a coin three times.", 2, 4)]
    for q, a, b in cases:
        tot = a * b
        e = "Multiply the choices: %d × %d = %d outcomes. Not %d: adding counts only one choice at a time." % (a, b, tot, a + b)
        if "three times" in q:
            e = "Each flip has 2 outcomes: 2 × 2 × 2 = 8 outcomes (HHH, HHT, HTH, HTT, THH, THT, TTH, TTT)."
            tot = 8
        its.append(mcn("%s How many outcomes are in the sample space?" % q, tot, [a + b, max(a, b), tot - 2], e))
    its.append(mcq("Which list is the sample space for flipping two coins?", ("HH, HT, TH, TT", "a"), [("HH, HT, TT", "b"), ("H, T", "c"), ("HH, TT", "d")],
                   "HT (first heads, then tails) and TH are different outcomes. There are 4."))
    its.append(mcq("A tree diagram shows 3 branches, and each has 4 branches. How many outcomes are at the ends?", ("12", 12), [("7", 7), ("4", 4), ("16", 16)],
                   "3 × 4 = 12 branch ends."))
    its.append(mcq("What is a compound event?", ("An event made of two or more simple events, like rolling a 6 and flipping heads", "a"),
                   [("An event that can never happen", "b"), ("An event with probability 1", "c"), ("Any event with a number cube", "d")],
                   "A compound event combines two or more events."))
    its.append(mcq("A menu has 3 soups, 5 main dishes and 2 desserts. How many meals of one soup, one main and one dessert are possible?", ("30", 30),
                   [("10", 10), ("15", 15), ("60", 60)], "3 × 5 × 2 = 30 meals."))
    its.append(mcq("A lock code uses 3 digits, each 0 to 9. How many codes are possible?", ("1,000", 1000), [("30", 30), ("27", 27), ("729", 729)],
                   "10 × 10 × 10 = 1,000 codes (000 to 999)."))
    for a, b, c in [(2, 3, 4), (4, 2, 5), (3, 3, 2), (2, 2, 6), (5, 4, 2), (6, 2, 2), (3, 4, 5)]:
        its.append(mcn("An outfit has a hat (%d choices), a shirt (%d choices) and shoes (%d choices). How many outfits are possible?" % (a, b, c), a * b * c,
                       [a + b + c, a * b + c, a * b], "%d × %d × %d = %d outfits." % (a, b, c, a * b * c)))
    return {"title": "Sample spaces: counting outcomes", "items": its[:20]}


# ------------------------------------------------------------ set 2: probability from sample space
def set_from_space():
    its = []
    dice = [("a sum of 7", 6), ("a sum of 12", 1), ("doubles (the same number on both)", 6), ("a sum of 10", 3), ("a sum less than 4", 3),
            ("a sum of 2 or 3", 3), ("an even sum", 18), ("a sum of 8", 5)]
    for ev, k in dice:
        v = F(k, 36)
        its.append(mcp("You roll two number cubes (36 outcomes). What is P(%s)?" % ev, v, [F(k, 11) if k < 11 else F(1, 2), F(k, 12) if k < 12 else F(1, 3), F(1, 6) if v != F(1, 6) else F(1, 12)],
                       "%d of the 36 outcomes work: %d/36%s." % (k, k, "" if v.denominator == 36 else " = %d/%d" % (v.numerator, v.denominator))))
    coins = [("exactly 2 heads", 3), ("at least 1 head", 7), ("no heads", 1), ("all three the same", 2)]
    for ev, k in coins:
        its.append(mcp("You flip a coin 3 times (8 outcomes). What is P(%s)?" % ev, F(k, 8), [F(k, 3) if k < 3 else F(1, 2), F(1, 3), F(8 - k, 8)],
                       "List the 8 outcomes: HHH, HHT, HTH, HTT, THH, THT, TTH, TTT. %d of them work: %d/8." % (k, k)))
    cs = [("heads and a 4", F(1, 12)), ("tails and an even number", F(1, 4)), ("heads and a number greater than 4", F(1, 6)), ("tails and a 1 or a 2", F(1, 6))]
    for ev, v in cs:
        its.append(mcp("You flip a coin and roll a number cube (12 outcomes). What is P(%s)?" % ev, v, [F(1, 2) + F(1, 6) if v == F(1, 12) else F(2, 3), F(1, 8), F(1, 2)],
                       "Count the outcomes that work out of 12, or multiply: P = %s." % pf(v)))
    sp = [("A spinner has red, blue and green (equal parts). You spin twice. What is P(red both times)?", F(1, 9), [F(2, 3), F(1, 6), F(1, 3)],
           "3 × 3 = 9 outcomes, and only red-red works: 1/9."),
          ("A spinner has red, blue and green (equal parts). You spin twice. What is P(the same color both times)?", F(1, 3), [F(1, 9), F(2, 3), F(1, 6)],
           "RR, BB and GG: 3 of 9 outcomes = 1/3."),
          ("You pick one of A, B, C and flip a coin. What is P(A and heads)?", F(1, 6), [F(5, 6), F(1, 5), F(1, 3)], "3 × 2 = 6 outcomes. Only A-heads works: 1/6."),
          ("A bag has 1 red and 1 blue cube. You pick one, put it back, then pick again. What is P(two different colors)?", F(1, 2), [F(1, 4), F(3, 4), F(1, 3)],
           "Outcomes: RR, RB, BR, BB. RB and BR work: 2/4 = 1/2.")]
    for q, v, ws, e in sp:
        its.append(mcp(q, v, ws, e))
    return {"title": "Probability from the sample space", "items": its}


# ------------------------------------------------------------ set 3: multiply independent events
def set_multiply():
    its = []
    pairs = [(F(1, 2), F(1, 6), "a coin lands heads", "a number cube shows 3"), (F(1, 4), F(1, 3), "a spinner lands on blue", "you draw a red card from 1 red and 2 black"),
             (F(2, 5), F(1, 2), "you pick a green marble (2 of 5)", "a coin lands tails"), (F(3, 4), F(2, 3), "it is sunny on Monday", "it is sunny on Tuesday (independent)"),
             (F(1, 6), F(1, 6), "the first cube shows 6", "the second cube shows 6"), (F(1, 2), F(1, 2), "the first coin is heads", "the second coin is heads"),
             (F(3, 10), F(1, 2), "you win a game (3 in 10)", "a coin lands heads"), (F(5, 6), F(5, 6), "the first cube is not a 6", "the second cube is not a 6"),
             (F(1, 5), F(3, 4), "a spinner lands on 1 (of 5)", "a different spinner lands on A, B or C (of 4)"), (F(2, 3), F(1, 4), "you pick a vowel from A, E, T", "you draw a heart (1/4)")]
    for a, b, ea, eb in pairs:
        v = a * b
        its.append(mcp("P(%s) = %s and P(%s) = %s. The events are independent. What is the probability that both happen?" % (ea, pf(a), eb, pf(b)), v,
                       [a + b if a + b <= 1 else F(1, 2), (a + b) / 2, max(a, b)],
                       "Multiply: %s × %s = %s. Not %s: adding gives the wrong answer for both events." % (pf(a), pf(b), pf(v), pf(a + b) if a + b <= 1 else "a number over 1")))
    for p, k in [(F(1, 2), 3), (F(1, 2), 4), (F(1, 6), 2), (F(1, 3), 2), (F(1, 2), 5)]:
        v = p ** k
        its.append(mcp("Each try has probability %s and the tries are independent. What is the probability of success %d times in a row?" % (pf(p), k), v,
                       [p * k if p * k <= 1 else F(1, 2), p, p / k], "Multiply %d times: (%s)<sup>%d</sup> = %s." % (k, pf(p), k, pf(v))))
    its.append(mcq("Which events are independent?", ("Flipping a coin and rolling a number cube", "a"),
                   [("Drawing two cards without putting the first back", "b"), ("Picking two students for two jobs from the same group, without repeats", "c"),
                    ("Picking two marbles without replacing the first", "d")], "One result does not change the other. Without replacement, the second draw depends on the first."))
    its.append(mcq("A bag has 3 red and 2 blue marbles. You pick one, put it back, then pick again. What is P(red, then red)?", (pf(F(9, 25)), "a"),
                   [(pf(F(6, 5)), "b"), (pf(F(3, 10)), "c"), (pf(F(6, 25)), "d")], "With replacement: 3/5 × 3/5 = 9/25."))
    its.append(mcq("A bag has 3 red and 2 blue marbles. You pick one and keep it, then pick again. What is P(red, then red)?", (pf(F(3, 10)), "a"),
                   [(pf(F(9, 25)), "b"), (pf(F(6, 25)), "c"), (pf(F(1, 2)), "d")], "Without replacement: 3/5 × 2/4 = 6/20 = 3/10."))
    its.append(mcq("A spinner is half red and half blue. You spin it twice. Which is more likely?", ("One red and one blue (in any order)", "a"),
                   [("Red both times", "b"), ("Blue both times", "c"), ("They are all equally likely", "d")],
                   "RB and BR give 1/4 + 1/4 = 1/2. RR and BB are 1/4 each."))
    its.append(mcq("The chance of rain is 30% on Saturday and 30% on Sunday (independent). What is the chance it rains both days?", ("9%", "a"),
                   [("60%", "b"), ("30%", "c"), ("15%", "d")], "0.3 × 0.3 = 0.09 = 9%."))
    return {"title": "Independent events: multiply", "items": its}


# ------------------------------------------------------------ set 4: tables and trees
def set_tables():
    its = []
    tbl = table(["", "Soccer", "Basketball", "Total"], [["Grade 7", "18", "12", "30"], ["Grade 8", "10", "20", "30"], ["Total", "28", "32", "60"]])
    qs = [("What is the probability that a student picked at random is in Grade 7 and plays soccer?", F(18, 60), [F(18, 30), F(18, 28), F(30, 60)],
           "18 of the 60 students: 18/60 = 3/10."),
          ("What is the probability that a student picked at random plays basketball?", F(32, 60), [F(12, 60), F(32, 28), F(20, 60)], "32 of 60: 32/60 = 8/15."),
          ("A Grade 8 student is picked. What is the probability the student plays basketball?", F(20, 30), [F(20, 60), F(20, 32), F(10, 30)], "Only the 30 Grade 8 students count: 20/30 = 2/3."),
          ("A soccer player is picked. What is the probability the player is in Grade 7?", F(18, 28), [F(18, 60), F(18, 30), F(10, 28)], "Only the 28 soccer players count: 18/28 = 9/14."),
          ("What is the probability that a student is in Grade 8 and plays soccer?", F(10, 60), [F(10, 30), F(10, 28), F(28, 60)], "10 of 60: 10/60 = 1/6.")]
    for q, v, ws, e in qs:
        its.append(mcp("The table shows 60 students and their favorite sport." + tbl + q, v, ws, e))
    tree = [("A tree diagram shows a coin flip (H or T), then a spinner (1, 2 or 3). How many outcomes are there?", 6, [5, 3, 8], "2 × 3 = 6."),
            ("A tree diagram shows 2 drinks, then 3 snacks, then 2 desserts. How many paths are there?", 12, [7, 6, 18], "2 × 3 × 2 = 12."),
            ("A tree shows heads/tails, then a number cube. How many paths end in heads and an odd number?", 3, [6, 1, 4], "Heads, then 1, 3 or 5: 3 paths."),
            ("A tree has 4 first branches and 4 second branches on each. How many paths have the same choice twice?", 4, [16, 8, 2], "AA, BB, CC, DD: 4 paths out of 16.")]
    for q, v, ws, e in tree:
        its.append(mcn(q, v, ws, e))
    pp = [("A coin is flipped twice. What is P(at least one head)?", F(3, 4), [F(1, 2), F(1, 4), F(2, 3)], "HH, HT, TH work: 3/4. Or 1 − P(TT) = 1 − 1/4."),
          ("Two number cubes are rolled. What is P(at least one 6)?", F(11, 36), [F(1, 3), F(1, 36), F(12, 36)], "6 outcomes have a 6 first, 6 have a 6 second, and 6-6 is counted twice: 6 + 6 − 1 = 11. 11/36."),
          ("A family has 3 children. Assuming boys and girls are equally likely, what is P(at least one girl)?", F(7, 8), [F(1, 2), F(3, 8), F(2, 3)], "Only BBB has no girl: 1 − 1/8 = 7/8."),
          ("You guess on 2 true/false questions. What is P(both right)?", F(1, 4), [F(1, 2), F(1, 3), 1], "1/2 × 1/2 = 1/4."),
          ("You guess on 3 multiple-choice questions with 4 choices each. What is P(all 3 right)?", F(1, 64), [F(3, 4), F(1, 12), F(1, 16)], "1/4 × 1/4 × 1/4 = 1/64.")]
    for q, v, ws, e in pp:
        its.append(mcp(q, v, ws, e))
    sims = [("To simulate a 50% chance, which tool works?", "Flip a fair coin", ["Roll a number cube and use 1 only", "Spin a spinner with 3 equal parts", "Draw from 4 cards and use 1"],
             "A fair coin gives heads half the time, matching 50%."),
            ("A player makes 1 out of 6 shots. Which simulation fits?", "Roll a number cube; a 1 means a make", ["Flip a coin; heads means a make", "Spin a spinner with 4 parts", "Pick from 10 cards; 1 to 6 means a make"],
             "A number cube gives 1 with probability 1/6."),
            ("In a simulation of 50 trials, the event happened 12 times. What is the estimated probability?", "12/50 = 0.24", ["12/38", "50/12", "0.12"],
             "Estimate = times it happened ÷ trials = 12/50 = 0.24."),
            ("Which gives a better estimate from a simulation?", "Running many trials", ["Running one trial", "Running 3 trials", "Stopping after the first success"],
             "More trials usually give an estimate closer to the true probability."),
            ("A cereal box has 1 of 4 prizes. To simulate buying boxes, a student spins a spinner with 4 equal parts. What does one spin stand for?",
             "The prize in one box", ["All 4 prizes", "The number of boxes you need", "The cost of a box"], "Each spin picks one of 4 equally likely prizes, like opening one box."),
            ("A simulation for 'a family with 2 children' uses two coin flips. What does HT stand for?", "A boy first, then a girl (if H = boy)", ["Two boys", "Two girls", "Nothing"],
             "Each flip stands for one child, in order.")]
    for q, good, bad, e in sims:
        its.append(mcq(q, (good, "g"), [(b, b) for b in bad], e))
    return {"title": "Tables, tree diagrams and simulations", "items": its}


# ------------------------------------------------------------ set 5: word problems
def set_words():
    its = []
    w = [("A café has 4 sandwiches and 3 drinks. One combo is picked at random. What is P(the turkey sandwich and lemonade)?", F(1, 12), [F(1, 7), F(2, 7), F(1, 4)],
          "4 × 3 = 12 combos, and 1 works: 1/12."),
         ("A password is a letter (A to E) followed by a digit (0 to 9). How many passwords are possible?", 50, [15, 14, 100], "5 × 10 = 50."),
         ("A quiz has 4 true/false questions. How many ways can you answer all of them?", 16, [8, 4, 6], "2 × 2 × 2 × 2 = 16."),
         ("A basketball player makes 80% of free throws. What is P(she makes 2 in a row)?", F(16, 25), [F(4, 5), F(8, 5) / 2, F(1, 25)], "0.8 × 0.8 = 0.64 = 16/25."),
         ("A spinner has 4 equal parts (1 to 4). You spin and roll a number cube. What is P(both show a 1)?", F(1, 24), [F(1, 10), F(1, 4), F(1, 6)], "1/4 × 1/6 = 1/24."),
         ("A light has a 1/10 chance of being red when you arrive. You pass 2 lights (independent). What is P(both red)?", F(1, 100), [F(1, 5), F(1, 20), F(1, 10)], "1/10 × 1/10 = 1/100."),
         ("A bag has 2 red, 3 blue and 5 green tiles. You pick one, replace it, and pick again. What is P(red, then green)?", F(1, 10), [F(7, 10), F(7, 20), F(1, 5)],
          "2/10 × 5/10 = 10/100 = 1/10."),
         ("Ana rolls two number cubes. What is P(the sum is 9)?", F(1, 9), [F(1, 6), F(9, 36), F(1, 11)], "(3,6), (4,5), (5,4), (6,3): 4/36 = 1/9."),
         ("A license plate uses 2 letters (A to Z) followed by 1 digit. How many plates are possible?", 6760, [62, 520, 676], "26 × 26 × 10 = 6,760."),
         ("You flip a coin 4 times. What is P(all heads)?", F(1, 16), [F(1, 4), F(1, 8), F(1, 2)], "(1/2)⁴ = 1/16."),
         ("A game spinner lands on 'win' 1/3 of the time. What is P(you lose two spins in a row)?", F(4, 9), [F(2, 3), F(1, 9), F(1, 3)], "P(lose) = 2/3. 2/3 × 2/3 = 4/9."),
         ("A test has 2 multiple-choice questions with 5 choices each. A student guesses. What is P(both wrong)?", F(16, 25), [F(4, 5), F(1, 25), F(8, 25)], "P(wrong) = 4/5. 4/5 × 4/5 = 16/25."),
         ("A restaurant has 5 main dishes and 4 desserts. You pick one of each at random. What is P(pasta and cake)?", F(1, 20), [F(1, 9), F(2, 9), F(1, 5)], "5 × 4 = 20 meals: 1/20."),
         ("A drawer has 4 black and 4 white socks. You take one, keep it, then take another. What is P(both black)?", F(3, 14), [F(1, 4), F(1, 2), F(3, 16)],
          "4/8 × 3/7 = 12/56 = 3/14."),
         ("Two friends each pick a number from 1 to 5. What is P(they pick the same number)?", F(1, 5), [F(1, 25), F(2, 5), F(1, 10)], "25 pairs, and 5 match: 5/25 = 1/5."),
         ("A weather app says 40% chance of rain each day for 2 days (independent). What is P(no rain on both days)?", F(9, 25), [F(3, 5), F(4, 25), F(1, 5)],
          "P(no rain) = 0.6. 0.6 × 0.6 = 0.36 = 9/25."),
         ("A coin is flipped and a 4-section spinner (red, blue, green, yellow) is spun. How many outcomes have heads or red?", 5, [3, 8, 6],
          "Heads with any color: 4. Tails with red: 1. Total 5."),
         ("A class picks a president and a vice president from 5 students (different people). How many ways?", 20, [25, 10, 9], "5 choices, then 4: 5 × 4 = 20."),
         ("A machine part fails 1 in 50 times. Two parts are used and work independently. What is P(neither fails)?", F(2401, 2500), [F(49, 50), F(24, 25), F(1, 2500)],
          "49/50 × 49/50 = 2,401/2,500."),
         ("A spinner has 3 equal parts: A, B, C. You spin 3 times. What is P(A, B, C in that order)?", F(1, 27), [F(1, 3), F(1, 9), F(1, 6)], "1/3 × 1/3 × 1/3 = 1/27.")]
    for q, v, ws, e in w:
        if isinstance(v, int):
            its.append(mcq(q, ("{:,}".format(v), v), [("{:,}".format(x), x) for x in ws if x != v], e))
        else:
            its.append(mcp(q, v, ws, e))
    return {"title": "Word problems", "items": its}


def body():
    rows = [["List", "Coin + coin", "HH, HT, TH, TT"], ["Table", "Two number cubes", "6 rows × 6 columns = 36"], ["Tree diagram", "Shirt (3) then pants (4)", "3 × 4 = 12 paths"]]
    return ("<h2>Sample spaces</h2><p>A <b>compound event</b> is made of two or more events. Its <b>sample space</b> is every possible outcome. "
            "Show it with a list, a table or a tree diagram. To count outcomes, <b>multiply</b> the number of choices at each step.</p>"
            + table(["Way to show it", "Example", "Outcomes"], rows)
            + "<h2>Probability of a compound event</h2><p>P = favorable outcomes ÷ all outcomes. For <b>independent</b> events (one does not change the other), "
            "multiply: P(A and B) = P(A) × P(B).</p>"
            + example("Flip a coin and roll a number cube. What is P(heads and 4)?", ["2 × 6 = 12 outcomes. Only H4 works.", "Or multiply: " + fr(1, 2) + " × " + fr(1, 6) + " = " + fr(1, 12) + "."], fr(1, 12))
            + example("A bag has 3 red and 2 blue marbles. Pick one, keep it, pick again. P(red, red)?", [fr(3, 5) + " × " + fr(2, 4) + " = " + fr(6, 20) + " = " + fr(3, 10) + "."], fr(3, 10))
            + "<h2>Common mistakes</h2><ul><li>Adding instead of multiplying: 3 shirts and 4 pants make 12 outfits, not 7.</li>"
            "<li>Counting HT and TH as one outcome.</li><li>Forgetting that without replacement, the second draw has one fewer item.</li></ul>")


def main():
    sets = [set_count(), set_from_space(), set_multiply(), set_tables(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "compound-probability",
        "title": "Compound Probability",
        "seo_title": "Grade 7 Compound Probability Worksheets: Sample Spaces, Tree Diagrams and Independent Events",
        "short_title": "Compound probability",
        "domain": "Statistics & Probability",
        "standard_code": "7.SP.C.8",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/SP/C/8/",
        "standard_text": "Find probabilities of compound events using organized lists, tables, tree diagrams, and simulation.",
        "meta_desc": "Free Grade 7 compound probability worksheets: sample spaces with lists, tables and tree diagrams, the counting principle, independent events, with and without replacement, simulations and word problems. 100 practice questions with an answer key.",
        "key_big": "Count outcomes by multiplying. For independent events, multiply the probabilities.",
        "key_sub": "Coin and number cube: 2 × 6 = 12 outcomes. P(heads and 4) = 1/2 × 1/6 = 1/12.",
        "body_html": body(),
        "faq": [
            {"q": "What is a compound event?", "a": "An event made of two or more simple events, like flipping heads and rolling a 4."},
            {"q": "How do you find the number of outcomes?", "a": "Multiply the number of choices at each step. 3 shirts and 4 pants make 3 × 4 = 12 outfits."},
            {"q": "How do you find the probability of two independent events?", "a": "Multiply their probabilities: P(A and B) = P(A) × P(B)."},
            {"q": "What changes without replacement?", "a": "After the first pick, there is one fewer item, so the second probability changes. With 3 red and 2 blue, P(red, red) = 3/5 × 2/4."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 16,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
