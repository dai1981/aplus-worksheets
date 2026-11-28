# -*- coding: utf-8 -*-
"""
Philippine science (DepEd MATATAG Science, Grades 3-10): country `ph`, subject `science`, grade `grade-N`.
  Domains: Grades 3-6 Materials / Living Things / Force, Motion, and Energy / Earth and Space;
           Grades 7-10 Science of Materials / Life Science / Force, Motion, and Energy / Earth and Space Science.
  PU(area, sort, slug, topic, std, title, short, what, kb, ks, a, b, ex, mist, faq, sets, allow=())   own text
  CP(area, sort, slug, src, std, **override)   text and the 5 sets of another unit ("mod:slug[:year]", X-style units:
      caon_sci*, caon_hs*, cabc_s*, au_sr*, za_s*), rewritten for the Philippines
  sets = lambda X: S(X, [(title, "mod:slug:set[:year]") or (title, [(part, n)])])  (cabc_sci.S, GM)
  Every maker goes through the shared pipeline (British spelling, names, drops), then build() turns the text into
  American English (color, center, meter, -ize, gasoline, flashlight, mom) with Filipino names and places, and
  1,000-style numbers (years kept).  Items with other countries' places, money, imperial units, snow and northern
  winter scenes are dropped.
build(mod, grade, slug): seed 73000 + 100 * grade + sort.
"""
import inspect
import json
import re
import za_sci  # noqa: F401  (patches au_sci for South Africa on import; ph_sci patches it again below)
import au_sci
import caon_sci
import cabc_sci
import uk_sci
import sci_common
import za_common
import ph_common
from sci_common import lesson, Unit
from cabc_sci import S, GM  # noqa: F401

URL = "https://www.deped.gov.ph/matatagcurriculumk147/"
D_LOW = ("Materials", "Living Things", "Force, Motion, and Energy", "Earth and Space")
D_HIGH = ("Science of Materials", "Life Science", "Force, Motion, and Energy", "Earth and Space Science")
D_SHS = ("Physical Science", "Life Science", "Earth and Space Science", "Biology", "Chemistry", "Physics")
URL_SHS = "https://www.deped.gov.ph/strengthened-shs-program/"
URL_COURSE = {"Biology 1": "https://www.deped.gov.ph/wp-content/uploads/Biology-1.pdf", "Biology 2": "https://www.deped.gov.ph/wp-content/uploads/Biology-2.pdf",
              "Chemistry 1": "https://www.deped.gov.ph/wp-content/uploads/Chemistry-1.pdf", "Physics 1": "https://www.deped.gov.ph/wp-content/uploads/Physics-1.pdf",
              "Physics 2": "https://www.deped.gov.ph/wp-content/uploads/Physics-2-1.pdf", "Earth and Space Science 1": "https://www.deped.gov.ph/wp-content/uploads/Earth-and-Space-Science-1.pdf"}
QUARTER = {3: D_LOW, 4: D_LOW, 5: D_LOW, 6: D_LOW,
           7: ("Science of Materials", "Life Science", "Force, Motion, and Energy", "Earth and Space Science"),
           8: ("Life Science", "Science of Materials", "Earth and Space Science", "Force, Motion, and Energy"),
           9: ("Force, Motion, and Energy", "Earth and Space Science", "Life Science", "Science of Materials"),
           10: ("Earth and Space Science", "Force, Motion, and Energy", "Science of Materials", "Life Science")}

GIRLS, BOYS = list(ph_common.GIRLS), list(ph_common.BOYS)
_G = set(au_sci._G) | set(caon_sci.GIRLS) | set(za_common.GIRLS) | set(za_common.FOREIGN_GIRLS) | set(ph_common.FOREIGN_GIRLS)
_Bo = set(au_sci._Bo) | set(caon_sci.BOYS) | set(za_common.BOYS) | set(za_common.FOREIGN_BOYS) | set(ph_common.FOREIGN_BOYS)
_G |= set(GIRLS)
_Bo |= set(BOYS)
FOREIGN = sorted((_G | _Bo) - set(GIRLS) - set(BOYS), key=len, reverse=True)

