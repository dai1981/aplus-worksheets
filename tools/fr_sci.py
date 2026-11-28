# -*- coding: utf-8 -*-
"""
France / Sciences。country `fr`、subject `science`（name「Sciences」）。
  grade: cp・ce1・ce2（Questionner le monde du vivant, de la matière et des objets、programme de sciences et technologie du cycle 2, BO n° 24 du 11 juin 2026）、
         cm1・cm2・6e（Sciences et technologie, cycle 3, même BO）、5e・4e・3e（Physique-chimie et SVT, programmes du cycle 4, BO n° 31 du 30 juillet 2020）、
         seconde・premiere・terminale（Physique-chimie et SVT du lycée, programmes 2019 ; première et terminale = enseignements de spécialité）
  単元: fr_sc2（cp・ce1・ce2）・fr_sc3（cm1・cm2）・fr_sc6・fr_sc5・fr_sc4・fr_sc3e・fr_sc10・fr_sc11・fr_sc12 の UNITS(grade)
  H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=, bank=, s4=)
    T は 3 つの表：(nom de la série, rows, fwd, back[, extra[, match]]) か (nom, {groupe: [éléments]})。groupe は「des herbivores」「du vivant」の形（fait partie {g}）
    TFt は正しい文、TFf は (phrase fausse, correction)、topic は「Quelle affirmation sur … est vraie ?」の「…」
  python3 fr_sci.py cm1 [slug|番号 …]   seed は 76000 + 100 × n + 番号
"""
import re
import sys
import math
import copy
import importlib
from sci_common import Unit, item
from ws_common import write_unit
import fr_common

UPDATED = "2026-11-28"
NB = " "
STD_URL_C23 = "https://www.education.gouv.fr/bo/2026/Hebdo24/MENE2611650A"
STD_URL_C4 = "https://eduscol.education.gouv.fr/4362/enseigner-au-cycle-4"
STD_URL_LY = {"P": "https://eduscol.education.gouv.fr/1648/programmes-et-ressources-en-physique-chimie-voie-gt",
              "S": "https://www.education.gouv.fr/reussir-au-lycee/les-programmes-du-lycee-general-et-technologique-9812"}
GRADES = {"cp": 1, "ce1": 2, "ce2": 3, "cm1": 4, "cm2": 5, "6e": 6, "5e": 7, "4e": 8, "3e": 9, "seconde": 10, "premiere": 11, "terminale": 12}
NAME = {"cp": "CP", "ce1": "CE1", "ce2": "CE2", "cm1": "CM1", "cm2": "CM2", "6e": "6e", "5e": "5e", "4e": "4e", "3e": "3e",
        "seconde": "seconde", "premiere": "première", "terminale": "terminale"}
MODULE = {"cp": "fr_sc2", "ce1": "fr_sc2", "ce2": "fr_sc2", "cm1": "fr_sc3", "cm2": "fr_sc3", "6e": "fr_sc6",
          "5e": "fr_sc5", "4e": "fr_sc4", "3e": "fr_sc3e", "seconde": "fr_sc10", "premiere": "fr_sc11", "terminale": "fr_sc12"}
DOM = {"M": "La matière", "V": "Le vivant", "C": "Le corps humain et la santé", "O": "Les objets techniques",
       "ME": "Matière, mouvement et énergie", "VT": "Le vivant et la planète Terre", "CS": "Le corps humain et la santé", "OT": "Objets techniques et numérique",
       "P": "Physique-chimie", "S": "Sciences de la vie et de la Terre"}
TOPICS = {"matter", "forces-and-motion", "energy", "waves-and-light", "living-things-and-ecosystems", "earth-and-space", "earths-systems", "working-scientifically", "engineering-design"}
BAD = re.compile(r"[぀-ヿ㐀-鿿豈-﫿가-힯ßäöü]")


def _txt(s):
    return re.sub(r"<[^>]+>", "", s)


def ok_text(s, where):
    t = _txt(s)
    assert not BAD.search(t), ("caractère", where, t[:80])
    assert "\\" not in s, where
    assert "  " not in t.strip(), ("espaces", where, t[:80])
    assert " ," not in t and " ." not in t.replace(" …", ""), ("ponctuation", where, t[:80])
    assert "\"" not in t and "'" not in t, ("guillemets", where, t[:80])
    assert not re.search(r" [?!:;]", t), ("espace insécable", where, t[:80])
    return s


