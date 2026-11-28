# -*- coding: utf-8 -*-
"""
España / Ciencias。country `es`、subject `science`（name「Ciencias」）。LOMLOE。
  grade: 1-primaria〜6-primaria（Conocimiento del Medio Natural, Social y Cultural, RD 157/2022。理科の部分だけ）、
         1-eso〜4-eso（Biología y Geología・Física y Química, RD 217/2022）、
         1-bachillerato・2-bachillerato（Biología, Geología y Ciencias Ambientales・Física y Química／Biología・Química・Física・Geología y Ciencias Ambientales, RD 243/2022）
  単元: es_sc1（1.º・2.º）・es_sc3（3.º・4.º）・es_sc5（5.º・6.º）・es_sc7・es_sc8・es_sc9・es_sc10・es_sc11・es_sc12 の UNITS(grade)
  H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=, bank=, s4=)
    T は 3 つの表：(nombre de la serie, rows, fwd, back[, extra[, match]]) か (nombre, {grupo: [elementos]})。grupo は「los herbívoros」の形（pertenece a {g}）
    TFt は正しい文、TFf は (frase falsa, corrección)、topic は「¿Qué afirmación sobre … es verdadera?」の「…」
  python3 es_sci.py 3-primaria [slug|番号 …]   seed は 78000 + 100 × n + 番号
"""
import re
import sys
import math
import copy
import importlib
from sci_common import Unit, item
from ws_common import write_unit
import es_common

UPDATED = "2026-11-28"
NB = " "
GRADES = {"1-primaria": 1, "2-primaria": 2, "3-primaria": 3, "4-primaria": 4, "5-primaria": 5, "6-primaria": 6,
          "1-eso": 7, "2-eso": 8, "3-eso": 9, "4-eso": 10, "1-bachillerato": 11, "2-bachillerato": 12}
NAME = {"1-primaria": "1.º de Primaria", "2-primaria": "2.º de Primaria", "3-primaria": "3.º de Primaria", "4-primaria": "4.º de Primaria",
        "5-primaria": "5.º de Primaria", "6-primaria": "6.º de Primaria", "1-eso": "1.º de ESO", "2-eso": "2.º de ESO", "3-eso": "3.º de ESO",
        "4-eso": "4.º de ESO", "1-bachillerato": "1.º de Bachillerato", "2-bachillerato": "2.º de Bachillerato"}
MODULE = {"1-primaria": "es_sc1", "2-primaria": "es_sc1", "3-primaria": "es_sc3", "4-primaria": "es_sc3", "5-primaria": "es_sc5", "6-primaria": "es_sc5",
          "1-eso": "es_sc7", "2-eso": "es_sc8", "3-eso": "es_sc9", "4-eso": "es_sc10", "1-bachillerato": "es_sc11", "2-bachillerato": "es_sc12"}
DOM = {"V": "La vida en nuestro planeta", "M": "Materia, fuerzas y energía", "A": "Iniciación en la actividad científica", "T": "Tecnología y digitalización",
       "B": "Biología y Geología", "F": "Física y Química",
       "BG": "Biología, Geología y Ciencias Ambientales", "FQ": "Física y Química", "BI": "Biología", "Q": "Química", "FI": "Física", "GC": "Geología y Ciencias Ambientales"}
CICLO = {1: "primer ciclo", 2: "primer ciclo", 3: "segundo ciclo", 4: "segundo ciclo", 5: "tercer ciclo", 6: "tercer ciclo"}
STD_URL = {"P": es_common.STD_URL, "E": es_common.STD_URL_ESO, "B": es_common.STD_URL_BACH}
TOPICS = {"matter", "forces-and-motion", "energy", "waves-and-light", "living-things-and-ecosystems", "earth-and-space", "earths-systems", "working-scientifically", "engineering-design"}
BAD = re.compile(r"[぀-ヿ㐀-鿿豈-﫿가-힯ßäöàèùêîôûçœ]")


def _txt(s):
    return re.sub(r"<[^>]+>", "", s)