# words in the shared (British) pipeline that we change before the American step
PH_REP = [
    (r"\bpupils\b", "learners"), (r"\bPupils\b", "Learners"), (r"\bpupil's\b", "learner's"),
    (r"\b([Aa]) pupil (drew|wrote|says|said|thinks|measured|made|was|is|has|wants|tested|noticed)\b", r"\1 learner \2"),
    (r"\bPupil\b", "Learner"), (r"\bpupil\b(?! of)", "learner"),
    (r"\bYear ([1-9])\b", r"Grade \1"), (r"\bmol dm⁻³", "mol/L"), (r"\bmol·dm⁻³", "mol/L"), (r"\bdm³", "L"), (r"9\.81(?!\d)", "9.8"),
    (r"\b(sound level|light|parking|water|gas|electricity|data|level|speed|power|pH|moisture|rain|newton) metres?\b", r"\1 meter"),
    (r"\bfootballs\b", "basketballs"), (r"\bfootball\b", "basketball"), (r"\bFootball\b", "Basketball"), (r"\bnetball\b", "volleyball"),
    (r"\bgum trees\b", "mahogany trees"), (r"\bgum tree\b", "mahogany tree"), (r"\bbushland\b", "forest"), (r"\bthe bush\b", "the forest"),
    (r"\bmaple\b", "narra"), (r"\bpine\b(?= cones?)", "pine"), (r"\boak trees?\b", "narra tree"),
    (r"\bbadgers?\b", "civet"), (r"\bhedgehogs?\b", "shrew"), (r"\bsquirrels?\b", "squirrel"), (r"\bfoxes\b", "civets"), (r"\bfox\b", "civet"),
    (r"\bdeer\b", "Philippine deer"), (r"\bPhilippine Philippine deer\b", "Philippine deer"),
    (r"\bhot radiator\b", "hot stove"), (r"\bradiators?\b", "electric fan"), (r"\bon (its|a|his|her) lead\b", r"on \1 leash"), (r"\bfortnight\b", "two weeks"), (r"\bthe fortnight\b", "the two weeks"), (r"\bbiro\b", "ballpen"), (r"\bballpoint pen\b", "ballpen"),
]
for a, b in zip(["Johannesburg", "Cape Town", "Durban", "Pretoria", "Soweto", "Polokwane", "Bloemfontein", "Port Elizabeth", "Gqeberha", "East London", "Kimberley"],
                ["Quezon City", "Cebu City", "Davao City", "Manila", "Pasig", "Baguio", "Iloilo City", "Bacolod", "Zamboanga City", "Tacloban", "Cagayan de Oro"]):
    PH_REP.append((r"\b" + a + r"\b", b))

LEAKS = sorted(set(w for w in za_sci.LEAKS if w not in ("high school", "elevator", "sidewalk", "garbage", "candy", "cookie", "cookies", "gasoline",
                                                        "flashlight", "aluminum", "middle school", "popsicle", "popsicles", "faucet", "grade", "grades", "soccer", "football")) | {
    "south africa", "south african", "south africans", "eskom", "sasol", "karoo", "fynbos", "springbok", "springboks", "braai", "rand", "rands",
    "witwatersrand", "drakensberg", "kruger", "limpopo", "gauteng", "kwazulu-natal", "taung", "sterkfontein", "load shedding", "spaza", "tuck shop",
    "learnt", "caps", "nsc", "matric", "rugby", "cricket", "bobotie", "biltong", "rooibos", "protea", "proteas", "baobab", "acacia", "zebra", "zebras",
    "lion", "lions", "giraffe", "giraffes", "elephant", "elephants", "hippo", "rhino", "rhinos", "cheetah", "leopard", "meerkat", "ostrich", "wildebeest",
    "polar bear", "polar bears", "penguin", "penguins", "arctic fox", "seal pup", "walrus", "reindeer", "caribou",
    "snow", "snowy", "snowfall", "snowflake", "snowflakes", "snowman", "snowball", "blizzard", "sled", "sledding", "ski", "skiing", "skis",
    "skating", "ice skating", "white flakes", "frost", "frosty", "icy road", "icy roads", "ice rink", "winter", "winters", "autumn", "snowshoe", "snowmelt", "snowplow", "snowplows", "snowboard", "snowboards", "snowing", "snowstorm", "snowstorms", "snowfield", "snowfields", "hockey", "puck", "pucks", "sleigh", "glacier skiing", "central heating", "fireplace", "heater", "heaters", "radiator", "frostbite", "icicle", "icicles", "winter coat", "mittens", "toboggan", "christmas tree",
})
LEAK_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in LEAKS), re.I)
SEASONAL = re.compile(r"\b(in (the )?(winter|autumn)|winter (day|morning|night|clothes|months?)|cold winter|autumn leaves|leaves (change colou?r|fall) in|in the fall)\b", re.I)


