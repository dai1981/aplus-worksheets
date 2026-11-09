# -*- coding: utf-8 -*-
"""
US Grade 7 Math: Converting Fractions to Decimals (7.NS.A.2d)
  python tools/gen_us_math_g7_converting_fractions_to_decimals.py
Long division turns a fraction into a decimal that ends (terminates) or repeats.
Wrong answers come from real mistakes: dividing the denominator by the numerator (3/8 -> 2.6),
writing the digits side by side (3/8 -> 0.38), putting the bar over the wrong digits
(1/6 = 0.1666… written 0.16 with the bar over both), and losing the negative sign.
"""
import random
from fractions import Fraction as F
from ws_common import (num, mcq, balance, People, B, table, example, write_unit, fr, MINUS)

R = random.Random(71301)
UPDATED = "2026-11-09"


def expand(v):
    """(sign, whole, non-repeating digits, repeating digits) of a fraction."""
    v = F(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    w, r = divmod(v.numerator, v.denominator)
    d = v.denominator
    digits, seen = [], {}
    while r and r not in seen:
        seen[r] = len(digits)
        r *= 10
        digits.append(str(r // d))
        r %= d
    if not r:
        return sign, w, "".join(digits), ""
    k = seen[r]
    return sign, w, "".join(digits[:k]), "".join(digits[k:])


def dhtml(v):
    """Decimal with a bar over the repeating digits."""
    sign, w, nr, rep = expand(v)
    s = (MINUS if sign else "") + "{:,}".format(w)
    if nr or rep:
        s += "." + nr
        if rep:
            s += "<span class='ov'>%s</span>" % rep
    return s


def dplain(v):
    sign, w, nr, rep = expand(v)
    s = (MINUS if sign else "") + str(w)
    if nr or rep:
        s += "." + nr + ((rep * 3)[:6] + "…") if rep else "." + nr
    return s


def fx(v):
    v = F(v)
    sgn = MINUS if v < 0 else ""
    w, r = divmod(abs(v.numerator), v.denominator)
    if r == 0:
        return sgn + str(w)
    return sgn + ((str(w) + " ") if w else "") + fr(r, v.denominator)


def side_by_side(v):
    """3/8 -> 0.38 (a common mistake), as a value."""
    v = abs(F(v))
    return F("0." + str(v.numerator) + str(v.denominator)) if v < 1 else None


def opts(v, ws):
    out = []
    for w in ws:
        if w is None:
            continue
        if isinstance(w, tuple):
            out.append(w)
        else:
            w = F(w)
            out.append((dhtml(w), w))
    return out


def to_dec_item(v, note=""):
    v = F(v)
    a = abs(v)
    flip = F(a.denominator, a.numerator) if a.numerator else None
    ws = [flip * (-1 if v < 0 else 1) if flip else None, side_by_side(v) * (-1 if v < 0 else 1) if side_by_side(v) else None, -v,
          v + F(1, 10), v - F(1, 100)]
    e = "Divide the numerator by the denominator: %d ÷ %d = %s." % (abs(v.numerator), v.denominator, dhtml(a))
    if v < 0:
        e += " Keep the negative sign: %s." % dhtml(v)
    if flip and flip != a:
        e += " Not %s: that divides %d by %d." % (dhtml(flip), a.denominator, a.numerator)
    return mcq("Write %s as a decimal.%s" % (B(fx(v)), note), (dhtml(v), v), opts(v, ws), e)


# ------------------------------------------------------------ set 1
def set_terminating():
    its = []
    for v in [F(1, 2), F(3, 4), F(2, 5), F(7, 10), F(3, 8), F(1, 4), F(4, 5), F(9, 20), F(7, 8), F(13, 25), F(1, 8), F(3, 50),
              F(5, 16), F(17, 20), F(11, 40)]:
        its.append(to_dec_item(v))
    its.append(mcq("Which fraction is the same as 0.6?", (fx(F(3, 5)), "a"), [(fx(F(1, 6)), "b"), (fr(6, 100), "c"), (fx(F(5, 3)), "d")],
                   "0.6 = 6/10 = 3/5. Not 1/6: 1 ÷ 6 = 0.1666…"))
    its.append(mcq("Which fraction equals 0.125?", (fx(F(1, 8)), "a"), [(fx(F(1, 25)), "b"), (fx(F(5, 4)), "c"), (fx(F(12, 5)), "d")],
                   "0.125 = 125/1000 = 1/8."))
    its.append(mcq("How do you change a fraction to a decimal?", ("Divide the numerator by the denominator.", "a"),
                   [("Divide the denominator by the numerator.", "b"), ("Write the numerator, a point, then the denominator.", "c"), ("Multiply the numerator by 10.", "d")],
                   "A fraction is a division: 3/8 means 3 ÷ 8 = 0.375."))
    its.append(mcq("Which is the first step to write %s as a decimal?" % B(fx(F(3, 4))), ("Find 3 ÷ 4", "a"), [("Find 4 ÷ 3", "b"), ("Find 3 × 4", "c"), ("Find 4 − 3", "d")],
                   "Numerator ÷ denominator: 3 ÷ 4 = 0.75."))
    its.append(mcq("A fraction in simplest form has a denominator of 20. What kind of decimal is it?", ("A terminating decimal", "a"),
                   [("A repeating decimal", "b"), ("A whole number", "c"), ("It cannot be written as a decimal", "d")],
                   "20 = 2 × 2 × 5. If the denominator has no prime factors other than 2 and 5, the decimal ends."))
    return {"title": "Terminating decimals", "items": its}


# ------------------------------------------------------------ set 2
def set_repeating():
    its = []
    for v in [F(1, 3), F(2, 3), F(1, 6), F(5, 6), F(1, 9), F(4, 9), F(2, 11), F(5, 12), F(7, 15), F(1, 7)]:
        its.append(to_dec_item(v))
    kinds = [(F(5, 8), True), (F(2, 7), False), (F(7, 20), True), (F(4, 15), False), (F(9, 40), True), (F(5, 18), False)]
    for v, term in kinds:
        good = "Terminating" if term else "Repeating"
        d = v.denominator
        fac = []
        x = d
        for p in [2, 3, 5, 7, 11, 13]:
            while x % p == 0:
                fac.append(str(p)); x //= p
        its.append(mcq("Is %s a terminating or a repeating decimal?" % B(fx(v)), (good, good), [("Repeating" if term else "Terminating", "x"),
                       ("Neither: it is a whole number", "w"), ("It depends on the numerator only", "n")],
                       "%s = %s. The denominator %d = %s %s." % (fx(v), dhtml(v), d, " × ".join(fac),
                                                                 "has only 2s and 5s, so it terminates" if term else "has a factor other than 2 and 5, so it repeats")))
    its.append(mcq("Which shows 0.272727… with bar notation?", ("0.<span class='ov'>27</span>", "a"),
                   [("0.2<span class='ov'>7</span>", "b"), ("0.<span class='ov'>2</span>7", "c"), ("0.27", "d")],
                   "The block 27 repeats, so the bar goes over both digits."))
    its.append(mcq("Which shows 0.1666… with bar notation?", ("0.1<span class='ov'>6</span>", "a"),
                   [("0.<span class='ov'>16</span>", "b"), ("0.<span class='ov'>1</span>6", "c"), ("0.16", "d")],
                   "Only the 6 repeats. 0.<span class='ov'>16</span> would mean 0.161616…"))
    its.append(mcq("What does 0.<span class='ov'>3</span> mean?", ("0.333… (the 3 repeats forever)", "a"),
                   [("0.3 exactly", "b"), ("0.03", "c"), ("3 ÷ 10", "d")], "The bar means the digits under it repeat forever. 0.<span class='ov'>3</span> = 1/3."))
    its.append(mcq("Which fraction equals 0.<span class='ov'>6</span>?", (fx(F(2, 3)), "a"), [(fx(F(3, 5)), "b"), (fr(6, 10), "c"), (fx(F(1, 6)), "d")],
                   "2 ÷ 3 = 0.666… = 0.<span class='ov'>6</span>. 3/5 and 6/10 are 0.6 exactly."))
    return {"title": "Repeating decimals and bar notation", "items": its}


# ------------------------------------------------------------ set 3
def set_mixed_negative():
    its = []
    for v in [F(-3, 4), F(-5, 8), F(-2, 3), F(-7, 20), F(-1, 6)]:
        its.append(to_dec_item(v))
    for v in [F(11, 4), F(19, 8), F(-21, 5), F(10, 3), F(-49, 6), F(53, 16)]:
        w = abs(v.numerator) // v.denominator
        part = abs(v) - w
        e = "Write the whole number, then change the fraction: %s = %s, so %s = %s." % (fx(part), dhtml(part), fx(v), dhtml(v))
        ws = [w + side_by_side(part) if side_by_side(part) else None, -v, v + (1 if v > 0 else -1), F(w) + F(part.denominator, part.numerator) / 10]
        ws = [x * (1 if v > 0 or x is None else 1) for x in ws]
        if v < 0:
            ws = [(-x if x is not None and x > 0 else x) for x in ws]
        its.append(mcq("Write %s as a decimal." % B(fx(v)), (dhtml(v), v), opts(v, ws), e))
    for d_, v in [("0.45", F(9, 20)), ("−0.8", F(-4, 5)), ("2.75", F(11, 4)), ("0.375", F(3, 8)), ("−1.6", F(-8, 5)), ("0.04", F(1, 25))]:
        ws = [F(abs(v.denominator), abs(v.numerator)) * (1 if v > 0 else -1), -v, F(int(d_.replace("−", "-").split(".")[1]), 10) if "." in d_ else v + 1]
        cands = [(fx(w), w) for w in ws if F(w) != v] + [(fx(v + F(1, v.denominator)), v + F(1, v.denominator))]
        its.append(mcq("Write %s as a fraction or mixed number in simplest form." % B(d_), (fx(v), v), cands,
                       "Read the place value and simplify: %s = %s." % (d_, fx(v))))
    its.append(mcq("Which decimal equals %s?" % B(fx(F(-7, 3))), (dhtml(F(-7, 3)), "a"), [(dhtml(F(7, 3)), "b"), ("−7.3", "c"), ("−2.3", "d")],
                   "7 ÷ 3 = 2.333…, so −7/3 = −2.<span class='ov'>3</span>."))
    its.append(mcq("Which decimal equals %s?" % B(fx(F(5, 2))), ("2.5", "a"), [("0.4", "b"), ("5.2", "c"), ("2.05", "d")], "5 ÷ 2 = 2.5."))
    its.append(mcq("Which is <b>not</b> equal to %s?" % B(fx(F(-3, 5))), ("−5/3".replace("5/3", fr(5, 3)), "a"),
                   [("−0.6", "b"), (fr("−3", "5"), "c"), (fr("3", "−5"), "d")],
                   "−3/5 = −0.6 = (−3)/5 = 3/(−5). −5/3 is a different number (−1.666…)."))
    return {"title": "Negatives, mixed numbers and back to fractions", "items": its}


# ------------------------------------------------------------ set 4
def set_compare():
    its = []
    pairs = [(F(3, 8), F("0.4")), (F(2, 3), F("0.67")), (F(5, 9), F("0.55")), (F(-1, 4), F("-0.3")), (F(7, 12), F("0.58")), (F(-5, 6), F("-0.8")),
             (F(4, 7), F("0.571")), (F(1, 3), F("0.33")),
             (F(3, 7), F("0.43")), (F(-4, 9), F("-0.45")), (F(9, 16), F("0.56")), (F(11, 15), F("0.73"))]
    ESC = {"<": "&lt;", ">": "&gt;", "=": "="}
    for a, b in pairs:
        sym = "<" if a < b else (">" if a > b else "=")
        e = "%s = %s. Compare with %s: %s %s %s." % (fx(a), dhtml(a), num(b), dhtml(a), ESC[sym], num(b))
        good = "%s %s %s" % (fx(a), ESC[sym], num(b))
        bad = [x for x in ["<", ">", "="] if x != sym]
        its.append(mcq("Which is true?", (good, "g"), [("%s %s %s" % (fx(a), ESC[x], num(b)), x) for x in bad] + [("They cannot be compared", "c")], e))
    orders = [[F(3, 5), F("0.58"), F(5, 8)], [F(-2, 3), F("-0.6"), F(-7, 10)], [F(1, 6), F("0.2"), F(3, 20)], [F(5, 4), F("1.2"), F(11, 9)]]
    for vals in orders:
        srt = sorted(vals)
        show = lambda v: fx(v) if v.denominator not in (10, 100, 1000) or len(str(v.denominator)) > 4 else num(v)
        shown = {v: (num(v) if v in [F("0.58"), F("-0.6"), F("0.2"), F("1.2")] else fx(v)) for v in vals}
        good = ", ".join(shown[v] for v in srt)
        bad1 = ", ".join(shown[v] for v in reversed(srt))
        bad2 = ", ".join(shown[v] for v in vals)
        bad3 = ", ".join(shown[v] for v in [srt[1], srt[0], srt[2]])
        cands = []
        for b_ in [bad1, bad2, bad3, ", ".join(shown[v] for v in [srt[0], srt[2], srt[1]])]:
            if b_ != good and b_ not in [c[0] for c in cands]:
                cands.append((b_, b_))
        its.append(mcq("Order from least to greatest: %s" % ", ".join(shown[v] for v in vals), (good, "g"), cands,
                       "As decimals: " + ", ".join("%s = %s" % (shown[v], dhtml(v)) for v in vals) + ". Least to greatest: " + good + "."))
    for vals in [[F(2, 9), F(1, 4), F("0.24")], [F(-3, 8), F(-2, 5), F("-0.39")], [F(7, 11), F("0.63"), F(5, 8)], [F(1, 7), F(1, 8), F("0.13")]]:
        big = max(vals)
        shown = {v: (num(v) if v.denominator in (100,) or v in [F("0.24"), F("-0.39"), F("0.63"), F("0.13")] else fx(v)) for v in vals}
        others = [v for v in vals if v != big]
        its.append(mcq("Which number is greatest?", (shown[big], "g"), [(shown[v], str(v)) for v in others] + [("They are all equal", "e")],
                       "As decimals: " + ", ".join("%s = %s" % (shown[v], dhtml(v)) for v in vals) + ". The greatest is %s." % shown[big]))
    return {"title": "Compare and order", "items": its}


# ------------------------------------------------------------ set 5
def set_words():
    its = []
    P = People(R)
    name, he, his = P.next()
    data = [
        ("%s made 7 of 8 free throws. What decimal shows the part %s made?" % (name, he), F(7, 8), [F(8, 7), F("0.78"), F(1, 8)], "7 ÷ 8 = 0.875."),
        ("A baseball player got 9 hits in 24 times at bat. What is the batting average as a decimal?", F(3, 8), [F(24, 9), F("0.924"), F(5, 8)],
         "9 ÷ 24 = 0.375 (a batting average of .375)."),
        ("A recipe needs 2/3 cup of oil. A measuring cup shows tenths. About how much is that?", F(2, 3), [F(3, 2), F("0.23"), F("0.6")],
         "2 ÷ 3 = 0.666…, a little less than 0.7 cup."),
        ("A board is 5 3/8 feet long. What is its length as a decimal?", F(43, 8), [F("5.38"), F("5.83"), F("5.125")], "3/8 = 0.375, so 5 3/8 = 5.375 feet."),
        ("A runner finished 1/6 of a race. What decimal is that?", F(1, 6), [F(6, 1), F("0.16"), F(1, 60)], "1 ÷ 6 = 0.1666… = 0.1<span class='ov'>6</span>."),
        ("The temperature changed by −3/4 degree each hour. What is the change as a decimal?", F(-3, 4), [F(3, 4), F("-0.34"), F(-4, 3)], "3 ÷ 4 = 0.75, so −0.75 degree."),
        ("A stock fell 5/8 of a dollar. What is the change as a decimal?", F(-5, 8), [F(5, 8), F("-0.58"), F("-1.6")], "5 ÷ 8 = 0.625, so the change is −$0.625."),
        ("In a class, 11 of 30 students walk to school. What decimal is that?", F(11, 30), [F(30, 11), F("0.1130"), F(11, 300)], "11 ÷ 30 = 0.3666… = 0.3<span class='ov'>6</span>."),
        ("A bag of flour weighs 2 1/4 pounds. What is the weight as a decimal?", F(9, 4), [F("2.14"), F("2.41"), F("2.5")], "1/4 = 0.25, so 2 1/4 = 2.25 pounds."),
        ("A survey found 4 out of 9 people like jazz. What decimal is that?", F(4, 9), [F(9, 4), F("0.49"), F("0.4")], "4 ÷ 9 = 0.444… = 0.<span class='ov'>4</span>."),
    ]
    for q, v, ws, e in data:
        q = q.replace("2/3", fr(2, 3)).replace("5 3/8", "5 " + fr(3, 8)).replace("1/6", fr(1, 6)).replace("−3/4", MINUS + fr(3, 4)).replace("5/8", fr(5, 8)).replace("2 1/4", "2 " + fr(1, 4))
        its.append(mcq(q, (dhtml(v), v), opts(v, ws), e))
    comp = [("Ana ran 3/5 of a mile. Ben ran 0.58 mile. Who ran farther?", "Ana", ["Ben", "They ran the same", "It cannot be told"], "3/5 = 0.6, and 0.6 > 0.58, so Ana ran farther."),
            ("Team A won 7 of 12 games. Team B won 0.6 of its games. Which team has the better record?", "Team B", ["Team A", "They are the same", "It cannot be told"],
             "7 ÷ 12 = 0.58<span class='ov'>3</span>, which is less than 0.6. Team B is better."),
            ("A bolt is 5/16 inch wide. A hole is 0.3 inch wide. Will the bolt fit?", "No, the bolt is wider.", ["Yes, the bolt is narrower.", "Yes, they are the same size.", "It cannot be told."],
             "5 ÷ 16 = 0.3125, which is more than 0.3. The bolt is too wide."),
            ("Mia saved 2/3 of her money. Leo saved 0.65 of his. Who saved the greater part?", "Mia", ["Leo", "They saved the same part", "It cannot be told"],
             "2/3 = 0.666…, which is more than 0.65."),
            ("Which is longer: 1 3/8 inches or 1.4 inches?", "1.4 inches", ["1 3/8 inches", "They are the same", "It cannot be told"], "3/8 = 0.375, so 1 3/8 = 1.375 < 1.4.")]
    for q, good, bad, e in comp:
        rp = lambda t: t.replace("3/5", fr(3, 5)).replace("5/16", fr(5, 16)).replace("2/3", fr(2, 3)).replace("1 3/8", "1 " + fr(3, 8))
        its.append(mcq(rp(q), (rp(good), "g"), [(rp(b), b) for b in bad], rp(e)))
    its.append(mcq("A calculator shows 0.142857142857… for a fraction with denominator 7. Which fraction is it?", (fr(1, 7), "a"),
                   [(fr(1, 4), "b"), (fr(14, 100), "c"), (fr(7, 1), "d")], "1 ÷ 7 = 0.<span class='ov'>142857</span>. The block 142857 repeats."))
    its.append(mcq("A scale shows 0.875 pound. Which fraction is that?", (fr(7, 8), "a"), [(fr(8, 7), "b"), (fr(875, 100), "c"), (fr(5, 8), "d")],
                   "0.875 = 875/1000 = 7/8."))
    its.append(mcq("A fuel gauge shows the tank is 0.375 full. Which fraction is that?", (fr(3, 8), "a"), [(fr(3, 75), "b"), (fr(37, 5), "c"), (fr(5, 8), "d")],
                   "0.375 = 375/1000 = 3/8."))
    its.append(mcq("Which fraction is a repeating decimal: %s, %s, %s or %s?" % (fr(3, 4), fr(7, 10), fr(5, 12), fr(9, 16)), (fr(5, 12), "a"),
                   [(fr(3, 4), "b"), (fr(7, 10), "c"), (fr(9, 16), "d")], "12 = 2 × 2 × 3. The factor 3 makes 5/12 = 0.41<span class='ov'>6</span> repeat."))
    its.append(mcq("Leo says 1/3 = 0.3. What is wrong?", ("1/3 = 0.333…, which is a little more than 0.3.".replace("1/3", fr(1, 3)), "a"),
                   [("1/3 = 3.0".replace("1/3", fr(1, 3)), "b"), ("1/3 = 0.13".replace("1/3", fr(1, 3)), "c"), ("Nothing is wrong.", "d")],
                   "1 ÷ 3 = 0.333… = 0.<span class='ov'>3</span>. 0.3 is 3/10."))
    return {"title": "Word problems", "items": its}


def body():
    rows = [[fr(1, 2), "1 ÷ 2", "0.5", "terminates"], [fr(3, 8), "3 ÷ 8", "0.375", "terminates"], [fr(2, 3), "2 ÷ 3", "0.<span class='ov'>6</span>", "repeats"],
            [fr(1, 6), "1 ÷ 6", "0.1<span class='ov'>6</span>", "repeats"], [fr(2, 11), "2 ÷ 11", "0.<span class='ov'>18</span>", "repeats"]]
    return ("<h2>A fraction is a division</h2><p>To change a fraction to a decimal, <b>divide the numerator by the denominator</b>. "
            "Use long division and keep adding zeros. The decimal either <b>ends</b> (terminates) or a group of digits <b>repeats</b> forever.</p>"
            + table(["Fraction", "Divide", "Decimal", "Type"], rows)
            + "<h2>Bar notation</h2><p>Draw a bar over the digits that repeat: 0.1666… = 0.1<span class='ov'>6</span> and 0.181818… = 0.<span class='ov'>18</span>. "
            "In simplest form, a fraction terminates only when its denominator has no prime factors except 2 and 5.</p>"
            + example("Write " + fr(5, 12) + " as a decimal.", ["5 ÷ 12 = 0.41666…", "The 6 repeats, so put the bar over the 6 only."], "0.41<span class='ov'>6</span>")
            + example("Write −2 " + fr(3, 4) + " as a decimal.", [fr(3, 4) + " = 3 ÷ 4 = 0.75.", "Keep the whole number and the sign."], "−2.75")
            + "<h2>Common mistakes</h2><ul><li>Dividing the wrong way: " + fr(3, 8) + " is 3 ÷ 8 = 0.375, not 8 ÷ 3.</li>"
            "<li>Writing the digits side by side: " + fr(3, 8) + " is not 0.38.</li>"
            "<li>Putting the bar over too many digits: 0.1666… is 0.1<span class='ov'>6</span>, not 0.<span class='ov'>16</span>.</li></ul>")


def main():
    sets = [set_terminating(), set_repeating(), set_mixed_negative(), set_compare(), set_words()]
    for st in sets:
        for it in st["items"]:
            it["e"] = it["e"].replace(" < ", " &lt; ").replace(" > ", " &gt; ")
    balance(sets, R)
    unit = {
        "slug": "converting-fractions-to-decimals",
        "title": "Converting Fractions to Decimals",
        "seo_title": "Grade 7 Converting Fractions to Decimals Worksheets: Terminating and Repeating Decimals",
        "short_title": "Fractions to decimals",
        "domain": "The Number System",
        "standard_code": "7.NS.A.2d",
        "standard_url": "https://www.thecorestandards.org/Math/Content/7/NS/A/2/",
        "standard_text": "Convert a rational number to a decimal using long division; know that the decimal form of a rational number terminates in 0s or eventually repeats.",
        "meta_desc": "Free Grade 7 fractions to decimals worksheets: divide to convert, terminating and repeating decimals, bar notation, negative and mixed numbers, decimals back to fractions, comparing and ordering, and word problems. 100 practice questions with an answer key.",
        "key_big": "Divide the numerator by the denominator. The decimal ends or repeats.",
        "key_sub": "3/8 = 3 ÷ 8 = 0.375. 2/3 = 0.666… = 0.6 with a bar over the 6.",
        "body_html": body(),
        "faq": [
            {"q": "How do you convert a fraction to a decimal?", "a": "Divide the numerator by the denominator. 3/8 = 3 ÷ 8 = 0.375."},
            {"q": "What is a repeating decimal?", "a": "A decimal in which a digit or group of digits repeats forever, like 2/3 = 0.666… or 2/11 = 0.181818…"},
            {"q": "How do I know if a fraction terminates?", "a": "Write it in simplest form. If the denominator has no prime factors other than 2 and 5, the decimal terminates. Otherwise it repeats."},
            {"q": "How do you write bar notation?", "a": "Draw a bar over only the digits that repeat. 0.1666… is written 0.16 with the bar over the 6 only."}],
        "sets": sets,
        "pdf_url": "",
        "sort": 13,
        "updated": UPDATED,
    }
    write_unit("us", "math", "grade-7", unit)


if __name__ == "__main__":
    main()
