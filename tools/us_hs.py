# -*- coding: utf-8 -*-
"""
Shared helpers for US Algebra 1 (Common Core State Standards, high school).
Same API as uk_ks3 and au_hs, so generators ported from those read the same way, with US conventions:
- numbers: commas from 1,000 (ws_common's own comma)
- money: $3.50 (no cent sign)
- US English (color, factor, parentheses, students), American names
make() takes the CCSS high school code (for example A-REI.B.3) and builds the standard URL and the
domain (the conceptual category) from it.
"""
import random
from fractions import Fraction as F
import ws_common
from ws_common import (par, frac, fr, mcq, balance, B, cap, fig, figure, svg_wrap, text,
                       line, table, number_line, write_unit, MINUS, GREEN, FILL, GRAY, INK, RED, BLUE, FONT, X)

from ws_common import dec, num, nums, comma   # noqa: E402  (US commas: 1,000)

UPDATED = "2026-11-18"
GIRLS = ["Emma", "Olivia", "Sofia", "Ava", "Maya", "Chloe", "Zoe", "Mei", "Aaliyah", "Grace", "Isabella", "Priya"]
BOYS = ["Liam", "Noah", "Mateo", "Ethan", "Jayden", "Lucas", "Marcus", "Kai", "Diego", "Owen", "Caleb", "Andre"]
TIMES = "×"
CITIES = ["Chicago", "Houston", "Phoenix", "Denver", "Atlanta", "Seattle", "Boston", "Miami"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def usd(v):
    """$3.50, $12, $0.75, $12,500."""
    v = F(v)
    neg = v < 0
    v = abs(v)
    if v.denominator == 1:
        out = "$" + comma(v)
    else:
        c = int(round(v * 100))
        out = "$" + comma(c // 100) + "." + ("%02d" % (c % 100))
    return (MINUS if neg else "") + out


aud = gbp = usd  # ported code may still call aud or gbp


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


DOMAIN = {"N": "Number & Quantity", "A": "Algebra", "F": "Functions", "S": "Statistics & Probability", "G": "Geometry"}


def std_url(code):
    """A-REI.B.3 -> https://www.thecorestandards.org/Math/Content/HSA/REI/B/3/"""
    cat, rest = code.split("-", 1)
    parts = rest.split(".")
    return "https://www.thecorestandards.org/Math/Content/HS%s/%s/" % (cat, "/".join(parts))


def make(slug, sort, code, title, seo_title, short_title, std_text, meta, key_big, key_sub, body, faq, sets, rnd, domain=None, grade="algebra-1"):
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
    assert len(sets) == 5
    balance(sets, rnd)
    unit = {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": domain or DOMAIN[code[0]], "standard_code": code, "standard_url": std_url(code),
        "standard_text": std_text, "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets,
        "pdf_url": "", "sort": sort, "updated": UPDATED,
    }
    write_unit("us", "math", grade, unit)


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
