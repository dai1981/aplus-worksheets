# -*- coding: utf-8 -*-
"""
Ontario secondary science: SNC1W (Grade 9, 2022), SNC2D (Grade 10, 2008), and the Grade 11-12 university courses
SBI3U, SCH3U, SPH3U, SBI4U, SCH4U, SPH4U (The Ontario Curriculum, Grades 11 and 12: Science, 2008).
country `ca-on`, subject `science`, grade `grade-9` ... `grade-12`; one grade page carries the courses of that grade
(domain = "Biology (SBI3U)").
  HU(course, strand, sort, slug, code, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, allow=())
      strand = "B" ... "F"; code = "D3.1, D3.2"; sets = lambda X: [(title, [(maker, n)]) x 5]
  X (in sets) = caon_sci.X plus
      X.ch(mod, slug, s, year=None, only=, rep=, drop=)  set s (1-5) of a UK A level (al_bio / al_chem / al_phys, year 12-13)
                                                        or India Class 11-12 (in_s11b ... in_s12p) unit, as one maker
      X.al(f, *kinds)                                   an al_* maker fixed to some kinds
  All makers go through caon_sci.cam (Canadian English and names, leak checks, once per unit).
build(mod, grade, slug): seed 67000 + 100 * grade + sort.  g = 9.8 m/s²; solutions in mL, L and mol/L.
"""
import contextlib
import importlib
import io
import json
import re
import caon_sci
import au_sr
import in_sci
import uk_alsci
import uk_sci
import sci_common
from caon_sci import People, _CSrc, _quotes, ca_text, _bad, _NAME_RE, SEEN, seed_of
from sci_common import lesson, Unit
from au_sci import sgnum, _fixnums
import al_phys

al_phys.G = 9.8

URL_910 = "https://www.edu.gov.on.ca/eng/curriculum/secondary/science910_2008.pdf"
URL_1112 = "https://www.edu.gov.on.ca/eng/curriculum/secondary/2009science11_12.pdf"
URL_SNC1W = "https://www.dcp.edu.gov.on.ca/en/curriculum/secondary-science/courses/snc1w/strands"
DOC_910 = "The Ontario Curriculum, Grades 9 and 10: Science (2008)"
DOC_1112 = "The Ontario Curriculum, Grades 11 and 12: Science (2008)"
COURSES = {
    "SNC1W": (9, "Science", URL_SNC1W, "The Ontario Curriculum, Science, Grade 9: SNC1W (2022)", {
        "B": ("Biology", "Sustainable Ecosystems and Climate Change"), "C": ("Chemistry", "Nature of Matter"),
        "D": ("Physics", "Principles and Applications of Electricity"), "E": ("Earth and Space Science", "Space Exploration")}),
    "SNC2D": (10, "Science", URL_910, DOC_910 + ", Science, Grade 10, Academic (SNC2D)", {
        "B": ("Biology", "Tissues, Organs, and Systems of Living Things"), "C": ("Chemistry", "Chemical Reactions"),
        "D": ("Earth and Space Science", "Climate Change"), "E": ("Physics", "Light and Geometric Optics")}),
    "SBI3U": (11, "Biology", URL_1112, DOC_1112 + ", Biology, Grade 11, University Preparation (SBI3U)", {
        "B": "Diversity of Living Things", "C": "Evolution", "D": "Genetic Processes", "E": "Animals: Structure and Function",
        "F": "Plants: Anatomy, Growth, and Function"}),
    "SCH3U": (11, "Chemistry", URL_1112, DOC_1112 + ", Chemistry, Grade 11, University Preparation (SCH3U)", {
        "B": "Matter, Chemical Trends, and Chemical Bonding", "C": "Chemical Reactions", "D": "Quantities in Chemical Reactions",
        "E": "Solutions and Solubility", "F": "Gases and Atmospheric Chemistry"}),
    "SPH3U": (11, "Physics", URL_1112, DOC_1112 + ", Physics, Grade 11, University Preparation (SPH3U)", {
        "B": "Kinematics", "C": "Forces", "D": "Energy and Society", "E": "Waves and Sound", "F": "Electricity and Magnetism"}),
    "SBI4U": (12, "Biology", URL_1112, DOC_1112 + ", Biology, Grade 12, University Preparation (SBI4U)", {
        "B": "Biochemistry", "C": "Metabolic Processes", "D": "Molecular Genetics", "E": "Homeostasis", "F": "Population Dynamics"}),
    "SCH4U": (12, "Chemistry", URL_1112, DOC_1112 + ", Chemistry, Grade 12, University Preparation (SCH4U)", {
        "B": "Organic Chemistry", "C": "Structure and Properties of Matter", "D": "Energy Changes and Rates of Reaction",
        "E": "Chemical Systems and Equilibrium", "F": "Electrochemistry"}),
    "SPH4U": (12, "Physics", URL_1112, DOC_1112 + ", Physics, Grade 12, University Preparation (SPH4U)", {
        "B": "Dynamics", "C": "Energy and Momentum", "D": "Gravitational, Electric, and Magnetic Fields", "E": "The Wave Nature of Light",
        "F": "Revolutions in Modern Physics"}),
}

