# -*- coding: utf-8 -*-
"""
México (Educación primaria, Plan de Estudio 2022 / Nueva Escuela Mexicana, Programas sintéticos SEP 2024) の単元生成の共通部品。
・country «mx»、lang «es-MX»、grade «N-primaria»（name «3.er grado de primaria»）。Carta (Letter)
・数は SEP の教科書と同じ: 1 000 以上は空白区切り（4 536、12 345。ノーブレークスペース）、小数は点（2.5）
・お金はペソ: $25、$3.50、50 centavos（硬貨 50¢・$1・$2・$5・$10・$20、紙幣 $20・$50・$100・$200・$500・$1 000）
・記号: 3 × 4、12 ÷ 3。余りは「23 ÷ 5 = 4 y sobran 3」。時刻は 8:15、「cuarto para las cuatro」（「menos cuarto」は使わない）
・スペインの生成スクリプト（gen_es_matematicas_*）の問題関数を src() で再利用する。mx_text() で数・お金・記号・語をメキシコ式に直し、
  直せない語（LEAKS）が残った問題は落とす
"""
import re
import random
import importlib
from ws_common import balance, write_unit, fig, svg_wrap, text, line  # noqa: F401
import es_common as ES
from es_common import mix, lesson, letra, nomfrac, keep, lim, sin, bank, relabel, NB  # noqa: F401

UPDATED = "2026-11-24"
F4 = "https://educacionbasica.sep.gob.mx/wp-content/uploads/2024/08/5.pdf"
F5 = "https://educacionbasica.sep.gob.mx/wp-content/uploads/2024/08/6.pdf"
STD_URL = {3: F4, 4: F4, 5: F5, 6: F5}
FASE = {1: 3, 2: 3, 3: 4, 4: 4, 5: 5, 6: 5}
GRADE_NAME = {1: "1.er grado de primaria", 2: "2.º grado de primaria", 3: "3.er grado de primaria", 4: "4.º grado de primaria", 5: "5.º grado de primaria", 6: "6.º grado de primaria"}
GRADE_SHORT = {1: "1.er grado", 2: "2.º grado", 3: "3.er grado", 4: "4.º grado", 5: "5.º grado", 6: "6.º grado"}
# contenidos de Saberes y Pensamiento Científico (Programa sintético): clave → (grupo en la página del grado, nombre del contenido)
CONT = {
    "N": ("Estudio de los números", "Estudio de los números"),
    "S": ("Suma y resta", "Suma y resta, su relación como operaciones inversas"),
    "P": ("Multiplicación y división", "Multiplicación y división, su relación como operaciones inversas"),
    "C": ("Figuras y cuerpos geométricos", "Cuerpos geométricos y sus características"),
    "F": ("Figuras y cuerpos geométricos", "Figuras geométricas y sus características"),
    "L": ("Medición", "Medición de longitud, masa y capacidad"),
    "A": ("Medición", "Cálculo de perímetro y área"),
    "T": ("Medición", "Medición del tiempo"),
    "D": ("Organización e interpretación de datos", "Organización e interpretación de datos"),
    # Fase 5
    "Q": ("Multiplicación y división", "Relaciones de proporcionalidad"),
    "U": ("Figuras y cuerpos geométricos", "Ubicación espacial"),
    "L5": ("Medición", "Medición de la longitud, masa y capacidad"),
    "V": ("Medición", "Perímetro, área y noción de volumen"),
    "B": ("Organización e interpretación de datos", "Nociones de probabilidad"),
}
GIRLS = ["Ximena", "Valentina", "Regina", "Camila", "Renata", "Sofía", "Fernanda", "Natalia", "Andrea", "Itzel", "Daniela", "Paola", "Lupita", "Mariana"]
BOYS = ["Santiago", "Diego", "Emiliano", "Leonardo", "Sebastián", "Mateo", "Luis", "Jorge", "Rodrigo", "Carlos", "Emilio", "Ángel", "Josué", "Iván"]
CIUDADES = ["Guadalajara", "Monterrey", "Puebla", "Mérida", "Oaxaca", "Querétaro", "Toluca", "León", "Morelia", "Veracruz"]