def _bad(text):
    t = uk_sci._text_of(text)
    bad = {m.group(1).lower() for m in LEAK_RE.finditer(t)}
    if re.search(r"[£₹¢€]|\$\s?\d|\bR\d|\bpence\b|°F|\b\d+ ?(ft|lb|oz|in\.)\b", t):
        bad.add("money/units")
    if SEASONAL.search(t):
        bad.add("temperate seasons")
    return bad


_US_OK = set(uk_sci.LEAKS) - {"fahrenheit", "gallon", "gallons", "inch", "inches", "mile", "miles", "ounce", "ounces", "pound", "pounds", "cilantro", "zucchini", "fries", "eggplant"}
FINAL_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in sorted(set(LEAKS) - _US_OK)), re.I)


def _bad_final(text):
    t = uk_sci._text_of(text)
    bad = {m.group(1).lower() for m in FINAL_RE.finditer(t)}
    if re.search(r"[£₹¢€]|\$\s?\d|\bR\d|\bpence\b|°F|\b\d+ ?(ft|lb|oz|in\.)\b", t):
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
    au_sci.AU_REP = PH_REP
    au_sci._bad = _bad
    au_sci._ALLN = None


_patch()


class People:
    def __init__(self, R):
        self.R = R
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]

    def next(self):
        return self.R.choice(self.pool)


PH_DROP = [r"\b(Ontario|Toronto|Canad\w*|Australi\w*|Sydney|Britain|British|England|India|Singapore|Texas|South Africa\w*)\b",
           r"\bRTP\b", r"room temperature and pressure", r"\b24 ?(dm|L)\b", r"mg/dL", r"kcal", r"\bdata booklet\b", r"\bexam board\b",
           r"g ?= ?10 ?N ?/ ?kg", r"\(g = 10\b", r"\b1/v\b", r"\b1/u\b", r"sign convention", r"\bu ?= ?[−-]", r"\bspecification\b",
           r"\bR ?\d", r"\bGrade (1[1-2])\b"]


def _light(it):
    """Filipino names and words on an item made outside the wrapped makers (Ontario own makers); None if a word does not fit"""
    if it is None:
        return None
    it = dict(it)

    def fx(s):
        s = uk_sci.uk_text(s)
        s = au_sci._NAME_RE.sub(lambda m: (GIRLS if m.group(1) in _G else BOYS)[sum(map(ord, m.group(1))) % len(GIRLS if m.group(1) in _G else BOYS)], s)
        for a, b in PH_REP:
            s = re.sub(a, b, s)
        return au_sci._fix_an(s)
    it["q"], it["e"], it["c"] = fx(it["q"]), fx(it["e"]), [fx(c) for c in it["c"]]
    if _bad(json.dumps(it, ensure_ascii=False)) or len({c.strip().lower() for c in it["c"]}) < 4:
        return None
    if re.search("|".join(PH_DROP), re.sub(r"<[^>]+>", " ", json.dumps(it, ensure_ascii=False))):
        return None
    return it


class X(cabc_sci.X):
    def _w(self, f, rep=(), drop=()):
        return self.src.wrap(f, list(rep), list(drop) + PH_DROP + cabc_sci.BC_DROP)

    def gen(self, mod, name, rep=(), drop=(), n=None):
        f = self.src(mod, name, list(rep), list(drop) + PH_DROP + cabc_sci.BC_DROP)
        return au_sci.limit(f, n) if n else f

    def w(self, f, rep=(), drop=(), n=None):
        g = self.src.wrap(f, list(rep), list(drop) + PH_DROP + cabc_sci.BC_DROP)
        return au_sci.limit(g, n) if n else g

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


def PU(area, sort, slug, topic, std, title, short, what, kb, ks, a, b, ex, mist, faq, sets, allow=(), course=None, q=None):
    assert area in D_LOW or area in D_HIGH or area in D_SHS, area
    return dict(area=area, sort=sort, slug=slug, topic=topic, std=std, title=title, short=short, what=what, kb=kb, ks=ks,
                think="<p>%s</p><p>%s</p>" % (a, b), ex=ex, mist=mist, faq=faq, sets=sets, allow=tuple(allow), course=course, q=q)


