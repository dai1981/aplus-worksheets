# -*- coding: utf-8 -*-
"""
Australian science (Australian Curriculum v9.0, Science F-10): subject `science`, grade `foundation` / `year-N`.
  AU(seed) -> (U, R, P, src)
    src("gen_uk_science_y6_how_light_travels", "g_x", rep=[(regex, new)], drop=[regex]) adopts any UK, US, SG or IN science
    maker with Australian names, Australian English (colour, metre, students, trucks, lollies) and Australian things
    (gum trees, possums, bushland); src.B("module", "B1") gives a bank list. Every loaded generator module is pointed at this
    unit (U, R, P), so the seed is ours.
  make_au(year, slug, sort, code, strand, std, title, short, meta, kb, ks, think, ex, mist, faq, sets)
    year 0 = Foundation; standard_code is the v9 code ("AC9S5U03"), domain is the strand ("Physical sciences"),
    seo_title "Year 5 Science: Light and Shadows Worksheets (Australian Curriculum)".
Numbers are written the Australian way (4536, 10 000) and checked for words that do not fit Australia (US spellings,
pence, Singapore, NHS ...). Seasons are the southern ones, so items that put winter in December or summer in July are dropped.
Seeds: 66000 + 100 * year + sort.
"""
import json
import re
import sys
import importlib
import random as _random
import sci_common
import uk_sci
from sci_common import (Unit, item, bank, lesson, kid_lesson, table, svg_wrap, text, line, fig, B, cap,
                        GREEN, BLUE, RED, INK, FILL, GRAY, FONT, ORANGE, BROWN, SKY, SUN, LEAF, rect, circle, arrow, sun, bar_chart, pie)
from uk_sci import once, USED
from au_hs import GIRLS, BOYS, People, CITIES
from sg_lss import sgnum
from uk_alsci import nf, tq
import uk_alsci

STD_URL = "https://v9.australiancurriculum.edu.au/f-10-curriculum/learning-areas/science"
STRANDS = ("Biological sciences", "Chemical sciences", "Earth and space sciences", "Physical sciences",
           "Science as a human endeavour", "Science inquiry")

# words that must not appear on an Australian page
LEAKS = [w for w in uk_sci.LEAKS if w not in ("recess",)] + [
    "pupil", "pupils", "lorry", "lorries", "pence", "penny", "badger", "badgers", "hedgehog", "hedgehogs", "conker", "conkers", "squirrel",
    "squirrels", "nhs", "gcse", "ks1", "ks2", "ks3", "ks4", "o-level", "psle", "singapore", "mrt", "hawker", "handphone", "rupee", "rupees",
    "india", "britain", "england", "london", "scotland", "uk", "usa", "america", "american", "texas", "ngss", "cbse", "ncert",
    "bonfire", "slow worm", "slow worms", "newt", "newts", "jaywalking", "snowman", "sledge", "sledges", "rain tree", "mangrove swamp in singapore",
    "fahrenheit", "grade 1", "grade 2", "grade 3", "grade 4", "grade 5", "grade 6", "grade 7", "grade 8"]
LEAK_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in LEAKS), re.I)
# northern-hemisphere seasons
SEASON_RE = re.compile(r"\b(December|January|February|Christmas)\b[^.?!]{0,60}\b(winter|snow\w*|freezing)\b|\b(winter|snow\w*)\b[^.?!]{0,60}\b(December|January|February|Christmas)\b"
                       r"|\b(June|July|August)\b[^.?!]{0,60}\b(summer|hottest|heatwave)\b|\b(summer|hottest)\b[^.?!]{0,60}\b(June|July|August)\b", re.I)

AU_REP = [(r"\bbar charts\b", "column graphs"), (r"\bbar chart\b", "column graph"), (r"\bBar charts\b", "Column graphs"), (r"\bBar chart\b", "Column graph"), (r"\bpracticing\b", "practising"), (r"\bPracticing\b", "Practising"), (r"\bpupils\b", "students"), (r"\bPupils\b", "Students"), (r"\bpupil's\b", "student's"), (r"\bpupil\b", "student"), (r"\bPupil\b", "Student"),
          (r"\blorries\b", "trucks"), (r"\blorry\b", "truck"), (r"\bsweets\b", "lollies"), (r"\bsweet wrappers\b", "lolly wrappers"),
          (r"\bwellies\b", "gumboots"), (r"\bwellington boots\b", "gumboots"), (r"\bin woodland\b", "in bushland"), (r"\bwoodlands?\b", "bushland"),
          (r"\ban oak tree\b", "a gum tree"), (r"\boak trees\b", "gum trees"), (r"\boak tree\b", "gum tree"), (r"\ban oak\b", "a gum tree"), (r"\boaks\b", "gum trees"),
          (r"\brain trees?\b", "gum tree"), (r"\bhedgehogs\b", "echidnas"), (r"\bhedgehog\b", "echidna"), (r"\bsquirrels\b", "possums"), (r"\bsquirrel\b", "possum"),
          (r"\bbadgers\b", "wombats"), (r"\bbadger\b", "wombat"), (r"\brobins\b", "magpies"), (r"\brobin\b", "magpie"), (r"\bsweaters?\b", "jumper"),
          (r"\bhandphones?\b", "mobile phone"), (r"\bplaytime\b", "recess"), (r"\bSecondary (\d)\b", "Year \\1"), (r"\bmol L⁻¹", "mol/L"),
          (r"\bmol dm⁻³", "mol/L"), (r"\bmol/dm³", "mol/L"), (r"\bdm³", "L"),
          (r"\bcoloring\b", "colouring"), (r"\bColoring\b", "Colouring")]