def ok_text(s, where):
    t = _txt(s)
    assert not BAD.search(t), ("carácter", where, t[:80])
    assert "\\" not in s, where
    assert "  " not in t.strip(), ("espacios", where, t[:80])
    assert " ," not in t and " ." not in t.replace(" …", ""), ("puntuación", where, t[:80])
    assert "\"" not in t and "'" not in t, ("comillas", where, t[:80])
    assert not re.search(r" [?!;]| :(?! )", t), ("espacio", where, t[:80])
    assert t.count("?") == t.count("¿") and t.count("!") == t.count("¡"), ("signos", where, t[:80])
    assert not re.search(r"\b(a|de) el ", t), ("contracción", where, t[:80])
    return s


def nbn(t):
    """5 cifras o más: grupos con espacio fino（4 cifras juntas, como en RAE）"""
    return re.sub(r"(?<![\d,])(\d{1,3})((?: \d{3})+)(?![\d,])", lambda m: m.group(1) + m.group(2).replace(" ", NB) if len(m.group(1) + m.group(2).replace(" ", "")) >= 5 else m.group(0), t)


def esc(t):
    t = re.sub(r"(^|[ (])([Aa]) el ", r"\1\2l ", t)
    t = re.sub(r"(^|[ (])([Dd])e el ", r"\1\2el ", t)
    t = nbn(t)
    return t.replace("< ", "&lt; ").replace(" >", " &gt;").replace("...", "…")


def it(q, a, wrong, e):
    if len({x.strip().lower() for x in [a] + list(wrong)}) < 4:
        return None
    return item(q, a, list(wrong), e)


# ------------------------------------------------------------ números（coma decimal, espacio a partir de 10 000）
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _es(s):
    neg = s.startswith("-")
    s = s.lstrip("-")
    a, _, b = s.partition(".")
    if len(a) >= 5:
        g = []
        while a:
            g.insert(0, a[-3:])
            a = a[:-3]
        a = NB.join(g)
    return ("−" if neg else "") + a + ("," + b if b else "")


def sci(x, d=3):
    m, e = (("%." + str(d - 1) + "e") % x).split("e")
    m = m.rstrip("0").rstrip(".") if "." in m else m
    return "%s · 10%s" % (_es(m), str(int(e)).translate(SUP))


def num(x, d=3):
    """d cifras significativas（sin ceros finales）。≥ 10⁶ o < 10⁻³ en notación científica"""
    if x != 0 and (abs(x) >= 1e6 or abs(x) < 1e-3):
        return sci(x, d)
    if isinstance(x, int) or float(x).is_integer():
        s = str(int(round(x)))
    elif abs(x) >= 10 ** (d - 1):
        e = int(math.floor(math.log10(abs(x))))
        s = str(int(round(x, d - 1 - e)))
    else:
        s = ("%." + str(d) + "g") % x
        if "e" in s:
            s = (("%." + str(d) + "f") % x).rstrip("0").rstrip(".")
    return _es(s)


def nq(q, ans, wrongs, unit, e, d=3, neg=False):
    """respuesta numérica。wrongs = errores típicos（iguales, negativos y cero se quitan）。menos de 3 → None"""
    a = num(ans, d)
    out = []
    for w in wrongs:
        if w is None:
            continue
        try:
            s = num(w, d)
        except (TypeError, ValueError, OverflowError):
            continue
        if s != a and s not in out and (neg or not s.startswith("−")) and s != "0":
            out.append(s)
    if len(out) < 3:
        return None
    u = ("" if unit == "°" else NB) + unit if unit else ""
    return it(q, a + u, [x + u for x in out[:3]], e)


def gq(s):
    return "«" + s + "»"


