# -*- coding: utf-8 -*-
"""
US Grade 8 Math: Exponent Rules (8.EE.A.1)
  python3 tools/gen_us_math_g8_exponent_rules.py
Product, quotient and power-of-a-power rules, zero and negative exponents, and evaluating numeric
expressions. Wrong answers come from real mistakes: multiplying exponents instead of adding,
multiplying the bases, subtracting in the wrong order, and reading a negative exponent as a negative number.
"""
import random
from fractions import Fraction as F
from ws_common import num, mcq, balance, B, table, example, write_unit, fr, MINUS

R = random.Random(80601)
UPDATED = "2026-11-16"


def pw(base, e):
    b = str(base) if not isinstance(base, int) or base >= 0 else "(%s%d)" % (MINUS, -base)
    ex = num(e)
    return "%s<sup>%s</sup>" % (b, ex)


def val(v):
    v = F(v)
    if v.denominator == 1:
        return num(v)
    return (MINUS if v < 0 else "") + fr(abs(v.numerator), v.denominator)


def pw_choices(base, right, wrongs):
    out = []
    for e in wrongs:
        if e is None:
            continue
        if isinstance(e, tuple):
            out.append((pw(e[0], e[1]), ("x", e[0], e[1])))
        else:
            out.append((pw(base, e), ("p", base, e)))
    return out


# ============================================================ set 1: product
def set_product():
    its = []
    for b, m, n in [(2, 3, 4), (5, 2, 6), (7, 4, 1), ("<i>x</i>", 3, 5), (3, 5, 5), ("<i>a</i>", 2, 7), (10, 3, 3), (4, 6, 2),
                    ("<i>y</i>", 1, 8), (6, 7, 3), (9, 2, 2), ("<i>m</i>", 4, 9), (2, -3, 5), (3, 6, -2), ("<i>x</i>", -4, 7),
                    (5, -2, -3), (8, 0, 4), ("<i>n</i>", 5, -5), (11, 2, 8), (2, 10, 5)]:
        q = "Simplify %s × %s." % (B(pw(b, m)), B(pw(b, n)))
        e = "Same base, so add the exponents: %s + %s = %s. The answer is <b>%s</b>." % (
            num(m), "(%s)" % num(n) if n < 0 else num(n), num(m + n), pw(b, m + n))
        cands = pw_choices(b, m + n, [m * n, m - n, n - m, m + n + 1])
        if isinstance(b, int):
            cands.insert(1, (pw(b * b, m + n), ("x", b * b, m + n)))
        its.append(mcq(q, (pw(b, m + n), ("p", b, m + n)), cands, e))
    return {"title": "Product rule: add exponents", "items": its}


# ============================================================ set 2: quotient
def set_quotient():
    its = []
    for b, m, n in [(2, 7, 3), (5, 8, 2), (10, 6, 4), ("<i>x</i>", 9, 4), (3, 5, 1), ("<i>a</i>", 12, 5), (7, 6, 6), (4, 3, 5),
                    ("<i>y</i>", 2, 7), (6, 10, 3), (9, -2, 3), ("<i>m</i>", 4, -3), (2, -1, -6), (8, 5, 9), ("<i>n</i>", 0, 3),
                    (3, 11, 4), (12, 4, 2), ("<i>x</i>", -5, -2), (5, 3, 3), (10, 2, -4)]:
        q = "Simplify %s ÷ %s." % (B(pw(b, m)), B(pw(b, n)))
        e = "Same base, so subtract the exponents: %s − %s = %s. The answer is <b>%s</b>." % (
            num(m), "(%s)" % num(n) if n < 0 else num(n), num(m - n), pw(b, m - n))
        if m - n == 0:
            e += " Any nonzero number to the power 0 is 1."
        cands = pw_choices(b, m - n, [m + n, n - m, F(m, n) if n and m % n == 0 else None, m * n if m * n != m - n else None, m - n - 1])
        cands = [c for c in cands if c[1] != ("p", b, m - n)]
        its.append(mcq(q, (pw(b, m - n), ("p", b, m - n)), cands, e))
    return {"title": "Quotient rule: subtract exponents", "items": its}