def CP(area, sort, slug, src, std, topic=None, **ov):
    """a unit with the text and sets of another unit (mod:slug[:year]); any field can be overridden"""
    assert area in D_LOW or area in D_HIGH or area in D_SHS, area
    bits = src.split(":")
    mod, sslug, year = bits[0], bits[1], (int(bits[2]) if len(bits) > 2 else None)
    u = _units(mod, year)[sslug]
    think = u["think"]
    assert isinstance(think, str), "kid-style lesson in %s: give think=" % src
    d = dict(area=area, sort=sort, slug=slug, topic=topic or u["title"], std=std, title=u["title"], short=u["short"], what=None,
             kb=u["kb"], ks=u["ks"], think=think, ex=u["ex"], mist=u["mist"], faq=u["faq"], allow=tuple(u.get("allow", ())),
             sets=lambda X: [(t, [(X.o(mod, sslug, i + 1, year), 20)]) for i, t in enumerate(_titles(X, mod, sslug, year))])
    for k, v in ov.items():
        if k in ("a", "b"):
            continue
        d[k] = v
    if "a" in ov:
        d["think"] = "<p>%s</p><p>%s</p>" % (ov["a"], ov["b"])
    return d


def _titles(X, mod, slug, year):
    u = X._units(mod, year)[slug]
    X._sync()
    fn = u["sets"]
    spec = fn(X) if len(inspect.signature(fn).parameters) else fn()
    return [t for t, _ in spec]


def seed_of(grade, sort):
    return 73000 + 100 * grade + sort


