# -*- coding: utf-8 -*-
"""
Nigeria SSS 1–3 Mathematics: makers written for Nigeria (WAEC / NECO style).
Each maker takes a random.Random and returns one item; AssertionError means "draw again".
Negative numbers are passed to mcq as text ("−3"), because mcq drops negative ints.
"""
import math
from fractions import Fraction as F
from ng_common import mcq, comma, naira, fig
from ng_p4a import K, ch

M = "−"


def sn(x):
    """Signed number as text: −3, 2/5, −7/2."""
    x = F(x)
    s = M if x < 0 else ""
    x = abs(x)
    return s + (str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator))


def dec(x, p=2):
    s = ("%." + str(p) + "f") % x
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return s.replace("-", M)


def term(c, k, first=False, v="x"):
    """One term c·vᵏ with its sign: '3x²', ' − 5x', ' + 7'."""
    sup = {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}
    c = F(c)
    if c == 0:
        return ""
    a = abs(c)
    cs = "" if (a == 1 and k) else sn(a)
    vk = "" if k == 0 else v if k == 1 else v + sup.get(k, "^%d" % k)
    if a.denominator != 1 and k:
        body = ("" if a.numerator == 1 else str(a.numerator)) + vk + "/" + str(a.denominator)
    else:
        body = cs + vk
    if first:
        return (M if c < 0 else "") + body
    return (" " + M + " " if c < 0 else " + ") + body


def poly(cs, v="x"):
    """cs = {power: coefficient} -> '2x³ − x + 4'."""
    out = ""
    for k in sorted(cs, reverse=True):
        if cs[k] == 0:
            continue
        out += term(cs[k], k, first=not out, v=v)
    return out or "0"


