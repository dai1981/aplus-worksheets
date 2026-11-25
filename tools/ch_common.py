# -*- coding: utf-8 -*-
"""
Schweiz (Deutschschweiz, Lehrplan 21) の共通部品。
・多くの単元は Deutschland の生成スクリプト（gen_de_mathe_*）を新しい seed で動かし、出てきた文をスイス式に直す（ch_text）
・スイス式: ß → ss、数は 1’000・10’000（アポストロフィ、4 けたから）、小数は点（2.5）、掛け算は ×（3 × 4）、割り算は :
・お金: 3.50 Fr.、45 Rp.（5 Rp. 未満の端数はない。端数のある問題は落とす）
・スイスの名前・地名・語（Velo, Brötli, Primarschule, Schulthek …）
・standard_code は Lehrplan 21 のコード（例: MA.1.A.2）、domain は Kompetenzbereich
"""
import importlib
import random
import re
import de_common as D
from ws_common import write_unit, balance, text, fig, svg_wrap, INK

UPDATED = "2026-11-25"
STD_URL = "https://sg.lehrplan.ch/container/SG_DE_Fachbereich_MA.pdf"
DOMAIN = {"Z": "Zahl und Variable", "F": "Form und Raum", "G": "Grössen, Funktionen, Daten und Zufall"}
KOMP = {
    "MA.1.A.1": "verstehen und verwenden arithmetische Begriffe und Symbole; sie lesen und schreiben Zahlen",
    "MA.1.A.2": "können flexibel zählen, Zahlen nach der Grösse ordnen und Ergebnisse überschlagen",
    "MA.1.A.3": "können addieren, subtrahieren, multiplizieren, dividieren und potenzieren",
    "MA.1.A.4": "können Terme vergleichen und umformen, Gleichungen lösen, Gesetze und Regeln anwenden",
    "MA.1.B.1": "können Zahl- und Operationsbeziehungen sowie arithmetische Muster erforschen und Erkenntnisse austauschen",
    "MA.1.B.2": "können Aussagen, Vermutungen und Ergebnisse zu Zahlen und Variablen überprüfen und begründen",
    "MA.1.C.1": "können Rechenwege darstellen, beschreiben, austauschen und nachvollziehen",
    "MA.1.C.2": "können Anzahlen, Zahlenfolgen und Terme veranschaulichen, beschreiben und verallgemeinern",
    "MA.2.A.1": "verstehen und verwenden geometrische Begriffe und Symbole",
    "MA.2.A.2": "können Figuren und Körper abbilden, zerlegen und zusammensetzen",
    "MA.2.A.3": "können Längen, Flächen und Volumen bestimmen und berechnen",
    "MA.2.B.1": "können geometrische Beziehungen erforschen, Vermutungen formulieren und Erkenntnisse austauschen",
    "MA.2.C.1": "können Körper und räumliche Beziehungen darstellen",
    "MA.2.C.2": "können Figuren falten, skizzieren, zeichnen und konstruieren",
    "MA.2.C.3": "können sich Figuren und Körper in verschiedenen Lagen vorstellen und Veränderungen beschreiben",
    "MA.2.C.4": "können Koordinaten von Figuren und Körpern bestimmen bzw. darstellen sowie Pläne lesen und zeichnen",
    "MA.3.A.1": "verstehen und verwenden Begriffe und Symbole zu Grössen, Funktionen, Daten und Zufall",
    "MA.3.A.2": "können Grössen schätzen, messen, umwandeln, runden und mit ihnen rechnen",
    "MA.3.A.3": "können funktionale Zusammenhänge beschreiben und Funktionswerte bestimmen",
    "MA.3.B.2": "können Sachsituationen zur Statistik, Kombinatorik und Wahrscheinlichkeit erforschen, Vermutungen formulieren und überprüfen",
    "MA.3.C.1": "können Daten zu Statistik, Kombinatorik und Wahrscheinlichkeit erheben, ordnen, darstellen, auswerten und interpretieren",
    "MA.3.C.2": "können Sachsituationen mathematisieren, darstellen, berechnen sowie Ergebnisse interpretieren und überprüfen",
    "MA.3.C.3": "können Terme, Formeln, Gleichungen und Tabellen mit Sachsituationen konkretisieren",
}
NB = " "
AP = "’"
DEBUG = []