# ---------------- American English and Philippine numbers ----------------
_US = [
    (r"\b(\w*(?:organ|recogn|real|special|minim|maxim|crystall|fertil|steril|neutral|ion|polar|stabil|util|categor|summar|memor|visual|emphas|harmon|hybrid|polymer|synthes|oxid|vapor|vapour|character|hypothes|optim|quant|capital|delocal|terminal|apolog|critic|standard|magnet|colon|sympath|immun|mobil|vandal|pasteur|homogen|ion|desalin|vulcan|sensit|motor|central|civil|industrial|global|urban|social|natural|symbol|metabol|caramel|carbon|fossil|item|emphas|patron|subsid|computer|digit|local|general|final|normal|legal|equal|modern|western|tropical|ideal))is(e|ed|es|ing|ation|ations|er|ers)\b", r"\1iz\2"),
    (r"\b(\w*(?:ana|para|cata|hydro|electro|dia|pyro))lys(e|ed|es|ing|er|ers)\b", r"\1lyz\2"),
    (r"\b([Cc])olour", r"\1olor"), (r"\b([Dd])iscolour", r"\1iscolor"), (r"\b([Bb])ehaviour", r"\1ehavior"), (r"\b([Ff])avour", r"\1avor"), (r"\b([Ff])lavour", r"\1lavor"),
    (r"\b([Nn])eighbour", r"\1eighbor"), (r"\b([Oo])dour", r"\1dor"), (r"\b([Vv])apour", r"\1apor"), (r"\b([Ll])abour", r"\1abor"), (r"\b([Hh])umour", r"\1umor"),
    (r"\b([Hh])arbour", r"\1arbor"), (r"\b([Rr])umour", r"\1umor"), (r"\b([Aa])rmour", r"\1rmor"), (r"\b([Hh])onour", r"\1onor"), (r"\b([Tt])umour", r"\1umor"),
    (r"\b([Ss])avour", r"\1avor"), (r"\b([Vv])igour", r"\1igor"),
    (r"\b(\w*)metre(s?)\b", r"\1meter\2"), (r"\b(\w*)litre(s?)\b", r"\1liter\2"), (r"\b(\w*)centre(s|d)?\b", r"\1center\2"), (r"\bCentre(s|d)?\b", r"Center\1"), (r"\b([Ff])ibre(s?)\b", r"\1iber\2"),
    (r"\b([Tt])heatre", r"\1heater"), (r"\b([Ss])ombre", r"\1omber"), (r"\bgrey", "gray"), (r"\bGrey", "Gray"), (r"\b([Aa])luminium\b", r"\1luminum"),
    (r"\b([Cc])aesium\b", r"\1esium"), (r"\b([Ss])ulphur", r"\1ulfur"), (r"\b([Mm])ould", r"\1old"), (r"\b([Ss])moulder", r"\1molder"),
    (r"\btyres\b", "tires"), (r"\btyre\b", "tire"), (r"\bTyres?\b", "Tires"), (r"\b([Pp])rogramme(s?)\b", r"\1rogram\2"), (r"\b([Cc])atalogue", r"\1atalog"),
    (r"\b([Aa])nalogue", r"\1nalog"), (r"\b([Dd])ialogue", r"\1ialog"), (r"\b([Oo])esophag", r"\1sophag"), (r"\bOesophag", "Esophag"), (r"\boesophag", "esophag"),
    (r"\b([Hh])aem", r"\1em"), (r"([Aa])naem", r"\1nem"), (r"([Ll])eukaem", r"\1eukem"), (r"\b([Ff])oet(us|uses|al)\b", r"\1et\2"), (r"\bOestrogen", "Estrogen"),
    (r"\boestrogen", "estrogen"), (r"\b([Dd])iarrhoea", r"\1iarrhea"), (r"\b([Pp])aediatric", r"\1ediatric"), (r"\bOedema", "Edema"), (r"\boedema", "edema"), (r"\b([Mm])anoeuvr(e|es|ed|ing)", r"\1aneuver"),
    (r"\b([Ee])ncyclopaedia", r"\1ncyclopedia"), (r"\b([Ll])eukocyte", r"\1eukocyte"), (r"\b([Hh])aemo", r"\1emo"), (r"\boestrus", "estrus"),
    (r"\b([Dd])efence(s?)\b", r"\1efense\2"), (r"\b([Oo])ffence(s?)\b", r"\1ffense\2"), (r"\b([Ll])icence(s?)\b", r"\1icense\2"), (r"\b([Pp])ractis(e|ed|es|ing)\b", r"\1ractic\2"),
    (r"\b([Tt]ravel|[Ll]abel|[Mm]odel|[Ff]uel|[Cc]ancel|[Ss]ignal|[Ll]evel|[Tt]otal|[Cc]hannel|[Cc]ounsel|[Dd]ial|[Tt]unnel|[Mm]arvel|[Pp]edal|[Ee]qual|[Rr]ival|[Ss]hovel|[Jj]ewel|[Qq]uarrel)l(ed|ing|er|ers)\b", r"\1\2"), (r"\b([Pp])ersonalis", r"\1ersonaliz"), (r"\b([Gg])alvanis", r"\1alvaniz"), (r"\b([Ss])ystematis", r"\1ystematiz"),
    (r"\b([Jj])ewellery\b", r"\1ewelry"), (r"\b([Pp])lough", r"\1low"), (r"\bkerb", "curb"), (r"\b([Aa])nticlockwise\b", "counterclockwise"), (r"\bAnticlockwise\b", "Counterclockwise"),
    (r"\b([Aa])eroplane(s?)\b", r"\1irplane\2"), (r"\b([Aa])ero(?=dynamic|sol)", r"\1ero"), (r"\b([Ss])ceptic", r"\1keptic"), (r"\b([Cc])heque", r"\1heck"),
    (r"\b([Ll])earnt\b", r"\1earned"), (r"\b([Bb])urnt\b", r"\1urned"), (r"\b([Ss])pelt\b", r"\1pelled"), (r"\b([Ss])pilt\b", r"\1pilled"), (r"\b([Dd])reamt\b", r"\1reamed"),
    (r"\btorches\b", "flashlights"), (r"\btorch\b", "flashlight"), (r"\bTorch\b", "Flashlight"), (r"\bpetrol\b", "gasoline"), (r"\bPetrol\b", "Gasoline"),
    (r"\bpetrol station\b", "gas station"), (r"\bMum\b", "Mom"), (r"\bmum\b", "mom"), (r"\bMummy\b", "Mommy"),
    (r"\brubbish bins?\b", "trash can"), (r"\brubbish\b", "garbage"), (r"\bRubbish\b", "Garbage"), (r"\bpavements\b", "sidewalks"), (r"\bpavement\b", "sidewalk"),
    (r"\bbiscuits\b", "cookies"), (r"\bbiscuit\b", "cookie"), (r"\bsweets\b", "candies"), (r"\bSweets\b", "Candies"), (r"\blorries\b", "trucks"), (r"\blorry\b", "truck"),
    (r"\bmobile phones\b", "cellphones"), (r"\bmobile phone\b", "cellphone"), (r"\bmaths\b", "math"), (r"\bMaths\b", "Math"), (r"\bcar park\b", "parking lot"),
    (r"\bjumpers\b", "sweaters"), (r"\bjumper\b", "sweater"), (r"\bjerseys\b", "sweaters"), (r"\bjersey\b", "sweater"), (r"\bnappies\b", "diapers"), (r"\bnappy\b", "diaper"),
    (r"\bcling (film|wrap)\b", "plastic wrap"), (r"\bpolythene\b", "polyethylene"), (r"\bspring balances\b", "spring scales"), (r"\bspring balance\b", "spring scale"),
    (r"\bearthed\b", "grounded"), (r"\bearthing\b", "grounding"), (r"\bcotton wool\b", "cotton balls"), (r"\bice lollies\b", "popsicles"), (r"\b([Aa])n ice lolly\b", r"\1 popsicle"), (r"\bice lolly\b", "popsicle"),
    (r"\bfridges\b", "refrigerators"), (r"\bfridge\b", "refrigerator"), (r"\btins\b", "cans"), (r"\btin can\b", "can"), (r"\bcrisps\b", "chips"), (r"\btap water\b", "tap water"),
    (r"\bthe taps?\b", "the faucet"), (r"\bdrawing pins?\b", "thumbtack"), (r"\bwoodlice\b", "pill bugs"), (r"\bwoodlouse\b", "pill bug"), (r"\bladybirds\b", "ladybugs"),
    (r"\bladybird\b", "ladybug"), (r"\bpushchair\b", "stroller"), (r"\bpram\b", "baby carriage"), (r"\bsellotape\b", "tape"), (r"\bplasticine\b", "modeling clay"),
    (r"\bbonfire\b", "campfire"), (r"\bpostbox\b", "mailbox"), (r"\btrolley\b", "cart"), (r"\btrolleys\b", "carts"), (r"\bdummy\b", "pacifier"),
    (r"\b([Mm])olecule", r"\1olecule"), (r"\bbar graph\b", "bar graph"), (r"\bmetre rule\b", "meter stick"), (r"\bmeter rule\b", "meter stick"),
    (r"\bbar charts\b", "bar graphs"), (r"\bbar chart\b", "bar graph"), (r"\bpie charts\b", "pie graphs"), (r"\bpie chart\b", "pie graph"), (r"\bper cent\b", "percent"), (r"\bgaol\b", "jail"), (r"\bstorey\b", "story"), (r"\bstoreys\b", "stories"), (r"\bdraughts\b", "drafts"), (r"\bdraught\b", "draft"),
    (r"\bhosepipe\b", "garden hose"), (r"\bwhilst\b", "while"), (r"\bamongst\b", "among"), (r"\bturquoise\b", "turquoise"),
    (r"\b([Ff])ertilis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1ertiliz"), (r"\b([Ss])terilis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1teriliz"), (r"\b([Nn])eutralis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1eutraliz"), (r"\b([Rr])ealis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1ealiz"), (r"\b([Oo])rganis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1rganiz"),
    (r"\b([Ii])onis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1oniz"), (r"\b([Mm])inimis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1inimiz"), (r"\b([Cc])arbonis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1arboniz"), (r"\b([Pp])olymeris(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1olymeriz"), (r"\b([Cc])rystallis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1rystalliz"),
    (r"\b([Ss])ummaris(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1ummariz"), (r"\b([Cc])ategoris(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1ategoriz"), (r"\b([Ee])vaporat", r"\1vaporat"), (r"\b([Ss])ymbolis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1ymboliz"), (r"\b([Hh])ypothesis(e|ed|es|ing)\b", r"\1ypothesiz\2"),
    (r"\b([Ss])ynthesis(e|ed|es|ing)\b", r"\1ynthesiz\2"), (r"\b([Ee])mphasis(e|ed|es|ing)\b", r"\1mphasiz\2"), (r"\b([Ss])pecialis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1pecializ"), (r"\b([Ss])tabilis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1tabiliz"),
    (r"\b([Uu])tilis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1tiliz"), (r"\b([Mm])agnetis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1agnetiz"), (r"\b([Oo])xidis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1xidiz"), (r"\b([Dd])enatur", r"\1enatur"), (r"\b([Pp])olaris(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1olariz"),
    (r"\b([Vv])isualis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1isualiz"), (r"\b([Rr])ecognis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1ecogniz"), (r"\b([Ii])mmunis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1mmuniz"), (r"\b([Hh])armonis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1armoniz"), (r"\b([Mm])emoris(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1emoriz"),
    (r"\b([Cc])haracteris(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1haracteriz"), (r"\b([Ss])tandardis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1tandardiz"), (r"\b([Mm])obilis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1obiliz"), (r"\b([Oo])ptimis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1ptimiz"), (r"\b([Dd])elocalis(?=(?:e|ed|es|ing|ation|ations|er|ers)\b)", r"\1elocaliz"),
    (r"\b([Aa])nalys(e|ed|es|ing)\b", r"\1nalyz\2"), (r"\b([Cc])atalys(e|ed|es|ing)\b", r"\1atalyz\2"), (r"\b([Hh])ydrolys(e|ed|es|ing)\b", r"\1ydrolyz\2"),
    (r"\b([Ee])lectrolys(e|ed|es|ing)\b", r"\1lectrolyz\2"), (r"\b([Pp])aralys(e|ed|es|ing)\b", r"\1aralyz\2"), (r"\b([Dd])ialys(e|ed|es|ing)\b", r"\1ialyz\2"),
]
_US = [(re.compile(a), b) for a, b in _US]
_YEAR = re.compile(r"(?<![\d,.])((?:1[5-9]|20)\d\d)(?!\d|[.,]\d| ?(?:m|km|kg|g|J|kJ|N|W|kW|s|mm|cm|nm|K|Pa|kPa|V|A|Hz|t|L|mL|cm³|m³|people|learners|students|°C|years? old)\b)")