# ============================================================ modular arithmetic
def mod_add(r):
    m = ch(r, [4, 5, 6, 7, 8, 9, 11, 12])
    a, b = r.randint(m, 40), r.randint(2, 30)
    ans = (a + b) % m
    return mcq("Find (%d + %d) mod %d." % (a, b, m), ans, [(a + b) // m, (ans + 1) % m, (ans + m - 1) % m, a + b - m, (a % m) * (b % m) % m],
               "%d + %d = %d. %d ÷ %d leaves a remainder of <b>%d</b>." % (a, b, a + b, a + b, m, ans), allow_zero=True)


def mod_sub(r):
    m = ch(r, [5, 6, 7, 8, 9, 11])
    a, b = r.randint(1, m - 1), r.randint(m, 3 * m)
    ans = (a - b) % m
    return mcq("Find (%d − %d) mod %d." % (a, b, m), ans, [(b - a) % m, (ans + 1) % m, (ans + m - 1) % m, abs(a - b) % m + 1],
               "%d − %d = %s. Add %d until the answer is between 0 and %d: the answer is <b>%d</b>." % (a, b, sn(a - b), m, m - 1, ans), allow_zero=True)


def mod_mul(r):
    m = ch(r, [5, 6, 7, 8, 9, 11, 12])
    a, b = r.randint(3, 25), r.randint(3, 15)
    ans = a * b % m
    return mcq("Evaluate %d × %d (mod %d)." % (a, b, m), ans, [(a + b) % m, (ans + 1) % m, a * b // m, (ans + 2) % m],
               "%d × %d = %d = %d × %d + %d, so the answer is <b>%d</b>." % (a, b, a * b, a * b // m, m, ans, ans), allow_zero=True)


def mod_solve(r):
    m = ch(r, [5, 7, 11])
    a = r.randint(2, m - 1)
    x = r.randint(1, m - 1)
    b = a * x % m
    others = [y for y in range(m) if y != x]
    r.shuffle(others)
    return mcq("Solve %dx ≡ %d (mod %d), where 0 ≤ x &lt; %d." % (a, b, m, m), x, others,
               "Try the values: %d × %d = %d, and %d ÷ %d leaves %d. So x = <b>%d</b>." % (a, x, a * x, a * x, m, b, x), allow_zero=True)


def mod_add_solve(r):
    m = ch(r, [5, 6, 7, 8, 9])
    x = r.randint(0, m - 1)
    a = r.randint(1, m - 1)
    b = (x + a) % m
    others = [y for y in range(m) if y != x]
    r.shuffle(others)
    return mcq("Solve x + %d ≡ %d (mod %d), where 0 ≤ x &lt; %d." % (a, b, m, m), x, others,
               "x = %d − %d = %s ≡ <b>%d</b> (mod %d)." % (b, a, sn(b - a), x, m), allow_zero=True)


DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def mod_day(r):
    d = r.randrange(7)
    n = r.randint(9, 200)
    ans = DAYS[(d + n) % 7]
    w = [DAYS[(d + n + 1) % 7], DAYS[(d + n - 1) % 7], DAYS[(d + n % 10) % 7] if DAYS[(d + n % 10) % 7] != ans else DAYS[(d + 3) % 7], DAYS[(d + 2 + n) % 7]]
    return mcq("Today is %s. What day of the week will it be in %d days?" % (DAYS[d], n), ans, w,
               "%d = 7 × %d + %d, so count on %d days from %s: <b>%s</b>." % (n, n // 7, n % 7, n % 7, DAYS[d], ans))


def mod_clock(r):
    h = r.randint(1, 12)
    n = r.randint(13, 100)
    ans = (h + n - 1) % 12 + 1
    w = [(ans % 12) + 1, (ans + 10) % 12 + 1, (h + n) % 24 or 24, (h + n % 10 - 1) % 12 + 1]
    return mcq("A clock shows %d o’clock. What will it show %d hours later?" % (h, n), "%d o’clock" % ans, ["%d o’clock" % x for x in w],
               "A clock works in mod 12. %d + %d = %d, and %d leaves %d after taking away twelves: <b>%d o’clock</b>." % (h, n, h + n, h + n, ans, ans))


def mod_table(r):
    m = ch(r, [4, 5, 6, 7])
    a, b = r.randint(1, m - 1), r.randint(1, m - 1)
    op = ch(r, ["+", "×"])
    ans = (a + b) % m if op == "+" else a * b % m
    return mcq("In the %s table for mod %d, what is the entry in the row for %d and the column for %d?" % ("addition" if op == "+" else "multiplication", m, a, b), ans,
               [a + b if op == "+" else a * b, (ans + 1) % m, (ans + m - 1) % m, a],
               "%d %s %d = %d, and %d mod %d = <b>%d</b>." % (a, op, b, a + b if op == "+" else a * b, a + b if op == "+" else a * b, m, ans), allow_zero=True)


# ============================================================ logarithms
def log_eval(r):
    b = ch(r, [2, 3, 4, 5, 10])
    k = r.randint(-2, 4) if b != 10 else r.randint(-3, 5)
    if k == 0:
        raise AssertionError
    n = F(b) ** k
    ns = sn(n) if n.denominator == 1 else ("1/%d" % n.denominator)
    if b == 10 and k < 0:
        ns = "0." + "0" * (-k - 1) + "1"
    base = "" if b == 10 else str(b).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    return mcq("Evaluate log%s %s." % (base, ns), sn(k), [sn(-k), sn(k + 1), sn(k - 1) if k - 1 else "1/%d" % b, sn(n / b) if n / b != k else sn(k * 2)],
               "%d to the power %s is %s, so the answer is <b>%s</b>." % (b, sn(k), ns, sn(k)))


def log_laws(r):
    kind = r.randrange(3)
    if kind == 0:
        a, b = r.sample([2, 4, 5, 20, 25, 50, 8, 125], 2)
        p = a * b
        k = round(math.log10(p))
        if 10 ** k != p:
            raise AssertionError
        return mcq("Simplify log %d + log %d." % (a, b), str(k), [str(k + 1), "log %d" % (a + b), str(k - 1) if k > 1 else "10"],
                   "log a + log b = log ab = log %d = <b>%d</b>." % (p, k))
    if kind == 1:
        p = ch(r, [100, 1000, 10000])
        b = ch(r, [2, 4, 5, 8, 20, 25, 40, 50])
        a = p * b
        k = round(math.log10(p))
        return mcq("Simplify log %s − log %d." % (comma(a), b), str(k), ["log %s" % comma(a - b), str(k + 1), str(k - 1)],
                   "log a − log b = log (a ÷ b) = log %s = <b>%d</b>." % (comma(p), k))
    b = ch(r, [2, 3, 5])
    n = r.randint(2, 4)
    m = r.randint(2, 4)
    sub = str(b).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    return mcq("Simplify %d log%s %d." % (m, sub, b ** n), str(m * n), [str(m + n), str(n), str(m * b ** n)],
               "log%s %d = %d, so %d × %d = <b>%d</b>." % (sub, b ** n, n, m, n, m * n))


def log_given(r):
    """Given log 2 = 0.3010 and log 3 = 0.4771, find the log of another number."""
    L = {2: 0.3010, 3: 0.4771}
    opts = [(4, "log 4 = 2 log 2", 2 * L[2]), (6, "log 6 = log 2 + log 3", L[2] + L[3]), (8, "log 8 = 3 log 2", 3 * L[2]), (9, "log 9 = 2 log 3", 2 * L[3]),
            (12, "log 12 = 2 log 2 + log 3", 2 * L[2] + L[3]), (18, "log 18 = log 2 + 2 log 3", L[2] + 2 * L[3]), (5, "log 5 = log 10 − log 2", 1 - L[2]),
            (15, "log 15 = log 3 + log 10 − log 2", L[3] + 1 - L[2]), (20, "log 20 = log 2 + log 10", L[2] + 1), (30, "log 30 = log 3 + log 10", L[3] + 1),
            (1.5, "log 1.5 = log 3 − log 2", L[3] - L[2]), (0.2, "log 0.2 = log 2 − log 10", L[2] - 1), (24, "log 24 = 3 log 2 + log 3", 3 * L[2] + L[3]),
            (27, "log 27 = 3 log 3", 3 * L[3]), (16, "log 16 = 4 log 2", 4 * L[2]), (36, "log 36 = 2 log 2 + 2 log 3", 2 * L[2] + 2 * L[3]),
            (45, "log 45 = 2 log 3 + log 10 − log 2", 2 * L[3] + 1 - L[2]), (0.6, "log 0.6 = log 2 + log 3 − log 10", L[2] + L[3] - 1)]
    n, how, v = ch(r, opts)
    f = lambda x: ("%.4f" % x).replace("-", M)
    w = [f(L[2] * L[3]), f(v + 0.3010), f(v - 0.4771), f(v * 2), f(-v), f(v + 1)]
    return mcq("Given that log 2 = 0.3010 and log 3 = 0.4771, find log %s." % (dec(n, 1) if isinstance(n, float) else n), f(v), [x for x in w if x != f(v)],
               "%s = <b>%s</b>." % (how, f(v)))


def log_solve(r):
    kind = r.randrange(3)
    if kind == 0:
        b = ch(r, [2, 3, 4, 5, 6, 7])
        n = r.randint(2, 4 if b < 6 else 3)
        return mcq("Solve log<sub>x</sub> %d = %d." % (b ** n, n), "x = %d" % b, ["x = %d" % (b ** n // n) if b ** n % n == 0 and b ** n // n != b else "x = %d" % (b + 1), "x = %d" % (b ** n * n), "x = %d" % (b * n)],
                   "x<sup>%d</sup> = %d, and %d<sup>%d</sup> = %d, so <b>x = %d</b>." % (n, b ** n, b, n, b ** n, b))
    if kind == 1:
        b = ch(r, [2, 3, 5])
        n = r.randint(2, 5)
        sub = str(b).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
        return mcq("Solve log%s x = %d." % (sub, n), "x = %s" % comma(b ** n), ["x = %d" % (b * n), "x = %d" % (n ** b), "x = %s" % comma(b ** (n + 1))],
                   "x = %d<sup>%d</sup> = <b>%s</b>." % (b, n, comma(b ** n)))
    a = r.randint(2, 9)
    k = ch(r, [1, 2])
    x = 10 ** k // a if (10 ** k) % a == 0 else None
    if not x:
        raise AssertionError
    return mcq("Solve log x + log %d = %d." % (a, k), "x = %d" % x, ["x = %d" % (10 ** k - a), "x = %d" % (x * 10), "x = %d" % (k * a)],
               "log %dx = %d, so %dx = %s and <b>x = %d</b>." % (a, k, a, comma(10 ** k), x))


def log_exp(r):
    """Change between index form and log form."""
    b = ch(r, [2, 3, 4, 5, 10])
    n = r.randint(2, 4)
    v = b ** n
    if n == b or b ** n == n ** b:
        raise AssertionError
    sub = "" if b == 10 else str(b).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    if r.random() < 0.5:
        return mcq("Write the equation %d<sup>%d</sup> = %s as a logarithm." % (b, n, comma(v)), "log%s %s = %d" % (sub, comma(v), n),
                   ["log%s %d = %s" % (sub, n, comma(v)), "log<sub>%d</sub> %d = %s" % (n, b, comma(v)), "log%s %d = %d" % (sub, b, n)],
                   "b<sup>n</sup> = N means log<sub>b</sub> N = n: <b>log%s %s = %d</b>." % (sub, comma(v), n))
    return mcq("Write the equation log%s %s = %d as a power (index form)." % (sub, comma(v), n), "%d<sup>%d</sup> = %s" % (b, n, comma(v)),
               ["%d<sup>%d</sup> = %d" % (n, b, v) if n ** b != v else "%d × %d = %d" % (b, n, b * n), "%s<sup>%d</sup> = %d" % (comma(v), n, b), "%d<sup>%s</sup> = %d" % (b, comma(v), n)],
               "log<sub>b</sub> N = n means b<sup>n</sup> = N: <b>%d<sup>%d</sup> = %s</b>." % (b, n, comma(v)))


# ============================================================ logical reasoning
STMT = [("it rains", "the ground is wet"), ("a number is even", "it is divisible by 2"), ("Ada studies hard", "she will pass the examination"),
        ("a shape is a square", "it has four equal sides"), ("you are in Kano", "you are in Nigeria"), ("the light is red", "the cars stop"),
        ("Musa eats too much", "he will be ill"), ("a triangle has three equal sides", "it is equilateral"), ("the market is open", "Tola will buy yams"),
        ("x = 3", "x² = 9"), ("a number ends in 0", "it is divisible by 5"), ("the generator is on", "the fan is working"),
        ("Chidi is late", "he will miss the bus"), ("a number is a multiple of 6", "it is a multiple of 3"), ("it is Sunday", "the shop is closed"),
        ("the water boils", "it is hot"), ("Ngozi practises every day", "she will win the race"), ("a polygon is a hexagon", "it has six sides"),
        ("the fuel tank is empty", "the car will stop"), ("Bayo saves money", "he can buy a phone"), ("an angle is 90°", "it is a right angle")]
NEG = [("The door is open.", "The door is not open."), ("Ada is tall.", "Ada is not tall."), ("All boys like football.", "Some boys do not like football."),
       ("Some girls play chess.", "No girl plays chess."), ("7 is a prime number.", "7 is not a prime number."), ("The sun is hot.", "The sun is not hot."),
       ("Every pupil passed the test.", "At least one pupil did not pass the test."), ("No fish can fly.", "Some fish can fly."), ("x is greater than 5.", "x is less than or equal to 5."),
       ("Lagos is a big city.", "Lagos is not a big city."), ("All triangles have three sides.", "Some triangles do not have three sides."), ("The bus is full.", "The bus is not full."),
       ("All mangoes are sweet.", "Some mangoes are not sweet."), ("Some teachers are strict.", "No teacher is strict."), ("Every road in the town is tarred.", "At least one road in the town is not tarred."),
       ("9 is an even number.", "9 is not an even number."), ("Kemi can swim.", "Kemi cannot swim."), ("x is less than 4.", "x is greater than or equal to 4."),
       ("All squares are rectangles.", "Some squares are not rectangles."), ("No student is absent today.", "Some students are absent today."), ("The river is deep.", "The river is not deep.")]


def lg_neg(r):
    p, n = ch(r, NEG)
    wrong = {"All boys like football.": ["No boy likes football.", "Some boys like football.", "All girls like football."],
             "Some girls play chess.": ["Some girls do not play chess.", "All girls play chess.", "Some boys play chess."],
             "Every pupil passed the test.": ["No pupil passed the test.", "Some pupils passed the test.", "Every pupil failed the test."],
             "No fish can fly.": ["All fish can fly.", "No fish can swim.", "Some fish cannot fly."],
             "x is greater than 5.": ["x is less than 5.", "x is greater than or equal to 5.", "x is equal to 5."],
             "All triangles have three sides.": ["No triangle has three sides.", "All triangles have four sides.", "Some triangles have three sides."],
             "All mangoes are sweet.": ["No mango is sweet.", "Some mangoes are sweet.", "All mangoes are sour."],
             "Some teachers are strict.": ["Some teachers are not strict.", "All teachers are strict.", "Some pupils are strict."],
             "Every road in the town is tarred.": ["No road in the town is tarred.", "Some roads in the town are tarred.", "Every road in the town is new."],
             "x is less than 4.": ["x is greater than 4.", "x is less than or equal to 4.", "x is equal to 4."],
             "All squares are rectangles.": ["No square is a rectangle.", "All rectangles are squares.", "Some squares are rectangles."],
             "No student is absent today.": ["All students are absent today.", "No student is present today.", "Some students are not absent today."]}
    w = wrong.get(p, [p.replace(" is ", " is always ", 1), "It is not true that " + p[0].lower() + p[1:-1] + " sometimes.", p.replace(".", " today.")])
    return mcq("What is the negation of the statement: “%s”" % p, n, w, "The negation is true exactly when the statement is false: <b>%s</b>" % n)


def lg_parts(r):
    a, b = ch(r, STMT)
    kind = r.randrange(3)
    s = "If %s, then %s." % (a, b)
    if kind == 0:
        ans = "If %s, then %s." % (b, a)
        w = ["If %s, then %s." % (_not(a), _not(b)), "If %s, then %s." % (_not(b), _not(a)), s]
        name = "converse"
        e = "The converse swaps the two parts: <b>%s</b>" % ans
    elif kind == 1:
        ans = "If %s, then %s." % (_not(b), _not(a))
        w = ["If %s, then %s." % (b, a), "If %s, then %s." % (_not(a), _not(b)), s]
        name = "contrapositive"
        e = "The contrapositive swaps the parts and makes both negative: <b>%s</b>" % ans
    else:
        ans = "If %s, then %s." % (_not(a), _not(b))
        w = ["If %s, then %s." % (b, a), "If %s, then %s." % (_not(b), _not(a)), s]
        name = "inverse"
        e = "The inverse makes both parts negative without swapping them: <b>%s</b>" % ans
    return mcq("Statement: “%s” Which is its <b>%s</b>?" % (s, name), ans, w, e)


def _not(s):
    rules = [(" is even", " is not even"), (" is divisible", " is not divisible"), (" studies hard", " does not study hard"), (" will pass", " will not pass"),
             (" is a square", " is not a square"), (" has four", " does not have four"), (" are in ", " are not in "), (" is red", " is not red"), (" stop", " do not stop"),
             (" eats too much", " does not eat too much"), (" will be ill", " will not be ill"), (" has three", " does not have three"), (" is equilateral", " is not equilateral"),
             (" is open", " is not open"), (" will buy", " will not buy"), ("x = 3", "x ≠ 3"), ("x² = 9", "x² ≠ 9"), (" ends in", " does not end in"),
             (" is on", " is not on"), (" is working", " is not working"), (" is late", " is not late"), (" will miss", " will not miss"), (" is a multiple", " is not a multiple"),
             (" is Sunday", " is not Sunday"), (" is closed", " is not closed"), (" rains", " does not rain"), (" is wet", " is not wet"),
             (" boils", " does not boil"), (" is hot", " is not hot"), (" practises", " does not practise"), (" will win", " will not win"), (" is a hexagon", " is not a hexagon"),
             (" has six", " does not have six"), (" is empty", " is not empty"), (" will stop", " will not stop"), (" saves", " does not save"), (" can buy", " cannot buy"),
             (" is 90°", " is not 90°"), (" is a right angle", " is not a right angle")]
    for a, b in rules:
        if a in s:
            return s.replace(a, b, 1)
    raise AssertionError(s)


TT = {"p ∧ q": lambda p, q: p and q, "p ∨ q": lambda p, q: p or q, "p ⇒ q": lambda p, q: (not p) or q, "p ⇔ q": lambda p, q: p == q, "~p ∧ q": lambda p, q: (not p) and q,
      "p ∨ ~q": lambda p, q: p or not q, "~(p ∧ q)": lambda p, q: not (p and q), "~p ⇒ q": lambda p, q: p or q}


def lg_truth(r):
    f = ch(r, sorted(TT))
    p, q = r.random() < 0.5, r.random() < 0.5
    v = TT[f](p, q)
    T = lambda x: "T" if x else "F"
    mean = {"∧": "and", "∨": "or", "⇒": "implies", "⇔": "if and only if"}
    return mcq("p is %s and q is %s. What is the truth value of %s?" % ("true" if p else "false", "true" if q else "false", f),
               "%s (%s)" % (T(v), "true" if v else "false"), ["%s (%s)" % (T(not v), "true" if not v else "false"), "It cannot be found", "Both T and F"],
               "Put p = %s and q = %s into %s: the result is <b>%s</b>. (∧ is and, ∨ is or, ⇒ is implies, ~ is not.)" % (T(p), T(q), f, "true" if v else "false"))


SYL = [("All mammals breathe air. A goat is a mammal.", "A goat breathes air.", ["All animals that breathe air are goats.", "A goat is not a mammal.", "Some mammals do not breathe air."]),
       ("All pupils in SSS 1 wear uniforms. Bola is in SSS 1.", "Bola wears a uniform.", ["Everyone who wears a uniform is in SSS 1.", "Bola is not a pupil.", "Bola does not wear a uniform."]),
       ("Every square is a rectangle. PQRS is a square.", "PQRS is a rectangle.", ["Every rectangle is a square.", "PQRS is not a rectangle.", "PQRS is a triangle."]),
       ("All prime numbers greater than 2 are odd. 13 is a prime number greater than 2.", "13 is odd.", ["13 is even.", "All odd numbers are prime.", "13 is not prime."]),
       ("If it rains, the match is cancelled. It rains.", "The match is cancelled.", ["The match is played.", "It does not rain.", "The match is moved to the morning."]),
       ("If the price rises, people buy less. People did not buy less.", "The price did not rise.", ["The price rose.", "People bought more.", "Nothing can be said."]),
       ("No reptile has feathers. A lizard is a reptile.", "A lizard has no feathers.", ["A lizard has feathers.", "All animals without feathers are lizards.", "A lizard is a bird."]),
       ("All doctors studied for many years. Dr Eze is a doctor.", "Dr Eze studied for many years.", ["Dr Eze did not study.", "Everyone who studies is a doctor.", "Dr Eze is a teacher."]),
       ("If a number is divisible by 9, it is divisible by 3. 54 is divisible by 9.", "54 is divisible by 3.", ["54 is not divisible by 3.", "Every number divisible by 3 is divisible by 9.", "54 is prime."]),
       ("All metals conduct electricity. Copper is a metal.", "Copper conducts electricity.", ["All things that conduct electricity are copper.", "Copper is not a metal.", "Copper does not conduct electricity."]),
       ("If Emeka passes WAEC, he will go to university. Emeka did not go to university.", "Emeka did not pass WAEC.", ["Emeka passed WAEC.", "Emeka went to university.", "Nothing can be said."]),
       ("Every rhombus has four equal sides. ABCD is a rhombus.", "ABCD has four equal sides.", ["ABCD has three sides.", "Every shape with four equal sides is ABCD.", "ABCD has no equal sides."]),
       ("All birds have feathers. A parrot is a bird.", "A parrot has feathers.", ["All animals with feathers are parrots.", "A parrot has no feathers.", "A parrot is not a bird."]),
       ("If the generator has no fuel, it will not work. The generator is working.", "The generator has fuel.", ["The generator has no fuel.", "The generator is not working.", "Nothing can be said."]),
       ("No even number greater than 2 is prime. 18 is an even number greater than 2.", "18 is not prime.", ["18 is prime.", "18 is odd.", "All numbers that are not prime are even."]),
       ("All pupils who pass get a certificate. Ada did not get a certificate.", "Ada did not pass.", ["Ada passed.", "Ada got a certificate.", "Everyone who gets a certificate is Ada."]),
       ("If a shape is a cube, it has 6 faces. Box Q is a cube.", "Box Q has 6 faces.", ["Box Q has 8 faces.", "Every shape with 6 faces is a cube.", "Box Q is not a cube."]),
       ("All civil servants in Abuja work on Monday. Mr Bello is a civil servant in Abuja.", "Mr Bello works on Monday.", ["Mr Bello does not work on Monday.", "Everyone who works on Monday is a civil servant.", "Mr Bello lives in Kano."])]


def lg_valid(r):
    p, c, w = ch(r, SYL)
    return mcq("Premises: %s What is a valid conclusion?" % p, c, w, "The conclusion must follow from the premises: <b>%s</b>" % c)


# ============================================================ approximation and percentage error
def pe_basic(r):
    k = K(r)
    actual = r.randint(20, 400)
    err = ch(r, [1, 2, 4, 5, 8, 10])
    if err * 100 % actual and (err * 1000) % actual:
        raise AssertionError
    meas = actual + ch(r, [err, -err])
    pct = F(err * 100, actual)
    if pct.denominator not in (1, 2, 4, 5, 10):
        raise AssertionError
    pv = dec(float(pct), 2)
    w = [dec(float(F(err * 100, meas)), 2), dec(float(pct) * 2, 2), dec(float(pct) / 10, 2), str(err)]
    return mcq("%s measured a length as %d cm. The actual length is %d cm. Find the percentage error." % (k["n"], meas, actual), pv + "%", [x + "%" for x in w if x != pv],
               "Error = %d cm. Percentage error = %d ÷ %d × 100 = <b>%s%%</b>." % (err, err, actual, pv))


def pe_limits(r):
    v = r.randint(12, 95)
    u = ch(r, [("cm", 1), ("kg", 1), ("m", 1)])
    lo, hi = v - 0.5, v + 0.5
    return mcq("A length is %d %s to the nearest %s. Between which limits does it lie?" % (v, u[0], u[0][:-1] if u[0] == "cm" else u[0]) if False else
               "A quantity is given as %d %s, correct to the nearest %s. What are its lower and upper limits?" % (v, u[0], {"cm": "centimetre", "kg": "kilogram", "m": "metre"}[u[0]]),
               "%s %s and %s %s" % (dec(lo, 1), u[0], dec(hi, 1), u[0]), ["%d %s and %d %s" % (v - 1, u[0], v + 1, u[0]), "%s %s and %s %s" % (dec(v - 0.05, 2), u[0], dec(v + 0.05, 2), u[0]), "%d %s and %d %s" % (v, u[0], v + 1, u[0])],
               "The greatest possible error is half the unit, 0.5 %s: <b>%s %s to %s %s</b>." % (u[0], dec(lo, 1), u[0], dec(hi, 1), u[0]))


def pe_max(r):
    v = ch(r, [2.5, 4, 5, 8, 10, 12.5, 20, 25, 40, 50])
    pct = F(5, 1) / F(str(v))
    pv = dec(float(pct), 4)
    return mcq("A mass is measured as %.1f kg, correct to the nearest 0.1 kg. Find the percentage error." % v, pv + "%",
               [dec(float(pct * 2), 4) + "%", dec(float(pct * 10), 4) + "%", dec(float(pct / 10), 5) + "%"],
               "Greatest possible error = 0.05 kg. Percentage error = 0.05 ÷ %.1f × 100 = <b>%s%%</b>." % (v, pv))


def pe_sf(r):
    x = r.randint(10000, 999999) / ch(r, [1, 10, 100, 1000, 10000])
    n = ch(r, [2, 3, 4])
    d = n - 1 - math.floor(math.log10(abs(x)))
    v = round(x, d)
    s = ("%." + str(max(d, 0)) + "f") % v
    if d < 0:
        s = comma(int(round(x, d)))
    if s.replace(",", "").replace(".", "").lstrip("0")[:n] == str(int(x * 10 ** max(d, 0)))[:n] and False:
        pass
    trunc = ("%." + str(max(d, 0)) + "f") % (math.floor(x * 10 ** d) / 10 ** d) if d >= 0 else comma(int(math.floor(x * 10 ** d) / 10 ** d))
    alt = ("%." + str(max(d + 1, 0)) + "f") % round(x, d + 1) if d + 1 >= 0 else comma(int(round(x, d + 1)))
    alt2 = ("%." + str(max(d - 1, 0)) + "f") % round(x, d - 1) if d - 1 >= 0 else comma(int(round(x, d - 1)))
    xs = (("%.6f" % x).rstrip("0").rstrip(".")) if x != int(x) else comma(int(x))
    w = [trunc, alt, alt2]
    if s in w[:1]:
        w[0] = ("%." + str(max(d, 0)) + "f") % (v + 10 ** -d) if d >= 0 else comma(int(v + 10 ** -d))
    return mcq("Write %s correct to %d significant figures." % (xs if x == int(x) else xs, n), s, w,
               "Keep %d significant figures and look at the next digit to round: <b>%s</b>." % (n, s))


# ============================================================ simultaneous linear and quadratic equations
def lq_solve(r):
    a, b = r.sample(range(-4, 6), 2)
    a, b = min(a, b), max(a, b)
    # y = x² + px + q meets y = mx + c at x = a, b:  x² + (p − m)x + (q − c) = 0 with roots a, b
    m = r.randint(-3, 3)
    c = r.randint(-5, 5)
    p = m - (a + b)
    q = c + a * b
    ya, yb = m * a + c, m * b + c
    quad = poly({2: 1, 1: p, 0: q})
    lin = poly({1: m, 0: c}) if m else str(sn(c))
    pt = lambda x, y: "(%s, %s)" % (sn(x), sn(y))
    ans = "%s and %s" % (pt(a, ya), pt(b, yb))
    w = ["%s and %s" % (pt(-a, ya), pt(-b, yb)), "%s and %s" % (pt(a, yb), pt(b, ya)), "%s and %s" % (pt(a, ya + 1), pt(b, yb + 1)) if a != b else ""]
    return mcq("Solve the simultaneous equations y = %s and y = %s." % (quad, lin), ans, [x for x in w if x and x != ans],
               "Put them equal: %s = 0, so x = %s or x = %s. Then y = %s: <b>%s</b>." % (poly({2: 1, 1: p - m, 0: q - c}), sn(a), sn(b), lin, ans))


def lq_sum(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    if a == b:
        raise AssertionError
    s, p = a + b, a * b
    return mcq("Solve x + y = %d and xy = %d." % (s, p), "x = %d, y = %d or x = %d, y = %d" % (min(a, b), max(a, b), max(a, b), min(a, b)),
               ["x = %d, y = %d only" % (min(a, b), max(a, b)), "x = %d, y = %d or x = %d, y = %d" % (min(a, b) + 1, max(a, b) - 1, max(a, b) - 1, min(a, b) + 1) if (min(a, b) + 1) * (max(a, b) - 1) != p else "x = %d, y = %d" % (s, 0),
                "x = %d, y = %d or x = %d, y = %d" % (-min(a, b), -max(a, b), -max(a, b), -min(a, b))],
               "y = %d − x, so x(%d − x) = %d, x² − %dx + %d = 0, (x − %d)(x − %d) = 0. <b>x = %d, y = %d or x = %d, y = %d</b>." % (s, s, p, s, p, a, b, min(a, b), max(a, b), max(a, b), min(a, b)))


def lq_line_circle(r):
    pts = [(3, 4), (4, 3), (0, 5), (5, 0), (-3, 4), (3, -4), (-4, 3), (4, -3)]
    p1, p2 = r.sample(pts, 2)
    if p1[0] == p2[0]:
        raise AssertionError
    m = F(p2[1] - p1[1], p2[0] - p1[0])
    c = p1[1] - m * p1[0]
    if m.denominator != 1 or c.denominator != 1:
        raise AssertionError
    lin = poly({1: m, 0: c}) if m else sn(c)
    s = sorted([p1, p2])
    pt = lambda x, y: "(%s, %s)" % (sn(x), sn(y))
    ans = "%s and %s" % (pt(*s[0]), pt(*s[1]))
    w = ["%s and %s" % (pt(-s[0][0], s[0][1]), pt(-s[1][0], s[1][1])), "%s and %s" % (pt(s[0][1], s[0][0]), pt(s[1][1], s[1][0])), "%s and %s" % (pt(s[0][0], -s[0][1]), pt(s[1][0], -s[1][1]))]
    return mcq("Find where the line y = %s meets the circle x² + y² = 25." % lin, ans, [x for x in w if x != ans],
               "Put y = %s into x² + y² = 25 and solve the quadratic in x: <b>%s</b>." % (lin, ans))


# ============================================================ differentiation
def _rpoly(r, deg=3):
    cs = {k: r.choice([c for c in range(-6, 7) if c]) for k in range(deg + 1) if r.random() < 0.8 or k == deg}
    return cs


def d_power(r):
    cs = _rpoly(r, r.randint(2, 4))
    d = {k - 1: c * k for k, c in cs.items() if k}
    if not d:
        raise AssertionError
    ans = poly(d)
    w1 = poly({k: c * k for k, c in cs.items() if k})
    w2 = poly({k - 1: c for k, c in cs.items() if k})
    w3 = poly({**d, 0: d.get(0, 0) + cs.get(0, 0)}) if cs.get(0) else poly({k - 1: c * (k - 1) for k, c in cs.items() if k > 1} or {0: 1})
    return mcq("Find dy/dx if y = %s." % poly(cs), ans, [w for w in (w1, w2, w3) if w != ans] + [poly({k - 1: -c * k for k, c in cs.items() if k})],
               "Multiply by the power, then take 1 from the power: <b>dy/dx = %s</b>." % ans)


def d_point(r):
    cs = _rpoly(r, r.randint(2, 3))
    x = r.randint(-3, 3)
    g = sum(c * k * x ** (k - 1) for k, c in cs.items() if k)
    yv = sum(c * x ** k for k, c in cs.items())
    return mcq("Find the gradient of the curve y = %s at the point where x = %s." % (poly(cs), sn(x)), sn(g), [sn(yv) if yv != g else sn(g + 2), sn(g + 1), sn(-g) if g else "1", sn(g - 2)],
               "dy/dx = %s. Put x = %s: <b>%s</b>." % (poly({k - 1: c * k for k, c in cs.items() if k}), sn(x), sn(g)))


def d_stat(r):
    kind = r.randrange(2)
    if kind == 0:
        a = ch(r, [1, 2, 3, -1, -2])
        h = r.randint(-4, 4)
        k = r.randint(-6, 6)
        cs = {2: a, 1: -2 * a * h, 0: a * h * h + k}
        ans = "(%s, %s), a %s point" % (sn(h), sn(k), "minimum" if a > 0 else "maximum")
        return mcq("Find the turning point of y = %s and say whether it is a maximum or a minimum." % poly(cs), ans,
                   ["(%s, %s), a %s point" % (sn(h), sn(k), "maximum" if a > 0 else "minimum"), "(%s, %s), a %s point" % (sn(-h), sn(k), "minimum" if a > 0 else "maximum"), "(%s, %s), a %s point" % (sn(h), sn(cs[0]), "minimum" if a > 0 else "maximum")],
                   "dy/dx = %s = 0 gives x = %s, and y = %s. d²y/dx² = %s is %s, so it is a <b>%s</b>." % (poly({1: 2 * a, 0: -2 * a * h}), sn(h), sn(k), sn(2 * a), "positive" if a > 0 else "negative", "minimum" if a > 0 else "maximum"))
    p, q = r.sample(range(-3, 4), 2)
    p, q = min(p, q), max(p, q)
    # y' = 3(x − p)(x − q) -> y = x³ − 3/2 (p+q)x² + 3pq x + c ; need even p+q
    if (p + q) % 2:
        raise AssertionError
    c = r.randint(-5, 5)
    cs = {3: 1, 2: F(-3 * (p + q), 2), 1: 3 * p * q, 0: c}
    ans = {p, q}
    pairs = [(-p, -q), (p, p + q) if p + q not in (p, q) else (p, q + 1), (3 * p, 3 * q), (p + 1, q + 1), (0, p + q)]
    w = []
    for a_, b_ in pairs:
        if {a_, b_} != ans and a_ != b_ and "x = %s and x = %s" % (sn(min(a_, b_)), sn(max(a_, b_))) not in w:
            w.append("x = %s and x = %s" % (sn(min(a_, b_)), sn(max(a_, b_))))
    w.append("x = %s only" % sn(q))
    return mcq("At which values of x does y = %s have stationary points?" % poly(cs), "x = %s and x = %s" % (sn(p), sn(q)), w,
               ("dy/dx = %s = 3(x − %s)(x − %s) = 0, so <b>x = %s and x = %s</b>." % (poly({2: 3, 1: -3 * (p + q), 0: 3 * p * q}), sn(p), sn(q), sn(p), sn(q))).replace("− −", "+ ").replace("(x − 0)", "x"))


def d_tangent(r):
    a = ch(r, [1, 2, 3, -1])
    b, c = r.randint(-4, 4), r.randint(-5, 5)
    x0 = r.randint(-2, 3)
    y0 = a * x0 * x0 + b * x0 + c
    m = 2 * a * x0 + b
    k = y0 - m * x0
    eq = "y = " + (poly({1: m, 0: k}) if m else sn(k))
    return mcq("Find the equation of the tangent to y = %s at the point (%s, %s)." % (poly({2: a, 1: b, 0: c}), sn(x0), sn(y0)), eq,
               ["y = " + poly({1: m + 1, 0: k - x0}) if m + 1 else "y = " + sn(k), "y = " + poly({1: y0, 0: m}) if y0 else "y = " + sn(m) + "x", "y = " + poly({1: m, 0: k + 2}) if m else "y = " + sn(k + 2)],
               "Gradient = dy/dx at x = %s = %s. Use y − y₁ = m(x − x₁) with the point (%s, %s): <b>%s</b>." % (sn(x0), sn(m), sn(x0), sn(y0), eq))


def d_motion(r):
    a, b, c = r.randint(1, 4), r.randint(1, 10), r.randint(0, 12)
    t = r.randint(1, 5)
    kind = r.randrange(2)
    s = poly({2: a, 1: b, 0: c}, v="t") if r.random() < 0.6 else poly({3: 1, 1: b, 0: c}, v="t")
    if "³" in s:
        v = 3 * t * t + b
        acc = 6 * t
        ds = "3t² + %d" % b
        dds = "6t"
    else:
        v = 2 * a * t + b
        acc = 2 * a
        ds = poly({1: 2 * a, 0: b}, v="t")
        dds = str(2 * a)
    if kind == 0:
        return mcq("A body moves so that its distance s metres after t seconds is s = %s. Find its velocity when t = %d." % (s, t), "%d m/s" % v,
                   ["%d m/s" % (v + b), "%d m/s" % acc if acc != v else "%d m/s" % (v + 1), "%d m/s" % (v - 1)],
                   "v = ds/dt = %s. At t = %d, <b>v = %d m/s</b>." % (ds, t, v))
    return mcq("The distance of a car is s = %s metres after t seconds. Find its acceleration when t = %d." % (s, t), "%d m/s²" % acc,
               ["%d m/s²" % v if v != acc else "%d m/s²" % (acc + 2), "%d m/s²" % (acc + 1), "%d m/s²" % (acc * t) if acc * t != acc else "0 m/s²"],
               "v = ds/dt = %s and a = dv/dt = %s. At t = %d, <b>a = %d m/s²</b>." % (ds, dds, t, acc))


def d_rule(r):
    kind = r.randrange(3)
    a, b, n = r.randint(1, 5), r.randint(-5, 5), r.randint(2, 4)
    if b == 0:
        raise AssertionError
    sup = {2: "²", 3: "³", 4: "⁴"}
    inner = poly({1: a, 0: b})
    if kind == 0:
        ans = "%d(%s)%s" % (n * a, inner, sup.get(n - 1, "")) if n * a != 1 else "(%s)%s" % (inner, sup[n - 1])
        return mcq("Differentiate y = (%s)%s." % (inner, sup[n]), ans, ["%d(%s)%s" % (n, inner, sup.get(n - 1, "")), "%d(%s)%s" % (a, inner, sup[n]), "%d(%s)%s" % (n * a, inner, sup[n])],
                   "Chain rule: n(ax + b)ⁿ⁻¹ × a = <b>%s</b>." % ans)
    if kind == 1:
        k = r.randint(2, 6)
        ans = "%sx%s" % (sn(-k * n) if -k * n != -1 else M, "⁻" + "⁰¹²³⁴⁵⁶⁷⁸⁹"[n + 1])
        return mcq("Find dy/dx if y = %d/x%s." % (k, sup[n]), ans, ["%sx⁻%s" % (sn(k * n), "⁰¹²³⁴⁵⁶⁷⁸⁹"[n + 1]), "%sx⁻%s" % (sn(-k * n), "⁰¹²³⁴⁵⁶⁷⁸⁹"[n - 1]), "%d/x%s" % (k * n, sup.get(n - 1, ""))],
                   "%d/x%s = %dx⁻%s. Bring the power down and take 1 away: <b>%s</b>." % (k, sup[n], k, "⁰¹²³⁴⁵⁶⁷⁸⁹"[n], ans))
    c = r.randint(1, 5)
    ans = poly({2: 3 * a, 1: 2 * b, 0: c})
    return mcq("Find dy/dx if y = x(%sx + %d) + %dx." % ("" if a == 1 else a, b, c) if b > 0 else "Find dy/dx if y = x(%sx %s %d) + %dx." % ("" if a == 1 else a, M, -b, c),
               poly({1: 2 * a, 0: b + c}), [poly({1: a, 0: b + c}), poly({2: a, 1: b + c}), poly({1: 2 * a, 0: c})],
               "Expand first: y = %s. Then <b>dy/dx = %s</b>." % (poly({2: a, 1: b + c}), poly({1: 2 * a, 0: b + c})))


# ============================================================ integration
def i_power(r):
    cs = _rpoly(r, r.randint(1, 3))
    integ = {}
    for k, c in cs.items():
        integ[k + 1] = F(c, k + 1)
    ans = poly(integ) + " + c"
    w1 = poly({k - 1: c * k for k, c in cs.items() if k}) + " + c"
    w2 = poly({k + 1: c for k, c in cs.items()}) + " + c"
    w3 = poly(integ)
    return mcq("Find ∫(%s) dx." % poly(cs), ans, [w1, w2, w3], "Add 1 to the power and divide by the new power, then add the constant c: <b>%s</b>." % ans)


def i_def(r):
    cs = _rpoly(r, r.randint(1, 2))
    a = r.randint(-1, 2)
    b = r.randint(a + 1, a + 3)
    Fn = lambda x: sum(F(c, k + 1) * x ** (k + 1) for k, c in cs.items())
    v = Fn(b) - Fn(a)
    wrong = [Fn(b) + Fn(a), Fn(b), sum(c * k * b ** (k - 1) for k, c in cs.items() if k) - sum(c * k * a ** (k - 1) for k, c in cs.items() if k), v + 1]
    return mcq("Evaluate ∫<sub>%s</sub><sup>%s</sup> (%s) dx." % (sn(a), sn(b), poly(cs)), sn(v), [sn(x) for x in wrong if x != v],
               "Integrate: %s. Then put in %s and %s and subtract: <b>%s</b>." % (poly({k + 1: F(c, k + 1) for k, c in cs.items()}), sn(b), sn(a), sn(v)))


def i_area(r):
    kind = r.randrange(2)
    if kind == 0:
        a, b = sorted(r.sample(range(0, 5), 2))
        k = ch(r, [1, 2, 3])
        v = F(k * (b ** 3 - a ** 3), 3)
        y = "x²" if k == 1 else "%dx²" % k
        return mcq("Find the area under the curve y = %s between x = %d and x = %d." % (y, a, b), sn(v) + " square units",
                   [sn(F(k * (b ** 2 - a ** 2))) + " square units", sn(k * (b ** 3 - a ** 3)) + " square units", sn(F(k * b ** 3, 3)) + " square units" if a else sn(v + 1) + " square units"],
                   "Area = ∫ %s dx from %d to %d = [%s]. So area = <b>%s square units</b>." % (y, a, b, ("x³/3" if k == 1 else "%sx³" % sn(F(k, 3))), sn(v)))
    p = r.randint(2, 6)
    # area between y = x(p − x) and the x-axis = p³/6
    v = F(p ** 3, 6)
    return mcq("Find the area enclosed by the curve y = %s and the x-axis." % poly({2: -1, 1: p}), sn(v) + " square units",
               [sn(F(p ** 3, 3)) + " square units", sn(F(p ** 2, 2)) + " square units", sn(F(p ** 3, 2)) + " square units"],
               "The curve meets the x-axis at x = 0 and x = %d. ∫ (%s) dx from 0 to %d = %d³/6 = <b>%s square units</b>." % (p, poly({2: -1, 1: p}), p, p, sn(v)))


def i_curve(r):
    a = r.randint(1, 4)
    b = r.randint(-5, 5)
    x0, y0 = r.randint(-2, 3), r.randint(-6, 8)
    c = y0 - (a * x0 * x0 + b * x0)
    ans = "y = " + poly({2: a, 1: b, 0: c})
    return mcq("The gradient of a curve is dy/dx = %s, and the curve passes through (%s, %s). Find its equation." % (poly({1: 2 * a, 0: b}), sn(x0), sn(y0)), ans,
               ["y = " + poly({2: a, 1: b}), "y = " + poly({2: 2 * a, 1: b, 0: c}), "y = " + poly({2: a, 1: b, 0: y0}) if y0 != c else "y = " + poly({2: a, 1: b, 0: c + 1})],
               "y = ∫(%s) dx = %s + c. Put in (%s, %s): c = %s, so <b>%s</b>." % (poly({1: 2 * a, 0: b}), poly({2: a, 1: b}), sn(x0), sn(y0), sn(c), ans))


# ============================================================ longitude and latitude (R = 6400 km, π = 22/7)
R_E = 6400
PI = F(22, 7)


def _km(x):
    return comma(int(round(float(x))))


def ll_diff(r):
    a = r.randint(2, 40)
    b = r.randint(2, 60)
    if r.random() < 0.5:
        e1, e2 = "%d°E" % a, "%d°W" % b
        d = a + b
        e = "One is east and one is west, so add: %d° + %d° = <b>%d°</b>." % (a, b, d)
        w = [abs(a - b), d + 10, d * 2]
    else:
        a, b = sorted(r.sample(range(2, 70), 2))
        side = ch(r, "EW")
        e1, e2 = "%d°%s" % (a, side), "%d°%s" % (b, side)
        d = b - a
        e = "Both are %s, so subtract: %d° − %d° = <b>%d°</b>." % ("east" if side == "E" else "west", b, a, d)
        w = [a + b, d + 10, abs(d - 5) or 1]
    return mcq("Find the difference in longitude between towns at %s and %s." % (e1, e2), "%d°" % d, ["%d°" % x for x in w if x != d], e)


def ll_meridian(r):
    t = ch(r, [7, 14, 21, 28, 35, 42, 45, 63, 70, 90])
    dist = F(t, 360) * 2 * PI * R_E
    if r.random() < 0.5:
        a = r.randint(0, 20)
        b = a + t
        q = "Two towns P(%d°N, 8°E) and Q(%d°N, 8°E) are on the same meridian. Find the distance PQ along the meridian. (Take R = 6400 km and π = 22/7.)" % (a, b)
    else:
        a = r.randint(1, min(t, 30) - 1) if t > 1 else 1
        b = t - a
        q = "Town X is at (%d°N, 5°E) and town Y is at (%d°S, 5°E). Find the distance XY along the meridian. (Take R = 6400 km and π = 22/7.)" % (a, b)
    return mcq(q, _km(dist) + " km", [_km(dist * 2) + " km", _km(dist / 2) + " km", _km(dist * F(866, 1000)) + " km"],
               "The angle at the centre is %d°. Distance = %d/360 × 2πR = %d/360 × 2 × 22/7 × 6400 ≈ <b>%s km</b>." % (t, t, t, _km(dist)))


COS = {0: 1.0, 30: 0.866, 45: 0.7071, 60: 0.5}


def ll_parallel(r):
    lat = ch(r, [30, 45, 60])
    t = ch(r, [14, 21, 28, 35, 42, 49, 56, 63, 70, 84, 105, 126])
    rad = R_E * COS[lat]
    dist = F(t, 360) * 2 * PI * F(str(rad))
    a = r.randint(2, 30)
    q = "Two towns are on latitude %d°N at longitudes %d°E and %d°E. Find the distance between them along the parallel of latitude. (Take R = 6400 km, π = 22/7 and cos %d° = %s.)" % (lat, a, a + t, lat, {30: "0.866", 45: "0.7071", 60: "0.5"}[lat])
    full = F(t, 360) * 2 * PI * R_E
    return mcq(q, _km(dist) + " km", [_km(full) + " km", _km(dist / 2) + " km", _km(F(t, 360) * 2 * PI * R_E * F(str(1 - COS[lat]))) + " km"],
               "The radius of the parallel is R cos %d° = %s km. Distance = %d/360 × 2π × %s ≈ <b>%s km</b>." % (lat, dec(rad, 1), t, dec(rad, 1), _km(dist)))


def ll_radius(r):
    lat = ch(r, [30, 45, 60])
    rad = R_E * COS[lat]
    return mcq("Find the radius of the parallel of latitude %d°N. (Take R = 6400 km and cos %d° = %s.)" % (lat, lat, {30: "0.866", 45: "0.7071", 60: "0.5"}[lat]),
               dec(rad, 1) + " km", [dec(R_E * (1 - COS[lat]), 1) + " km", "6,400 km", dec(R_E * COS[90 - lat] if 90 - lat in COS else R_E / 3, 1) + " km"],
               "r = R cos θ = 6400 × %s = <b>%s km</b>." % ({30: "0.866", 45: "0.7071", 60: "0.5"}[lat], dec(rad, 1)))


def ll_time(r):
    a = r.randint(1, 12) * 15
    side = ch(r, ["east", "west"])
    h = r.randint(7, 15)
    dh = a // 15
    local = (h + dh) % 24 if side == "east" else (h - dh) % 24
    f = lambda x: "%d:00 %s" % ((x - 1) % 12 + 1, "a.m." if x < 12 else "p.m.")
    return mcq("Town Q is %d° %s of town P. When it is %s at P, what is the local time at Q? (The time changes by 1 hour for every 15°.)" % (a, side, f(h)), f(local),
               [f((h - dh) % 24 if side == "east" else (h + dh) % 24), f((h + dh + 1) % 24), f((h + a // 10) % 24)],
               "%d° ÷ 15° = %d hours. Towns to the east are ahead, so <b>%s</b>." % (a, dh, f(local)))


# ============================================================ commercial arithmetic
def c_shares(r):
    k = K(r)
    n = ch(r, [200, 400, 500, 1000, 1500, 2000, 2500, 5000])
    par = ch(r, [1, 2, 5])
    pct = ch(r, [5, 8, 10, 12, 15, 20])
    div = F(n * par * pct, 100)
    if div.denominator != 1:
        raise AssertionError
    return mcq("%s owns %s shares of ₦%d each in a company. The company pays a dividend of %d%%. How much does %s receive?" % (k["n"], comma(n), par, pct, k["he"]), naira(int(div)),
               [naira(n * pct), naira(int(div) * 10), naira(n * par)], "Value of shares = %s × ₦%d = %s. %d%% of it = <b>%s</b>." % (comma(n), par, naira(n * par), pct, naira(int(div))))


def c_buy_shares(r):
    k = K(r)
    price = ch(r, [F(5, 2), 3, 4, 5, F(15, 2), 8, 10, 12])
    n = ch(r, [100, 200, 400, 500, 1000])
    cost = price * n
    if cost.denominator != 1:
        raise AssertionError
    total = int(cost)
    return mcq("%s has %s to buy shares sold at %s each. How many shares can %s buy?" % (k["n"], naira(total), naira(float(price)), k["he"]), comma(n),
               [comma(total), comma(n * 2), comma(n // 2) if n // 2 else "50"], "%s ÷ %s = <b>%s shares</b>." % (naira(total), naira(float(price)), comma(n)))


def c_income_tax(r):
    k = K(r)
    inc = ch(r, [1200000, 1500000, 1800000, 2400000, 3000000, 3600000])
    allow = ch(r, [200000, 300000, 400000, 500000, 600000])
    rate = ch(r, [5, 7, 10, 15])
    taxable = inc - allow
    tax = taxable * rate // 100
    return mcq("%s earns %s a year. %s tax-free allowance is %s, and tax is charged at %d%% on the rest. How much tax does %s pay?" % (k["n"], naira(inc), k["His"], naira(allow), rate, k["he"]),
               naira(tax), [naira(inc * rate // 100), naira(taxable), naira(allow * rate // 100)],
               "Taxable income = %s − %s = %s. Tax = %d%% of it = <b>%s</b>." % (naira(inc), naira(allow), naira(taxable), rate, naira(tax)))


def c_annuity(r):
    p = ch(r, [10000, 20000, 50000, 100000])
    i = ch(r, [5, 10, 20])
    n = ch(r, [2, 3])
    f = F(100 + i, 100)
    fv = p * ((f ** n - 1) / F(i, 100))
    if fv.denominator != 1:
        raise AssertionError
    return mcq("A man pays %s into a savings plan at the end of every year for %d years. The plan pays %d%% compound interest a year. How much is in the plan just after the last payment?" % (naira(p), n, i),
               naira(int(fv)), [naira(p * n), naira(int(p * n * f)), naira(int(fv) + p)],
               "Each payment grows: %s. Add them: <b>%s</b>." % (" + ".join(naira(int(p * f ** k)) for k in range(n - 1, -1, -1)), naira(int(fv))))


def c_amortise(r):
    k = K(r)
    loan = ch(r, [120000, 240000, 360000, 480000, 600000])
    rate = ch(r, [10, 12, 15, 20])
    yrs = ch(r, [1, 2])
    months = 12 * yrs
    total = loan + loan * rate * yrs // 100
    m = total // months
    if total % months:
        raise AssertionError
    return mcq("%s borrows %s at %d%% simple interest per year for %d year%s and pays it back in equal monthly instalments. How much is each instalment?" % (k["n"], naira(loan), rate, yrs, "s" if yrs > 1 else ""),
               naira(m), [naira(loan // months), naira(total), naira(m + loan * rate // 1200)],
               "Total to pay = %s + %s = %s. Each month = %s ÷ %d = <b>%s</b>." % (naira(loan), naira(total - loan), naira(total), naira(total), months, naira(m)))


# ============================================================ trigonometric ratios of any angle (degrees)
R2, R3 = "√2", "√3"
EXACT = {0: ("0", "1", "0"), 30: ("1/2", R3 + "/2", "1/" + R3), 45: ("1/" + R2, "1/" + R2, "1"), 60: (R3 + "/2", "1/2", R3), 90: ("1", "0", None)}
FN = ["sin", "cos", "tan"]


def _ref(a):
    q = 1 if a < 90 else 2 if a < 180 else 3 if a < 270 else 4
    ref = a if q == 1 else 180 - a if q == 2 else a - 180 if q == 3 else 360 - a
    return q, ref


def _sign(f, q):
    return {"sin": q in (1, 2), "cos": q in (1, 4), "tan": q in (1, 3)}[f]


def t_quadrant(r):
    a = r.choice([x for x in range(5, 360, 5) if x % 90])
    q, ref = _ref(a)
    names = {1: "the first quadrant", 2: "the second quadrant", 3: "the third quadrant", 4: "the fourth quadrant"}
    if r.random() < 0.5:
        return mcq("In which quadrant is an angle of %d°?" % a, names[q], [names[k] for k in (1, 2, 3, 4) if k != q],
                   "%d° is between %d° and %d°: <b>%s</b>." % (a, (q - 1) * 90, q * 90, names[q]))
    return mcq("Find the reference (acute) angle for %d°." % a, "%d°" % ref, ["%d°" % x for x in (90 - ref, 180 - ref, a - 90, 360 - ref) if x > 0 and x != ref],
               "%d° is in %s, so the acute angle with the x-axis is <b>%d°</b>." % (a, names[q], ref))


def t_sign(r):
    a = r.choice([x for x in range(10, 360, 10) if x % 90])
    f = ch(r, FN)
    q, ref = _ref(a)
    pos = _sign(f, q)
    ans = "Positive" if pos else "Negative"
    return mcq("Is %s %d° positive or negative?" % (f, a), ans, ["Negative" if pos else "Positive", "Zero", "It cannot be found"],
               "%d° is in quadrant %d. Only %s is positive there (All, Sin, Tan, Cos), so %s %d° is <b>%s</b>." % (a, q, {1: "all", 2: "sin", 3: "tan", 4: "cos"}[q], f, a, ans.lower()))


def t_value(r):
    a = ch(r, [120, 135, 150, 210, 225, 240, 300, 315, 330, 180, 270, 360])
    f = ch(r, FN)
    q, ref = _ref(a % 360) if a % 90 else (None, None)
    if a % 90 == 0:
        v = {("sin", 180): "0", ("cos", 180): "−1", ("tan", 180): "0", ("sin", 270): "−1", ("cos", 270): "0", ("tan", 270): None, ("sin", 360): "0", ("cos", 360): "1", ("tan", 360): "0"}[(f, a)]
        if v is None:
            raise AssertionError
        pool = ["0", "1", "−1", "1/2"]
        return mcq("Find the value of %s %d°." % (f, a), v, [x for x in pool if x != v], "Use the graph of %s: <b>%s %d° = %s</b>." % (f, f, a, v))
    base = EXACT[ref][FN.index(f)]
    v = base if _sign(f, q) else "−" + base
    other = "−" + base if v == base else base
    alt = EXACT[90 - ref][FN.index(f)] or R3
    w = [other, alt, "−" + alt if alt != "0" else "1"]
    return mcq("Find the exact value of %s %d°." % (f, a), v, [x for x in w if x != v],
               "%d° is in quadrant %d with reference angle %d°. %s %d° = %s, and the sign there is %s: <b>%s</b>." % (a, q, ref, f, ref, base, "+" if v == base else "−", v))


def t_amp(r):
    a = ch(r, [1, 2, 3, 4, 5])
    b = ch(r, [1, 2, 3, 4, 6])
    f = ch(r, ["sin", "cos"])
    y = "y = %s%s %sx" % ("" if a == 1 else "%d " % a, f, "" if b == 1 else b)
    if r.random() < 0.5:
        return mcq("What is the period of %s?" % y, "%d°" % (360 // b), ["%d°" % x for x in (360, 360 * b, 180 // b if 180 % b == 0 else 90, 360 // b + 90) if x != 360 // b],
                   "The period of %s bx is 360° ÷ b = 360° ÷ %d = <b>%d°</b>." % (f, b, 360 // b))
    return mcq("What is the amplitude of %s?" % y, str(a), [str(x) for x in (b, 2 * a, a + 1, 360 // b) if x != a],
               "The amplitude is the number in front of %s: <b>%d</b>. The graph goes from −%d to %d." % (f, a, a, a))


def t_maxmin(r):
    c = r.randint(1, 6)
    a = r.randint(1, 5)
    f = ch(r, ["sin", "cos"])
    sgn = ch(r, ["+", "−"])
    y = "y = %d %s %s%s x" % (c, sgn, "" if a == 1 else "%d " % a, f)
    kind = r.randrange(2)
    mx, mn = c + a, c - a
    if kind == 0:
        return mcq("Find the maximum value of %s." % y, sn(mx), [sn(x) for x in (mn, c, a, c * a) if x != mx],
                   "%s x is between −1 and 1, so the largest value is %d + %d = <b>%s</b>." % (f, c, a, sn(mx)))
    return mcq("Find the minimum value of %s." % y, sn(mn), [sn(x) for x in (mx, c, -a, c - 1) if x != mn],
               "%s x is between −1 and 1, so the smallest value is %d − %d = <b>%s</b>." % (f, c, a, sn(mn)))


SOLVE = [("sin", "1/2", (30, 150)), ("sin", "−1/2", (210, 330)), ("cos", "1/2", (60, 300)), ("cos", "−1/2", (120, 240)), ("tan", "1", (45, 225)), ("tan", "−1", (135, 315)),
         ("sin", "√3/2", (60, 120)), ("cos", "√3/2", (30, 330)), ("sin", "−√3/2", (240, 300)), ("cos", "−√3/2", (150, 210)), ("tan", "√3", (60, 240)), ("tan", "−√3", (120, 300)),
         ("sin", "1/√2", (45, 135)), ("cos", "1/√2", (45, 315)), ("cos", "−1/√2", (135, 225)), ("sin", "−1/√2", (225, 315)), ("tan", "1/√3", (30, 210))]


def t_solve(r):
    f, v, (a, b) = ch(r, SOLVE)
    q1, ref = _ref(a)
    ans = "%d° and %d°" % (a, b)
    others = [(ref, 180 - ref), (ref, 360 - ref), (180 + ref, 360 - ref), (180 - ref, 180 + ref)]
    w = ["%d° and %d°" % p for p in others if set(p) != {a, b}]
    return mcq("Solve %s x = %s for 0° ≤ x ≤ 360°." % (f, v), ans, w,
               "The acute angle with %s = %s is %d°. %s is %s in the quadrants that give <b>%s</b>." % (f, v.lstrip("−"), ref, f, "negative" if v.startswith("−") else "positive", ans))
