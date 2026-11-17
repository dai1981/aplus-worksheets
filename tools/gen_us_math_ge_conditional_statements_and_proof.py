# -*- coding: utf-8 -*-
"""
US Geometry: Conditional Statements and Proof (Common Core G-CO.C.9)
  python3 tools/gen_us_math_ge_conditional_statements_and_proof.py
Hypothesis and conclusion; converse, inverse and contrapositive; counterexamples and truth values;
the Law of Detachment and the Law of Syllogism; properties of equality used as reasons in proofs.
Wrong answers come from real mistakes: mixing up the converse and the inverse, thinking the converse of a
true statement is always true, reasoning backward from the conclusion, and confusing the symmetric and
transitive properties.
"""
import random
from us_hs import B, S, make, lesson, collect, T, num, MINUS

R = random.Random(92501)

# subject, pronoun, p, q, not p, not q, converse true?  (p starts with the subject, q with the pronoun)
RAW = [
    ("an angle", "it", "an angle measures 90°", "it is a right angle", "an angle does not measure 90°", "it is not a right angle", True),
    ("two angles", "they", "two angles are vertical angles", "they are congruent", "two angles are not vertical angles", "they are not congruent", False),
    ("a figure", "it", "a figure is a square", "it is a rectangle", "a figure is not a square", "it is not a rectangle", False),
    ("a number", "it", "a number ends in 0", "it is divisible by 5", "a number does not end in 0", "it is not divisible by 5", False),
    ("two lines", "they", "two lines are perpendicular", "they form right angles", "two lines are not perpendicular", "they do not form right angles", True),
    ("a triangle", "it", "a triangle has three congruent sides", "it is equilateral", "a triangle does not have three congruent sides", "it is not equilateral", True),
    ("", "", "<i>x</i> = 4", "<i>x</i>² = 16", "<i>x</i> ≠ 4", "<i>x</i>² ≠ 16", False),
    ("", "", "you live in Chicago", "you live in Illinois", "you do not live in Chicago", "you do not live in Illinois", False),
    ("a polygon", "it", "a polygon has five sides", "it is a pentagon", "a polygon does not have five sides", "it is not a pentagon", True),
    ("two angles", "they", "two angles form a linear pair", "they are supplementary", "two angles do not form a linear pair", "they are not supplementary", False),
    ("a number", "it", "a number is even", "it is divisible by 2", "a number is not even", "it is not divisible by 2", True),
    ("two angles", "they", "two angles are complementary", "they add to 90°", "two angles are not complementary", "they do not add to 90°", True),
    ("an animal", "it", "an animal is a robin", "it is a bird", "an animal is not a robin", "it is not a bird", False),
    ("a triangle", "it", "a triangle is a right triangle", "it has a 90° angle", "a triangle is not a right triangle", "it does not have a 90° angle", True),
    ("a quadrilateral", "it", "a quadrilateral is a rhombus", "it has four congruent sides", "a quadrilateral is not a rhombus", "it does not have four congruent sides", True),
    ("", "", "today is Saturday", "tomorrow is Sunday", "today is not Saturday", "tomorrow is not Sunday", True),
]


def swap(subj, pron, s):
    """move the subject between clauses: 'it is a bird' -> 'an animal is a bird' and back"""
    if not subj:
        return s
    if s.startswith(pron + " "):
        return subj + s[len(pron):]
    if s.startswith(subj + " "):
        return pron + s[len(subj):]
    return s


ST = [(p, q, np_, nq, ct, subj, pron) for subj, pron, p, q, np_, nq, ct in RAW]


def forms(e):
    p, q, np_, nq, ct, subj, pron = e
    w = lambda x: swap(subj, pron, x)
    return {"original": cond(p, q), "converse": cond(w(q), w(p)), "inverse": cond(np_, nq), "contrapositive": cond(w(nq), w(np_))}


def cond(p, q):
    s = "If %s, then %s." % (p, q)
    return s[0].upper() + s[1:]


def subj(q, p):
    """make the pronoun in the new hypothesis clear when p and q are swapped"""
    return q


