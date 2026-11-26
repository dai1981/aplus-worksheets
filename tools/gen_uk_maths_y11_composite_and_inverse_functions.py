# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Composite and Inverse Functions
  python3 tools/gen_uk_maths_y11_composite_and_inverse_functions.py
Runs the question makers of gen_us_math_a2_composition_and_inverse_functions with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_ks3 import QN, T, expr, num, MINUS, lesson
from uk_gcse import port

X = "<i>x</i>"


def one_fn(r):
    k = r.choice(["lin", "lin", "quad", "solve"])
    a, b = r.choice([2, 3, 4, 5, -2, -3]), r.randint(-9, 9)
    v = r.randint(-5, 6)
    if k == "lin":
        f = expr([(a, X), (b, "")])
        return QN("f(%s) = %s. Find f(%s)." % (X, f, num(v)), a * v + b, [a + v + b, a * v - b, a * (v + b)],
                  "Replace %s with %s: %s × %s + %s = <b>%s</b>." % (X, num(v), num(a), num(v), num(b), num(a * v + b)))
    if k == "quad":
        c = r.randint(-9, 9)
        f = expr([(1, X + "²"), (c, "")])
        return QN("f(%s) = %s. Find f(%s)." % (X, f, num(v)), v * v + c, [2 * v + c, -(v * v) + c if v < 0 else v * v - c, v + c],
                  "%s² = %s, so f(%s) = <b>%s</b>." % (num(v), num(v * v), num(v), num(v * v + c)))
    y = a * v + b
    f = expr([(a, X), (b, "")])
    return QN("f(%s) = %s. Solve f(%s) = %s." % (X, f, X, num(y)), v, [a * y + b, y - b, v + 1 if (y + b) % a else (y + b) // a],
              "%s = %s, so %s = <b>%s</b>." % (f, num(y), X, num(v)))


BODY = lesson(
    "<p><b>Function notation</b>: f(<i>x</i>) = 2<i>x</i> + 3 means “double, then add 3”. f(5) = 13.</p>"
    "<p>A <b>composite function</b> fg(<i>x</i>) means f(g(<i>x</i>)): do g first, then f. Usually fg(<i>x</i>) ≠ gf(<i>x</i>).</p>"
    "<p>The <b>inverse function</b> f<sup>−1</sup>(<i>x</i>) undoes f. Write <i>y</i> = f(<i>x</i>), make <i>x</i> the subject, then swap the letters.</p>",
    [("f(<i>x</i>) = <i>x</i>² + 1 and g(<i>x</i>) = 2<i>x</i> − 3. Find fg(2).", ["g(2) = 1", "f(1) = 2"], "2"),
     ("Find f<sup>−1</sup>(<i>x</i>) when f(<i>x</i>) = 4<i>x</i> + 7.", ["<i>y</i> = 4<i>x</i> + 7", "<i>x</i> = (<i>y</i> − 7) ÷ 4"], "f<sup>−1</sup>(<i>x</i>) = (<i>x</i> − 7) ÷ 4")],
    ["Doing f first in fg(<i>x</i>). Start with g, the function nearest to <i>x</i>.",
     "Writing f<sup>−1</sup>(<i>x</i>) as 1 ÷ f(<i>x</i>). The −1 is not a power here.",
     "Undoing the steps in the same order. Undo them in reverse order."])
FAQ = [("What does fg(x) mean?", "It is a composite function: put x into g first, then put the answer into f. So fg(x) = f(g(x))."),
       ("How do you find an inverse function?", "Write y = f(x), rearrange to make x the subject, then swap x and y. The result is f⁻¹(x)."),
       ("How can you check an inverse function?", "Put a number into f, then put the answer into f⁻¹. You should get back the number you started with.")]


if __name__ == "__main__":
    port('gen_us_math_a2_composition_and_inverse_functions', 91102, 11, 'composite-and-inverse-functions', 2, 'A',
         'Interpret the reverse process as the inverse function; interpret the succession of two functions as a composite function.',
         'Composite and Inverse Functions', 'Composite and inverse functions',
         meta='Free Year 11 GCSE maths worksheets on function notation, composite functions fg(x) and inverse functions f⁻¹(x). 100 questions with answers.',
         rep=[], swap={"one_ops": one_fn}, body=BODY, faq=FAQ, kb="fg(x) means do g first, then f.", ks="The inverse f⁻¹(x) undoes f.", set_titles=["Function notation", "Evaluate composite functions", "Write a composite function", "Find the inverse", "Check inverses and problems"])
