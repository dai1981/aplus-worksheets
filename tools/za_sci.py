# -*- coding: utf-8 -*-
"""
South African science (CAPS): country `za`, subject `science`, grade `grade-N`.
  Grade 4-6  Natural Sciences and Technology (strands Life and Living / Matter and Materials / Energy and Change / Planet Earth and Beyond)
  Grade 7-9  Natural Sciences (same four strands)
  Grade 10-12 Physical Sciences (domain "Physical Sciences: Chemistry" / "Physical Sciences: Physics") and Life Sciences on one grade page
  ZU(area, sort, slug, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, allow=())
      sets = lambda X: S(X, [(title, "mod:slug:set[:year]") or (title, [(part, n)])])   (cabc_sci.S, GM)
  X: the BC X (X.o for caon_*, cabc_*, au_sr* units, X.ch for al_*/in_s*, X.gen/B/pool/rows/w/f), but every maker goes
  through South African English: British spelling (uk_sci.ukm), South African names, words (learners, pavement, petrol, torch,
  jersey, rubbish, sweets, mol·dm⁻³), southern-hemisphere seasons; items with words that do not fit (Canada, Ontario, Australia,
  UK, India, $, £, ₹, pence, inches, Year N, GCSE ...) are dropped.  Numbers: decimal comma and 4 536 (za_numbers), years kept.
  Grade 10-12 physics units: m·s⁻¹, m·s⁻², g = 9,8 m·s⁻².
build(mod, grade, slug): seed 71000 + 100 * grade + sort.
"""
import inspect
import json
import re
import au_sci
import caon_sci
import caon_hs
import cabc_sci
import uk_sci
import sci_common
import za_common
from sci_common import lesson, Unit
from cabc_sci import S, GM  # noqa: F401  (used by the unit modules)

URL_NST = "https://wcedeportal.westerncape.gov.za/eresource/curriculum-and-assessment-policy-statement-caps-natural-science-technology-gr-4-6"
URL_NS = "https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20NATURAL%20SCIENCES%20GR%207-9%20%20WEB.pdf"
URL_PS = "https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20%20PHYSICAL%20SCIENCE%20WEB.pdf"
URL_LS = "https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20_%20LIFE%20SCIENCES%20_%20GR%2010-12%20Web_2636.pdf"
STRANDS = ("Life and Living", "Matter and Materials", "Energy and Change", "Planet Earth and Beyond")
FET = ("Physical Sciences: Chemistry", "Physical Sciences: Physics", "Life Sciences")

# ---- South African rules for every maker (au_sci.aum is patched) ----
GIRLS, BOYS = list(za_common.GIRLS), list(za_common.BOYS)
_G = set(au_sci._G) | set(au_sci.GIRLS) | set(caon_sci.GIRLS) | set(za_common.FOREIGN_GIRLS)
_Bo = set(au_sci._Bo) | set(au_sci.BOYS) | set(caon_sci.BOYS) | set(za_common.FOREIGN_BOYS)
FOREIGN = sorted((_G | _Bo) - set(GIRLS) - set(BOYS), key=len, reverse=True)

