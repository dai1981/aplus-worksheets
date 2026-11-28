# -*- coding: utf-8 -*-
"""
Nigerian science: country `ng`, subject `science`, grades primary-1..6, jss-1..3, sss-1..3.
  Primary 1-3 Basic Science, Primary 4-6 Basic Science and Technology, JSS 1-3 Intermediate Science (the revised
  basic education curriculum, 2025), and SSS 1-3 Biology, Chemistry and Physics (senior secondary curriculum,
  WAEC and NECO syllabuses).
  Domains (basic): the NERDC themes Learning About Our Environment / Living and Non-Living Things / You and Energy /
  Science and Development; (SSS): Biology / Chemistry / Physics.
  NU(theme, sort, slug, std, title, short, what, kb, ks, a, b, ex, mist, faq, sets)   own text
  NC(theme, sort, slug, src, std=None, **override)   text and the 5 sets of another X-style unit ("mod:slug[:year]":
      ph_s3, ph_s7, ph_s11, za_s4, za_s7, za_s10-12, cabc_s*, caon_sci*, caon_hs*, au_sr*), rewritten for Nigeria
  Items go through the shared British pipeline (au_sci), then Nigerian names and places; items with other countries'
  places, money, typhoons, snow and northern winter are dropped.  Numbers 1,000-style (years kept).
build(mod, grade, slug): seed 74000 + 100 * level + sort (primary-N: N, jss-N: 6 + N, sss-N: 9 + N).
"""
import inspect
import json
import re
import za_sci  # noqa: F401
import au_sci
import caon_sci
import cabc_sci
import uk_sci
import sci_common
import za_common
import ph_common
import ng_common
from sci_common import lesson, Unit
from cabc_sci import S, GM  # noqa: F401

URL = "https://nerdc.gov.ng/"
THEMES = ("Learning About Our Environment", "Living and Non-Living Things", "You and Energy", "Science and Development")
SSS = ("Biology", "Chemistry", "Physics")

GIRLS, BOYS = list(ng_common.GIRLS), list(ng_common.BOYS)
_G = set(au_sci._G) | set(caon_sci.GIRLS) | set(za_common.GIRLS) | set(za_common.FOREIGN_GIRLS) | set(ph_common.GIRLS) | set(ph_common.FOREIGN_GIRLS) | set(ng_common.FOREIGN_GIRLS)
_Bo = set(au_sci._Bo) | set(caon_sci.BOYS) | set(za_common.BOYS) | set(za_common.FOREIGN_BOYS) | set(ph_common.BOYS) | set(ph_common.FOREIGN_BOYS) | set(ng_common.FOREIGN_BOYS)
_G |= set(GIRLS) | {"Diane", "Bianca", "Patricia", "Rose", "Isabel", "Sheila", "Hazel", "Kyla", "Jenny", "Lorna", "Ella", "Emily", "Sophie", "Hannah", "Abigail", "Madison", "Avery", "Mila", "Layla", "Scarlett"}
_Bo |= set(BOYS) | {"Kenneth", "Jose", "Emman", "Kevin", "Mark", "Vincent", "Lance", "Rodel", "Jomar", "Arnel", "Ramon", "Renz", "Jericho", "Bryan", "Mason", "Logan", "Lucas", "Jacob", "Michael", "James", "Henry"}
FOREIGN = sorted((_G | _Bo) - set(GIRLS) - set(BOYS), key=len, reverse=True)

WHO = {"p": "pupils"}   # "pupils" in primary, "students" in JSS and SSS (set by build)

