# -*- coding: utf-8 -*-
"""
India Class 12 Maths, NCERT Chapter 1: Relations and Functions (CBSE Unit I Relations and Functions)
  python3 tools/gen_in_maths_c12_relations_and_functions.py
Reflexive, symmetric and transitive relations, equivalence relations and equivalence classes, counting relations
with a property, one-one (injective), onto (surjective) and bijective functions, and counting one-one and onto
functions between finite sets (own makers).
Wrong answers come from real mistakes: calling a relation reflexive when one (a, a) is missing, forgetting that
transitivity needs every chain checked, calling x² one-one on R, thinking every one-one function is onto, and
mⁿ for the number of one-one functions.
"""
import random, math, itertools
from in_sr import U, T2, X, sup
from in_common import num, comma

R = random.Random(912101)


def st(pairs):
    return "{" + ", ".join("(%d, %d)" % p for p in pairs) + "}"


def props(A, Rl):
    S = set(Rl)
    ref = all((a, a) in S for a in A)
    sym = all((b, a) in S for a, b in S)
    tra = all((a, d) in S for a, b in S for c, d in S if b == c)
    return ref, sym, tra


def name(p):
    ref, sym, tra = p
    if ref and sym and tra:
        return "An equivalence relation"
    have = [n for n, v in zip(["reflexive", "symmetric", "transitive"], p) if v]
    if not have:
        return "Neither reflexive, symmetric nor transitive"
    return " and ".join(have).capitalize() + " only"


ALL = ["An equivalence relation", "Reflexive only", "Symmetric only", "Transitive only", "Reflexive and symmetric only", "Reflexive and transitive only",
       "Symmetric and transitive only", "Neither reflexive, symmetric nor transitive"]


def one_rel(r):
    A = [1, 2, 3]
    allp = [(a, b) for a in A for b in A]
    n = r.randint(1, 6)
    Rl = sorted(r.sample(allp, n))
    p = props(A, Rl)
    right = name(p)
    wr = [w for w in ALL if w != right]
    r.shuffle(wr)
    near = [w for w in wr if sum(x in w.lower() for x in ("reflexive", "symmetric", "transitive")) >= 1][:3]
    why = []
    for nm, v in zip(["reflexive", "symmetric", "transitive"], p):
        why.append("%s %s" % (nm, "yes" if v else "no"))
    return T2("A = {1, 2, 3} and R = %s. Which describes R?" % st(Rl), right, near if len(near) == 3 else wr[:3],
              "Check each property: %s. So R is <b>%s</b>." % ("; ".join(why), right[0].lower() + right[1:]))


RULES = [("a − b is divisible by %d", lambda a, b, k: (a - b) % k == 0, True, True, True),
         ("a ≤ b", lambda a, b, k: a <= b, True, False, True),
         ("a &lt; b", lambda a, b, k: a < b, False, False, True),
         ("|a − b| ≤ %d", lambda a, b, k: abs(a - b) <= k, True, True, False),
         ("a + b is even", lambda a, b, k: (a + b) % 2 == 0, True, True, True),
         ("a + b is odd", lambda a, b, k: (a + b) % 2 == 1, False, True, False),
         ("a = b", lambda a, b, k: a == b, True, True, True),
         ("b = a + 1", lambda a, b, k: b == a + 1, False, False, False),
         ("a divides b", lambda a, b, k: b % a == 0, True, False, True),
         ("ab ≥ 0", lambda a, b, k: a * b >= 0, True, True, False)]


def one_rule(r):
    t, f, ref, sym, tra = r.choice(RULES)
    k = r.choice([2, 3, 4, 5])
    rule = t % k if "%d" in t else t
    dom = "Z" if "divides" not in t else "N"
    right = name((ref, sym, tra))
    wr = [w for w in ALL if w != right]
    r.shuffle(wr)
    return T2("R is the relation on %s given by a R b if %s. Which describes R?" % (dom, rule), right, wr[:3],
              "Reflexive: %s. Symmetric: %s. Transitive: %s. So R is <b>%s</b>." % ("yes" if ref else "no", "yes" if sym else "no", "yes" if tra else "no", right[0].lower() + right[1:]))


