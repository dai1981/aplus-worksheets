# -*- coding: utf-8 -*-
"""
Italia / Scienze。country `it`、subject `science`（name「Scienze」）。
  grade: classe-prima〜classe-quinta（scuola primaria）、prima-media〜terza-media（Indicazioni nazionali per il curricolo 2012, scienze）、
         prima-liceo〜quinta-liceo（liceo scientifico: Fisica e Scienze naturali（Biologia, Chimica, Scienze della Terra）, DM 211/2010）
  単元: it_sc1（classe prima・seconda）・it_sc3（terza・quarta）・it_sc5（quinta）・it_sc6〜it_sc8（media）・it_sc9〜it_sc13（liceo）の UNITS(grade)
  H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=, bank=, s4=)
    T は 3 つの表：(nome della serie, rows, fwd, back[, extra[, match]]) か (nome, {gruppo: [elementi]})。gruppo は「gli erbivori」の形（appartiene a {g} → agli erbivori）
    TFt は正しい文、TFf は (frase falsa, correzione)、topic は「Quale affermazione su … è vera?」の「…」（su + articolo は自動で縮約）
  アポストロフィは ’（文字に挟まれた ' は esc が ’ に直す）。数は 1000 / 12 000（ノーブレークスペース）、小数はコンマ、6,02 × 10²³
  python3 it_sci.py classe-terza [slug|番号 …]   seed は 79000 + 100 × n + 番号
"""
import re
import sys
import math
import copy
import importlib
from sci_common import Unit, item
from ws_common import write_unit
import it_common

UPDATED = "2026-11-28"
NB = " "
GRADES = {"classe-prima": 1, "classe-seconda": 2, "classe-terza": 3, "classe-quarta": 4, "classe-quinta": 5,
          "prima-media": 6, "seconda-media": 7, "terza-media": 8,
          "prima-liceo": 9, "seconda-liceo": 10, "terza-liceo": 11, "quarta-liceo": 12, "quinta-liceo": 13}
NAME = {"classe-prima": "classe prima", "classe-seconda": "classe seconda", "classe-terza": "classe terza", "classe-quarta": "classe quarta",
        "classe-quinta": "classe quinta", "prima-media": "prima media", "seconda-media": "seconda media", "terza-media": "terza media",
        "prima-liceo": "prima liceo", "seconda-liceo": "seconda liceo", "terza-liceo": "terza liceo", "quarta-liceo": "quarta liceo", "quinta-liceo": "quinta liceo"}
MODULE = {"classe-prima": "it_sc1", "classe-seconda": "it_sc1", "classe-terza": "it_sc3", "classe-quarta": "it_sc3", "classe-quinta": "it_sc5",
          "prima-media": "it_sc6", "seconda-media": "it_sc7", "terza-media": "it_sc8",
          "prima-liceo": "it_sc9", "seconda-liceo": "it_sc10", "terza-liceo": "it_sc11", "quarta-liceo": "it_sc12", "quinta-liceo": "it_sc13"}
DOM = {"O": "Esplorare e descrivere oggetti e materiali", "O5": "Oggetti, materiali e trasformazioni", "S": "Osservare e sperimentare sul campo",
       "U": "L’uomo, i viventi e l’ambiente",
       "FC": "Fisica e chimica", "AT": "Astronomia e scienze della Terra", "B": "Biologia",
       "FI": "Fisica", "BI": "Biologia", "CH": "Chimica", "ST": "Scienze della Terra"}
TOPICS = {"matter", "forces-and-motion", "energy", "waves-and-light", "living-things-and-ecosystems", "earth-and-space", "earths-systems", "working-scientifically", "engineering-design"}
BAD = re.compile(r"[぀-ヿ㐀-鿿豈-﫿가-힯ßäüçœñêîôû¿¡]")
ART = r"(il|lo|la|i|gli|le)"
PREP = {"di": "de", "a": "a", "da": "da", "in": "ne", "su": "su"}
ARTF = {"il": "l", "lo": "llo", "la": "lla", "i": "i", "gli": "gli", "le": "lle"}


