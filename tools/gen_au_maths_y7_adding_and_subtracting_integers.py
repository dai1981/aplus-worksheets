# -*- coding: utf-8 -*-
"""
AU Year 7 Maths: Adding and subtracting integers (Australian Curriculum v9.0: AC9M7N07)
  python3 tools/gen_au_maths_y7_adding_and_subtracting_integers.py
Comparing and ordering integers, adding positive and negative integers, subtracting, subtracting a negative,
and problems with temperatures, sea level, lifts and bank balances.
Wrong answers come from real mistakes: −7 > −2 because 7 > 2, ignoring a sign, treating "minus a negative"
as minus, and subtracting the wrong way round for a difference.
"""
import random
from fractions import Fraction as F
from au_hs import num, par, mcq, B, S, make, lesson, collect, People, aud, MINUS, QN, T

R = random.Random(70801)
P = People(R)


def Qn(q, ans, wrongs, e):
    return QN(q, ans, wrongs, e)


# ------------------------------------------------------------ set 1: comparing and ordering
def one_order(r):
    kind = r.choice(["sym", "sym", "list", "list", "between"])
    if kind == "sym":
        a, b = r.sample(range(-20, 15), 2)
        if a >= 0 and b >= 0:
            return None
        right = "&lt;" if a < b else "&gt;"
        q = "Which symbol makes this true? %s" % B("%s ☐ %s" % (num(a), num(b)))
        e = "%s is further %s on the number line than %s, so %s %s %s." % (num(a), "left" if a < b else "right", num(b), num(a), "&lt;" if a < b else "&gt;", num(b))
        return T(q, right, ["&gt;" if right == "&lt;" else "&lt;", "=", "You cannot compare negative numbers"], e)
    if kind == "list":
        vals = r.sample(range(-25, 20), 5)
        if sum(1 for v in vals if v < 0) < 2:
            return None
        asc = r.random() < 0.6
        right = ", ".join(num(v) for v in sorted(vals, reverse=not asc))
        by_digits = ", ".join(num(v) for v in sorted(vals, key=lambda v: (abs(v)), reverse=not asc))
        rev = ", ".join(num(v) for v in sorted(vals, reverse=asc))
        neg_wrong = ", ".join(num(v) for v in sorted([v for v in vals if v < 0], reverse=asc) + sorted([v for v in vals if v >= 0], reverse=not asc)) if asc else             ", ".join(num(v) for v in sorted([v for v in vals if v >= 0], reverse=True) + sorted([v for v in vals if v < 0]))
        q = "Write these integers in %s order: %s" % ("ascending (smallest to largest)" if asc else "descending (largest to smallest)", B(", ".join(num(v) for v in vals)))
        e = "On a number line, numbers further left are smaller. <b>%s</b>." % right
        wr = [w for w in dict.fromkeys([by_digits, neg_wrong, rev]) if w != right]
        if len(wr) < 3:
            return None
        return T(q, right, wr, e)
    a = r.randint(-30, -5)
    b = a + r.randint(4, 12)
    ins = r.randint(a + 1, b - 1)
    outs = [a - r.randint(1, 5), b + r.randint(1, 5), -ins if -ins > b or -ins < a else b + 7]
    q = "Which integer is between %s and %s?" % (num(a), num(b))
    return QN(q, ins, outs, "%s &lt; <b>%s</b> &lt; %s." % (num(a), num(ins), num(b)), near=())


# ------------------------------------------------------------ set 2: adding integers
def one_add(r):
    a = r.choice([r.randint(-15, -1), r.randint(1, 15)])
    b = r.randint(-15, -1)
    if r.random() < 0.3:
        a, b = b, a
    if a + b == 0:
        return None
    s = a + b
    q = "Work out %s." % B("%s + %s" % (num(a), par(b)))
    e = "Start at %s and move %d to the %s on the number line. The answer is <b>%s</b>." % (
        num(a), abs(b), "left" if b < 0 else "right", num(s))
    return Qn(q, s, [-s, a - b, abs(a) + abs(b), b - a], e)


def one_sub_pos(r):
    a = r.randint(-12, 9)
    b = r.randint(2, 15)
    s = a - b
    if a == 0 or s == 0 or s > 0:
        return None
    q = "Work out %s." % B("%s %s %d" % (num(a), MINUS, b))
    e = "Subtracting %d moves %d to the left: %s %s %d = <b>%s</b>." % (b, b, num(a), MINUS, b, num(s))
    return Qn(q, s, [-s, a + b, abs(a) - b if abs(a) != b else -(a + b) + 1, s + 1], e)




