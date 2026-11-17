# -*- coding: utf-8 -*-
"""
UK Year 7 Maths: Order of Operations, BIDMAS (KS3 Number)
  python3 tools/gen_uk_maths_y7_order_of_operations.py
Multiplication and division before addition and subtraction, brackets, powers, negative numbers,
fraction bars, and placing brackets to make a statement true.
Wrong answers come from real mistakes: working left to right, adding before multiplying, and applying a
power to the product (3 × 2² read as 6²).
"""
import random
from fractions import Fraction as F
from uk_ks3 import num, par, mcq, B, S, make, lesson, collect, QN, T, fr, MINUS

R = random.Random(70301)


def show(tokens):
    out = []
    for i, t in enumerate(tokens):
        if isinstance(t, (int, F)):
            lead = i == 0 or tokens[i - 1] == "("
            out.append(num(t) if t >= 0 or lead else "(%s)" % num(t))
        else:
            out.append({"*": "×", "/": "÷", "-": MINUS}.get(t, t))
    s = " ".join(out)
    return s.replace("( ", "(").replace(" )", ")").replace(" ^ ", "^")


def ev(tokens):
    """BIDMAS value of a token list with + - * / ^ and brackets."""
    src = []
    for t in tokens:
        if isinstance(t, (int, F)):
            src.append("F(%d,%d)" % (F(t).numerator, F(t).denominator))
        else:
            src.append({"^": "**"}.get(t, t))
    return F(eval(" ".join(src), {"F": F}))


def ltr(tokens):
    """Strict left-to-right (brackets still first, powers ignored as a separate step)."""
    def inner(ts):
        # resolve brackets
        out, i = [], 0
        while i < len(ts):
            if ts[i] == "(":
                depth, j = 1, i + 1
                while depth:
                    depth += {"(": 1, ")": -1}.get(ts[j], 0) if isinstance(ts[j], str) else 0
                    j += 1
                out.append(inner(ts[i + 1:j - 1]))
                i = j
            else:
                out.append(ts[i])
                i += 1
        acc = F(out[0])
        k = 1
        while k < len(out):
            op, b = out[k], F(out[k + 1])
            if op == "+": acc += b
            elif op == "-": acc -= b
            elif op == "*": acc *= b
            elif op == "/":
                if b == 0: return None
                acc /= b
            elif op == "^": acc = acc ** int(b)
            k += 2
        return acc
    try:
        return inner(tokens)
    except Exception:
        return None


def pw(b, e):
    return "%s<sup>%d</sup>" % (num(b) if b >= 0 else "(%s)" % num(b), e)


def item(tokens, extra_wrong=(), html=None, why="", wr2=()):
    val = ev(tokens)
    if val.denominator != 1:
        return None
    w = [ltr(tokens)] + list(extra_wrong) + list(wr2)
    q = "Work out %s." % B(html or show(tokens))
    e = (why + " The answer is <b>%s</b>." % num(val)).strip()
    return QN(q, val, [x for x in w if x is not None and F(x).denominator == 1], e)


# ------------------------------------------------------------ set 1: × ÷ before + −
def one_md(r):
    a, b, c = r.randint(2, 20), r.randint(2, 9), r.randint(2, 9)
    form = r.randint(0, 3)
    if form == 0:
        t = [a, "+", b, "*", c]; why = "Multiply first: %d × %d = %d, then %d + %d." % (b, c, b * c, a, b * c)
        x = [a + b + c, a * b + c]
    elif form == 1:
        if a <= b * c: a += b * c
        t = [a, "-", b, "*", c]; why = "Multiply first: %d × %d = %d, then %d − %d." % (b, c, b * c, a, b * c)
        x = [a - b - c, a - b + c]
    elif form == 2:
        t = [a, "+", b * c, "/", c]; why = "Divide first: %d ÷ %d = %d, then %d + %d." % (b * c, c, b, a, b)
        x = [a + b * c - c, a + b * c * c]
    else:
        d = r.randint(2, 6)
        t = [b, "*", c, "-", d, "*", 2]; why = "Do both multiplications first: %d − %d." % (b * c, d * 2)
        x = [b * c - d + 2, b * (c - d) * 2]
    return item(t, x, why=why)


