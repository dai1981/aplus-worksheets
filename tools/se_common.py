# -*- coding: utf-8 -*-
"""
Sverige（Lgr22, Kursplan i matematik）の単元生成の共通部品。de_common の絵の部品の上に作る。
・文はスウェーデン語。子ども向けに短い文、「du」で話しかける
・数: 1 000 から空白（ノーブレークスペース）で区切る（4 536、12 000）。小数はコンマ（2,5）
・記号: 3 · 4 ではなく 3 × 4（svenska läroböcker の多くと同じ）、12 / 3 ではなく 12 : 3、17 : 5 = 3 rest 2
・お金: 25 kr（öre は使わない）
・時刻: 8.15（kl. 8.15）、アナログは「kvart över tre」「halv fyra」（= 3:30）
・HTML の属性はシングルクォート、バックスラッシュなし
"""
import re
import de_common as D
from ws_common import (fig, svg_wrap, text, line, balance, write_unit, fr,   # noqa: F401
                       GREEN, FILL, GRAY, INK, RED, BLUE, FONT)
from de_common import pick_unique, mix, table  # noqa: F401

UPDATED = "2026-11-26"
STD_URL = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/kursplaner-i-grundskolan/matematik"
DOMAIN = {
    "T": "Taluppfattning och tals användning",
    "A": "Algebra",
    "G": "Geometri",
    "S": "Sannolikhet och statistik",
    "F": "Samband och förändring",
    "P": "Problemlösning",
}
GIRLS = ["Alice", "Maja", "Vera", "Ella", "Wilma", "Elsa", "Astrid", "Saga", "Alma", "Selma", "Ebba", "Nora", "Amira", "Freja"]
BOYS = ["Noah", "Hugo", "William", "Liam", "Oscar", "Elias", "Adam", "Ludvig", "Nils", "Leo", "Viktor", "Ali", "Melvin", "Olle"]
NB = " "


def num(n):
    """1000 → 1 000（4 けたから区切る）"""
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
    ip, _, fp = s.partition(".")
    return num(int(ip)) + ("," + fp if fp else "")


def kr(n):
    return "%s%skr" % (num(n), NB)


def u(v, unit):
    """3 cm、2 l（数と単位のあいだはノーブレークスペース）"""
    return "%s%s%s" % (num(v) if isinstance(v, int) else dec(v), NB, unit)


D.num = num  # de_common の図の数字も 1 000 の形に


class Kids:
    """名前と代名詞（hon/han、henne/honom、hennes/hans）"""
    def __init__(self, rnd):
        self.pool = [(n, "f") for n in GIRLS] + [(n, "m") for n in BOYS]
        rnd.shuffle(self.pool)
        self.i = 0

    def next(self):
        p = self.pool[self.i % len(self.pool)]
        self.i += 1
        return p

    def name(self):
        return self.next()[0]

    def two(self):
        a = self.next()
        b = self.next()
        return a[0], b[0]


def hon(g):
    return "hon" if g == "f" else "han"


def Hon(g):
    return "Hon" if g == "f" else "Han"


def hennes(g):
    return "hennes" if g == "f" else "hans"


# ------------------------------------------------------------ talord
_E = ["noll", "ett", "två", "tre", "fyra", "fem", "sex", "sju", "åtta", "nio", "tio", "elva", "tolv",
      "tretton", "fjorton", "femton", "sexton", "sjutton", "arton", "nitton"]
_T = ["", "", "tjugo", "trettio", "fyrtio", "femtio", "sextio", "sjuttio", "åttio", "nittio"]


def ord_(n):
    """345 → trehundrafyrtiofem（ett ord, som i svenska skolböcker）"""
    n = int(n)
    if n < 20:
        return _E[n]
    if n < 100:
        t, e = divmod(n, 10)
        return _T[t] + (_E[e] if e else "")
    if n < 1000:
        h, r = divmod(n, 100)
        return ("ett" if h == 1 else _E[h]) + "hundra" + (ord_(r) if r else "")
    if n < 1000000:
        t, r = divmod(n, 1000)
        return ("et" if t == 1 else ord_(t)) + "tusen" + (ord_(r) if r else "")
    raise ValueError(n)


