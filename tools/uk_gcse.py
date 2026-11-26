# -*- coding: utf-8 -*-
"""
UK Key Stage 4 maths (Year 10 and 11, GCSE Mathematics) helpers.
port(modname, seed, year, slug, sort, strand, std_text, title, short, meta_topic) runs another country's generator
(Singapore Secondary or US high school) with a new seed and UK names, money (£) and number style, captures the unit
it builds, turns the text into British GCSE wording (ukify) and writes content/uk/maths/year-N/{slug}.json.
Items that still mention Singapore, GST, dollars, feet, miles and so on stop the build (check LEAKS) so they can be fixed.
make_gcse() writes a hand-made unit with the same fields.
"""
import importlib
import random
import re
import ws_common
from ws_common import write_unit, balance
import uk_ks3

UPDATED = "2026-11-26"
STD_URL = "https://www.gov.uk/government/publications/gcse-mathematics-subject-content-and-assessment-objectives"
STRANDS = {"N": "KS4: Number", "A": "KS4: Algebra", "R": "KS4: Ratio, proportion and rates of change", "G": "KS4: Geometry and measures",
           "P": "KS4: Probability", "S": "KS4: Statistics"}
DOMAINS = uk_ks3.DOMAINS
UK_PLACES = ["Leeds", "Bristol", "York", "Cardiff", "Oxford", "Brighton", "Norwich", "Bath"]


def comma(n):
    return "{:,}".format(int(n))


def _sg_lists():
    import sg_sec
    return sg_sec.GIRLS, sg_sec.BOYS, sg_sec.PLACES


WORDS = [("Secondary 1", "Year 7"), ("Secondary 2", "Year 8"), ("Secondary 3", "Year 10"), ("Secondary 4", "Year 11"), ("Sec 1", "Year 7"), ("Sec 2", "Year 8"),
         ("Sec 3", "Year 10"), ("Sec 4", "Year 11"), ("O-Level", "GCSE"), ("O-level", "GCSE"), ("the MOE syllabus", "the GCSE specification"), ("MOE syllabus", "GCSE specification"),
         ("students", "pupils"), ("Students", "Pupils"), ("Grade 9", "Year 10"), ("Grade 10", "Year 10"), ("Grade 11", "Year 11"), ("Algebra 1", "GCSE"), ("Algebra 2", "GCSE"),
         ("cents", "pence"), ("dollars", "pounds"), ("dollar", "pound"), ("Rationalize", "Rationalise"), ("rationalize", "rationalise"), ("rationalizing", "rationalising")]
LEAKS = re.compile(r"Singapore|\bMRT\b|\bHDB\b|hawker|\bGST\b|\bS\$|\$|\d\s?(?:feet|foot|ft)\b|\binch|\bmiles?\b|\bmph\b|\d\s?°F\b|\bgallons?\b|\bpounds? \(lb\)|\blb\b|\bounces?\b|\bU\.S\.|\bAmerica|\bring?git\b|¢")


def _group(t):
    """UK number style outside tags: 10 000 / 10\u00a0000 -> 10,000 and 4536 -> 4,536 (years 1800-2100 kept unless money)."""
    parts = re.split(r"(<[^>]+>)", t)
    out = []
    for p in parts:
        if not p.startswith("<"):
            p = re.sub(r"(?<![\d.,])(\d{1,3})((?:[\u00a0\u202f]\d{3})+|(?: 000)+)(?!\d)", lambda m: m.group(1) + re.sub(r"[\u00a0\u202f ]", ",", m.group(2)), p)
            p = re.sub(r"(£?)(?<![\d.,])(\d)(\d{3})(?![\d,])", lambda m: m.group(0) if (not m.group(1) and 1800 <= int(m.group(2) + m.group(3)) <= 2100) else m.group(1) + m.group(2) + "," + m.group(3), p)
        out.append(p)
    return "".join(out)


def ukify(s, names, rep=(), sg=False):
    from uk_sci import uk_text
    if not isinstance(s, str):
        return s
    for a, b in rep:
        s = s.replace(a, b)
    s = re.sub(r"\$(?=\s?[\d−-]|<i>)", "£", s)
    s = re.sub(r"(\d{1,3})((?:[   ]\d{3})+)(?![\d])", lambda m: m.group(1) + m.group(2).replace(" ", ",").replace(" ", ",").replace(" ", ","), s) if " " in s or " " in s else s
    for a, b in WORDS:
        s = re.sub(r"(?<!\w)%s(?!\w)" % re.escape(a), b, s)
    for a, b in names:
        s = re.sub(r"(?<![\w-])%s(?![\w-])" % re.escape(a), b, s)
    return uk_text(s)


def adopt(mod, rnd, seen=None):
    """Point a generator module (and the gen_* modules it imported) at UK names, £ and UK number style."""
    seen = seen if seen is not None else set()
    if id(mod) in seen:
        return mod
    seen.add(id(mod))
    for name in ("gbp", "aud", "usd", "cad", "sgd", "money"):
        if hasattr(mod, name) and callable(getattr(mod, name)) and name != "money":
            setattr(mod, name, uk_ks3.gbp)
    if hasattr(mod, "comma"):
        mod.comma = comma
    if hasattr(mod, "People") and isinstance(getattr(mod, "People"), type):
        mod.People = uk_ks3.People
    if hasattr(mod, "P") and hasattr(getattr(mod, "P"), "next"):
        mod.P = uk_ks3.People(rnd)
    for name in ("PLACES", "CITIES", "TOWNS"):
        if hasattr(mod, name) and isinstance(getattr(mod, name), list) and all(isinstance(x, str) for x in getattr(mod, name)):
            setattr(mod, name, list(UK_PLACES))
    for name in ("GIRLS", "BOYS"):
        if hasattr(mod, name):
            setattr(mod, name, list(uk_ks3.GIRLS if name == "GIRLS" else uk_ks3.BOYS))
    for v in list(vars(mod).values()):
        if hasattr(v, "__name__") and getattr(v, "__name__", "").startswith("gen_") and hasattr(v, "__file__"):
            adopt(v, rnd, seen)
    return mod


