# -*- coding: utf-8 -*-
"""
Deutschland / Naturwissenschaften。country `de`、subject `science`（name「Naturwissenschaften」）。
  grade: klasse-1〜klasse-4（Sachunterricht: naturwissenschaftliche, technische und geographische Perspektive des Perspektivrahmens Sachunterricht）、
         klasse-5・6（Naturwissenschaften: Biologie und Physik）、klasse-7〜10（Biologie, Chemie, Physik。1 つの学年ページに科目が並ぶ（domain が科目名））
  単元: de_s1（Klasse 1–2）・de_s3（3–4）・de_s5（5–6）・de_s7・de_s8・de_s9・de_s10 の UNITS(grade)
  H(dom, slug, title, short, std, what, kb, ks, think, ex, mist, faq, T, TFt, TFf, topic, tp, calc=, bank=, s4=)
    T は 3 つの表：(Rundenname, rows, fwd, back[, extra]) か (Rundenname, {Gruppe im Dativ: [Dinge]})。fwd は「{k}」、back は「{v}」を含む問題文
    TFt は正しい文、TFf は (falscher Satz, so ist es richtig)、topic は「Welche Aussage über … ist richtig?」の「…」（Akkusativ）
  python3 de_sci.py klasse-3 [slug|番号 …]   seed は 87000 + 100 × Klasse + 番号
"""
import re
import sys
import copy
import importlib
from sci_common import Unit, item
from ws_common import write_unit
import de_common

UPDATED = "2026-11-28"
STD_URL_SU = "https://www.klinkhardt.de/newsite/media/20130314_9783781519923Inh.pdf"
STD_URL = {"B": "https://www.iqb.hu-berlin.de/bista/subject/2024_06_13WeBiS_.pdf",
           "C": "https://www.iqb.hu-berlin.de/bista/subject/2024_06_13WeBiS__1.pdf",
           "P": "https://www.iqb.hu-berlin.de/bista/subject/2024_06_13WeBiS__2.pdf"}
GRADES = {"klasse-%d" % n: n for n in range(1, 14)}
STD_URL_AHR = "https://www.kmk.org/aktuelles-1/artikelansicht/kultusministerkonferenz-beschliesst-bildungsstandards-fuer-die-allgemeine-hochschulreife-in-den-naturwissenschaften.html"
PHASE = {11: "Einführungsphase", 12: "Qualifikationsphase 1", 13: "Qualifikationsphase 2"}
MODULE = {"klasse-1": "de_s1", "klasse-2": "de_s1", "klasse-3": "de_s3", "klasse-4": "de_s3", "klasse-5": "de_s5", "klasse-6": "de_s5",
          "klasse-7": "de_s7", "klasse-8": "de_s8", "klasse-9": "de_s9", "klasse-10": "de_s10",
          "klasse-11": "de_s11", "klasse-12": "de_s12", "klasse-13": "de_s13"}
DOM = {"L": "Lebende Natur", "N": "Nicht lebende Natur", "T": "Technik", "W": "Wetter, Erde und Himmel",
       "B": "Biologie", "C": "Chemie", "P": "Physik"}
PERSP = {"L": "Naturwissenschaftliche Perspektive", "N": "Naturwissenschaftliche Perspektive", "T": "Technische Perspektive", "W": "Geographische Perspektive"}
TOPICS = {"matter", "forces-and-motion", "energy", "waves-and-light", "living-things-and-ecosystems", "earth-and-space", "earths-systems", "working-scientifically", "engineering-design"}
BAD = re.compile(r"[぀-ヿ㐀-鿿豈-﫿가-힯]")
NB = "\u00a0"


def _txt(s):
    return re.sub(r"<[^>]+>", "", s)


def ok_text(s, where):
    t = _txt(s)
    assert not BAD.search(t), ("CJK", where, t[:80])
    assert "\\" not in s, where
    assert "  " not in t.strip(), ("Leerzeichen", where, t[:80])
    assert " ," not in t and " ." not in t.replace(" …", ""), ("Satzzeichen", where, t[:80])
    assert "\"" not in t and "'" not in t.replace("So geht's", ""), ("Anführungszeichen", where, t[:80])
    return s


def esc(t):
    """< > die keine HTML-Tags sind → &lt; &gt;"""
    return t.replace("< ", "&lt; ").replace(" >", " &gt;").replace("...", "…")