# Ontario words for other countries' high-school questions
HS_REP = [(r"\bnonrenewable\b", "non-renewable"), (r"\bNonrenewable\b", "Non-renewable"), (r"9\.81(?!\d)", "9.8"),
          (r"\bAs on the data sheet,? ", ""), (r"\bmol dm<sup>−3</sup>", "mol/L"), (r"\bmol L⁻¹", "mol/L"), (r"\bmol L<sup>−1</sup>", "mol/L"),
          (r"mol dm⁻³ min⁻¹", "mol L⁻¹ min⁻¹"), (r"mol dm⁻³", "mol/L"), (r"\bpetrol pump\b", "gas station"),
          (r"\b(\w*(?:hybrid|delocal|polar|fertil|quant|polymer|synthes|capital|vernal|terminal|ion|neutral|optim|steril|crystall|oxid|vapor|vapour|real|minim|maxim|special|stabil|util|categor|summar|memor|visual|emphas|organ|recogn|character|hypothes))is(e|ed|es|ing|ation|ations)\b", r"\1iz\2"),
          (r"\b(\w*(?:hydro|electro|cata|ana|para|dia))lys(e|ed|es|ing|er|ers)\b", r"\1lyz\2"), (r"\banticlockwise\b", "counterclockwise"),
          (r"\bAnticlockwise\b", "Counterclockwise"), (r"\bearthed\b", "grounded"), (r"\bearthing\b", "grounding"), (r"\bearth wire\b", "ground wire"), (r"\b1 molecule of glucose are\b", "1 molecule of glucose is")]
HS_DROP = [au_sr.SR_LEAK.pattern, r"mg/dL", r"kcal", r"\bRTP\b", r"room temperature and pressure", r"\b24 ?(dm|L)\b", r"\b24\.0 ?(dm|L)\b",
           r"\bdata booklet\b", r"\bspecification\b", r"\bexam board\b", r"\bIndia\b", r"\bkharif\b",
           r"\b(Woodlands|Clementi|Tampines|Sengkang|Jurong|Pasir Ris|Bukit|Bedok|Punggol|Changi|Sentosa|Yishun|Hougang|Toa Payoh|Ang Mo Kio)\b",
           r"g ?= ?10 ?N ?/ ?kg", r"\(g = 10\b", r"\b1/v\b", r"\b1/u\b", r"sign convention", r"\bu ?= ?[−-]"]


def HU(course, strand, sort, slug, code, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, allow=()):
    assert course in COURSES and strand in COURSES[course][4], (course, strand)
    return dict(course=course, strand=strand, sort=sort, slug=slug, code=code, std=std, title=title, short=short, meta=meta,
                kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, allow=tuple(allow))


def subject_of(u):
    s = COURSES[u["course"]][4][u["strand"]]
    return s[0] if isinstance(s, tuple) else COURSES[u["course"]][1]


def strand_name(u):
    s = COURSES[u["course"]][4][u["strand"]]
    return s[1] if isinstance(s, tuple) else s