def _names():
    import sg_sec
    import ws_common as wc
    pairs = list(zip(sg_sec.GIRLS, uk_ks3.GIRLS)) + list(zip(sg_sec.BOYS, uk_ks3.BOYS)) + list(zip(sg_sec.PLACES, UK_PLACES))
    pairs += list(zip(wc.GIRLS, uk_ks3.GIRLS)) + list(zip(wc.BOYS, uk_ks3.BOYS))
    try:
        import us_hs
        pairs += list(zip(getattr(us_hs, "GIRLS", []), uk_ks3.GIRLS)) + list(zip(getattr(us_hs, "BOYS", []), uk_ks3.BOYS))
    except ImportError:
        pass
    seen, out = set(), []
    for a, b in sorted(pairs, key=lambda p: -len(p[0])):
        if a not in seen and a != b and a not in uk_ks3.GIRLS + uk_ks3.BOYS:
            seen.add(a)
            out.append((a, b))
    return out


def _seo(year, short):
    small = {"and", "of", "in", "the", "a", "to", "or"}
    t = " ".join(w if (i and w in small) else w[0].upper() + w[1:] for i, w in enumerate(short.split()))
    return "Year %d Maths: %s Worksheets (GCSE)" % (year, t)


def make_gcse(year, slug, sort, strand, title, short, std_text, meta, key_big, key_sub, body, faq, sets, rnd, seo=None):
    for s in sets:
        assert len(s["items"]) == 20, s["title"]
    assert len(sets) == 5
    balance(sets, rnd)
    for s in sets:
        for it in s["items"]:
            t = re.sub(r"<svg\b.*?</svg>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"], flags=re.S)
            assert not LEAKS.search(re.sub(r"<[^>]+>", " ", t)), (slug, LEAKS.search(re.sub(r"<[^>]+>", " ", t)).group(0), it["q"][:200])
            assert len(set(it["c"])) == 4, it
    for t in [body, key_big, key_sub, meta] + [x for f in faq for x in f]:
        m = LEAKS.search(re.sub(r"<svg\b.*?</svg>|<[^>]+>", " ", t)) or re.search(r"Common Core|CCSS|\bGrade \d|Algebra [12]|\b[A-Z]-[A-Z]{2,3}\.[A-Z]\.\d", t)
        assert not m, (slug, m.group(0), t[:200])
    unit = {
        "slug": slug, "title": title, "seo_title": seo or _seo(year, short), "short_title": short,
        "domain": DOMAINS[strand], "standard_code": STRANDS[strand], "standard_url": STD_URL,
        "standard_text": std_text, "meta_desc": meta, "key_big": key_big, "key_sub": key_sub,
        "body_html": body, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets,
        "pdf_url": "", "sort": sort, "updated": UPDATED,
    }
    write_unit("uk", "maths", "year-%d" % year, unit)


def port(modname, seed, year, slug, sort, strand, std_text, title, short, meta=None, fix=None, set_titles=None, rep=(), swap=None, body=None, faq=None, kb=None, ks=None):
    """Run another generator's build() with UK settings and write it as a UK GCSE unit."""
    mod = importlib.import_module(modname)
    ws_common.comma = comma
    R = random.Random(seed)
    mod.R = R
    adopt(mod, R)
    got = {}

    def capture(*a, **k):
        a = list(a)
        i = next(j for j, x in enumerate(a) if isinstance(x, list) and x and isinstance(x[0], dict) and "items" in x[0])
        got.update(meta=a[i - 5], kb=a[i - 4], ks=a[i - 3], body=a[i - 2], faq=a[i - 1], sets=a[i])
    mod.make = capture
    for k, f in (swap or {}).items():
        setattr(mod, k, f)
    (getattr(mod, "build", None) or getattr(mod, "main"))()
    names = _names()
    u = lambda s: ukify(s, names, rep, modname.startswith("gen_sg_"))
    sets = got["sets"]
    for n, s in enumerate(sets):
        s["title"] = u(set_titles[n]) if set_titles else u(s["title"])
        for it in s["items"]:
            it["q"], it["e"] = u(it["q"]), u(it["e"])
            it["c"] = [u(c) for c in it["c"]]
            if fix:
                fix(it)
    if body is not None:
        got["body"] = body
    if faq is not None:
        got["faq"] = faq
    if kb is not None:
        got["kb"] = kb
    if ks is not None:
        got["ks"] = ks
    faq = [(u(q), u(a)) for q, a in got["faq"]]
    m = meta or re.sub(r"^Free [^:]*?(worksheets|practice)", "Free Year %d GCSE maths worksheets" % year, u(got["meta"]))
    make_gcse(year, slug, sort, strand, title, short, std_text, m, u(got["kb"]), u(got["ks"]), u(got["body"]), faq, sets, R)