# ------------------------------------------------------------ klockan
TIM = ["tolv", "ett", "två", "tre", "fyra", "fem", "sex", "sju", "åtta", "nio", "tio", "elva", "tolv"]


def klocka_ord(h, m):
    """analog: 'kvart över tre', 'halv fyra' (3:30), 'fem i halv fyra' (3:25)"""
    h12 = h % 12 or 12
    nx = TIM[h12 % 12 + 1]
    cur = TIM[h12]
    w = {0: cur, 5: "fem över " + cur, 10: "tio över " + cur, 15: "kvart över " + cur, 20: "tjugo över " + cur,
         25: "fem i halv " + nx, 30: "halv " + nx, 35: "fem över halv " + nx, 40: "tjugo i " + nx,
         45: "kvart i " + nx, 50: "tio i " + nx, 55: "fem i " + nx}
    return w[m]


def hm(h, m):
    """8.15 / 14.30（svensk skrivregel: punkt mellan timmar och minuter）"""
    return "%d.%02d" % (h, m)


# ------------------------------------------------------------ frågor
_NUM_RE = re.compile(r"^(.*?)(\d{1,3}(?: \d{3})*)([^\d]*)$")


def mcq(q, correct, cands, e, fill=True):
    """4 alternativ. Saknas felsvar fylls de med närliggande tal (fill=False → None)."""
    correct = str(correct)
    seen = {correct}
    pick = []
    for c in cands:
        if c is None:
            continue
        c = str(c)
        if c in seen or c == "" or c.startswith("-") or c.startswith("−"):
            continue
        seen.add(c)
        pick.append(c)
        if len(pick) == 3:
            break
    if len(pick) < 3 and fill and "<" not in correct:
        m = _NUM_RE.match(correct)
        if m:
            v = int(m.group(2).replace(NB, ""))
            st = 1
            while v and v % (st * 10) == 0 and st < 100:
                st *= 10
            for d in (st, -st, 2 * st, -2 * st, 10 * st, 3 * st):
                nv = v + d
                if nv <= 0:
                    continue
                c = "%s%s%s" % (m.group(1), num(nv), m.group(3))
                if c not in seen:
                    seen.add(c)
                    pick.append(c)
                if len(pick) == 3:
                    break
    if len(pick) < 3:
        return None
    return {"q": q, "c": [correct] + pick, "a": 0, "e": e}


def example(q, steps, answer):
    return ("<div class='sn-ex'><span class='sn-ex-t'>Exempel</span><p class='sn-ex-q'>%s</p>%s"
            "<p class='sn-ex-a'>Svar: %s</p></div>" % (q, "".join("<p class='sn-ex-s'>%s</p>" % s for s in steps), answer))


def lesson(think, examples, mist, extra=""):
    """body_html：Så tänker du → Exempel → Vanliga fel"""
    h = "<h2>Så tänker du</h2>" + "".join("<p>%s</p>" % t for t in think)
    h += extra
    h += "".join(examples)
    h += "<h2>Vanliga fel</h2>" + table(["Fel", "Rätt"], mist)
    return h


plain_text = D.plain_text
GRADE_NAME = {"arskurs-%d" % g: "Årskurs %d" % g for g in range(1, 10)}
GRADE_NAME["forskoleklass"] = "Förskoleklass"
GY = ["1c", "2c", "3c", "4", "5"]
for _k in GY:
    GRADE_NAME["matematik-" + _k] = "Matematik nivå " + _k
STAGE = {1: "1–3", 2: "1–3", 3: "1–3", 4: "4–6", 5: "4–6", 6: "4–6", 7: "7–9", 8: "7–9", 9: "7–9"}
DOMAIN.update({
    "FK": "Matematiska resonemang och uttrycksformer",
    "AF": "Aritmetik, algebra och funktioner", "TV": "Trigonometri och vektorer", "SS": "Sannolikhet och statistik",
    "LG": "Logik och geometri", "DI": "Differential- och integralkalkyl", "KT": "Komplexa tal och polynom",
    "TR": "Trigonometri", "DE": "Differentialekvationer", "DM": "Diskret matematik och bevis", "PT": "Problemlösning och tillämpningar",
})
STD_URL_F = "https://www.skolverket.se/undervisning/grundskolan/laroplan-och-kursplaner-for-grundskolan/laroplan-lgr22-for-grundskolan-samt-for-forskoleklassen-och-fritidshemmet"
STD_URL_GY = {"1c": "https://syllabuswebb.skolverket.se/subject/MATE/1/pdf", "2c": "https://syllabuswebb.skolverket.se/subject/MATE/1/pdf",
              "3c": "https://syllabuswebb.skolverket.se/subject/MAT/11/pdf", "4": "https://syllabuswebb.skolverket.se/subject/MAT/11/pdf", "5": "https://syllabuswebb.skolverket.se/subject/MAT/11/pdf"}