ZA_REP = [
    (r"\b(\w*(?:organ|recogn|real|special|minim|maxim|crystall|fertil|steril|neutral|ion|polar|stabil|util|categor|summar|memor|visual|emphas|harmon|hybrid|polymer|synthes|oxid|vapor|vapour|character|hypothes|optim|quant|capital|delocal|terminal|apolog|critic|standard|magnet|colon|sympath|immun|mobil))iz(e|ed|es|ing|ation|ations|er|ers)\b", r"\1is\2"),
    (r"\b(\w*(?:ana|para|cata|hydro|electro|dia))lyz(e|ed|es|ing|er|ers)\b", r"\1lys\2"),
    (r"\b([Cc])olorless\b", r"\1olourless"), (r"\b([Ff])avor(s|ed|ing|able|ite|ites)?\b", r"\1avour\2"), (r"\b([Bb])ehavior(s|al)?\b", r"\1ehaviour\2"),
    (r"\bAn elevator\b", "A lift"), (r"\ban elevator\b", "a lift"), (r"\belevators?\b", "lift"),
    (r"\bcounterclockwise\b", "anticlockwise"), (r"\bCounterclockwise\b", "Anticlockwise"),
    (r"\bmol/L\b", "mol·dm⁻³"), (r"\bmol/dm³", "mol·dm⁻³"), (r"\bmol dm⁻³", "mol·dm⁻³"), (r"\bmol L⁻¹", "mol·dm⁻³"), (r"\bmol dm<sup>−3</sup>", "mol·dm⁻³"),
    (r"9\.81(?!\d)", "9.8"), (r"\bpupils\b", "learners"), (r"\bPupils\b", "Learners"), (r"\bpupil's\b", "learner's"),
    (r"\bstudents\b", "learners"), (r"\bStudents\b", "Learners"), (r"\bstudent\b", "learner"), (r"\bStudent\b", "Learner"),
    (r"\b([Aa]) pupil (drew|wrote|says|said|thinks|measured|made|was|is|has|wants|tested|noticed)\b", r"\1 learner \2"),
    (r"\bYear ([1-9])\b", r"Grade \1"), (r"\b(sound level|light|parking|water|gas|electricity|data|level|speed|power|pH|moisture|rain|newton) metres?\b", r"\1 meter"), (r"\bPupil\b", "Learner"), (r"\bpupil\b(?! of)", "learner"), (r"\bsidewalks\b", "pavements"), (r"\bsidewalk\b", "pavement"), (r"\bfootpaths\b", "pavements"), (r"\bfootpath\b", "pavement"),
    (r"\bgarbage cans?\b", "rubbish bin"), (r"\bgarbage\b", "rubbish"), (r"\bGarbage\b", "Rubbish"), (r"\bcandy\b", "sweets"), (r"\blollies\b", "sweets"),
    (r"\bcookies\b", "biscuits"), (r"\bcookie\b", "biscuit"), (r"\bgasoline\b", "petrol"), (r"\bGasoline\b", "Petrol"), (r"\bgas station\b", "petrol station"),
    (r"\bflashlights\b", "torches"), (r"\bflashlight\b", "torch"), (r"\bsweaters\b", "jerseys"), (r"\bsweater\b", "jersey"), (r"\bjumpers\b", "jerseys"), (r"\bjumper\b", "jersey"),
    (r"\bpopsicles\b", "ice lollies"), (r"\bpopsicle\b", "ice lolly"), (r"\bicy poles\b", "ice lollies"), (r"\bicy pole\b", "ice lolly"),
    (r"\b(a|the) elevator\b", r"\1 lift"), (r"\bspring scales\b", "spring balances"), (r"\bspring scale\b", "spring balance"),
    (r"\ban esky\b", "a cooler box"), (r"\beskys?\b", "cooler box"), (r"\bcolumn graphs\b", "bar graphs"), (r"\bcolumn graph\b", "bar graph"),
    (r"\bbicarb soda\b", "bicarbonate of soda"), (r"\bBicarb soda\b", "Bicarbonate of soda"), (r"\bbaking soda\b", "bicarbonate of soda"), (r"\bBaking soda\b", "Bicarbonate of soda"),
    (r"\bgum trees\b", "blue gum trees"), (r"\bgum tree\b", "blue gum tree"), (r"\bin bushland\b", "in the bush"), (r"\bbushland\b", "bush"),
    (r"\bMom\b", "Mum"), (r"\bmom\b", "mum"), (r"\btires\b", "tyres"), (r"\btire\b", "tyre"), (r"\baluminum\b", "aluminium"), (r"\bAluminum\b", "Aluminium"),
    (r"\bsulphur", "sulfur"), (r"\bSulphur", "Sulfur"), (r"\bparking lots?\b", "parking area"), (r"\bwashroom\b", "toilet"), (r"\brecess\b", "break"),
    (r"\bin fall\b", "in autumn"), (r"\bIn fall\b", "In autumn"), (r"\bfall and winter\b", "autumn and winter"), (r"\bthe fall\b(?! of)", "autumn"),
    (r"\bsow bugs\b", "woodlice"), (r"\bsow bug\b", "woodlouse"), (r"\bslaters\b", "woodlice"), (r"\bslater\b", "woodlouse"),
    (r"\bladybugs\b", "ladybirds"), (r"\bladybug\b", "ladybird"), (r"\bthumbtacks\b", "drawing pins"), (r"\bthumbtack\b", "drawing pin"),
    (r"\bplastic wrap\b", "cling wrap"), (r"\bcling film\b", "cling wrap"), (r"\bpolyethylene\b", "polythene"), (r"\bvacation\b", "holidays"),
    (r"\bfaucets?\b", "tap"), (r"\btrucks\b", "trucks"), (r"\blorries\b", "trucks"), (r"\blorry\b", "truck"), (r"\bcellphones\b", "cellphones"), (r"\bmobile phones?\b", "cellphone"),
    (r"\bfootballs\b", "soccer balls"), (r"\bfootball\b", "soccer"), (r"\bFootball\b", "Soccer"), (r"\bfooty\b", "soccer"),
    (r"\bbar charts\b", "bar graphs"), (r"\bbar chart\b", "bar graph"), (r"\bpower plants\b", "power stations"), (r"\bpower plant\b", "power station"),
    (r"\bgas stove\b", "gas stove"), (r"\bcoolers\b", "cooler boxes"), (r"\ba cooler\b", "a cooler box"), (r"\bacetaminophen\b", "paracetamol"),
    (r"\bground beef\b", "mince"), (r"\bzucchini\b", "baby marrows"), (r"\beggplants?\b", "brinjal"), (r"\bhigh school\b", "secondary school"),
]
for a, b in za_common.ZA_PLACES:
    ZA_REP.append((r"\b" + a + r"\b", b))