# ------------------------------------------------------------ set 1: hypothesis and conclusion
def one_hc(r):
    p, q, np_, nq, ct, subj, pron = r.choice(ST)
    s = cond(p, q)
    if r.random() < 0.5:
        return T("What is the <b>hypothesis</b> of this statement? %s" % B(s), p, [q, np_, nq],
                 "The hypothesis is the part after \"if\": <b>%s</b>." % p)
    if r.random() < 0.5:
        return T("What is the <b>conclusion</b> of this statement? %s" % B(s), q, [p, nq, np_],
                 "The conclusion is the part after \"then\": <b>%s</b>." % q)
    form = r.choice(["All", "Every"])
    pairs = {
        "a figure is a square": ("All squares are rectangles.", cond("a figure is a square", "it is a rectangle")),
        "an animal is a robin": ("Every robin is a bird.", cond("an animal is a robin", "it is a bird")),
        "you live in Chicago": ("People who live in Chicago live in Illinois.", cond("you live in Chicago", "you live in Illinois")),
        "two angles are vertical angles": ("Vertical angles are congruent.", cond("two angles are vertical angles", "they are congruent")),
        "a number ends in 0": ("Numbers that end in 0 are divisible by 5.", cond("a number ends in 0", "it is divisible by 5")),
        "two angles form a linear pair": ("Angles that form a linear pair are supplementary.", cond("two angles form a linear pair", "they are supplementary")),
    }
    if p not in pairs:
        return None
    plain, right = pairs[p]
    f = forms((p, q, np_, nq, ct, subj, pron))
    wrong = [f["converse"], f["inverse"], f["contrapositive"]]
    return T("Which shows %s written as a conditional statement?" % B(plain), right, wrong,
             "Put the group being described after \"if\" and the property after \"then\": <b>%s</b>" % right)


# ------------------------------------------------------------ set 2: converse, inverse, contrapositive
def one_cic(r):
    ent = r.choice(ST)
    forms_ = forms(ent)
    if r.random() < 0.65:
        want = r.choice(["converse", "inverse", "contrapositive"])
        e = {"converse": "The converse switches the hypothesis and the conclusion: <b>%s</b>",
             "inverse": "The inverse negates both parts and keeps the order: <b>%s</b>",
             "contrapositive": "The contrapositive switches and negates both parts: <b>%s</b>"}[want] % forms_[want]
        return T("Statement: %s Which is its <b>%s</b>?" % (B(forms_["original"]), want), forms_[want],
                 [v for k, v in forms_.items() if k != want], e)
    want = r.choice(["converse", "inverse", "contrapositive"])
    right = want.capitalize()
    return T("Statement: %s What is this new statement called? %s" % (B(forms_["original"]), B(forms_[want])), right,
             [x.capitalize() for x in ["converse", "inverse", "contrapositive", "biconditional"] if x != want],
             "Compare with the original. Switched only: converse. Negated only: inverse. Switched and negated: contrapositive. This is the <b>%s</b>." % want)


