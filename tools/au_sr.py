# -*- coding: utf-8 -*-
"""
Australian Senior Secondary science (Australian Curriculum: Senior Secondary, Biology, Chemistry, Physics and
Earth and Environmental Science, Units 1-4): subject `science`, grade `year-11` (Units 1 and 2) / `year-12` (Units 3 and 4).
One grade page carries the four subjects (domain = the subject).
  SR(subject, unit, sort, slug, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets)
      unit = 1-4; topic = the sub-unit ("Ecosystem dynamics"); sets = lambda X: [(title, [(maker, n), ...]) x 5]
      standard_code "Biology Unit 1: Ecosystem dynamics", standard_url = the ACARA subject page
  X (in sets): X.R, X.U, X.P
      X.ch(mod, slug, s, year=None, rep=, drop=)  all makers of set s (1-5) of another unit, as one maker:
          UK A level (al_bio / al_chem / al_phys with year 12 or 13) or India Class 11-12 (in_s11b ... in_s12p)
      X.al(f, *kinds)        an al_* maker fixed to some kinds
      X.gen(module, name)    a maker from any gen_ science generator (US, UK, SG, IN, AU)
      X.pool(rows)           hand-written rows (q, a, [w, w, w], e)
  Everything goes through au_sci.aum: Australian names and English; items with words that do not fit are dropped,
  and a question (names and numbers removed) with the same answer is used once per unit.
build(mod, year, slug): seed 66000 + 100 * year + sort (au_sci.seed_of). g = 9.8 m/s².
"""
import copy
import json
import re
import contextlib
import io
import importlib
import au_sci
import in_sci
import uk_alsci
import sci_common
from au_sci import AU, aum, _bad, _NAME_RE, _fixnums, seed_of, nq, tq, rows, keep, limit, sgnum
from sci_common import item, lesson
import al_phys

al_phys.G = 9.8

URL = "https://australiancurriculum.edu.au/senior-secondary-curriculum/science/%s"
SUBJ = {
    "Biology": ("biology", ["Biodiversity and the interconnectedness of life", "Cells and multicellular organisms",
                            "Heredity and continuity of life", "Maintaining the internal environment"]),
    "Chemistry": ("chemistry", ["Chemical fundamentals: structure, properties and reactions", "Molecular interactions and reactions",
                                "Equilibrium, acids and redox reactions", "Structure, synthesis and design"]),
    "Physics": ("physics", ["Thermal, nuclear and electrical physics", "Linear motion and waves", "Gravity and electromagnetism",
                            "Revolutions in modern physics"]),
    "Earth and Environmental Science": ("earth-and-environmental-science", [
        "Introduction to Earth systems", "Earth processes – energy transfers and transformations",
        "Living on Earth – extracting, using and managing Earth resources", "The changing Earth – the cause and impact of Earth hazards"]),
}
SHORT = {"Earth and Environmental Science": "Earth and Environmental Science"}
# words from the source syllabuses that do not fit an Australian senior page
SR_LEAK = re.compile(r"\b(A level|AS level|NCERT|CBSE|JEE|NEET|data sheet|Class 1[12]|GCSE|O-Level|brinjal|ladyfinger|neem|tulsi|"
                     r"Ganga|Yamuna|Delhi|Mumbai|Kolkata|Chennai|lakh|crore|kharif|rabi|paddy|bajra|jowar|ragi|Abingdon|Siberian crane)\b", re.I)
# words in other countries' questions that Australians say differently
GEN_REP = [(r"\bnonrenewable\b", "non-renewable"), (r"\bNonrenewable\b", "Non-renewable"), (r"\ban? hurricane\b", "a tropical cyclone"),
           (r"\bhurricanes\b", "tropical cyclones"), (r"\bhurricane\b", "tropical cyclone"), (r"\bwildfires\b", "bushfires"), (r"\bwildfire\b", "bushfire"),
           (r"\bWildfires\b", "Bushfires"), (r"\bWildfire\b", "Bushfire"), (r"\bclearing brush\b", "clearing scrub")]
