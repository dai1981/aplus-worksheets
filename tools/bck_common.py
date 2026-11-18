# -*- coding: utf-8 -*-
"""
Shared helpers for the BC Kindergarten units (gen_cabc_math_k_*.py).
Kindergarten in British Columbia, ages 5 to 6. Numbers to 10. Very short sentences and a picture in almost every
question. Built on the US Kindergarten pictures (k_pics), the k_common question helpers and the AU Foundation
pictures (f_common), with Canadian English (colour, centre, favourite), Canadian names and BC contexts.
"""
import re
import k_pics
from k_common import mcq as k_mcq

LIMIT = [10]


def _ok(c):
    toks = re.findall(r"\d+", re.sub("<[^>]+>", "", str(c)))
    return all(int(t) <= LIMIT[0] for t in toks)


def mcq(q, correct, cands, e, allow_zero=False):
    """k_common.mcq, dropping wrong answers with numbers bigger than the unit's limit (10)."""
    return k_mcq(q, correct, [c for c in cands if c is not None and _ok(c)], e, allow_zero)
from ws_common import write_unit, table

UPDATED = "2026-11-18"
STD_URL = "https://curriculum.gov.bc.ca/curriculum/mathematics/k/core"
PEOPLE = [("Ava", "she", "her"), ("Liam", "he", "his"), ("Maya", "she", "her"), ("Ethan", "he", "his"),
          ("Chloe", "she", "her"), ("Noah", "he", "his"), ("Harper", "she", "her"), ("Arjun", "he", "his"),
          ("Mei", "she", "her"), ("Owen", "he", "his"), ("Sofia", "she", "her"), ("Jayden", "he", "his"),
          ("Amira", "she", "her"), ("Lucas", "he", "his"), ("Hana", "she", "her"), ("Ryan", "he", "his")]

k_pics.NAMES["bug"] = ("ladybug", "ladybugs")


class Kids:
    def __init__(self, rnd):
        self.pool = PEOPLE[:]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return dict(n=p[0], he=p[1], He=p[1].capitalize(), his=p[2], His=p[2].capitalize())


CA_WORDS = [("colors", "colours"), ("color", "colour"), ("Color", "Colour"), ("favorite", "favourite"), ("center", "centre"),
            ("gray", "grey"), ("ladybird", "ladybug"), ("Foundation", "Kindergarten"), ("maths", "math"), ("Maths", "Math")]


def ca(s):
    for a, b in CA_WORDS:
        s = s.replace(a, b)
    s = re.sub(r"\bThere are 1 (dot|canoe|duck|kayak|eagle|ladybug|star|apple|ball|button|fish|flower|heart|cup)s?\b", r"There is 1 \1", s)
    s = s.replace("There are 1 ", "There is 1 ").replace(" 1 dots", " 1 dot")
    return s


def collect(maker, n, rnd, tries=3000):
    """Call maker(rnd) until n different questions are made."""
    out, seen = [], set()
    for _ in range(tries):
        try:
            it = maker(rnd)
        except AssertionError:
            continue
        if not it:
            continue
        key = it["q"] + "|" + "|".join(sorted(it["c"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
        if len(out) == n:
            return out
    raise AssertionError("only %d items from %s" % (len(out), maker.__name__))


def S(title, items):
    return {"title": title, "items": items}


def balance(sets, rnd):
    """Each answer position is correct 5 times in a set. Items marked _fixed (choices A to D for parts of one
    picture) keep their order."""
    for s in sets:
        assert len(s["items"]) == 20, (s["title"], len(s["items"]))
        targets = [0, 1, 2, 3] * 5
        for it in s["items"]:
            if it.get("_fixed") and it["a"] in targets:
                targets.remove(it["a"])
        rnd.shuffle(targets)
        k = 0
        for it in s["items"]:
            if it.pop("_fixed", False):
                continue
            t = targets[k]
            k += 1
            c = it["c"]
            wrong = [x for i, x in enumerate(c) if i != it["a"]]
            rnd.shuffle(wrong)
            it["c"] = wrong[:t] + [c[it["a"]]] + wrong[t:]
            it["a"] = t


class Cycle:
    """Positions 0, 1, 2, 3, 0, 1, ... so that lettered picture answers are spread evenly."""
    def __init__(self):
        self.i = 0

    def next(self):
        self.i += 1
        return (self.i - 1) % 4


def letters(it, letter, labels=None):
    """Turn an item into an A-D picture question whose choices stay in order."""
    it["c"] = list(labels or "ABCD")
    it["a"] = it["c"].index(letter)
    it["_fixed"] = True
    return it


def fix_letter_choices(sets):
    """Picture questions answered with A, B, C, D keep the letters in order (any extra choice goes last)."""
    for s in sets:
        for it in s["items"]:
            if it.get("_fixed"):
                continue
            lets = [c for c in it["c"] if c in ("A", "B", "C", "D")]
            if len(lets) >= 2 and all(c in ("A", "B", "C", "D") or c.startswith("They ") or c.startswith("We cannot") for c in it["c"]):
                ans = it["c"][it["a"]]
                it["c"] = sorted(lets) + [c for c in it["c"] if c not in lets]
                it["a"] = it["c"].index(ans)
                it["_fixed"] = True


def finish(sets, rnd, max_num=10, extra_ok=()):
    fix_letter_choices(sets)
    balance(sets, rnd)
    seen = set()
    for s in sets:
        s["title"] = ca(s["title"])
        for it in s["items"]:
            key = it["q"] + "|".join(sorted(it["c"]))
            assert key not in seen, it["q"][-100:]
            seen.add(key)
            for c in it["c"]:
                for tok in re.findall(r"\d+", re.sub("<[^>]+>", "", c)):
                    assert int(tok) <= max_num or int(tok) in extra_ok, (c, it["q"][-80:])
            it["q"] = ca(it["q"]).replace("<svg ", "<svg data-pf='lg' ")
            it["c"] = [ca(c) for c in it["c"]]
            it["e"] = ca(it["e"])
    return sets


def make(slug, sort, domain, title, short_title, std_text, meta, key_big, key_sub, body, faq, sets, seo_title=None):
    seo = seo_title or "Kindergarten %s Worksheets: Free Math with Pictures and Answers (BC Curriculum)" % short_title
    unit = {
        "slug": slug, "sort": sort, "updated": UPDATED, "pdf_url": "",
        "title": title, "seo_title": seo, "short_title": short_title, "domain": domain,
        "standard_code": "Kindergarten: %s" % domain, "standard_url": STD_URL, "standard_text": std_text,
        "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": ca(body), "faq": [{"q": ca(q), "a": ca(a)} for q, a in faq], "sets": sets,
    }
    write_unit("ca-bc", "math", "kindergarten", unit)


def fig(svg):
    return "<div class='qfig'>" + svg + "</div>"


def figure(svg, cap):
    return "<figure class='sn-fig'>%s<figcaption>%s</figcaption></figure>" % (svg, cap)


def lesson(think, examples, mistakes_rows):
    """Think → example pictures → common mistakes, in short sentences."""
    h = "<h2>How to think about it</h2>" + think
    h += "<h2>Examples</h2>" + "".join(examples)
    h += "<h2>Common mistakes</h2>" + table(["Mistake", "What to do"], mistakes_rows)
    return h


def plain(s):
    return re.sub("<[^>]+>", "", s)