# ------------------------------------------------------------ set 3: counterexamples and truth values
CE = [
    ("If a number is prime, then it is odd.", "2", ["3", "9", "15"], "2 is prime but it is even, so the statement is false."),
    ("If <i>x</i>² = 25, then <i>x</i> = 5.", "<i>x</i> = %s5" % MINUS, ["<i>x</i> = 5", "<i>x</i> = 25", "<i>x</i> = 0"],
     "(%s5)² = 25 too, but %s5 ≠ 5." % (MINUS, MINUS)),
    ("If a quadrilateral has four right angles, then it is a square.", "A 3 cm by 5 cm rectangle", ["A 4 cm by 4 cm square", "A trapezoid", "A triangle"],
     "A 3 by 5 rectangle has four right angles but is not a square."),
    ("If a number is divisible by 3, then it is divisible by 9.", "12", ["18", "27", "10"], "12 is divisible by 3 but not by 9."),
    ("If a number is odd, then it is prime.", "9", ["7", "13", "8"], "9 is odd but 9 = 3 × 3, so it is not prime."),
    ("If |<i>x</i>| = 3, then <i>x</i> = 3.", "<i>x</i> = %s3" % MINUS, ["<i>x</i> = 3", "<i>x</i> = 0", "<i>x</i> = 9"],
     "|%s3| = 3, but %s3 ≠ 3." % (MINUS, MINUS)),
    ("If <i>x</i> &gt; <i>y</i>, then <i>x</i>² &gt; <i>y</i>².", "<i>x</i> = 1, <i>y</i> = %s2" % MINUS,
     ["<i>x</i> = 3, <i>y</i> = 2", "<i>x</i> = 5, <i>y</i> = 1", "<i>x</i> = 4, <i>y</i> = 0"],
     "1 &gt; %s2, but 1² = 1 is not greater than (%s2)² = 4." % (MINUS, MINUS)),
    ("If a polygon has four sides, then it is a rectangle.", "A trapezoid", ["A square", "A rectangle", "A triangle"],
     "A trapezoid has four sides but is not a rectangle. (A triangle does not have four sides, so it does not test the statement.)"),
    ("If two angles are supplementary, then they form a linear pair.", "Two separate angles of 100° and 80°",
     ["Two adjacent angles of 120° and 60° on a line", "Two angles of 30° and 60°", "Two angles of 90° and 90° on a line"],
     "100° + 80° = 180°, so they are supplementary, but they are not adjacent, so they are not a linear pair."),
    ("If an angle is acute, then it measures less than 60°.", "A 75° angle", ["A 45° angle", "A 100° angle", "A 30° angle"],
     "75° is acute (less than 90°) but it is not less than 60°."),
    ("If <i>ab</i> &gt; 0, then <i>a</i> &gt; 0.", "<i>a</i> = %s2, <i>b</i> = %s3" % (MINUS, MINUS),
     ["<i>a</i> = 2, <i>b</i> = 3", "<i>a</i> = %s2, <i>b</i> = 3" % MINUS, "<i>a</i> = 0, <i>b</i> = 5"],
     "(%s2)(%s3) = 6 &gt; 0, but <i>a</i> = %s2 is not positive." % (MINUS, MINUS, MINUS)),
    ("If a number is a multiple of 4, then it is a multiple of 8.", "12", ["16", "24", "6"], "12 is a multiple of 4 but not of 8."),
]


def one_ce(r):
    if r.random() < 0.55:
        s, right, wr, e = r.choice(CE)
        return T("Which is a <b>counterexample</b> to this statement? %s" % B(s), right, wr,
                 "A counterexample makes the hypothesis true and the conclusion false. " + e + " <b>%s</b>." % right)
    ent = r.choice(ST)
    p, q, np_, nq, ct = ent[:5]
    form = r.choice(["converse", "contrapositive", "inverse"])
    text = forms(ent)[form]
    true = True if form == "contrapositive" else ct
    right = "True" if true else "False"
    why = {"contrapositive": "A contrapositive always has the same truth value as the original statement, which is true.",
           "converse": "The converse is %s." % ("true here: this statement works both ways, like a definition" if ct else "false: the conclusion can be true when the hypothesis is not"),
           "inverse": "The inverse has the same truth value as the converse, which is %s here." % ("true" if ct else "false")}[form]
    return T("The statement %s is true. Is its %s, %s, true or false?" % (B(cond(p, q)), form, B(text)), right,
             ["False" if true else "True", "It depends on the reader", "It cannot be written"], why + " <b>%s</b>." % right)


# ------------------------------------------------------------ set 4: laws of logic
CHAINS = [
    ("Maria practices every day", "she makes the team", "she plays in the first game"),
    ("it snows overnight", "school is canceled", "Jamal stays home"),
    ("two angles are a linear pair", "they are supplementary", "their measures add to 180°"),
    ("a figure is a square", "it is a rhombus", "its diagonals are perpendicular"),
    ("the battery is dead", "the phone will not turn on", "Kai cannot call home"),
    ("<i>x</i> + 3 = 10", "<i>x</i> = 7", "2<i>x</i> = 14"),
    ("Owen gets an A on the test", "he gets an A in the class", "he makes the honor roll"),
    ("the temperature drops below 32°F", "the pond freezes", "people can skate on the pond"),
    ("a triangle is equilateral", "it is isosceles", "it has at least two congruent sides"),
]


def capf(s):
    return s if s.startswith("<") else s[0].upper() + s[1:]