SR_REP = [(r"\bAs on the data sheet,? ", ""), (r"9\.81(?!\d)", "9.8"), (r"\bmol dm<sup>−3</sup>", "mol/L"),
          (r"\bmol L⁻¹", "mol/L"), (r"\bmol L<sup>−1</sup>", "mol/L"), (r"mol dm⁻³ min⁻¹", "mol L⁻¹ min⁻¹"), (r"mol dm⁻³", "mol/L"),
          (r"\bfaeces\b", "faeces"), (r"\bpetrol pump\b", "service station")]


def SR(subject, unit, sort, slug, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, allow=()):
    assert subject in SUBJ and 1 <= unit <= 4
    return dict(subject=subject, unit=unit, sort=sort, slug=slug, topic=topic, std=std, title=title, short=short, meta=meta,
                kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, allow=tuple(allow))


class X:
    def __init__(self, U, R, P, src):
        self.U, self.R, self.P, self.src = U, R, P, src
        self._spec = {}

    def _sync(self):
        in_sci._R[0] = self.R
        uk_alsci._R[0] = self.R
        self.src.sync()

    def _units(self, mod, year):
        key = (mod, year)
        if key not in self._spec:
            self._sync()
            with contextlib.redirect_stdout(io.StringIO()):
                m = importlib.import_module(mod)
            m.R = self.R
            us = m.UNITS(year) if year is not None else m.UNITS()
            self._spec[key] = {u["slug"]: u for u in us}
        return self._spec[key]

    def ch(self, mod, slug, s, year=None, rep=(), drop=(), only=None):
        """set s (1-5) of unit slug in module mod, as one maker (only: indexes of makers in that set)"""
        u = self._units(mod, year)[slug]
        key = ("spec", mod, year, slug)
        if key not in self._spec:
            self._sync()
            self._spec[key] = u["sets"]() if callable(u["sets"]) else u["sets"]
        ms = self._spec[key][s - 1][1]
        if only is not None:
            ms = [ms[i] for i in only]
        if mod.startswith("in_s"):          # India odd-one-out tables mix unrelated groups: leave them out
            drop = list(drop) + [r'"q": "Which of these (is|are) ']
        fs = [(self._w(f, rep, drop), n) for f, n in ms]
        tot = sum(n for _, n in fs)

        def g():
            self._sync()
            r = self.R.random() * tot
            for f, n in fs:
                r -= n
                if r < 0:
                    return f()
            return fs[-1][0]()
        g.__name__ = "%s_%s_%d" % (mod, slug, s)
        return g

    def _w(self, f, rep=(), drop=()):
        return self.src.wrap(f, GEN_REP + list(rep), list(drop) + [SR_LEAK.pattern, r"mg/dL", r"kcal"])

    def al(self, f, *kinds, rep=(), drop=()):
        R = self

        def g0():
            return f(R.R.choice(kinds)) if kinds else f()
        g0.__name__ = f.__name__
        return self._w(g0, rep, drop)

    def w(self, f, rep=(), drop=()):
        """an own maker (Australian checks and the unit's repeat filter)"""
        return self._w(f, rep, drop)

    def f(self, factory, rep=(), drop=()):
        """an own maker made by factory(R)"""
        return self._w(factory(self.R), rep, drop)

    def gen(self, mod, name, rep=(), drop=()):
        return self.src(mod, name, GEN_REP + list(rep), list(drop) + [SR_LEAK.pattern, r"mg/dL", r"kcal"])

    def mod(self, name):
        return self.src.mod(name)

    def pool(self, rs):
        its = [item(*r) for r in rs]
        R = self.R

        def f():
            return copy.deepcopy(R.choice(its))
        f.n = len(its)
        return f

    def rows(self, rs, fwd, back=None, extra=()):
        return rows(self.R, rs, fwd, back, extra)