CONTR = [(r"\b([Dd])e le ", r"\1u "), (r"\b([Dd])e les ", r"\1es "), (r"(^|[ (])à le ", r"\1au "), (r"(^|[ (])à les ", r"\1aux "),
         (r"(^|[ (])À le ", r"\1Au "), (r"(^|[ (])À les ", r"\1Aux "), (r"\b([Dd])e ([aeiouyéèêâîô])", r"\1’\2"), (r"\b([Qq])ue ([aeiouyéèêâîô])", r"\1u’\2")]


def contr(t):
    for a, b in CONTR:
        t = re.sub(a, b, t)
    return t


def nbn(t):
    return re.sub(r"(\d) (\d{3})(?!\d)", "\\1" + NB + "\\2", t)


def esc(t):
    t = nbn(contr(t))
    t = t.replace("< ", "&lt; ").replace(" >", " &gt;").replace("...", "…")
    return fr_common.fp(t)


def it(q, a, wrong, e):
    if len({x.strip().lower() for x in [a] + list(wrong)}) < 4:
        return None
    return item(q, a, list(wrong), e)


# ------------------------------------------------------------ nombres（virgule, espaces insécables à partir de 1 000）
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _fr(s):
    neg = s.startswith("-")
    s = s.lstrip("-")
    a, _, b = s.partition(".")
    if len(a) >= 4:
        g = []
        while a:
            g.insert(0, a[-3:])
            a = a[:-3]
        a = NB.join(g)
    return ("−" if neg else "") + a + ("," + b if b else "")


def sci(x, d=3):
    m, e = (("%." + str(d - 1) + "e") % x).split("e")
    m = m.rstrip("0").rstrip(".") if "." in m else m
    return "%s × 10%s" % (_fr(m), str(int(e)).translate(SUP))


def num(x, d=3):
    """d chiffres significatifs（zéros finaux supprimés）。≥ 10⁶ ou < 10⁻³ en écriture scientifique"""
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
    return _fr(s)


def nq(q, ans, wrongs, unit, e, d=3, neg=False):
    """réponse numérique。wrongs = erreurs typiques（égales, négatives, nulles supprimées）。moins de 3 → None"""
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
    return "«" + NB + s + NB + "»"


# ------------------------------------------------------------ parties
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
                    return it("Quelle association est correcte ?", k + sep + v, [a + sep + b for a, b in w], dot((fe or "{k} : {v}").format(k=k, v=v)))
                b = bad_pairs(1)
                if not b:
                    return None
                bk, bv = b[0]
                ok = [p for p in rows if p[0] != bk]
                if len(ok) < 3:
                    return None
                w = R.R.sample(ok, 3)
                right = [vv for kk, vv in rows if kk == bk]
                return it("Quelle association est fausse ?", bk + sep + bv, [a + sep + c for a, c in w], dot("La bonne association est : %s – %s" % (bk, right[0])))
            if back and r < 0.6:
                kk = {a for a, b in rows if b == v}
                w = [x for x in keys if x not in kk and tk[x] == t]
                if len(w) < 3:
                    return None
                return it(back.format(v=v), k, R.R.sample(w, 3), dot((be or fe or "{k} : {v}").format(k=k, v=v)))
            w = [x for x in vals if x not in same and tv[x] == t] + [x for x in extra if x not in same]
            if len(w) < 3:
                return None
            return it(fwd.format(k=k), v, R.R.sample(w, 3), dot((fe or "{k} : {v}").format(k=k, v=v)))
        return mk

    def G(self, groups, pos="Lequel fait partie {g} ?", neg="Lequel ne fait pas partie {g} ?"):
        R = self
        names = sorted(groups)

        def mk():
            g = R.R.choice(names)
            mine = groups[g]
            other = [(h, x) for h in names if h != g for x in groups[h] if x not in mine]
            if neg and R.R.random() < 0.4 and len(mine) >= 3:
                h, a = R.R.choice(other)
                return it(neg.format(g=g), a, R.R.sample(mine, 3), "%s fait partie %s." % (gq(a), h))
            a = R.R.choice(mine)
            ws = sorted({x for _, x in other})
            if len(ws) < 3:
                return None
            return it(pos.format(g=g), a, R.R.sample(ws, 3), "%s fait partie %s." % (gq(a), g))
        return mk

    def TF(self, true, false, topic):
        R = self

        def mk():
            if R.R.random() < 0.5:
                a = R.R.choice(true)
                w = [f for f, _ in R.R.sample(false, 3)]
                stem = R.R.choice(["Quelle affirmation sur %s est vraie ?", "Quelle phrase sur %s est juste ?"]) % topic
                return it(stem, a, w, a)
            f, c = R.R.choice(false)
            w = R.R.sample(true, 3)
            stem = R.R.choice(["Quelle affirmation sur %s est fausse ?", "Quelle phrase sur %s est fausse ?"]) % topic
            return it(stem, f, w, "La phrase %s est fausse. %s" % (gq(f.rstrip(".")), c))
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
    assert len(T) == 3 and tp in TOPICS, slug
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
        out.append((s4 or ("Calculer et appliquer" if calc else "Exercices mélangés"), mix))
        out.append(("Vrai ou faux ?", [(K_.TF(TFt, TFf, topic), 20)]))
        return out
    return dict(dom=dom, slug=slug, title=title, short=short, std=std, what=what, kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, tp=tp)


