# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Scientific Notation (8.EE.A.3, 8.EE.A.4)
  python3 tools/gen_us_math_g8_scientific_notation.py
Write large and small numbers in scientific notation and back, compare them, find how many times
larger one is, and multiply, divide, add and subtract in scientific notation. Wrong answers come from
real mistakes: counting the wrong number of places, the wrong sign of the exponent, a first factor
that is not between 1 and 10, and adding the exponents when dividing.
"""
import random
from decimal import Decimal as D, getcontext
from ws_common import mcq, balance, B, table, example, write_unit, MINUS

getcontext().prec = 40
R = random.Random(80701)
UPDATED = "2026-11-16"


def dstr(d):
    """Plain decimal text with commas in the whole part: 3,500,000 or 0.00042."""
    d = D(d).normalize()
    s = format(d, "f")
    neg = s.startswith("-")
    s = s.lstrip("-")
    ip, _, fp = s.partition(".")
    ip = "{:,}".format(int(ip))
    return (MINUS if neg else "") + ip + ("." + fp if fp else "")


def sci(m, e):
    m = D(m).normalize()
    ms = format(m, "f")
    return "%s × 10<sup>%s</sup>" % (ms, (MINUS + str(-e)) if e < 0 else str(e))


def to_sci(d):
    d = D(d)
    e = d.copy_abs().adjusted()
    m = (d / (D(10) ** e)).normalize()
    return m, e


# ============================================================ set 1: large numbers
def set_large():
    its = []
    for n in ["3500000", "42000", "607000000", "9100", "12000000000", "5000000", "780000", "30400000", "2600000000", "95000",
              "1050000", "8000000000", "414000", "67000000", "123000", "7700000000000", "250000000", "18000", "903000000", "4000000000000"]:
        m, e = to_sci(n)
        q = "Write %s in scientific notation." % B(dstr(n))
        ex = "Move the decimal point %d places left to get %s (between 1 and 10). So the answer is <b>%s</b>." % (e, format(m, "f"), sci(m, e))
        wr = [sci(m, e - 1), sci(m, e + 1), sci(m * 10, e - 1), sci(m, -e)]
        its.append(mcq(q, (sci(m, e), (m, e)), [(w, w) for w in wr], ex))
    return {"title": "Large numbers", "items": its}


# ============================================================ set 2: small numbers
def set_small():
    its = []
    for n in ["0.0042", "0.00065", "0.000007", "0.031", "0.0000189", "0.0005", "0.00000072", "0.08", "0.000303", "0.0000000016"]:
        m, e = to_sci(n)
        q = "Write %s in scientific notation." % B(dstr(n))
        ex = ("Move the decimal point %d places right to get %s. A small number has a negative exponent: <b>%s</b>."
              % (-e, format(m, "f"), sci(m, e)))
        wr = [sci(m, -e), sci(m, e - 1), sci(m, e + 1), sci(m * 10, e - 1)]
        its.append(mcq(q, (sci(m, e), (m, e)), [(w, w) for w in wr], ex))
    for m, e in [("4.5", -3), ("2", -5), ("7.08", -2), ("1.6", -7), ("9", -1), ("3.33", -4), ("6.1", -6), ("8.25", -5), ("5", -8), ("1.02", -3)]:
        v = D(m) * D(10) ** e
        q = "Write %s in standard form." % B(sci(m, e))
        ex = "A negative exponent means a small number. Move the decimal point %d places left: <b>%s</b>." % (-e, dstr(v))
        wr = [dstr(D(m) * D(10) ** (-e)), dstr(v * 10), dstr(v / 10), MINUS + dstr(D(m) * D(10) ** (-e))]
        its.append(mcq(q, (dstr(v), v), [(w, w) for w in wr], ex))
    o = its
    order = [o[0], o[10], o[1], o[11], o[2], o[12], o[3], o[13], o[4], o[14], o[5], o[15], o[6], o[16], o[7], o[17], o[8],
             o[18], o[9], o[19]]
    return {"title": "Small numbers", "items": order}


# ============================================================ set 3: standard form and which is correct
def set_standard():
    its = []
    for m, e in [("6.2", 5), ("3", 8), ("1.75", 4), ("9.01", 6), ("4.4", 3), ("2.5", 9), ("8.06", 7), ("7", 2), ("5.123", 5), ("1.9", 10)]:
        v = D(m) * D(10) ** e
        q = "Write %s in standard form." % B(sci(m, e))
        ex = "Move the decimal point %d places right: <b>%s</b>." % (e, dstr(v))
        wr = [dstr(v * 10), dstr(v / 10), dstr(D(m.replace(".", "")) * D(10) ** e) if "." in m else dstr(v * 100), dstr(D(m) * D(10) ** (-e))]
        its.append(mcq(q, (dstr(v), v), [(w, w) for w in wr], ex))
    for good, bads, why in [
        (sci("3.2", 4), [("32 × 10<sup>3</sup>"), ("0.32 × 10<sup>5</sup>"), ("3.2 × 4<sup>10</sup>")], "The first factor must be at least 1 and less than 10."),
        (sci("7", -3), ["7 × 10<sup>−3.5</sup>", "70 × 10<sup>−4</sup>", "0.7 × 10<sup>−2</sup>"], "The first factor must be between 1 and 10, and the power of 10 must be a whole number."),
        (sci("1", 6), ["10 × 10<sup>5</sup>", "0.1 × 10<sup>7</sup>", "1 × 6<sup>10</sup>"], "1 is allowed as the first factor; 10 is not."),
        (sci("9.99", 2), ["99.9 × 10<sup>1</sup>", "0.999 × 10<sup>3</sup>", "9.99 + 10<sup>2</sup>"], "Only 9.99 is between 1 and 10, and it must be times a power of 10."),
        (sci("4.06", -8), ["40.6 × 10<sup>−9</sup>", "4.06 × 10<sup>8</sup>", "0.406 × 10<sup>−7</sup>"], "4.06 is between 1 and 10 and the exponent is a whole number."),
    ]:
        its.append(mcq("Which number is written in scientific notation?", (good, good), [(b, b) for b in bads],
                       why + " The answer is <b>%s</b>." % good))
    for wrong, right in [("45 × 10<sup>4</sup>", sci("4.5", 5)), ("0.6 × 10<sup>3</sup>", sci("6", 2)), ("123 × 10<sup>−5</sup>", sci("1.23", -3)),
                         ("0.08 × 10<sup>9</sup>", sci("8", 7)), ("31 × 10<sup>−2</sup>", sci("3.1", -1))]:
        q = "Rewrite %s in correct scientific notation." % B(wrong)
        m, e = right.split(" × 10<sup>")
        e = e.replace("</sup>", "").replace(MINUS, "-")
        ee = int(e)
        wr = [sci(m, ee + 1), sci(m, ee - 2), sci(m, -ee)]
        ex = "Make the first factor between 1 and 10, then change the exponent to match: <b>%s</b>." % right
        its.append(mcq(q, (right, right), [(w, w) for w in wr], ex))
    o = its
    order = [o[0], o[10], o[1], o[15], o[2], o[11], o[3], o[16], o[4], o[12], o[5], o[17], o[6], o[13], o[7], o[18], o[8],
             o[14], o[9], o[19]]
    return {"title": "Standard form and correct notation", "items": order}


# ============================================================ set 4: compare
def set_compare():
    its = []
    for (m1, e1), (m2, e2) in [(("3", 8), ("6", 7)), (("2.5", -4), ("9", -5)), (("7.1", 6), ("7.1", 9)), (("4", 3), ("3.9", 3)),
                               (("1.2", -6), ("1.2", -3)), (("8", 12), ("9", 11)), (("5.5", -2), ("5.4", -2)), (("6", 10), ("2", 11))]:
        a, b = D(m1) * D(10) ** e1, D(m2) * D(10) ** e2
        big = sci(m1, e1) if a > b else sci(m2, e2)
        q = "Which is greater: %s or %s?" % (B(sci(m1, e1)), B(sci(m2, e2)))
        if e1 != e2:
            ex = "Compare the exponents first: 10<sup>%s</sup> vs 10<sup>%s</sup>. The greater power wins: <b>%s</b>." % (
                str(e1).replace("-", MINUS), str(e2).replace("-", MINUS), big)
        else:
            ex = "The exponents are the same, so compare %s and %s: <b>%s</b> is greater." % (m1, m2, big)
        other = sci(m2, e2) if big == sci(m1, e1) else sci(m1, e1)
        its.append(mcq(q, (big, big), [(other, other), ("They are equal", "eq"), ("We cannot tell", "ct")], ex))
    for (m1, e1), (m2, e2), ans in [(("6", 8), ("2", 5), "3,000"), (("9", 7), ("3", 4), "3,000"), (("8", 12), ("4", 9), "2,000"),
                                    (("5", 6), ("1", 3), "5,000"), (("1", 9), ("2", 6), "500"), (("3", 10), ("1.5", 8), "200"),
                                    (("4", -3), ("2", -6), "2,000"), (("7", 5), ("7", 2), "1,000"), (("1.2", 7), ("4", 4), "300"),
                                    (("2", 9), ("5", 6), "400"), (("6", -2), ("3", -5), "2,000"), (("9", 11), ("3", 7), "30,000")]:
        a, b = D(m1) * D(10) ** e1, D(m2) * D(10) ** e2
        r = a / b
        assert dstr(r) == ans, (r, ans)
        q = "How many times greater is %s than %s?" % (B(sci(m1, e1)), B(sci(m2, e2)))
        ex = "Divide: %s ÷ %s = %s, and 10<sup>%s</sup> ÷ 10<sup>%s</sup> = 10<sup>%s</sup>. So it is <b>%s</b> times greater." % (
            m1, m2, format((D(m1) / D(m2)).normalize(), "f"), str(e1).replace("-", MINUS), str(e2).replace("-", MINUS),
            str(e1 - e2).replace("-", MINUS), ans)
        wr = [dstr(r * 10), dstr(r / 10), dstr(D(m1) / D(m2)) if dstr(D(m1) / D(m2)) != ans else dstr(r * 100), str(e1 - e2)]
        its.append(mcq(q, (ans, r), [(w, w) for w in wr], ex))
    o = its
    order = [o[0], o[8], o[1], o[9], o[2], o[10], o[3], o[11], o[4], o[12], o[5], o[13], o[6], o[14], o[7], o[15], o[16],
             o[17], o[18], o[19]]
    return {"title": "Compare and how many times", "items": order}


# ============================================================ set 5: operations and real life
def set_ops():
    its = []
    for (m1, e1), op, (m2, e2) in [(("2", 3), "×", ("3", 4)), (("4", 5), "×", ("2", -2)), (("6", 8), "÷", ("3", 2)), (("5", 7), "×", ("4", 3)),
                                   (("9", 6), "÷", ("3", 8)), (("1.5", 4), "×", ("6", 5)), (("8", -3), "÷", ("2", -7)), (("2.5", 6), "×", ("4", -9)),
                                   (("7.2", 10), "÷", ("2.4", 4)), (("3", 9), "×", ("3", 9))]:
        a, b = D(m1) * D(10) ** e1, D(m2) * D(10) ** e2
        v = a * b if op == "×" else a / b
        m, e = to_sci(v)
        q = "Find %s. Write the answer in scientific notation." % B("(%s) %s (%s)" % (sci(m1, e1), op, sci(m2, e2)))
        mm = D(m1) * D(m2) if op == "×" else D(m1) / D(m2)
        ee = e1 + e2 if op == "×" else e1 - e2
        ex = "%s the numbers: %s %s %s = %s. %s the exponents: 10<sup>%s</sup>." % (
            "Multiply" if op == "×" else "Divide", m1, op, m2, format(mm.normalize(), "f"), "Add" if op == "×" else "Subtract",
            str(ee).replace("-", MINUS))
        if mm >= 10 or mm < 1:
            ex += " Adjust so the first factor is between 1 and 10."
        ex += " The answer is <b>%s</b>." % sci(m, e)
        wrong_e = e1 - e2 if op == "×" else e1 + e2
        wr = [sci(m, e + 1), sci(m, e - 1), sci(m, wrong_e + (e - ee)) if wrong_e + (e - ee) != e else sci(m, -e), sci(mm, ee) if (mm >= 10 or mm < 1) else sci(m, e + 2)]
        its.append(mcq(q, (sci(m, e), (m, e)), [(w, w) for w in wr], ex))
    for q, ans, wr, ex in [
        ("The Sun is about 1.5 × 10<sup>8</sup> km from Earth. The Moon is about 3.8 × 10<sup>5</sup> km away. About how many times farther is the Sun?",
         "About 400 times", ["About 40 times", "About 4,000 times", "About 3 times"],
         "1.5 × 10<sup>8</sup> ÷ 3.8 × 10<sup>5</sup> ≈ 0.4 × 10<sup>3</sup> = 400. <b>About 400 times</b>."),
        ("A virus is about 1 × 10<sup>−7</sup> m long. A bacterium is about 2 × 10<sup>−6</sup> m long. How many times longer is the bacterium?",
         "20 times", ["2 times", "200 times", "10 times"], "2 × 10<sup>−6</sup> ÷ 1 × 10<sup>−7</sup> = 2 × 10<sup>1</sup> = <b>20 times</b>."),
        ("The US population is about 3.3 × 10<sup>8</sup>. Each person drinks about 2 × 10<sup>2</sup> liters of milk a year. About how much is that in all?",
         "6.6 × 10<sup>10</sup> liters", ["6.6 × 10<sup>16</sup> liters", "5.3 × 10<sup>10</sup> liters", "6.6 × 10<sup>6</sup> liters"],
         "3.3 × 2 = 6.6 and 10<sup>8</sup> × 10<sup>2</sup> = 10<sup>10</sup>: <b>6.6 × 10<sup>10</sup> liters</b>."),
        ("Add: 3 × 10<sup>5</sup> + 4 × 10<sup>4</sup>.", "3.4 × 10<sup>5</sup>", ["7 × 10<sup>9</sup>", "7 × 10<sup>5</sup>", "3.04 × 10<sup>5</sup>"],
         "Write 4 × 10<sup>4</sup> as 0.4 × 10<sup>5</sup>. Then 3 + 0.4 = 3.4: <b>3.4 × 10<sup>5</sup></b>."),
        ("Subtract: 9 × 10<sup>6</sup> − 5 × 10<sup>5</sup>.", "8.5 × 10<sup>6</sup>", ["4 × 10<sup>1</sup>", "4 × 10<sup>6</sup>", "8.95 × 10<sup>6</sup>"],
         "Write 5 × 10<sup>5</sup> as 0.5 × 10<sup>6</sup>. Then 9 − 0.5 = 8.5: <b>8.5 × 10<sup>6</sup></b>."),
        ("A hard drive holds 2 × 10<sup>12</sup> bytes. A photo is 4 × 10<sup>6</sup> bytes. How many photos fit?", "5 × 10<sup>5</sup>",
         ["2 × 10<sup>6</sup>", "8 × 10<sup>18</sup>", "5 × 10<sup>6</sup>"], "2 ÷ 4 = 0.5 and 10<sup>12</sup> ÷ 10<sup>6</sup> = 10<sup>6</sup>: 0.5 × 10<sup>6</sup> = <b>5 × 10<sup>5</sup></b>."),
        ("Light travels about 3 × 10<sup>5</sup> km each second. How far does it travel in 6 × 10<sup>1</sup> seconds (1 minute)?",
         "1.8 × 10<sup>7</sup> km", ["1.8 × 10<sup>6</sup> km", "18 × 10<sup>5</sup> km", "5 × 10<sup>3</sup> km"],
         "3 × 6 = 18 and 10<sup>5</sup> × 10<sup>1</sup> = 10<sup>6</sup>: 18 × 10<sup>6</sup> = <b>1.8 × 10<sup>7</sup> km</b>."),
        ("A calculator shows 4.2E−5. What number is it?", "0.000042", ["420,000", "0.0000042", "4.2"],
         "E−5 means × 10<sup>−5</sup>: 4.2 × 10<sup>−5</sup> = <b>0.000042</b>."),
        ("A calculator shows 7.3E9. What number is it?", "7,300,000,000", ["730,000,000", "73,000,000,000", "0.0000000073"],
         "E9 means × 10<sup>9</sup>: <b>7,300,000,000</b>."),
        ("Earth’s mass is about 6 × 10<sup>24</sup> kg. Jupiter’s is about 1.9 × 10<sup>27</sup> kg. About how many times heavier is Jupiter?",
         "About 300 times", ["About 30 times", "About 3,000 times", "About 3 times"],
         "1.9 × 10<sup>27</sup> ÷ 6 × 10<sup>24</sup> ≈ 0.3 × 10<sup>3</sup> = 300. <b>About 300 times</b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], ex))
    o = its
    order = [o[0], o[10], o[1], o[17], o[2], o[13], o[3], o[18], o[4], o[11], o[5], o[14], o[6], o[15], o[7], o[16], o[8],
             o[12], o[9], o[19]]
    return {"title": "Operations and real life", "items": order}


def body():
    return ("<h2>What is scientific notation?</h2>"
            "<p>Scientific notation writes a number as <b>a × 10<sup>n</sup></b>, where a is at least 1 and less than 10, and n is a whole number.</p>"
            + table(["Standard form", "Scientific notation", "Why"], [
                ["3,500,000", "3.5 × 10<sup>6</sup>", "decimal point moves 6 places left"],
                ["0.00042", "4.2 × 10<sup>−4</sup>", "decimal point moves 4 places right"]])
            + "<p>Big numbers have a positive exponent. Small numbers (less than 1) have a negative exponent.</p>"
            + example("Find (6 × 10<sup>8</sup>) ÷ (3 × 10<sup>2</sup>).", ["Divide the numbers: 6 ÷ 3 = 2.",
                      "Subtract the exponents: 8 − 2 = 6."], "2 × 10<sup>6</sup>")
            + example("How many times greater is 9 × 10<sup>7</sup> than 3 × 10<sup>4</sup>?", ["9 ÷ 3 = 3.",
                      "10<sup>7</sup> ÷ 10<sup>4</sup> = 10<sup>3</sup>.", "3 × 10<sup>3</sup> = 3,000."], "3,000 times")
            + "<h2>Common mistakes</h2><ul><li>A first factor that is 10 or more: 35 × 10<sup>5</sup> should be 3.5 × 10<sup>6</sup>.</li>"
            "<li>The wrong sign: 0.004 is 4 × 10<sup>−3</sup>, not 4 × 10<sup>3</sup>.</li>"
            "<li>Counting places wrong: count every place the decimal point moves.</li>"
            "<li>Adding the exponents when you divide. Subtract them.</li></ul>")


def main():
    sets = [set_large(), set_small(), set_standard(), set_compare(), set_ops()]
    balance(sets, R)
    unit = {
        "slug": "scientific-notation",
        "title": "Scientific Notation",
        "seo_title": "Grade 8 Scientific Notation Worksheets: Convert, Compare, Multiply and Divide",
        "short_title": "Scientific notation",
        "domain": "Expressions & Equations",
        "standard_code": "8.EE.A.4",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/EE/A/4/",
        "standard_text": "Perform operations with numbers expressed in scientific notation, including problems where both decimal and scientific notation are used. Use scientific notation and choose units of appropriate size for measurements of very large or very small quantities. Interpret scientific notation that has been generated by technology.",
        "meta_desc": "Free Grade 8 scientific notation worksheets: write large and small numbers in scientific notation and standard form, compare them, find how many times greater, and multiply, divide, add and subtract. 100 questions with an answer key.",
        "key_big": "Write a number as a × 10ⁿ, with a at least 1 and less than 10.",
        "key_sub": "Big numbers: positive n. Small numbers: negative n. Multiply → add exponents, divide → subtract.",
        "body_html": body(),
        "faq": [
            {"q": "How do you write a number in scientific notation?", "a": "Move the decimal point until the number is between 1 and 10. Count the places you moved. Moving left gives a positive exponent; moving right gives a negative one. 3,500,000 = 3.5 × 10⁶."},
            {"q": "What does a negative exponent mean in scientific notation?", "a": "It means the number is less than 1. 4.2 × 10⁻⁴ = 0.00042."},
            {"q": "How do you multiply numbers in scientific notation?", "a": "Multiply the first factors and add the exponents. Then adjust so the first factor is between 1 and 10."},
            {"q": "What does 4.2E−5 on a calculator mean?", "a": "E means × 10 to the power. 4.2E−5 = 4.2 × 10⁻⁵ = 0.000042."}],
        "sets": sets, "pdf_url": "", "sort": 7, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
