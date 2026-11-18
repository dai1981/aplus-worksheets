# -*- coding: utf-8 -*-
"""
Texas Grade 7 Math: Theoretical and Experimental Probability and Predictions (TEKS 7.6C, 7.6D, 7.6E, 7.6I)
  python3 tools/gen_ustx_math_g7_probability.py
Theoretical probability, the complement of an event, experimental probability, predictions from theoretical and
experimental probability, and word problems (US Grade 7 makers with a new seed, plus an own prediction maker).
Wrong answers come from real mistakes: using the count instead of the probability, forgetting the complement adds to
1, and expecting experimental results to match exactly.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import random
import gen_us_math_g7_probability as prb
adopt(prb)
prb.R = random.Random(670200)
from fractions import Fraction as F
tx_common.GRADE = "grade-7"

def one_predict(r):
    kind = r.choice(["cube", "spin", "exp", "bag"])
    if kind == "cube":
        n = r.choice([60, 120, 180, 240, 300])
        side = r.choice(["a 3", "an even number", "a number greater than 4", "a 1 or a 2"])
        p = {"a 3": F(1, 6), "an even number": F(1, 2), "a number greater than 4": F(1, 3), "a 1 or a 2": F(1, 3)}[side]
        v = p * n
        return mcq("A number cube is rolled %d times. About how many times should it land on %s?" % (n, side), str(v), [str(n - v), str(n // 6) if n // 6 != v else str(v * 2), str(p.numerator * 10)],
                   "P = %s. %s × %d = <b>%d</b>. This is a prediction from theoretical probability." % (fr(p.numerator, p.denominator), fr(p.numerator, p.denominator), n, v))
    if kind == "spin":
        k = r.choice([4, 5, 8, 10])
        c = r.randint(1, k - 1)
        n = k * r.choice([10, 20, 30, 50])
        p = F(c, k)
        return mcq("A spinner has %d equal sections. %d are blue. It is spun %d times. About how many times should it land on blue?" % (k, c, n), str(p * n), [str(n - p * n), str(c * 10), str(n // k)] if n // k != p * n else [str(n - p * n), str(c * 10 + 1), str(p * n + k)],
                   "P(blue) = %s. %s × %d = <b>%d</b>." % (fr(c, k), fr(c, k), n, p * n))
    if kind == "exp":
        t = r.choice([20, 25, 40, 50])
        h = r.randint(t // 5, 4 * t // 5)
        n = t * r.choice([4, 10, 20])
        v = F(h, t) * n
        if v.denominator != 1:
            return None
        return mcq("In %d trials, a thumbtack landed point up %d times. Predict how many times it will land point up in %d trials." % (t, h, n), str(v), [str(n - v), str(h + n - t), str(F(t - h, t) * n) if F(t - h, t) * n != n - v else str(v + h)],
                   "Experimental probability = %d/%d. %d/%d × %d = <b>%d</b>." % (h, t, h, t, n, v))
    red, blue, green = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    tot = red + blue + green
    n = tot * r.choice([5, 10, 20])
    v = F(red, tot) * n
    return mcq("A bag has %d red, %d blue and %d green marbles. A marble is drawn and replaced %d times. About how many times should a red marble be drawn?" % (red, blue, green, n), str(v), [str(red * 10), str(n - v), str(n // 3) if n // 3 != v else str(v + red)],
               "P(red) = %d/%d. %d/%d × %d = <b>%d</b>." % (red, tot, red, tot, n, v))


def build():
    sets, R = build_sets([
        ("Theoretical probability", [("run", prb.set_simple, (), 20)]),
        ("An event and its complement", [("run", prb.set_complement, (), 20)]),
        ("Experimental probability", [("run", prb.set_experiment, (), 20)]),
        ("Make predictions", [("collect", one_predict, 20)]),
        ("Word problems", [("run", prb.set_words, (), 20)]),
    ], 67020)
    finish(sets, R)
    body = lesson('<ul><li><b>Theoretical probability</b> = favorable outcomes ÷ possible outcomes.</li><li><b>Experimental probability</b> = times the event happened ÷ number of trials.</li><li>An event and its <b>complement</b> add to 1: P(not A) = 1 − P(A).</li><li>To <b>predict</b>, multiply the probability by the number of trials.</li></ul>',
        [example("Roll a number cube 120 times. How many 3s?", ["P(3) = 1/6", "1/6 × 120"], "about 20"), example("P(rain) = 0.3", ["1 − 0.3"], "P(no rain) = 0.7")],
        [['Using the count instead of the probability', 'Divide by the total number of outcomes or trials.'], ['Forgetting the complement adds to 1', 'P(A) + P(not A) = 1.'], ['Expecting results to match exactly', 'Predictions are about the expected number; real results vary.']])
    faq = [('What does TEKS 7.6I ask?', 'Determine experimental and theoretical probabilities related to simple and compound events using data and sample spaces.'), ('What does TEKS 7.6E ask?', 'Find the probabilities of a simple event and its complement and describe the relationship between the two.'), ('Why can experimental and theoretical probability differ?', 'Real trials have chance variation. With many trials they get closer.'), ('What does TEKS 7.6D ask?', 'Make predictions and determine solutions using theoretical probability for simple and compound events.')]
    make('probability-and-predictions', 20, 'Proportionality', '7.6C, 7.6D, 7.6E, 7.6I',
         '7.6C make predictions and determine solutions using experimental data for simple and compound events; 7.6D make predictions and determine solutions using theoretical probability for simple and compound events; 7.6E find the probabilities of a simple event and its complement and describe the relationship between the two; 7.6I determine experimental and theoretical probabilities related to simple and compound events using data and sample spaces',
         'Theoretical and Experimental Probability and Predictions', 'Probability and Predictions',
         'Free Grade 7 probability worksheets for Texas TEKS 7.6: theoretical and experimental probability, complements, predictions and word problems. 100 questions with answers.',
         'Predict: probability × number of trials.', 'P(3) = 1/6, so about 20 threes in 120 rolls. P(not A) = 1 − P(A).',
         body, faq, sets, seo_title='Grade 7 Theoretical and Experimental Probability Worksheets (TEKS 7.6, STAAR)')


if __name__ == "__main__":
    build()