def us(s):
    """American spelling and words in text (not in tags), and 1,000-style numbers; years are kept"""
    keep = {}

    def hold(m):
        k = "⁣%d⁣" % len(keep)
        keep[k] = m.group(1)
        return k
    out = []
    for p in re.split(r"(<svg.*?</svg>|<[^>]+>)", s, flags=re.S):
        if p.startswith("<"):
            if p.startswith("<svg"):
                p = re.sub(r"(>)([^<]+)(<)", lambda m: m.group(1) + _words(m.group(2)) + m.group(3), p)
                p = re.sub(r"(aria-label=')([^']*)(')", lambda m: m.group(1) + _words(m.group(2)) + m.group(3), p)
            out.append(p)
            continue
        p = _words(p)
        p = _YEAR.sub(hold, p)
        p = re.sub("(\\d{1,3})[  ](\\d{3})(?:[  ](\\d{3}))?(?![\\d])", lambda m: m.group(1) + "," + m.group(2) + ("," + m.group(3) if m.group(3) else ""), p)
        p = re.sub(r"(?<![\d.,:/#−-])(\d{4,6})(?![\d]|[.,]\d)", lambda m: "{:,}".format(int(m.group(1))), p)
        out.append(p)
    s = "".join(out)
    for k, v in keep.items():
        s = s.replace(k, v)
    return s


