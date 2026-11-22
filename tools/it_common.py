# -*- coding: utf-8 -*-
"""
Italia (scuola primaria, Indicazioni nazionali per il curricolo) の単元生成の共通部品。
・文はイタリア語。子ども向けに短い文、tu で話しかける（Calcola, Scegli, Quanti …?）
・数: 4 桁はそのまま（1000、4536）、5 桁以上はノーブレークスペースで区切る（12 000）。小数はコンマ（2,5）
・記号: 3 × 4、12 : 3（÷ も可）、時刻は 8:15、時間の長さは 1 h 25 min
・お金: 3,50 €、50 cent
・位の名前: u, da, h, uk（unità, decine, centinaia, migliaia）
・HTML の属性はシングルクォート、バックスラッシュなし（check.py と同じルール）
・絵は fr_common の部品を使い、aria-label をイタリア語にする
"""
import math
import re
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)
import fr_common as _F
from fr_common import pick_unique, mix  # noqa: F401

UPDATED = "2026-11-22"
NB = "\u00a0"
FOIS = "×"
DIV = ":"
STD_URL = "https://www.mim.gov.it/documents/20182/10554370/curricolo_web.pdf"
DOMAIN = {"N": "Numeri", "S": "Spazio e figure", "M": "Misure", "D": "Relazioni, dati e previsioni", "P": "Problemi"}
GRADE_NAME = {"classe-prima": "Classe prima", "classe-seconda": "Classe seconda", "classe-terza": "Classe terza",
              "classe-quarta": "Classe quarta", "classe-quinta": "Classe quinta"}
GIRLS = ["Giulia", "Sofia", "Aurora", "Alice", "Ginevra", "Emma", "Giorgia", "Beatrice", "Anna", "Vittoria", "Chiara", "Martina", "Greta", "Sara"]
BOYS = ["Leonardo", "Francesco", "Tommaso", "Edoardo", "Alessandro", "Lorenzo", "Mattia", "Gabriele", "Riccardo", "Andrea", "Matteo", "Pietro", "Luca", "Marco"]


# ------------------------------------------------------------ numbers
def num(n):
    """1000, 4536, 12 000（5 桁以上はノーブレークスペースで区切る）"""
    n = int(n)
    s = str(abs(n))
    if len(s) >= 5:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return ("−" if n < 0 else "") + s


def dec(v, places=None):
    """numero decimale con la virgola: 2,5 / 1,25"""
    if places is None:
        s = ("%.3f" % v).rstrip("0").rstrip(".")
    else:
        s = ("%." + str(places) + "f") % v
    ip, _, fp_ = s.partition(".")
    return num(int(ip)) + ("," + fp_ if fp_ else "")


def eur(cents, c=False):
    """denaro: 350 → 3,50 €, 300 → 3 €, 45 → 45 cent（c=True のとき 1 € 未満は cent）"""
    cents = int(cents)
    if c and cents < 100:
        return "%d%scent" % (cents, NB)
    e, r = divmod(cents, 100)
    if r == 0:
        return "%s%s€" % (num(e), NB)
    return "%s,%02d%s€" % (num(e), r, NB)


def unit(v, u):
    return "%s%s%s" % (num(v) if isinstance(v, int) else v, NB, u)


def ora(h, m):
    """8:15, 14:00"""
    return "%d:%02d" % (h, m)


def dur(mins):
    """durata: 1 h 25 min, 45 min, 2 h"""
    h, m = divmod(int(mins), 60)
    if h and m:
        return "%d%sh%s%d%smin" % (h, NB, NB, m, NB)
    if h:
        return "%d%sh" % (h, NB)
    return "%d%smin" % (m, NB)


def pl(n, s, p):
    """1 matita / 3 matite"""
    return "%s %s" % (num(n), s if n == 1 else p)


