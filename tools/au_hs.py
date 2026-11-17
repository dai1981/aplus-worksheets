# -*- coding: utf-8 -*-
"""
Shared helpers for AU Years 7 and 8 (Australian Curriculum v9.0, Mathematics).
Same API as uk_ks3 so the generators read the same way, with Australian conventions:
- numbers: 4 digits with no separator (4536); 5 digits and more grouped with a no-break space (10 000)
- money: $ and c (no 1c or 2c coins, so cash amounts end in 0 or 5 cents); GST is 10%
- Australian English (colour, metre, maths, students), Australian names
make() takes the v9 content description code (for example AC9M7N01) and its original text.
"""
import random
from fractions import Fraction as F
import ws_common
from ws_common import (par, frac, fr, mcq, balance, B, cap, fig, figure, svg_wrap, text,
                       line, table, number_line, write_unit, MINUS, GREEN, FILL, GRAY, INK, RED, BLUE, FONT, X)

NBSP = " "


def comma(n):
    """Australian grouping: 4536, 10 000 (no-break space)."""
    n = int(n)
    return str(n) if abs(n) < 10000 else "{:,}".format(n).replace(",", NBSP)


ws_common.comma = comma          # every ws_common helper (dec, num, number_line) now groups the Australian way
from ws_common import dec, num, nums   # noqa: E402  (they look up comma at call time)

UPDATED = "2026-11-18"
STD_URL = "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/mathematics"
GIRLS = ["Charlotte", "Isla", "Mia", "Amelia", "Harper", "Chloe", "Ruby", "Mei", "Zara", "Matilda", "Sienna", "Priya"]
BOYS = ["Oliver", "Jack", "Noah", "William", "Lachlan", "Liam", "Aarav", "Kai", "Cooper", "Ethan", "Hamish", "Tom"]
TIMES = "×"
CITIES = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Hobart", "Darwin", "Canberra"]


class People:
    def __init__(self, rnd):
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p


def aud(v):
    """$3.50, $12, 75c (amounts under $1), $12 500."""
    v = F(v)
    if 0 < v < 1:
        return "%dc" % int(v * 100)
    if v.denominator == 1:
        return "$" + comma(v)
    return "$" + comma(int(v)) + "." + ("%02d" % int(round((v - int(v)) * 100)))


gbp = aud  # ported code may still call gbp


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


DOMAIN = [("SP", "Space"), ("ST", "Statistics"), ("N", "Number"), ("A", "Algebra"), ("M", "Measurement"), ("P", "Probability")]


def domain_of(code):
    tail = code[5:]  # AC9M7 + strand + nn
    for k, name in DOMAIN:
        if tail.startswith(k):
            return name
    raise ValueError(code)


def make(year, slug, sort, code, title, seo_title, short_title, std_text, meta, key_big, key_sub, body, faq, sets, rnd):
    assert code.startswith("AC9M%d" % year), code
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
    assert len(sets) == 5
    balance(sets, rnd)
    unit = {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": domain_of(code), "standard_code": code, "standard_url": STD_URL,
        "standard_text": std_text, "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets,
        "pdf_url": "", "sort": sort, "updated": UPDATED,
    }
    write_unit("au", "maths", "year-%d" % year, unit)


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
