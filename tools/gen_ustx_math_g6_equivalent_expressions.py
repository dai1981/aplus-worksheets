# -*- coding: utf-8 -*-
"""
Texas Grade 6 Math: Equivalent Expressions and Properties of Operations (TEKS 6.7C, 6.7D)
  python3 tools/gen_ustx_math_g6_equivalent_expressions.py
Naming properties of operations, combining like terms, the distributive property, factoring with the GCF, and
testing whether two expressions are equivalent (the US Grade 6 makers with Texas names, plus an own properties
maker).
Wrong answers come from real mistakes: multiplying only the first term, adding unlike terms, and mixing up the
commutative and associative properties.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)
import gen_us_math_g6_equivalent_expressions as eqx
adopt(eqx)
tx_common.GRADE = "grade-6"

PROPS = ["Commutative property", "Associative property", "Distributive property", "Identity property", "Inverse property"]


def one_prop(r):
    v = r.choice("xyntab")
    a, b, c = r.sample(range(2, 15), 3)
    ex = {0: ["%d + %s = %s + %d" % (a, v, v, a), "%d × %s = %s × %d" % (a, v, v, a), "%d%s + %d = %d + %d%s" % (a, v, b, b, a, v)],
          1: ["(%d + %d) + %s = %d + (%d + %s)" % (a, b, v, a, b, v), "(%d × %d)%s = %d(%d%s)" % (a, b, v, a, b, v)],
          2: ["%d(%s + %d) = %d%s + %d" % (a, v, b, a, v, a * b), "%d%s + %d%s = (%d + %d)%s" % (a, v, b, v, a, b, v), "%d(%s − %d) = %d%s − %d" % (a, v, b, a, v, a * b)],
          3: ["%s + 0 = %s" % (v, v), "1 × %s = %s" % (v, v), "%d%s × 1 = %d%s" % (a, v, a, v)],
          4: ["%s + (−%s) = 0" % (v, v), "%d × %s = 1" % (a, fr(1, a)), "%d + (−%d) = 0" % (a, a)]}
    k = r.choice([0, 0, 1, 1, 2, 2, 3, 4])
    e = r.choice(ex[k])
    why = ["The order changes; the grouping does not.", "The grouping (parentheses) changes; the order does not.", "Multiplication is spread over addition or subtraction.",
           "Adding 0 or multiplying by 1 keeps the same value.", "A number and its opposite add to 0; a number and its reciprocal multiply to 1."][k]
    return mcq("Which property does this show?<br>%s" % e, PROPS[k], [p for i, p in enumerate(PROPS) if i != k][:3] if k != 4 else PROPS[:3], "%s This is the <b>%s</b>." % (why, PROPS[k].lower()))


def build():
    sets, R = build_sets([
        ("Name the property", [("collect", one_prop, 20)]),
        ("Combine like terms", [("run", eqx.set_like_terms, ("rnd", eqx.People), 20)]),
        ("The distributive property: expand", [("run", eqx.set_expand, ("rnd", eqx.People), 20)]),
        ("Factor using the GCF", [("run", eqx.set_factor, ("rnd", eqx.People), 20)]),
        ("Are the expressions equivalent?", [("run", eqx.set_equivalent, ("rnd", eqx.People), 20)]),
    ], 66015)
    finish(sets, R)
    body = lesson('<ul><li><b>Equivalent expressions</b> have the same value for every value of the variable.</li><li>Properties: <b>commutative</b> (change the order), <b>associative</b> (change the grouping), <b>distributive</b> 3(x + 4) = 3x + 12, <b>identity</b> (x + 0, 1 × x), <b>inverse</b> (x + (−x) = 0).</li><li><b>Like terms</b> have the same variable part: 5y + 2y = 7y.</li><li>To test, substitute a value for the variable into both expressions.</li></ul>',
        [example("3(2x + 5)", ["3 × 2x = 6x", "3 × 5 = 15"], "6x + 15"), example("12x + 8", ["GCF of 12 and 8 is 4", "4(3x + 2)"], "4(3x + 2)")],
        [['Multiplying only the first term: 3(x + 4) = 3x + 4', 'Multiply every term inside: 3x + 12.'], ['Adding unlike terms: 3x + 4 = 7x', '3x and 4 are not like terms.'], ['Mixing up commutative and associative', 'Commutative changes order; associative changes grouping.']])
    faq = [('What does TEKS 6.7C ask?', 'Determine if two expressions are equivalent using concrete models, pictorial models and algebraic representations.'), ('What does TEKS 6.7D ask?', 'Generate equivalent expressions using the properties of operations: inverse, identity, commutative, associative and distributive properties.'), ('How can I check if two expressions are equivalent?', 'Substitute the same value into both. If they differ for any value, they are not equivalent.'), ('What are like terms?', 'Terms with the same variable raised to the same power, like 4a and 9a.')]
    make('equivalent-expressions', 15, 'Expressions, Equations and Relationships', '6.7C, 6.7D',
         '6.7C determine if two expressions are equivalent using concrete models, pictorial models, and algebraic representations; 6.7D generate equivalent expressions using the properties of operations: inverse, identity, commutative, associative, and distributive properties',
         'Equivalent Expressions and Properties of Operations', 'Equivalent Expressions',
         'Free Grade 6 worksheets for Texas TEKS 6.7C and 6.7D: properties of operations, combining like terms, the distributive property, factoring with the GCF and equivalent expressions. 100 questions with answers.',
         'Equivalent expressions are equal for every value of the variable.', '3(x + 4) = 3x + 12. 5y + 2y = 7y.',
         body, faq, sets, seo_title='Grade 6 Equivalent Expressions and Properties of Operations Worksheets (TEKS 6.7C, 6.7D, STAAR)')


if __name__ == "__main__":
    build()
