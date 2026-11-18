# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Place Value to 100,000 (TEKS 3.2A, 3.2B)
  python3 tools/gen_ustx_math_g3_place_value.py
Read and write numbers to 100,000, the value of a digit, expanded form and expanded notation, composing and
decomposing in more than one way (14 hundreds), and the 10 times relationship between places.
Wrong answers come from real mistakes: reading the digit instead of its value, forgetting a zero placeholder
(40,050 written as 4,050), mixing up expanded form and expanded notation, and thinking 14 hundreds is not allowed.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, comma, words, pv_chart_svg,
                       PLACES_PV, PLACE_VAL, example)

R = random.Random(60101)


def rnum(r, lo=1000, hi=99999, zeros=True):
    n = r.randint(lo, hi)
    if zeros and r.random() < 0.35:
        s = list(str(n))
        i = r.randrange(1, len(s))
        s[i] = "0"
        n = int("".join(s))
    return n


def drop_zero(n):
    s = str(n)
    i = s.find("0", 1)
    return int(s[:i] + s[i + 1:]) if i > 0 else None


def swap2(n):
    s = list(str(n))
    for i in range(len(s) - 1):
        if s[i] != s[i + 1]:
            s[i], s[i + 1] = s[i + 1], s[i]
            return int("".join(s)) if s[0] != "0" else None
    return None


def expanded(n):
    s = str(n)
    parts = [comma(int(d) * 10 ** (len(s) - 1 - i)) for i, d in enumerate(s) if d != "0"]
    return " + ".join(parts)


def notation(n):
    s = str(n)
    parts = ["(%s × %s)" % (d, comma(10 ** (len(s) - 1 - i))) for i, d in enumerate(s) if d != "0"]
    return " + ".join(parts)


