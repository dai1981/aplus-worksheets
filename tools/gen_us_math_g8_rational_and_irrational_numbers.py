# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Rational and Irrational Numbers (8.NS.A.1, 8.NS.A.2)
  python3 tools/gen_us_math_g8_rational_and_irrational_numbers.py
Tell rational from irrational numbers, write fractions as decimals, change repeating decimals to
fractions, estimate irrational numbers (√2, π) and place them on a number line, and order real numbers.
Wrong answers come from real mistakes: calling every root irrational, calling every long decimal
irrational, writing 0.3 repeating as 3/10, and treating π as exactly 3.14.
"""
import math, random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fig, fr, MINUS, svg_wrap, text, line, INK, RED

R = random.Random(80901)
UPDATED = "2026-11-16"
RAT, IRR = "Rational", "Irrational"


def rt(n):
    return "√<span style='text-decoration:overline'>%s</span>" % n


def bar(s):
    return "<span style='text-decoration:overline'>%s</span>" % s


def v(x):
    x = F(x)
    if x.denominator == 1:
        return num(x)
    return (MINUS if x < 0 else "") + fr(abs(x.numerator), x.denominator)


# ============================================================ set 1: classify
def set_classify():
    its = []
    for shown, ok, why in [
        (rt(2), False, "2 is not a perfect square, so √2 never ends and never repeats."),
        (rt(16), True, "√16 = 4, a whole number."),
        ("π", False, "π = 3.14159… never ends and never repeats."),
        (fr(3, 7), True, "It is a fraction of two integers."),
        ("0.75", True, "0.75 = 3/4."),
        ("0.%s" % bar("3"), True, "A repeating decimal can be written as a fraction: 1/3."),
        (rt(10), False, "10 is not a perfect square."),
        (MINUS + "8", True, "−8 = −8/1."),
        (rt(49), True, "√49 = 7."),
        ("0.1010010001…", False, "The pattern grows, so the digits never repeat in a block."),
        (rt(fr(1, 4)), True, "√(1/4) = 1/2."),
        ("2π", False, "Twice an irrational number is still irrational."),
        ("1.%s" % bar("27"), True, "It repeats the block 27, so it is a fraction."),
        (rt(50), False, "50 is not a perfect square."),
        ("0", True, "0 = 0/1."),
        (rt(3) + " + 1", False, "√3 is irrational, so √3 + 1 is too."),
        ("3.14", True, "3.14 = 314/100. (π is not 3.14; 3.14 is only close to π.)"),
        (rt(100) + " ÷ 2", True, "√100 ÷ 2 = 10 ÷ 2 = 5."),
        (rt(8), False, "8 is not a perfect square."),
        ("<sup>3</sup>√<span style='text-decoration:overline'>27</span>", True, "∛27 = 3."),
    ]:
        ans = RAT if ok else IRR
        its.append(mcq("Is %s rational or irrational?" % B(shown), (ans, ans),
                       [(c, c) for c in [RAT, IRR, "Both", "Neither: it is not a real number"] if c != ans],
                       why + " <b>%s</b>." % ans))
    return {"title": "Rational or irrational?", "items": its}


# ============================================================ set 2: fractions to decimals
def set_to_dec():
    its = []
    for (a, b), dec, wr, kind in [
        ((1, 4), "0.25", ["0.4", "1.4", "0.14"], "ends"), ((2, 3), "0.%s" % bar("6"), ["0.6", "0.23", "1.5"], "repeats"),
        ((5, 8), "0.625", ["0.58", "1.6", "0.85"], "ends"), ((1, 6), "0.1%s" % bar("6"), ["0.16", "0.%s" % bar("16"), "6.0"], "repeats"),
        ((7, 9), "0.%s" % bar("7"), ["0.79", "0.7", "1.29"], "repeats"), ((3, 11), "0.%s" % bar("27"), ["0.311", "0.3", "0.%s" % bar("3")], "repeats"),
        ((9, 20), "0.45", ["0.92", "2.2", "0.9"], "ends"), ((4, 15), "0.2%s" % bar("6"), ["0.415", "0.26", "0.%s" % bar("26")], "repeats"),
        ((7, 12), "0.58%s" % bar("3"), ["0.712", "0.58", "1.71"], "repeats"), ((13, 25), "0.52", ["0.1325", "1.92", "0.25"], "ends"),
    ]:
        q = "Write %s as a decimal." % B(fr(a, b))
        e = "Divide %d ÷ %d = %s. It %s. The answer is <b>%s</b>." % (a, b, dec, "ends" if kind == "ends" else "repeats (shown by the bar)", dec)
        its.append(mcq(q, (dec, dec), [(w, w) for w in wr], e))
    for q, ans, wr, e in [
        ("Which fraction gives a repeating decimal?", fr(1, 3), [fr(1, 4), fr(3, 8), fr(7, 10)],
         "1/4, 3/8 and 7/10 end. 1/3 = 0.333… repeats. The answer is <b>%s</b>." % fr(1, 3)),
        ("Which fraction gives a decimal that ends?", fr(3, 16), [fr(2, 9), fr(5, 6), fr(4, 7)],
         "16 = 2 × 2 × 2 × 2, so 3/16 = 0.1875 ends. The answer is <b>%s</b>." % fr(3, 16)),
        ("Every fraction of two integers, written as a decimal, …", "either ends or repeats", ["always ends", "never repeats", "is irrational"],
         "Rational numbers <b>either end or repeat</b>."),
        ("A decimal goes on forever and never repeats. What is it?", "Irrational", ["Rational", "A whole number", "A fraction"],
         "Never ending and never repeating means <b>irrational</b>."),
        ("What is %s as a decimal?" % fr(1, 9), "0.%s" % bar("1"), ["0.9", "0.19", "1.9"], "1 ÷ 9 = 0.111… = <b>0.%s</b>." % bar("1")),
        ("What is %s as a decimal?" % fr(5, 11), "0.%s" % bar("45"), ["0.511", "0.5", "0.%s" % bar("5")], "5 ÷ 11 = 0.4545… = <b>0.%s</b>." % bar("45")),
        ("What is %s as a decimal?" % fr(3, 5), "0.6", ["0.35", "1.67", "0.%s" % bar("6")], "3 ÷ 5 = <b>0.6</b>."),
        ("What is %s as a decimal?" % fr(5, 6), "0.8%s" % bar("3"), ["0.56", "0.%s" % bar("83"), "1.2"], "5 ÷ 6 = 0.8333… = <b>0.8%s</b>." % bar("3")),
        ("Which is the same as 0.%s?" % bar("3"), fr(1, 3), [fr(3, 10), fr(33, 100), fr(3, 1)], "0.333… = <b>%s</b>, not 3/10 (that is 0.3)." % fr(1, 3)),
        ("Which is the same as 0.%s?" % bar("9"), "1", [fr(9, 10), fr(99, 100), "0.9"], "0.999… = 3 × 0.333… = 3 × 1/3 = <b>1</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[12], o[1], o[13], o[2], o[16], o[3], o[10], o[4], o[14], o[5], o[11], o[6], o[17], o[7], o[18], o[8],
             o[15], o[9], o[19]]
    return {"title": "Fractions as decimals", "items": order}


# ============================================================ set 3: repeating decimals to fractions
def set_to_frac():
    its = []
    for digits, pre, ans, wr in [
        ("4", "", F(4, 9), [F(4, 10), F(4, 99), F(9, 4)]), ("7", "", F(7, 9), [F(7, 10), F(7, 99), F(77, 100)]),
        ("2", "", F(2, 9), [F(1, 5), F(2, 99), F(22, 100)]), ("5", "", F(5, 9), [F(1, 2), F(5, 99), F(55, 100)]),
        ("36", "", F(4, 11), [F(9, 25), F(4, 1), F(6, 11)]), ("18", "", F(2, 11), [F(9, 50), F(2, 1), F(1, 9)]),
        ("45", "", F(5, 11), [F(9, 20), F(5, 9), F(5, 1)]), ("12", "", F(4, 33), [F(3, 25), F(4, 3), F(1, 3)]),
        ("81", "", F(9, 11), [F(81, 100), F(9, 10), F(81, 9)]), ("6", "1", F(1, 6), [F(16, 100), F(16, 99), F(6, 9)]),
        ("3", "8", F(5, 6), [F(83, 100), F(83, 99), F(8, 9)]), ("27", "", F(3, 11), [F(27, 100), F(3, 10), F(27, 9)]),
        ("1", "", F(1, 9), [F(1, 10), F(1, 99), F(11, 100)]), ("09", "", F(1, 11), [F(9, 100), F(1, 9), F(9, 10)]),
        ("6", "", F(2, 3), [F(3, 5), F(33, 50), F(2, 33)]), ("3", "1", F(2, 15), [F(13, 100), F(13, 99), F(1, 3)]),
    ]:
        shown = "0.%s%s" % (pre, bar(digits))
        q = "Write %s as a fraction in simplest form." % B(shown)
        if pre:
            e = ("Let x = %s. Multiply by 10: 10x = %s.%s. Multiply by 100: 100x = %s%s.%s. Subtract: 90x = %s, so x = %s = <b>%s</b>."
                 % (shown, pre, bar(digits), pre, digits, bar(digits), int(pre + digits) - int(pre), fr(int(pre + digits) - int(pre), 90), v(ans)))
        else:
            k = len(digits)
            p = 10 ** k
            raw = fr(int(digits), p - 1)
            e = ("Let x = %s. Multiply by %d: %dx = %s.%s. Subtract: %dx = %s, so x = %s<b>%s</b>."
                 % (shown, p, p, str(int(digits)), bar(digits), p - 1, int(digits), (raw + " = ") if F(int(digits), p - 1) != F(int(digits)) / (p - 1) or raw != v(ans) else "", v(ans)))
        its.append(mcq(q, (v(ans), ans), [(v(w), w) for w in wr], e))
    for q, ans, wr, e in [
        ("Why do we multiply x = 0.%s by 10?" % bar("4"), "So the repeating parts line up and subtract away",
         ["To make it a whole number", "Because 4 is less than 10", "To make it irrational"],
         "10x = 4.444… and x = 0.444… have the same digits after the point: <b>so the repeating parts line up and subtract away</b>."),
        ("To change 0.%s to a fraction, which number do you multiply x by?" % bar("72"), "100", ["10", "72", "1,000"],
         "Two digits repeat, so multiply by <b>100</b>."),
        ("Is 0.%s rational?" % bar("142857"), "Yes, it is 1/7", ["No, it is too long", "No, it never ends", "Only if rounded"],
         "Every repeating decimal is rational. 0.142857142857… = <b>1/7</b>."),
        ("Which number is 0.%s?" % bar("3") + " + 0.%s" % bar("6"), "1", ["0.9", fr(9, 10), "0.%s" % bar("96")],
         "1/3 + 2/3 = <b>1</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[16], o[2], o[3], o[12], o[17], o[14], o[4], o[5], o[18], o[6], o[7], o[13], o[8], o[11], o[9],
             o[10], o[15], o[19]]
    return {"title": "Repeating decimals to fractions", "items": order}


# ============================================================ set 4: estimate and number line
def nline(lo, hi, mark, label):
    m, u = 24, 70
    W = (hi - lo) * u + 2 * m
    s = [line(m - 8, 30, W - m + 8, 30, INK, 2)]
    for k in range((hi - lo) * 10 + 1):
        x = m + k * u / 10
        big = k % 10 == 0
        s.append(line(x, 30 - (8 if big else 4), x, 30 + (8 if big else 4), INK, 1.6 if big else 1))
        if big:
            s.append(text(x, 54, str(lo + k // 10), 14))
    xm = m + (mark - lo) * u
    s.append("<circle cx='%.1f' cy='30' r='5' fill='%s'/>" % (xm, RED))
    s.append(text(xm, 16, label, 13, col=RED))
    return svg_wrap(int(W), 62, "".join(s), "number line")


def set_estimate():
    its = []
    for n, lo, hi in [(2, 1, 2), (3, 1, 2), (5, 2, 3), (7, 2, 3), (11, 3, 4), (20, 4, 5), (30, 5, 6), (45, 6, 7), (60, 7, 8), (90, 9, 10)]:
        r = math.sqrt(n)
        tenth = round(r, 1)
        q = "To the nearest tenth, what is %s?" % B(rt(n))
        e = ("%d² = %d and %d² = %d, so %s is between %d and %d. Try tenths: %.1f² = %.2f and %.1f² = %.2f. So %s ≈ <b>%.1f</b>."
             % (lo, lo * lo, hi, hi * hi, rt(n), lo, hi, tenth, tenth * tenth, tenth + 0.1 if tenth * tenth < n else tenth - 0.1,
                (tenth + 0.1) ** 2 if tenth * tenth < n else (tenth - 0.1) ** 2, rt(n), tenth))
        wr = ["%.1f" % (n / 2), "%.1f" % (tenth + 0.2), "%.1f" % (tenth - 0.2), "%.1f" % (lo + (n - lo * lo) / 10)]
        its.append(mcq(q, ("%.1f" % tenth, tenth), [(w, w) for w in wr if w != "%.1f" % tenth], e))
    for n, lo, hi in [(2, 1, 2), (8, 2, 3), (15, 3, 4), (27, 5, 6), (40, 6, 7)]:
        r = math.sqrt(n)
        svg = nline(lo, hi, round(r, 1), "?")
        q = fig(svg) + "Which number is closest to the point?"
        ans = rt(n)
        cands = [rt(lo * lo), rt(hi * hi), rt(n + 2 * hi + 1)]
        e = "%s ≈ %.1f, which is where the point is. The answer is <b>%s</b>." % (rt(n), r, ans)
        its.append(mcq(q, (ans, ans), [(c, c) for c in cands], e))
    for q, ans, wr, e in [
        ("Which is the best estimate of π?", "3.14", ["3", "3.41", "22"], "π = 3.14159…, so <b>3.14</b> is the best estimate here."),
        ("About what is 2π?", "6.28", ["5.14", "6.14", "9.86"], "2 × 3.14 = <b>6.28</b>."),
        ("Between which two whole numbers is π²?", "9 and 10", ["6 and 7", "3 and 4", "12 and 13"], "π ≈ 3.14 and 3.14² ≈ 9.86: <b>9 and 10</b>."),
        ("Which is closer to √10: 3 or 4?", "3", ["4", "They are the same distance", "We cannot tell"],
         "√10 ≈ 3.16, which is closer to <b>3</b>."),
        ("Which is the best estimate of √2?", "1.41", ["1.2", "2", "1.14"], "1.41² = 1.9881, very close to 2: <b>1.41</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[15], o[10], o[1], o[16], o[2], o[11], o[17], o[3], o[19], o[12], o[4], o[18], o[5], o[13], o[6], o[7],
             o[14], o[8], o[9]]
    return {"title": "Estimate irrational numbers", "items": order}


# ============================================================ set 5: order
def set_order():
    its = []
    for items, ask in [
        ([("3", 3), (rt(8), math.sqrt(8)), ("π", math.pi), ("2.9", 2.9)], "least"),
        ([(rt(50), math.sqrt(50)), ("7.2", 7.2), (fr(15, 2), 7.5), ("7", 7)], "greatest"),
        ([(rt(3), math.sqrt(3)), ("1.7", 1.7), (fr(9, 5), 1.8), ("1.%s" % bar("6"), 5 / 3)], "greatest"),
        ([("π", math.pi), ("3.1", 3.1), (rt(10), math.sqrt(10)), (fr(22, 7), 22 / 7)], "greatest"),
        ([(MINUS + rt(5), -math.sqrt(5)), (MINUS + "2", -2), (MINUS + "2.3", -2.3), (MINUS + fr(9, 4), -2.25)], "least"),
        ([(rt(20), math.sqrt(20)), ("4.4", 4.4), (fr(9, 2), 4.5), ("4.%s" % bar("3"), 13 / 3)], "least"),
        ([("0.%s" % bar("5"), 5 / 9), ("0.5", 0.5), (fr(4, 7), 4 / 7), (rt("0.25"), 0.5000001)], "greatest"),
        ([(rt(2), math.sqrt(2)), ("1.4", 1.4), (fr(3, 2), 1.5), ("1.%s" % bar("4"), 13 / 9)], "greatest"),
    ]:
        vals = [x for _, x in items]
        idx = vals.index(max(vals) if ask == "greatest" else min(vals))
        ans = items[idx][0]
        e = "Write each as a decimal: %s. The %s is <b>%s</b>." % (
            ", ".join("%s ≈ %.3f" % (s, x) for s, x in items).replace("-", MINUS), ask, ans)
        its.append(mcq("Which number is the <b>%s</b>?" % ask, (ans, ans), [(s, s) for i, (s, _) in enumerate(items) if i != idx], e))
    for q, ans, wr, e in [
        ("Which list is in order from least to greatest?", "%s, 1.5, %s" % (rt(2), rt(3)), ["1.5, %s, %s" % (rt(2), rt(3)),
         "%s, %s, 1.5" % (rt(3), rt(2)), "%s, %s, 1.5" % (rt(2), rt(3))], "√2 ≈ 1.41, 1.5, √3 ≈ 1.73. The order is <b>√2, 1.5, √3</b>."),
        ("Which list is in order from least to greatest?", "3, π, %s" % rt(10), ["π, 3, %s" % rt(10), "3, %s, π" % rt(10),
         "%s, π, 3" % rt(10)], "3, π ≈ 3.14, √10 ≈ 3.16. The order is <b>3, π, √10</b>."),
        ("Which is true?", "%s &lt; 2.5 &lt; %s" % (rt(5), rt(7)), ["%s &lt; 2.5 &lt; %s" % (rt(7), rt(5)), "2.5 &lt; %s &lt; %s" % (rt(5), rt(7)),
         "%s &lt; %s &lt; 2.5" % (rt(5), rt(7))], "√5 ≈ 2.24 and √7 ≈ 2.65, so <b>√5 &lt; 2.5 &lt; √7</b>."),
        ("Which number is between 6 and 7?", rt(40), [rt(30), rt(50), rt(70)], "6² = 36 and 7² = 49. Only 40 is between: <b>√40</b>."),
        ("Which number is between 4 and 5?", rt(22), [rt(15), rt(26), rt(30)], "4² = 16 and 5² = 25. Only 22 is between: <b>√22</b>."),
        ("How many whole numbers are between √10 and √50?", "4", ["40", "3", "5"], "√10 ≈ 3.2 and √50 ≈ 7.1. The whole numbers 4, 5, 6, 7: <b>4</b>."),
        ("Which is an irrational number between 3 and 4?", rt(12), [rt(9), "3.5", fr(7, 2)], "√12 ≈ 3.46 and 12 is not a perfect square: <b>√12</b>."),
        ("Which is a rational number between √2 and √3?", "1.5", [rt(2.5).replace("2.5", "2.5"), "π ÷ 2", "1.%s" % bar("9")],
         "1.5 = 3/2 is rational, and 1.41 &lt; 1.5 &lt; 1.73. <b>1.5</b>."),
        ("Ana says √25 is irrational because it has a root sign. Is she right?", "No, √25 = 5", ["Yes, all roots are irrational", "Yes, it never ends", "No, it is 12.5"],
         "√25 = 5, a whole number, so it is rational. <b>No, √25 = 5</b>."),
        ("Ben says 0.%s is irrational because it never ends. Is he right?" % bar("2"), "No, it repeats, so it is 2/9",
         ["Yes, never-ending decimals are irrational", "Yes, it cannot be a fraction", "No, it is 2/10"],
         "It repeats, so it is rational: <b>0.222… = 2/9</b>."),
        ("Which set contains only irrational numbers?", "√2, π, √11", ["√4, π, √11", "√2, 0.%s, π" % bar("3"), "1.5, √7, π"],
         "√4 = 2 and 0.333… and 1.5 are rational. <b>√2, π, √11</b> are all irrational."),
        ("Which set contains only rational numbers?", "−4, 0.%s, √36" % bar("6"), ["−4, √6, 0.5", "π, 3, 1/2", "√9, √10, 2"],
         "−4, 0.666… = 2/3 and √36 = 6 are all rational: <b>−4, 0.%s, √36</b>." % bar("6")),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[11], o[1], o[12], o[2], o[8], o[3], o[16], o[4], o[17], o[9], o[5], o[13], o[10], o[6], o[18], o[14],
             o[19], o[7], o[15]]
    assert len({id(i) for i in order}) == 20
    return {"title": "Compare and order real numbers", "items": order}


def body():
    return ("<h2>Rational and irrational numbers</h2>"
            "<p>A <b>rational</b> number can be written as a fraction of two integers. As a decimal, it <b>ends</b> or <b>repeats</b>. "
            "An <b>irrational</b> number cannot: its decimal never ends and never repeats.</p>"
            + table(["Rational", "Irrational"], [["5, −3, 0", "√2, √3, √5"], ["3/4 = 0.75", "π = 3.14159…"],
                                                ["1/3 = 0.333…", "0.1010010001…"], ["√16 = 4", "√10"]])
            + example("Write 0.%s as a fraction." % bar("4"), ["Let x = 0.444….", "10x = 4.444….", "Subtract: 9x = 4, so x = 4/9."], "4/9")
            + example("Estimate √20.", ["4² = 16 and 5² = 25, so √20 is between 4 and 5.", "4.5² = 20.25, so √20 is a bit less than 4.5."], "about 4.47")
            + "<h2>Common mistakes</h2><ul><li>Calling every root irrational: √25 = 5 is rational.</li>"
            "<li>Calling every long decimal irrational: 0.333… repeats, so it is rational.</li>"
            "<li>Writing 0.333… as 3/10. It is 1/3.</li>"
            "<li>Thinking π = 3.14 exactly. 3.14 is only an estimate.</li></ul>")


def main():
    sets = [set_classify(), set_to_dec(), set_to_frac(), set_estimate(), set_order()]
    balance(sets, R)
    unit = {
        "slug": "rational-and-irrational-numbers",
        "title": "Rational and Irrational Numbers",
        "seo_title": "Grade 8 Rational and Irrational Numbers Worksheets: Repeating Decimals, Estimating √2 and π",
        "short_title": "Rational and irrational",
        "domain": "The Number System",
        "standard_code": "8.NS.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/NS/A/1/",
        "standard_text": "Know that numbers that are not rational are called irrational. Understand informally that every number has a decimal expansion; for rational numbers show that the decimal expansion repeats eventually, and convert a decimal expansion which repeats eventually into a rational number.",
        "meta_desc": "Free Grade 8 rational and irrational numbers worksheets: classify numbers, write fractions as decimals, change repeating decimals to fractions, estimate √2 and π, place them on a number line, and order real numbers. 100 questions with an answer key.",
        "key_big": "Rational numbers end or repeat as decimals. Irrational numbers never end and never repeat.",
        "key_sub": "√2, √3 and π are irrational. √16 = 4 and 0.333… = 1/3 are rational.",
        "body_html": body(),
        "faq": [
            {"q": "What is the difference between rational and irrational numbers?", "a": "A rational number can be written as a fraction of integers, and its decimal ends or repeats. An irrational number cannot; its decimal never ends and never repeats, like √2 or π."},
            {"q": "Is a repeating decimal rational?", "a": "Yes. Every repeating decimal can be written as a fraction. For example, 0.444… = 4/9."},
            {"q": "Is every square root irrational?", "a": "No. The square root of a perfect square is rational: √49 = 7. √2 and √10 are irrational."},
            {"q": "How do you change a repeating decimal to a fraction?", "a": "Let x be the decimal. Multiply by 10 (or 100 for two repeating digits) and subtract to remove the repeating part. 0.444…: 10x − x = 4, so x = 4/9."}],
        "sets": sets, "pdf_url": "", "sort": 9, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