# ------------------------------------------------------------ names
class Kids:
    """nomi con genere: next() → (nome, 'lei'|'lui')"""

    def __init__(self, rnd):
        self.pool = [(n, "lei") for n in GIRLS] + [(n, "lui") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def two(self):
        a = self.next()
        b = self.next()
        while b[0] == a[0]:
            b = self.next()
        return a, b


def art(p):
    """articolo davanti a un aggettivo: « Giulia è stata brava » / « Luca è stato bravo »"""
    return "a" if p[1] == "lei" else "o"


# ------------------------------------------------------------ questions
def mcq(q, correct, cands, e, neg=False):
    """4 択：正解＋重複しない誤答 3 つ。足りないときは答えの数を ±1、±2 … した近い数で補う。"""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or (not neg and (c.startswith("-") or c.startswith("−"))):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3:
        import os
        if os.environ.get("IT_WARN"):
            print("FILL:", re.sub(r"<[^>]+>", " ", q)[-90:], "|", correct)
    if len(pick) < 3 and "<" not in correct:
        m = re.match(r"^(.*?)(\d(?:\d|\u00a0(?=\d))*(?:,\d+)?)([^\d]*)$", correct)
        if m:
            raw = m.group(2).replace(NB, "")
            places = len(raw.split(",")[1]) if "," in raw else 0
            v = int(raw.replace(",", ""))
            for d_ in (1, -1, 2, -2, 3, 10, -10):
                nv = v + d_
                if nv <= 0:
                    continue
                body = num(nv) if places == 0 else "%s,%s" % (num(nv // 10 ** places), str(nv % 10 ** places).rjust(places, "0"))
                c = "%s%s%s" % (m.group(1), body, m.group(3))
                if c not in seen:
                    seen.add(c)
                    pick.append(c)
                if len(pick) == 3:
                    break
    assert len(pick) == 3, (q, correct, cands)
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


# ------------------------------------------------------------ lesson
table = _F.table


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Esempio</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Risposta: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html : Come si fa → Esempi → Errori frequenti（frasi brevi）"""
    h = "<h2>Come si fa</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(example(a, b, c) for a, b, c in examples)
    h += "<h2>Errori frequenti</h2>" + table(["Errore frequente", "Che cosa fare"], mist)
    return h


def plain_text(t):
    t = re.sub(r"<span class='fr'><span class='fn'>(.*?)</span><span class='fd'>([^<]*)</span></span>", r"\1/\2", t)
    assert not re.search(r"<[a-zA-Z/]", t), t
    return t


def make_unit(rnd, slug, dom, std_text, title, short_title, meta_desc,
              key_big, key_sub, body_html, faq, sets, sort, grade="classe-terza"):
    sets = [{"title": t, "items": items} for t, items in sets]
    assert len(sets) == 5, slug
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
        for it in s["items"]:
            k = re.sub(r"\s+", " ", it["q"])
            assert k not in allq, ("duplicate question", slug, k)
            allq.add(k)
    balance(sets, rnd)
    gname = GRADE_NAME[grade]
    seo_title = "%s %s: schede di matematica con soluzioni" % (short_title, gname.lower())
    title, seo_title, short_title, meta_desc, key_big, key_sub = [plain_text(x) for x in (title, seo_title, short_title, meta_desc, key_big, key_sub)]
    dname = DOMAIN[dom]
    write_unit("it", "matematica", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": dname, "standard_code": "%s · %s" % (gname, dname), "standard_url": STD_URL,
        "standard_text": std_text + (" (sintesi degli obiettivi di apprendimento al termine della classe terza della scuola secondaria di primo grado, Indicazioni nazionali)" if grade.endswith("-media") else
                                      " (sintesi degli obiettivi di apprendimento al termine della classe %s, Indicazioni nazionali)" % ("quinta" if grade in ("classe-quarta", "classe-quinta") else "terza")),
        "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


# ------------------------------------------------------------ pictures（fr_common の絵に、イタリア語のラベル）
wrap = _F.wrap


def relabel(svg, label):
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label.replace("'", "’"), svg, count=1)


def retta(lo, hi, step, marks=(), labels=None, every=None, width=460):
    """retta numerica"""
    s = _F.droite(lo, hi, step, marks, labels, "retta numerica", every, width)
    return s.replace(">1" + NB + "000<", ">1000<")


def blocchi(m, c, d, u):
    """materiale multibase: migliaia, centinaia, decine, unità"""
    s = _F.blocs(m, c, d, u, label="%d migliaia, %d centinaia, %d decine, %d unità" % (m, c, d, u))
    return s.replace(">1" + NB + "000<", ">1000<")


def tabella_valore(n, cols=3):
    """tabella h da u（uk h da u）"""
    head = ["uk", "h", "da", "u"][4 - cols:]
    ds = str(n).rjust(cols, " ")
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head),
               "".join("<td style='text-align:center;min-width:30px'>%s</td>" % (d if d != " " else "") for d in ds)))


def istogramma(data, unit_label="", step=None):
    return relabel(_F.barres(data, unit_label, "istogramma", step), "istogramma")


def soldi_svg(items):
    """items: importi in centesimi; da 500 in su, banconote"""
    s = _F.argent_svg(items)
    return relabel(s, "monete e banconote: in tutto %s" % eur(sum(items)).replace(NB, " "))


def solido_svg(kind, r=34, color="#cfe6d6"):
    """cubo, parallelepipedo, sfera, cilindro, cono, piramide"""
    k = {"cubo": "cube", "parallelepipedo": "pave", "sfera": "boule", "cilindro": "cylindre", "cono": "cone", "piramide": "pyramide"}[kind]
    return relabel(_F.solide_svg(k, r, color), "un solido")


def orologio(h, m, size=170):
    from tw_common import clock as _clock
    return _clock(h, m, size, label="orologio")


def colonna(rows, op="+", label="operazione in colonna", result=None):
    import de_common
    return de_common.schriftlich(rows, op, None, label, result)


def striscia(d, k, w=300):
    return relabel(_F.bande(d, k, w), "striscia divisa in %d parti uguali, %d colorate" % (d, k))


def cerchio(d, k, r=60):
    return relabel(_F.disque(d, k, r), "cerchio diviso in %d parti uguali, %d colorate" % (d, k))


# ------------------------------------------------------------ numeri in lettere (fino a 9999)
_U = ["zero", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove", "dieci",
      "undici", "dodici", "tredici", "quattordici", "quindici", "sedici", "diciassette", "diciotto", "diciannove"]
_D = {2: "venti", 3: "trenta", 4: "quaranta", 5: "cinquanta", 6: "sessanta", 7: "settanta", 8: "ottanta", 9: "novanta"}


def _w99(n):
    if n < 20:
        return _U[n]
    d, u = divmod(n, 10)
    t = _D[d]
    if u == 0:
        return t
    if u in (1, 8):
        t = t[:-1]                     # ventuno, trentotto
    return t + ("tré" if u == 3 else _U[u])


def lettere(n):
    """numero in lettere: 342 → trecentoquarantadue, 1000 → mille"""
    if n == 0:
        return "zero"
    out = ""
    k, n = divmod(n, 1000)
    if k:
        out += "mille" if k == 1 else _w99(k) + "mila" if k < 100 else lettere(k) + "mila"
    c, r = divmod(n, 100)
    if c:
        out += ("cento" if c == 1 else _U[c] + "cento")
        if r and (r // 10 == 8 or r == 8):
            out = out[:-1]             # centottanta
    if r:
        w = _w99(r)
        if w == "tre" and (c or k):
            w = "tré"                  # centotré
        out += w
    return out