# ============================================================ set 3: power of a power
def set_power():
    its = []
    for b, m, n in [(2, 3, 2), (5, 4, 3), ("<i>x</i>", 2, 5), (3, 1, 6), (10, 2, 4), ("<i>a</i>", 3, 3), (7, 5, 2), (4, -2, 3),
                    ("<i>y</i>", 6, -1), (2, -3, -2), (6, 0, 5), ("<i>m</i>", 4, 4)]:
        q = "Simplify %s." % B("(%s)<sup>%s</sup>" % (pw(b, m), num(n)))
        e = "Power of a power: multiply the exponents. %s × %s = %s. The answer is <b>%s</b>." % (
            num(m), "(%s)" % num(n) if n < 0 else num(n), num(m * n), pw(b, m * n))
        cands = pw_choices(b, m * n, [m + n, m ** 2 if m > 0 else None, m * n + 1, -m * n, m - n])
        cands = [c for c in cands if c[1] != ("p", b, m * n)]
        its.append(mcq(q, (pw(b, m * n), ("p", b, m * n)), cands, e))
    for (a, b), n, ans in [((2, "<i>x</i>"), 3, "8<i>x</i><sup>3</sup>"), ((3, "<i>a</i>"), 2, "9<i>a</i><sup>2</sup>"),
                           ((5, "<i>y</i>"), 2, "25<i>y</i><sup>2</sup>"), ((2, "<i>m</i>"), 4, "16<i>m</i><sup>4</sup>")]:
        q = "Simplify %s." % B("(%d%s)<sup>%d</sup>" % (a, b, n))
        e = "Raise each factor to the power %d: %d<sup>%d</sup> = %d, so the answer is <b>%s</b>." % (n, a, n, a ** n, ans)
        wr = ["%d%s<sup>%d</sup>" % (a, b, n), "%d%s<sup>%d</sup>" % (a * n, b, n), "%d%s" % (a ** n, b)]
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    for q, ans, wr, e in [
        ("Simplify (<i>x</i><sup>2</sup>)<sup>3</sup> × <i>x</i><sup>4</sup>.", "<i>x</i><sup>10</sup>",
         ["<i>x</i><sup>9</sup>", "<i>x</i><sup>24</sup>", "<i>x</i><sup>20</sup>"], "(x²)³ = x⁶. Then x⁶ × x⁴ = <b>x<sup>10</sup></b>."),
        ("Simplify 2<sup>5</sup> × 2<sup>3</sup> ÷ 2<sup>4</sup>.", "2<sup>4</sup>", ["2<sup>2</sup>", "2<sup>12</sup>", "2<sup>60</sup>"],
         "Add then subtract: 5 + 3 − 4 = 4. The answer is <b>2<sup>4</sup></b>."),
        ("Simplify (3<sup>4</sup>)<sup>2</sup> ÷ 3<sup>5</sup>.", "3<sup>3</sup>", ["3<sup>1</sup>", "3<sup>13</sup>", "3<sup>40</sup>"],
         "(3⁴)² = 3⁸. Then 3⁸ ÷ 3⁵ = <b>3<sup>3</sup></b>."),
        ("Which is equal to 4<sup>6</sup>?", "(4<sup>2</sup>)<sup>3</sup>", ["4<sup>2</sup> × 4<sup>3</sup>", "4<sup>2</sup> + 4<sup>4</sup>", "(4<sup>3</sup>)<sup>3</sup>"],
         "(4²)³ = 4^(2 × 3) = 4⁶. The answer is <b>(4<sup>2</sup>)<sup>3</sup></b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[1], o[12], o[2], o[3], o[13], o[4], o[5], o[14], o[6], o[15], o[7], o[16], o[8], o[17], o[9], o[18],
             o[10], o[19], o[11]]
    return {"title": "Power of a power", "items": order}


# ============================================================ set 4: zero and negative
def set_neg():
    its = []
    for b, e_ in [(7, 0), (2, -3), (5, -2), (10, -3), (3, -4), (4, -1), (-6, 0), (1, -9), (6, -2), (2, -5), (9, -1), (-2, -3)]:
        v = F(b) ** e_
        q = "What is the value of %s?" % B(pw(b, e_))
        if e_ == 0:
            e = "Any nonzero number to the power 0 is 1. The answer is <b>1</b>."
            wr = [F(0), F(b), F(-1)]
        else:
            e = "A negative exponent means 1 over the positive power: %s = 1 ÷ %s = <b>%s</b>." % (pw(b, e_), pw(b, -e_), val(v))
            wr = [-(F(b) ** (-e_)), F(b) * e_, -v, F(1, b * -e_) if b * -e_ else None, F(b) ** (-e_), F(-e_, b)]
        its.append(mcq(q, (val(v), v), [(val(w), w) for w in wr if w is not None], e))
    FR = "<span class='fr'><span class='fn'>1</span><span class='fd'>%s</span></span>"
    for txt, ans, wr, e in [
        ("Write %s with a positive exponent." % pw("<i>x</i>", -4), FR % pw("<i>x</i>", 4),
         [MINUS + pw("<i>x</i>", 4), pw("<i>x</i>", 4), MINUS + "4<i>x</i>"], "<i>x</i><sup>−4</sup> = 1 ÷ <i>x</i><sup>4</sup>."),
        ("Write %s with a positive exponent." % pw(3, -2), FR % pw(3, 2), [MINUS + pw(3, 2), pw(3, 2), MINUS + "6"],
         "3<sup>−2</sup> = 1 ÷ 3<sup>2</sup>."),
        ("Write 1 ÷ %s with a negative exponent." % pw(5, 3), pw(5, -3), [MINUS + pw(5, 3), pw(5, 3), pw(3, 5)],
         "1 ÷ 5<sup>3</sup> = 5<sup>−3</sup>."),
        ("Write 1 ÷ %s with a negative exponent." % pw("<i>a</i>", 6), pw("<i>a</i>", -6),
         [MINUS + pw("<i>a</i>", 6), pw("<i>a</i>", 6), "6<i>a</i>"], "1 ÷ <i>a</i><sup>6</sup> = <i>a</i><sup>−6</sup>."),
    ]:
        its.append(mcq(txt, (ans, ans), [(w, w) for w in wr], e + " The answer is <b>%s</b>." % ans))
    for q, ans, wr, e in [
        ("Is 2<sup>−3</sup> a negative number?", "No, it is 1/8", ["Yes, it is −8", "Yes, it is −6", "No, it is 8"],
         "A negative exponent makes a fraction, not a negative number: 2⁻³ = 1/8. <b>No, it is 1/8</b>."),
        ("Why is 5<sup>0</sup> equal to 1?", "5³ ÷ 5³ = 5⁰, and any number divided by itself is 1",
         ["Because 5 × 0 = 0", "Because 0 is the same as 1", "It is not; 5⁰ = 0"],
         "By the quotient rule, 5³ ÷ 5³ = 5⁰. But 125 ÷ 125 = 1. So <b>5⁰ = 1</b>."),
        ("Which is the greatest?", "2<sup>0</sup>", ["2<sup>−1</sup>", "2<sup>−2</sup>", "2<sup>−3</sup>"],
         "2⁰ = 1, 2⁻¹ = 1/2, 2⁻² = 1/4, 2⁻³ = 1/8. The greatest is <b>2<sup>0</sup></b>."),
        ("Which is equal to 0.001?", "10<sup>−3</sup>", ["10<sup>3</sup>", "10<sup>−2</sup>", "−10<sup>3</sup>"],
         "0.001 = 1/1,000 = 1 ÷ 10³ = <b>10<sup>−3</sup></b>."),
    ]:
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[6], o[1], o[12], o[2], o[16], o[3], o[13], o[4], o[17], o[5], o[14], o[7], o[18], o[8], o[15], o[9],
             o[19], o[10], o[11]]
    return {"title": "Zero and negative exponents", "items": order}


