# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Multiplying a 2-Digit Number by a 1-Digit Number (TEKS 3.4G)
  python3 tools/gen_ustx_math_g3_multiply_two_digit.py
Multiplying by multiples of 10 (the US Grade 3 maker with Texas names and new numbers), area models and partial
products, breaking apart with the distributive property, the standard algorithm with regrouping, and word problems.
Wrong answers come from real mistakes: multiplying only the ones (6 × 47 = 242), adding the partial products
wrongly, forgetting the regrouped ten, and writing the regrouped ten instead of adding it.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, comma, run, adopt, svg_wrap, text,
                       GREEN, FILL, INK, BLUE, example)
import gen_us_math_g3_multiples_of_10 as us10

adopt(us10)
R = random.Random(60701)


def area2_svg(a, t, o):
    """Area model for a × (t tens + o ones): two rectangles, widths in proportion."""
    W = 380
    wt = W * t * 10 / float(t * 10 + o) if o else W
    wt = max(min(wt, W - 70), 150) if o else W
    h = 80
    s = ["<rect x='30' y='30' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (wt, h, FILL, GREEN),
         text(30 + wt / 2, 22, str(t * 10), 16), text(18, 30 + h / 2 + 5, str(a), 16),
         text(30 + wt / 2, 30 + h / 2 + 6, "%d × %d" % (a, t * 10), 15, col=INK, weight=400)]
    if o:
        s += ["<rect x='%.1f' y='30' width='%.1f' height='%d' fill='#e8f0fa' stroke='%s' stroke-width='2'/>" % (30 + wt, W - wt, h, GREEN),
              text(30 + wt + (W - wt) / 2, 22, str(o), 16), text(30 + wt + (W - wt) / 2, 30 + h / 2 + 6, "%d × %d" % (a, o), 15, col=INK, weight=400)]
    return svg_wrap(W + 40, h + 40, "".join(s), "area model for %d × %d split into %d and %d" % (a, t * 10 + o, t * 10, o))


def pick(r, regroup=None):
    a = r.randint(2, 9)
    n = r.randint(12, 98)
    if n % 10 == 0:
        return None
    if regroup is True and a * (n % 10) < 10:
        return None
    if regroup is False and a * (n % 10) >= 10:
        return None
    return a, n


# ------------------------------------------------------------ set 2: area models and partial products
def one_area(r):
    p = pick(r)
    if not p:
        return None
    a, n = p
    t, o = divmod(n, 10)
    kind = r.choice(["total", "part", "part"])
    pic = fig(area2_svg(a, t, o))
    if kind == "total":
        return mcq(pic + "Use the area model to find %d × %d." % (a, n), a * n, [a * t * 10 + o, a * t + a * o, a * n + a, a * t * 10 + a * o + 10],
                   "%d × %d = %d and %d × %d = %d. Add the partial products: %d + %d = <b>%d</b>." % (a, t * 10, a * t * 10, a, o, a * o, a * t * 10, a * o, a * n))
    which = r.choice(["tens", "ones"])
    if which == "tens":
        return mcq(pic + "What is the area of the bigger part (%d × %d)?" % (a, t * 10), a * t * 10, [a * t, a * t * 10 + a, (a + 1) * t * 10],
                   "%d × %d tens = %d tens = <b>%d</b>." % (a, t, a * t, a * t * 10))
    return mcq(pic + "%d × %d = %d. What else do you add to find %d × %d?" % (a, t * 10, a * t * 10, a, n), "%d × %d = %d" % (a, o, a * o),
               ["%d × %d = %d" % (a, t, a * t), "%d + %d = %d" % (a, o, a + o), "%d × %d = %d" % (a, n, a * n)],
               "%d is %d + %d. You still need the ones part: <b>%d × %d = %d</b>." % (n, t * 10, o, a, o, a * o))


# ------------------------------------------------------------ set 3: break apart (distributive property)
def one_break(r):
    p = pick(r)
    if not p:
        return None
    a, n = p
    t, o = divmod(n, 10)
    kind = r.choice(["expr", "expr", "fill"])
    if kind == "expr":
        right = "(%d × %d) + (%d × %d)" % (a, t * 10, a, o)
        wrong = ["(%d × %d) + %d" % (a, t * 10, o), "(%d × %d) + (%d × %d)" % (a, t, a, o), "(%d + %d) × (%d + %d)" % (a, t * 10, a, o)]
        return mcq("Which expression has the same value as %d × %d?" % (a, n), right, wrong,
                   "Break %d into %d + %d and multiply each part by %d: <b>%s</b> = %d + %d = %d." % (n, t * 10, o, a, right, a * t * 10, a * o, a * n))
    return mcq("%d × %d = (%d × %d) + (%d × ☐). What number goes in the box?" % (a, n, a, t * 10, a), o, [t, n, a, t * 10],
               "%d = %d + %d, so the box is <b>%d</b>." % (n, t * 10, o, o))