def _words(p):
    for rx, b in _US:
        p = rx.sub(b, p)
    return p


def build(mod, grade, slug):
    us_ = mod.UNITS(grade) if len(inspect.signature(mod.UNITS).parameters) else mod.UNITS()
    u = next(x for x in us_ if x["slug"] == slug)
    sort = u["sort"]
    U = Unit(seed_of(grade, sort))
    R = U.R
    P = People(R)
    uk_sci.USED.clear()
    au_sci.SEEN.clear()
    caon_sci.SEEN.clear()
    src = au_sci._Src(U, P)
    x = X(U, R, P, src)
    spec = u["sets"](x)
    sets = U.sets(spec)
    area = u["area"]
    for st in sets:
        st["title"] = us(st["title"])
        for it in st["items"]:
            for k in ("q", "e"):
                it[k] = us(re.sub(r"(?<=[\s(=])-(?=\d)", "−", caon_sci._quotes(it[k])))
            it["c"] = [us(re.sub(r"(?<=[\s(=])-(?=\d)", "−", caon_sci._quotes(c))) for c in it["c"]]
            assert len({c.strip().lower() for c in it["c"]}) == 4, it["c"]
    loc = _loc_text
    think = loc(u["think"])
    ex = [(loc(q), [loc(s) for s in st_], loc(a)) for q, st_, a in u["ex"]]
    mist = [loc(m) for m in u["mist"]]
    body = us(lesson(think, ex, mist))
    faq = [(us(loc(q)), us(loc(a))) for q, a in u["faq"]]
    for k in ("std", "kb", "ks", "short", "topic", "title"):
        u[k] = us(loc(re.sub(r"<sub>([^<]*)</sub>", r"\1", u[k])))
    if not u.get("what"):
        u["what"] = ", ".join(t[0].lower() + t[1:] for t, _ in spec[:4]) + " and " + spec[4][0][0].lower() + spec[4][0][1:]
    url = URL
    if grade <= 10:
        q = QUARTER[grade].index(area) + 1
        meta = us("Free Grade %d Science worksheets (MATATAG, Quarter %d: %s): %s. 100 questions with answers." % (grade, q, area, loc(u["what"])))
        seo = "Grade %d Science: %s Worksheets (MATATAG)" % (grade, u["title"])
        if len(seo) > 95:
            seo = "Grade %d Science: %s Worksheets" % (grade, u["title"])
        code = "Grade %d, Quarter %d: %s" % (grade, q, area)
        std = "%s (summary of the MATATAG Science curriculum, Grade %d, Quarter %d: %s)" % (u["std"], grade, q, area)
    else:
        course, q = u["course"], u["q"]
        per = "Term" if course == "General Science" else "Quarter"
        name = "Grade 11 General Science" if course == "General Science" else course
        meta = us("Free %s worksheets (Strengthened SHS curriculum, %s %d): %s. 100 questions with answers." % (name, per, q, loc(u["what"])))
        seo = "%s: %s Worksheets (Strengthened SHS)" % (name, u["title"])
        if len(seo) > 95:
            seo = "%s: %s Worksheets" % (name, u["title"])
        code = "%s, %s %d: %s" % (name, per, q, u["topic"])
        std = "%s (summary of the Strengthened Senior High School curriculum, %s, %s %d)" % (u["std"], course, per, q)
        url = URL_COURSE.get(course, URL_SHS)
    blob = json.dumps([u["title"], seo, u["short"], meta, u["kb"], u["ks"], body, faq, sets, std], ensure_ascii=False)
    bad = sorted(_bad_final(blob) - set(u["allow"]))
    if bad:
        low = blob.lower()
        raise AssertionError("Words that do not fit the Philippines: %s %s" % (bad, [low[max(0, low.find(w) - 100):low.find(w) + 40] for w in bad]))
    txt = re.sub(r"<[^>]+>", " ", blob)
    m = re.search("|".join(PH_DROP[:1]), txt)
    assert not m, "Word left: %s [%s]" % (m.group(0), txt[max(0, m.start() - 150):m.end() + 60])
    m = au_sci._NAME_RE.search(txt)
    assert not m, "Foreign name left: %s [%s]" % (m.group(1), txt[max(0, m.start() - 100):m.end() + 40])
    assert "\\" not in blob
    m = re.search(r"\b(colour|centre|metres?|litres?|behaviour|favour|aluminium|organis(e|ed|es|ing|ation)|recognis(e|ed|es|ing)|realis(e|ed|es|ing))\b", blob, re.I)
    assert not m, (m.group(0), blob[max(0, m.start() - 120):m.end() + 40])
    sci_common.make("grade-%d" % grade, slug, sort, code, std, u["title"], seo, u["short"], meta, u["kb"], u["ks"], body,
                    faq, sets, domain=area, country="ph", url=url)


def _loc_text(s):
    s = uk_sci.uk_text(s)
    s = au_sci._NAME_RE.sub(lambda m: (GIRLS if m.group(1) in _G else BOYS)[sum(map(ord, m.group(1))) % len(GIRLS if m.group(1) in _G else BOYS)], s)
    for a, b in PH_REP:
        s = re.sub(a, b, s)
    return s