# ------------------------------------------------------------ set 2: brackets
def one_br(r):
    a, b, c = r.randint(2, 12), r.randint(2, 9), r.randint(2, 9)
    form = r.randint(0, 3)
    if form == 0:
        t = [c, "*", "(", a, "+", b, ")"]; why = "Brackets first: %d + %d = %d, then × %d." % (a, b, a + b, c)
        extra = [c * a + b, c + a + b]
    elif form == 1:
        if a - b < 2: a, b = b + a + 1, a
        t = ["(", a, "-", b, ")", "*", c]; why = "Brackets first: %d − %d = %d, then × %d." % (a, b, a - b, c)
        extra = [a - b * c, a * c - b]
    elif form == 2:
        s = b + c
        t = [s * a, "/", "(", b, "+", c, ")"]; why = "Brackets first: %d + %d = %d, then %d ÷ %d." % (b, c, s, s * a, s)
        extra = [F(s * a, b) + c]
    else:
        d = r.randint(1, 5)
        t = [a, "+", "(", b, "+", d, ")", "*", c]; why = "Brackets, then multiply, then add: %d + %d × %d." % (a, b + d, c)
        extra = [(a + b + d) * c, a + b + d * c]
    return item(t, extra, why=why)


# ------------------------------------------------------------ set 3: indices
def one_pow(r):
    b, e2 = r.randint(2, 6), r.choice([2, 2, 2, 3])
    if e2 == 3 and b > 5: b = r.randint(2, 4)
    a = r.randint(2, 9)
    form = r.randint(0, 3)
    p = b ** e2
    if form == 0:
        val = a * p; html = "%d × %s" % (a, pw(b, e2)); wr = [(a * b) ** e2, a * b * e2, a + p]
        why = "Powers before multiplying: %s = %d, then %d × %d." % (pw(b, e2), p, a, p)
    elif form == 1:
        val = a + p; html = "%d + %s" % (a, pw(b, e2)); wr = [(a + b) ** e2, a + b * e2, a * p]
        why = "Power first: %s = %d, then %d + %d." % (pw(b, e2), p, a, p)
    elif form == 2:
        c = r.randint(1, 4)
        val = (a + c) ** 2; html = "(%d + %d)<sup>2</sup>" % (a, c); wr = [a * a + c * c, a + c * c, (a + c) * 2]
        why = "Bracket first: %d + %d = %d, then %d<sup>2</sup>." % (a, c, a + c, a + c)
    else:
        c = r.randint(2, 5)
        if p - a * c <= 0: return None
        val = p - a * c; html = "%s %s %d × %d" % (pw(b, e2), MINUS, a, c); wr = [(p - a) * c, b * e2 - a * c, p - a + c]
        why = "Power first (%d), then multiply (%d), then subtract." % (p, a * c)
    q = "Work out %s." % B(html)
    return QN(q, val, wr, why + " The answer is <b>%s</b>." % num(val))