def one_law(r):
    p, q, s_ = r.choice(CHAINS)
    kind = r.choice(["det", "det", "back", "syl", "syl"])
    if kind == "det":
        q_ = "Given: %s %s is true. What can you conclude?" % (B(cond(p, q)), "“%s”" % p)
        right = capf(q) + "."
        return T(q_, right, [capf(s_) + ".", "No conclusion can be made.", "If %s, then %s." % (q, p)],
                 "Law of Detachment: the hypothesis is true, so the conclusion is true. <b>%s</b>" % right)
    if kind == "back":
        q_ = "Given: %s %s is true. What can you conclude?" % (B(cond(p, q)), "“%s”" % q)
        right = "No conclusion can be made."
        return T(q_, right, [capf(p) + ".", capf(s_) + ".", "It is false that %s." % p],
                 "The conclusion being true does not prove the hypothesis. Something else could make it true. <b>%s</b>" % right)
    q_ = "Given: %s and %s What can you conclude by the Law of Syllogism?" % (B(cond(p, q).rstrip(".") + ","), B(cond(q, s_)))
    right = cond(p, s_)
    return T(q_, right, [cond(s_, p), cond(q, p), "No conclusion can be made."],
             "The conclusion of the first statement is the hypothesis of the second, so chain them: <b>%s</b>" % right)


# ------------------------------------------------------------ set 5: reasons in proofs
PROPS = ["Reflexive Property", "Symmetric Property", "Transitive Property", "Substitution Property",
         "Addition Property of Equality", "Subtraction Property of Equality", "Multiplication Property of Equality",
         "Division Property of Equality", "Distributive Property"]


def one_prop(r):
    a, b, c = r.randint(2, 9), r.randint(2, 15), r.randint(3, 20)
    P1, P2, P3 = r.sample(["AB", "CD", "EF", "GH", "JK", "PQ", "RS"], 3)
    n1, n2 = r.sample(range(1, 7), 2)
    kind = r.choice(PROPS)
    st = {
        "Reflexive Property": r.choice(["%s = %s" % (P1, P1), "m∠%d = m∠%d" % (n1, n1), "<span class='ov'>%s</span> ≅ <span class='ov'>%s</span>" % (P1, P1)]),
        "Symmetric Property": r.choice(["If %s = %s, then %s = %s." % (P1, P2, P2, P1), "If m∠%d = m∠%d, then m∠%d = m∠%d." % (n1, n2, n2, n1)]),
        "Transitive Property": "If %s = %s and %s = %s, then %s = %s." % (P1, P2, P2, P3, P1, P3),
        "Substitution Property": "If <i>x</i> = %d and %d<i>x</i> + <i>y</i> = %d, then %d + <i>y</i> = %d." % (a, b, c + a * b, a * b, c + a * b),
        "Addition Property of Equality": "If <i>x</i> %s %d = %d, then <i>x</i> = %d." % (MINUS, b, c, b + c),
        "Subtraction Property of Equality": "If <i>x</i> + %d = %d, then <i>x</i> = %d." % (b, b + c, c),
        "Multiplication Property of Equality": "If <i>x</i> ÷ %d = %d, then <i>x</i> = %d." % (a, c, a * c),
        "Division Property of Equality": "If %d<i>x</i> = %d, then <i>x</i> = %d." % (a, a * c, c),
        "Distributive Property": "If %d(<i>x</i> + %d) = %d, then %d<i>x</i> + %d = %d." % (a, b, a * (b + c), a, a * b, a * (b + c)),
    }[kind]
    near = {"Reflexive Property": ["Symmetric Property", "Transitive Property", "Substitution Property"],
            "Symmetric Property": ["Transitive Property", "Reflexive Property", "Substitution Property"],
            "Transitive Property": ["Symmetric Property", "Substitution Property", "Reflexive Property"],
            "Substitution Property": ["Transitive Property", "Distributive Property", "Symmetric Property"],
            "Addition Property of Equality": ["Subtraction Property of Equality", "Substitution Property", "Multiplication Property of Equality"],
            "Subtraction Property of Equality": ["Addition Property of Equality", "Division Property of Equality", "Substitution Property"],
            "Multiplication Property of Equality": ["Division Property of Equality", "Distributive Property", "Addition Property of Equality"],
            "Division Property of Equality": ["Multiplication Property of Equality", "Subtraction Property of Equality", "Distributive Property"],
            "Distributive Property": ["Multiplication Property of Equality", "Substitution Property", "Addition Property of Equality"]}[kind]
    why = {"Reflexive Property": "Anything is equal (or congruent) to itself.",
           "Symmetric Property": "The two sides of an equation can be switched.",
           "Transitive Property": "Two things equal to the same thing are equal to each other.",
           "Substitution Property": "A value replaces the variable it equals.",
           "Addition Property of Equality": "%d was added to both sides." % b,
           "Subtraction Property of Equality": "%d was subtracted from both sides." % b,
           "Multiplication Property of Equality": "Both sides were multiplied by %d." % a,
           "Division Property of Equality": "Both sides were divided by %d." % a,
           "Distributive Property": "%d was multiplied by each term inside the parentheses." % a}[kind]
    return T("Which property justifies this step? %s" % B(st), kind, near, why + " <b>%s</b>." % kind)


