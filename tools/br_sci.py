# -*- coding: utf-8 -*-
"""
Brasil / Ciências。country `br`、subject `science`（name「Ciências」）。
  grade: 1-ano〜9-ano（BNCC Ciências, Ensino Fundamental: Matéria e energia／Vida e evolução／Terra e Universo）、
         1-serie〜3-serie（BNCC Ensino Médio, Ciências da Natureza e suas Tecnologias: Física／Química／Biologia。学年への配分は一般的な教科書の順）
  単元: br_sc1（1º・2º）・br_sc3（3º・4º）・br_sc5・br_sc6・br_sc7・br_sc8・br_sc9・br_em1・br_em2・br_em3 の UNITS(grade)
  H(dom, slug, codes, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=, bank=, s4=)
    codes は BNCC のコード（EF05CI02、EM13CNT101）のリスト
    T は 3 つの表：(nome, rows, fwd, back[, extra[, match]]) か (nome, {grupo: [itens]})。grupo は「os herbívoros」の形（pertence a {g} → aos herbívoros）
    TFt は正しい文、TFf は (frase falsa, correção)、topic は「Qual afirmação sobre … é verdadeira?」の「…」
  数は 1.000（4 けたから点）、小数はコンマ、6,02 × 10²³
  python3 br_sci.py 5-ano [slug|番号 …]   seed は 75000 + 100 × n + 番号
"""
import re
import sys
import math
import copy
import importlib
from sci_common import Unit, item
from ws_common import write_unit

UPDATED = "2026-11-28"
NB = " "
GRADES = {"1-ano": 1, "2-ano": 2, "3-ano": 3, "4-ano": 4, "5-ano": 5, "6-ano": 6, "7-ano": 7, "8-ano": 8, "9-ano": 9,
          "1-serie": 10, "2-serie": 11, "3-serie": 12}
NAME = {"1-ano": "1º ano", "2-ano": "2º ano", "3-ano": "3º ano", "4-ano": "4º ano", "5-ano": "5º ano", "6-ano": "6º ano",
        "7-ano": "7º ano", "8-ano": "8º ano", "9-ano": "9º ano", "1-serie": "1ª série", "2-serie": "2ª série", "3-serie": "3ª série"}
MODULE = {"1-ano": "br_sc1", "2-ano": "br_sc1", "3-ano": "br_sc3", "4-ano": "br_sc3", "5-ano": "br_sc5", "6-ano": "br_sc6",
          "7-ano": "br_sc7", "8-ano": "br_sc8", "9-ano": "br_sc9", "1-serie": "br_em1", "2-serie": "br_em2", "3-serie": "br_em3"}
DOM = {"M": "Matéria e energia", "V": "Vida e evolução", "T": "Terra e Universo",
       "FI": "Física", "QU": "Química", "BI": "Biologia"}
STD_URL = "http://basenacionalcomum.mec.gov.br/images/BNCC_EI_EF_110518_versaofinal_site.pdf"
STD_URL_EM = "http://basenacionalcomum.mec.gov.br/images/historico/BNCC_EnsinoMedio_embaixa_site_110518.pdf"
TOPICS = {"matter", "forces-and-motion", "energy", "waves-and-light", "living-things-and-ecosystems", "earth-and-space", "earths-systems", "working-scientifically", "engineering-design"}
BAD = re.compile(r"[぀-ヿ㐀-鿿豈-﫿가-힯ßäöüœìòùîû¿¡]")
ART = {"o": ("ao", "do", "no", "pelo"), "a": ("à", "da", "na", "pela"), "os": ("aos", "dos", "nos", "pelos"), "as": ("às", "das", "nas", "pelas")}
PREP = {"a": 0, "de": 1, "em": 2, "por": 3}


def _txt(s):
    return re.sub(r"<[^>]+>", "", s)


def ok_text(s, where):
    t = _txt(s)
    assert not BAD.search(t), ("caractere", where, t[:80])
    assert "\\" not in s, where
    assert "  " not in t.strip(), ("espaços", where, t[:80])
    assert " ," not in t and " ." not in t.replace(" …", ""), ("pontuação", where, t[:80])
    assert "\"" not in t and "'" not in t, ("aspas", where, t[:80])
    assert not re.search(r" [?!;]| :(?! )", t), ("espaço", where, t[:80])
    assert not re.search(r"(^|[ («>])([Dd]e|[Ee]m|[Pp]or|a) (o|a|os|as) ", t), ("contração", where, t[:80])
    assert not re.search(r"\b([a-záéíóúâêôãõç]{2,}) \1\b", t, re.I), ("palavra repetida", where, t[:80])
    return s


