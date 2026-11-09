# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Probability (7.SP.C.5, 7.SP.C.6, 7.SP.C.7)
  python tools/gen_us_math_g7_probability.py
Likelihood from 0 to 1, theoretical probability, the complement, experimental probability
and predictions. Wrong answers come from real mistakes: writing favorable : unfavorable
instead of favorable ÷ total, forgetting to subtract from 1 for "not", using the total of
one color as the denominator, and expecting experimental results to match exactly.
"""
import math
import random
from fractions import Fraction as F
from ws_common import (num, frac, mcq, balance, People, B, fig, figure, svg_wrap, text, table, example,
                       write_unit, GREEN, BLUE, RED, INK, fr)

R = random.Random(70901)
UPDATED = "2026-11-09"
COLS = {"red": "#c0392b", "blue": "#1f5fa8", "green": "#2e8b57", "yellow": "#e0b000", "purple": "#7d3c98"}


def pf(v):
    v = F(v)
    if v == 0:
        return "0"
    if v == 1:
        return "1"
    return fr(v.numerator, v.denominator)


def opt(v):
    return (pf(v), F(v))


def mcp(q, v, ws, e):
    v = F(v)
    d = v.denominator
    ws = list(ws) + [v + F(1, d), v - F(1, d), v / 2, F(v.numerator, d + 1)]
    cands = [opt(w) for w in ws if 0 <= F(w) <= 1 and F(w) != v]
    return mcq(q, opt(v), cands, e)


def spinner(parts, label="spinner"):
    """parts: list of colour names, equal sections."""
    W, H, cx, cy, r = 200, 200, 100, 100, 82
    n = len(parts)
    s = []
    for i, c in enumerate(parts):
        a1 = 2 * math.pi * i / n - math.pi / 2
        a2 = 2 * math.pi * (i + 1) / n - math.pi / 2
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='#fff' stroke-width='2'/>" % (cx, cy, x1, y1, r, r, x2, y2, COLS[c]))
        am = (a1 + a2) / 2
        s.append(text(cx + r * 0.62 * math.cos(am), cy + r * 0.62 * math.sin(am) + 5, c[0].upper(), 14, col="#fff"))
    s.append("<circle cx='%d' cy='%d' r='%d' fill='none' stroke='%s' stroke-width='2'/>" % (cx, cy, r, INK))
    s.append("<path d='M%d %d L%d %d' stroke='%s' stroke-width='4'/><circle cx='%d' cy='%d' r='6' fill='%s'/>" % (cx, cy, cx + 30, cy - 40, INK, cx, cy, INK))
    return svg_wrap(W, H, "".join(s), label)


def bag(counts, label="marbles in a bag"):
    """counts: [(colour, n)]. Drawn as rows of marbles."""
    items = [c for c, k in counts for _ in range(k)]
    per = 8
    rows = (len(items) + per - 1) // per
    W, H = 30 * per + 20, 30 * rows + 20
    s = []
    for i, c in enumerate(items):
        x, y = 25 + (i % per) * 30, 25 + (i // per) * 30
        s.append("<circle cx='%d' cy='%d' r='12' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y, COLS[c], INK))
    return svg_wrap(W, H, "".join(s), label)


# ------------------------------------------------------------ set 1
def set_likelihood():
    its = []
    words = [("impossible", F(0)), ("certain", F(1)), ("equally likely as not", F(1, 2)), ("unlikely", F(1, 5)), ("likely", F(4, 5))]
    for w, v in words:
        bad = [x for x in [F(0), F(1, 5), F(1, 2), F(4, 5), F(1)] if x != v][:3]
        its.append(mcp("Which probability best describes an event that is %s?" % B(w), v, bad,
                       "Probability goes from 0 (impossible) to 1 (certain). 1/2 means equally likely. Near 0 is unlikely and near 1 is likely."))
    events = [("rolling a 7 on a standard number cube (1 to 6)", "impossible"), ("the sun rising tomorrow morning", "certain"),
              ("a fair coin landing on heads", "equally likely as not"), ("rolling a 1 on a number cube", "unlikely"),
              ("rolling a number less than 6 on a number cube", "likely"), ("picking a red card from a deck with 26 red and 26 black cards", "equally likely as not"),
              ("picking a blue marble from a bag of only red marbles", "impossible")]
    for ev, good in events:
        bad = [x for x in ["impossible", "unlikely", "equally likely as not", "likely", "certain"] if x != good]
        R.shuffle(bad)
        its.append(mcq("How likely is %s?" % ev, (good, good), [(b, b) for b in bad[:3]],
                       {"impossible": "It can never happen, so the probability is 0.", "certain": "It will surely happen, so the probability is 1.",
                        "equally likely as not": "Half of the outcomes work, so the probability is 1/2.",
                        "unlikely": "Only 1 of 6 outcomes works. 1/6 is close to 0.", "likely": "5 of 6 outcomes work. 5/6 is close to 1."}[good]))
    vals = [("0.95", "likely"), ("0.08", "unlikely"), ("0.5", "equally likely as not"), ("1.2", "not possible as a probability")]
    for v, good in vals:
        bad = [x for x in ["impossible", "unlikely", "equally likely as not", "likely", "certain", "not possible as a probability"] if x != good][:3]
        if good == "not possible as a probability":
            bad = ["likely", "certain", "unlikely"]
        its.append(mcq("An event has a probability of %s. How would you describe it?" % B(v), (good, good), [(b, b) for b in bad],
                       "A probability is never less than 0 or more than 1." if v == "1.2" else
                       "%s is %s, so the event is %s." % (v, "close to 1" if good == "likely" else "close to 0" if good == "unlikely" else "exactly 1/2", good)))
    its.append(mcq("Which number <b>cannot</b> be a probability?", ("−0.3", "a"), [("0", "b"), ("0.99", "c"), ("1", "d")],
                   "A probability is between 0 and 1. A negative number cannot be a probability."))
    its.append(mcq("Which event is <b>more</b> likely?", ("An event with probability 0.7", "a"),
                   [("An event with probability 0.3", "b"), ("An event with probability 1/4", "c"), ("An event with probability 0.07", "d")],
                   "The closer to 1, the more likely. 0.7 is the largest."))
    its.append(mcq("Which is the same probability as 3/4?", ("75%", "a"), [("34%", "b"), ("0.34", "c"), ("7.5%", "d")],
                   "3 ÷ 4 = 0.75 = 75%."))
    its.append(mcq("Which is the same probability as 40%?", ("0.4", "a"), [("4", "b"), ("0.04", "c"), ("1/40", "d")],
                   "40% = 40/100 = 0.4 = 2/5."))
    return {"title": "Likelihood from 0 to 1", "items": its}


# ------------------------------------------------------------ set 2
def set_simple():
    its = []
    spins = [(["red", "blue", "red", "green"], "red"), (["blue", "yellow", "blue", "blue", "green", "red"], "blue"),
             (["green", "red", "yellow", "red", "blue", "red", "green", "red"], "red"), (["purple", "yellow", "green", "blue", "red"], "yellow"),
             (["red", "red", "blue", "green", "blue", "red"], "blue"), (["yellow", "green", "yellow", "green", "yellow", "green", "red", "blue"], "green")]
    for parts, c in spins:
        k, n = parts.count(c), len(parts)
        v = F(k, n)
        ws = [F(k, n - k) if n - k and k < n - k else F(1, n), F(1, n), 1 - v, F(1, len(set(parts)))]
        e = "%d of the %d equal sections are %s, so P(%s) = %d/%d%s." % (k, n, c, c, k, n, "" if v == F(k, n) and math.gcd(k, n) == 1 else " = %s" % (str(v.numerator) + "/" + str(v.denominator)))
        if n - k and k < n - k:
            w = F(k, n - k)
            e += " Not %d/%d: divide by all %d sections, not just the sections that are not %s." % (w.numerator, w.denominator, n, c)
        its.append(mcp("The spinner has equal sections. What is the probability of landing on %s?" % B(c) + fig(spinner(parts)), v, ws, e))
    bags = [([("red", 3), ("blue", 5)], "red"), ([("green", 4), ("yellow", 2), ("blue", 6)], "green"), ([("red", 2), ("blue", 2), ("green", 6)], "green"),
            ([("purple", 5), ("yellow", 3), ("red", 2)], "yellow")]
    for counts, c in bags:
        tot = sum(k for _, k in counts)
        k = dict(counts)[c]
        v = F(k, tot)
        ws = [F(k, tot - k) if k < tot - k else F(1, tot), F(1, len(counts)), 1 - v, F(1, tot)]
        e = "There are %d %s marbles out of %d in all. P(%s) = %d/%d%s." % (k, c, tot, c, k, tot, "" if math.gcd(k, tot) == 1 else " = %d/%d" % (v.numerator, v.denominator))
        its.append(mcp("You pick one marble without looking. What is the probability it is %s?" % B(c) + fig(bag(counts)), v, ws, e))
    dice = [("a 4", F(1, 6)), ("an even number", F(1, 2)), ("a number greater than 4", F(1, 3)), ("a number less than 3", F(1, 3)),
            ("a multiple of 3", F(1, 3)), ("a prime number (2, 3 or 5)", F(1, 2))]
    for ev, v in dice:
        k = v * 6
        ws = [F(int(k), 6 - int(k)) if k < 6 - k else F(1, 6), 1 - v, F(1, 6) if v != F(1, 6) else F(1, 2), F(int(k), 10)]
        its.append(mcp("You roll a fair number cube with faces 1 to 6. What is P(%s)?" % ev, v, ws,
                       "%d of the 6 faces %s, so the probability is %d/6%s." % (k, "works" if k == 1 else "work", k, "" if v.denominator == 6 else " = %d/%d" % (v.numerator, v.denominator))))
    letters = "MISSISSIPPI"
    its.append(mcp("Each letter of the word MISSISSIPPI is on its own card. You pick one card. What is P(S)?", F(4, 11), [F(1, 4), F(4, 7), F(1, 11)],
                   "There are 11 letters and 4 of them are S. P(S) = 4/11."))
    its.append(mcp("A class has 12 girls and 15 boys. The teacher picks one student at random. What is P(girl)?", F(4, 9), [F(4, 5), F(5, 9), F(1, 2)],
                   "12 girls out of 27 students: 12/27 = 4/9. Not 4/5 (12/15): divide by all 27 students."))
    its.append(mcp("A month has 30 days. One day is picked at random. What is the probability that it is the 15th?", F(1, 30), [F(1, 15), F(15, 30), F(1, 31)],
                   "Only 1 of the 30 days works: 1/30."))
    its.append(mcp("A jar has 10 cards numbered 1 to 10. What is P(a number greater than 7)?", F(3, 10), [F(7, 10), F(3, 7), F(2, 5)],
                   "8, 9 and 10 work: 3 out of 10 = 3/10."))
    return {"title": "Theoretical probability", "items": its}


# ------------------------------------------------------------ set 3
def set_complement():
    its = []
    for p in [F(1, 4), F(2, 7), F(5, 8), F(3, 10), F(1, 6), F(7, 12)]:
        ws = [p, F(p.denominator - p.numerator, p.numerator) if p.denominator - p.numerator < p.numerator else F(1, p.denominator), 1 - p - F(1, p.denominator)]
        its.append(mcp("The probability that it rains tomorrow is %s. What is the probability that it does <b>not</b> rain?" % pf(p), 1 - p, ws,
                       "An event and its complement add to 1: 1 − %d/%d = %d/%d." % (p.numerator, p.denominator, (1 - p).numerator, (1 - p).denominator)))
    for dec_, ans in [("0.35", "0.65"), ("0.9", "0.1"), ("0.02", "0.98"), ("0.48", "0.52"), ("0.7", "0.3")]:
        wrong = [str(round(1 - float(ans) + 0.0, 2)), str(round(float(ans) - 0.1, 2)), str(round(float(dec_) * 2, 2)) if float(dec_) * 2 < 1 else str(round(1 - float(dec_) / 2, 3))]
        cands = []
        for w in wrong:
            if w != ans and w not in [c[0] for c in cands]:
                cands.append((w, w))
        cands += [("0.5", "0.5"), ("1", "1")]
        its.append(mcq("P(win) = %s. What is P(not win)?" % B(dec_), (ans, ans), cands, "P(not win) = 1 − %s = %s." % (dec_, ans)))
    for pct, ans in [(30, 70), (85, 15), (12, 88)]:
        its.append(mcq("There is a%s %d%% chance of snow. What is the chance of no snow?" % ("n" if pct in (8, 11, 18, 80, 85) else "", pct), ("%d%%" % ans, ans),
                       [("%d%%" % pct, pct), ("%d%%" % (100 - ans + 10 if 100 - ans + 10 != ans else 50), -1), ("%d%%" % (50 if ans != 50 else 40), -2)],
                       "100%% − %d%% = %d%%." % (pct, ans)))
    its.append(mcp("A bag has 3 red, 4 blue and 5 green marbles. What is P(<b>not</b> green)?", F(7, 12), [F(5, 12), F(7, 5), F(1, 3)],
                   "7 of the 12 marbles are not green (3 red + 4 blue). Or 1 − 5/12 = 7/12."))
    its.append(mcp("A spinner has 8 equal sections, 3 of them yellow. What is P(not yellow)?", F(5, 8), [F(3, 8), F(3, 5), F(1, 8)],
                   "5 of the 8 sections are not yellow: 5/8. Check: 3/8 + 5/8 = 1."))
    its.append(mcp("You roll a number cube. What is P(not 6)?", F(5, 6), [F(1, 6), F(1, 5), F(1, 2)], "5 of the 6 faces are not 6: 5/6."))
    its.append(mcq("P(A) = 0.4. Which statement is true?", ("P(not A) = 0.6", "a"), [("P(not A) = 0.4", "b"), ("P(not A) = 1.4", "c"), ("P(not A) = −0.4", "d")],
                   "P(A) + P(not A) = 1, so P(not A) = 1 − 0.4 = 0.6."))
    its.append(mcq("A weather app says the chance of rain is 0%. What does that mean?", ("It is not expected to rain at all.", "a"),
                   [("It will surely rain.", "b"), ("Rain and no rain are equally likely.", "c"), ("It will rain a little.", "d")],
                   "A probability of 0 means the event is impossible (or not expected)."))
    its.append(mcp("A bag has only red and blue tiles. P(red) = 3/8. What is P(blue)?", F(5, 8), [F(3, 8), F(3, 5), F(1, 2)],
                   "There are only two colours, so P(blue) = 1 − 3/8 = 5/8."))
    return {"title": "The complement: not happening", "items": its}


# ------------------------------------------------------------ set 4
def set_experiment():
    its = []
    exps = [("A coin was flipped 50 times and landed on heads 28 times.", "heads", F(28, 50)),
            ("A number cube was rolled 60 times. It showed 3 twelve times.", "rolling a 3", F(12, 60)),
            ("A spinner was spun 40 times and landed on blue 14 times.", "blue", F(14, 40)),
            ("A basketball player made 18 of 25 shots.", "making a shot", F(18, 25)),
            ("Out of 80 cars that passed, 32 were white.", "a white car", F(32, 80))]
    for s, ev, v in exps:
        k, n = int(v * {F(28, 50): 50, F(12, 60): 60, F(14, 40): 40, F(18, 25): 25, F(32, 80): 80}[v]), {F(28, 50): 50, F(12, 60): 60, F(14, 40): 40, F(18, 25): 25, F(32, 80): 80}[v]
        ws = [F(k, n - k) if k < n - k else F(1, 2), F(1, 2) if v != F(1, 2) else F(1, 3), F(1, 6) if v != F(1, 6) else F(1, 4), 1 - v]
        its.append(mcp("%s What is the experimental probability of %s?" % (s, ev), v, ws,
                       "Experimental probability = times it happened ÷ total tries = %d/%d = %s." % (k, n, "/".join([str(v.numerator), str(v.denominator)]))))
    preds = [("The probability of rolling a 5 is 1/6. You roll a number cube 120 times. About how many times should you expect a 5?", 20, [6, 5, 100]),
             ("A spinner lands on red with probability 1/4. It is spun 200 times. About how many times will it land on red?", 50, [4, 25, 150]),
             ("A player makes 70% of free throws. About how many will she make in 40 tries?", 28, [12, 70, 30]),
             ("The probability a light bulb is broken is 0.02. About how many broken bulbs are in a box of 500?", 10, [2, 100, 25]),
             ("A coin is flipped 300 times. About how many heads do you expect?", 150, [100, 300, 200]),
             ("Out of 50 students surveyed, 15 walk to school. A school has 600 students. About how many walk to school?", 180, [15, 450, 90])]
    for q, v, ws in preds:
        its.append(mcq(q, (str(v), v), [(str(w), w) for w in ws],
                       "Multiply the probability by the number of tries. %s" % {20: "1/6 × 120 = 20.", 50: "1/4 × 200 = 50.", 28: "0.7 × 40 = 28.", 10: "0.02 × 500 = 10.",
                                                                               150: "1/2 × 300 = 150.", 180: "15/50 = 0.3, and 0.3 × 600 = 180."}[v]))
    its.append(mcq("A coin is flipped 10 times and lands on heads 7 times. What does this show?",
                   ("Experimental results can differ from the theoretical probability of 1/2.", "a"),
                   [("The coin must be unfair.", "b"), ("The theoretical probability of heads is 7/10.", "c"), ("The next flip will be tails.", "d")],
                   "With only 10 flips, results vary a lot. With many more flips, the fraction of heads usually gets closer to 1/2."))
    its.append(mcq("Which is most likely to give an experimental probability close to the theoretical probability?",
                   ("Doing the experiment 1,000 times", "a"), [("Doing it 5 times", "b"), ("Doing it 10 times", "c"), ("Doing it once", "d")],
                   "More trials usually bring the experimental probability closer to the theoretical probability."))
    its.append(mcq("A spinner was spun 100 times: red 48, blue 27, green 25. Which spinner is most likely?",
                   ("Red covers about half; blue and green about a quarter each.", "a"),
                   [("All three colours are equal.", "b"), ("Blue covers half.", "c"), ("Green covers half.", "d")],
                   "48/100 is close to 1/2, and 27/100 and 25/100 are close to 1/4."))
    its.append(mcp("A spinner landed on yellow 9 times in 30 spins. Based on this, what is the probability of yellow?", F(3, 10), [F(9, 21), F(1, 9), F(1, 3)],
                   "9/30 = 3/10. Not 9/21: divide by all 30 spins."))
    its.append(mcq("A bag has 2 red and 8 blue marbles. You pick and replace a marble 50 times. About how many reds should you expect?", ("10", 10),
                   [("2", 2), ("25", 25), ("40", 40)], "P(red) = 2/10 = 1/5. 1/5 × 50 = 10."))
    its.append(mcq("Theoretical P(green) = 1/3. In 60 spins, green came up 26 times. Which is true?", ("Green came up more than expected (20).", "a"),
                   [("Green came up less than expected.", "b"), ("Green came up exactly as expected.", "c"), ("The spinner has 26 sections.", "d")],
                   "Expected: 1/3 × 60 = 20. 26 is more than 20."))
    its.append(mcp("A survey found that 12 of 40 people like jazz best. What is the experimental probability that a person likes jazz best?", F(3, 10), [F(12, 28), F(1, 4), F(7, 10)],
                   "12/40 = 3/10."))
    its.append(mcq("Two number cubes are rolled 36 times. A sum of 7 came up 8 times. The theoretical probability is 6/36. Which is true?",
                   ("The experimental probability (8/36) is a little higher than 6/36.", "a"),
                   [("The experimental probability is 6/8.", "b"), ("A sum of 7 is impossible.", "c"), ("The numbers must match exactly.", "d")],
                   "8/36 is a little more than 6/36. Small differences are normal in experiments."))
    its.append(mcq("A spinner has 4 equal sections, 1 of them green. Ana spins it 80 times. About how many times should it land on green?", ("20", 20),
                   [("4", 4), ("60", 60), ("1", 1)], "P(green) = 1/4. 1/4 × 80 = 20."))
    return {"title": "Experimental probability and predictions", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    its.append(mcp("A raffle sells 250 tickets. You buy 5. What is the probability that you win?", F(1, 50), [F(1, 5), F(5, 245), F(1, 250)],
                   "5 winning chances out of 250 tickets: 5/250 = 1/50."))
    its.append(mcp("A box has 6 chocolate, 4 vanilla and 10 strawberry cookies. You pick one. What is P(chocolate or vanilla)?", F(1, 2), [F(3, 10), F(1, 5), F(5, 10 + 0) * 0 + F(2, 5)],
                   "6 + 4 = 10 cookies out of 20: 10/20 = 1/2."))
    its.append(mcp("A class of 30 has 18 students with a pet. One is picked at random. What is P(no pet)?", F(2, 5), [F(3, 5), F(12, 18), F(1, 30)],
                   "30 − 18 = 12 have no pet. 12/30 = 2/5."))
    its.append(mcq("A game: you win if a number cube shows 1 or 2. Your friend wins on 3, 4, 5 or 6. Is it fair?", ("No, your friend is twice as likely to win.", "a"),
                   [("Yes, both have a chance.", "b"), ("No, you are more likely to win.", "c"), ("Yes, it is a number cube.", "d")],
                   "P(you) = 2/6 = 1/3 and P(friend) = 4/6 = 2/3. A fair game needs equal chances."))
    its.append(mcq("A bag has 4 red marbles and some blue marbles. P(red) = 1/3. How many blue marbles are there?", ("8", 8), [("4", 4), ("12", 12), ("3", 3)],
                   "If 4 is 1/3 of the total, the total is 12. 12 − 4 = 8 blue. Not 12: that is the total."))
    its.append(mcq("A spinner has 5 equal parts: 2 red and 3 blue. You spin 75 times. About how many times will it land on blue?", ("45", 45),
                   [("30", 30), ("3", 3), ("25", 25)], "P(blue) = 3/5. 3/5 × 75 = 45."))
    its.append(mcp("A drawer has 5 black socks and 7 white socks. You pick one in the dark. What is P(white)?", F(7, 12), [F(7, 5), F(5, 12), F(1, 2)],
                   "7 white out of 12 socks: 7/12."))
    its.append(mcq("A store says 1 in every 40 cereal boxes has a prize. About how many prizes are in 1,000 boxes?", ("25", 25),
                   [("40", 40), ("1", 1), ("250", 250)], "1/40 × 1,000 = 25."))
    its.append(mcq("A quality check finds 3 bad phones in a sample of 150. The factory makes 5,000 phones. About how many are bad?", ("100", 100),
                   [("3", 3), ("50", 50), ("150", 150)], "3/150 = 1/50. 1/50 × 5,000 = 100."))
    its.append(mcp("The letters of MATH are on 4 cards. You pick one. What is P(a vowel)?", F(1, 4), [F(1, 3), F(3, 4), F(1, 2)],
                   "Only A is a vowel: 1 out of 4."))
    its.append(mcp("A playlist has 20 songs: 8 pop, 7 rock and 5 jazz. It plays one at random. What is P(rock)?", F(7, 20), [F(7, 13), F(1, 3), F(13, 20)],
                   "7 rock songs out of 20: 7/20. Not 7/13: divide by all 20 songs."))
    its.append(mcq("A meteorologist says there is a 60% chance of rain on each of the next 10 days. About how many rainy days should you expect?", ("6", 6),
                   [("60", 60), ("4", 4), ("10", 10)], "60% of 10 = 6 days."))
    its.append(mcp("A number from 1 to 20 is picked at random. What is P(a multiple of 4)?", F(1, 4), [F(4, 20) * 0 + F(1, 5), F(4, 5), F(1, 20)],
                   "4, 8, 12, 16 and 20 work: 5 out of 20 = 1/4."))
    its.append(mcq("Event A has probability 0.25 and event B has probability 0.6. Which is true?", ("B is more likely than A.", "a"),
                   [("A is more likely than B.", "b"), ("They are equally likely.", "c"), ("A is impossible.", "d")], "0.6 is greater than 0.25, so B is more likely."))
    its.append(mcp("A bag has 3 red, 3 blue and 3 green cubes. You take out one blue cube and keep it. Then you pick one more. What is P(blue)?", F(1, 4),
                   [F(1, 3), F(2, 9), F(3, 8)], "Now there are 8 cubes and 2 are blue: 2/8 = 1/4."))
    its.append(mcq("A spinner is spun 120 times and lands on purple 30 times. The spinner has 8 equal sections. How many sections are probably purple?", ("2", 2),
                   [("30", 30), ("4", 4), ("1", 1)], "30/120 = 1/4 of the spins. 1/4 of 8 sections is 2."))
    its.append(mcp("Two coins are flipped. The outcomes are HH, HT, TH and TT. What is P(exactly one head)?", F(1, 2), [F(1, 4), F(1, 3), F(3, 4)],
                   "HT and TH have exactly one head: 2 out of 4 = 1/2. Not 1/3: HT and TH are different outcomes."))
    its.append(mcp("A school has 400 students. 140 are in Grade 7. A student is chosen at random. What is P(Grade 7)?", F(7, 20), [F(7, 13), F(13, 20), F(1, 3)],
                   "140/400 = 7/20."))
    its.append(mcq("Which spinner gives P(red) = 3/8?", ("8 equal sections, 3 red", "a"),
                   [("3 equal sections, 1 red", "b"), ("8 equal sections, 5 red", "c"), ("11 equal sections, 3 red", "d")],
                   "3 red out of 8 equal sections is 3/8. 3 red and 8 not red would be 3/11."))
    its.append(mcq("A survey of 60 students finds 24 prefer soccer. In a school of 450, about how many prefer soccer?", ("180", 180),
                   [("24", 24), ("270", 270), ("36", 36)], "24/60 = 0.4. 0.4 × 450 = 180."))
    return {"title": "Word problems", "items": its}


def body():
    sp = spinner(["red", "blue", "red", "green"])
    rows = [["0", "impossible"], ["less than 1/2", "unlikely"], ["1/2", "equally likely"], ["more than 1/2", "likely"], ["1", "certain"]]
    return ("<h2>What probability means</h2><p>A <b>probability</b> is a number from 0 to 1 that tells how likely an event is.</p>"
            + table(["Probability", "Meaning"], rows)
            + "<h2>Theoretical probability</h2><p>When all outcomes are equally likely: <b>P(event) = number of favorable outcomes ÷ total number of outcomes</b>. "
            "The <b>complement</b> is the event not happening: P(not A) = 1 − P(A).</p>"
            + figure(sp, "2 of the 4 equal sections are red, so P(red) = 2/4 = 1/2.")
            + "<h2>Experimental probability</h2><p>Experimental probability = times it happened ÷ number of tries. "
            "To predict, multiply the probability by the number of tries. More tries usually bring the experimental probability closer to the theoretical one.</p>"
            + example("A bag has 3 red and 5 blue marbles. Find P(red) and P(not red).", ["P(red) = 3 ÷ (3 + 5) = 3/8.", "P(not red) = 1 − 3/8 = 5/8."], "3/8 and 5/8")
            + example("P(rolling a 5) = 1/6. About how many 5s in 120 rolls?", ["1/6 × 120 = 20."], "about 20")
            + "<h2>Common mistakes</h2><ul><li>Comparing to the other outcomes: 3 red and 5 blue gives 3/8, not 3/5.</li>"
            "<li>Forgetting the complement: P(not red) is 1 − P(red).</li><li>Expecting an experiment to match exactly: results vary, especially with few tries.</li></ul>")


def main():
    sets = [set_likelihood(), set_simple(), set_complement(), set_experiment(), set_words()]
    balance(sets, R)
    unit = {
        "slug": "probability",
        "title": "Probability",
        "seo_title": "Grade 7 Probability Worksheets: Likelihood, Theoretical and Experimental Probability",
        "short_title": "Probability",
        "domain": "Statistics & Probability",
        "standard_code": "7.SP.C.5–7",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/SP/C/5/",
        "standard_text": "Understand that the probability of a chance event is a number between 0 and 1 that expresses the likelihood of the event occurring. Approximate the probability of a chance event by collecting data and observing its long-run relative frequency, and predict the approximate relative frequency given the probability. Develop a probability model and use it to find probabilities of events.",
        "meta_desc": "Free Grade 7 probability worksheets: likelihood from 0 to 1, theoretical probability with spinners, marbles and number cubes, the complement, experimental probability and predictions. 100 practice questions with an answer key.",
        "key_big": "P(event) = favorable outcomes ÷ total outcomes, a number from 0 to 1.",
        "key_sub": "P(not A) = 1 − P(A). To predict, multiply the probability by the number of tries.",
        "body_html": body(),
        "faq": [
            {"q": "How do you find a probability?", "a": "Divide the number of favorable outcomes by the total number of equally likely outcomes. A bag with 3 red and 5 blue marbles has P(red) = 3/8."},
            {"q": "What is the complement of an event?", "a": "It is the event not happening. The two probabilities add to 1, so P(not A) = 1 − P(A)."},
            {"q": "What is the difference between experimental and theoretical probability?", "a": "Theoretical probability comes from the possible outcomes. Experimental probability comes from what actually happened in trials, such as 28 heads in 50 flips = 28/50."},
            {"q": "How do I make a prediction?", "a": "Multiply the probability by the number of trials. If P(5) = 1/6, expect about 1/6 × 120 = 20 fives in 120 rolls."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 9,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
