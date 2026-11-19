# -*- coding: utf-8 -*-
"""
Philippines Grade 7 Math (MATATAG): Experiments, Outcomes and Probability (Grade 7: Data and Probability)
  python3 tools/gen_ph_math_g7_probability.py
Listing outcomes and sample spaces, theoretical probability (BC Grade 7 and US Grade 7 makers), results of
experiments such as tossing coins and rolling dice, comparing experimental and theoretical probability, and problems.
Wrong answers come from real mistakes: missing outcomes in a list, writing the probability upside down, and
expecting an experiment to match the theory exactly.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_cabc_math_g7_probability as cbp
adopt(cbp)
if hasattr(cbp, 'R'): cbp.R = random.Random(707290)
import gen_us_math_g7_probability as usp
adopt(usp)
if hasattr(usp, 'R'): usp.R = random.Random(707291)
ph_common.GRADE = "grade-7"

def uniq(fn):
    """Never give the same question twice, even with other wrong answers."""
    seen = set()
    def f(r):
        it = fn(r)
        if it is None or it["q"] in seen:
            raise AssertionError("repeat")
        seen.add(it["q"])
        return it
    f.__name__ = fn.__name__
    return f


from fractions import Fraction as F


def one_exp(r):
    k = Kid(r).next()
    if r.random() < 0.5:
        n = r.choice([20, 30, 40, 50, 60, 80, 100])
        h = r.randint(n * 2 // 5, n * 3 // 5)
        fr_ = F(h, n)
        q = "%s tosses a coin %d times and gets heads %d times. What is the experimental probability of heads?" % (k["n"], n, h)
        return mcq(q, fr(fr_.numerator, fr_.denominator), [fr(1, 2) if fr_ != F(1, 2) else fr(h + 1, n), fr(n - h, n) if F(n - h, n) != fr_ else fr(h, n + 1), fr(h, n - h)],
                   "Experimental probability = times it happened ÷ number of trials = %d ÷ %d = <b>%s</b>. (The theoretical probability is %s.)" % (h, n, fr(fr_.numerator, fr_.denominator), fr(1, 2)))
    n = r.choice([30, 36, 42, 48, 60, 72])
    p_ = r.randint(n // 3, n * 2 // 3)
    q = "%s rolls a die %d times. A prime number (2, 3 or 5) comes up %d times. How many times would you <b>expect</b> a prime number in theory?" % (k["n"], n, p_)
    return mcq(q, n // 2, [p_ if p_ != n // 2 else p_ + 2, n // 3, n // 6], "P(prime) = %s = %s. %s × %d = <b>%d</b> times. The actual result, %d, is close but not exact." % (fr(3, 6), fr(1, 2), fr(1, 2), n, n // 2, p_))


def build():
    sets, R = build_sets([
        ("Outcomes and sample spaces", [("run", cbp.set_sample_spaces, (), 16), ("run", usp.set_likelihood, (), 4)]),
        ("Probability of an outcome", [("run", usp.set_simple, (), 20)]),
        ("Results of experiments", [("run", cbp.set_experimental, (), 14), ("collect", uniq(one_exp), 6)]),
        ("Experiments and predictions", [("run", usp.set_experiment, (), 20)]),
        ("Experimental or theoretical?", [("run", cbp.set_compare, (), 20)]),
    ], 70729)
    finish(sets, R)
    body = lesson("<ul><li>An <b>experiment</b> is an activity with results we can observe, like tossing a coin. Each result is an <b>outcome</b>. All the outcomes form the <b>sample space</b>.</li><li>Outcomes can be written in words, as lists like {H, T}, or in tables and tree diagrams.</li><li>Theoretical probability = number of favorable outcomes ÷ number of possible outcomes. Rolling a prime on a die: {2, 3, 5}, so 3 ÷ 6 = <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>.</li><li>Experimental probability = number of times it happened ÷ number of trials. With more trials, it usually gets closer to the theoretical probability.</li></ul>",
        [example("A coin lands heads 23 times in 40 tosses", ["23 ÷ 40"], "experimental probability 0.575")],
        [['Missing outcomes', 'Use a table or tree diagram to list them all.'], ['Upside down', 'Favorable outcomes go on top.'], ['Expecting an exact match', 'Experiments vary; more trials get closer.']])
    faq = [('What does MATATAG Math 7 ask about probability?', 'Collect data from experiments, express outcomes in words and/or symbols and represent them in tables and/or graphs, and solve problems using the outcomes of experiments.'), ('What is the sample space of tossing two coins?', '{HH, HT, TH, TT}.'), ('Can a probability be more than 1?', 'No. It is from 0 to 1.'), ('Why do experimental results differ from the theory?', 'Because of chance; the difference usually shrinks with more trials.')]
    make('probability-experiments-and-outcomes', 29, 'Data and Probability', 'Grade 7: Data and Probability',
         'Collect data from experiments (e.g., number of heads obtained when tossing a coin a number of times, number of prime numbers obtained when rolling a die a number of times); express outcomes in words and/or symbols, and represent outcomes in tables and/or graphs; solve problems using the outcomes of experiments.',
         'Experiments, Outcomes and Probability', 'Experiments and Outcomes',
         'Free Grade 7 probability worksheets for the DepEd MATATAG curriculum: experiments, outcomes, sample spaces, theoretical and experimental probability. 100 questions with answers.',
         'Probability = favorable outcomes ÷ possible outcomes.', 'More trials: experimental probability gets closer to theoretical.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