def seed_of(n, sort):
    return 76000 + 100 * n + sort


def subj(n, d):
    if n <= 3:
        return "Questionner le monde"
    if n <= 6:
        return "Sciences et technologie"
    return "Physique-chimie" if d == "P" else "SVT"


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Exemple</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Réponse : %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist):
    h = "<h2>Comment faire</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += "".join(examples)
    h += "<h2>Erreurs fréquentes</h2>" + fr_common.table(["Erreur fréquente", "Ce qu’il faut retenir"], mist)
    return fr_common.fp(h)


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
        ok_text(fr_common.fp(s), u["slug"])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["what"]):
        assert "<" not in s, s
    lim = (40, 40, 100) if n <= 2 else (60, 60, 150)
    assert len(u["title"]) <= lim[0] and len(u["kb"]) <= lim[1] and len(u["ks"]) <= lim[2], (u["slug"], len(u["title"]), len(u["kb"]), len(u["ks"]))
    d = u["dom"]
    dom = DOM[d]
    sj = subj(n, d)
    if n <= 6:
        cyc = 2 if n <= 3 else 3
        code = "Programme du cycle %d · %s" % (cyc, dom)
        tail = " (résumé du programme de sciences et technologie du cycle %d, BO n° 24 du 11 juin 2026)" % cyc
        url = STD_URL_C23
    elif n <= 9:
        code = "Programme du cycle 4 · %s" % dom
        tail = " (résumé du programme du cycle 4 de %s, BO n° 31 du 30 juillet 2020)" % ("physique-chimie" if d == "P" else "sciences de la vie et de la Terre")
        url = STD_URL_C4
    else:
        lvl = {10: "Programme de seconde", 11: "Spécialité de première", 12: "Spécialité de terminale"}[n]
        code = "%s · %s" % (lvl, dom)
        tail = " (résumé du programme %s, %s)" % ({10: "de seconde générale et technologique", 11: "de l’enseignement de spécialité de première", 12: "de l’enseignement de spécialité de terminale"}[n],
                                                 "physique-chimie" if d == "P" else "sciences de la vie et de la Terre")
        url = STD_URL_LY[d]
    gname = NAME[grade]
    seo = "%s – %s %s : fiches et exercices corrigés" % (u["short"], sj, gname)
    write_unit("fr", "science", grade, {
        "slug": u["slug"], "title": u["title"], "seo_title": seo,
        "short_title": u["short"], "domain": dom, "standard_code": code,
        "standard_url": url, "standard_text": fr_common.fp(u["std"] + tail),
        "meta_desc": fr_common.fp("%s en %s (%s) : %s. 100 exercices corrigés en ligne avec explications et une fiche à imprimer avec corrigé." % (u["short"], sj, gname, u["what"])),
        "key_big": fr_common.fp(u["kb"]), "key_sub": fr_common.fp(u["ks"]), "body_html": body,
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
    import fr_sci
    fr_sci.main()