NG_REP = [
    (r"\b([Ll])earners'", lambda m: (WHO["p"][0].upper() if m.group(1) == "L" else WHO["p"][0]) + WHO["p"][1:] + "'"),
    (r"\blearners\b", lambda m: WHO["p"]), (r"\bLearners\b", lambda m: WHO["p"].capitalize()),
    (r"\blearner\b", lambda m: WHO["p"][:-1]), (r"\bLearner\b", lambda m: WHO["p"][:-1].capitalize()),
    (r"\bmol dm⁻³", "mol dm⁻³"), (r"\bmol/L\b", "mol dm⁻³"), (r"\bmol L⁻¹", "mol dm⁻³"), (r"\bg L⁻¹", "g dm⁻³"),
    (r"\b(?!caps)(\w{3,}?)iz(e|ed|es|ing|ation|ations|er|ers)\b", r"\1is\2"), (r"\b(ana|para|cata|hydro|electro|dia)lyz(e|ed|es|ing)\b", r"\1lys\2"),
    (r"\bcarabaos\b", "cows"), (r"\bcarabao\b", "cow"), (r"\bjeepneys\b", "buses"), (r"\bjeepney\b", "bus"), (r"\bnarra\b", "iroko"),
    (r"\bmaple\b", "iroko"), (r"\boak trees?\b", "iroko tree"), (r"\bgum trees\b", "mango trees"), (r"\bgum tree\b", "mango tree"),
    (r"\bbadgers\b", "mongooses"), (r"\bbadger\b", "mongoose"), (r"\bdeer\b", "antelope"), (r"\bcalamansi\b", "lime"), (r"\bsari-sari store\b", "shop"),
    (r"\bspaza shops?\b", "shop"), (r"\btuck shop\b", "school canteen"), (r"\bbraai\b", "barbecue"), (r"\brooibos\b", "zobo"), (r"\bbiltong\b", "suya"),
    (r"\b([Pp])rogram(s?)\b(?! (?:a|the) computer)", r"\1rogramme\2"), (r"\b([Aa])irplane(s?)\b", r"\1eroplane\2"), (r"\bdurians\b", "mangoes"), (r"\bdurian\b", "mango"), (r"\bDurian\b", "Mango"), (r"\ba rambutan\b", "an agbalumo"), (r"\brambutans?\b", "agbalumo (African star apple)"), (r"\bsatsumas?\b", "orange"), (r"\bsausage rolls?\b", "meat pie"), (r"\bgarbage\b", "rubbish"), (r"\bGarbage\b", "Rubbish"), (r"\bfortnight\b", "two weeks"), (r"\b([Cc])ounterclockwise\b", r"anticlockwise"), (r"\bfetus(es)?\b", r"foetus\1"), (r"\bfetal\b", "foetal"), (r"\bbiro\b", "biro"),
]
for a, b in zip(["Johannesburg", "Cape Town", "Durban", "Pretoria", "Soweto", "Polokwane", "Bloemfontein", "Port Elizabeth", "Gqeberha", "East London", "Kimberley",
                 "Quezon City", "Cebu City", "Davao City", "Manila", "Pasig", "Baguio", "Iloilo City", "Bacolod", "Zamboanga City", "Tacloban", "Cagayan de Oro"],
                ng_common.PLACES * 2):
    NG_REP.append((r"\b" + a + r"\b", b))

NG_OK = {"football", "soccer", "pupil", "pupils", "grade", "grades", "lion", "lions", "elephant", "elephants", "hippo", "leopard", "baobab", "acacia",
         "crocodile", "crocodiles", "giraffe", "giraffes"}
