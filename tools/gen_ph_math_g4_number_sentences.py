# -*- coding: utf-8 -*-
"""
Philippines Grade 4 Math (MATATAG): Completing Number Sentences: Properties of Operations and Equivalent Facts (Grade 4: Number and Algebra)
  python3 tools/gen_ph_math_g4_number_sentences.py
Completing number sentences that show the commutative, associative, identity, zero and distributive properties (US
Grade 3 makers and own makers), and number sentences with equivalent number facts such as 4 + ☐ = 6 + 3 and
6 × ☐ = 3 × 8 (own makers).
Wrong answers come from real mistakes: writing the answer of the left side in the box, adding the numbers that are
shown, and thinking subtraction can be turned around.
"""
import ph_common
from ph_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example, peso, words)
import random
import gen_us_math_g3_properties as usq
adopt(usq)
if hasattr(usq, 'R'): usq.R = random.Random(704240)
ph_common.GRADE = "grade-4"

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


PROPS = ["Commutative property of addition", "Associative property of addition", "Identity property of addition", "Commutative property of multiplication",
         "Associative property of multiplication", "Identity property of multiplication", "Zero property of multiplication", "Distributive property"]


def one_prop(r):
    a, b, c = r.sample(range(2, 60), 3)
    s, t = r.randint(2, 9), r.randint(2, 9)
    kind = r.randrange(8)
    if kind == 0:
        sent, ans, blank = "%d + %d = %d + ☐" % (a, b, b), a, PROPS[0]
    elif kind == 1:
        sent, ans, blank = "(%d + %d) + %d = %d + (☐ + %d)" % (a, b, c, a, c), b, PROPS[1]
    elif kind == 2:
        sent, ans, blank = "%d + ☐ = %d" % (a, a), 0, PROPS[2]
    elif kind == 3:
        sent, ans, blank = "%d × %d = ☐ × %d" % (s, t, s), t, PROPS[3]
        if s == t:
            raise AssertionError
    elif kind == 4:
        u = r.randint(2, 9)
        sent, ans, blank = "(%d × %d) × %d = %d × (%d × ☐)" % (s, t, u, s, t), u, PROPS[4]
    elif kind == 5:
        sent, ans, blank = "%d × ☐ = %d" % (a, a), 1, PROPS[5]
    elif kind == 6:
        sent, ans, blank = "%d × ☐ = 0" % a, 0, PROPS[6]
    else:
        u = r.randint(2, 9)
        sent, ans, blank = "%d × (%d + %d) = (%d × %d) + (%d × ☐)" % (s, t, u, s, t, s), u, PROPS[7]
    if r.random() < 0.5:
        cands = [x for x in PROPS if x != blank]
        r.shuffle(cands)
        if "multiplication" in blank:
            cands.sort(key=lambda x: "multiplication" not in x)
        return mcq("Complete the number sentence: <b>%s</b>. Which property does it show?" % sent, blank, cands[:3],
                   "☐ = %d. The sentence shows the <b>%s</b>." % (ans, blank.lower()))
    wr = {0: [a + b, b, a - 1], 1: [a, c, a + b], 2: [a, 1, a + a], 3: [s, s * t, t + 1], 4: [s, t, s * t], 5: [0, a, 10], 6: [1, a, 10], 7: [t, s, t + u if kind == 7 else 1]}[kind]
    return mcq("What number goes in the box? <b>%s</b>" % sent, ans, wr, "This is the %s, so ☐ = <b>%d</b>." % (blank.lower(), ans), allow_zero=True)


def one_eq_add(r):
    a, b, c = r.randint(2, 60), r.randint(2, 60), r.randint(2, 60)
    kind = r.choice(["add", "add", "sub", "mix"])
    if kind == "add":
        total = b + c
        if total <= a:
            raise AssertionError
        x = total - a
        sent = "%d + ☐ = %d + %d" % (a, b, c)
        wr = [total, a + b + c, abs(b - a) + c if abs(b - a) + c != x else x + 1]
        e = "%d + %d = %d. So %d + ☐ must also be %d: ☐ = %d − %d = <b>%d</b>." % (b, c, total, a, total, total, a, x)
    elif kind == "sub":
        big = r.randint(30, 99)
        d = r.randint(2, big - 10)
        a2 = big + r.randint(1, 20)
        x = a2 - (big - d)
        sent = "%d − ☐ = %d − %d" % (a2, big, d)
        wr = [big - d, d, x + 2]
        e = "%d − %d = %d. So %d − ☐ must also be %d: ☐ = %d − %d = <b>%d</b>." % (big, d, big - d, a2, big - d, a2, big - d, x)
    else:
        total = a + b
        if total <= c:
            raise AssertionError
        x = total - c
        sent = "%d + %d = ☐ + %d" % (a, b, c)
        wr = [total, total + c, x + 10]
        e = "%d + %d = %d. ☐ + %d must also be %d: ☐ = <b>%d</b>." % (a, b, total, c, total, x)
    return mcq("What number makes the sentence true? <b>%s</b>" % sent, x, wr, e)