# ============================================================ set 5: evaluate
def set_eval():
    its = []
    for b, m, n, op in [(3, 2, -5, "×"), (2, 6, 3, "÷"), (5, -2, 4, "×"), (10, 3, 5, "÷"), (4, -3, 2, "×"), (2, -2, -4, "×"),
                        (6, 5, 3, "÷"), (3, 4, -6, "×"), (7, 2, 4, "÷"), (2, 10, 7, "÷"), (9, -1, 2, "×"), (10, -6, 4, "×")]:
        ex = m + n if op == "×" else m - n
        v = F(b) ** ex
        q = "What is the value of %s?" % B("%s %s %s" % (pw(b, m), op, pw(b, n)))
        e = "%s the exponents: %s %s %s = %s. %s = <b>%s</b>." % (
            "Add" if op == "×" else "Subtract", num(m), "+" if op == "×" else "−", "(%s)" % num(n) if n < 0 else num(n), num(ex),
            pw(b, ex), val(v))
        wrong_ex = m * n if op == "×" else F(m, n) if n and m % n == 0 else n - m
        wr = [F(b) ** wrong_ex if isinstance(wrong_ex, int) or (isinstance(wrong_ex, F) and wrong_ex.denominator == 1) else None,
              F(b) ** (-ex), -v, F(b) * ex, v * b]
        its.append(mcq(q, (val(v), v), [(val(w), w) for w in wr if w is not None and abs(w) < 10 ** 9], e))
    for q, ans, wr, e in [
        ("Which expression equals 3<sup>−4</sup>?", "1/81", ["−81", "−12", "1/12"], "3⁻⁴ = 1 ÷ 3⁴ = 1 ÷ 81 = <b>1/81</b>."),
        ("A bacteria colony doubles each hour. It starts with 2<sup>3</sup> cells. After 5 hours it has 2<sup>3</sup> × 2<sup>5</sup> cells. How many is that?",
         "256", ["128", "2<sup>15</sup>", "64"], "2³ × 2⁵ = 2⁸ = <b>256</b>."),
        ("A screen has 10<sup>6</sup> pixels. A picture uses 10<sup>4</sup> of them. How many such pictures fill the screen?", "100",
         ["10,000", "1,000", "10"], "10⁶ ÷ 10⁴ = 10² = <b>100</b>."),
        ("Ana says 2<sup>3</sup> × 2<sup>4</sup> = 4<sup>7</sup>. What is the mistake?", "She multiplied the bases",
         ["She added the exponents", "Nothing, she is right", "She should subtract the exponents"],
         "Keep the base: 2³ × 2⁴ = 2⁷. <b>She multiplied the bases</b>."),
        ("Leo says (5<sup>2</sup>)<sup>3</sup> = 5<sup>5</sup>. What should it be?", "5<sup>6</sup>", ["5<sup>5</sup>", "5<sup>8</sup>", "25<sup>3</sup> = 5<sup>5</sup>"],
         "Power of a power: multiply 2 × 3 = 6. The answer is <b>5<sup>6</sup></b>."),
        ("Which is the same as 1/8?", "2<sup>−3</sup>", ["2<sup>3</sup>", "−2<sup>3</sup>", "8<sup>1</sup>"], "1/8 = 1 ÷ 2³ = <b>2<sup>−3</sup></b>."),
        ("Which is greater: 3<sup>−2</sup> or 2<sup>−3</sup>?", "2<sup>−3</sup>", ["3<sup>−2</sup>", "They are equal", "We cannot tell"],
         "3<sup>−2</sup> = 1/9 and 2<sup>−3</sup> = 1/8. 1/8 is greater than 1/9, so <b>2<sup>−3</sup></b> is greater."),
        ("What is 4<sup>3</sup> × 4<sup>−3</sup>?", "1", ["0", "16", "−1"], "4³ × 4⁻³ = 4⁰ = <b>1</b>."),
    ]:
        if ans == "1/81":
            ans = "<span class='fr'><span class='fn'>1</span><span class='fd'>81</span></span>"
            wr = ["−81", "−12", "<span class='fr'><span class='fn'>1</span><span class='fd'>12</span></span>"]
            e = "3⁻⁴ = 1 ÷ 3⁴ = 1 ÷ 81 = <b>%s</b>." % ans
        its.append(mcq(q, (ans, ans), [(w, w) for w in wr], e))
    o = its
    order = [o[0], o[12], o[1], o[17], o[2], o[13], o[3], o[18], o[4], o[14], o[5], o[19], o[6], o[15], o[7], o[16], o[8],
             o[9], o[10], o[11]]
    return {"title": "Evaluate expressions", "items": order}