# ------------------------------------------------------------ set 3: subtracting
def one_sub_pos(r):
    a = r.randint(-12, 9)
    b = r.randint(2, 15)
    s = a - b
    if a == 0 or s == 0 or s > 0:
        return None
    q = "Work out %s." % B("%s %s %d" % (num(a), MINUS, b))
    e = "Subtracting %d moves %d to the left: %s %s %d = <b>%s</b>." % (b, b, num(a), MINUS, b, num(s))
    return Qn(q, s, [-s, a + b, abs(a) - b if abs(a) != b else -(a + b) + 1, s + 1], e)


def one_sub_neg(r):
    a = r.randint(-12, 12)
    b = r.randint(-12, -1)
    if a == 0 or a - b == 0:
        return None
    s = a - b
    q = "Work out %s." % B("%s %s %s" % (num(a), MINUS, par(b)))
    e = "Subtracting a negative is the same as adding: %s %s %s = %s + %d = <b>%s</b>." % (
        num(a), MINUS, par(b), num(a), -b, num(s))
    return Qn(q, s, [a + b, -s, -a + b, s - 2], e)




def one_mix(r):
    a, b, c = r.randint(-12, 12), r.randint(-12, 12), r.randint(-12, 12)
    if 0 in (a, b, c):
        return None
    ops = [r.choice(["+", MINUS]) for _ in range(2)]
    v = a
    for op, x in zip(ops, (b, c)):
        v = v + x if op == "+" else v - x
    q = "Work out %s." % B("%s %s %s %s %s" % (num(a), ops[0], par(b), ops[1], par(c)))
    naive = a
    for op, x in zip(ops, (b, c)):
        naive = naive + abs(x) if op == "+" else naive - abs(x)
    mid = a + b if ops[0] == "+" else a - b
    e = "Work from left to right: %s %s %s = %s, then %s %s %s = <b>%s</b>." % (num(a), ops[0], par(b), num(mid), num(mid), ops[1], par(c), num(v))
    return Qn(q, v, [naive, -v, v + 2], e)


# ------------------------------------------------------------ set 5: problems
def problems():
    its = []
    for city, t0, ch in [("Thredbo", 3, -8), ("Canberra", -2, 13), ("Hobart", 6, -9), ("Perisher", -5, 7), ("Ballarat", 1, -6)]:
        t1 = t0 + ch
        q = "At %s in %s the temperature was %s °C. It %s by %d degrees. What is the temperature now?" % (
            "dawn" if ch > 0 else "6 pm", city, num(t0), "rose" if ch > 0 else "fell overnight", abs(ch))
        e = "%s %s %d = <b>%s °C</b>." % (num(t0), "+" if ch > 0 else MINUS, abs(ch), num(t1))
        its.append(QN(q, t1, [t0 - ch, -t1, abs(t0) + abs(ch)], e, unit=" °C"))
    for lo, hi, a, b in [(-6, 9, "overnight in Canberra", "at lunchtime"), (-11, -3, "on Mt Kosciuszko at dawn", "at midday"),
                         (-4, 14, "in Thredbo at 5 am", "at 2 pm")]:
        d = hi - lo
        q = "The temperature was %s °C %s and %s °C %s. How many degrees warmer was it %s?" % (num(lo), a, num(hi), b, b)
        e = "Difference = %s %s %s = %s + %d = <b>%d degrees</b>." % (num(hi), MINUS, par(lo), num(hi), -lo, d)
        its.append(QN(q, d, [abs(hi + lo), abs(abs(lo) - abs(hi))], e, unit=" degrees", near=(1, 2, -1, 10)))
    for h, depth in [(45, -18), (150, -30), (12, -27)]:
        d = h - depth
        q = "A seagull is %d m above sea level. A diver on the Great Barrier Reef is at %s m. How far apart are they vertically?" % (h, num(depth))
        e = "%d %s %s = %d + %d = <b>%d m</b>." % (h, MINUS, par(depth), h, -depth, d)
        its.append(QN(q, d, [abs(h + depth), h, -depth], e, unit=" m"))
    for bal, out in [(55, 80), (25, 60), (-30, 45), (-12, 18)]:
        name, he, his = P.next()
        nb = bal - out
        f = lambda v: (MINUS if v < 0 else "") + aud(abs(v))
        q = "The balance of %s's bank account is %s. %s pays %s by card. What is the balance now?" % (name, f(bal), he.capitalize(), aud(out))
        e = "%s %s %d = <b>%s</b>." % (num(bal), MINUS, out, f(nb))
        its.append(QN(q, nb, [-nb, bal + out, -(abs(bal) + out)], e, fmt=f))
    for start, moves in [(2, [-3, +5]), (-2, [+6, -7]), (4, [-6, -1])]:
        end = start + sum(moves)
        lvl = lambda v: ("level %s" % num(v)) if v != 0 else "the ground floor (level 0)"
        q = "A lift starts at %s. It goes %s %d levels, then %s %d levels. Which level is it on now?" % (
            lvl(start), "down" if moves[0] < 0 else "up", abs(moves[0]), "down" if moves[1] < 0 else "up", abs(moves[1]))
        e = "%s %s = <b>%s</b>." % (num(start), " ".join(("+ %d" % m) if m > 0 else ("%s %d" % (MINUS, -m)) for m in moves), num(end))
        its.append(QN(q, end, [start + abs(moves[0]) + abs(moves[1]) if end != start + abs(moves[0]) + abs(moves[1]) else end + 2, -end, start - sum(moves)], e))
    data = [("Which is the coldest temperature?", "−9 °C", ["−3 °C", "0 °C", "2 °C"], "−9 is furthest left on the number line, so <b>−9 °C</b> is coldest."),
            ("A submarine is at −120 m. It rises 45 m. What is its new depth?", "−75 m", ["−165 m", "75 m", "−45 m"], "−120 + 45 = <b>−75 m</b>.")]
    its += [T(q, a, w, e) for q, a, w, e in data]
    return its