def make_unit(rnd, slug, dom, std_text, title, short_title, meta_desc, key_big, key_sub,
              body_html, faq, sets, sort, grade="arskurs-3"):
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
    if grade == "forskoleklass":
        seo_title = "%s i förskoleklass: arbetsblad i matematik med facit" % short_title
        code, url = "Lgr22 förskoleklass · %s" % DOMAIN[dom], STD_URL_F
        tail = " (sammanfattning av det centrala innehållet för förskoleklassen i Lgr22, kapitel 3)"
    elif grade.startswith("matematik-"):
        k = grade.split("-", 1)[1]
        seo_title = "%s – Matematik %s: uppgifter med facit" % (short_title, k)
        code, url = "Gy25 Matematik nivå %s · %s" % (k, DOMAIN[dom]), STD_URL_GY[k]
        tail = " (sammanfattning av det centrala innehållet i ämnesplanen i matematik för gymnasieskolan, nivå %s)" % k
    else:
        g = int(grade.split("-")[1])
        seo_title = "%s %s: arbetsblad i matematik med facit" % (short_title, gname.lower())
        code, url = "Lgr22 åk %s · %s" % (STAGE[g], DOMAIN[dom]), STD_URL
        tail = " (sammanfattning av det centrala innehållet i kursplanen i matematik, Lgr22, årskurs %s)" % STAGE[g]
    title, seo_title, short_title, meta_desc, key_big, key_sub = map(plain_text, (title, seo_title, short_title, meta_desc, key_big, key_sub))
    assert len(title) <= 70 and len(key_big) <= 40 and len(key_sub) <= 60, (slug, title, key_big, key_sub)
    write_unit("se", "matematik", grade, {
        "slug": slug, "title": title, "seo_title": seo_title, "short_title": short_title,
        "domain": DOMAIN[dom], "standard_code": code, "standard_url": url,
        "standard_text": std_text + tail,
        "meta_desc": meta_desc, "key_big": key_big, "key_sub": key_sub,
        "body_html": body_html, "faq": faq, "sets": sets, "pdf_url": "", "sort": sort, "updated": UPDATED,
    })


# ------------------------------------------------------------ bilder
wrap = D.wrap


def tallinje(lo, hi, step, marks=(), labels=None, every=None, width=460):
    return D.zahlenstrahl(lo, hi, step, marks, labels, "tallinje", every, width)


def positionstabell(n, cols=3):
    head = ["Tusental", "Hundratal", "Tiotal", "Ental"][-cols:]
    ds = str(n).rjust(cols, "0")[-cols:]
    return ("<table class='sn-table' style='width:auto;margin:6px 0'><thead><tr>%s</tr></thead>"
            "<tbody><tr>%s</tr></tbody></table>" % ("".join("<th>%s</th>" % c for c in head),
                                                   "".join("<td style='text-align:center;min-width:44px'>%s</td>" % c for c in ds)))


def basemat(h, t, e):
    return D.dienes(h, t, e, label="%d hundratal, %d tiotal, %d ental" % (h, t, e))


def stapel(data, unit_label="", step=None):
    return D.saeulen(data, unit_label, "stapeldiagram", step)


def streck(n):
    return D.strichliste(n).replace("Strichliste mit %d Strichen" % n, "streckräkning med %d streck" % n)


def uppstallning(rows, op="+", result=None):
    rows = [r.replace(NB, "") for r in rows]
    return D.schriftlich(rows, op, None, "uppställning", result)


def klocka(h, m, size=170):
    from tw_common import clock as _clock
    return _clock(h, m, size, label="analog klocka")