# names from other countries' generators -> Australian names (same gender)
import ws_common as _ws  # noqa: E402
import sg_sec as _sg  # noqa: E402
import in_common as _in  # noqa: E402
_G = set(uk_sci.GIRLS) | set(_ws.GIRLS) | set(_sg.GIRLS) | set(_in.GIRLS)
_Bo = set(uk_sci.BOYS) | set(_ws.BOYS) | set(_sg.BOYS) | set(_in.BOYS)
FOREIGN = sorted((_G | _Bo) - set(GIRLS) - set(BOYS), key=len, reverse=True)
_NAME_RE = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in FOREIGN))
_NR = _random.Random(2024)


_EYE = re.compile(r"\b(eyes?|iris|retina|cornea|lens|optic)\b", re.I)


def _bad(text):
    t = uk_sci._text_of(text)
    bad = {m.group(1).lower() for m in LEAK_RE.finditer(t)}
    if _EYE.search(t):
        bad -= {"pupil", "pupils"}
    if "£" in t or "₹" in t:
        bad.add("£/₹")
    if SEASON_RE.search(t):
        bad.add("northern seasons")
    return bad


def _fix_an(s):
    s = re.sub(r"\b([Aa])n (?=[bcdfgjklmnpqrstvwxyz])", lambda m: m.group(1) + " ", s)
    s = re.sub(r"(?<!\d )\b([Aa]) (?=(?!one\b|once\b|and\b|is\b|in\b|or\b|of\b|at\b|as\b|are\b|if\b|on\b|eu|uni|use)(?:[aeiou][a-z]|hour\b))",
               lambda m: m.group(1) + "n ", s)
    return s


def aum(f, rep=()):
    """wrap a UK/US/SG/IN maker: British spelling first, then Australian names, words and things; None if a word does not fit"""
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
                pool = [n for n in (GIRLS if k in _G else BOYS) if n not in sub.values()]
                sub[k] = _NR.choice(pool)
            return sub[k]

        eye = bool(_EYE.search(uk_sci._text_of(json.dumps(it, ensure_ascii=False))))

        def fx(s):
            s = _NAME_RE.sub(nm, s)
            for a, b in list(AU_REP) + list(rep):
                if eye and "upil" in a:
                    continue
                s = re.sub(a, b, s)
            return _fix_an(s)
        it["q"], it["e"] = fx(it["q"]), fx(it["e"])
        it["c"] = [fx(c) for c in it["c"]]
        if _bad(json.dumps(it, ensure_ascii=False)) or len({c.strip().lower() for c in it["c"]}) < 4:
            return None
        if not _seen_once(it):
            return None
        return it
    g.__name__ = getattr(f, "__name__", "g")
    return g


SEEN = set()
_ALLN = None


def _seen_once(it):
    """drop items whose question (names and numbers removed) and correct answer were already used in this unit"""
    global _ALLN
    if _ALLN is None:
        _ALLN = re.compile(r"\b(%s)\b('s)?" % "|".join(sorted(_G | _Bo | set(GIRLS) | set(BOYS), key=len, reverse=True)))
    q = re.sub(r"<(table|svg|figure)\b.*?</\1>", " ", it["q"], flags=re.S)
    q = re.sub(r"\d+(\.\d+)?", "#", _ALLN.sub("N", re.sub(r"<[^>]+>", " ", q)))
    k = (" ".join(q.split()).lower(), it["c"][it["a"]].lower())
    if k in SEEN:
        return False
    SEEN.add(k)
    return True


_mods = {}


class _Src:
    def __init__(self, U, P):
        self.U, self.P = U, P

    def _mod(self, name):
        if name not in _mods:
            _mods[name] = importlib.import_module(name)
        self.sync()
        return _mods[name]

    def sync(self):
        for k, m in list(sys.modules.items()):
            if m is None or not (k.startswith("gen_") or k.startswith("al_") or k in ("sci_foodweb",)):
                continue
            if hasattr(m, "R"):
                m.R = self.U.R
            if hasattr(m, "U") and isinstance(getattr(m, "U"), sci_common.Unit):
                m.U = self.U
            if hasattr(m, "P") and hasattr(m.P, "next"):
                try:
                    m.P = type(m.P)(self.U.R)
                except TypeError:
                    pass

    def wrap(self, f, rep=(), drop=()):
        g0 = aum(f, rep)
        dr = re.compile("|".join(drop), re.I) if drop else None

        def g():
            self.sync()
            it = g0()
            if it is None:
                return None
            if dr and dr.search(re.sub(r"<[^>]+>", " ", json.dumps(it, ensure_ascii=False))):
                return None
            return it
        g.__name__ = getattr(f, "__name__", "g")
        return g

    def __call__(self, mod, name, rep=(), drop=()):
        return self.wrap(getattr(self._mod(mod), name), rep, drop)

    def B(self, mod, name, rep=(), drop=()):
        """a bank (list of makers) as one maker that picks a random row; the unit drops repeats"""
        fs = [self.wrap(f, rep, drop) for f in getattr(self._mod(mod), name)]
        U = self.U

        def g():
            return U.R.choice(fs)()
        g.n = len(fs)
        return g

    def mod(self, name):
        return self._mod(name)