# ------------------------------------------------------------ partes
class K:
    def __init__(self, R):
        self.R = R

    def P(self, rows, fwd, back=None, fe=None, be=None, match=True, sep=" – ", extra=()):
        R = self
        tag = {}
        for r in rows:
            tag[(r[0], r[1])] = r[2] if len(r) > 2 else None
        rows = [(r[0], r[1]) for r in rows]
        tk = {r[0]: tag[r] for r in rows}
        tv = {r[1]: tag[r] for r in rows}
        keys = sorted({k for k, _ in rows})
        vals = sorted({v for _, v in rows})
        good = set(rows)

        def bad_pairs(n):
            out = set()
            for _ in range(80):
                k = R.R.choice(keys)
                v = R.R.choice([x for x in vals if tv[x] == tk[k]])
                if (k, v) not in good:
                    out.add((k, v))
                if len(out) >= n:
                    break
            return sorted(out)

        def dot(e):
            e = e if e.endswith((".", "!", "?")) else e + "."
            return e[0].upper() + e[1:]

        def mk():
            k, v = R.R.choice(rows)
            t = tag[(k, v)]
            same = {vv for kk, vv in rows if kk == k}
            r = R.R.random()
            if match and r < 0.25 and len(rows) >= 4:
                if R.R.random() < 0.5:
                    w = bad_pairs(3)
                    if len(w) < 3 or len({a for a, _ in w} | {k}) < 4:
                        return None
                    return it("¿Qué pareja es correcta?", k + sep + v, [a + sep + b for a, b in w], dot((fe or "{k}: {v}").format(k=k, v=v)))
                b = bad_pairs(1)
                if not b:
                    return None
                bk, bv = b[0]
                ok = [p for p in rows if p[0] != bk]
                if len(ok) < 3:
                    return None
                w = R.R.sample(ok, 3)
                right = [vv for kk, vv in rows if kk == bk]
                return it("¿Qué pareja es incorrecta?", bk + sep + bv, [a + sep + c for a, c in w], dot("La pareja correcta es: %s – %s" % (bk, right[0])))
            if back and r < 0.6:
                kk = {a for a, b in rows if b == v}
                w = [x for x in keys if x not in kk and tk[x] == t]
                if len(w) < 3:
                    return None
                return it(back.format(v=v), k, R.R.sample(w, 3), dot((be or fe or "{k}: {v}").format(k=k, v=v)))
            w = [x for x in vals if x not in same and tv[x] == t] + [x for x in extra if x not in same]
            if len(w) < 3:
                return None
            return it(fwd.format(k=k), v, R.R.sample(w, 3), dot((fe or "{k}: {v}").format(k=k, v=v)))
        return mk

    def G(self, groups, pos="¿Cuál pertenece a {g}?", neg="¿Cuál no pertenece a {g}?"):
        R = self
        names = sorted(groups)

        def mk():
            g = R.R.choice(names)
            mine = groups[g]
            other = [(h, x) for h in names if h != g for x in groups[h] if x not in mine]
            if neg and R.R.random() < 0.4 and len(mine) >= 3:
                h, a = R.R.choice(other)
                return it(neg.format(g=g), a, R.R.sample(mine, 3), "%s pertenece a %s." % (gq(a), h))
            a = R.R.choice(mine)
            ws = sorted({x for _, x in other})
            if len(ws) < 3:
                return None
            return it(pos.format(g=g), a, R.R.sample(ws, 3), "%s pertenece a %s." % (gq(a), g))
        return mk

    def TF(self, true, false, topic):
        R = self

        def mk():
            if R.R.random() < 0.5:
                a = R.R.choice(true)
                w = [f for f, _ in R.R.sample(false, 3)]
                stem = R.R.choice(["¿Qué afirmación sobre %s es verdadera?", "¿Qué frase sobre %s es correcta?"]) % topic
                return it(stem, a, w, a)
            f, c = R.R.choice(false)
            w = R.R.sample(true, 3)
            stem = R.R.choice(["¿Qué afirmación sobre %s es falsa?", "¿Qué frase sobre %s es incorrecta?"]) % topic
            return it(stem, f, w, "La frase %s es falsa. %s" % (gq(f.rstrip(".")), c))
        return mk

    def B(self, rows):
        its = [it(*r) for r in rows]
        R = self

        def mk():
            return copy.deepcopy(R.R.choice(its))
        mk.n = len(its)
        return mk

    def F(self, fn):
        R = self

        def mk():
            return fn(R.R)
        return mk



def H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=None, bank=None, s4=None):
    assert len(T) == 3 and tp in TOPICS and dom in DOM, slug
    for s in TFt + [a for a, _ in TFf]:
        assert s.endswith("."), (slug, s)

    def part(K_, t):
        if isinstance(t[1], dict):
            return K_.G(t[1])
        name, rows, fwd, back = t[:4]
        return K_.P(rows, fwd, back, extra=t[4] if len(t) > 4 else (), match=t[5] if len(t) > 5 else True)

    def sets(K_):
        out = [(t[0], [(part(K_, t), 20)]) for t in T]
        if calc:
            mix = [(K_.F(calc), 15), (part(K_, T[1]), 5)]
        elif bank:
            n = min(20, len(bank) - 3)
            mix = [(K_.B(bank), n)] + ([(part(K_, T[1]), 20 - n)] if n < 20 else [])
        else:
            mix = [(part(K_, T[0]), 7), (part(K_, T[1]), 7), (part(K_, T[2]), 6)]
        out.append((s4 or ("Calcula y aplica" if calc else "Ejercicios variados"), mix))
        out.append(("¿Verdadero o falso?", [(K_.TF(TFt, TFf, topic), 20)]))
        return out
    return dict(dom=dom, slug=slug, title=title, short=short, std=std, what=what, kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, tp=tp)