def build():
    sets = [S("Hypothesis and conclusion", collect(one_hc, 20, R)),
            S("Converse, inverse and contrapositive", collect(one_cic, 20, R)),
            S("Counterexamples and truth values", collect(one_ce, 20, R)),
            S("Laws of Detachment and Syllogism", collect(one_law, 20, R)),
            S("Reasons in a proof", collect(one_prop, 20, R))]
    body = lesson(
        "<p>A <b>conditional statement</b> has the form <b>If <i>p</i>, then <i>q</i></b>. <i>p</i> is the hypothesis and <i>q</i> is the conclusion.</p>"
        "<ul><li><b>Converse</b>: If <i>q</i>, then <i>p</i> (switch).</li><li><b>Inverse</b>: If not <i>p</i>, then not <i>q</i> (negate).</li>"
        "<li><b>Contrapositive</b>: If not <i>q</i>, then not <i>p</i> (switch and negate). It always has the same truth value as the original.</li></ul>"
        "<p>One <b>counterexample</b> (hypothesis true, conclusion false) proves a statement false.</p>"
        "<p>In a <b>proof</b>, every step needs a reason: a given fact, a definition, a postulate, a theorem, or a property such as the Transitive Property.</p>",
        [("Write the contrapositive of \"If two angles are vertical angles, then they are congruent.\"",
          ["Switch the parts and negate both"], "If two angles are not congruent, then they are not vertical angles. (True)"),
         ("If it rains, the game is canceled. If the game is canceled, we go to the movies. It rains. What happens?",
          ["Law of Syllogism: if it rains, we go to the movies", "Law of Detachment: it rains, so we go to the movies"], "We go to the movies.")],
        ["Mixing up the converse and the inverse. Converse switches; inverse negates.",
         "Assuming the converse of a true statement is true. Vertical angles are congruent, but congruent angles are not always vertical.",
         "Reasoning backward. If p then q, and q is true, tells you nothing about p.",
         "Mixing up symmetric (a = b, so b = a) and transitive (a = b and b = c, so a = c)."])
    faq = [("What is the contrapositive of a conditional statement?",
            "Switch the hypothesis and conclusion and negate both: if not q, then not p. It is true exactly when the original statement is true."),
           ("What is a counterexample?", "An example where the hypothesis is true but the conclusion is false. One counterexample is enough to show a statement is false."),
           ("What is the Law of Detachment?", "If 'if p, then q' is true and p is true, then q is true."),
           ("What is the Law of Syllogism?", "If 'if p, then q' and 'if q, then r' are both true, then 'if p, then r' is true.")]
    make("conditional-statements-and-proof", 5, "G-CO.C.9",
         "Conditional Statements and Proof",
         "Conditional Statements Worksheet: Converse, Inverse, Contrapositive (Geometry) | 100 Questions",
         "Conditional Statements",
         "Prove theorems about lines and angles. Theorems include: vertical angles are congruent; when a transversal crosses parallel lines, alternate interior angles are congruent and corresponding angles are congruent; points on a perpendicular bisector of a line segment are exactly those equidistant from the segment's endpoints.",
         "Free Geometry worksheet on conditional statements: converse, inverse, contrapositive, counterexamples, laws of logic and reasons in proofs. 100 questions with answers.",
         "If p, then q. The contrapositive (if not q, then not p) is true exactly when the original is.",
         "A converse can be false even when the statement is true. One counterexample disproves a statement.",
         body, faq, sets, R, domain="Reasoning and Proof", grade="geometry")


if __name__ == "__main__":
    build()
