# -*- coding: utf-8 -*-
"""
Shared helpers for India (CBSE / NCERT Mathematics). Same API as sg_sec and uk_ks3, with Indian conventions:
- numbers: Indian grouping 4,536; 12,345; 1,23,456 (lakh); 1,23,45,678 (crore)
- money: ₹250, ₹1,250, ₹45.50
- British/Indian English (colour, metre, centre, maths, zeroes, factorisation), Indian names and places
- π is usually given as 22/7 (as in NCERT exercises)
make() writes content/in/maths/class-N/{slug}.json with the CBSE unit and NCERT chapter.
adopt() reuses question makers from other countries' generators with Indian names, money and numbers;
ok() drops questions that still contain words from other countries.
"""
import re
from fractions import Fraction as F
import ws_common
from ws_common import (par, frac, fr, mcq, balance, B, cap, fig, figure, svg_wrap, text,
                       line, table, number_line, write_unit, MINUS, GREEN, FILL, GRAY, INK, RED, BLUE, FONT, X)


def comma(n):
    """Indian grouping: 4,536 / 12,345 / 1,23,456 / 1,23,45,678."""
    n = int(n)
    s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return ("-" if n < 0 else "") + s


ws_common.comma = comma
from ws_common import dec, num, nums   # noqa: E402

UPDATED = "2026-11-22"
STD_URL = "https://www.cbseacademic.nic.in/web_material/CurriculumMain26/Sec/Maths_Sec_2025-26.pdf"
GIRLS = ["Priya", "Ananya", "Diya", "Meera", "Sneha", "Kavya", "Isha", "Riya", "Aditi", "Pooja", "Nisha", "Shreya"]
BOYS = ["Aarav", "Rohan", "Arjun", "Kabir", "Vivaan", "Ishaan", "Rahul", "Aditya", "Karan", "Siddharth", "Nikhil", "Dev"]
PLACES = ["Delhi", "Mumbai", "Jaipur", "Chennai", "Kolkata", "Pune", "Lucknow", "Bhopal", "Kochi", "Indore", "Patna", "Nagpur"]
TIMES = "×"