class Kids(ES.Kids):
    def __init__(self, rnd):
        self.pool = [(n, "ella") for n in GIRLS] + [(n, "él") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0


# ------------------------------------------------------------ números y dinero
def num(n):
    """4 536, 12 345（1 000 以上はノーブレークスペースで区切る。SEP の教科書と同じ）"""
    n = int(n)
    s = str(abs(n))
    if len(s) >= 4:
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        s = NB.join(g)
    return ("−" if n < 0 else "") + s


def dec(v, places=None):
    if places is None:
        s = ("%.3f" % v).rstrip("0").rstrip(".")
    else:
        s = ("%." + str(places) + "f") % v
    ip, _, fp_ = s.partition(".")
    return num(int(ip)) + ("." + fp_ if fp_ else "")


def peso(cents, c=False):
    """350 → $3.50, 300 → $3, 50 → 50 centavos（c=True）"""
    cents = int(cents)
    if c and cents < 100:
        return "%d%s%s" % (cents, NB, "centavo" if cents == 1 else "centavos")
    e, r = divmod(cents, 100)
    return "$" + num(e) + (".%02d" % r if r else "")


def hora(h, m):
    return "%d:%02d" % (h, m)


HORAS = ["doce", "una", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce"]


def hora_letra(h, m):
    """8:15 → «las ocho y cuarto»; 3:45 → «cuarto para las cuatro»; 1:50 → «diez para las dos»"""
    h12 = h % 12
    art = lambda k: "la una" if k % 12 == 1 else "las " + HORAS[k % 12]
    if m == 0:
        return art(h12) + " en punto"
    if m == 15:
        return art(h12) + " y cuarto"
    if m == 30:
        return art(h12) + " y media"
    if m < 30:
        return art(h12) + " y " + letra(m)
    falta = 60 - m
    return ("cuarto" if falta == 15 else letra(falta)) + " para " + art(h12 + 1)


def pl(n, s, p):
    return "%s %s" % (num(n), s if n == 1 else p)


# ------------------------------------------------------------ España → México
WORDS = [("ha redondeado", "redondeó"), ("montañeros", "alpinistas"), ("huchas", "alcancías"), ("baloncesto", "basquetbol"), ("en forma compleja", "con dos unidades"), ("prisma rectangular (ortoedro)", "prisma rectangular"), ("ortoedros", "prismas rectangulares"), ("ortoedro", "prisma rectangular"), ("vallas", "cercas"), ("valla", "cerca"), ("baldosas", "losetas"), ("baldosa", "loseta"), ("hucha", "alcancía"),
         ("coma debajo de coma", "punto debajo de punto"), ("1 décima", "1 décimo"), ("1 centésima", "1 centésimo"), ("1 milésima", "1 milésimo"),
         ("ha recorrido", "recorrió"), ("ha acertado", "acertó"), ("ha volado", "voló"), ("sin comas", "sin el punto"), ("numerador : denominador", "numerador ÷ denominador"), ("se han recorrido", "se recorrieron"), ("ha ahorrado", "ahorró"), ("ha leído", "leyó"), ("han leído", "leyeron"), ("ha gastado", "gastó"), ("han gastado", "gastaron"), ("ha ganado", "ganó"), ("ha vendido", "vendió"), ("han vendido", "vendieron"), ("ha corrido", "corrió"), ("ha sacado", "sacó"), ("ha obtenido", "obtuvo"), ("Un grifo", "Una llave"), ("En rebajas", "En oferta"), ("Una noria", "Una rueda de la fortuna"), ("una noria", "una rueda de la fortuna"), ("La noria", "La rueda de la fortuna"), ("la noria", "la rueda de la fortuna"), ("ha girado", "giró"), ("césped", "pasto"), ("sin solaparse", "sin encimarse"), ("tejado", "techo"), ("Un brik", "Un envase de cartón"), ("un brik", "un envase de cartón"), ("Cara o cruz", "Águila o sol"), ("cara o cruz", "águila o sol"), ("sacar cruz", "sacar sol"), ("salga cruz", "salga sol"), ("sale cruz", "sale sol"),
         ("sacar cara", "sacar águila"), ("salga cara", "salga águila"), ("sale cara", "sale águila"), ("«cruz»", "«sol»"), ("«cara»", "«águila»"), ("sucesos", "eventos"), ("suceso", "evento"),
         ("se ha anotado", "se anotó"), ("ha salido cara", "ha caído águila"), ("cara, porque", "águila, porque"), ("cruz, porque", "sol, porque"), ("cara y cruz", "águila y sol"), ("ha caído águila", "cayó águila"), ("ha salido", "salió"), ("han salido", "salieron"), ("ha anotado", "anotó"), ("en rebajas", "en oferta"), ("un grifo", "una llave"), ("el grifo", "la llave"), ("han recorrido", "recorrieron"), ("como si no hubiera coma", "como si no hubiera punto"), ("se alquilan", "se rentan"), ("alquilan", "rentan"), ("alquila", "renta"), ("alquilar", "rentar"), ("alquiler", "renta"), ("sin la coma", "sin el punto"), ("chinchetas", "tachuelas"), ("chincheta", "tachuela"), ("han comido", "comieron"), ("han pintado", "pintaron"), ("han recogido", "recogieron"), ("ha comprado", "compró"), ("han ocupado", "ocuparon"),
         ("han quedado", "quedaron"), ("Iker", "Iván"), ("la coma", "el punto"), ("una décima", "un décimo"), ("una centésima", "un centésimo"), ("una milésima", "un milésimo"),
         ("las décimas", "los décimos"), ("las centésimas", "los centésimos"), ("las milésimas", "los milésimos"), ("décimas", "décimos"), ("centésimas", "centésimos"), ("milésimas", "milésimos"), ("zumos", "jugos"), ("zumo", "jugo"), ("gominolas", "dulces"), ("chuches", "dulces"), ("caramelos", "dulces"), ("caramelo", "dulce"),
         ("autobuses", "camiones"), ("autobús", "camión"), ("patatas", "papas"), ("patata", "papa"), ("melocotones", "duraznos"), ("melocotón", "durazno"),
         ("bolígrafos", "plumones"), ("bolígrafo", "plumón"), ("rotuladores", "marcadores"), ("rotulador", "marcador"),
         ("pegatinas", "estampas"), ("pegatina", "estampa"), ("mariquitas", "catarinas"), ("mariquita", "catarina"), ("móviles", "celulares"), ("móvil", "celular"),
         ("cacahuetes", "cacahuates"), ("cacahuete", "cacahuate"), ("piscinas", "albercas"), ("piscina", "alberca"), ("camisetas", "playeras"), ("camiseta", "playera"),
         ("las zapatillas", "los tenis"), ("unas zapatillas", "unos tenis"), ("magdalenas", "mantecadas"), ("magdalena", "mantecada"),
         ("cuadernillo", "cuaderno"), ("coger", "tomar"), ("coge", "toma"), ("cogen", "toman"), ("cogió", "tomó"), ("coges", "tomas"),
         ("se estropean", "se echan a perder"), ("se estropea", "se echa a perder"), ("frutería", "frutería"),
         ("Madrid", "Ciudad de México"), ("Barcelona", "Guadalajara"), ("Sevilla", "Puebla"),
         ("Valencia", "Monterrey"), ("Bilbao", "Mérida"), ("Zaragoza", "Querétaro"), ("Málaga", "Oaxaca"), ("Granada", "Morelia"), ("Salamanca", "Toluca"),
         ("Toledo", "León"), ("Córdoba", "Veracruz"), ("ladrillos", "tabiques"), ("castañas", "nueces"),
         ("Lucía", "Ximena"), ("Martina", "Regina"), ("Hugo", "Emiliano"), ("Álvaro", "Rodrigo"), ("Manuel", "Iván"), ("Marcos", "Josué"), ("Adrián", "Leonardo"),
         ("Alba", "Itzel"), ("Noa", "Renata"), ("Vega", "Lupita"), ("Pablo", "Jorge"), ("Martín", "Santiago"), ("Lucas", "Sebastián"), ("Carla", "Mariana"),
         ("Julia", "Fernanda"), ("Emma", "Natalia"), ("Olivia", "Paola"), ("Alejandro", "Carlos"), ("Mario", "Emilio"), ("Paula", "Andrea"), ("María", "Camila"),
         ("los gráficos", "las gráficas"), ("el gráfico", "la gráfica"), ("del gráfico", "de la gráfica"), ("este gráfico", "esta gráfica"), ("un gráfico", "una gráfica"),
         ("gráficos de barras", "gráficas de barras"), ("gráfico de barras", "gráfica de barras"), ("gráficos", "gráficas"), ("en el gráfico", "en la gráfica"),
         ("agujas", "manecillas"), ("aguja", "manecilla"), ("la esfera del reloj", "la carátula del reloj"),
         ("del colegio", "de la escuela"), ("al colegio", "a la escuela"), ("el colegio", "la escuela"), ("un colegio", "una escuela"), ("este colegio", "esta escuela"),
         ("mi colegio", "mi escuela"), ("su colegio", "su escuela"), ("coches", "carros"), ("coche", "carro"),
         ("ha durado", "duró"), ("han durado", "duraron"), ("ha tardado", "tardó"),
         ("llevadas", "reagrupaciones"), ("con llevada", "con reagrupación"), ("sin llevada", "sin reagrupación"), ("llevada", "reagrupación")]
LEAKS = ["€", "euro", "céntimo", "España", "vosotros", "habéis", "tenéis", "sabéis", "CCAA", "LOMLOE", "4.º", "5.º", "6.º", "Primaria",
         "tarta", "gominola", "chuche", "cromo", "tiza", "estuche", "bocadillo", "gafas", "folio", "ordenador", "zapatilla", "cole ", "el cole", "gorro", "nata", "judías", "tebeo", "chaqueta", "jersey", "AVE", "Renfe", "colegio", "metro de Madrid", "Galicia", "Andaluc", "Canarias", "Asturias", "Cataluña", "Comunidad",
         "Betis", "Athletic", "Real Sociedad", "Atlético", "Real Madrid", "Real Ciudad", "Teide", "Mulhacén", "Moncayo", "cucurucho", "baraja española", "Aneto", "Pirineo"]
LEAK_RE = [r"gr[áa]fico", r"\b(la|las) (una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce) menos\b", r"\bos\b", r"\bvuestr"]


def _w(s, a, b):
    if a[0].isupper():
        return re.sub(r"(?<![\wÁÉÍÓÚáéíóúñÑ])" + re.escape(a) + r"(?![\wáéíóúñ])", b, s)
    s = re.sub(r"(?<![\wÁÉÍÓÚáéíóúñÑ])" + re.escape(a) + r"(?![\wáéíóúñ])", b, s)
    A, B = a[0].upper() + a[1:], b[0].upper() + b[1:]
    return re.sub(r"(?<![\wÁÉÍÓÚáéíóúñÑ])" + re.escape(A) + r"(?![\wáéíóúñ])", B, s)


def _money(m):
    raw = m.group(1).replace(NB, "").replace(" ", "")
    if "," in raw:
        e, c = raw.split(",")
        return "$" + num(int(e)) + "." + c.ljust(2, "0")[:2]
    return "$" + num(int(raw))


def _txt(t, yr_all=False):
    """texto sin etiquetas (español de España → México)"""
    t = re.sub(r"(\d[\d" + NB + r" ]*(?:,\d+)?)[" + NB + r" ]?€", _money, t)
    t = re.sub(r"\beuros\b", "pesos", t)
    t = re.sub(r"\beuro\b", "peso", t)
    t = re.sub(r"céntimos", "centavos", t)
    t = re.sub(r"céntimo", "centavo", t)
    t = re.sub(r"(?<=\d),(?=\d)", ".", t)                                # 2,5 → 2.5
    yr = yr_all or re.search(r"nac|año|cumpl", t)
    t = re.sub(r"(?<![\d$])(?<!\d[.,:" + NB + r" ])(\d)(\d{3})(?!\d|[,:]\d)", lambda m: m.group(0) if yr and 1000 <= int(m.group(0)) <= 2100 else m.group(1) + NB + m.group(2), t)   # 4536 → 4 536（años no）
    t = re.sub(r"\b1 (unidad|decena|centena)es de millar", r"1 \1 de millar", t)
    t = re.sub(r"\b1 (decena|centena)s\b", r"1 \1", t)
    t = re.sub(r"(escala(?: de)?) 1[ " + NB + r"]?:[ " + NB + r"]?(?=\d)", r"\1 1:", t)          # escala 1 : 100 → 1:100
    t = re.sub(r"(^|\s): (1[ " + NB + r"]000|100|10)(?=:)", r"\1÷ \2", t)          # «: 1 000: 7 dm³»
    t = re.sub(r"(?<=\S) : (?=[\d(])", " ÷ ", t)                                  # 12 : 3, L : 3.14, diámetro : 2 → ÷                        # 12 : 3 → 12 ÷ 3
    t = re.sub(r"(?<=[\d)])" + NB + ":" + NB + r"(?=[\d(])", NB + "÷" + NB, t)
    t = t.replace(" y resto ", " y residuo ").replace("resto ", "residuo ").replace(" resto", " residuo")
    for a, b in WORDS:
        t = _w(t, a, b)
    t = re.sub(r"\b([Dd])e el\b", r"\1el", t)
    t = re.sub(r"\b([Aa]) el\b", r"\1l", t)
    return t


def mx_text(s):
    """convierte solo el texto fuera de las etiquetas (también el texto de los SVG)"""
    parts = re.split(r"(<[^>]*>)", s)
    yr = bool(re.search(r"nac|año|cumpl", re.sub(r"<[^>]*>", " ", s)))
    out = "".join(p if p.startswith("<") else _txt(p, yr) for p in parts)
    sp = "[ " + NB + "]"
    return re.sub(r"(</span>|\d|\)|°)(" + sp + "):(" + sp + r")(?=<span class='fr'>|\d|\()", r"\1\2÷\3", out)   # 2/5 : 1/2 → 2/5 ÷ 1/2


def ok(it):
    t = re.sub(r"<[^>]*>", " ", it["q"] + " " + " ".join(it["c"]) + " " + it["e"])
    for w in LEAKS:
        if w in t:
            return False
    for r in LEAK_RE:
        if re.search(r, t):
            return False
    return len(set(it["c"])) == 4


def mx_item(it):
    if it is None:
        return None
    it = dict(it)
    yr = bool(re.search(r"nac|año|cumpl", it["q"]))
    it["q"], it["e"] = mx_text(it["q"] if not yr else it["q"]), mx_text(it["e"] + (" <i hidden>año</i>" if yr else ""))
    it["e"] = it["e"].replace(" <i hidden>año</i>", "")
    it["c"] = [mx_text(c + (" <i hidden>año</i>" if yr else "")).replace(" <i hidden>año</i>", "") for c in it["c"]]
    labels = " ".join(re.findall(r"aria-label='([^']*)'", it["q"]))
    if not ok(it) or any(w in labels for w in ("€", "euro", "céntimo")):
        return None
    return it


def mx(maker):
    def mk():
        return mx_item(maker())
    mk.__name__ = getattr(maker, "__name__", "mk")
    return mk


def src(modname, seed, *names, lv=None, mx_=9999, dec_=True, sin_=(), rep=(), extra=(), patch=None):
    """importa un generador de España, cambia su R (y LV), filtra y pasa a México"""
    m = importlib.import_module(modname)
    if getattr(m, "_mx_seed", None) != (seed, lv):
        m.R = random.Random(seed)
        if hasattr(m, "K"):
            m.K = Kids(m.R)
        if lv is not None:
            m.LV = lv
        m._mx_seed = (seed, lv)
        m._es_seed = seed
    for k, v in (patch or {}).items():
        setattr(m, k, v)
    preds = [lim(mx_, dec=dec_)]
    if sin_:
        preds.append(sin(*sin_))
    preds.extend(extra)
    out = []
    for n in names:
        mk = keep(getattr(m, n), *preds)

        def f(mk=mk):
            it = mk()
            if it and rep:
                it = dict(it)
                for a, b in rep:
                    it["q"], it["e"] = it["q"].replace(a, b), it["e"].replace(a, b)
                    it["c"] = [c.replace(a, b) for c in it["c"]]
            return mx_item(it)
        f.__name__ = n
        out.append(f)
    return out[0] if len(out) == 1 else out


def mcq(q, correct, cands, e, neg=False):
    return ES.mcq(q, correct, cands, e, neg)


# ------------------------------------------------------------ dibujos
COIN = {50: ("50¢", 17, "#c9ced3", None), 100: ("$1", 19, "#e8c766", "#c9ced3"), 200: ("$2", 21, "#e8c766", "#c9ced3"), 500: ("$5", 23, "#e8c766", "#c9ced3"),
        1000: ("$10", 25, "#c9ced3", "#e8c766"), 2000: ("$20", 27, "#e8c766", "#c9ced3")}
BILL = {2000: ("$20", "#8ec5e8"), 5000: ("$50", "#e3a6c8"), 10000: ("$100", "#e88f8f"), 20000: ("$200", "#9fd39a"), 50000: ("$500", "#c9b58f"), 100000: ("$1 000", "#c3a6e0")}


def dinero_svg(items, label=None):
    """items: lista de valores en centavos; monedas (≤ $20 moneda) y billetes (b + valor, p. ej. 'b2000')"""
    x, H = 8, 70
    s = []
    for v in items:
        if isinstance(v, str) and v.startswith("b"):
            val = int(v[1:])
            lab, col = BILL[val]
            s.append("<rect x='%d' y='10' width='86' height='46' rx='5' fill='%s' stroke='#555' stroke-width='1.5'/>" % (x, col))
            s.append("<circle cx='%d' cy='33' r='13' fill='#ffffff' fill-opacity='0.55'/>" % (x + 62))
            s.append(text(x + 30, 39, lab.replace(" ", NB), 15, weight=700))
            x += 94
        else:
            lab, r, col, ring = COIN[v]
            cx = x + r
            if ring:
                s.append("<circle cx='%d' cy='35' r='%d' fill='%s' stroke='#555' stroke-width='1.5'/>" % (cx, r, ring))
                s.append("<circle cx='%d' cy='35' r='%d' fill='%s'/>" % (cx, r - 6, col))
            else:
                s.append("<circle cx='%d' cy='35' r='%d' fill='%s' stroke='#555' stroke-width='1.5'/>" % (cx, r, col))
            s.append(text(cx, 40, lab, 12 if r < 22 else 13, weight=700))
            x += 2 * r + 8
    W = max(x, 60)
    lab = label or "dinero: " + ", ".join((BILL[int(v[1:])][0] + " billete") if isinstance(v, str) else COIN[v][0] for v in items)
    return fig(svg_wrap(W, H, "".join(s), lab))


# ------------------------------------------------------------ la unidad
def make_unit(rnd, slug, cont, std_text, title, short_title, meta_desc, key_big, key_sub, body_html, faq, sets, sort, lv=3):
    sets = [{"title": t, "items": items} for t, items in sets]
    assert len(sets) == 5, slug
    allq = set()
    for s in sets:
        assert len(s["items"]) == 20, (slug, s["title"], len(s["items"]))
        for it in s["items"]:
            k = re.sub(r"\s+", " ", it["q"])
            assert k not in allq, ("duplicate question", slug, k)
            allq.add(k)
            for x in [it["q"], it["e"]] + it["c"]:
                assert "€" not in x and "céntimo" not in x, x
    balance(sets, rnd)
    gname = GRADE_NAME[lv]
    seo_title = "%s – %s: ejercicios de matemáticas con respuestas" % (short_title, gname)
    title, seo_title, short_title, meta_desc, key_big, key_sub = [ES.plain_text(x) for x in (title, seo_title, short_title, meta_desc, key_big, key_sub)]
    assert len(key_big) <= 36 and len(key_sub) <= 50 and len(title) <= 50, (slug, key_big, key_sub, title)
    grp, full = CONT[cont]
    write_unit("mx", "matematicas", "%d-primaria" % lv, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": grp, "standard_code": "Fase %d, %s · %s" % (FASE[lv], GRADE_SHORT[lv], full),
        "standard_url": STD_URL[lv],
        "standard_text": std_text + " (resumen de los procesos de desarrollo de aprendizaje de %s, Programa sintético de la Fase %d, SEP 2024)" % (GRADE_SHORT[lv], FASE[lv]),
        "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": [{"q": q, "a": a} for q, a in faq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def unit(slug, sort, cont, std, title, short, meta, key_big, key_sub, think, examples, mist, faq, spec, seed, pic="", lv=3):
    """spec = [(título de la serie, [(generador, número), …])] × 5"""
    R = random.Random(seed)
    seen = set()
    sets = [(t, mix(R, seen, parts)) for t, parts in spec]
    make_unit(R, slug, cont, std, title, short, meta, key_big, key_sub, lesson(think, examples, mist, pic), faq, sets, sort, lv=lv)


def bloques_mx(m, c, d, u):
    return mx_text(ES.bloques(m, c, d, u))