LEAKS = sorted(set(w for w in za_sci.LEAKS if w not in NG_OK) | {
    "south africa", "south african", "south africans", "eskom", "sasol", "karoo", "fynbos", "springbok", "springboks", "braai", "rand", "rands",
    "witwatersrand", "drakensberg", "kruger", "limpopo", "gauteng", "kwazulu-natal", "taung", "sterkfontein", "load shedding", "spaza", "tuck shop",
    "caps", "nsc", "matric", "rugby", "cricket", "bobotie", "biltong", "rooibos", "protea", "proteas", "zebra", "zebras", "rhino", "rhinos", "meerkat",
    "wildebeest", "kangaroo", "koala", "platypus",
    "philippines", "philippine", "filipino", "filipinos", "pagasa", "phivolcs", "typhoon", "typhoons", "jeepney", "jeepneys", "carabao", "sari-sari",
    "peso", "pesos", "luzon", "visayas", "mindanao", "mayon", "taal", "pinatubo", "manila", "cebu", "davao", "tagalog", "habagat", "amihan", "tarsier",
    "adobo", "sinigang", "barangay", "ndrrmc", "deped", "matatag", "quezon", "palawan", "bohol", "batangas", "laguna", "monsoon", "monsoons",
    "polar bear", "polar bears", "penguin", "penguins", "arctic fox", "seal pup", "walrus", "reindeer", "caribou", "moose",
    "snow", "snowy", "snowfall", "snowflake", "snowflakes", "snowman", "snowball", "blizzard", "sled", "sledding", "ski", "skiing", "skis",
    "skating", "ice skating", "frost", "frosty", "icy road", "icy roads", "ice rink", "winter", "winters", "autumn", "snowmelt", "snowplow", "snowstorm",
    "hockey", "puck", "pucks", "sleigh", "central heating", "fireplace", "radiator", "frostbite", "icicle", "icicles", "winter coat", "mittens", "toboggan",
    "christmas tree", "tornado", "tornadoes", "hurricane", "hurricanes", "oak", "oaks", "acorn", "acorns", "robin", "robins", "bear", "bears",
    "wolf", "wolves", "elk", "energy star", "butterfly pea", "daffodil", "daffodils", "kiwi", "bluebell", "bluebells", "maple", "beech", "conker", "conkers",
})
LEAK_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in LEAKS), re.I)
SEASONAL = re.compile(r"\b(in (the )?(winter|autumn)|winter (day|morning|night|clothes|months?)|cold winter|autumn leaves|leaves (change colou?r|fall) in|in the fall|four seasons|in (the )?summer|(last|next|this|hot|dry|cold) summer|summer (day|days|holiday|holidays|evening|nights?))\b", re.I)
MONEY = re.compile(r"[£₹¢€₱]|\$\s?\d|\bR\s?\d|\bpence\b|\bcents?\b|°F|\b\d+ ?(ft|lb|oz|in\.)\b")


def _bad(text):
    t = uk_sci._text_of(text)
    bad = {m.group(1).lower() for m in LEAK_RE.finditer(t)}
    if MONEY.search(t):
        bad.add("money/units")
    if SEASONAL.search(t):
        bad.add("temperate seasons")
    return bad


def _patch():
    au_sci.GIRLS[:] = GIRLS
    au_sci.BOYS[:] = BOYS
    au_sci._G = _G
    au_sci._Bo = _Bo
    au_sci.FOREIGN = FOREIGN
    au_sci._NAME_RE = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in FOREIGN))
    au_sci.AU_REP = NG_REP
    au_sci._bad = _bad
    au_sci._ALLN = None


_patch()


class People:
    def __init__(self, R):
        self.R = R
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]

    def next(self):
        return self.R.choice(self.pool)


NG_DROP = [r"\b(Ontario|Toronto|Canad\w*|Australi\w*|Sydney|Britain|British|England|India|Singapore|Texas|South Africa\w*|Philippin\w*|Filipino)\b",
           r"\bRTP\b", r"room temperature and pressure", r"mg/dL", r"kcal", r"\bdata booklet\b", r"\bexam board\b",
           r"\b1/v\b", r"\b1/u\b", r"sign convention", r"\bu ?= ?[−-]", r"\bspecification\b", r"\bR ?\d", r"\b(Grade|Year) \d", r"\bMATATAG\b", r"\bQuarter \d"]


def _fix(s):
    s = uk_sci.uk_text(s)
    s = au_sci._NAME_RE.sub(lambda m: (GIRLS if m.group(1) in _G else BOYS)[sum(map(ord, m.group(1))) % len(GIRLS if m.group(1) in _G else BOYS)], s)
    for a, b in NG_REP:
        s = re.sub(a, b, s)
    return au_sci._fix_an(s)


def _light(it):
    """Nigerian names and words on an item made outside the wrapped makers; None if a word does not fit"""
    if it is None:
        return None
    it = dict(it)
    it["q"], it["e"], it["c"] = _fix(it["q"]), _fix(it["e"]), [_fix(c) for c in it["c"]]
    if _bad(json.dumps(it, ensure_ascii=False)) or len({c.strip().lower() for c in it["c"]}) < 4:
        return None
    if re.search("|".join(NG_DROP), re.sub(r"<[^>]+>", " ", json.dumps(it, ensure_ascii=False))):
        return None
    return it


