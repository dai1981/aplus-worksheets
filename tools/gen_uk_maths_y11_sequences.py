# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Arithmetic and Geometric Sequences
  python3 tools/gen_uk_maths_y11_sequences.py
Runs the question makers of gen_us_math_a1_arithmetic_and_geometric_sequences with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_ks3 import T, QN, expr, num, MINUS, lesson
from uk_gcse import port

N = "<i>n</i>"


def seq_str(a, b, c):
    return ", ".join(num(a * n * n + b * n + c) for n in range(1, 6)).replace("-", MINUS) + ", …"


def one_quad(r):
    a, b, c = r.choice([1, 1, 2, 3]), r.randint(-5, 5), r.randint(-6, 6)
    terms = seq_str(a, b, c)
    k = r.choice(["nth", "nth", "next", "second"])
    if k == "next":
        nx = a * 36 + b * 6 + c
        return QN("What is the next term of the quadratic sequence %s?" % terms, nx, [a * 25 + b * 5 + c + (a * 9 + b + (a * 2) * 0), nx + 2 * a, nx - 2 * a],
                  "The second difference is %d. Continue the first differences to find the 6th term: <b>%s</b>." % (2 * a, num(nx)))
    if k == "second":
        return QN("What is the second difference of the sequence %s?" % terms, 2 * a, [a, a * 3, b + a], "Find the first differences, then the differences between them: <b>%d</b>." % (2 * a))
    right = expr([(a, N + "²"), (b, N), (c, "")])
    wr = [expr([(2 * a, N + "²"), (b, N), (c, "")]), expr([(a, N + "²"), (b + 1, N), (c - 1, "")]), expr([(a, N + "²"), (c, N), (b, "")])]
    wr = [w for w in dict.fromkeys(wr) if w != right]
    if len(wr) < 3:
        return None
    return T("What is the <i>n</i>th term of the quadratic sequence %s?" % terms, right, wr,
             "Second difference %d, so the %s² coefficient is %d ÷ 2 = %d. Subtract %s from each term and find the linear part: <b>%s</b>." % (2 * a, N, 2 * a, a, expr([(a, N + "²")]), right))



BODY = lesson(
    "<p>An <b>arithmetic</b> sequence adds the same number each time (the common difference). Its <i>n</i>th term is <i>dn</i> + <i>c</i>.</p>"
    "<p>A <b>geometric</b> sequence multiplies by the same number each time (the common ratio).</p>"
    "<p>A <b>quadratic</b> sequence has a constant <b>second difference</b>. The <i>n</i>² coefficient is half the second difference.</p>",
    [("Find the <i>n</i>th term of 5, 8, 11, 14, …", ["Common difference 3", "3<i>n</i> gives 3, 6, 9, …; add 2"], "3<i>n</i> + 2"),
     ("Find the <i>n</i>th term of 2, 7, 14, 23, …", ["First differences 5, 7, 9; second difference 2", "<i>n</i>² gives 1, 4, 9, 16; subtract: 1, 3, 5, 7 = 2<i>n</i> − 1"], "<i>n</i>² + 2<i>n</i> − 1")],
    ["Writing <i>n</i> + 3 for 5, 8, 11, … (the difference 3 goes in front of <i>n</i>).",
     "Using the whole second difference as the <i>n</i>² coefficient instead of half of it.",
     "Adding instead of multiplying for a geometric sequence."])
FAQ = [("How do you find the nth term of an arithmetic sequence?", "Find the common difference d. The nth term is dn + c, where c makes the first term correct."),
       ("How do you find the nth term of a quadratic sequence?", "Find the second difference and halve it to get the coefficient of n². Subtract that n² part from each term, then find the nth term of what is left."),
       ("What is a geometric sequence?", "A sequence where each term is the one before multiplied by the same number, the common ratio, such as 3, 6, 12, 24.")]

if __name__ == "__main__":
    port('gen_us_math_a1_arithmetic_and_geometric_sequences', 91101, 11, 'sequences', 1, 'A',
         'Recognise and use sequences of triangular, square and cube numbers, simple arithmetic progressions, Fibonacci-type sequences and simple geometric progressions; deduce expressions for the nth term.',
         'Arithmetic and Geometric Sequences', 'Sequences',
         meta='Free Year 11 GCSE maths worksheets on arithmetic and geometric sequences, the nth term and term-to-term rules. 100 questions with answers.',
         rep=[], swap={"one_rec": one_quad}, body=BODY, faq=FAQ, kb="Arithmetic: add the same number. Geometric: multiply by the same number.", ks="Quadratic sequences have a constant second difference.", set_titles=["Arithmetic or geometric?", "The nth term of arithmetic sequences", "Geometric sequences", "Quadratic sequences", "Sequence problems"])