# ------------------------------------------------------------ set 4: negatives and fraction bars
def one_neg(r):
    form = r.randint(0, 3)
    if form == 0:
        a, b, c = r.randint(2, 9), -r.randint(2, 9), r.randint(2, 6)
        return item([a, "+", b, "*", c], [a - b * c, a + b + c], why="Multiply first: %s × %d = %s." % (num(b), c, num(b * c)))
    if form == 1:
        a, b = -r.randint(2, 6), r.randint(2, 9)
        val = a * a - b
        html = "%s %s %d" % (pw(a, 2), MINUS, b)
        return QN("Work out %s." % B(html), val, [-a * a - b, 2 * a - b, -val],
                  "(%s)<sup>2</sup> = %d (a negative squared is positive), then %d − %d. The answer is <b>%s</b>." % (num(a), a * a, a * a, b, num(val)))
    if form == 2:
        a, b, c = -r.randint(2, 9), r.randint(2, 8), r.randint(2, 8)
        return item(["(", a, "-", b, ")", "*", c], [(a + b) * c, a - b * c], why="Bracket first: %s − %d = %s." % (num(a), b, num(a - b)))
    top1, top2 = r.randint(4, 30), r.randint(2, 20)
    d1 = r.randint(2, 9)
    d2 = d1 + r.randint(2, 6)
    s = top1 + top2
    if s % (d2 - d1):
        return None
    val = F(s, d2 - d1)
    html = "%s" % fr("%d + %d" % (top1, top2), "%d %s %d" % (d2, MINUS, d1))
    wr = [F(top1, d2) + F(top2, 1) - d1, top1 + F(top2, d2) - d1, F(s, d2 + d1)]
    wr = [w for w in wr if w.denominator == 1]
    return QN("Work out %s." % B(html), val, wr,
              "A fraction bar works like brackets: top = %d, bottom = %d, so %d ÷ %d. The answer is <b>%s</b>." % (s, d2 - d1, s, d2 - d1, num(val)))


# ------------------------------------------------------------ set 5: brackets to make it true, and problems
def one_place(r):
    a, b, c, d = r.randint(2, 9), r.randint(2, 9), r.randint(2, 6), r.randint(1, 9)
    forms = [
        ([a, "+", b, "*", c], ["(", a, "+", b, ")", "*", c]),
        ([a, "*", b, "+", c], [a, "*", "(", b, "+", c, ")"]),
        ([a + b * c, "-", b, "*", c], ["(", a + b * c, "-", b, ")", "*", c]),
        ([a, "+", b, "*", c, "-", d], [a, "+", b, "*", "(", c, "-", d, ")"] if c > d else ["(", a, "+", b, ")", "*", c, "-", d]),
    ]
    plain, good = r.choice(forms)
    target = ev(good)
    if target == ev(plain) or target.denominator != 1 or target <= 0:
        return None
    # other bracket placements (all different value)
    n = len(plain)
    nums_idx = [i for i in range(0, n, 2)]
    alts = []
    for i in nums_idx:
        for j in nums_idx:
            if j <= i or (i == 0 and j == n - 1):
                continue
            t = plain[:i] + ["("] + plain[i:j + 1] + [")"] + plain[j + 1:]
            val = ev(t)
            if val != target and show(t) not in [show(x) for x in alts]:
                alts.append(t)
    alts.append(plain)
    if len(alts) < 3:
        return None
    r.shuffle(alts)
    q = "Where do the brackets go to make this true? %s = %s" % (B(show(plain)), B(num(target)))
    e = "%s: work out the bracket first. Check: it gives %s." % (B(show(good)), num(target))
    return T(q, show(good) + " = " + num(target), [show(t) + " = " + num(target) for t in alts[:3]], e)


