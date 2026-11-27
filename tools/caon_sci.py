# -*- coding: utf-8 -*-
"""
Ontario science (The Ontario Curriculum, Grades 1-8: Science and Technology, 2022): country `ca-on`, subject `science`, grade `grade-N`.
Each grade has four strands with one topic each (B Life Systems, C Matter and Energy, D Structures and Mechanisms,
E Earth and Space Systems); strand A (STEM Skills and Connections) is used inside the units.
  CU(strand, sort, slug, code, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, pic=None, allow=())
      strand = "B" ... "E"; code = "B2.3" style expectation numbers of that strand; sets = lambda X: [(title, [(maker, n)]) x 5]
      pic (Grades 1-2): a picture for kid_lesson, think is then (lead, [points])
  X (in sets): X.R, X.P
      X.gen(module, name, rep=, drop=, n=)  a maker from any gen_ science generator (US, UK, SG, IN, AU); n = at most n in the unit
      X.B(module, name)                     a bank list of another generator as one maker
      X.pool(rows) / X.rows(table, fwd, back) / X.w(maker) / X.f(factory)
  Everything goes through cam(): British spelling first (uk_sci.ukm), then Canadian English (colour, centre, metre, litre,
  but -ize, aluminum, tire, truck, gas, flashlight, Mom, candy, cookies, garbage, sidewalk, washroom) and Canadian names.
  Items with words that do not fit Ontario (pence, Year N, Australian animals, southern seasons, inches) are dropped, and a
  question (names and numbers removed) with the same answer is used once per unit.
build(grade, slug): seed 67000 + 100 * grade + sort.  Numbers: 4536, 10 000 (sgnum).  g = 9.8 N/kg.
"""
import copy
import json
import re
import importlib
import random as _random
import au_sci
import uk_sci
import sci_common
from sci_common import item, lesson, kid_lesson, Unit
from au_sci import _Src, sgnum, _fixnums, limit, keep, rows, nq, tq

STD_URL = "https://www.dcp.edu.gov.on.ca/en/curriculum/science-technology/grades/grade-%d/strands"
STRANDS = {"A": "STEM Skills and Connections", "B": "Life Systems", "C": "Matter and Energy", "D": "Structures and Mechanisms",
           "E": "Earth and Space Systems"}
TOPICS = {
    1: {"B": "Needs and Characteristics of Living Things", "C": "Energy in Our Lives", "D": "Materials, Objects, and Everyday Structures",
        "E": "Daily and Seasonal Changes"},
    2: {"B": "Growth and Changes in Animals", "C": "Properties of Liquids and Solids", "D": "Simple Machines and Movement",
        "E": "Air and Water in the Environment"},
    3: {"B": "Growth and Changes in Plants", "C": "Forces Causing Movement", "D": "Strong and Stable Structures", "E": "Soils in the Environment"},
    4: {"B": "Habitats and Communities", "C": "Light and Sound", "D": "Machines and Mechanisms", "E": "Rocks, Minerals, and Erosion"},
    5: {"B": "Human Organ Systems", "C": "Properties of and Changes in Matter", "D": "Forces Acting on Structures",
        "E": "Conservation of Energy and Resources"},
    6: {"B": "Biodiversity", "C": "Electrical Phenomena", "D": "Flight", "E": "Space"},
    7: {"B": "Interactions in the Environment", "C": "Pure Substances and Mixtures", "D": "Form and Function", "E": "Heat in the Environment"},
    8: {"B": "Cells", "C": "Fluids", "D": "Systems in Action", "E": "Water Systems"},
}
GIRLS = ["Olivia", "Emma", "Maya", "Zoe", "Amira", "Mei", "Chloe", "Priya", "Leah", "Hana", "Ava", "Sofia"]
BOYS = ["Liam", "Noah", "Aiden", "Lucas", "Owen", "Arjun", "Ethan", "Jayden", "Benjamin", "Mateo", "Nathan", "Kai"]


class People:
    def __init__(self, R):
        self.R = R
        self.pool = [(n, "she", "her") for n in GIRLS] + [(n, "he", "his") for n in BOYS]

    def next(self):
        return self.R.choice(self.pool)


