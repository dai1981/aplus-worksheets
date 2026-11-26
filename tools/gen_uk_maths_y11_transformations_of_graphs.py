# -*- coding: utf-8 -*-
"""
UK Year 11 Maths (GCSE, KS4): Transformations of Graphs
  python3 tools/gen_uk_maths_y11_transformations_of_graphs.py
Runs the question makers of gen_us_math_a2_transformations_of_functions with a new seed, UK names, £ and UK number style (uk_gcse.port).
"""
from uk_ks3 import T, num, MINUS, lesson
from uk_gcse import port

X = "<i>x</i>"


def vec(a, b):
    return "<span class='mx m1'><span>%s</span><span>%s</span></span>" % (num(a), num(b))


def one_vec(r):
    a, b = r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]), r.choice([-6, -4, -3, -2, -1, 0, 1, 2, 3, 5])
    k = r.choice(["eq", "vec"])
    inner = "f(%s %s %d)" % (X, MINUS if a > 0 else "+", abs(a))
    outer = "" if b == 0 else " %s %d" % ("+" if b > 0 else MINUS, abs(b))
    right = "<i>y</i> = " + inner + outer
    if k == "eq":
        wr = ["<i>y</i> = f(%s %s %d)%s" % (X, "+" if a > 0 else MINUS, abs(a), outer),
              "<i>y</i> = f(%s %s %d)%s" % (X, MINUS if a > 0 else "+", abs(a), "" if b == 0 else " %s %d" % (MINUS if b > 0 else "+", abs(b))),
              "<i>y</i> = f(%s)%s %s %d" % (X, outer, "+" if a > 0 else MINUS, abs(a))]
        return T("The graph of <i>y</i> = f(%s) is translated by the vector %s. What is the equation of the new graph?" % (X, vec(a, b)), right, wr,
                 "Right %s means f(%s %s %s); up %s means add %s outside: <b>%s</b>." % (num(a), X, MINUS, num(a), num(b), num(b), right))
    return T("Which vector translates <i>y</i> = f(%s) onto %s?" % (X, right), vec(a, b), [vec(-a, b), vec(a, -b) if b else vec(b, a), vec(-a, -b) if b else vec(0, a)],
             "Inside the bracket the change is the opposite way: the graph moves %s %d; outside: %s %d. Vector %s." % ("right" if a > 0 else "left", abs(a), "up" if b >= 0 else "down", abs(b), vec(a, b)))


BODY = lesson(
    "<p>For a graph <i>y</i> = f(<i>x</i>):</p>"
    "<ul><li><i>y</i> = f(<i>x</i>) + <i>a</i> is a translation by the vector (0, <i>a</i>): up <i>a</i>.</li>"
    "<li><i>y</i> = f(<i>x</i> + <i>a</i>) is a translation by (−<i>a</i>, 0): <b>left</b> <i>a</i>. Inside the bracket the change is the opposite way.</li>"
    "<li><i>y</i> = −f(<i>x</i>) is a reflection in the <i>x</i>-axis; <i>y</i> = f(−<i>x</i>) is a reflection in the <i>y</i>-axis.</li></ul>",
    [("Describe <i>y</i> = f(<i>x</i> − 3) + 2.", ["Inside: right 3", "Outside: up 2"], "translation by the vector (3, 2)"),
     ("(2, 5) is on <i>y</i> = f(<i>x</i>). Where is it on <i>y</i> = f(<i>x</i> + 3) − 1?", ["Left 3, down 1"], "(−1, 4)")],
    ["Moving right for f(<i>x</i> + 3). It moves left 3.",
     "Putting the vertical change inside the bracket.",
     "Mixing up −f(<i>x</i>) (reflection in the <i>x</i>-axis) and f(−<i>x</i>) (reflection in the <i>y</i>-axis)."])
FAQ = [("How do you translate a graph to the right?", "Replace x with (x − a). For example, y = f(x − 4) is y = f(x) moved 4 units right."),
       ("What does y = −f(x) do?", "It reflects the graph in the x-axis. A minus inside, y = f(−x), reflects it in the y-axis."),
       ("How do you write a translation as a vector?", "The top number is the move right (negative for left) and the bottom number is the move up (negative for down). y = f(x − 2) + 5 is the vector (2, 5).")]


if __name__ == "__main__":
    port('gen_us_math_a2_transformations_of_functions', 91103, 11, 'transformations-of-graphs', 3, 'A',
         'Sketch translations and reflections of a given function: y = f(x) + a, y = f(x + a), y = −f(x) and y = f(−x).',
         'Transformations of Graphs', 'Transformations of graphs',
         meta='Free Year 11 GCSE maths worksheets on translations, reflections and stretches of graphs y = f(x). 100 questions with answers.',
         rep=[('related to the graph of the parent function', 'related to the graph of'), ('the parent function', 'the graph of'), ('parent function', 'graph'), ('vertical shrink by a factor of', 'vertical stretch, scale factor'), ('vertical stretch by a factor of', 'vertical stretch, scale factor'), ('horizontal shrink by a factor of', 'horizontal stretch, scale factor'), ('horizontal stretch by a factor of', 'horizontal stretch, scale factor'), ('Shift ', 'Translate '), ('shift ', 'translate '), ('over the x-axis', 'in the x-axis'), ('over the y-axis', 'in the y-axis'), ('over the <i>x</i>-axis', 'in the <i>x</i>-axis'), ('over the <i>y</i>-axis', 'in the <i>y</i>-axis')], swap={"one_eo": one_vec}, body=BODY, faq=FAQ, kb="Inside the bracket the graph moves the opposite way.", ks="y = f(x − a) + b is a translation by the vector (a, b).", set_titles=["Describe the transformation", "Write the transformed function", "Move a point", "Match the graph", "Translations as vectors"])