def problems():
    its = []
    data = [
        ("A cinema ticket costs £8 and popcorn costs £3. Four friends each buy a ticket and popcorn. Which calculation gives the total cost?",
         "(8 + 3) × 4", ["8 + 3 × 4", "8 × 3 + 4", "8 + 3 + 4"], "Each friend pays 8 + 3, and there are 4 friends, so the bracket is needed: (8 + 3) × 4 = £44."),
        ("Leo buys 3 pens at 45p each and a ruler at 60p. Which calculation gives the total in pence?",
         "3 × 45 + 60", ["(3 + 45) × 60", "3 × (45 + 60)", "3 + 45 × 60"], "3 pens cost 3 × 45, then add the ruler: 3 × 45 + 60 = 195p."),
        ("A class of 30 pupils is split into teams of 6, and 2 more teams join from another class. Which calculation gives the number of teams?",
         "30 ÷ 6 + 2", ["30 ÷ (6 + 2)", "30 + 6 ÷ 2", "(30 + 2) ÷ 6"], "30 ÷ 6 = 5 teams, then add 2 more: 30 ÷ 6 + 2 = 7."),
        ("A rectangle is 7 cm long and 4 cm wide. Which calculation gives its perimeter?",
         "2 × (7 + 4)", ["2 × 7 + 4", "7 × 4 + 2", "7 + 4 × 2"], "Perimeter = 2 × (length + width) = 2 × 11 = 22 cm."),
        ("Grace had £50. She spent £12 and then shared the rest equally with her sister. Which calculation gives how much each gets?",
         "(50 − 12) ÷ 2", ["50 − 12 ÷ 2", "50 ÷ 2 − 12", "50 − 12 × 2"], "Take off the £12 first (bracket), then halve: (50 − 12) ÷ 2 = £19."),
        ("A taxi charges £3 plus £2 for every mile. Which calculation gives the cost of a 6-mile journey?",
         "3 + 2 × 6", ["(3 + 2) × 6", "3 × 2 + 6", "3 + 2 + 6"], "The £3 is paid once; the £2 is paid 6 times: 3 + 2 × 6 = £15."),
        ("The temperature was −4 °C. It rose by 3 °C each hour for 5 hours. Which calculation gives the new temperature?",
         "−4 + 3 × 5", ["(−4 + 3) × 5", "−4 × 3 + 5", "−4 + 3 + 5"], "The rise is 3 × 5 = 15 degrees, so −4 + 15 = 11 °C."),
        ("Which calculation has the answer 20?", "(2 + 3) × 4", ["2 + 3 × 4", "2 × 3 + 4", "2 + 3 + 4"], "(2 + 3) × 4 = 5 × 4 = 20. The others give 14, 10 and 9."),
    ]
    for q, a, w, e in data:
        its.append(T(q, a, w, e))
    for q, val, wr, e in [
        ("Ruby says 10 − 2 × 3 = 24. What is the correct answer?", 4, [24, 16, 18], "Multiply first: 2 × 3 = 6, then 10 − 6 = <b>4</b>. Ruby worked left to right."),
        ("Arjun says 2 × 3<sup>2</sup> = 36. What is the correct answer?", 18, [36, 12, 81], "Square first: 3<sup>2</sup> = 9, then 2 × 9 = <b>18</b>."),
        ("Work out 48 ÷ 4 × 2.", 24, [6, 96, 12], "Division and multiplication have equal priority, so go left to right: 48 ÷ 4 = 12, 12 × 2 = <b>24</b>."),
        ("Work out 20 − 8 + 5.", 17, [7, 3, 33], "Addition and subtraction have equal priority, so go left to right: 20 − 8 = 12, 12 + 5 = <b>17</b>."),
        ("Work out 36 ÷ (2 + 4) × 3.", 18, [2, 3, 108], "Bracket: 6. Then left to right: 36 ÷ 6 = 6, 6 × 3 = <b>18</b>."),
        ("Work out 5 + 3<sup>2</sup> × 2 − 4.", 19, [60, 28, 128], "3<sup>2</sup> = 9, 9 × 2 = 18, then 5 + 18 − 4 = <b>19</b>."),
        ("Work out 100 − 4 × (3 + 2)<sup>2</sup>.", 0, [2400, 96, 80], "(3 + 2)<sup>2</sup> = 25, 4 × 25 = 100, 100 − 100 = <b>0</b>."),
        ("Work out 7 × 8 − 6 ÷ 2.", 53, [25, 28, 50], "7 × 8 = 56 and 6 ÷ 2 = 3, then 56 − 3 = <b>53</b>."),
        ("Work out (−3)<sup>2</sup> + 4 × (−2).", 1, [-17, -10, 26], "(−3)<sup>2</sup> = 9 and 4 × (−2) = −8, so 9 − 8 = <b>1</b>."),
        ("Work out 6 + 18 ÷ 3<sup>2</sup>.", 8, [F(24, 9), 30, 12], "3<sup>2</sup> = 9, 18 ÷ 9 = 2, then 6 + 2 = <b>8</b>."),
        ("Work out 3 × (12 − 2 × 4).", 12, [40, 28, 60], "Inside the bracket, multiply first: 12 − 8 = 4. Then 3 × 4 = <b>12</b>."),
        ("Work out 2<sup>3</sup> + 3<sup>2</sup>.", 17, [12, 72, 11], "2<sup>3</sup> = 8 and 3<sup>2</sup> = 9, so 8 + 9 = <b>17</b>."),
    ]:
        its.append(QN(q, val, [w for w in wr if F(w).denominator == 1], e))
    return its