# ------------------------------------------------------------ set 1: read and write numbers
def one_read(r):
    n = rnum(r)
    kind = r.choice(["chart", "to_words", "to_num", "to_num"])
    if kind == "chart":
        return mcq(fig(pv_chart_svg(n)) + "What number does the place value chart show?", n, [drop_zero(n), swap2(n), n + 10000 if n < 90000 else n - 10000, int(str(n)[::-1]) if str(n)[-1] != "0" else None],
                   "Read the digits from left to right and put a comma after the thousands: <b>%s</b>." % comma(n))
    if kind == "to_words":
        wrong = [swap2(n), drop_zero(n), n + 1000 if n < 98000 else n - 1000, n + 100]
        wrong = [words(w) for w in wrong if w]
        return mcq("How do you write <b>%s</b> in words?" % comma(n), words(n), wrong,
                   "Say the thousands first, then the rest: <b>%s</b>." % words(n))
    wrong = [drop_zero(n), swap2(n), n * 10 if n < 10000 else n // 10 if n % 10 == 0 else n + 10]
    return mcq("Which number is <b>%s</b>?" % words(n), n, wrong + [n + 100 if n < 99900 else n - 100],
               "%s thousand is %s. Then add the rest: <b>%s</b>." % (words(n // 1000).capitalize(), comma(n // 1000 * 1000), comma(n)))


# ------------------------------------------------------------ set 2: value of a digit
def one_value(r):
    n = rnum(r, 10000, 99999, zeros=False)
    p = r.randrange(0, 5)
    d = int(str(n)[4 - p])
    if d == 0 or d == 1:
        return None
    v = d * PLACE_VAL[p]
    kind = r.choice(["value", "value", "place"])
    if kind == "value":
        wrong = [d, d * PLACE_VAL[p + 1] if p < 4 else d * 10, d * PLACE_VAL[p - 1] if p > 0 else d * 100, d * 1000 if p != 3 else d * 100]
        return mcq(fig(pv_chart_svg(n, red=p)) + "What is the value of the red digit?", v, wrong,
                   "The %d is in the %s place, so its value is %d × %s = <b>%s</b>." % (d, PLACES_PV[p], d, comma(PLACE_VAL[p]), comma(v)))
    return mcq("In %s, which digit is in the <b>%s</b> place?" % (comma(n), PLACES_PV[p]), str(d),
               [c for c in dict.fromkeys(str(n)) if c != str(d)] + ["0"],
               "Count places from the right: ones, tens, hundreds, thousands, ten thousands. The %s digit is <b>%d</b>." % (PLACES_PV[p], d))


# ------------------------------------------------------------ set 3: expanded form and expanded notation
def one_expand(r):
    n = rnum(r, 10000, 99999)
    kind = r.choice(["form", "notation", "back"])
    m1, m2 = drop_zero(n), swap2(n)
    if kind == "form":
        wrong = [expanded(x) for x in (m2, m1, n + 1000 if n < 98000 else n - 1000) if x]
        wrong.append(" + ".join(str(c) for c in str(n) if c != "0"))
        return mcq("Which shows %s in <b>expanded form</b>?" % comma(n), expanded(n), wrong,
                   "Write the value of each digit and add them: <b>%s</b>." % expanded(n))
    if kind == "notation":
        wrong = [notation(x) for x in (m2, m1, n + 100 if n < 99800 else n - 100) if x] + [expanded(n)]
        return mcq("Which shows %s in <b>expanded notation</b>?" % comma(n), notation(n), wrong,
                   "Expanded notation shows each digit times its place value: <b>%s</b>." % notation(n))
    wrong = [m1, m2, int(str(n).replace("0", "")) if "0" in str(n) else n + 10, n + 10000 if n < 90000 else n - 10000]
    return mcq("What number is %s?" % (expanded(n) if r.random() < 0.5 else notation(n)), n, wrong,
               "Put each digit in its place. Use 0 for a place with no value: <b>%s</b>." % comma(n))


# ------------------------------------------------------------ set 4: compose and decompose
def one_compose(r):
    kind = r.choice(["many", "how_many", "how_many", "other_way"])
    if kind == "many":
        tt, th, h, t, o = r.randint(1, 8), r.randint(10, 19), r.randint(0, 9), r.randint(0, 9), r.randint(0, 9)
        n = tt * 10000 + th * 1000 + h * 100 + t * 10 + o
        q = "What number is %d ten thousands, %d thousands, %d hundreds, %d tens and %d ones?" % (tt, th, h, t, o)
        wrong = [int("%d%d%d%d%d" % (tt, th, h, t, o)) if int("%d%d%d%d%d" % (tt, th, h, t, o)) < 1000000 else None,
                 tt * 10000 + (th % 10) * 1000 + h * 100 + t * 10 + o, n + 10000, n - 1000]
        return mcq(q, n, wrong, "%d thousands is %s. So the number is %s + %s + %d + %d + %d = <b>%s</b>." % (th, comma(th * 1000), comma(tt * 10000), comma(th * 1000), h * 100, t * 10, o, comma(n)))
    if kind == "how_many":
        unit = r.choice([(100, "hundreds"), (1000, "thousands"), (10, "tens")])
        k = r.randint(12, 95) if unit[0] != 10 else r.randint(120, 950)
        n = k * unit[0]
        return mcq("How many <b>%s</b> are in %s?" % (unit[1], comma(n)), k, [k // 10 if k >= 20 else k * 10, int(str(k)[-1]), k * 10, k + 1],
                   "%s = %s × %s. There are <b>%s</b> %s." % (comma(n), comma(k), comma(unit[0]), comma(k), unit[1]))
    n = rnum(r, 10000, 99999, zeros=False)
    tt, th, h = n // 10000, (n // 1000) % 10, (n // 100) % 10
    rest = n % 100
    right = "%d ten thousands, %d thousands, %d hundreds and %d" % (tt - 1, th + 10, h, rest)
    wrong = ["%d ten thousands, %d thousands, %d hundreds and %d" % (tt - 1, th, h, rest),
             "%d ten thousands, %d thousands, %d hundreds and %d" % (tt, th + 10, h, rest),
             "%d ten thousands, %d thousands, %d hundreds and %d" % (tt - 1, th + 1, h, rest)]
    if tt < 2:
        return None
    return mcq("Which is another way to make %s?" % comma(n), right, wrong,
               "Break 1 ten thousand into 10 thousands: %d ten thousands and %d thousands. <b>%s</b>." % (tt - 1, th + 10, right.capitalize()))


# ------------------------------------------------------------ set 5: 10 times and word problems
def one_ten(r):
    kind = r.choice(["times", "times", "story", "story", "between"])
    if kind == "times":
        d = r.randint(2, 9)
        p = r.randint(0, 3)
        a, b = d * PLACE_VAL[p], d * PLACE_VAL[p + 1]
        if r.random() < 0.5:
            return mcq("The value of %d in %s is how many times the value of %d in %s?" % (d, comma(b), d, comma(a)), 10, [100, 1000, d],
                       "%s is 10 times %s. Each place is <b>10</b> times the place to its right." % (comma(b), comma(a)))
        return mcq("What is 10 times %s?" % comma(a), b, [a * 100, a + 10, a * 10 // 100 if a >= 100 else None, a * 10 + 10],
                   "10 times moves each digit one place to the left: <b>%s</b>." % comma(b))
    if kind == "between":
        a = r.choice([(10, "tens", 1000, "thousand"), (100, "hundreds", 10000, "ten thousand"), (10, "tens", 100, "hundred"),
                      (1000, "thousands", 100000, "hundred thousand"), (100, "hundreds", 1000, "thousand")])
        k = a[2] // a[0]
        return mcq("How many %s make 1 %s?" % (a[1], a[3]), k, [k * 10, k // 10 if k >= 10 else 5, 10 if k != 10 else 1000],
                   "%s ÷ %s = %s. <b>%s</b> %s make 1 %s." % (comma(a[2]), comma(a[0]), comma(k), comma(k), a[1], a[3]))
    item, size = r.choice([("sheets of paper", 100), ("stickers", 100), ("beads", 1000), ("tickets", 1000), ("pennies", 100)])
    box = "box" if size == 1000 else "pack"
    boxes = "boxes" if box == "box" else "packs"
    k = r.randint(12, 60) if size == 100 else r.randint(11, 45)
    n = k * size
    if r.random() < 0.5:
        return mcq("A store has %s %s. They come in %s of %s. How many %s is that?" % (comma(n), item, boxes, comma(size), boxes), k, [k * 10, k // 10 if k >= 20 else k + 10, n // 10],
                   "%s = %s × %s, so it is <b>%s</b> %s." % (comma(n), comma(k), comma(size), comma(k), boxes))
    return mcq("A school orders %s %s of %s, %s in each %s. How many %s is that?" % (comma(k), boxes, item, comma(size), box, item), n, [k * size // 10, k * size * 10, k + size],
               "%s %s of %s is %s × %s = <b>%s</b>." % (comma(k), boxes, comma(size), comma(k), comma(size), comma(n)))


def build():
    sets = [S("Read and write numbers", collect(one_read, 20, R)),
            S("The value of a digit", collect(one_value, 20, R)),
            S("Expanded form and expanded notation", collect(one_expand, 20, R)),
            S("Compose and decompose numbers", collect(one_compose, 20, R)),
            S("10 times as much and word problems", collect(one_ten, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>Each digit has a <b>place</b>: ones, tens, hundreds, thousands, ten thousands. Its <b>value</b> is the digit times its place.</li>"
        "<li>Each place is <b>10 times</b> the place to its right. 10 hundreds make 1 thousand; 10 thousands make 1 ten thousand.</li>"
        "<li><b>Expanded form</b> adds the values: 40,000 + 5,000 + 200 + 6. <b>Expanded notation</b> shows the multiplication: (4 × 10,000) + (5 × 1,000) + (2 × 100) + (6 × 1).</li>"
        "<li>A number can be made in more than one way: 45,206 is also 3 ten thousands, 15 thousands, 2 hundreds and 6 ones.</li></ul>",
        [figure(pv_chart_svg(45206, red=3), "In 45,206 the red 5 is in the thousands place. Its value is 5,000."),
         example("Write 30,405 in expanded form.", ["3 ten thousands = 30,000", "0 thousands: skip", "4 hundreds = 400", "0 tens: skip", "5 ones = 5"], "30,000 + 400 + 5")],
        [["Saying the digit, not its value", "Multiply by the place: the 5 in 45,206 is worth 5,000."],
         ["Leaving out a zero: 40,050 written as 4,050", "Use 0 to hold every empty place."],
         ["Thinking a place can only hold 0 to 9 when you decompose", "14 thousands is fine. It is 1 ten thousand and 4 thousands."]])
    faq = [("What does TEKS 3.2A ask Grade 3 students to do?", "Compose and decompose numbers up to 100,000 as so many ten thousands, thousands, hundreds, tens and ones, with pictures, numbers and expanded notation."),
           ("What is the difference between expanded form and expanded notation?", "Expanded form adds the value of each digit (40,000 + 5,000 + 6). Expanded notation shows each digit times its place value ((4 × 10,000) + (5 × 1,000) + (6 × 1))."),
           ("What is the 10 times relationship?", "Each place is worth 10 times the place to its right. The 3 in 3,000 is worth 10 times the 3 in 300 (TEKS 3.2B)."),
           ("How is place value tested on the STAAR?", "Questions ask for the value of a digit, which number matches a model or expanded notation, and another way to make a number, such as 15 thousands instead of 1 ten thousand and 5 thousands.")]
    make("place-value-to-100000", 1, "Number and Operations", "3.2A, 3.2B",
         "3.2A compose and decompose numbers up to 100,000 as a sum of so many ten thousands, so many thousands, so many hundreds, so many tens, and so many ones using objects, pictorial models, and numbers, including expanded notation as appropriate; 3.2B describe the mathematical relationships found in the base-10 place value system through the hundred thousands place",
         "Place Value to 100,000: Expanded Notation and Composing Numbers", "Place Value to 100,000",
         "Free Grade 3 place value worksheets for Texas TEKS 3.2A and 3.2B: read and write numbers to 100,000, the value of a digit, expanded form and expanded notation, composing numbers in different ways and the 10 times relationship. 100 STAAR-style questions with answers.",
         "A digit's value is the digit times its place.", "Each place is 10 times the place to its right. 14 thousands is the same as 1 ten thousand and 4 thousands.",
         body, faq, sets, seo_title="Grade 3 Place Value to 100,000 Worksheets: Expanded Notation (TEKS 3.2A, STAAR)")


if __name__ == "__main__":
    build()
