# -*- coding: utf-8 -*-
"""
Texas Grade 4 Math: Multiplying by 10 and 100 (TEKS 4.4B)
  python3 tools/gen_ustx_math_g4_times_10_100.py
Products of a number and 10 or 100 using place value and properties of operations, missing factors, multiplying
tens and hundreds by a 1-digit number, and word problems.
Wrong answers come from real mistakes: adding a zero instead of multiplying by 100, writing one zero for 100, and
mixing up 10 and 100.
"""
import tx_common
from tx_common import (finish, make, lesson, adopt, People, Kid, mcq, fig, figure, fr, comma, build_sets, example)

tx_common.GRADE = "grade-4"

def one_basic(r):
    n = r.choice([r.randint(2, 99), r.randint(100, 999), r.randint(1000, 9999)])
    m = r.choice([10, 100])
    return mcq("%s × %d = ?" % (comma(n), m), comma(n * m), [comma(n * (110 - m)), comma(n + m), comma(n * m * 10), comma(n * m // 10) if n * m // 10 != n * (110 - m) else comma(n * m + m)],
               "Multiplying by %d moves each digit %s to the left: <b>%s</b>." % (m, "one place" if m == 10 else "two places", comma(n * m)))


def one_missing(r):
    n = r.randint(3, 999)
    m = r.choice([10, 100])
    kind = r.choice(["factor", "mult"])
    if kind == "factor":
        return mcq("%s × ☐ = %s" % (comma(n), comma(n * m)), comma(m), [comma(110 - m), "1,000", comma(n * m - n)], "%s has %s more zero%s than %s: ☐ = <b>%d</b>." % (comma(n * m), "one" if m == 10 else "two", "" if m == 10 else "s", comma(n), m))
    return mcq("☐ × %d = %s" % (m, comma(n * m)), comma(n), [comma(n * 10 if m == 100 else n // 10 if n >= 10 else n * 100), comma(n * m // 100 if m == 100 else n + 10), comma(n + 1)],
               "Undo × %d: <b>%s</b>." % (m, comma(n)))


def one_tens(r):
    a = r.randint(2, 9)
    t = r.randint(2, 9)
    m = r.choice([10, 100])
    kind = r.choice(["val", "prop"])
    if kind == "val":
        return mcq("%d × %s = ?" % (a, comma(t * m)), comma(a * t * m), [comma(a * t), comma(a * t * m * 10), comma(a + t * m), comma(a * t * m // 10)],
                   "%d × %d = %d. Then × %d: <b>%s</b>." % (a, t, a * t, m, comma(a * t * m)))
    return mcq("Which shows how to find %d × %s?" % (a, comma(t * m)), "(%d × %d) × %d" % (a, t, m), ["(%d + %d) × %d" % (a, t, m), "%d × %d + %d" % (a, t, m), "(%d × %d) + %d" % (a, t * m, m)],
               "%s = %d × %d, so %d × %s = <b>(%d × %d) × %d</b> = %s (associative property)." % (comma(t * m), t, m, a, comma(t * m), a, t, m, comma(a * t * m)))


def one_story(r):
    k = Kid(r).next()
    kind = r.choice([("boxes", "pencils", 100), ("packs", "stickers", 10), ("rolls", "pennies", 100), ("bags", "marbles", 10), ("cases", "water bottles", 100), ("crates", "oranges", 100)])
    cont, thing, m = kind
    n = r.randint(3, 85)
    return mcq("A school buys %d %s of %s. Each has %d %s. How many %s is that?" % (n, cont, thing, m, thing, thing), comma(n * m), [comma(n + m), comma(n * (110 - m)), comma(n * m * 10)],
               "%d × %d = <b>%s</b>." % (n, m, comma(n * m)))


def one_compare(r):
    a = r.randint(2, 99)
    b = r.randint(2, 99)
    x, y = a * 100, b * 10
    if x == y:
        return None
    sym = "&gt;" if x > y else "&lt;"
    return mcq("Compare: %d × 100 ☐ %d × 10" % (a, b), sym, ["&lt;" if sym == "&gt;" else "&gt;", "=", "+"],
               "%d × 100 = %s and %d × 10 = %s, so use <b>%s</b>." % (a, comma(x), b, comma(y), sym))


def build():
    sets, R = build_sets([
        ("Multiply by 10 and 100", [("collect", one_basic, 20)]),
        ("Missing factors", [("collect", one_missing, 20)]),
        ("Multiply tens and hundreds", [("collect", one_tens, 20)]),
        ("Compare products", [("collect", one_compare, 20)]),
        ("Word problems", [("collect", one_story, 20)]),
    ], 64006)
    finish(sets, R)
    body = lesson('<ul><li>Multiplying by <b>10</b> makes each digit worth 10 times as much: every digit moves one place to the left and a 0 fills the ones place. 46 × 10 = 460.</li><li>Multiplying by <b>100</b> moves every digit two places to the left: 46 × 100 = 4,600.</li><li>Use facts and properties: 7 × 300 = (7 × 3) × 100 = 2,100.</li></ul>',
        [example("58 × 100", ["Each digit moves two places left."], "5,800"), example("6 × 400", ["6 × 4 = 24", "24 × 100 = 2,400"], "2,400")],
        [['Adding 100 instead of multiplying: 58 × 100 = 158', '× 100 makes the number 100 times as large.'], ['Writing only one zero for × 100', '100 has two zeros: move the digits two places.'], ['Mixing up 10 and 100', 'Count the zeros in the factor.']])
    faq = [('What does TEKS 4.4B ask?', 'Determine products of a number and 10 or 100 using properties of operations and place value understandings.'), ('Why does multiplying by 10 add a zero?', 'Every digit moves to a place worth 10 times as much, so the ones place becomes 0.'), ('How do you multiply 8 × 700?', '8 × 7 = 56, then 56 × 100 = 5,600.'), ('Does this work for big numbers?', 'Yes. 2,345 × 100 = 234,500.')]
    make('multiplying-by-10-and-100', 6, 'Number and Operations', '4.4B',
         '4.4B determine products of a number and 10 or 100 using properties of operations and place value understandings',
         'Multiplying by 10 and 100', 'Multiplying by 10 and 100',
         'Free Grade 4 worksheets for Texas TEKS 4.4B: multiply by 10 and 100, missing factors, multiply tens and hundreds with facts, compare products and word problems. 100 questions with answers.',
         '× 10 moves each digit one place left; × 100 moves it two places.', '7 × 300 = (7 × 3) × 100 = 2,100.',
         body, faq, sets, seo_title='Grade 4 Multiplying by 10 and 100 Worksheets (TEKS 4.4B, STAAR)')


if __name__ == "__main__":
    build()