# words from other countries' generators that must not appear in Indian questions
LEAKS = ["$", "£", "€", "¢", " R1", "GST", "VAT", "HST", "pence", "penny", "cents", "dollar", "pound", "euro",
         "Singapore", "Sentosa", "Jurong", "Tampines", "Woodlands", "Changi", "Bishan", "Punggol", "Clementi", "MRT", "hawker",
         "Secondary", "Sec ", "O-Level", "MOE", "GCSE", "KS3", "Year 7", "Year 8", "Year 9", "Grade ", "pupils",
         "London", "Manchester", "Texas", "Sydney", "Toronto", "Cape Town", "miles", "mile ", "inch", "feet", "yard", "pint", "gallon", "ounce", "lb",
         "Fahrenheit", "°F", "snow", "hockey", "Wei", "Jun Jie", "Siti", "Mei", "Hui", "Nurul", "Xin", "Zhi", "Hafiz", "Ahmad", "Imran", "Marcus", "Farah", "Rachel", "Daniel", "Ethan",
         "None", "nan"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def inr(v):
    """₹250, ₹1,250, ₹45.50, ₹1,25,000."""
    v = F(v)
    neg = v < 0
    v = abs(v)
    if v.denominator == 1:
        out = "₹" + comma(v)
    else:
        c = int(v * 100 + F(1, 2))
        out = "₹" + comma(c // 100) + "." + ("%02d" % (c % 100))
    return (MINUS if neg else "") + out


def v(name):
    return "<i>%s</i>" % name


def plain(s):
    return re.sub(r"<[^>]*>", " ", s)


def ok(it):
    if it is None:
        return False
    t = it["q"] + " " + " ".join(it["c"]) + " " + it["e"]
    t = re.sub(r"aria-label='[^']*'", "", t)
    p = plain(t)
    for w in LEAKS:
        if (re.search(r"\b%s\b" % re.escape(w.strip()), p) if w.strip().isalpha() else w in p):
            return False
    if any(re.search(r"\d\.\d{4,}", plain(c)) for c in it["c"]):
        return False
    return len(set(it["c"])) == 4


def collect(make_one, n, rnd, tries=6000, seen=None):
    out = []
    seen = set() if seen is None else seen
    for _ in range(tries):
        try:
            it = make_one(rnd)
        except (AssertionError, TypeError, ValueError, ZeroDivisionError, IndexError, KeyError):
            continue
        if not ok(it):
            continue
        key = re.sub(r"\b(%s)\b" % "|".join(GIRLS + BOYS), "N", it["q"])
        key = re.sub(r"\b(he|she|his|her|him)\b", "P", key)
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
        if len(out) == n:
            return out
    raise AssertionError("only %d items from %s" % (len(out), getattr(make_one, "__name__", "?")))


def mix(rnd, parts, seen):
    """parts: [(make_one, n)] -> 20 items, shuffled"""
    items = []
    for f, n in parts:
        items += collect(f, n, rnd, seen=seen)
    rnd.shuffle(items)
    return items


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


UNITS = {"I": "Number Systems", "II": "Algebra", "III": "Coordinate Geometry", "IV": "Geometry",
         "V": "Trigonometry", "VI": "Mensuration", "VII": "Statistics and Probability"}

IN_WORDS = [("Secondary 1", "Class 8"), ("Secondary 2", "Class 9"), ("Secondary 3", "Class 10"), ("Secondary 4", "Class 10"),
            ("the MOE syllabus", "the CBSE syllabus"), ("MOE syllabus", "CBSE syllabus"), ("O-Level", "board exam"),
            ("pupils", "students"), ("learners", "students"), ("zeros", "zeroes"), ("factorization", "factorisation"),
            ("simultaneous linear equations", "pair of linear equations"), ("Simultaneous linear equations", "Pair of linear equations")]


def indify(s):
    for a, b in IN_WORDS:
        s = s.replace(a, b)
    return s


def make(level, slug, sort, unit, chapter, title, short_title, std_text, meta, key_big, key_sub, body, faq, sets, rnd):
    """unit: CBSE unit number ('I'..'VII'), chapter: NCERT chapter number"""
    assert unit in UNITS, unit
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
    assert len(sets) == 5
    balance(sets, rnd)
    def minus(t):
        parts = re.split(r"(<svg.*?</svg>)", t)
        return "".join(p if p.startswith("<svg") else re.sub(r"(?<=[\s=(>])-(?=\d)", MINUS, p) for p in parts)
    one = lambda t: minus(indify(re.sub(r"(?<![\d.,/])\b1 (hour|minute|second|day|week|year|rupee|litre|metre)s\b", r"1 \1", t)))
    for s in sets:
        for it in s["items"]:
            m = re.match(r"(<svg.*?</svg>)(.*)$", it["q"], re.S)
            if m:   # a figure written before the question goes after it, in a figure box
                it["q"] = m.group(2) + fig(m.group(1))
            it["q"] = re.sub(r"<svg (?!data-pf)", "<svg data-pf='lg' ", it["q"])   # figures print large
            it["q"], it["e"] = one(it["q"]), one(it["e"])
            it["c"] = [one(c) for c in it["c"]]
    seo_title = "%s Class %d Worksheet with Answers (NCERT Chapter %d)" % (title.split(":")[0], level, chapter)
    unit_json = {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": UNITS[unit], "standard_code": "Class %d, Chapter %d: %s" % (level, chapter, title.split(":")[0]),
        "standard_url": STD_URL, "standard_text": std_text, "meta_desc": indify(meta), "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": indify(q), "a": indify(a)} for q, a in faq], "sets": sets,
        "pdf_url": "", "sort": sort, "updated": UPDATED,
    }
    write_unit("in", "maths", "class-%d" % level, unit_json)


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


def fv(val):
    """exact value: integer or fraction html (negative with −)"""
    val = F(val)
    if val.denominator == 1:
        return num(val.numerator)
    s = MINUS if val < 0 else ""
    return s + fr(str(abs(val.numerator)), str(val.denominator))


def adopt(mod, rnd):
    """Reuse question makers from another country's generator with Indian names, money and numbers."""
    ws_common.comma = comma
    for name in ("gbp", "aud", "usd", "cad", "sgd", "rand"):
        if hasattr(mod, name):
            setattr(mod, name, inr)
    if hasattr(mod, "comma"):
        mod.comma = comma
    if hasattr(mod, "People"):
        mod.People = People
    if hasattr(mod, "P"):
        mod.P = People(rnd)
    for name in ("PLACES", "CITIES", "TOWNS"):
        if hasattr(mod, name):
            setattr(mod, name, list(PLACES))
    for name in ("GIRLS", "BOYS"):
        if hasattr(mod, name):
            setattr(mod, name, list(GIRLS if name == "GIRLS" else BOYS))
    return mod