def seed_of(n, sort):
    return 78000 + 100 * n + sort


def subj(n, d):
    if n <= 6:
        return "Conocimiento del Medio"
    return DOM[d]


def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ("<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead>"
            "<tbody>%s</tbody></table></div>" % (h, b))


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Ejemplo</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Respuesta: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist):
    h = "<h2>Cómo se piensa</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += "".join(examples)
    h += "<h2>Errores frecuentes</h2>" + table(["Error frecuente", "Lo que hay que recordar"], mist)
    return h


def build(grade, u, sort):
    n = GRADES[grade]
    U_ = Unit(seed_of(n, sort))
    sets = U_.sets(u["sets"](K(U_.R)))
    for s in sets:
        s["title"] = esc(s["title"])
        for x in s["items"]:
            x["q"], x["e"] = esc(x["q"]), esc(x["e"])
            x["c"] = [esc(c) for c in x["c"]]
            for t in [x["q"], x["e"]] + x["c"]:
                ok_text(t, u["slug"])
    ex = [example(esc(q), [esc(t) for t in st], esc(a)) for q, st, a in u["ex"]]
    body = lesson([esc(t) for t in u["think"]], ex, [(esc(a), esc(b)) for a, b in u["mist"]])
    fq = [(esc(q), esc(a)) for q, a in u["faq"]]
    u = dict(u, kb=nbn(u["kb"]), ks=nbn(u["ks"]), std=nbn(u["std"]), what=nbn(u["what"]))
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["std"], u["what"], body) + tuple(a + b for a, b in fq):
        ok_text(s, u["slug"])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["what"]):
        assert "<" not in s, s
    lim = (40, 40, 100) if n <= 2 else (60, 60, 150)
    assert len(u["title"]) <= lim[0] and len(u["kb"]) <= lim[1] and len(u["ks"]) <= lim[2], (u["slug"], len(u["title"]), len(u["kb"]), len(u["ks"]))
    d = u["dom"]
    dom = DOM[d]
    sj = subj(n, d)
    gname = NAME[grade]
    if n <= 6:
        code = "LOMLOE Primaria (%s) · %s" % (CICLO[n], dom)
        tail = " (resumen de los saberes básicos de Conocimiento del Medio Natural, Social y Cultural, %s, Real Decreto 157/2022)" % CICLO[n]
        url = STD_URL["P"]
    elif n <= 10:
        code = "LOMLOE ESO · %s" % dom
        tail = " (resumen de los saberes básicos de %s, Real Decreto 217/2022)" % dom
        url = STD_URL["E"]
    else:
        code = "LOMLOE Bachillerato · %s" % dom
        tail = " (resumen de los saberes básicos de %s de %s, Real Decreto 243/2022)" % (dom, gname)
        url = STD_URL["B"]
    seo = "%s – %s %s: fichas con soluciones" % (u["short"], sj, gname)
    write_unit("es", "science", grade, {
        "slug": u["slug"], "title": u["title"], "seo_title": seo,
        "short_title": u["short"], "domain": dom, "standard_code": code,
        "standard_url": url, "standard_text": u["std"] + tail,
        "meta_desc": "%s en %s (%s): %s. 100 ejercicios resueltos en línea con explicaciones y una ficha para imprimir con soluciones." % (u["short"], sj, gname, u["what"]),
        "key_big": u["kb"], "key_sub": u["ks"], "body_html": body,
        "faq": [{"q": q, "a": a} for q, a in fq], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


def units(grade):
    m = importlib.import_module(MODULE[grade])
    return m.UNITS(grade)


def main():
    grade = sys.argv[1]
    only = sys.argv[2:]
    for i, u in enumerate(units(grade)):
        if only and u["slug"] not in only and str(i + 1) not in only:
            continue
        build(grade, u, i + 1)
        print("wrote", grade, u["slug"])


if __name__ == "__main__":
    import es_sci
    es_sci.main()