class X(caon_sci.X):
    def __init__(self, U, R, P, src):
        super().__init__(U, R, P, src)
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

    def _w(self, f, rep=(), drop=()):
        return self.src.wrap(f, HS_REP + list(rep), list(drop) + HS_DROP)

    def ch(self, mod, slug, s, year=None, rep=(), drop=(), only=None):
        u = self._units(mod, year)[slug]
        key = ("spec", mod, year, slug)
        if key not in self._spec:
            self._sync()
            self._spec[key] = u["sets"]() if callable(u["sets"]) else u["sets"]
        ms = self._spec[key][s - 1][1]
        if only is not None:
            ms = [ms[i] for i in only]
        if mod.startswith("in_s"):
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

    def al(self, f, *kinds, rep=(), drop=()):
        R = self.R

        def g0():
            return f(R.choice(kinds)) if kinds else f()
        g0.__name__ = f.__name__
        return self._w(g0, rep, drop)

    def gen(self, mod, name, rep=(), drop=(), n=None):
        return super().gen(mod, name, HS_REP + list(rep), list(drop) + HS_DROP, n)

    def w(self, f, rep=(), drop=(), n=None):
        return super().w(f, HS_REP + list(rep), list(drop) + HS_DROP, n)


ML_REP = au_sr.ML_REP


def _fix(t, subject):
    for a, b in HS_REP + (ML_REP if subject in ("Biology", "Chemistry") else []):
        t = re.sub(a, b, t)
    t = re.sub(r"(^|>)([^<]*)", lambda m: m.group(1) + re.sub(r"(?<![\d.,])(\d{1,3})((?:,\d{3})+)(?![\d])",
                                                              lambda n: n.group(1) + n.group(2).replace(",", ""), m.group(2)), t)
    t = re.sub(r"(?<=[\s(=])-(?=\d)", "−", t)
    return _quotes(ca_text(t))


def build(mod, grade, slug):
    u = next(x for x in mod.UNITS() if x["slug"] == slug)
    sort = u["sort"]
    gr, subj0, url, doc, _ = COURSES[u["course"]]
    assert gr == grade
    U = Unit(seed_of(grade, sort))
    R = U.R
    P = People(R)
    uk_sci.USED.clear()
    SEEN.clear()
    src = _CSrc(U, P)
    allow = set(u["allow"])
    x = X(U, R, P, src)
    sets = U.sets(u["sets"](x))
    subj = subject_of(u)
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"], it["c"] = _fix(it["q"], subj), _fix(it["e"], subj), [_fix(c, subj) for c in it["c"]]
            assert len({c.strip().lower() for c in it["c"]}) == 4, it["c"]
    sets = _fixnums(sets)
    body = sgnum(lesson(u["think"], u["ex"], u["mist"]))
    sname = strand_name(u)
    course_subj = subj0
    seo = "Grade %d %s (%s): %s Worksheets (Ontario)" % (grade, course_subj, u["course"], u["title"])
    if len(seo) > 95:
        seo = "Grade %d %s (%s): %s Worksheets" % (grade, course_subj, u["course"], u["title"])
    code = "%s: %s" % (u["course"], u["code"])
    std = "%s (summary of %s, Strand %s: %s)" % (u["std"], doc, u["strand"], sname)
    blob = json.dumps([u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets, std], ensure_ascii=False)
    bad = sorted(_bad(blob) - allow)
    assert not bad, "Words that do not fit Ontario: %s" % bad
    txt = re.sub(r"<[^>]+>", " ", blob)
    m = au_sr.SR_LEAK.search(txt)
    assert not m, "Source syllabus word left: %s" % m.group(0)
    m = _NAME_RE.search(txt)
    assert not m, "Foreign name left: %s" % m.group(1)
    assert "\\" not in blob, blob[max(0, blob.index("\\") - 120):blob.index("\\") + 40]
    dom = "%s (%s)" % (subj, u["course"])
    sci_common.make("grade-%d" % grade, slug, sort, code, std, u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body,
                    [(q, a) for q, a in u["faq"]], sets, domain=dom, country="ca-on", url=url)


def main(mod, grade, slug):
    build(importlib.import_module(mod), grade, slug)