def it(q, a, wrong, e):
    return item(q, a, list(wrong), e)


# ------------------------------------------------------------ Zahlen（Dezimalkomma, ab 5 Stellen schmales Leerzeichen）
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _de(s):
    """'12345.6' → '12 345,6'"""
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
    return "%s · 10%s" % (_de(m), str(int(e)).translate(SUP).replace("⁻", "⁻"))


def num(x, d=3):
    """d gültige Ziffern（Nullen am Ende fallen weg）。≥ 10⁶ oder < 10⁻³ als · 10ⁿ"""
    if x != 0 and (abs(x) >= 1e6 or abs(x) < 1e-3):
        return sci(x, d)
    if isinstance(x, int) or float(x).is_integer():
        s = str(int(round(x)))
    else:
        s = ("%." + str(d) + "g") % x
        if "e" in s:
            s = (("%." + str(d) + "f") % x).rstrip("0").rstrip(".")
    return _de(s)


def nq(q, ans, wrongs, unit, e, d=3):
    """Zahlenantwort。wrongs = typische Fehler（gleiche, negative, 0 fallen weg）。weniger als 3 → None"""
    a = num(ans, d)
    out = []
    for w in wrongs:
        if w is None:
            continue
        try:
            s = num(w, d)
        except (TypeError, ValueError, OverflowError):
            continue
        if s != a and s not in out and not s.startswith("−") and s != "0":
            out.append(s)
    if len(out) < 3:
        return None
    u = ("" if unit == "°" else NB) + unit if unit else ""
    return it(q, a + u, [x + u for x in out[:3]], e)
# ------------------------------------------------------------ Aufgabenteile
class K:
    def __init__(self, R):
        self.R = R

    def P(self, rows, fwd, back=None, fe=None, be=None, match=True, sep=" – ", extra=()):
        """rows: [(k, v)] oder [(k, v, tag)]。mit tag kommen die Ablenker nur aus Zeilen mit gleichem tag"""
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
            e = e.replace(".:", ":").replace(".–", " –")
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
                    return it("Welches Paar passt zusammen?", k + sep + v, [a + sep + b for a, b in w], dot((fe or "{k}: {v}").format(k=k, v=v)))
                b = bad_pairs(1)
                if not b:
                    return None
                bk, bv = b[0]
                ok = [p for p in rows if p[0] != bk]
                if len(ok) < 3:
                    return None
                w = R.R.sample(ok, 3)
                right = [vv for kk, vv in rows if kk == bk]
                return it("Welches Paar passt nicht zusammen?", bk + sep + bv, [a + sep + c for a, c in w], dot("Richtig ist: %s – %s" % (bk, right[0])))
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

    def G(self, groups, pos="Was gehört zu {g}?", neg="Was gehört nicht zu {g}?"):
        R = self

        def zu(t):
            return t.replace("zu dem ", "zum ").replace("zu der ", "zur ")
        names = sorted(groups)

        def mk():
            g = R.R.choice(names)
            mine = groups[g]
            other = [(h, x) for h in names if h != g for x in groups[h] if x not in mine]
            if neg and R.R.random() < 0.4 and len(mine) >= 3:
                h, a = R.R.choice(other)
                return it(zu(neg.format(g=g)), a, R.R.sample(mine, 3), zu("%s gehört zu %s." % (a[0].upper() + a[1:], h)))
            a = R.R.choice(mine)
            ws = sorted({x for _, x in other})
            if len(ws) < 3:
                return None
            return it(zu(pos.format(g=g)), a, R.R.sample(ws, 3), zu("%s gehört zu %s." % (a[0].upper() + a[1:], g)))
        return mk

    def TF(self, true, false, topic):
        R = self

        def mk():
            if R.R.random() < 0.5:
                a = R.R.choice(true)
                w = [f for f, _ in R.R.sample(false, 3)]
                stem = R.R.choice(["Welche Aussage über %s ist richtig?", "Was stimmt über %s?"]) % topic
                return it(stem, a, w, a)
            f, c = R.R.choice(false)
            w = R.R.sample(true, 3)
            stem = R.R.choice(["Welche Aussage über %s ist falsch?", "Was stimmt nicht über %s?"]) % topic
            return it(stem, f, w, "Die Aussage „%s“ ist falsch. %s" % (f.rstrip("."), c))
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
        if calc and bank:
            mix = [(K_.F(calc), 12), (K_.B(bank), min(8, len(bank) - 3))]
            mix.append((part(K_, T[0]), 20 - sum(n for _, n in mix)))
        elif calc:
            mix = [(K_.F(calc), 15), (part(K_, T[1]), 5)]
        elif bank:
            n = min(20, len(bank) - 3)
            mix = [(K_.B(bank), n)] + ([(part(K_, T[1]), 20 - n)] if n < 20 else [])
        else:
            mix = [(part(K_, T[0]), 7), (part(K_, T[1]), 7), (part(K_, T[2]), 6)]
        out.append((s4 or ("Rechnen und Anwenden" if calc else "Gemischte Übung"), mix))
        out.append(("Richtig oder falsch?", [(K_.TF(TFt, TFf, topic), 20)]))
        return out
    return dict(dom=dom, slug=slug, title=title, short=short, std=std, what=what, kb=kb, ks=ks, think=think, ex=ex, mist=mist, faq=faq, sets=sets, tp=tp)


