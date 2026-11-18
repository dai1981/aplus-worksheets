# -*- coding: utf-8 -*-
"""
Texas Grade 5 Math: Prime and Composite Numbers (TEKS 5.4A)
  python3 tools/gen_ustx_math_g5_prime_composite.py
Classifying numbers as prime or composite, finding which number in a list is prime or composite, factor pairs
and factor lists (the US Grade 4 makers), and word problems with arrays.
Wrong answers come from real mistakes: thinking odd means prime, calling 1 prime, and missing a factor pair.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g4_factors_multiples as fm
adopt(fm)
tx_common.GRADE = "grade-5"

PR = [p for p in range(2, 100) if all(p % d for d in range(2, p))]


def nfac(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)


def one_which(r):
    want = r.choice(["prime", "composite"])
    odd_comp = [n for n in range(9, 100, 2) if n not in PR]
    if want == "prime":
        right = r.choice([p for p in PR if p > 10])
        others = r.sample(odd_comp, 3)
    else:
        right = r.choice(odd_comp)
        others = r.sample([p for p in PR if p > 10], 3)
    f = [d for d in range(2, right) if right % d == 0]
    e = ("%d has only 2 factors, 1 and %d, so it is <b>prime</b>." % (right, right)) if want == "prime" else ("%d = %d × %d, so it has more than 2 factors. It is <b>composite</b>." % (right, f[0], right // f[0]))
    return mcq("Which of these numbers is %s?" % want, str(right), [str(x) for x in others], e)


def one_count(r):
    n = r.randint(12, 60)
    k = nfac(n)
    fs = [d for d in range(1, n + 1) if n % d == 0]
    return mcq("How many factors does %d have?" % n, str(k), [str(k - 1), str(k + 1), str(k // 2) if k // 2 not in (k - 1, k + 1) else str(k + 2)],
               "The factors of %d are %s. That is <b>%d</b> factors, so %d is %s." % (n, ", ".join(map(str, fs)), k, n, "prime" if k == 2 else "composite"))


def build():
    sets, R = build_sets([
        ("Prime, composite or neither?", [("run", fm.set_prime, (fm.People,), 20)]),
        ("Which number is prime or composite?", [("collect", one_which, 20)]),
        ("Factor pairs", [("run", fm.set_pairs, (fm.People,), 20)]),
        ("Lists of factors", [("run", fm.set_factors, (fm.People,), 10), ("collect", one_count, 10)]),
        ("Arrays and word problems", [("run", fm.set_words, (fm.People,), 20)]),
    ], 65012)
    finish(sets, R)
    body = lesson('<ul><li>A <b>prime number</b> has exactly 2 factors: 1 and itself (2, 3, 5, 7, 11, 13 ...).</li><li>A <b>composite number</b> has more than 2 factors (4, 6, 8, 9, 10 ...).</li><li>1 is <b>neither</b>: it has only 1 factor.</li><li>To test a number, try dividing by 2, 3, 5 and 7. If one divides evenly, the number is composite.</li></ul>',
        [example("Is 51 prime or composite?", ["5 + 1 = 6, so 3 divides 51", "51 = 3 × 17"], "composite"), example("Is 37 prime or composite?", ["Not divisible by 2, 3, 5 or 7"], "prime")],
        [['Thinking every odd number is prime', '9, 15, 21, 27 and 51 are odd but composite.'], ['Calling 1 prime', '1 has only one factor, so it is neither.'], ['Thinking 2 is composite because it is even', '2 has exactly 2 factors. It is the only even prime.']])
    faq = [('What does TEKS 5.4A ask?', 'Identify prime and composite numbers.'), ('Is 1 a prime number?', 'No. 1 has only one factor, so it is neither prime nor composite.'), ('What is the only even prime number?', '2. Every other even number has 2 as a factor.'), ('How can an array show a composite number?', 'If the number can make a rectangle with more than one row and more than one column, it is composite.')]
    make('prime-and-composite-numbers', 12, 'Algebraic Reasoning', '5.4A',
         '5.4A identify prime and composite numbers',
         'Prime and Composite Numbers', 'Prime and Composite Numbers',
         'Free Grade 5 prime and composite number worksheets for Texas TEKS 5.4A: classify numbers, find which is prime or composite, factor pairs, factor lists and array word problems. 100 questions with answers.',
         'Prime: exactly 2 factors. Composite: more than 2 factors.', '1 is neither. 2 is the only even prime. 51 = 3 × 17 is composite.',
         body, faq, sets, seo_title='Grade 5 Prime and Composite Numbers Worksheets (TEKS 5.4A, STAAR)')


if __name__ == "__main__":
    build()