# ---- words ----
CA_REP = [
    (r"\b([Oo]rgan|[Rr]ecogn|[Rr]eal|[Ss]pecial|[Mm]inim|[Mm]axim|[Cc]rystall|[Vv]apor|[Mm]agnet|[Ff]ertil|[Ii]on|[Ss]teril|[Nn]eutral|[Cc]ategor|[Ss]ummar|[Mm]emor|[Vv]isual|[Ss]tabil|[Uu]til|[Ee]mphas|[Hh]armon|[Cc]olon|[Oo]ptim|[Pp]rior|[Ss]tandard|[Cc]ivil|[Pp]olar|[Ss]ympath|[Aa]polog|[Cc]haracter|[Oo]xid|[Hh]ypothes|[Ss]ynthes)is(e|es|ed|ing|ation|ations|er|ers)\b", r"\1iz\2"),
    (r"\bvapouris", "vaporiz"), (r"\b([Aa])nalys(e|ed|es|ing)\b", r"\1nalyz\2"), (r"\b([Pp])aralys(e|ed|es|ing)\b", r"\1aralyz\2"),
    (r"\baluminium\b", "aluminum"), (r"\bAluminium\b", "Aluminum"), (r"\bsulphur", "sulfur"), (r"\bSulphur", "Sulfur"), (r"\bcaesium\b", "cesium"),
    (r"\bhaemoglobin\b", "hemoglobin"), (r"\boesophagus\b", "esophagus"), (r"\bOesophagus\b", "Esophagus"), (r"\bfaeces\b", "feces"),
    (r"\bfoetus\b", "fetus"), (r"\boestrogen\b", "estrogen"), (r"\bOestrogen\b", "Estrogen"), (r"\banaemia\b", "anemia"), (r"\bhaem", "hem"),
    (r"\bmoulds\b", "molds"), (r"\bmould\b", "mold"), (r"\bMould\b", "Mold"), (r"\bmouldy\b", "moldy"),
    (r"\btyres\b", "tires"), (r"\btyre\b", "tire"), (r"\bTyres\b", "Tires"), (r"\bTyre\b", "Tire"), (r"\bkerbs?\b", "curb"), (r"\bprogrammes?\b", "program"),
    (r"\bmaths\b", "math"), (r"\bMaths\b", "Math"), (r"\bpupils\b", "students"), (r"\bPupils\b", "Students"), (r"\bpupil's\b", "student's"),
    (r"\bYear ([1-8])\b", "Grade \\1"), (r"\byear ([1-8]) (students|class)\b", "Grade \\1 \\2"),
    (r"\blorries\b", "trucks"), (r"\blorry\b", "truck"), (r"\bLorries\b", "Trucks"), (r"\bLorry\b", "Truck"),
    (r"\bpetrol\b", "gasoline"), (r"\bPetrol\b", "Gasoline"), (r"\btorches\b", "flashlights"), (r"\btorch\b", "flashlight"), (r"\bTorches\b", "Flashlights"), (r"\bTorch\b", "Flashlight"),
    (r"\bMum\b", "Mom"), (r"\bmum\b", "mom"), (r"\bMummy\b", "Mommy"), (r"\bsweets\b", "candy"), (r"\bsweet wrappers\b", "candy wrappers"), (r"\blollies\b", "candy"),
    (r"\bbiscuits\b", "cookies"), (r"\bbiscuit\b", "cookie"), (r"\bcrisps\b", "chips"), (r"\bfizzy drinks?\b", "pop"),
    (r"\brubbish\b", "garbage"), (r"\bRubbish\b", "Garbage"), (r"\blitter bins?\b", "garbage can"), (r"\bdustbins?\b", "garbage can"),
    (r"\bshopping trolleys\b", "shopping carts"), (r"\bshopping trolley\b", "shopping cart"), (r"\btrolleys\b", "carts"), (r"\btrolley\b", "cart"), (r"\bTrolleys\b", "Carts"), (r"\bTrolley\b", "Cart"),
    (r"\bsledges\b", "sleds"), (r"\bsledge\b", "sled"), (r"\bpower stations\b", "power plants"), (r"\bpower station\b", "power plant"),
    (r"\bcar parks\b", "parking lots"), (r"\bcar park\b", "parking lot"), (r"\bgo to the toilet\b", "go to the washroom"),
    (r"\bjumpers\b", "sweaters"), (r"\bjumper\b", "sweater"), (r"\bwellies\b", "rubber boots"), (r"\bwellington boots\b", "rubber boots"),
    (r"\bgumboots\b", "rubber boots"), (r"\bgumboot\b", "rubber boot"), (r"\bpavements\b", "sidewalks"), (r"\bpavement\b", "sidewalk"),
    (r"\bfootpaths\b", "sidewalks"), (r"\bfootpath\b", "sidewalk"), (r"\bladybirds\b", "ladybugs"), (r"\bladybird\b", "ladybug"),
    (r"\bLadybirds\b", "Ladybugs"), (r"\bLadybird\b", "Ladybug"), (r"\bwoodlice\b", "sow bugs"), (r"\bwoodlouse\b", "sow bug"),
    (r"\bslaters\b", "sow bugs"), (r"\bslater\b", "sow bug"), (r"\bWoodlice\b", "Sow bugs"), (r"\bSlaters\b", "Sow bugs"),
    (r"\bdraughts\b", "drafts"), (r"\bdraught\b", "draft"), (r"\bdraughty\b", "drafty"), (r"\baeroplanes\b", "airplanes"), (r"\baeroplane\b", "airplane"),
    (r"\bAeroplanes\b", "Airplanes"), (r"\bAeroplane\b", "Airplane"), (r"\b(a|the) lift\b", r"\1 elevator"),
    (r"\bfootball\b", "soccer"), (r"\bFootball\b", "Soccer"), (r"\bfooty\b", "soccer"),
    (r"\ba spring balance \(force meter\)", "a spring scale"), (r"\bspring balances\b", "spring scales"), (r"\bspring balance\b", "spring scale"),
    (r"\bnewton meters?\b", "spring scale"), (r"\bnewton metres?\b", "spring scale"), (r"\bforce meters?\b", "spring scale"), (r"\bforcemeters?\b", "spring scale"),
    (r"\bcolumn graphs\b", "bar graphs"), (r"\bcolumn graph\b", "bar graph"), (r"\bColumn graphs\b", "Bar graphs"), (r"\bColumn graph\b", "Bar graph"),
    (r"\bbar charts\b", "bar graphs"), (r"\bbar chart\b", "bar graph"), (r"\bBar chart\b", "Bar graph"),
    (r"\ban esky\b", "a cooler"), (r"\beskys?\b", "cooler"), (r"\bicy poles\b", "popsicles"), (r"\bicy pole\b", "popsicle"),
    (r"\bice lollies\b", "popsicles"), (r"\bice lolly\b", "popsicle"), (r"\bbitumen\b", "asphalt"), (r"\btarmac\b", "asphalt"),
    (r"\bin bushland\b", "in the forest"), (r"\bbushland\b", "forest"), (r"\bgum trees\b", "maple trees"), (r"\bgum tree\b", "maple tree"),
    (r"\ba maple tree\b", "a maple tree"), (r"\bbicarb soda\b", "baking soda"), (r"\bBicarb soda\b", "Baking soda"),
    (r"\bmobile phones\b", "cellphones"), (r"\bmobile phone\b", "cellphone"), (r"\bfortnight\b", "two weeks"), (r"\bholidays\b", "vacation"),
    (r"\bsecondary school\b", "high school"), (r"\bheadteacher\b", "principal"), (r"\bcling film\b", "plastic wrap"), (r"\bkitchen foil\b", "aluminum foil"),
    (r"\bwashing-up liquid\b", "dish soap"), (r"\bwashing up liquid\b", "dish soap"), (r"\bpolythene\b", "polyethylene"), (r"\bcotton wool\b", "cotton balls"),
    (r"\bresultant force\b", "net force"), (r"\bResultant force\b", "Net force"), (r"\bparacetamol\b", "acetaminophen"),
    (r"\bmol/dm³", "mol/L"), (r"\bmol dm⁻³", "mol/L"), (r"\bdm³", "L"), (r"\btrainers\b", "running shoes"), (r"\bpost box\b", "mailbox"), (r"\bletterbox\b", "mailbox"),
    (r"\bcooker\b", "stove"), (r"\bplaytime\b", "recess"), (r"\bfavour", "favour"), (r"\bautumn\b", "fall"), (r"\bAutumn\b", "Fall"),
    (r"\b(sound level|light|parking|water|gas|electricity|data|level|speed|power|pH|moisture|rain) metres?\b", r"\1 meter"),
    (r"\b([Aa]) pupil (drew|wrote|says|said|thinks|measured|made|was|is|has|wants|tested|noticed)\b", r"\1 student \2"), (r"\bdrawing pins\b", "thumbtacks"), (r"\bdrawing pin\b", "thumbtack"), (r"\bcaused by man\b", "caused by people"), (r"\bman-made\b", "human-made"), (r"(\d) ?ml\b", r"\1 mL"), (r"\bsg(pond|garden|reef)\b", r"\1"),
    (r"\bin the UK\b", "in Ontario"), (r"\bthe UK\b", "Ontario"), (r"\bin the U\.S\.(?=[\s,?])", "in Canada"), (r"\bin the United States\b", "in Canada"),
    (r"\bthe gullet\b", "the esophagus"), (r"\bgullet\b", "esophagus"), (r"\bGullet\b", "Esophagus"), (r"\bice candy\b", "popsicles"),
    (r"\blean mince\b", "lean ground beef"), (r"\bmince\b", "ground beef"), (r"\bcourgettes?\b", "zucchini"), (r"\baubergines?\b", "eggplant"),
    (r"\bminibeasts\b", "small creatures"), (r"\bMinibeasts\b", "Small creatures"), (r"\bminibeast\b", "small creature"),
    (r"\bpaving slabs?\b", "patio stone"), (r"\btin openers?\b", "can opener"), (r"\bfly-tipping\b", "illegal dumping"),
    (r"(?<=\d) ?am\b(?![-\w])", " a.m."), (r"(?<=\d) ?pm\b(?![-\w])", " p.m."), (r"\bhandphones?\b", "cellphone"), (r"\bpracticing\b", "practising"),
]
_CA_REP = [(re.compile(a), b) for a, b in CA_REP]