# スイスの名前（Kids が使う。性別はそろえる）
D.GIRLS[:] = ["Mia", "Emma", "Lina", "Elena", "Lea", "Laura", "Lara", "Nina", "Alina", "Leonie", "Malea", "Ayla", "Seraina", "Ronja"]
D.BOYS[:] = ["Noah", "Liam", "Matteo", "Luca", "Gabriel", "Levin", "Leon", "Nico", "Jan", "Gian", "Samuel", "Tim", "Arian", "Julian"]

WORDS = [
    (r"\bGrundschule", "Primarschule"), (r"\bGrundschüler", "Primarschüler"), (r"\bBrötchen\b", "Brötli"),
    (r"\bFahrrads?\b", "Velo"), (r"\bFahrräder(n)?\b", "Velos"), (r"\bFahrrad", "Velo"),
    (r"\bSchulranzen\b", "Schulthek"), (r"\bRanzen\b", "Thek"), (r"\bStra(ss|ß)enbahn", "Tram"), (r"\bBürgersteig", "Trottoir"),
    (r"\bSahne\b", "Rahm"), (r"\bPaprika\b", "Peperoni"), (r"\bKlassenfahrt", "Schulreise"), (r"\bPausenbrot", "Znüni"),
    (r"\bMülleimer", "Abfalleimer"), (r"\bBerlin\b", "Bern"), (r"\bHamburg\b", "Basel"), (r"\bMünchen\b", "Zürich"),
    (r"\bKöln\b", "Luzern"), (r"\bFrankfurt\b", "St. Gallen"), (r"\bStuttgart\b", "Wil"), (r"\bDresden\b", "Chur"),
    (r"\bLeipzig\b", "Thun"), (r"\bBremen\b", "Aarau"), (r"\bHannover\b", "Olten"), (r"\bKassel\b", "Aarau"), (r"\bFulda\b", "Zürich"), (r"\bAugsburg\b", "Winterthur"), (r"\bUlm\b", "Frauenfeld"), (r"\bMannheim\b", "St. Gallen"), (r"\bNürnberg\b", "Schaffhausen"),
    (r"\bBundesland\b", "Kanton"), (r"\bBundesländer", "Kantone"),
    (r"\bMathe Klasse (\d+)", r"Mathematik \1. Klasse"), (r"\b([Ii]n|[Aa]b) Klasse (\d+)", r"\1 der \2. Klasse"),
    (r"\bKlasse (\d+)(?![a-z\d])", r"\1. Klasse"), (r"\bMathe-Arbeitsbl", "Mathematik-Arbeitsbl"), (r"\bMathe\b", "Mathematik"),
    (r"\bKMK-Bildungsstandards?\b", "Lehrplan 21"), (r"\bBildungsstandards\b", "Lehrplan 21"),
    (r"\bCroissants?\b", "Gipfeli"), (r"\bKommaschreibweise", "Dezimalschreibweise"), (r"\bKommazahl", "Dezimalzahl"),
    (r"\bBücherei", "Bibliothek"), (r"\bLieblings-AG\b", "Lieblingskurs"),
    (r"\bKomma unter Komma", "Punkt unter Punkt"), (r"\b(hinter|vor|nach|mit) dem Komma", r"\1 dem Punkt"),
    (r"\bdas Komma\b", "der Punkt"), (r"\bDas Komma\b", "Der Punkt"), (r"\bdes Kommas\b", "des Punktes"), (r"\b(mit|ohne) Komma\b", r"\1 Punkt"),
    (r"\bKommastelle", "Dezimalstelle"), (r"\bKommabeträge", "Geldbeträge"), (r"\bKomma\b", "Punkt"),
    (r"\bEuro\b", "Franken"), (r"\bCent\b", "Rappen"),
]
DE_NAMES = {"Emma": "Chiara", "Mia": "Sara", "Hannah": "Elin", "Sophia": "Zoe", "Lena": "Julia", "Marie": "Nora", "Anna": "Jael", "Lina": "Svenja",
            "Clara": "Livia", "Ida": "Annina", "Paula": "Flurina", "Aylin": "Ladina", "Frieda": "Tamara", "Leni": "Fabienne",
            "Ben": "Gion", "Paul": "Dario", "Leon": "Fabio", "Finn": "Mattia", "Elias": "Joel", "Felix": "Remo", "Jonas": "Silvan",
            "Emil": "Andrin", "Max": "Flurin", "Anton": "Yanick", "Theo": "Severin", "Moritz": "Reto", "Yusuf": "Beat", "Luca": "Dominik"}
