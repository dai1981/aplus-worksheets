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


SG_WORDS = [("Year 7", "Secondary 1"), ("Year 8", "Secondary 2"), ("Year 9", "Secondary 2"), ("KS3 ", ""), ("Key Stage 3", "secondary school"),
            ("the National Curriculum", "the MOE syllabus"), ("National Curriculum", "MOE syllabus"), ("GCSE", "O-Level"), ("pupils", "students")]


def sgify(s):
    for a, b in SG_WORDS:
        s = s.replace(a, b)
    return s


def make(level, slug, sort, code, title, seo_title, short_title, std_text, meta, key_big, key_sub, body, faq, sets, rnd):
    assert code in SUB, code
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