# words that must not appear on an Ontario page
LEAKS = [
    # US spellings (Canada writes colour, centre, metre, litre, grey, fibre ...)
    "color", "colors", "colored", "colorful", "center", "centers", "meter", "meters", "centimeter", "centimeters", "millimeter", "millimeters",
    "kilometer", "kilometers", "liter", "liters", "milliliter", "milliliters", "behavior", "behaviors", "gray", "favorite", "fiber", "fibers",
    "neighbor", "neighbors", "neighborhood", "odor", "harbor", "theater", "catalog",
    # British / Australian words
    "tyre", "tyres", "lorry", "lorries", "petrol", "mum", "aluminium", "sweets", "biscuit", "biscuits", "maths", "pupils", "rubbish",
    "trolley", "trolleys", "sledge", "jumper", "wellies", "pavement", "ladybird", "woodlouse", "woodlice", "slater", "slaters", "esky",
    "icy pole", "footpath", "bushland", "gum tree", "lollies", "aeroplane", "nappy", "pence", "penny", "year 1", "year 2", "year 3",
    "year 4", "year 5", "year 6", "year 7", "year 8", "year 9", "gcse", "ks1", "ks2", "ks3", "ks4", "a level", "o-level", "psle", "nhs",
    "conker", "conkers", "badger", "badgers", "hedgehog", "hedgehogs", "slow worm", "dormouse", "bonfire night", "sixth form",
    # Australian, British, Singapore, Indian and US things
    "koala", "koalas", "kangaroo", "kangaroos", "wombat", "wombats", "platypus", "echidna", "echidnas", "possum", "possums", "kookaburra",
    "kookaburras", "emu", "emus", "dingo", "dingoes", "wallaby", "wallabies", "galah", "galahs", "cockatoo", "cockatoos", "lorikeet",
    "lorikeets", "goanna", "goannas", "magpie", "magpies", "quokka", "numbat", "bilby", "cassowary", "billabong", "outback", "wattle",
    "eucalyptus", "great barrier reef", "uluru", "australia", "australian", "sydney", "melbourne", "brisbane", "perth", "adelaide",
    "queensland", "tasmania", "canberra", "britain", "england", "english channel", "scotland", "wales", "london",
    "manchester", "birmingham", "thames", "singapore", "hawker", "mrt", "durian", "pandan", "rain tree", "uk", "united kingdom", "u.s.", "sugar glider", "eatwell", "eatwell guide", "sunbird", "coral trout", "mangrove", "mangroves", "monitor lizard", "india", "delhi", "mumbai",
    "rupee", "rupees", "neem", "texas", "florida", "arizona", "california", "ngss", "cbse", "ncert", "wet season", "dry season",
    # units Ontario does not use
    "inch", "inches", "pound", "pounds", "ounce", "ounces", "gallon", "gallons", "mile", "miles", "fahrenheit", 
]
LEAK_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in LEAKS), re.I)
# southern-hemisphere seasons
SEASON_RE = re.compile(r"\b(December|January|February|Christmas)\b[^.?!]{0,60}\b(summer|hottest|heatwave)\b|\b(summer|hottest)\b[^.?!]{0,60}\b(December|January|February|Christmas)\b"
                       r"|\b(June|July|August)\b[^.?!]{0,60}\b(winter|snow\w*|freezing)\b|\b(winter|snow\w*)\b[^.?!]{0,60}\b(June|July|August)\b", re.I)