# ------------------------------------------------------------ set 4: standard algorithm
def one_std(r):
    p = pick(r, regroup=r.random() < 0.75)
    if not p:
        return None
    a, n = p
    t, o = divmod(n, 10)
    carry = a * o // 10
    kind = r.choice(["product", "product", "carry"])
    if kind == "carry" and carry:
        return mcq("Multiply %d × %d with the standard algorithm. First, %d × %d = %d. What do you write in the ones place, and what do you regroup?" % (n, a, a, o, a * o),
                   "Write %d, regroup %d ten%s" % (a * o % 10, carry, "" if carry == 1 else "s"),
                   ["Write %d, regroup %d" % (carry, a * o % 10) if a * o % 10 != carry else "Write %d, regroup %d tens" % (a * o, 0), "Write %d, regroup nothing" % (a * o), "Write %d, regroup %d tens" % (a * o % 10, carry + 1)],
                   "%d = %d tens and %d ones. Write the %d ones, and regroup <b>%d ten%s</b> to add to the tens." % (a * o, carry, a * o % 10, a * o % 10, carry, "" if carry == 1 else "s"))
    no_carry = (a * t % 10) * 10 + a * o % 10 + a * t // 10 * 100
    return mcq("What is %d × %d?" % (n, a), a * n, [no_carry if no_carry != a * n else a * n + 10, a * t * 10 + o, a * o + t * 10, a * n + 10 if no_carry != a * n + 10 else a * n - 10],
               "Ones: %d × %d = %d%s. Tens: %d × %d = %d tens%s. So %d × %d = <b>%s</b>." % (a, o, a * o, ", write %d and regroup %d" % (a * o % 10, carry) if carry else "", a, t, a * t, " plus %d regrouped = %d tens" % (carry, a * t + carry) if carry else "", n, a, comma(a * n)))


# ------------------------------------------------------------ set 5: word problems
STORIES = [("A Texas peach farm packs {n} peaches in each crate. How many peaches are in {a} crates?", "peaches"),
           ("Each bus to the science museum holds {n} students. How many students can {a} buses hold?", "students"),
           ("{k} saves {n} dollars each month for {a} months. How many dollars does {k} save?", "dollars"),
           ("A movie theater has {a} rows with {n} seats in each row. How many seats are there?", "seats"),
           ("A box holds {n} crayons. How many crayons are in {a} boxes?", "crayons"),
           ("{k} rides {n} miles on a bike each week. How many miles does {k} ride in {a} weeks?", "miles"),
           ("A baker makes {n} tortillas in a batch. How many tortillas are in {a} batches?", "tortillas")]


def one_story(r):
    p = pick(r)
    if not p:
        return None
    a, n = p
    t_, unit = r.choice(STORIES)
    k = Kid(r).next()
    q = t_.format(a=a, n=n, k=k["n"])
    t, o = divmod(n, 10)
    return mcq(q, "%s %s" % (comma(a * n), unit), ["%d %s" % (a + n, unit), "%d %s" % (a * t * 10 + o, unit), "%d %s" % (a * n + 10, unit), "%d %s" % (a * n - a, unit)],
               "%d × %d = (%d × %d) + (%d × %d) = %d + %d = <b>%s %s</b>." % (a, n, a, t * 10, a, o, a * t * 10, a * o, comma(a * n), unit))


def build():
    s1 = run(us10.set_facts, "rnd", "seen", seed=91)["items"]
    sets = [S("Multiply by multiples of 10", s1),
            S("Area models and partial products", collect(one_area, 20, R)),
            S("Break apart: the distributive property", collect(one_break, 20, R)),
            S("The standard algorithm", collect(one_std, 20, R)),
            S("Word problems", collect(one_story, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>Break the 2-digit number into tens and ones: 47 = 40 + 7.</li>"
        "<li>Multiply each part, then add the <b>partial products</b>: 6 × 47 = (6 × 40) + (6 × 7) = 240 + 42 = 282.</li>"
        "<li>An <b>area model</b> shows the two parts as two rectangles.</li>"
        "<li>In the <b>standard algorithm</b>, multiply the ones first. If the product is 10 or more, regroup the tens and add them after you multiply the tens.</li></ul>",
        [figure(area2_svg(6, 4, 7), "6 × 47: 6 × 40 = 240 and 6 × 7 = 42. 240 + 42 = 282."),
         example("Find 38 × 4 with the standard algorithm.", ["Ones: 4 × 8 = 32. Write 2, regroup 3 tens.", "Tens: 4 × 3 = 12 tens. Add the 3 regrouped tens: 15 tens.", "Write 15 tens as 150 and add the 2."], "152")],
        [["Multiplying only the ones: 6 × 47 = 242", "Multiply both the tens and the ones."],
         ["Forgetting the regrouped tens", "Write the regrouped ten above the tens column and add it."],
         ["Writing 6 × 4 = 24 instead of 6 × 40 = 240", "The 4 in 47 means 4 tens, so the partial product is 240."]])
    faq = [("What does TEKS 3.4G ask?", "Use strategies and algorithms, including the standard algorithm, to multiply a 2-digit number by a 1-digit number. Strategies include mental math, partial products and the properties of operations."),
           ("What are partial products?", "The products you get when you multiply the tens and the ones separately, like 6 × 40 = 240 and 6 × 7 = 42. Their sum is the answer."),
           ("How does an area model help?", "It shows the number split into tens and ones as two rectangles, so you can see both partial products."),
           ("When do Texas students learn the standard algorithm?", "Grade 3 students start with a 2-digit by 1-digit number (TEKS 3.4G). Grade 4 extends it to bigger numbers.")]
    make("multiplying-two-digit-by-one-digit", 7, "Number and Operations", "3.4G",
         "3.4G use strategies and algorithms, including the standard algorithm, to multiply a two-digit number by a one-digit number. Strategies may include mental math, partial products, and the commutative, associative, and distributive properties",
         "Multiplying a 2-Digit Number by a 1-Digit Number", "Multiplying 2-Digit by 1-Digit Numbers",
         "Free Grade 3 worksheets for Texas TEKS 3.4G: multiply by multiples of 10, area models, partial products, the distributive property, the standard algorithm with regrouping and word problems. 100 questions with answers.",
         "Multiply the tens and the ones, then add.", "6 × 47 = (6 × 40) + (6 × 7) = 240 + 42 = 282. In the standard algorithm, regroup and add the extra tens.",
         body, faq, sets, seo_title="Grade 3 Multiplying 2-Digit by 1-Digit Numbers Worksheets (TEKS 3.4G, STAAR)")


if __name__ == "__main__":
    build()