LEAKS = sorted(set(w for w in uk_sci.LEAKS if w not in ("recess", "football", "soccer", "pupil", "pupils", "grade", "grades")) | {
    # North American and Australian words
    "aluminum", "sidewalk", "garbage", "candy", "cookie", "cookies", "gasoline", "flashlight", "popsicle", "eh", "toonie", "loonie", "nickel coin",
    "esky", "icy pole", "footpath", "bushland", "lollies", "column graph", "arvo", "ute",
    "koala", "koalas", "kangaroo", "kangaroos", "wombat", "wombats", "platypus", "echidna", "echidnas", "possum", "possums", "kookaburra", "kookaburras",
    "emu", "emus", "dingo", "dingoes", "wallaby", "wallabies", "galah", "galahs", "cockatoo", "cockatoos", "lorikeet", "lorikeets", "goanna", "goannas",
    "quokka", "numbat", "bilby", "cassowary", "billabong", "outback", "wattle bird", "moose", "raccoon", "raccoons", "skunk", "skunks", "maple", "maples",
    "chipmunk", "chipmunks", "beaver", "beavers", "loon", "loons", "groundhog", "bison", "bald eagle", "blue jay", "cardinal bird", "monarch butterflies",
    # places and school systems of other countries
    "canada", "canadian", "canadians", "ontario", "toronto", "ottawa", "quebec", "vancouver", "british columbia", "alberta", "manitoba", "nunavut", "yukon",
    "great lakes", "lake ontario", "lake erie", "lake superior", "niagara", "canadian shield", "canadarm", "radarsat",
    "australia", "australian", "australians", "sydney", "melbourne", "brisbane", "perth", "adelaide", "queensland", "tasmania", "canberra", "darwin city",
    "great barrier reef", "uluru", "murray river", "britain", "british", "england", "english channel", "scotland", "wales", "london", "manchester", "birmingham",
    "thames", "uk", "united kingdom", "u.s.", "usa", "america", "american", "americans", "united states", "texas", "florida", "arizona", "california", "alaska",
    "new york", "chicago", "singapore", "india", "indian", "delhi", "mumbai", "kolkata", "chennai", "rupee", "rupees", "neem",
    "year 1", "year 2", "year 3", "year 4", "year 5", "year 6", "year 7", "year 8", "year 9", "year 10", "year 11", "year 12", "year 13",
    "gcse", "ks1", "ks2", "ks3", "ks4", "a level", "a-level", "o-level", "psle", "nhs", "ngss", "cbse", "ncert", "eqao", "hst", "snc1w", "snc2d",
    "sixth form", "high school", "middle school", "freshman", "sophomore",
    # units South Africa does not use
    "inch", "inches", "pound", "pounds", "ounce", "ounces", "gallon", "gallons", "mile", "miles", "fahrenheit", "feet", "yard", "yards", "mph",
})
LEAK_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in LEAKS), re.I)


def _bad(text):
    t = uk_sci._text_of(text)
    bad = {m.group(1).lower() for m in LEAK_RE.finditer(t)}
    if re.search(r"[£₹¢₱]|\$\s?\d|\bpence\b|°F|\b\d+ ?(ft|lb|oz|in\.)\b", t):
        bad.add("money/units")
    if au_sci.SEASON_RE.search(t):
        bad.add("northern seasons")
    return bad