def AU(seed):
    U = Unit(seed)
    R = U.R
    P = People(R)
    uk_sci.USED.clear()
    SEEN.clear()
    return U, R, P, _Src(U, P)


def seed_of(year, sort):
    return 66000 + 100 * year + sort


def _fixnums(sets):
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"] = sgnum(it["q"]), sgnum(it["e"])
            it["c"] = [sgnum(c) for c in it["c"]]
    return sets


def grade_of(year):
    return "foundation" if year == 0 else "year-%d" % year


def label(year):
    return "Foundation" if year == 0 else "Year %d" % year


def make_au(year, slug, sort, code, strand, std_text, title, short, meta, key_big, key_sub, think, ex, mist, faq, sets,
            allow=(), seo=None, pic=None):
    """pic: for Foundation-Year 2 a picture for kid_lesson (think is then (lead, [points]))."""
    assert strand in STRANDS, strand
    sets = _fixnums(sets)
    if pic is not None:
        lead, points = think
        body = kid_lesson(pic, lead, points, ex, mist)
    else:
        body = lesson(think, ex, mist)
    body = sgnum(body)
    seo = seo or "%s Science: %s Worksheets (Australian Curriculum)" % (label(year), title)
    if len(seo) > 95:
        seo = "%s Science: %s Worksheets" % (label(year), title)
    if year <= 2:
        assert len(title) <= 40 and len(key_big) <= 40 and len(key_sub) <= 90, (title, key_big, key_sub)
    blob = json.dumps([title, seo, short, meta, key_big, key_sub, body, faq, sets, std_text], ensure_ascii=False)
    bad = sorted(_bad(blob) - set(allow))
    assert not bad, "Words that do not fit Australia: %s" % bad
    m = _NAME_RE.search(re.sub(r"<[^>]+>", " ", blob))
    assert not m, "Foreign name left: %s" % m.group(1)
    sci_common.make(grade_of(year), slug, sort, code, std_text, title, seo, short, meta, key_big, key_sub, body, faq, sets,
                    domain=strand, country="au", url=STD_URL)


# ---- small makers (same as sg_ol) ----
_TZ = re.compile(r"(\d\.\d*?[1-9])0+(?!\d)|(\d)\.0+(?!\d)")


def trim(s):
    return _TZ.sub(lambda m: m.group(1) or m.group(2), s)


def nq(q, val, wrongs, unit, e, sf=3, keep=False):
    it = uk_alsci.nq(q, val, wrongs, unit, e, sf)
    if it is None or keep:
        return it
    c = [trim(x) for x in it["c"]]
    if len({x.lower() for x in c}) < 4:
        return None
    it["c"] = c
    it["e"] = trim(it["e"])
    return it


def ex(x):
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    if isinstance(x, int):
        return str(x)
    return trim("%.6f" % x)


def rows(R, rs, fwd, back=None, extra=()):
    """two-way fact table maker: rs = [(a, b) or (a, b, why)]"""
    rs = [r if len(r) == 3 else (r[0], r[1], "") for r in rs]

    def f():
        a, b, e = R.choice(rs)
        if back and R.random() < 0.5:
            others = sorted({x for x, y, _ in rs if y != b})
            if len(others) < 3:
                return None
            return tq(back % b, a, R.sample(others, 3), e or "%s: %s." % (a[0].upper() + a[1:], b.rstrip(".")))
        others = sorted(({y for x, y, _ in rs if y != b} | set(extra)) - {b})
        if len(others) < 3:
            return None
        return tq(fwd % a, b, R.sample(others, 3), e or "%s: %s." % (a[0].upper() + a[1:], b.rstrip(".")))
    return f


def pool(R, rs):
    """a maker that returns a random hand-written row (q, a, [w, w, w], e); the unit drops repeats"""
    its = [item(*r) for r in rs]

    def f():
        import copy
        return copy.deepcopy(R.choice(its))
    f.n = len(its)
    return f


def keep(f, pred):
    def g():
        it = f()
        return it if it and pred(it) else None
    g.__name__ = getattr(f, "__name__", "g")
    return g


def limit(f, n):
    """use maker f at most n times in the whole unit (for makers whose questions differ only by a number or object)"""
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
