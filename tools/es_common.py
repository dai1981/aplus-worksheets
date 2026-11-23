# -*- coding: utf-8 -*-
"""
España (Educación Primaria, LOMLOE, Real Decreto 157/2022) の単元生成の共通部品。
・文はスペイン語（スペイン）。子ども向けに短い文、tú で話しかける（Calcula, Elige, ¿Cuántos …?）
・数: 4 桁はそのまま（4536）、5 桁以上はノーブレークスペースで区切る（12 345。RAE のとおり）。小数はコンマ（2,5）
・記号: 3 × 4、12 : 3（割り算はスペインの学校と同じ「:」）。余りは「23 : 5 = 4 y resto 3」
・時刻は 8:15、時間の長さは 1 h 25 min。お金: 3,50 €、50 céntimos（硬貨 1・2・5・10・20・50 céntimos と 1・2 €、紙幣 5〜500 €）
・位の名前: U, D, C, UM, DM, CM（unidades, decenas, centenas, unidades de millar…）
・HTML の属性はシングルクォート、バックスラッシュなし（check.py と同じルール）
・絵は fr_common・de_common の部品を使い、aria-label をスペイン語にする
"""
import os
import re
import random
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)
import fr_common as _F
from fr_common import pick_unique, mix  # noqa: F401

UPDATED = "2026-11-23"
NB = " "
POR = "×"
DIV = ":"
STD_URL = "https://www.boe.es/buscar/act.php?id=BOE-A-2022-3296"
DOMAIN = {"N": "Sentido numérico", "M": "Sentido de la medida", "E": "Sentido espacial", "A": "Sentido algebraico", "S": "Sentido estocástico"}
GRADE_NAME = {"%d-primaria" % i: "%d.º de Primaria" % i for i in range(1, 7)}
CICLO = {1: "primer ciclo", 2: "primer ciclo", 3: "segundo ciclo", 4: "segundo ciclo", 5: "tercer ciclo", 6: "tercer ciclo"}
GIRLS = ["Lucía", "Sofía", "Martina", "María", "Julia", "Paula", "Valeria", "Emma", "Daniela", "Carla", "Alba", "Noa", "Olivia", "Vega"]
BOYS = ["Hugo", "Martín", "Lucas", "Mateo", "Leo", "Daniel", "Alejandro", "Pablo", "Manuel", "Álvaro", "Adrián", "Mario", "Diego", "Marcos"]


# ------------------------------------------------------------ numbers
def num(n):
    """4536, 12 345（5 桁以上はノーブレークスペースで区切る）"""
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
    """número decimal con coma: 2,5 / 1,25"""
    if places is None:
        s = ("%.3f" % v).rstrip("0").rstrip(".")
    else:
        s = ("%." + str(places) + "f") % v
    ip, _, fp_ = s.partition(".")
    return num(int(ip)) + ("," + fp_ if fp_ else "")


def dz(n, k, keep=False):
    """entero n × 10^−k con coma: dz(25, 1) → 2,5; dz(250, 2) → 2,5（keep=True で 2,50）"""
    n = int(n)
    neg = n < 0
    ip, fp_ = divmod(abs(n), 10 ** k)
    f = str(fp_).rjust(k, "0") if k else ""
    if not keep:
        f = f.rstrip("0")
    return ("−" if neg else "") + num(ip) + ("," + f if f else "")


def eur(cents, c=False):
    """dinero: 350 → 3,50 €, 300 → 3 €, 45 → 45 céntimos（c=True のとき 1 € 未満は céntimos）"""
    cents = int(cents)
    if c and cents < 100:
        return "%d%s%s" % (cents, NB, "céntimo" if cents == 1 else "céntimos")
    e, r = divmod(cents, 100)
    if r == 0:
        return "%s%s€" % (num(e), NB)
    return "%s,%02d%s€" % (num(e), r, NB)


def unit(v, u):
    return "%s%s%s" % (num(v) if isinstance(v, int) else v, NB, u)


def hora(h, m):
    """8:15, 14:00"""
    return "%d:%02d" % (h, m)


def dur(mins):
    """duración: 1 h 25 min, 45 min, 2 h"""
    h, m = divmod(int(mins), 60)
    if h and m:
        return "%d%sh%s%d%smin" % (h, NB, NB, m, NB)
    if h:
        return "%d%sh" % (h, NB)
    return "%d%smin" % (m, NB)


def pl(n, s, p):
    """1 lápiz / 3 lápices"""
    return "%s %s" % (num(n), s if n == 1 else p)


# ------------------------------------------------------------ names
class Kids:
    """nombres con género: next() → (nombre, 'ella'|'él')"""

    def __init__(self, rnd):
        self.pool = [(n, "ella") for n in GIRLS] + [(n, "él") for n in BOYS]
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