_DE_NAME_RE = re.compile(r"\b(%s)(s?)\b" % "|".join(sorted(DE_NAMES, key=len, reverse=True)))
LEAKS = ["€", " ct", "ct ", "Euro", "Cent", "ß", "Bundesland", "Grundschul", "Brötchen", "Fahrrad", "KMK", "Pfennig", "Kita", "Sonnabend",
         "Kommaschreibweise", "Komma", "Düsseldorf", "Dortmund", "Duisburg", "Bonn", "Mainz", "Kiel", "Rostock", "Potsdam", "Erfurt", "Magdeburg", "Bayern", "Sachsen"]


def _money(s):
    s = re.sub(r"(\d+),(\d\d)[  ]?€", r"\1.\2 Fr.", s)
    s = re.sub(r"(\d[\d ]*)[  ]?€", lambda m: m.group(1) + NB + "Fr.", s)
    s = re.sub(r"(\d+)[  ]?ct\b", lambda m: m.group(1) + NB + "Rp.", s)
    s = re.sub(r"(?<=[\s?=(])€", "Fr.", s)
    s = re.sub(r"(?<=[\s?=(])ct\b", "Rp.", s)
    return s


def _group(m):
    d = m.group(0)
    out = ""
    while len(d) > 3:
        out = AP + d[-3:] + out
        d = d[:-3]
    return d + out


def _textnode(s, full):
    s = s.replace("ß", "ss")
    s = _money(s)
    s = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", "", s)            # 10 000 → 10000（あとで ’ を付ける）
    s = re.sub(r"(?<=[\d☐□])\u00a0(?=[\d☐□]{3}(?![\d☐□]))", AP, s)
    s = re.sub(r"(?<=\d),(?=\d)", ".", s)                          # 2,5 → 2.5
    # 4 けた以上の整数に ’（小数部・時刻・年は除く）
    def grp(m):
        v = int(m.group(0))
        a, b = max(0, m.start() - 25), m.end() + 12
        ctx = full[a:b] if full is not None else s[max(0, m.start() - 25):m.end() + 12]
        if 1900 <= v <= 2099 and re.search(r"Jahr|geboren|Geburt|Kalender|\d\.\d{1,2}\.|Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember", ctx):
            return m.group(0)
        return _group(m)
    s = re.sub(r"(?<![\d.:’/])\d{4,}(?!\d|:\d)", grp, s)
    s = re.sub(r"(?<=\S)([\u00a0 ])·([\u00a0 ])(?=\S)", r"\1×\2", s)
    s = s.replace("·", "×")       # Deutschland: Malpunkt, Schweiz: ×
    s = re.sub(r"(Fr|Rp)\.\.", r"\1.", s)
    for a, b in WORDS:
        s = re.sub(a, b, s)
    s = _DE_NAME_RE.sub(lambda m: DE_NAMES[m.group(1)] + m.group(2), s)
    return s


