# -*- coding: utf-8 -*-
"""
Shared helpers for UK Key Stage 3 generators (Years 7 to 9).
Builds on ws_common: British English, UK names, pounds and pence, and one make() that fills in
the KS3 standard fields. Negative numbers use the real minus sign (U+2212); 1,000 and above get commas.
"""
import random
from fractions import Fraction as F
from ws_common import (num, par, dec, frac, fr, comma, mcq, nums, balance, B, cap, fig, figure, svg_wrap, text,
                       line, table, number_line, write_unit, MINUS, GREEN, FILL, GRAY, INK, RED, BLUE, FONT, X)

UPDATED = "2026-11-17"
STD_URL = "https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study"
GIRLS = ["Amelia", "Olivia", "Isla", "Freya", "Poppy", "Ava", "Grace", "Aisha", "Maya", "Ruby", "Zara", "Evie"]
BOYS = ["Oliver", "Harry", "George", "Alfie", "Arjun", "Leo", "Jack", "Noah", "Ethan", "Kai", "Mohammed", "Theo"]
TIMES = "×"


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def gbp(v):
    """£3.50, £12, 75p (for amounts under £1)."""
    v = F(v)
    if 0 < v < 1:
        return "%dp" % int(v * 100)
    if v.denominator == 1:
        return "£" + comma(v)
    return "£" + comma(int(v)) + "." + ("%02d" % int(round((v - int(v)) * 100)))


def v(name):
    """Italic algebra letter."""
    return "<i>%s</i>" % name


def sq(x):
    return "%s²" % x


def collect(make_one, n, rnd, tries=4000):
    """Call make_one(rnd) until n items with different question text; make_one returns an item or None."""
    out, seen = [], set()
    for _ in range(tries):
        try:
            it = make_one(rnd)
        except AssertionError:
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
    """Body HTML in the order: how to think -> worked examples -> common mistakes."""
    h = "<h2>How it works</h2>" + think + extra
    for q, steps, ans in examples:
        h += ("<div class='sn-ex'><span class='sn-ex-t'>Example</span><p class='sn-ex-q'>%s</p>%s"
              "<p class='sn-ex-a'>Answer: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), ans))
    h += "<h2>Common mistakes</h2><ul>" + "".join("<li>%s</li>" % m for m in mistakes) + "</ul>"
    return h


STRANDS = {
    "N": "KS3: Number",
    "A": "KS3: Algebra",
    "R": "KS3: Ratio, proportion and rates of change",
    "G": "KS3: Geometry and measures",
    "P": "KS3: Probability",
    "S": "KS3: Statistics",
}
DOMAINS = {"N": "Number", "A": "Algebra", "R": "Ratio and Proportion", "G": "Geometry and Measures",
           "P": "Probability", "S": "Statistics"}


def make(year, slug, sort, strand, title, seo_title, short_title, std_text, meta, key_big, key_sub, body, faq, sets, rnd):
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
    assert len(sets) == 5
    balance(sets, rnd)
    unit = {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": DOMAINS[strand], "standard_code": STRANDS[strand], "standard_url": STD_URL,
        "standard_text": std_text, "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets,
        "pdf_url": "", "sort": sort, "updated": UPDATED,
    }
    write_unit("uk", "maths", "year-%d" % year, unit)


def opts(correct, wrongs, fmt=None):
    """Quick candidates: values -> (html, key). fmt turns a value into html (default num)."""
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
    """Text answers: every choice is plain html, compared as text."""
    return mcq(q, (correct, correct), [(x, x) for x in wrongs], e)


def QN(q, ans, wrongs, e, fmt=None, unit="", near=(1, -1, 2, -2, 10, -10)):
    """Number answer. Wrong values from mistakes first; if fewer than 3 differ, add near misses."""
    f = fmt or num
    ans = F(ans)
    ws = [F(w) for w in wrongs if w is not None] + [ans + d for d in near]
    cands = [(f(w) + unit, w) for w in ws if w != ans and f(w) is not None]
    return mcq(q, (f(ans) + unit, ans), cands, e)


def term(c, var, first=False):
    """One signed term: (3, 'x') -> ' + 3x'; (-1, 'x') -> ' − x'; (5, '') -> ' + 5'."""
    c = F(c)
    if c == 0:
        return ""
    mag = abs(c)
    body = (num(mag) if (mag != 1 or not var) else "") + var
    if first:
        return (MINUS if c < 0 else "") + body
    return (" %s " % (MINUS if c < 0 else "+")) + body


def expr(terms):
    """[(3,'<i>x</i>'), (-2,'')] -> '3x − 2'. Zero terms dropped; empty gives 0."""
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