class X(cabc_sci.X):
    def _w(self, f, rep=(), drop=()):
        return self.src.wrap(f, list(rep), list(drop) + NG_DROP + cabc_sci.BC_DROP)

    def gen(self, mod, name, rep=(), drop=(), n=None):
        f = self.src(mod, name, list(rep), list(drop) + NG_DROP + cabc_sci.BC_DROP)
        return au_sci.limit(f, n) if n else f

    def w(self, f, rep=(), drop=(), n=None):
        g = self.src.wrap(f, list(rep), list(drop) + NG_DROP + cabc_sci.BC_DROP)
        return au_sci.limit(g, n) if n else g

    def f(self, factory, rep=(), drop=(), n=None, raw=True):
        g0 = super().f(factory, rep, drop, n, raw)

        def g():
            return _light(g0())
        g.__name__ = getattr(g0, "__name__", "f")
        return g

    def o(self, mod, slug, s, year=None):
        g0 = super().o(mod, slug, s, year)

        def g():
            return _light(g0())
        g.__name__ = g0.__name__
        return g


def _units(mod, year):
    import importlib
    m = importlib.import_module(mod)
    us = m.UNITS(year) if len(inspect.signature(m.UNITS).parameters) else m.UNITS()
    return {u["slug"]: u for u in us}


def _area_ok(a):
    assert a in THEMES or a in SSS, a


def NU(area, sort, slug, std, title, short, what, kb, ks, a, b, ex, mist, faq, sets, allow=(), topic=None):
    _area_ok(area)
    return dict(area=area, sort=sort, slug=slug, topic=topic or title, std=std, title=title, short=short, what=what, kb=kb, ks=ks,
                think="<p>%s</p><p>%s</p>" % (a, b), ex=ex, mist=mist, faq=faq, sets=sets, allow=tuple(allow))


def NC(area, sort, slug, src, std=None, **ov):
    """a unit with the text and sets of another unit (mod:slug[:year]); any field can be overridden"""
    _area_ok(area)
    bits = src.split(":")
    mod, sslug, year = bits[0], bits[1], (int(bits[2]) if len(bits) > 2 else None)
    u = _units(mod, year)[sslug]
    think = u["think"]
    assert isinstance(think, str), "kid-style lesson in %s: give a= and b=" % src
    d = dict(area=area, sort=sort, slug=slug, topic=u["title"], std=std or u["std"], title=u["title"], short=u["short"], what=u.get("what"),
             kb=u["kb"], ks=u["ks"], think=think, ex=u["ex"], mist=u["mist"], faq=u["faq"], allow=tuple(u.get("allow", ())),
             sets=lambda X: [(t, [(X.o(mod, sslug, i + 1, year), 20)]) for i, t in enumerate(_titles(X, mod, sslug, year))])
    if u.get("sets") is not None and mod.startswith("ph_s"):
        d["sets"] = u["sets"]          # Philippine units: their own set lists (they already point to the sources)
    for k, v in ov.items():
        if k in ("a", "b", "sub"):
            continue
        d[k] = v
    if "a" in ov:
        d["think"] = "<p>%s</p><p>%s</p>" % (ov["a"], ov["b"])
    d["sub"] = list(ov.get("sub", ()))
    d["fill"] = dict(ov.get("fill", {}))
    for k in ("std", "title", "short", "kb", "ks", "think", "ex", "mist", "faq", "what", "topic"):
        if d.get(k) is not None and d["sub"]:
            t = json.dumps(d[k], ensure_ascii=False)
            for a, b in d["sub"]:
                t = t.replace(json.dumps(a, ensure_ascii=False)[1:-1], json.dumps(b, ensure_ascii=False)[1:-1])
            d[k] = json.loads(t)
            if k == "ex":
                d[k] = [tuple(e) for e in d[k]]
            if k == "faq":
                d[k] = [tuple(e) for e in d[k]]
    return d


def _titles(X, mod, slug, year):
    u = X._units(mod, year)[slug]
    X._sync()
    fn = u["sets"]
    spec = fn(X) if len(inspect.signature(fn).parameters) else fn()
    return [t for t, _ in spec]