def _txt(s):
    return re.sub(r"<[^>]+>", "", s)


def ok_text(s, where):
    t = _txt(s)
    assert not BAD.search(t), ("carattere", where, t[:80])
    assert "\\" not in s, where
    assert "  " not in t.strip(), ("spazi", where, t[:80])
    assert " ," not in t and " ." not in t.replace(" …", ""), ("punteggiatura", where, t[:80])
    assert "\"" not in t and "'" not in t, ("virgolette", where, t[:80])
    assert not re.search(r" [?!;]| :(?! )", t), ("spazio", where, t[:80])
    assert not re.search(r"\b([Dd]i|[Aa]|[Dd]a|[Ii]n|[Ss]u) (il|lo|la|i|gli|le|l’) ", t), ("preposizione articolata", where, t[:80])
    return s


def nbn(t):
    """5 cifre o più: gruppi con spazio（4 cifre unite）"""
    return re.sub(r"(?<![\d,])(\d{1,3})((?: \d{3})+)(?![\d,])", lambda m: m.group(1) + m.group(2).replace(" ", NB) if len(m.group(1) + m.group(2).replace(" ", "")) >= 5 else m.group(0), t)


def _contr(m):
    p, a = m.group(2), m.group(3)
    base = PREP[p.lower()]
    out = base + ARTF[a.lower()]
    if p[0].isupper():
        out = out[0].upper() + out[1:]
    return m.group(1) + out + " "


def esc(t):
    t = re.sub(r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ])", "’", t)
    t = re.sub(r"(^|[ («>])(di|a|da|in|su|Di|A|Da|In|Su) " + ART + " ", _contr, t)
    t = re.sub(r"(^|[ («>])(di|a|da|in|su|Di|A|Da|In|Su) l’", lambda m: m.group(1) + (PREP[m.group(2).lower()] if m.group(2).islower() else PREP[m.group(2).lower()].capitalize()) + "ll’", t)
    t = nbn(t)
    return t.replace("< ", "&lt; ").replace(" >", " &gt;").replace("...", "…")


def it(q, a, wrong, e):
    if len({x.strip().lower() for x in [a] + list(wrong)}) < 4:
        return None
    return item(q, a, list(wrong), e)


# ------------------------------------------------------------ numeri（virgola decimale, spazio da 10 000）
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _it(s):
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
    return "%s × 10%s" % (_it(m), str(int(e)).translate(SUP))


def num(x, d=3):
    """d cifre significative（senza zeri finali）。≥ 10⁶ o < 10⁻³ in notazione scientifica"""
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
    return _it(s)


def nq(q, ans, wrongs, unit, e, d=3, neg=False):
    """risposta numerica。wrongs = errori tipici（uguali, negativi e zero si tolgono）。meno di 3 → None"""
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
    u = ("" if unit == "°" else NB) + unit if unit else ""
    return it(q, a + u, [x + u for x in out[:3]], e)


def gq(s):
    return "«" + s + "»"