def _contr(m):
    p, a = m.group(2), m.group(3)
    out = ART[a][PREP[p.lower()]]
    if p[0].isupper():
        out = out[0].upper() + out[1:]
    return m.group(1) + out + " "


def esc(t):
    t = re.sub(r"(^|[ («>])(de|em|por|a|De|Em|Por) (o|a|os|as) ", _contr, t)
    return t.replace("< ", "&lt; ").replace(" >", " &gt;").replace("...", "…")


def it(q, a, wrong, e):
    if len({x.strip().lower() for x in [a] + list(wrong)}) < 4:
        return None
    return item(q, a, list(wrong), e)


# ------------------------------------------------------------ números（vírgula decimal, ponto de milhar a partir de 1.000）
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _br(s):
    neg = s.startswith("-")
    s = s.lstrip("-")
    a, _, b = s.partition(".")
    if len(a) >= 4:
        g = []
        while a:
            g.insert(0, a[-3:])
            a = a[:-3]
        a = ".".join(g)
    return ("−" if neg else "") + a + ("," + b if b else "")


def sci(x, d=3):
    m, e = (("%." + str(d - 1) + "e") % x).split("e")
    m = m.rstrip("0").rstrip(".") if "." in m else m
    return "%s × 10%s" % (_br(m), str(int(e)).translate(SUP))


def num(x, d=3):
    """d algarismos significativos（sem zeros finais）。≥ 10⁶ ou < 10⁻³ em notação científica"""
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
    return _br(s)


def nq(q, ans, wrongs, unit, e, d=3, neg=False):
    """resposta numérica。wrongs = erros típicos（iguais, negativos e zero são retirados）。menos de 3 → None"""
    a = num(ans, d)
    out = []
    for w in wrongs:
        if w is None:
            continue
        try:
            s = num(w, d)
        except (TypeError, ValueError, OverflowError, ZeroDivisionError):
            continue
        if s != a and s not in out and (neg or not s.startswith("−")) and s != "0":
            out.append(s)
    if len(out) < 3:
        return None
    u = ("" if unit in ("°", "%") else NB) + unit if unit else ""
    return it(q, a + u, [x + u for x in out[:3]], e)


def gq(s):
    return "“" + s + "”"


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
                    return it("Qual par está correto?", k + sep + v, [a + sep + b for a, b in w], dot((fe or "{k}: {v}").format(k=k, v=v)))
                b = bad_pairs(1)
                if not b:
                    return None
                bk, bv = b[0]
                ok = [p for p in rows if p[0] != bk]
                if len(ok) < 3:
                    return None
                w = R.R.sample(ok, 3)
                right = [vv for kk, vv in rows if kk == bk]
                return it("Qual par está errado?", bk + sep + bv, [a + sep + c for a, c in w], dot("O par correto é: %s – %s" % (bk, right[0])))
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

    def G(self, groups, pos="Qual destes pertence a {g}?", neg="Qual destes não pertence a {g}?"):
        R = self
        names = sorted(groups)

        def mk():
            g = R.R.choice(names)
            mine = groups[g]
            other = [(h, x) for h in names if h != g for x in groups[h] if x not in mine]
            if neg and R.R.random() < 0.4 and len(mine) >= 3:
                h, a = R.R.choice(other)
                return it(neg.format(g=g), a, R.R.sample(mine, 3), "%s pertence a %s." % (gq(a), h))
            a = R.R.choice(mine)
            ws = sorted({x for _, x in other})
            if len(ws) < 3:
                return None
            return it(pos.format(g=g), a, R.R.sample(ws, 3), "%s pertence a %s." % (gq(a), g))
        return mk

    def TF(self, true, false, topic):
        R = self

        def mk():
            if R.R.random() < 0.5:
                a = R.R.choice(true)
                w = [f for f, _ in R.R.sample(false, 3)]
                stem = R.R.choice(["Qual afirmação sobre %s é verdadeira?", "Qual frase sobre %s está correta?"]) % topic
                return it(stem, a, w, a)
            f, c = R.R.choice(false)
            w = R.R.sample(true, 3)
            stem = R.R.choice(["Qual afirmação sobre %s é falsa?", "Qual frase sobre %s está errada?"]) % topic
            return it(stem, f, w, "A frase %s é falsa. %s" % (gq(f.rstrip(".")), c))
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