def _subt(t, u):
    for a, b in u.get("sub", ()):
        t = t.replace(a, b)
    return t


def level(grade):
    k, n = grade.rsplit("-", 1)
    return int(n) + {"primary": 0, "jss": 6, "sss": 9}[k]


def seed_of(grade, sort):
    return 74000 + 100 * level(grade) + sort


def label(grade):
    k, n = grade.rsplit("-", 1)
    return ("Primary %s" if k == "primary" else k.upper() + " %s") % n


def course(grade):
    k, n = grade.rsplit("-", 1)
    if k == "primary":
        return "Basic Science" if int(n) <= 3 else "Basic Science and Technology"
    return "Intermediate Science" if k == "jss" else None


# ---------------- numbers ----------------
_YEAR = re.compile(r"(?<![\d,.])((?:1[5-9]|20)\d\d)(?!\d|[.,]\d| ?(?:m|km|kg|g|J|kJ|N|W|kW|s|mm|cm|nm|K|Pa|kPa|V|A|Hz|t|L|mL|cm³|m³|dm³|people|pupils|students|°C|years? old)\b)")


def ng(s):
    """1,000-style numbers in text (not in tags); years are kept"""
    keep = {}

    def hold(m):
        k = "⁣%d⁣" % len(keep)
        keep[k] = m.group(1)
        return k
    out = []
    for p in re.split(r"(<svg.*?</svg>|<[^>]+>)", s, flags=re.S):
        if p.startswith("<"):
            out.append(p)
            continue
        p = _YEAR.sub(hold, p)
        p = re.sub("(\\d{1,3})[  ](\\d{3})(?:[  ](\\d{3}))?(?![\\d])", lambda m: m.group(1) + "," + m.group(2) + ("," + m.group(3) if m.group(3) else ""), p)
        p = re.sub(r"(?<![\d.,:/#−-])(\d{4,6})(?![\d]|[.,]\d)", lambda m: "{:,}".format(int(m.group(1))), p)
        out.append(p)
    s = "".join(out)
    for k, v in keep.items():
        s = s.replace(k, v)
    return s


AMERICAN = re.compile(r"\b(colors?|colored|center(s|ed)?|meters?|liters?|behaviors?|favorite|aluminum|fiber|gray|organiz(e|ed|es|ing|ation)|recogniz(e|ed|es|ing)|realiz(e|ed|es|ing)|"
                      r"analyz(e|ed|es|ing)|vapor|odor|neighbor\w*|flashlights?|gasoline|sidewalks?|cookies?|candy|candies|mom|esophag\w*|estrogen|fetus|hemoglobin|"
                      r"programs?|tires?|counterclockwise|jewelry|plow|airplanes?)\b")
METER_OK = re.compile(r"\b(sound level|light|parking|water|gas|electricity|data|level|speed|power|pH|moisture|rain|newton|volt|amp|ohm|joule|flow|exposure) meters?\b", re.I)