def body():
    return lesson(
        "<p>On a number line, numbers to the <b>left are smaller</b>: −9 &lt; −2 &lt; 0 &lt; 3.</p>"
        "<p>Adding a positive number moves right; adding a negative number moves left. Subtracting a positive moves left. "
        "<b>Subtracting a negative is the same as adding</b>: 3 − (−5) = 3 + 5 = 8.</p>"
        "<p>To find the difference between two temperatures, subtract the lower from the higher.</p>",
        [("Order −4, 2, −11, 0, 7 from smallest to largest.", ["Furthest left first."], "−11, −4, 0, 2, 7"),
         ("Work out −4 + (−6).", ["Start at −4 and move 6 to the left."], "−10"),
         ("Work out −2 − (−7).", ["Subtracting −7 is adding 7: −2 + 7."], "5")],
        ["Thinking −7 is bigger than −2 because 7 is bigger than 2.",
         "Treating 3 − (−5) as 3 − 5. Two minus signs next to each other make a plus.",
         "Thinking −4 + (−6) = 10. Adding a negative makes the number smaller.",
         "For a temperature difference, subtracting the wrong way: from −8 °C to 5 °C is 13 degrees, not 3."])


def main():
    sets = [S("Comparing and ordering integers", collect(one_order, 20, R)),
            S("Adding integers", collect(one_add, 20, R)),
            S("Subtracting integers", collect(one_sub_pos, 8, R) + collect(one_sub_neg, 12, R)),
            S("Adding and subtracting in one calculation", collect(one_mix, 20, R)),
            S("Integer problems", problems())]
    make(7, "adding-and-subtracting-integers", 8, "AC9M7N07",
         "Adding and Subtracting Integers: Ordering, Number Lines and Problems",
         "Year 7 Integers Worksheets: Comparing, Ordering, Adding and Subtracting Negative Numbers (Free, Answer Key)",
         "Adding and subtracting integers",
         "compare, order and solve problems involving addition and subtraction of integers",
         "Free Year 7 maths worksheets on integers for the Australian Curriculum (AC9M7N07): comparing and ordering, adding and "
         "subtracting negative numbers, subtracting a negative, and temperature, sea level and bank problems. 100 questions with an answer key.",
         "Subtracting a negative is adding: 3 − (−5) = 8.",
         "On a number line, further left is smaller, so −9 < −2.",
         body(),
         [("Why is −9 smaller than −2?", "−9 is further left on the number line. Being 9 below zero is colder than being 2 below zero."),
          ("Why does subtracting a negative number give a bigger answer?", "Taking away a debt leaves you better off. On the number line, 3 − (−5) is the gap from −5 up to 3, which is 8."),
          ("What is −4 + (−6)?", "−10. Adding a negative number moves you further left."),
          ("How do I find the difference between −8 °C and 5 °C?", "Subtract the lower from the higher: 5 − (−8) = 13 degrees.")],
         sets, R)


if __name__ == "__main__":
    main()