_EYE = re.compile(r"\b(eyes?|iris|retina|cornea|lens|optic)\b", re.I)


_INSTR = re.compile(r"\b(sound level|light|parking|water|gas|electricity|data|level|speed|power|pH|moisture|rain|volt|amp|multi|thermo|baro) ?meters?\b", re.I)


def _bad(text):
    t = _INSTR.sub("INSTRUMENT", uk_sci._text_of(text))
    bad = {m.group(1).lower() for m in LEAK_RE.finditer(t)}
    if "£" in t or "₹" in t:
        bad.add("£/₹")
    if SEASON_RE.search(t):
        bad.add("southern seasons")
    if re.search(r"°F|\bft\b|\blb\b|\boz\b|\d ?p\b(?![.\w])", t):
        bad.add("units")
    return bad


# names from other countries' generators -> Ontario names (same gender)
import ws_common as _ws  # noqa: E402
import sg_sec as _sg  # noqa: E402
import in_common as _in  # noqa: E402
import au_hs as _au  # noqa: E402
_G = set(uk_sci.GIRLS) | set(_ws.GIRLS) | set(_sg.GIRLS) | set(_in.GIRLS) | set(_au.GIRLS)
_Bo = set(uk_sci.BOYS) | set(_ws.BOYS) | set(_sg.BOYS) | set(_in.BOYS) | set(_au.BOYS)
FOREIGN = sorted((_G | _Bo) - set(GIRLS) - set(BOYS), key=len, reverse=True)
_NAME_RE = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in FOREIGN))
_ALLN = re.compile(r"\b(%s)\b('s)?" % "|".join(sorted(_G | _Bo | set(GIRLS) | set(BOYS), key=len, reverse=True)))
_NR = _random.Random(2025)