# ------------------------------------------------------------ parti
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
                    return it("Quale coppia è corretta?", k + sep + v, [a + sep + b for a, b in w], dot((fe or "{k}: {v}").format(k=k, v=v)))
                b = bad_pairs(1)
                if not b:
                    return None
                bk, bv = b[0]
                ok = [p for p in rows if p[0] != bk]
                if len(ok) < 3:
                    return None
                w = R.R.sample(ok, 3)
                right = [vv for kk, vv in rows if kk == bk]
                return it("Quale coppia è sbagliata?", bk + sep + bv, [a + sep + c for a, c in w], dot("La coppia corretta è: %s – %s" % (bk, right[0])))
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

    def G(self, groups, pos="Quale appartiene a {g}?", neg="Quale non appartiene a {g}?"):
        R = self
        names = sorted(groups)

        def mk():
            g = R.R.choice(names)
            mine = groups[g]
            other = [(h, x) for h in names if h != g for x in groups[h] if x not in mine]
            if neg and R.R.random() < 0.4 and len(mine) >= 3:
                h, a = R.R.choice(other)
                return it(neg.format(g=g), a, R.R.sample(mine, 3), "%s appartiene a %s." % (gq(a), h))
            a = R.R.choice(mine)
            ws = sorted({x for _, x in other})
            if len(ws) < 3:
                return None
            return it(pos.format(g=g), a, R.R.sample(ws, 3), "%s appartiene a %s." % (gq(a), g))
        return mk

    def TF(self, true, false, topic):
        R = self

        def mk():
            if R.R.random() < 0.5:
                a = R.R.choice(true)
                w = [f for f, _ in R.R.sample(false, 3)]
                stem = R.R.choice(["Quale affermazione su %s è vera?", "Quale frase su %s è corretta?"]) % topic
                return it(stem, a, w, a)
            f, c = R.R.choice(false)
            w = R.R.sample(true, 3)
            stem = R.R.choice(["Quale affermazione su %s è falsa?", "Quale frase su %s è sbagliata?"]) % topic
            return it(stem, f, w, "La frase %s è falsa. %s" % (gq(f.rstrip(".")), c))
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
        out.append((s4 or ("Calcola e applica" if calc else "Esercizi misti"), mix))
        out.append(("Vero o falso?", [(K_.TF(TFt, TFf, topic), 20)]))
        return out
    return dict(dom=dom, slug=slug, title=title, short=short, std=std, what=what, kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, tp=tp)


def seed_of(n, sort):
    return 79000 + 100 * n + sort


def subj(n, d):
    if n <= 8:
        return "Scienze"
    return DOM[d]


def table(head, rows):
    h = "".join("<th>%s</th>" % c for c in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return ("<div class='sn-tw'><table class='sn-table'><thead><tr>%s</tr></thead>"
            "<tbody>%s</tbody></table></div>" % (h, b))


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Esempio</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Risposta: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist):
    h = "<h2>Come si ragiona</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += "".join(examples)
    h += "<h2>Errori frequenti</h2>" + table(["Errore frequente", "Da ricordare"], mist)
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
    if d == "O" and n >= 4:
        d = "O5"
    dom = DOM[d]
    sj = subj(n, d)
    gname = NAME[grade]
    if n <= 5:
        assert d in ("O", "O5", "S", "U"), u["slug"]
        code = "Indicazioni nazionali · Scienze, scuola primaria · %s" % dom
        tail = " (sintesi degli obiettivi di apprendimento di scienze al termine della classe %s della scuola primaria, Indicazioni nazionali per il curricolo 2012)" % ("terza" if n <= 3 else "quinta")
        url = it_common.STD_URL
    elif n <= 8:
        assert d in ("FC", "AT", "B"), u["slug"]
        code = "Indicazioni nazionali · Scienze, secondaria di primo grado · %s" % dom
        tail = " (sintesi degli obiettivi di apprendimento di scienze al termine della scuola secondaria di primo grado, Indicazioni nazionali per il curricolo 2012)"
        url = it_common.STD_URL
    else:
        assert d in ("FI", "BI", "CH", "ST"), u["slug"]
        area = "Fisica" if d == "FI" else "Scienze naturali (%s)" % dom
        code = "Indicazioni nazionali per i licei · %s" % area
        tail = " (sintesi degli obiettivi specifici di apprendimento di %s del liceo scientifico, %s, DM 211/2010)" % ("fisica" if d == "FI" else "scienze naturali", gname)
        url = it_common.STD_URL_LICEI
    seo = "%s – %s %s: schede ed esercizi con soluzioni" % (u["short"], sj, gname)
    write_unit("it", "science", grade, {
        "slug": u["slug"], "title": u["title"], "seo_title": seo,
        "short_title": u["short"], "domain": dom, "standard_code": code,
        "standard_url": url, "standard_text": u["std"] + tail,
        "meta_desc": "%s in %s (%s): %s. 100 esercizi corretti online con spiegazioni e una scheda da stampare con le soluzioni." % (u["short"], sj, gname, u["what"]),
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
    import it_sci
    it_sci.main()