def _patch():
    au_sci.GIRLS[:] = GIRLS
    au_sci.BOYS[:] = BOYS
    au_sci._G = _G
    au_sci._Bo = _Bo
    au_sci.FOREIGN = FOREIGN
    au_sci._NAME_RE = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in FOREIGN))
    au_sci.AU_REP = ZA_REP
    au_sci._bad = _bad
    au_sci._ALLN = None


_patch()


class People:
    def __init__(self, R):
        self.R = R
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]

    def next(self):
        return self.R.choice(self.pool)


ZA_DROP = [r"\b(Ontario|Toronto|Canad\w*|Australi\w*|Sydney|Britain|British|England|India|Singapore|Texas|America\w*)\b",
           r"\bRTP\b", r"room temperature and pressure", r"\b24 ?(dm|L)\b", r"mg/dL", r"kcal", r"\bdata booklet\b", r"\bexam board\b",
           r"g ?= ?10 ?N ?/ ?kg", r"\(g = 10\b", r"\b1/v\b", r"\b1/u\b", r"sign convention", r"\bu ?= ?[−-]", r"\bspecification\b"]


def _light(it):
    """South African words and names on an item made outside the wrapped makers (Ontario own makers); None if a word does not fit"""
    if it is None:
        return None
    it = dict(it)

    def fx(s):
        s = uk_sci.uk_text(s)
        s = au_sci._NAME_RE.sub(lambda m: (GIRLS if m.group(1) in _G else BOYS)[sum(map(ord, m.group(1))) % 20], s)
        for a, b in ZA_REP:
            s = re.sub(a, b, s)
        return au_sci._fix_an(s)
    it["q"], it["e"], it["c"] = fx(it["q"]), fx(it["e"]), [fx(c) for c in it["c"]]
    if _bad(json.dumps(it, ensure_ascii=False)) or len({c.strip().lower() for c in it["c"]}) < 4:
        return None
    if re.search("|".join(ZA_DROP), re.sub(r"<[^>]+>", " ", json.dumps(it, ensure_ascii=False))):
        return None
    return it


class X(cabc_sci.X):
    def _w(self, f, rep=(), drop=()):
        return self.src.wrap(f, list(rep), list(drop) + ZA_DROP + cabc_sci.BC_DROP)

    def gen(self, mod, name, rep=(), drop=(), n=None):
        f = self.src(mod, name, list(rep), list(drop) + ZA_DROP + cabc_sci.BC_DROP)
        return au_sci.limit(f, n) if n else f

    def w(self, f, rep=(), drop=(), n=None):
        g = self.src.wrap(f, list(rep), list(drop) + ZA_DROP + cabc_sci.BC_DROP)
        return au_sci.limit(g, n) if n else g

    def o(self, mod, slug, s, year=None):
        g0 = super().o(mod, slug, s, year)

        def g():
            return _light(g0())
        g.__name__ = g0.__name__
        return g


def ZU(area, sort, slug, topic, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, allow=()):
    assert area in STRANDS or area in FET, area
    return dict(area=area, sort=sort, slug=slug, topic=topic, std=std, title=title, short=short, meta=meta, kb=kb, ks=ks,
                think=think, ex=ex, mist=mist, faq=faq, sets=sets, allow=tuple(allow))


def seed_of(grade, sort):
    return 71000 + 100 * grade + sort


_YEAR = re.compile(r"(?<![\d,.])((?:1[5-9]|20)\d\d)(?![\d,.]| ?(?:m|km|kg|g|J|kJ|N|W|kW|s|mm|cm|nm|K|Pa|kPa|V|A|Hz|t|L|mL|dm|cm³|m³|people|learners|°C)\b)")
_SI = [(r"\bm/s²", "m·s⁻²"), (r"\bm/s<sup>2</sup>", "m·s⁻²"), (r"\bkg·m/s\b", "kg·m·s⁻¹"), (r"\bkg m/s\b", "kg·m·s⁻¹"), (r"\bm/s\b", "m·s⁻¹"),
       (r"\bkm/h\b", "km·h⁻¹"), (r"\bN/kg\b", "N·kg⁻¹"), (r"\bN m\b", "N·m"), (r"\bJ/(kg|g)·°C", r"J·\1⁻¹·°C⁻¹")]