# solution volumes are in mL for Biology and Chemistry (cm³ stays for solids in Physics and Earth science)
ML_REP = [(r"\bcm<sup>3</sup>", "mL"), (r"\bcm³", "mL"), (r"\bdm<sup>3</sup>", "L"), (r"\bdm³", "L"), (r"dm⁻⁶", "L⁻²"), (r"dm⁶", "L²"), (r"dm⁻⁹", "L⁻³"), (r"dm⁹", "L³"), (r"dm⁻³", "L⁻¹")]


def _fix(t, subject=""):
    for a, b in SR_REP + (ML_REP if subject in ("Biology", "Chemistry") else []):
        t = re.sub(a, b, t)
    # straight double quotes in text -> curly quotes (attributes use single quotes)
    t = re.sub(r"(^|>)([^<]*)", lambda m: m.group(1) + re.sub(r'"([^"]*)"', "“\\1”", m.group(2)).replace('"', "”"), t)
    # 1,300 -> 1300 (Australian numbers; sgnum adds a space from 5 digits)
    t = re.sub(r"(^|>)([^<]*)", lambda m: m.group(1) + re.sub(r"(?<![\d.,])(\d{1,3})((?:,\d{3})+)(?![\d])", lambda n: n.group(1) + n.group(2).replace(",", ""), m.group(2)), t)
    return re.sub(r"(?<=[\s(=])-(?=\d)", "−", t)


def build(mod, year, slug):
    u = next(x for x in mod.UNITS(year) if x["slug"] == slug)
    sort = u["sort"]
    U, R, P, src = AU(seed_of(year, sort))
    allow = set(u.get("allow", ()))
    if not hasattr(au_sci, "_bad0"):
        au_sci._bad0 = au_sci._bad
    au_sci._bad = lambda t: au_sci._bad0(t) - allow       # words this unit may use (ore grade, the Golden Mile)
    x = X(U, R, P, src)
    spec = u["sets"](x)
    sets = U.sets(spec)
    for st in sets:
        for it in st["items"]:
            sj = u["subject"]
            it["q"], it["e"], it["c"] = _fix(it["q"], sj), _fix(it["e"], sj), [_fix(c, sj) for c in it["c"]]
            assert len({c.strip().lower() for c in it["c"]}) == 4, it["c"]
    sets = _fixnums(sets)
    body = sgnum(lesson(u["think"], u["ex"], u["mist"]))
    subj = u["subject"]
    small = {"and", "of", "in", "the", "a", "to", "or", "for", "on"}
    ts = " ".join(w if (i and w in small) else w[0].upper() + w[1:] for i, w in enumerate(u["short"].split()))
    seo = "Year %d %s: %s Worksheets (Australian Curriculum)" % (year, subj, ts)
    if len(seo) > 95:
        seo = "Year %d %s: %s Worksheets" % (year, subj, ts)
    code = "%s Unit %d: %s" % (subj, u["unit"], u["topic"])
    std = "%s (Senior Secondary %s, Unit %d: %s)" % (u["std"], subj, u["unit"], SUBJ[subj][1][u["unit"] - 1])
    blob = json.dumps([u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets, std], ensure_ascii=False)
    bad = sorted(au_sci._bad(blob))
    assert not bad, "Words that do not fit Australia: %s" % bad
    txt = re.sub(r"<[^>]+>", " ", blob)
    m = SR_LEAK.search(txt)
    assert not m, "Source syllabus word left: %s" % m.group(0)
    m = _NAME_RE.search(txt)
    assert not m, "Foreign name left: %s" % m.group(1)
    assert "\\" not in blob, blob[max(0, blob.index("\\") - 120):blob.index("\\") + 40]
    sci_common.make("year-%d" % year, slug, sort, code, std, u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body,
                    [(q, a) for q, a in u["faq"]], sets, domain=subj, country="au", url=URL % SUBJ[subj][0])
