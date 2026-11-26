# -*- coding: utf-8 -*-
"""
UK science (National Curriculum in England, science programmes of study): subject `science`, grade `year-N`.
Builds on sci_common: British English (colour, metre, litre, centre, torch, Mum), UK names, and make_uk() that fills
in the standard fields: standard_code "Year 6: Light", domain = the programme of study heading ("Light"),
standard_url = the GOV.UK science programmes of study page.
make_uk() checks the whole unit for American spellings and words (LEAKS) before it writes.
"""
import json
import re
import sci_common
from sci_common import (Unit, item, bank, lesson, kid_lesson, table, pick, bar_chart, pie, arrow, sun, rect, circle,
                        svg_wrap, text, line, fig, figure, B, cap, GREEN, BLUE, RED, INK, FILL, GRAY, FONT,
                        ORANGE, BROWN, SKY, SUN, LEAF)
from uk_ks3 import People, GIRLS, BOYS

STD_URL = "https://www.gov.uk/government/publications/national-curriculum-in-england-science-programmes-of-study"
STD_URL_KS4 = "https://www.gov.uk/government/publications/national-curriculum-in-england-science-programmes-of-study"

# American spellings and words that must not appear (whole words, case-insensitive)
LEAKS = ["color", "colors", "colored", "colorful", "center", "centers", "meter", "meters", "centimeter", "centimeters",
         "millimeter", "millimeters", "kilometer", "kilometers", "liter", "liters", "milliliter", "milliliters",
         "behavior", "behaviors", "gray", "aluminum", "favorite", "flashlight", "flashlights", "mom", "math", "fiber",
         "fibers", "grade", "grades", "gasoline", "faucet", "sidewalk", "candy", "cookie", "cookies",
         "vacation", "soccer", "neighbor", "neighbors", "neighborhood", "mold", "molds", "odor", "vapor", "harbor",
         "tire", "tires", "diaper", "diapers", "fries", "zucchini", "eggplant", "cilantro", "flashcard", "recess",
         "fahrenheit", "ladybug", "ladybugs", "inch", "inches", "pound", "pounds", "ounce", "ounces", "gallon", "gallons", "mile", "miles"]
LEAK_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(w) for w in LEAKS), re.I)


def _text_of(unit_json):
    t = re.sub(r"<[^>]+>", " ", unit_json)
    return re.sub(r"(newton|level|sound|light|gas|electricity|parking|water|data) meters?|forcemeters?", " ", t, flags=re.I)    # meter = measuring instrument (correct in British English)


def make_uk(year, slug, sort, topic, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets,
            code=None, domain=None, allow=()):
    """year: 1..6 (KS1-KS2) or 7..9 (KS3); topic: the programme of study heading ("Light")."""
    grade = "year-%d" % year
    code = code or "Year %d: %s" % (year, topic)
    blob = json.dumps([title, seo_title, short, meta, key_big, key_sub, body, faq, sets, std_text], ensure_ascii=False)
    bad = sorted({m.group(1).lower() for m in LEAK_RE.finditer(_text_of(blob))} - set(allow))
    assert not bad, "American words: %s" % bad
    sci_common.make(grade, slug, sort, code, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets,
                    domain=domain or topic, country="uk", url=STD_URL)


USED = {}


def once(key, n=1):
    USED[key] = USED.get(key, 0) + 1
    return USED[key] <= n


def make_ks3(year, slug, sort, subject, topic, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets, allow=()):
    """KS3 (Year 7-9): subject = Biology / Chemistry / Physics; standard_code 'KS3 Biology: Cells and organisation'."""
    make_uk(year, slug, sort, topic, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets,
            code="KS3 %s: %s" % (subject, topic), domain=subject, allow=allow)