def body():
    return lesson(
        "<p>Use <b>BIDMAS</b> to decide what to do first:</p>"
        "<ol><li><b>B</b>rackets</li><li><b>I</b>ndices (powers and roots)</li><li><b>D</b>ivision and <b>M</b>ultiplication, left to right</li>"
        "<li><b>A</b>ddition and <b>S</b>ubtraction, left to right</li></ol>"
        "<p>A fraction bar acts like a bracket around the top and around the bottom.</p>",
        [("Work out 5 + 3 × 4.", ["Multiply first: 3 × 4 = 12.", "Then 5 + 12 = 17."], "17"),
         ("Work out 2 × 3².", ["Index first: 3² = 9.", "Then 2 × 9 = 18."], "18"),
         ("Work out 20 − 8 + 5.", ["+ and − have equal priority: go left to right.", "20 − 8 = 12, then 12 + 5 = 17."], "17")],
        ["Working left to right: 5 + 3 × 4 is not 8 × 4 = 32.",
         "Multiplying before the power: 2 × 3² is not 6² = 36.",
         "Doing addition before subtraction: 20 − 8 + 5 is 17, not 7. D and M (and A and S) have the same priority.",
         "Forgetting that (−3)² = 9 but −3² usually means −9."])


def main():
    sets = [S("Multiply and divide first", collect(one_md, 20, R)),
            S("Brackets first", collect(one_br, 20, R)),
            S("Indices (powers)", collect(one_pow, 20, R)),
            S("Negative numbers and fraction bars", collect(one_neg, 20, R)),
            S("Brackets, mistakes and problems", problems())]
    make(7, "order-of-operations", 3, "N",
         "Order of Operations: BIDMAS with Brackets and Powers",
         "Year 7 BIDMAS Worksheets: Order of Operations with Brackets, Indices and Negative Numbers",
         "Order of operations (BIDMAS)",
         "Use conventional notation for the priority of operations, including brackets, powers, roots and reciprocals.",
         "Free Year 7 BIDMAS worksheets: multiply and divide before adding, brackets first, powers, negative numbers, "
         "fraction bars and writing calculations for word problems. 100 questions with step-by-step answers.",
         "BIDMAS: Brackets, Indices, Division and Multiplication, Addition and Subtraction.",
         "D and M have equal priority, so do them left to right. The same is true for A and S.",
         body(),
         [("What does BIDMAS stand for?", "Brackets, Indices, Division, Multiplication, Addition, Subtraction. It tells you the order to do a calculation."),
          ("Is multiplication always before division?", "No. Multiplication and division have the same priority, so you work from left to right: 48 ÷ 4 × 2 = 24."),
          ("What is the difference between BIDMAS and BODMAS?", "Nothing. The O stands for Orders, another word for indices (powers)."),
          ("Why is 2 × 3² equal to 18 and not 36?", "The index is done before the multiplication: 3² = 9, then 2 × 9 = 18.")],
         sets, R)


if __name__ == "__main__":
    main()
