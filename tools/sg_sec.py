# -*- coding: utf-8 -*-
"""
Shared helpers for Singapore Secondary 1 and 2 (MOE 2020 O-Level / G3 Mathematics syllabus, formerly Express).
Same API as uk_ks3 and au_hs, so generators ported from those read the same way, with Singapore conventions:
- numbers: 4 digits with no separator (4536); 5 digits and more grouped with a no-break space (10 000), as in MOE papers
- money: $3.50, $0.75 (Singapore dollars); GST is 9%
- British English (colour, metre, maths, students), Singapore names and places
make() takes the syllabus sub-strand code (N1 to N9, G1 to G7, S1 to S2) and its original text.
"""
import random
from fractions import Fraction as F
import ws_common
from ws_common import (par, frac, fr, mcq, balance, B, cap, fig, figure, svg_wrap, text,
                       line, table, number_line, write_unit, MINUS, GREEN, FILL, GRAY, INK, RED, BLUE, FONT, X)

NBSP = " "


def comma(n):
    """Singapore grouping: 4536, 10 000 (no-break space)."""
    n = int(n)
    return str(n) if abs(n) < 10000 else "{:,}".format(n).replace(",", NBSP)


ws_common.comma = comma
from ws_common import dec, num, nums   # noqa: E402

UPDATED = "2026-11-18"
STD_URL = "https://www.moe.gov.sg/-/media/files/secondary/syllabuses/maths/2020-express_na-maths_syllabuses.ashx"
GIRLS = ["Wei Ling", "Priya", "Siti", "Mei Ling", "Hui Min", "Nurul", "Rachel", "Aisha", "Jia Hui", "Kavya", "Xin Yi", "Farah"]
BOYS = ["Jun Jie", "Ahmad", "Ravi", "Wei Jie", "Daniel", "Hafiz", "Arjun", "Ethan", "Zhi Hao", "Imran", "Marcus", "Kumar"]
TIMES = "×"
PLACES = ["Jurong", "Tampines", "Woodlands", "Changi", "Sentosa", "Bishan", "Punggol", "Clementi"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def sgd(v):
    """$3.50, $12, $0.75, $12 500."""
    v = F(v)
    neg = v < 0
    v = abs(v)
    if v.denominator == 1:
        out = "$" + comma(v)
    else:
        c = int(round(v * 100))
        out = "$" + comma(c // 100) + "." + ("%02d" % (c % 100))
    return (MINUS if neg else "") + out


gbp = aud = usd = sgd   # ported code may still call these


def v(name):
    return "<i>%s</i>" % name


def sq(x):
    return "%s²" % x


def collect(make_one, n, rnd, tries=4000):
    out, seen = [], set()
    for _ in range(tries):
        try:
            it = make_one(rnd)
        except (AssertionError, TypeError):
            continue
        if it is None:
            continue
        key = it["q"] + "|" + "|".join(sorted(it["c"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
        if len(out) == n:
            return out
    raise AssertionError("only %d items" % len(out))


def S(title, items):
    assert len(items) == 20, (title, len(items))
    return {"title": title, "items": items}


def lesson(think, examples, mistakes, extra=""):
    h = "<h2>How it works</h2>" + think + extra
    for q, steps, ans in examples:
        h += ("<div class='sn-ex'><span class='sn-ex-t'>Example</span><p class='sn-ex-q'>%s</p>%s"
              "<p class='sn-ex-a'>Answer: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), ans))
    h += "<h2>Common mistakes</h2><ul>" + "".join("<li>%s</li>" % m for m in mistakes) + "</ul>"
    return h


SUB = {"N1": "Numbers and their Operations", "N2": "Ratio and Proportion", "N3": "Percentage", "N4": "Rate and Speed",
       "N5": "Algebraic Expressions and Formulae", "N6": "Functions and Graphs", "N7": "Equations and Inequalities",
       "G1": "Angles, Triangles and Polygons", "G2": "Congruence and Similarity", "G4": "Pythagoras' Theorem and Trigonometry",
       "G5": "Mensuration", "S1": "Data Handling and Analysis", "S2": "Probability"}
STRAND = {"N": "Number and Algebra", "G": "Geometry and Measurement", "S": "Statistics and Probability"}



# syllabus text (MOE 2020 O-Level Mathematics, Secondary 1 and 2 content) for each unit
STD_TEXT = {
    "primes-hcf-and-lcm": "primes and prime factorisation; finding highest common factor (HCF) and lowest common multiple (LCM), squares, cubes, square roots and cube roots by prime factorisation",
    "integers-and-the-number-line": "negative numbers, integers, rational numbers, real numbers and their four operations; representation and ordering of numbers on the number line; use of <, >, ≤, ≥",
    "approximation-and-estimation": "approximation and estimation (including rounding off numbers to a required number of decimal places or significant figures, and estimating the results of computation)",
    "ratio": "ratios involving rational numbers; writing a ratio in its simplest form; problems involving ratio",
    "percentage": "expressing one quantity as a percentage of another; comparing two quantities by percentage; percentages greater than 100%; increasing/decreasing a quantity by a given percentage; reverse percentages; problems involving percentages",
    "rate-and-speed": "concepts of average rate, speed, constant speed and average speed; conversion of units (e.g. km/h to m/s); problems involving rate and speed",
    "algebraic-expressions-and-substitution": "using letters to represent numbers; interpreting notations; evaluation of algebraic expressions and formulae; translation of simple real-world situations into algebraic expressions",
    "simplifying-linear-expressions": "addition and subtraction of linear expressions; simplification of linear expressions; use brackets and extract common factors",
    "number-patterns": "recognising and representing patterns/relationships by finding an algebraic expression for the nth term",
    "linear-equations": "concept of equation; solving linear equations in one variable; solving simple fractional equations that can be reduced to linear equations; formulating a linear equation in one variable to solve problems",
    "linear-graphs-and-gradient": "Cartesian coordinates in two dimensions; linear functions y = ax + b; graphs of linear functions; the gradient of a linear graph as the ratio of the vertical change to the horizontal change (positive and negative gradients)",
    "angles-triangles-and-quadrilaterals": "right, acute, obtuse and reflex angles; vertically opposite angles, angles on a straight line, angles at a point; properties of triangles and special quadrilaterals",
    "parallel-lines-and-polygons": "angles formed by two parallel lines and a transversal: corresponding angles, alternate angles, interior angles; properties of regular polygons; angle sum of interior and exterior angles of any convex polygon",
    "perimeter-and-area": "area of parallelogram and trapezium; problems involving perimeter and area of composite plane figures",
    "volume-and-surface-area-of-prisms-and-cylinders": "volume and surface area of prism and cylinder; conversion between cm² and m², and between cm³ and m³; problems involving volume and surface area of composite solids",
    "expansion-and-factorisation": "expansion of the product of algebraic expressions; use of (a + b)² = a² + 2ab + b², (a − b)² = a² − 2ab + b² and a² − b² = (a + b)(a − b); factorisation of quadratic expressions",
    "algebraic-fractions": "multiplication and division of simple algebraic fractions; addition and subtraction of algebraic fractions with linear or quadratic denominator",
    "changing-the-subject-of-a-formula": "changing the subject of a formula; finding the value of an unknown quantity in a given formula",
    "linear-inequalities": "concept of equation and inequality; solving simple inequalities in the form ax ≤ b, ax ≥ b, ax < b and ax > b, and representing the solution on the number line",
    "simultaneous-equations": "graphs of linear equations in two variables (ax + by = c); solving simultaneous linear equations in two variables by substitution and elimination methods and the graphical method; formulating a pair of linear equations in two variables to solve problems",
    "quadratic-equations": "solving quadratic equations in one variable by factorisation",
    "quadratic-graphs": "quadratic functions y = ax² + bx + c; graphs of quadratic functions and their properties: positive or negative coefficient of x², maximum and minimum points, symmetry",
    "direct-and-inverse-proportion": "direct and inverse proportion",
    "map-scales": "map scales (distance and area)",
    "congruence-and-similarity": "congruent figures; similar figures; properties of similar triangles and polygons: corresponding angles are equal, corresponding sides are proportional; enlargement and reduction of a plane figure; solving simple problems involving congruence and similarity",
    "pythagoras-theorem": "use of Pythagoras' theorem; determining whether a triangle is right-angled given the lengths of three sides",
    "trigonometric-ratios": "use of trigonometric ratios (sine, cosine and tangent) of acute angles to calculate unknown sides and angles in right-angled triangles",
    "volume-of-cones-and-spheres": "volume and surface area of pyramid, cone and sphere",
    "mean-median-and-mode": "mean, mode and median as measures of central tendency for a set of data; purposes and use of mean, mode and median",
    "stem-and-leaf-diagrams": "analysis and interpretation of dot diagrams, histograms and stem-and-leaf diagrams",
    "frequency-tables-and-grouped-data": "calculation of the mean for grouped data; analysis and interpretation of tables, bar graphs, pie charts and histograms",
    "probability": "probability as a measure of chance; probability of single events (including listing all the possible outcomes in a simple chance situation to calculate the probability)",
}
# Singapore titles where the ported one used other names
TITLES = {
    "expansion-and-factorisation": ("Expansion and Factorisation of Quadratic Expressions", "Expansion and factorisation"),
    "linear-inequalities": ("Linear Inequalities: Solving and the Number Line", "Linear inequalities"),
    "trigonometric-ratios": ("Trigonometric Ratios: Sine, Cosine and Tangent", "Trigonometric ratios"),
    "mean-median-and-mode": ("Mean, Median and Mode", "Mean, median and mode"),
    "frequency-tables-and-grouped-data": ("Frequency Tables, Grouped Data and Pie Charts", "Frequency tables and grouped data"),
    "congruence-and-similarity": ("Congruence and Similarity: Similar Triangles and Scale Factors", "Congruence and similarity"),
    "volume-of-cones-and-spheres": ("Volume of Cylinders, Cones and Spheres", "Volume of cones and spheres"),
    "quadratic-graphs": ("Graphs of Quadratic Functions", "Quadratic graphs"),
    "simultaneous-equations": ("Simultaneous Linear Equations", "Simultaneous equations"),
    "changing-the-subject-of-a-formula": ("Changing the Subject of a Formula", "Changing the subject of a formula"),
}

SG_WORDS = [("Year 7", "Secondary 1"), ("Year 8", "Secondary 2"), ("Year 9", "Secondary 2"), ("KS3 ", ""), ("Key Stage 3", "secondary school"),
            ("the National Curriculum", "the MOE syllabus"), ("National Curriculum", "MOE syllabus"), ("GCSE", "O-Level"), ("pupils", "students")]


def sgify(s):
    for a, b in SG_WORDS:
        s = s.replace(a, b)
    return s


def make(level, slug, sort, code, title, seo_title, short_title, std_text, meta, key_big, key_sub, body, faq, sets, rnd):
    assert code in SUB, code
    std_text = STD_TEXT[slug]
    if slug in TITLES:
        title, short_title = TITLES[slug]
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
    assert len(sets) == 5
    balance(sets, rnd)
    import re as _re
    one = lambda t: _re.sub(r"(?<![\d.,/])\b1 (hour|minute|second|day|week|year|cent|litre|metre)s\b", r"1 \1", t).replace("pupils", "students")
    for s in sets:
        for it in s["items"]:
            it["q"], it["e"] = one(it["q"]), one(it["e"])
            it["c"] = [one(c) for c in it["c"]]
    seo_title = "Sec %d %s Worksheets: Free Secondary %d Maths with Answers (MOE Syllabus)" % (level, short_title[0].upper() + short_title[1:], level)
    meta = sgify(meta)
    faq = [(sgify(q), sgify(a)) for q, a in faq]
    unit = {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": STRAND[code[0]], "standard_code": "Secondary %d: %s" % (level, SUB[code]), "standard_url": STD_URL,
        "standard_text": std_text, "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets,
        "pdf_url": "", "sort": sort, "updated": UPDATED,
    }
    write_unit("sg", "maths", "secondary-%d" % level, unit)


def opts(correct, wrongs, fmt=None):
    f = fmt or num
    c = (f(correct), F(correct) if not isinstance(correct, str) else correct)
    w = []
    for x in wrongs:
        if x is None:
            continue
        w.append((f(x), F(x) if not isinstance(x, str) else x))
    return c, w


def Q(q, correct, wrongs, e, fmt=None):
    c, w = opts(correct, wrongs, fmt)
    return mcq(q, c, w, e)


def T(q, correct, wrongs, e):
    return mcq(q, (correct, correct), [(x, x) for x in wrongs], e)


def QN(q, ans, wrongs, e, fmt=None, unit="", near=(1, -1, 2, -2, 10, -10)):
    f = fmt or num
    ans = F(ans)
    ws = [F(w) for w in wrongs if w is not None] + [ans + d for d in near]

    def safe(w):
        try:
            return f(w)
        except (TypeError, AssertionError):
            return None
    cands = [(safe(w) + unit, w) for w in ws if w != ans and safe(w) is not None]
    return mcq(q, (f(ans) + unit, ans), cands, e)


def term(c, var, first=False):
    c = F(c)
    if c == 0:
        return ""
    mag = abs(c)
    body = (num(mag) if (mag != 1 or not var) else "") + var
    if first:
        return (MINUS if c < 0 else "") + body
    return (" %s " % (MINUS if c < 0 else "+")) + body


def expr(terms):
    out = ""
    for c, var in terms:
        if F(c) == 0:
            continue
        out += term(c, var, first=(out == ""))
    return out or "0"


def ordinal(n):
    n = int(n)
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)