def ca_text(s, sub=None):
    parts = re.split(r"(<[^>]+>)", s)
    out = []
    for p in parts:
        if not p.startswith("<"):
            if sub is not None:
                def nm(m):
                    k = m.group(1)
                    if k not in sub:
                        pool = [n for n in (GIRLS if k in _G else BOYS) if n not in sub.values()]
                        sub[k] = _NR.choice(pool)
                    return sub[k]
                p = _NAME_RE.sub(nm, p)
            for rx, b in _CA_REP:
                p = rx.sub(b, p)
        out.append(p)
    t = au_sci._fix_an("".join(out))
    t = re.sub(r"\b([Aa])n (?=(uk|uni|use|usu|eu|ewe|one\b|once\b))", r"\1 ", t)
    return t.replace("a.m..", "a.m.").replace("p.m..", "p.m.")


SEEN = set()


def _seen_once(it):
    q = re.sub(r"<(table|svg|figure)\b.*?</\1>", " ", it["q"], flags=re.S)
    q = re.sub(r"\d+(\.\d+)?", "#", _ALLN.sub("N", re.sub(r"<[^>]+>", " ", q)))
    k = (" ".join(q.split()).lower(), it["c"][it["a"]].lower())
    if k in SEEN:
        return False
    SEEN.add(k)
    return True


def cam(f, rep=()):
    """wrap any maker: British spelling first, then Canadian English and names; None if a word does not fit"""
    g0 = uk_sci.ukm(f)
    rx = [(re.compile(a), b) for a, b in rep]

    def g():
        it = g0()
        if it is None:
            return None
        it = dict(it)
        sub = {}

        def fx(s):
            for a, b in rx:
                s = a.sub(b, s)
            return ca_text(s, sub)
        it["q"], it["e"] = fx(it["q"]), fx(it["e"])
        it["c"] = [fx(c) for c in it["c"]]
        if _bad(json.dumps(it, ensure_ascii=False)) or len({c.strip().lower() for c in it["c"]}) < 4:
            return None
        if not _seen_once(it):
            return None
        return it
    g.__name__ = getattr(f, "__name__", "g")
    return g


class _CSrc(_Src):
    def wrap(self, f, rep=(), drop=()):
        g0 = cam(f, rep)
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