def body():
    return ("<h2>The exponent rules</h2>"
            + table(["Rule", "Example"], [
                ["Multiply, same base: add exponents", "2<sup>3</sup> × 2<sup>4</sup> = 2<sup>7</sup>"],
                ["Divide, same base: subtract exponents", "5<sup>6</sup> ÷ 5<sup>2</sup> = 5<sup>4</sup>"],
                ["Power of a power: multiply exponents", "(3<sup>2</sup>)<sup>4</sup> = 3<sup>8</sup>"],
                ["Zero exponent", "7<sup>0</sup> = 1"],
                ["Negative exponent", "2<sup>−3</sup> = 1 ÷ 2<sup>3</sup> = 1/8"]])
            + example("Find the value of 3<sup>2</sup> × 3<sup>−5</sup>.", ["Add the exponents: 2 + (−5) = −3.",
                      "3<sup>−3</sup> = 1 ÷ 3<sup>3</sup> = 1 ÷ 27."], "1/27")
            + "<h2>Common mistakes</h2><ul><li>Multiplying the exponents when you multiply: 2³ × 2⁴ is 2⁷, not 2¹².</li>"
            "<li>Multiplying the bases: 2³ × 2⁴ is not 4⁷.</li>"
            "<li>Thinking a negative exponent makes a negative number: 2⁻³ = 1/8, not −8.</li>"
            "<li>Thinking 5⁰ = 0. It is 1.</li></ul>")