def one_class(r):
    k = r.choice([2, 3, 4, 5])
    n = r.choice([10, 12, 15, 20])
    a = r.randint(0, k - 1)
    cls = [x for x in range(n + 1) if (x - a) % k == 0]
    A = "{0, 1, 2, …, %d}" % n
    if r.random() < 0.5:
        return T2("R = {(a, b) : |a − b| is a multiple of %d} on A = %s. Find the equivalence class [%d]." % (k, A, a), "{" + ", ".join(map(str, cls)) + "}",
                  ["{" + ", ".join(str(x) for x in range(n + 1) if (x - a) % k != 0)[:60] + "}" if k == 2 else "{" + ", ".join(str(x) for x in range(a, n + 1, k + 1)) + "}",
                   "{" + ", ".join(map(str, cls[1:])) + "}", "{%d}" % a],
                  "[%d] is the set of elements related to %d: those that differ from %d by a multiple of %d. <b>{%s}</b>." % (a, a, a, k, ", ".join(map(str, cls))))
    return T2("How many equivalence classes does R = {(a, b) : a − b is divisible by %d} have on Z?" % k, str(k), [str(k - 1), str(k + 1), "Infinitely many"],
              "The classes are the remainders 0, 1, …, %d on division by %d: <b>%d</b> classes." % (k - 1, k, k))


FUN = [("f(x) = %d<i>x</i> + %d", "R", "R", True, True), ("f(x) = <i>x</i>²", "R", "R", False, False), ("f(x) = <i>x</i>³", "R", "R", True, True),
       ("f(x) = |<i>x</i>|", "R", "R", False, False), ("f(x) = <i>x</i>²", "N", "N", True, False), ("f(x) = 2<i>x</i>", "N", "N", True, False),
       ("f(x) = <i>x</i> + 1", "N", "N", True, False), ("f(x) = <i>x</i> + 1", "Z", "Z", True, True), ("f(x) = [<i>x</i>]", "R", "R", False, False),
       ("f(x) = <i>x</i>²", "R", "[0, ∞)", False, True), ("f(x) = 2<i>x</i>", "Z", "Z", True, False), ("f(x) = <i>x</i>³", "N", "N", True, False)]
FNAME = {(True, True): "One-one and onto (bijective)", (True, False): "One-one but not onto", (False, True): "Onto but not one-one", (False, False): "Neither one-one nor onto"}


def one_fun(r):
    t, A, B, inj, sur = r.choice(FUN)
    if "%d" in t:
        t = t % (r.choice([2, 3, 4, 5, -2, -3]), r.randint(-7, 7))
        t = t.replace("+ -", "− ").replace("−0", "0").replace(" + 0", "")
    t = t.replace("f(x)", "f(<i>x</i>)")
    right = FNAME[(inj, sur)]
    why = {"x²_R": "f(−1) = f(1), so it is not one-one; negative numbers have no pre-image, so it is not onto."}
    return T2("f : %s → %s, %s. Which is true?" % (A, B, t), right, [v for k, v in FNAME.items() if v != right],
              "%s: %s. %s: %s. So f is <b>%s</b>." % ("One-one", "different inputs give different outputs" if inj else "two different inputs give the same output",
                                                    "Onto", "every element of the co-domain is an image" if sur else "some element of the co-domain is not an image", right[0].lower() + right[1:]))