def H(dom, slug, codes, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=None, bank=None, s4=None):
    assert len(T) == 3 and tp in TOPICS and dom in DOM, slug
    assert codes and all(re.match(r"^(EF0\dCI\d\d|EM13CNT\d{3})$", c) for c in codes), (slug, codes)
    for s in TFt + [a for a, _ in TFf]:
        assert s.endswith("."), (slug, s)

    def part(K_, t):
        if isinstance(t[1], dict):
            return K_.G(t[1])
        name, rows, fwd, back = t[:4]
        return K_.P(rows, fwd, back, extra=t[4] if len(t) > 4 else (), match=t[5] if len(t) > 5 else True, fe=t[6] if len(t) > 6 else None)

    def sets(K_):
        out = [(t[0], [(part(K_, t), 20)]) for t in T]
        if calc:
            mix = [(K_.F(calc), 15), (part(K_, T[1]), 5)]
        elif bank:
            n = min(20, len(bank) - 3)
            mix = [(K_.B(bank), n)] + ([(part(K_, T[1]), 20 - n)] if n < 20 else [])
        else:
            mix = [(part(K_, T[0]), 7), (part(K_, T[1]), 7), (part(K_, T[2]), 6)]
        out.append((s4 or ("Calcule e aplique" if calc else "Exercícios variados"), mix))
        out.append(("Verdadeiro ou falso?", [(K_.TF(TFt, TFf, topic), 20)]))
        return out
    return dict(dom=dom, slug=slug, codes=codes, title=title, short=short, std=std, what=what, kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, tp=tp)


def seed_of(n, sort):
    return 75000 + 100 * n + sort


def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ("<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead>"
            "<tbody>%s</tbody></table></div>" % (h, b))


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Exemplo</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Resposta: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist):
    h = "<h2>Como pensar</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += "".join(examples)
    h += "<h2>Erros comuns</h2>" + table(["Erro comum", "Lembre-se"], mist)
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
    u = dict(u, title=esc(u["title"]), short=esc(u["short"]), kb=esc(u["kb"]), ks=esc(u["ks"]), std=esc(u["std"]), what=esc(u["what"]))
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["std"], u["what"], body) + tuple(a + b for a, b in fq):
        ok_text(s, u["slug"])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["what"]):
        assert "<" not in s and "&lt;" not in s and "&gt;" not in s, s
    lim = (40, 40, 100) if n <= 2 else (60, 60, 150)
    assert len(u["title"]) <= lim[0] and len(u["kb"]) <= lim[1] and len(u["ks"]) <= lim[2], (u["slug"], len(u["title"]), len(u["kb"]), len(u["ks"]))
    d = u["dom"]
    dom = DOM[d]
    gname = NAME[grade]
    if n <= 9:
        assert d in ("M", "V", "T"), u["slug"]
        code = "BNCC Ciências · %s" % ", ".join(u["codes"])
        tail = " (síntese das habilidades da BNCC de Ciências, %s do Ensino Fundamental, unidade temática %s)" % (gname, dom)
        url = STD_URL
        sj = "Ciências"
        seo = "%s – Ciências %s: atividades com gabarito" % (u["short"], gname)
        where = "Ciências do %s" % gname
    else:
        assert d in ("FI", "QU", "BI"), u["slug"]
        code = "BNCC Ensino Médio · Ciências da Natureza · %s" % ", ".join(u["codes"])
        tail = " (síntese das habilidades da BNCC de Ciências da Natureza e suas Tecnologias para o Ensino Médio; %s, %s)" % (dom.lower(), gname)
        url = STD_URL_EM
        sj = dom
        seo = "%s – %s %s do Ensino Médio: atividades com gabarito" % (u["short"], dom, gname)
        where = "%s da %s do Ensino Médio" % (dom, gname)
    write_unit("br", "science", grade, {
        "slug": u["slug"], "title": u["title"], "seo_title": seo,
        "short_title": u["short"], "domain": dom, "standard_code": code,
        "standard_url": url, "standard_text": u["std"] + tail,
        "meta_desc": "%s em %s: %s. 100 exercícios corrigidos na hora, com explicações, e uma atividade para imprimir com gabarito." % (u["short"], where, u["what"]),
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
    import br_sci
    br_sci.main()