def main():
    sets = [set_product(), set_quotient(), set_power(), set_neg(), set_eval()]
    balance(sets, R)
    unit = {
        "slug": "exponent-rules",
        "title": "Exponent Rules: Product, Quotient, Zero and Negative Exponents",
        "seo_title": "Grade 8 Exponent Rules Worksheets: Product, Quotient, Power, Zero and Negative Exponents",
        "short_title": "Exponent rules",
        "domain": "Expressions & Equations",
        "standard_code": "8.EE.A.1",
        "standard_url": "https://www.thecorestandards.org/Math/Content/8/EE/A/1/",
        "standard_text": "Know and apply the properties of integer exponents to generate equivalent numerical expressions. For example, 3² × 3⁻⁵ = 3⁻³ = 1/3³ = 1/27.",
        "meta_desc": "Free Grade 8 exponent rules worksheets: multiply and divide powers with the same base, power of a power, zero and negative exponents, and evaluate expressions like 3² × 3⁻⁵. 100 questions with an answer key.",
        "key_big": "Same base: multiply → add exponents, divide → subtract, power of a power → multiply.",
        "key_sub": "Any nonzero number to the power 0 is 1. A negative exponent means 1 over the positive power.",
        "body_html": body(),
        "faq": [
            {"q": "What are the rules of exponents?", "a": "With the same base, add exponents when you multiply, subtract when you divide, and multiply when you raise a power to a power. a⁰ = 1 and a⁻ⁿ = 1/aⁿ."},
            {"q": "Why is any number to the zero power equal to 1?", "a": "Because aⁿ ÷ aⁿ = a⁰ by the quotient rule, and any nonzero number divided by itself is 1."},
            {"q": "Does a negative exponent make a number negative?", "a": "No. A negative exponent makes a fraction: 2⁻³ = 1/2³ = 1/8."},
            {"q": "Can I add exponents if the bases are different?", "a": "No. The rules only work for the same base. 2³ × 3⁴ cannot be combined into one power."}],
        "sets": sets, "pdf_url": "", "sort": 6, "updated": UPDATED,
    }
    write_unit("us", "math", "grade-8", unit)


if __name__ == "__main__":
    main()