def seed_of(n, sort):
    return 87000 + 100 * n + sort


def subj(n, dom):
    return "Sachunterricht" if n <= 4 else ("Naturwissenschaften" if n <= 6 else DOM[dom])


def build(grade, u, sort):
    n = GRADES[grade]
    U_ = Unit(seed_of(n, sort))
    sets = U_.sets(u["sets"](K(U_.R)))
    for s in sets:
        for x in s["items"]:
            x["q"], x["e"] = esc(x["q"]), esc(x["e"])
            x["c"] = [esc(c) for c in x["c"]]
            for t in [x["q"], x["e"]] + x["c"]:
                ok_text(t, u["slug"])
    ex = [de_common.example(esc(q), [esc(t) for t in st], esc(a)) for q, st, a in u["ex"]]
    body = de_common.lesson([esc(t) for t in u["think"]], ex, [(esc(a), esc(b)) for a, b in u["mist"]])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["std"], u["what"], body) + tuple(a + b for a, b in u["faq"]):
        ok_text(s, u["slug"])
    for s in (u["title"], u["short"], u["kb"], u["ks"], u["what"]):
        assert "<" not in s, s
    lim = (40, 40, 100) if n <= 2 else (60, 60, 150)
    assert len(u["title"]) <= lim[0] and len(u["kb"]) <= lim[1] and len(u["ks"]) <= lim[2], (u["slug"], len(u["title"]), len(u["kb"]), len(u["ks"]))
    d = u["dom"]
    dom = DOM[d]
    sj = subj(n, d)
    if n <= 4:
        code = "Perspektivrahmen Sachunterricht · " + PERSP[d]
        tail = " (Zusammenfassung nach dem Perspektivrahmen Sachunterricht der GDSU, 2013; die Lehrpläne der Länder setzen ähnliche Schwerpunkte)"
        url = STD_URL_SU
    elif n >= 11:
        code = "Bildungsstandards %s (Allgemeine Hochschulreife)" % dom
        tail = " (Zusammenfassung; Bildungsstandards im Fach %s für die Allgemeine Hochschulreife, KMK 18.06.2020; Oberstufe, %s)" % (dom, PHASE[n])
        url = STD_URL_AHR
    else:
        code = "Bildungsstandards %s (MSA)" % dom
        tail = " (Zusammenfassung; Bildungsstandards im Fach %s für den Mittleren Schulabschluss, KMK 2004 i. d. F. vom 13.06.2024)" % dom
        url = STD_URL[d]
    seo = "%s – %s Klasse %d%s: Arbeitsblätter mit Lösungen" % (u["short"], sj, n, " (Oberstufe)" if n >= 11 else "")
    write_unit("de", "science", grade, {
        "slug": u["slug"], "title": u["title"], "seo_title": seo,
        "short_title": u["short"], "domain": dom, "standard_code": code,
        "standard_url": url, "standard_text": u["std"] + tail,
        "meta_desc": "Übungen zum Thema %s für %s in Klasse %d: %s. 100 Übungsaufgaben online mit Erklärungen und ein Arbeitsblatt zum Ausdrucken mit Lösungen." % (u["short"], sj, n, u["what"]),
        "key_big": u["kb"], "key_sub": u["ks"], "body_html": body,
        "faq": [{"q": q, "a": a} for q, a in u["faq"]], "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
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
    import de_sci
    de_sci.main()