def one_count(r):
    m, n = r.randint(2, 4), r.randint(2, 5)
    k = r.choice(["all", "inj", "onto", "bij", "rel"])
    if k == "all":
        return T2("A has %d elements and B has %d elements. How many functions are there from A to B?" % (m, n), comma(n ** m), [comma(m ** n), str(m * n), comma(2 ** (m * n))],
                  "Each of the %d elements of A has %d choices: %d<sup>%d</sup> = <b>%s</b>." % (m, n, n, m, comma(n ** m)))
    if k == "inj":
        if m > n:
            return T2("A has %d elements and B has %d elements. How many one-one functions are there from A to B?" % (m, n), "0", [str(math.perm(n, n)), comma(n ** m), str(m * n)],
                      "A one-one function needs at least as many elements in B as in A. Here %d &gt; %d, so there are <b>0</b>." % (m, n))
        return T2("A has %d elements and B has %d elements. How many one-one functions are there from A to B?" % (m, n), comma(math.perm(n, m)), [comma(n ** m), comma(math.comb(n, m)), str(m * n)],
                  "The first element has %d choices, the next %d, and so on: <sup>%d</sup>P<sub>%d</sub> = <b>%s</b>." % (n, n - 1, n, m, comma(math.perm(n, m))))
    if k == "bij":
        n = r.randint(2, 6)
        return T2("How many one-one functions are there from {1, 2, …, %d} to itself?" % n, comma(math.factorial(n)), [comma(n ** n), str(n), comma(2 ** n)],
                  "A one-one function from a finite set to itself is a bijection, so there are %d! = <b>%s</b>." % (n, comma(math.factorial(n))))
    if k == "onto":
        m = r.randint(3, 5)
        val = 2 ** m - 2
        return T2("How many onto functions are there from {1, 2, …, %d} to {a, b}?" % m, str(val), [str(2 ** m), str(2 ** m - 1), str(m)],
                  "Of the 2<sup>%d</sup> = %d functions, only the two constant ones are not onto: <b>%d</b>." % (m, 2 ** m, val))
    n = r.randint(2, 3)
    return T2("How many relations on A = {1, 2%s} are reflexive?" % (", 3" if n == 3 else ""), str(2 ** (n * n - n)), [str(2 ** (n * n)), str(2 ** n), str(n * n - n)],
              "The %d pairs (a, a) must be in R; each of the other %d pairs may or may not be: 2<sup>%d</sup> = <b>%d</b>." % (n, n * n - n, n * n - n, 2 ** (n * n - n)))


U(12, 1, "relations-and-functions", 1, "RF", "Relations and Functions: Equivalence Relations, One-one and Onto Functions", "relations and functions",
  "Types of relations: reflexive, symmetric, transitive and equivalence relations; one to one and onto functions (summary of the CBSE syllabus)",
  "Class 12 Relations and Functions worksheet (NCERT Chapter 1): reflexive, symmetric and transitive relations, equivalence classes, one-one, onto and bijective functions, and counting functions. 100 questions with answers.",
  "Equivalence = reflexive + symmetric + transitive.", "One-one: different inputs, different outputs. Onto: every element of the co-domain is an image.",
  "<ul><li>R on A is <b>reflexive</b> if (a, a) ∈ R for every a; <b>symmetric</b> if (a, b) ∈ R ⇒ (b, a) ∈ R; <b>transitive</b> if (a, b), (b, c) ∈ R ⇒ (a, c) ∈ R.</li>"
  "<li>An <b>equivalence relation</b> has all three. It splits A into disjoint <b>equivalence classes</b>.</li>"
  "<li>f is <b>one-one</b> if f(x<sub>1</sub>) = f(x<sub>2</sub>) ⇒ x<sub>1</sub> = x<sub>2</sub>; <b>onto</b> if every element of the co-domain has a pre-image; <b>bijective</b> if both.</li>"
  "<li>From a set of m elements to one of n elements: n<sup>m</sup> functions, <sup>n</sup>P<sub>m</sub> one-one functions (m ≤ n).</li></ul>",
  [("Is R = {(a, b) : a ≤ b} on Z an equivalence relation?", ["Reflexive: a ≤ a, yes", "Symmetric: 1 ≤ 2 but not 2 ≤ 1, no", "Transitive: yes"], "No, it is not symmetric")],
  ["Calling a relation reflexive when one pair (a, a) is missing.", "Saying f(x) = x² on R is one-one.", "Thinking a one-one function must be onto when the sets are infinite."],
  [("Is every bijective function invertible?", "Yes. A function has an inverse exactly when it is one-one and onto."),
   ("Is the empty relation transitive?", "Yes; there are no pairs to break the rule.")],
  [("Properties of a relation", [(one_rel, 20)]),
   ("Relations given by a rule", [(one_rule, 10), (one_class, 10)]),
   ("One-one and onto functions", [(one_fun, 20)]),
   ("Counting functions and relations", [(one_count, 16), (one_class, 4)]),
   ("Mixed problems", [(one_rel, 10), (one_fun, 6), (one_count, 4)])], 912101)