def ch_text(s):
    if not isinstance(s, str):
        return s
    parts = re.split(r"(<[^>]*>)", s)
    out = []
    for p in parts:
        if p.startswith("<"):
            p = p.replace("ß", "ss")
            p = re.sub(r"aria-label='([^']*)'", lambda m: "aria-label='%s'" % _textnode(m.group(1), None).replace("'", "’"), p)
            out.append(p)
        else:
            out.append(_textnode(p, p))
    return re.sub(r"(Fr|Rp)\.((?:</[a-z]+>)+)\.", r"\1.\2", "".join(out))


def money_ok(s):
    for m in re.finditer(r"(\d+)\.(\d\d) ?Fr\.", s):
        if int(m.group(2)) % 5:
            return False
    for m in re.finditer(r"(\d+) ?Rp\.", s):
        if int(m.group(1)) % 5:
            return False
    return True


def leak(s):
    t = re.sub(r"<[^>]*>", " ", s)
    return [w for w in LEAKS if w in t]


def item_ok(it):
    blob = it["q"] + " " + " ".join(it["c"]) + " " + it["e"]
    if leak(blob) or not money_ok(blob):
        if DEBUG:
            DEBUG.append((leak(blob), money_ok(blob), it["q"][:90]))
        return False
    return len(set(it["c"])) == len(it["c"])


_orig_mcq = D.mcq


def mcq(*a, **k):
    try:
        it = _orig_mcq(*a, **k)
    except AssertionError:
        return None
    if not it:
        return it
    it = dict(it)
    it["q"], it["e"] = ch_text(it["q"]), ch_text(it["e"])
    it["c"] = [ch_text(c) for c in it["c"]]
    return it if item_ok(it) else None


D.mcq = mcq    # 以後 import される生成スクリプトはスイス式の mcq を使う


def chf(rp):
    """Rappen → 3.50 Fr. / 3 Fr. / 45 Rp."""
    rp = int(rp)
    if rp < 100:
        return "%d%sRp." % (rp, NB)
    f, r = divmod(rp, 100)
    return ("%s%sFr." % (_group_int(f), NB)) if r == 0 else ("%s.%02d%sFr." % (_group_int(f), r, NB))


def _group_int(n):
    return re.sub(r"\d{4,}", _group, str(n))


def num(n):
    n = int(n)
    return ("−" if n < 0 else "") + _group_int(abs(n))


# ------------------------------------------------------------ Schweizer Geld (Bild)
def coin(cx, cy, rp):
    r = {5: 14, 10: 15, 20: 16, 50: 14, 100: 17, 200: 19, 500: 21}[rp]
    fillc = "#e6d37a" if rp == 5 else "#d6d6d6"
    lab = {5: "5", 10: "10", 20: "20", 50: "½", 100: "1", 200: "2", 500: "5"}[rp]
    sub = "Rp." if rp < 50 else "Fr."
    return ("<circle cx='%.1f' cy='%.1f' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (cx, cy, r, fillc, INK)
            + text(cx, cy + 1, lab, 11, weight=700) + text(cx, cy + 9, sub, 6.5))


def note(x, y, fr):
    col = {10: "#f3d36b", 20: "#e8a0a0", 50: "#9fd39f", 100: "#9fc3e8", 200: "#d8b38a", 1000: "#c7a6e0"}[fr]
    return ("<rect x='%.1f' y='%.1f' width='70' height='38' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>"
            % (x, y, col, INK) + text(x + 35, y + 25, "%d%sFr." % (fr, NB), 14, weight=700))