def one_eq_mul(r):
    kind = r.choice(["mul", "mul", "div"])
    if kind == "mul":
        a, b = r.randint(2, 12), r.randint(2, 12)
        p = a * b
        ds = [d for d in range(2, 13) if p % d == 0 and d not in (a, b) and p // d <= 12]
        if not ds:
            raise AssertionError
        c = r.choice(ds)
        x = p // c
        sent = "%d × ☐ = %d × %d" % (c, a, b)
        wr = [p, a + b - c if a + b - c > 0 else a + b, a if a != x else b]
        e = "%d × %d = %d. %d × ☐ must also be %d: ☐ = %d ÷ %d = <b>%d</b>." % (a, b, p, c, p, p, c, x)
    else:
        q = r.randint(2, 12)
        d1, d2 = r.sample(range(2, 10), 2)
        sent = "%d ÷ ☐ = %d ÷ %d" % (q * d1, q * d2, d2)
        x = d1
        wr = [q, q * d2, d2]
        e = "%d ÷ %d = %d. %d ÷ ☐ must also be %d: ☐ = %d ÷ %d = <b>%d</b>." % (q * d2, d2, q, q * d1, q, q * d1, q, x)
    return mcq("What number makes the sentence true? <b>%s</b>" % sent, x, wr, e)


def one_true(r):
    a, b, c = r.randint(5, 50), r.randint(5, 50), r.randint(2, 9)
    good = ["%d + %d = %d + %d" % (a, b, b, a), "%d × %d = %d × %d" % (c, a, a, c), "%d + %d = %d + %d" % (a, b, a + 1, b - 1), "%d × %d = %d × %d" % (2 * c, a, c, 2 * a)]
    bad = ["%d − %d = %d − %d" % (max(a, b), min(a, b), min(a, b), max(a, b)), "%d ÷ %d = %d ÷ %d" % (c * a, c, c, c * a), "%d + %d = %d + %d" % (a, b, a + 1, b + 1),
           "%d × %d = %d × %d" % (c, a, c + 1, a - 1)]
    if a == b:
        raise AssertionError
    ev = lambda t: [eval(x.replace("×", "*").replace("÷", "/").replace("−", "-")) for x in t.split(" = ")]
    if not all(ev(t)[0] == ev(t)[1] for t in good) or any(ev(t)[0] == ev(t)[1] for t in bad):
        raise AssertionError
    if r.random() < 0.5:
        g = r.choice(good)
        return mcq("Which number sentence is <b>true</b>?", g, r.sample(bad, 3), "Work out both sides: %s. Both sides are equal. The others are not. <b>%s</b>." % (g, g))
    b_ = r.choice(bad)
    return mcq("Which number sentence is <b>not</b> true?", b_, r.sample(good, 3), "The two sides of %s are not equal. Subtraction and division cannot be turned around, and changing the numbers must keep the same value. <b>%s</b>." % (b_, b_))


def build():
    sets, R = build_sets([
        ("Turn-around facts", [("run", usq.set_commutative, ("rnd",), 10), ("collect", uniq(one_prop), 10)]),
        ("Grouping and splitting", [("run", usq.set_associative, ("rnd",), 10), ("run", usq.set_distributive, ("rnd",), 10)]),
        ("Equivalent addition and subtraction facts", [("collect", uniq(one_eq_add), 20)]),
        ("Equivalent multiplication and division facts", [("collect", uniq(one_eq_mul), 20)]),
        ("Properties and true sentences", [("collect", uniq(one_prop), 12), ("collect", one_true, 8)]),
    ], 70424)
    finish(sets, R)
    body = lesson('<ul><li>The equal sign means <b>both sides have the same value</b>. It does not mean “the answer comes next”.</li><li>Properties: you can add or multiply in any order (commutative: 4 + 3 = 3 + 4), and group the numbers any way (associative). Adding 0 or multiplying by 1 keeps the number (identity). Multiplying by 0 gives 0.</li><li>For equivalent facts like 4 + ☐ = 6 + 3, work out the side you know (9), then find the number that makes the other side 9.</li><li>Subtraction and division cannot be turned around.</li></ul>',
        [example("4 + ☐ = 6 + 3", ["6 + 3 = 9", "4 + 5 = 9"], "5"), example("6 × ☐ = 3 × 8", ["3 × 8 = 24", "24 ÷ 6 = 4"], "4")],
        [['Writing the left side’s answer', 'In 4 + ☐ = 6 + 3, ☐ is not 4 + 6 or 9.'], ['Adding the numbers you see', 'Make both sides equal.'], ['Turning subtraction around', '9 − 4 is not 4 − 9.']])
    faq = [('What does MATATAG Math 4 ask about number sentences?', 'Complete a number sentence to represent a property of operations (for example 4 + 3 = 3 + __) and to represent equivalent number facts (for example 4 + __ = 6 + 3).'), ('What is the commutative property?', 'Changing the order of the numbers in addition or multiplication does not change the answer.'), ('Does the commutative property work for subtraction?', 'No.'), ('Why learn equivalent facts?', 'They help with mental math and with solving equations later.')]
    make('number-sentences-properties-and-equivalent-facts', 24, 'Number and Algebra', 'Grade 4: Number and Algebra',
         'Complete a number sentence to represent a property of operations (e.g., 4 + 3 = 3 + __, commutative property of addition), and to represent equivalent number facts (e.g., 4 + __ = 6 + 3).',
         'Completing Number Sentences: Properties of Operations and Equivalent Facts', 'Number Sentences',
         'Free Grade 4 number sentence worksheets for the DepEd MATATAG curriculum: commutative, associative, identity and distributive properties and equivalent number facts. 100 questions with answers.',
         'The equal sign means both sides have the same value.', 'Work out the side you know first.',
         body, faq, sets, seo_title=None)


if __name__ == "__main__":
    build()
