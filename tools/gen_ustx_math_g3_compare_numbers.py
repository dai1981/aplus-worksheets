# -*- coding: utf-8 -*-
"""
Texas Grade 3 Math: Comparing and Ordering Numbers to 100,000 (TEKS 3.2D)
  python3 tools/gen_ustx_math_g3_compare_numbers.py
True comparisons with >, < and =, the greatest and least number, ordering from least to greatest, missing digits
and numbers between, and word problems with Texas towns, stadiums and school data.
Wrong answers come from real mistakes: comparing the last digits first, thinking a number with more 9s is
greater, reading > and < the wrong way round, and ordering greatest to least when asked for least to greatest.
"""
import random
from tx_common import (Kid, mcq, collect, finish, make, fig, figure, lesson, S, comma, pv_chart_svg, example, PLACES)

R = random.Random(60201)


def near_pair(r):
    """Two numbers that share their first digits and differ at one place."""
    n = r.randint(10000, 99999)
    s = list(str(n))
    i = r.randrange(1, 5)
    d = int(s[i])
    e = r.choice([x for x in range(10) if x != d])
    s[i] = str(e)
    m = int("".join(s))
    return n, m, i


# ------------------------------------------------------------ set 1: which comparison is true?
def one_true(r):
    n, m, i = near_pair(r)
    if r.random() < 0.3:
        m = int(str(n)[1:]) if str(n)[1] != "0" else m
    big, small = max(n, m), min(n, m)
    right = r.choice(["%s &gt; %s" % (comma(big), comma(small)), "%s &lt; %s" % (comma(small), comma(big))])
    wrong = ["%s &lt; %s" % (comma(big), comma(small)), "%s &gt; %s" % (comma(small), comma(big)), "%s = %s" % (comma(big), comma(small))]
    return mcq("Which comparison is true?", right, wrong,
               "Compare from the left. The first place where the digits differ decides it. %s is greater than %s, so <b>%s</b> is true." % (comma(big), comma(small), right))


# ------------------------------------------------------------ set 2: greatest and least
def one_most(r):
    n, m, i = near_pair(r)
    others = set([n, m])
    while len(others) < 4:
        a, b, _ = near_pair(r)
        x = int(str(n)[:2] + str(a)[2:]) if r.random() < 0.6 else a % 10000 if a % 10000 >= 1000 else a
        others.add(x)
    vals = list(others)
    r.shuffle(vals)
    word = r.choice(["greatest", "least"])
    t = max(vals) if word == "greatest" else min(vals)
    q = "Which number is the <b>%s</b>?<br>%s" % (word, "; ".join(comma(v) for v in vals))
    return mcq(q, t, [v for v in vals if v != t],
               "Line the numbers up by place value and compare from the left. The %s is <b>%s</b>." % (word, comma(t)))