def geld_svg(items):
    """items: Rappen; ab 1000 Rp. (10 Fr.) Noten, sonst Münzen. Andere Werte (z. B. 1 Rp., 5-Franken-Note) → ValueError"""
    for c in items:
        if c not in (5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 100000):
            raise ValueError("kein Schweizer Geld: %r" % c)
    s, x = [], 6
    for c in sorted([c for c in items if c >= 1000], reverse=True):
        s.append(note(x, 6, c // 100))
        x += 78
    for c in sorted([c for c in items if c < 1000], reverse=True):
        s.append(coin(x + 20, 25, c))
        x += 44
    return fig(svg_wrap(int(x + 4), 50, "".join(s), "Geld: zusammen %s" % chf(sum(items)).replace(NB, " ")))


# ------------------------------------------------------------ Einheit schreiben
def write(slug, grade, sort, codes, dom, title, short, meta, kb, ks, body, faq, sets, rnd, seo=None, std_note=""):
    """sets: [{"title", "items"}] oder [(Titel, items)]"""
    sets = [s if isinstance(s, dict) else {"title": s[0], "items": s[1]} for s in sets]
    sets = [{"title": ch_text(s["title"]), "items": s["items"]} for s in sets]
    assert len(sets) == 5
    seen = set()
    for st in sets:
        assert len(st["items"]) == 20, (slug, st["title"], len(st["items"]))
        for it in st["items"]:
            k = re.sub(r"\s+", " ", it["q"])
            assert k not in seen, ("duplicate", slug, k)
            seen.add(k)
            assert item_ok(it), (slug, it["q"][:80], leak(it["q"] + " ".join(it["c"]) + it["e"]))
    balance(sets, rnd)
    gnum = int(grade.split("-")[1])
    std = "Die Schülerinnen und Schüler %s (Lehrplan 21, %s)." % ("; sie ".join(KOMP[c] for c in codes), ", ".join(codes))
    t = lambda s: D.plain_text(ch_text(s))
    u = {
        "slug": slug, "title": t(title),
        "seo_title": seo or "%s – Mathematik %d. Klasse: Arbeitsblätter mit Lösungen" % (t(short), gnum),
        "short_title": t(short), "domain": DOMAIN[dom], "standard_code": ", ".join(codes), "standard_url": STD_URL,
        "standard_text": std + std_note, "meta_desc": t(meta), "key_big": t(kb), "key_sub": t(ks),
        "body_html": ch_text(body), "faq": [{"q": ch_text(f["q"]), "a": ch_text(f["a"])} for f in faq],
        "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    }
    for f in ("title", "meta_desc", "key_big", "key_sub", "body_html"):
        assert not leak(u[f]), (slug, f, leak(u[f]))
    for f in u["faq"]:
        assert not leak(f["q"] + f["a"]), (slug, f)
    write_unit("ch", "mathematik", grade, u)


def from_de(modname, seed, slug, grade, sort, codes, dom, seo=None, fix=None, std_note="", pre=None):
    """Deutschland の生成スクリプトを新しい seed で動かし、make_unit の中身を受け取ってスイス式で書く"""
    mod = importlib.import_module(modname)
    mod.R = random.Random(seed)
    for k in ("K", "KIDS"):
        if isinstance(getattr(mod, k, None), D.Kids):
            setattr(mod, k, D.Kids(mod.R))
    got = {}

    def cap(rnd, slug_, dom_, std_text, title, seo_title, short_title, meta_desc, key_big, key_sub, body_html, faq, sets, sort_, grade="klasse-3"):
        got.update(title=title, short=short_title, meta=meta_desc, kb=key_big, ks=key_sub, body=body_html, faq=faq, sets=sets)
    mod.make_unit = cap
    if pre:
        pre(mod)
    mod.main()
    if fix:
        fix(got)
    write(slug, grade, sort, codes, dom, got["title"], got["short"], got["meta"], got["kb"], got["ks"], got["body"], got["faq"],
          got["sets"], random.Random(seed + 7), seo=seo, std_note=std_note)


D.geld_svg = geld_svg    # Deutschland の生成スクリプトの絵もスイスの硬貨・紙幣に