def num(s, fet=False):
    """decimal comma and 4 536 in text (not in tags); years stay as they are"""
    keep = {}

    def hold(m):
        k = "%d" % len(keep)
        keep[k] = m.group(1)
        return k
    parts = re.split(r"(<[^>]+>)", s)
    out = []
    for p in parts:
        if not p.startswith("<"):
            p = _YEAR.sub(hold, p)
            if fet:
                for a, b in _SI:
                    p = re.sub(a, b, p)
        out.append(p)
    s = za_common.za_numbers("".join(out))
    for k, v in keep.items():
        s = s.replace(k, v)
    return s


def label(grade):
    return "Grade %d" % grade


def build(mod, grade, slug):
    us = mod.UNITS(grade) if len(inspect.signature(mod.UNITS).parameters) else mod.UNITS()
    u = next(x for x in us if x["slug"] == slug)
    sort = u["sort"]
    U = Unit(seed_of(grade, sort))
    R = U.R
    P = People(R)
    uk_sci.USED.clear()
    au_sci.SEEN.clear()
    caon_sci.SEEN.clear()
    src = au_sci._Src(U, P)
    x = X(U, R, P, src)
    sets = U.sets(u["sets"](x))
    area = u["area"]
    fet = grade >= 10
    subj = "Chemistry" if "Chemistry" in area else ("Biology" if area == "Life Sciences" else "")
    for st in sets:
        for it in st["items"]:
            for k in ("q", "e"):
                it[k] = caon_sci._quotes(it[k])
                it[k] = num(re.sub(r"(?<=[\s(=])-(?=\d)", "−", it[k]), fet and subj != "Biology")
            it["c"] = [num(re.sub(r"(?<=[\s(=])-(?=\d)", "−", caon_sci._quotes(c)), fet and subj != "Biology") for c in it["c"]]
            assert len({c.strip().lower() for c in it["c"]}) == 4, it["c"]
    body = num(lesson(u["think"], u["ex"], u["mist"]), fet and subj != "Biology")
    faq = [(num(q), num(a, fet and subj != "Biology")) for q, a in u["faq"]]
    gl = label(grade)
    if grade <= 6:
        subject, url = "Natural Sciences and Technology", URL_NST
    elif grade <= 9:
        subject, url = "Natural Sciences", URL_NS
    elif area == "Life Sciences":
        subject, url = "Life Sciences", URL_LS
    else:
        subject, url = "Physical Sciences", URL_PS
    seo = "%s %s: %s Worksheets (CAPS)" % (gl, subject, u["title"])
    if len(seo) > 95:
        seo = "%s %s: %s Worksheets" % (gl, subject, u["title"])
    if len(seo) > 95:
        seo = "%s: %s Worksheets (CAPS)" % (gl, u["title"])
    for k in ("std", "kb", "ks", "meta", "short", "topic"):
        u[k] = re.sub(r"<sub>([^<]*)</sub>", r"\1", u[k])
    code = "%s %s: %s" % (gl, subject, u["topic"])
    std = "%s (summary of CAPS %s, %s, %s: %s)" % (u["std"], subject, gl, area.replace("Physical Sciences: ", ""), u["topic"])
    blob = json.dumps([u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body, faq, sets, std], ensure_ascii=False)
    bad = sorted(_bad(blob) - set(u["allow"]) - {"northern seasons"})
    for st in sets:
        for it in st["items"]:
            assert not au_sci.SEASON_RE.search(re.sub(r"<[^>]+>", " ", it["q"] + " " + it["c"][it["a"]] + " " + it["e"])), it["q"]
    if bad:
        low = blob.lower()
        raise AssertionError("Words that do not fit South Africa: %s %s" % (bad, [low[max(0, low.find(w) - 100):low.find(w) + 40] for w in bad]))
    txt = re.sub(r"<[^>]+>", " ", blob)
    m = re.search("|".join(ZA_DROP), txt)
    assert not m, "Word left: %s [%s]" % (m.group(0), txt[max(0, m.start() - 150):m.end() + 60])
    m = au_sci._NAME_RE.search(txt)
    assert not m, "Foreign name left: %s [%s]" % (m.group(1), txt[max(0, m.start() - 100):m.end() + 40])
    assert "\\" not in blob
    sci_common.make("grade-%d" % grade, slug, sort, code, std, u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body,
                    faq, sets, domain=area, country="za", url=url)