# ---- reuse US (NGSS) makers in British English ----
UKSP = [("colors", "colours"), ("colored", "coloured"), ("colorful", "colourful"), ("color", "colour"), ("centers", "centres"), ("center", "centre"),
        ("kilometers", "kilometres"), ("kilometer", "kilometre"), ("centimeters", "centimetres"), ("centimeter", "centimetre"),
        ("millimeters", "millimetres"), ("millimeter", "millimetre"), ("meters", "metres"), ("meter", "metre"),
        ("milliliters", "millilitres"), ("milliliter", "millilitre"), ("liters", "litres"), ("liter", "litre"),
        ("behaviors", "behaviours"), ("behavior", "behaviour"), ("gray", "grey"), ("aluminum", "aluminium"), ("favorite", "favourite"),
        ("flashlights", "torches"), ("flashlight", "torch"), ("fibers", "fibres"), ("fiber", "fibre"), ("molds", "moulds"), ("mold", "mould"),
        ("odor", "odour"), ("vapor", "vapour"), ("gasoline", "petrol"), ("soccer", "football"), ("neighborhood", "neighbourhood"),
        ("neighbors", "neighbours"), ("neighbor", "neighbour"), ("tires", "tyres"), ("tire", "tyre"), ("cookies", "biscuits"), ("cookie", "biscuit"),
        ("candy", "sweets"), ("ladybugs", "ladybirds"), ("ladybug", "ladybird"), ("Mom", "Mum"), ("mom", "mum"),
        ("analyze", "analyse"), ("analyzing", "analysing"), ("organize", "organise"), ("organized", "organised"), ("recognize", "recognise"),
        ("sulfur", "sulfur"), ("specialized", "specialised"), ("modeling", "modelling"), ("labeled", "labelled"), ("labeling", "labelling"),
        ("defense", "defence"), ("hemoglobin", "haemoglobin"), ("esophagus", "oesophagus"), ("fetus", "fetus"), ("anemia", "anaemia"),
        ("network covalent solid", "giant covalent structure"), ("molecular solid", "simple molecular substance"), ("ionic solid", "giant ionic lattice"), ("metallic solid", "metal"), ("London dispersion forces", "intermolecular forces"), ("London forces", "intermolecular forces"), ("average atomic mass", "relative atomic mass"), ("organizations", "organisations"), ("organization", "organisation"), ("Organization", "Organisation"), ("mol/L", "mol/dm³"), ("Tylenol", "paracetamol"), ("fiberglass", "fibreglass"), ("Fiberglass", "Fibreglass"), ("net force", "resultant force"), ("Net force", "Resultant force"), ("polyethylene", "polythene"), ("ethylene", "ethene"), ("polypropylene", "polypropene"), ("propylene", "propene"), ("sleds", "sledges"), ("sled", "sledge"), ("power plants", "power stations"), ("power plant", "power station"), ("fertilizers", "fertilisers"), ("fertilizer", "fertiliser"), ("trash", "rubbish"), ("parking lots", "car parks"), ("parking lot", "car park"), ("biking", "cycling"), ("single replacement reaction", "displacement reaction"), ("single replacement", "displacement"), ("cesium", "caesium"), ("Cesium", "Caesium"), ("nonmetals", "non-metals"), ("nonmetal", "non-metal"), ("Nonmetals", "Non-metals"), ("Nonmetal", "Non-metal"), ("activity series", "reactivity series"), ("Activity series", "Reactivity series"), ("Cellular respiration", "Respiration"), ("cellular respiration", "respiration"), ("use the bathroom", "go to the toilet"), ("bathroom", "toilet"), ("Grade 8", "Year 9"), ("Grade 7", "Year 8"), ("Grade 6", "Year 7"), ("students", "pupils"), ("Students", "Pupils")]
_UKSP = [(re.compile(r"(?<!\w)%s(?!\w)" % re.escape(a)), b) for a, b in UKSP]


def uk_text(s):
    parts = re.split(r"(<[^>]+>)", s)
    out = []
    for p in parts:
        if not p.startswith("<"):
            for rx, b in _UKSP:
                p = rx.sub(b, p)
        out.append(p)
    t = "".join(out)
    t = re.sub(r"(?<![\d,.])1 units\b", "1 unit", t)
    t = re.sub(r"\b(What mass of [^?]{1,40}?) are needed", r"\1 is needed", t)
    t = re.sub(r"\b([Aa]) (8|11|18|80|800|8,000)(?=[\s.,])", lambda m: m.group(1) + "n " + m.group(2), t)
    t = re.sub(r"\b(T|t)he ([a-z]+[^s\W]s) population\b", lambda m: m.group(1) + "he number of " + m.group(2), t)
    return t


def ukm(f):
    """wrap a (US) maker: British spellings; drop the item if an American word or unit is still there"""
    def g():
        it = f()
        if it is None:
            return None
        it = dict(it)
        it["q"] = uk_text(it["q"])
        it["e"] = uk_text(it["e"])
        it["c"] = [uk_text(c) for c in it["c"]]
        if LEAK_RE.search(_text_of(json.dumps(it, ensure_ascii=False))) or re.search(r"°F|\bft\b|\blb\b|\boz\b", it["q"] + " ".join(it["c"])):
            return None
        if len({c.strip().lower() for c in it["c"]}) < 4:
            return None
        names = "|".join(GIRLS + BOYS + list(getattr(sci_common, "GIRLS", [])) + list(getattr(sci_common, "BOYS", [])))
        norm = re.sub(r"<(table|svg|figure)\b.*?</\1>", " ", it["q"], flags=re.S)
        norm = re.sub(r"\d+(\.\d+)?", "#", re.sub(r"\b(%s)\b('s)?" % names, "N", re.sub(r"<[^>]+>", " ", norm)))
        if not once(("ukq", norm, it["c"][0])):
            return None
        return it
    g.__name__ = getattr(f, "__name__", "g")
    return g


def adopt_us(modname, U):
    """import a US science generator and point it at this unit (UK names)"""
    import importlib
    m = importlib.import_module(modname)
    m.U = U
    m.R = U.R
    m.P = People(U.R)
    return m


def make_ks4(year, slug, sort, subject, topic, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets, allow=()):
    """KS4 (Year 10-11, GCSE Combined Science): standard_code 'KS4 Chemistry: Atomic structure and the Periodic Table'."""
    make_uk(year, slug, sort, topic, std_text, title, seo_title, short, meta, key_big, key_sub, body, faq, sets,
            code="KS4 %s: %s" % (subject, topic), domain=subject, allow=allow)
