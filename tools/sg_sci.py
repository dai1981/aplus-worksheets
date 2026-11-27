# -*- coding: utf-8 -*-
"""
Singapore science (MOE Primary Science Syllabus 2023): subject `science`, grade `primary-N` (Primary 3-6).
Builds on sci_common and uk_sci: British English (colour, metre, litre), Singapore names and places, and make_sg()
that fills in the standard fields: standard_code "Primary 6: Energy forms and uses (Photosynthesis)",
domain = the syllabus theme (Diversity / Cycles / Systems / Interactions / Energy), standard_url = the MOE syllabus page.
make_sg() checks the whole unit for American and UK-only words before it writes.
UK makers can be reused with adopt_uk(modname, U) and sgm(maker) (Singapore names, no UK-only words).
"""
import json
import re
import sci_common
import uk_sci
from sci_common import (Unit, item, bank, lesson, table, pick, bar_chart, pie, arrow, sun, rect, circle,
                        svg_wrap, text, line, fig, figure, B, cap, GREEN, BLUE, RED, INK, FILL, GRAY, FONT,
                        ORANGE, BROWN, SKY, SUN, LEAF)
from sg_sec import GIRLS, BOYS, People
from uk_sci import once, USED

STD_URL = "https://www.moe.gov.sg/primary/curriculum/syllabus"
THEMES = ("Diversity", "Cycles", "Systems", "Interactions", "Energy")

# words that must not appear on a Singapore page (US spellings from uk_sci, plus UK-only things)
LEAKS = uk_sci.LEAKS + ["year 3", "year 4", "year 5", "year 6", "ks2", "ks3", "gcse", "pence", "badger", "badgers", "hedgehog",
                        "hedgehogs", "slow worm", "slow worms", "newt", "newts", "conker", "conkers", "bonfire", "snowman", "sledge", "sledges", "nhs"]
LEAK_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in LEAKS), re.I)
# UK things that have a Singapore version
SG_REP = [(r"\ban oak tree", "a rain tree"), (r"woolly jumpers?", "woollen sweater"), (r"\bjumpers?\b", "sweater"), (r"\boak trees?\b", "rain tree"), (r"\ban oak\b", "a rain tree"),
          (r"\bin woodland\b", "in a forest"), (r"\bwoodland\b", "forest"), (r"\bwellies\b", "rain boots"), (r"\bwellington boots\b", "rain boots"),
          (r"\bpond skaters?\b", "water strider"), (r"\brobins\b", "sparrows"), (r"\brobin\b", "sparrow"),
          (r"\bplaytime\b", "recess"), (r"\bbiscuit tin\b", "biscuit tin")]
UK_NAMES = [n for n in uk_sci.GIRLS + uk_sci.BOYS if n not in GIRLS + BOYS]


def _bad(text):
    t = uk_sci._text_of(text)
    bad = {m.group(1).lower() for m in LEAK_RE.finditer(t)}
    if "£" in t:
        bad.add("£")
    return bad


def make_sg(level, slug, sort, theme, topic, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets, allow=()):
    """level: 3..6; theme: Diversity/Cycles/Systems/Interactions/Energy; topic: the syllabus topic
    ("Energy forms and uses (Photosynthesis)")."""
    assert theme in THEMES, theme
    blob = json.dumps([title, seo_title, short, meta, key_big, key_sub, body, faq, sets, std_text], ensure_ascii=False)
    bad = sorted(_bad(blob) - set(allow))
    assert not bad, "Words that do not fit Singapore: %s" % bad
    names = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in UK_NAMES))
    m = names.search(re.sub(r"<[^>]+>", " ", blob))
    assert not m, "UK name left: %s" % m.group(1)
    sci_common.make("primary-%d" % level, slug, sort, "Primary %d: %s" % (level, topic), std_text, title, seo_title, short, meta,
                    key_big, key_sub, body, faq, sets, domain=theme, country="sg", url=STD_URL)


# ---- reuse UK makers with Singapore names ----
_NAME_RE = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in sorted(UK_NAMES, key=len, reverse=True)))


_NR = __import__("random").Random(2023)


def sgm(f, rep=()):
    """wrap a UK (or US) maker: British spelling, Singapore names; drop the item if a word does not fit"""
    g0 = uk_sci.ukm(f)

    def g():
        it = g0()
        if it is None:
            return None
        it = dict(it)
        sub = {}

        def nm(m):
            k = m.group(1)
            if k not in sub:
                pool = [n for n in (GIRLS if k in uk_sci.GIRLS else BOYS) if n not in sub.values()]
                sub[k] = _NR.choice(pool)
            return sub[k]

        def fix(s):
            s = _NAME_RE.sub(nm, s)
            for a, b in list(SG_REP) + list(rep):
                s = re.sub(a, b, s)
            s = re.sub(r"\b([Aa])n (?=[bcdfgjklmnpqrstvwxyz])", lambda m: m.group(1) + " ", s)
            s = re.sub(r"(?<!\d )\b([Aa]) (?=(?!one\b|once\b|and\b|is\b|in\b|or\b|of\b|at\b|as\b|are\b|if\b)(?:[aeio][a-z]|hour\b))", lambda m: m.group(1) + "n ", s)
            return s
        it["q"], it["e"] = fix(it["q"]), fix(it["e"])
        it["c"] = [fix(c) for c in it["c"]]
        if _bad(json.dumps(it, ensure_ascii=False)) or len({c.strip().lower() for c in it["c"]}) < 4:
            return None
        return it
    g.__name__ = getattr(f, "__name__", "g")
    return g


def adopt_uk(modname, U):
    """import a UK science generator and point it at this unit"""
    import importlib
    m = importlib.import_module(modname)
    m.U = U
    m.R = U.R
    if hasattr(m, "P"):
        m.P = uk_sci.People(U.R)
    return m


class use:
    """S = use(U, "gen_uk_science_y3_magnets_attract_and_repel", rep=[...], drop=[...]):
    S.g_pic -> the UK maker with Singapore names (sgm); S.B1 -> list of its bank makers, wrapped the same way.
    drop: words (regex) that make an item leave out (topics outside the Singapore syllabus)."""

    def __init__(self, U, modname, rep=(), drop=()):
        self.m = adopt_uk(modname, U)
        self.rep = rep
        self.drop = re.compile("|".join(drop), re.I) if drop else None

    def _w(self, f):
        g = sgm(f, self.rep)
        if not self.drop:
            return g

        def h():
            it = g()
            if it and self.drop.search(re.sub(r"<[^>]+>", " ", json.dumps(it, ensure_ascii=False))):
                return None
            return it
        h.__name__ = g.__name__
        return h

    def __getattr__(self, name):
        obj = getattr(self.m, name)
        if isinstance(obj, list):
            return [self._w(f) for f in obj]
        return self._w(obj)


def upto(f, n):
    """let maker f give at most n items in the whole unit (so a numeric maker does not fill the sets)"""
    box = [0]

    def g():
        if box[0] >= n:
            return None
        it = f()
        if it:
            box[0] += 1
        return it
    g.__name__ = getattr(f, "__name__", "g")
    return g