def ao(p, masc, fem):
    """concordancia: ao(p, 'contento', 'contenta')"""
    return fem if p[1] == "ella" else masc


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
    if len(pick) < 3 and os.environ.get("ES_WARN"):
        print("FILL:", re.sub(r"<[^>]+>", " ", q)[-90:], "|", correct)
    if len(pick) < 3 and "<" not in correct:
        m = re.match(r"^(.*?)(\d(?:\d| (?=\d))*(?:,\d+)?)([^\d]*)$", correct)
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


def bank(R, items, name="bank"):
    """generador que elige de una lista [(pregunta, respuesta, [incorrectas])]"""
    def mk():
        q, a, w = R.choice(items)
        return mcq(q, a, w, "Respuesta: <b>%s</b>." % a)
    mk.__name__ = name
    return mk


# ------------------------------------------------------------ lesson
table = _F.table


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Ejemplo</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Respuesta: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html : Cómo se hace → Ejemplos → Errores frecuentes（frases cortas）"""
    h = "<h2>Cómo se hace</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(example(a, b, c) for a, b, c in examples)
    h += "<h2>Errores frecuentes</h2>" + table(["Error frecuente", "Qué hacer"], mist)
    return h


def plain_text(t):
    t = re.sub(r"<span class='fr'><span class='fn'>(.*?)</span><span class='fd'>([^<]*)</span></span>", r"\1/\2", t)
    assert not re.search(r"<[a-zA-Z/]", t), t
    return t


def make_unit(rnd, slug, dom, std_text, title, short_title, meta_desc,
              key_big, key_sub, body_html, faq, sets, sort, grade="4-primaria"):
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
    lvl = int(grade.split("-")[0])
    seo_title = "%s – %s: fichas de matemáticas con soluciones" % (short_title, gname)
    title, seo_title, short_title, meta_desc, key_big, key_sub = [plain_text(x) for x in (title, seo_title, short_title, meta_desc, key_big, key_sub)]
    # la parte de arriba de la página: frases cortas
    assert len(key_big) <= 36 and len(key_sub) <= 50 and len(title) <= 50, (slug, key_big, key_sub, title)
    dname = DOMAIN[dom]
    write_unit("es", "matematicas", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": dname, "standard_code": "%s · %s" % (gname, dname), "standard_url": STD_URL,
        "standard_text": std_text + " (resumen de los saberes básicos de Matemáticas del %s de Educación Primaria, Real Decreto 157/2022)" % CICLO[lvl],
        "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


# ------------------------------------------------------------ pictures（fr_common の絵に、スペイン語のラベル）
wrap = _F.wrap


def relabel(svg, label):
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label.replace("'", "’"), svg, count=1)


def _num4(svg):
    """fr_common の絵の「1 000」（4 桁）を「1000」に"""
    return re.sub(r">(\d)[   ](\d{3})<", r">\1\2<", svg)


def recta(lo, hi, step, marks=(), labels=None, every=None, width=460):
    """recta numérica"""
    return _num4(_F.droite(lo, hi, step, marks, labels, "recta numérica", every, width))


def bloques(m, c, d, u):
    """bloques multibase: millares, centenas, decenas, unidades"""
    return _num4(_F.blocs(m, c, d, u, label="bloques: %d millares, %d centenas, %d decenas, %d unidades" % (m, c, d, u)))


def tabla_valor(n, cols=4):
    """tabla de valor posicional: CMi DMi UMi CM DM UM C D U"""
    head = ["CMi", "DMi", "UMi", "CM", "DM", "UM", "C", "D", "U"][9 - cols:]
    ds = str(n).rjust(cols, " ")
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head),
               "".join("<td style='text-align:center;min-width:30px'>%s</td>" % (d if d != " " else "") for d in ds)))


def tabla_decimal(centesimas, places=2, ints=1):
    """tabla de valor posicional con decimales: U, d c（centesimas = valor × 100）"""
    head = ["C", "D", "U"][3 - ints:] + ["d", "c", "m"][:places]
    ip, fp_ = divmod(int(centesimas), 100)
    ds = str(ip).rjust(ints, " ") + str(fp_).rjust(2, "0")[:places]
    cells = []
    for i, d in enumerate(ds):
        b = " style='text-align:center;min-width:30px%s'" % (";border-left:3px solid #333" if i == ints else "")
        cells.append("<td%s>%s</td>" % (b, d if d != " " else ""))
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead><tbody><tr>%s</tr></tbody></table>"
            % ("".join("<th>%s</th>" % h for h in head), "".join(cells)))


def grafico(data, unit_label="", step=None):
    """gráfico de barras"""
    return _num4(relabel(_F.barres(data, unit_label, "gráfico de barras", step), "gráfico de barras"))


def dinero_svg(items):
    """items: cantidades en céntimos; desde 500, billetes"""
    s = _F.argent_svg(items)
    return relabel(s, "monedas y billetes: en total %s" % eur(sum(items)).replace(NB, " "))


def cuerpo_svg(kind, r=34, color="#cfe6d6"):
    """cubo, prisma, esfera, cilindro, cono, piramide"""
    k = {"cubo": "cube", "prisma": "pave", "esfera": "boule", "cilindro": "cylindre", "cono": "cone", "piramide": "pyramide"}[kind]
    return relabel(_F.solide_svg(k, r, color), "un cuerpo geométrico")


def reloj(h, m, size=170):
    from tw_common import clock as _clock
    return _clock(h, m, size, label="reloj de agujas")


def vertical(rows, op="+", label="operación en vertical", result=None):
    """cuenta en vertical sobre papel cuadriculado"""
    import de_common
    return de_common.schriftlich(rows, op, None, label, result)


def tira(d, k, w=300):
    return relabel(_F.bande(d, k, w), "tira dividida en %d partes iguales, %d %s" % (d, k, "coloreada" if k == 1 else "coloreadas"))


def circulo(d, k, r=60):
    return relabel(_F.disque(d, k, r), "círculo dividido en %d partes iguales, %d %s" % (d, k, "coloreada" if k == 1 else "coloreadas"))


# ------------------------------------------------------------ números en letra (hasta 999 999)
_U = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
      "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve",
      "veinte", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
_D = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
_C = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos", 7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def _w99(n):
    if n < 30:
        return _U[n]
    d, u = divmod(n, 10)
    return _D[d] + ("" if u == 0 else " y " + _U[u])


def _w999(n):
    if n == 100:
        return "cien"
    c, r = divmod(n, 100)
    if not c:
        return _w99(r)
    return _C[c] + ("" if r == 0 else " " + _w99(r))


def letra(n):
    """número en letra: 342 → trescientos cuarenta y dos; 21 000 → veintiún mil"""
    if n == 0:
        return "cero"
    k, r = divmod(n, 1000)
    out = ""
    if k:
        if k == 1:
            out = "mil"
        else:
            w = _w999(k)
            w = re.sub(r"veintiuno$", "veintiún", w)
            w = re.sub(r"(^|\s)uno$", r"\1un", w)
            out = w + " mil"
    if r:
        out += (" " if out else "") + _w999(r)
    return out


# ------------------------------------------------------------ reutilizar generadores
def keep(maker, *preds):
    def mk():
        it = maker()
        if it is None:
            return None
        for p in preds:
            if not p(it):
                return None
        return it
    mk.__name__ = getattr(maker, "__name__", "mk")
    return mk


def use(modname, seed, *names, preds=()):
    """importa otro generador de España, cambia su R y devuelve los generadores pedidos"""
    import importlib
    m = importlib.import_module(modname)
    if getattr(m, "_es_seed", None) != seed:
        m.R = random.Random(seed)
        if hasattr(m, "K"):
            m.K = Kids(m.R)
        m._es_seed = seed
    out = [keep(getattr(m, n), *preds) for n in names]
    return out[0] if len(out) == 1 else out


# ------------------------------------------------------------ fracciones
_DEN = {2: "medio", 3: "tercio", 4: "cuarto", 5: "quinto", 6: "sexto", 7: "séptimo", 8: "octavo", 9: "noveno", 10: "décimo",
        11: "onceavo", 12: "doceavo", 100: "centésimo"}


def nomfrac(n, d):
    """3/4 → «tres cuartos», 1/2 → «un medio»"""
    w = _DEN[d] if d in _DEN else "%savo" % _U[d] if d < 20 else None
    if n == 1:
        return "un " + w
    t = _U[n] if n < 20 else letra(n)
    if t.endswith("veintiuno"):
        t = t[:-3] + "ún"
    elif t.endswith("uno"):
        t = t[:-1]
    return "%s %ss" % (t, w)


def letra_big(n):
    """hasta 999 999 999: 2 345 000 → dos millones trescientos cuarenta y cinco mil"""
    m, r = divmod(n, 10 ** 6)
    if not m:
        return letra(n)
    if m == 1:
        out = "un millón"
    else:
        w = letra(m)
        w = re.sub(r"veintiuno$", "veintiún", w)
        w = re.sub(r"(^|\s)uno$", r"\1un", w)
        out = w + " millones"
    if r:
        out += " " + letra(r)
    return out