# ------------------------------------------------------------ set 3: put in order
def one_order(r):
    base = r.randint(10, 98) * 1000
    vals = set()
    while len(vals) < 3:
        vals.add(base + r.choice([r.randint(100, 999), r.randint(10, 99) * 10, r.randint(1000, 1999)]))
    if r.random() < 0.4:
        vals.pop()
        vals.add(base // 10 + r.randint(1, 900) if base // 10 > 1000 else base + 3)
    vals = sorted(vals)
    up = r.random() < 0.5
    right = vals if up else vals[::-1]
    show = lambda v: "; ".join(comma(x) for x in v)
    opts = [vals[::-1] if up else vals, [vals[1], vals[0], vals[2]], [vals[0], vals[2], vals[1]], [vals[2], vals[0], vals[1]]]
    return mcq("Which list is in order from <b>%s</b>?" % ("least to greatest" if up else "greatest to least"), show(right), [show(o) for o in opts if o != right],
               "Compare from the left. %s: <b>%s</b>." % ("Smallest first" if up else "Largest first", show(right)))


# ------------------------------------------------------------ set 4: missing digits and numbers between
def one_between(r):
    kind = r.choice(["between", "digit", "symbol"])
    if kind == "between":
        a = r.randint(10, 97) * 1000
        b = a + r.choice([1000, 2000])
        t = r.randint(a + 1, b - 1)
        wrong = [a - r.randint(1, 900), b + r.randint(1, 900), int(str(t)[:-1]) if t >= 10000 and int(str(t)[:-1]) > 999 else t * 10, a + 10000]
        return mcq("Which number is between %s and %s?" % (comma(a), comma(b)), t, wrong,
                   "<b>%s</b> is greater than %s and less than %s." % (comma(t), comma(a), comma(b)))
    if kind == "digit":
        n = r.randint(10000, 99999)
        s = str(n)
        i = r.randrange(1, 4)
        d = int(s[i])
        if d in (0, 9):
            return None
        shown = s[:i] + "☐" + s[i + 1:]
        shown = shown[:-3] + "," + shown[-3:] if i != len(s) - 3 else shown[:-3] + "," + shown[-3:]
        right = r.choice([x for x in range(d + 1, 10)])
        wrong = [x for x in range(0, d + 1)]
        r.shuffle(wrong)
        return mcq("Which digit makes this true? %s &gt; %s" % (shown, comma(n)), str(right), [str(w) for w in wrong],
                   "The other digits are the same, so the box must be greater than %d. <b>%d</b> works." % (d, right), allow_zero=True)
    n, m, i = near_pair(r)
    sym = "&gt;" if n > m else "&lt;"
    return mcq("Which symbol makes this true? %s ☐ %s" % (comma(n), comma(m)), sym, ["&lt;" if sym == "&gt;" else "&gt;", "=", "+"],
               "Compare from the left. %s is %s %s, so use <b>%s</b>." % (comma(n), "greater than" if sym == "&gt;" else "less than", comma(m), sym))


# ------------------------------------------------------------ set 5: word problems
def one_story(r):
    K = Kid(r)
    k = K.next()
    kind = r.choice(["stadium", "stadium", "town", "steps", "steps", "books", "books", "fans"])
    if kind == "town":
        a, b = r.sample(PLACES[4:], 2)
        x, y, _ = near_pair(r)
        q = "A town near %s has %s people. A town near %s has %s people. Which town has more people?" % (a, comma(x), b, comma(y))
        win = "The town near %s" % (a if x > y else b)
        return mcq(q, win, ["The town near %s" % (b if x > y else a), "They have the same number", "We cannot tell"],
                   "%s %s %s, so <b>%s</b> has more." % (comma(max(x, y)), "&gt;", comma(min(x, y)), "t" + win[1:]))
    if kind == "stadium":
        names = ["Stadium A", "Stadium B", "Stadium C", "Stadium D"]
        vals = r.sample(range(40000, 99999), 4)
        vals[1] = int(str(vals[0])[:2] + str(vals[1])[2:])
        if len(set(vals)) < 4:
            return None
        t = max(vals)
        q = "Four football stadiums hold %s." % ", ".join("%s: %s seats" % (n, comma(v)) for n, v in zip(names, vals)) + " Which stadium holds the most people?"
        return mcq(q, names[vals.index(t)], [n for n in names if n != names[vals.index(t)]],
                   "Compare from the left: %s is the greatest. <b>%s</b>." % (comma(t), names[vals.index(t)]))
    if kind == "steps":
        x, y, _ = near_pair(r)
        if x == y:
            return None
        q = "%s walked %s steps in March and %s steps in April. Which comparison is true?" % (k["n"], comma(x), comma(y))
        right = "March %s April" % ("&gt;" if x > y else "&lt;")
        wrong = ["March %s April" % ("&lt;" if x > y else "&gt;"), "March = April", "April %s March" % ("&gt;" if x > y else "&lt;")]
        return mcq(q, right, wrong, "%s %s %s, so <b>%s</b>." % (comma(x), "&gt;" if x > y else "&lt;", comma(y), right))
    if kind == "books":
        vals = sorted(r.sample(range(12000, 30000), 3))
        libs = ["North Library", "Central Library", "South Library"]
        r.shuffle(libs)
        show = [0, 1, 2]
        while show == [0, 1, 2]:
            r.shuffle(show)
        q = " ".join("%s has %s books." % (libs[i], comma(vals[i])) for i in show) + " Order the libraries from least books to greatest."
        right = "; ".join(libs)
        wrong = ["; ".join(libs[::-1]), "; ".join([libs[1], libs[0], libs[2]]), "; ".join([libs[0], libs[2], libs[1]])]
        return mcq(q, right, wrong, "%s &lt; %s &lt; %s: <b>%s</b>." % (comma(vals[0]), comma(vals[1]), comma(vals[2]), right))
    x = r.randint(20000, 60000)
    y = x + r.choice([-1, 1]) * r.choice([10, 100, 1000])
    q = "On Friday %s fans came to the game. On Saturday %s fans came. On which day did more fans come?" % (comma(x), comma(y))
    day = "Friday" if x > y else "Saturday"
    return mcq(q, day, ["Saturday" if day == "Friday" else "Friday", "The same on both days", "We cannot tell"],
               "%s %s %s: <b>%s</b>." % (comma(max(x, y)), "&gt;", comma(min(x, y)), day))


def build():
    sets = [S("Which comparison is true?", collect(one_true, 20, R)),
            S("Greatest and least", collect(one_most, 20, R)),
            S("Put numbers in order", collect(one_order, 20, R)),
            S("Symbols, missing digits and numbers between", collect(one_between, 20, R)),
            S("Word problems", collect(one_story, 20, R))]
    finish(sets, R)
    body = lesson(
        "<ul><li>A number with more digits is greater: 10,000 &gt; 9,999.</li>"
        "<li>If the numbers have the same number of digits, compare from the <b>left</b>. The first place where the digits differ decides.</li>"
        "<li>&gt; means <b>is greater than</b>. &lt; means <b>is less than</b>. The open side faces the greater number.</li>"
        "<li>To order, find the least, then the next, and so on.</li></ul>",
        [figure(pv_chart_svg(45206), "45,206"), figure(pv_chart_svg(45026), "45,026: same ten thousands and thousands, but 2 hundreds &gt; 0 hundreds, so 45,206 &gt; 45,026."),
         example("Order 38,915; 38,519; 9,999 from least to greatest.", ["9,999 has 4 digits, so it is least.", "38,915 and 38,519: the hundreds are 9 and 5.", "5 &lt; 9, so 38,519 comes next."], "9,999; 38,519; 38,915")],
        [["Comparing the ones digits first", "Start at the left, with the greatest place."],
         ["Thinking the number with more 9s is greater", "Look at the first place where the digits differ, not how many 9s there are."],
         ["Reading &gt; and &lt; backward", "The open mouth faces the greater number."]])
    faq = [("What does TEKS 3.2D ask?", "Compare and order whole numbers up to 100,000 and show the comparison with &gt;, &lt; or =."),
           ("How do you compare two 5-digit numbers?", "Line them up by place value and compare from the ten thousands place. The first place with different digits tells which number is greater."),
           ("How can I remember &gt; and &lt;?", "The symbol opens toward the greater number: 52,000 &gt; 25,000."),
           ("What if the numbers have a different number of digits?", "The number with more digits is greater. Any 5-digit number is greater than any 4-digit number.")]
    make("comparing-and-ordering-numbers", 2, "Number and Operations", "3.2D",
         "3.2D compare and order whole numbers up to 100,000 and represent comparisons using the symbols >, <, or =",
         "Comparing and Ordering Numbers to 100,000", "Comparing and Ordering Numbers",
         "Free Grade 3 worksheets for Texas TEKS 3.2D: compare numbers to 100,000 with &gt;, &lt; and =, find the greatest and least, order numbers, missing digits and word problems. 100 STAAR-style questions with answers.",
         "Compare from the left. The first place where the digits differ decides.", "&gt; means greater than and &lt; means less than. The open side faces the greater number.",
         body, faq, sets, seo_title="Grade 3 Comparing and Ordering Numbers to 100,000 Worksheets (TEKS 3.2D, STAAR)")


if __name__ == "__main__":
    build()