def build(mod, grade, slug):
    _patch()     # importing the Philippine units patches au_sci for the Philippines; set it back to Nigeria
    lv = level(grade)
    us_ = mod.UNITS(grade) if len(inspect.signature(mod.UNITS).parameters) else mod.UNITS()
    u = next(x for x in us_ if x["slug"] == slug)
    sort = u["sort"]
    WHO["p"] = "pupils" if lv <= 6 else "students"
    U = Unit(seed_of(grade, sort))
    R = U.R
    P = People(R)
    uk_sci.USED.clear()
    au_sci.SEEN.clear()
    caon_sci.SEEN.clear()
    src = au_sci._Src(U, P)
    x = X(U, R, P, src)
    spec = u["sets"](x)
    fill = u.get("fill", {})

    def wm(m):
        def g():
            return _light(m())
        g.__name__ = getattr(m, "__name__", "m")
        return g
    spec2 = []
    for t, ms in spec:
        ms = list(ms)
        for fsrc in ([fill[t]] if isinstance(fill.get(t), str) else fill.get(t, [])):
            b = fsrc.split(":")
            ms.append((x.o(b[0], b[1], int(b[2]), int(b[3]) if len(b) > 3 else None), 20))
        spec2.append((_subt(t, u), [(wm(m), n) for m, n in ms]))
    spec = spec2
    sets = U.sets(spec)
    area = u["area"]
    for st in sets:
        st["title"] = ng(_fix(st["title"]))
        for it in st["items"]:
            for k in ("q", "e"):
                it[k] = ng(re.sub(r"(?<=[\s(=])-(?=\d)", "−", caon_sci._quotes(it[k])))
            it["c"] = [ng(re.sub(r"(?<=[\s(=])-(?=\d)", "−", caon_sci._quotes(c))) for c in it["c"]]
            assert len({c.strip().lower() for c in it["c"]}) == 4, it["c"]
    think = _fix(u["think"])
    ex = [(_fix(q), [_fix(s) for s in st_], _fix(a)) for q, st_, a in u["ex"]]
    mist = [_fix(m) for m in u["mist"]]
    body = ng(lesson(think, ex, mist))
    faq = [(ng(_fix(q)), ng(_fix(a))) for q, a in u["faq"]]
    for k in ("std", "kb", "ks", "short", "topic", "title"):
        u[k] = ng(_fix(re.sub(r"<sub>([^<]*)</sub>", r"\1", u[k])))
    if not u.get("what"):
        u["what"] = ", ".join(t[0].lower() + t[1:] for t, _ in spec[:4]) + " and " + spec[4][0][0].lower() + spec[4][0][1:]
    what = ng(_fix(re.sub(r"<[^>]+>", "", u["what"])))
    name = label(grade)
    if lv <= 9:
        c = course(grade)
        meta = "Free %s %s worksheets (NERDC curriculum, theme: %s): %s. 100 questions with answers." % (name, c, area, what)
        seo = "%s %s: %s Worksheets (NERDC)" % (name, c, u["title"])
        if len(seo) > 95:
            seo = "%s %s: %s Worksheets" % (name, c, u["title"])
        if len(seo) > 95:
            seo = "%s Science: %s Worksheets" % (name, u["title"])
        code = "%s %s: %s" % (name, c, area)
        std = "%s (summary of the %s curriculum, %s, theme: %s)" % (u["std"], c, name, area)
    else:
        meta = "Free %s %s worksheets (senior secondary curriculum, WAEC and NECO): %s. 100 questions with answers." % (name, area, what)
        seo = "%s %s: %s Worksheets (WAEC/NECO)" % (name, area, u["title"])
        if len(seo) > 95:
            seo = "%s %s: %s Worksheets" % (name, area, u["title"])
        code = "%s %s: %s" % (name, area, u["topic"])
        std = "%s (summary of the senior secondary %s curriculum, %s; WAEC and NECO syllabuses)" % (u["std"], area, name)
    blob = json.dumps([u["title"], seo, u["short"], meta, u["kb"], u["ks"], body, faq, sets, std], ensure_ascii=False)
    bad = sorted(_bad(blob) - set(u["allow"]))
    if bad:
        low = blob.lower()
        raise AssertionError("Words that do not fit Nigeria: %s %s" % (bad, [low[max(0, low.find(w) - 100):low.find(w) + 40] for w in bad]))
    txt = re.sub(r"<[^>]+>", " ", blob)
    m = re.search("|".join(NG_DROP[:1]), txt)
    assert not m, "Word left: %s [%s]" % (m.group(0), txt[max(0, m.start() - 150):m.end() + 60])
    m = au_sci._NAME_RE.search(txt)
    assert not m, "Foreign name left: %s [%s]" % (m.group(1), txt[max(0, m.start() - 100):m.end() + 40])
    assert "\\" not in blob
    t2 = METER_OK.sub("", txt)
    m = AMERICAN.search(t2)
    assert not m, ("American spelling", m.group(0), t2[max(0, m.start() - 120):m.end() + 40])
    sci_common.make(grade, slug, sort, code, std, u["title"], seo, u["short"], meta, u["kb"], u["ks"], body,
                    faq, sets, domain=area, country="ng", url=URL)