def CU(strand, sort, slug, code, std, title, short, meta, kb, ks, think, ex, mist, faq, sets, pic=None, allow=()):
    assert strand in STRANDS
    return dict(strand=strand, sort=sort, slug=slug, code=code, std=std, title=title, short=short, meta=meta, kb=kb, ks=ks,
                think=think, ex=ex, mist=mist, faq=faq, sets=sets, pic=pic, allow=tuple(allow))


class X:
    def __init__(self, U, R, P, src):
        self.U, self.R, self.P, self.src = U, R, P, src

    def gen(self, mod, name, rep=(), drop=(), n=None):
        f = self.src(mod, name, rep, drop)
        return limit(f, n) if n else f

    def B(self, mod, name, rep=(), drop=(), n=None):
        if callable(getattr(self.src.mod(mod), name)):
            return self.gen(mod, name, rep, drop, n)
        g = self.src.B(mod, name, rep, drop)
        return limit(g, n) if n else g

    def mod(self, name):
        return self.src.mod(name)

    def w(self, f, rep=(), drop=(), n=None):
        g = self.src.wrap(f, rep, drop)
        return limit(g, n) if n else g

    def f(self, factory, rep=(), drop=(), n=None, raw=True):
        """an own maker made by factory(R); raw: no 'same question with other numbers' filter (numbers are the point)"""
        if raw:
            g = factory(self.R)
            return limit(g, n) if n else g
        return self.w(factory(self.R), rep, drop, n)

    def pool(self, rs):
        return self.w(au_sci.pool(self.R, rs))

    def rows(self, rs, fwd, back=None, extra=()):
        return self.w(rows(self.R, rs, fwd, back, extra))


def _quotes(t):
    """straight double quotes in text -> curly quotes (attributes use single quotes)"""
    return re.sub(r"(^|>)([^<]*)", lambda m: m.group(1) + re.sub(r'"([^"]*)"', "\u201c\\1\u201d", m.group(2)).replace('"', "\u201d"), t)


def seed_of(grade, sort):
    return 67000 + 100 * grade + sort


def build(mod, grade, slug):
    u = next(x for x in mod.UNITS() if x["slug"] == slug)
    sort = u["sort"]
    U = Unit(seed_of(grade, sort))
    R = U.R
    P = People(R)
    uk_sci.USED.clear()
    SEEN.clear()
    src = _CSrc(U, P)
    allow = set(u["allow"])
    x = X(U, R, P, src)
    sets = U.sets(u["sets"](x))
    for st in sets:
        for it in st["items"]:
            it["q"], it["e"], it["c"] = _quotes(ca_text(it["q"])), _quotes(ca_text(it["e"])), [_quotes(ca_text(c)) for c in it["c"]]
            it["q"], it["e"] = re.sub(r"(?<=[\s(=])-(?=\d)", "−", it["q"]), re.sub(r"(?<=[\s(=])-(?=\d)", "−", it["e"])
            assert len({c.strip().lower() for c in it["c"]}) == 4, it["c"]
    sets = _fixnums(sets)
    if u["pic"] is not None:
        lead, points = u["think"]
        body = kid_lesson(u["pic"], lead, points, u["ex"], u["mist"])
    else:
        body = lesson(u["think"], u["ex"], u["mist"])
    body = sgnum(body)
    strand = STRANDS[u["strand"]]
    topic = TOPICS[grade][u["strand"]]
    seo = "Grade %d Science: %s Worksheets (Ontario Curriculum)" % (grade, u["title"])
    if len(seo) > 95:
        seo = "Grade %d Science: %s Worksheets" % (grade, u["title"])
    code = "Grade %d: %s" % (grade, u["code"])
    std = "%s (summary of the Ontario Science and Technology curriculum, 2022, Strand %s: %s – %s)" % (u["std"], u["strand"], strand, topic)
    blob = json.dumps([u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body, u["faq"], sets, std], ensure_ascii=False)
    bad = sorted(_bad(blob) - allow)
    assert not bad, "Words that do not fit Ontario: %s" % bad
    m = _NAME_RE.search(re.sub(r"<[^>]+>", " ", blob))
    assert not m, "Foreign name left: %s" % m.group(1)
    assert "\\" not in blob, blob[max(0, blob.index("\\") - 120):blob.index("\\") + 40]
    sci_common.make("grade-%d" % grade, slug, sort, code, std, u["title"], seo, u["short"], u["meta"], u["kb"], u["ks"], body,
                    [(q, a) for q, a in u["faq"]], sets, domain=strand, country="ca-on", url=STD_URL % grade)


def main(mod, grade, slug):
    build(importlib.import_module(mod), grade, slug)
