# -*- coding: utf-8 -*-
"""Sverige årskurs 1–2（lågstadiet, Lgr22）: 単元関数は lv = 1 または 2 を受け取る。
・絵は k_pics（svenska aria-label）、se_a3a/se_a3b（årskurs 3）の絵と問題関数を lim() で数を絞って再利用
・とても短い文。åk 1 は 20 まで（talraden till 100）、åk 2 は 100 まで
"""
import math
import random
import re
import k_pics as KP
import se_common as C
from se_common import num, kr, NB, mcq, klocka, klocka_ord, hm, stapel, streck, tallinje, basemat, positionstabell, wrap, text, line, fig, INK, GREEN, FILL, RED, BLUE
import se_m as S
import se_a3a as A
import se_a3b as B

SAK = {"apple": ("äpple", "äpplen", "ett"), "star": ("stjärna", "stjärnor", "en"), "ball": ("boll", "bollar", "en"), "button": ("knapp", "knappar", "en"),
       "fish": ("fisk", "fiskar", "en"), "flower": ("blomma", "blommor", "en"), "heart": ("hjärta", "hjärtan", "ett"), "duck": ("anka", "ankor", "en"),
       "cup": ("kopp", "koppar", "en"), "bug": ("nyckelpiga", "nyckelpigor", "en")}
KINDS = list(SAK)


def R():
    return S.R


def ri(a, b):
    return S.R.randint(a, b)


def ch(xs):
    return S.R.choice(list(xs))


def sh(xs):
    xs = list(xs)
    S.R.shuffle(xs)
    return xs


def coin():
    return S.R.random() < 0.5


def K():
    return S.K


def sak(n, k):
    return "%d %s" % (n, SAK[k][0] if n == 1 else SAK[k][1])


def pl(k):
    return SAK[k][1]


def P(svg, label, lg=False):
    svg = re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)
    if lg:
        svg = svg.replace("<svg ", "<svg data-pf='lg' ", 1)
    return fig(svg)


def lista(xs):
    xs = [str(x) for x in xs]
    return ", ".join(xs[:-1]) + " och " + xs[-1]


def MQ(t, r, w, e):
    w = [str(x) for x in w if x is not None and str(x) != str(r)]
    ws = []
    for x in w:
        if x not in ws:
            ws.append(x)
    ws = ws[:3]
    if len(ws) < 3:
        return None
    return mcq("%s %s?" % (t, lista(sh([str(r)] + ws))), str(r), ws, e)


_TAGS = re.compile(r"<[^>]+>")
_NUMS = re.compile(r"\d+(?: \d{3})*")


def nums(it):
    t = _TAGS.sub(" ", it["q"] + " " + " ".join(it["c"]))
    return [int(x.replace(NB, "")) for x in _NUMS.findall(t)]


def lim(mk, n, extra=None):
    def f():
        it = mk()
        if it is None or any(v > n for v in nums(it)):
            return None
        if extra and not extra(it):
            return None
        return it
    f.__name__ = getattr(mk, "__name__", "lim")
    return f


def maker(ufn, name):
    """åk 3 の単元関数から問題関数を取り出す"""
    d = ufn()
    for _, parts in d["sets"]:
        for mk, _n in parts:
            if mk.__name__ == name:
                return mk
    raise KeyError(name)


def unit(slug, dom, title, short, std, meta, kb, ks, sets, think, ex, mist, faq):
    return S.unit(slug, dom, title, short, std, meta, kb, ks, sets, think, ex, mist, faq)


# ============================================================ tal till 20 (åk 1) / tal till 100 (åk 2)
def tal(lv):
    top = 20 if lv == 1 else 100

    def antal():
        k = ch(KINDS)
        n = ri(3, 20)
        pic = P(KP.row_svg(n, k), sak(n, k), lg=n > 10)
        return mcq("Hur många %s är det?" % pl(k) + pic, str(n), [str(n + 1), str(n - 1), str(n + 2), str(n - 2)], "Räkna fem i taget: det är <b>%d</b>." % n)

    def ruta():
        n = ri(2, 20)
        pic = P(KP.tenframe_svg(n, 2, ch(KINDS + ["dot"])), "två tiorutor med %d saker" % n)
        return mcq("Vilket tal visar tiorutorna?" + pic, str(n), [str(n + 1), str(n - 1), str(n + 10) if n <= 10 else str(n - 10)], "En full tioruta är 10. Svar: <b>%d</b>." % n)

    def block():
        t, e = ri(1, 9), ri(0, 9)
        n = 10 * t + e
        pic = P(basemat(0, t, e), "%d tiotal och %d ental" % (t, e))
        return mcq("Vilket tal visar bilden?" + pic, str(n), [str(10 * e + t) if e else str(n + 1), str(t + e), str(n + 10) if n < 90 else str(n - 10)], "%d tiotal och %d ental är <b>%d</b>." % (t, e, n))

    def granne():
        n = ri(1, top - 1)
        k = ri(0, 2)
        if k == 0:
            return mcq("Vilket tal kommer efter %d?" % n, str(n + 1), [str(n - 1), str(n + 2), str(n + 10) if n + 10 <= top else str(n)], "Ett mer än %d är <b>%d</b>." % (n, n + 1))
        if k == 1:
            if n < 2:
                return None
            return mcq("Vilket tal kommer före %d?" % n, str(n - 1), [str(n + 1), str(n - 2), str(n - 10) if n > 10 else str(n)], "Ett mindre än %d är <b>%d</b>." % (n, n - 1))
        if n < 2:
            return None
        return mcq("Vilket tal ligger mellan %d och %d?" % (n - 1, n + 1), str(n), [str(n + 1), str(n - 1), str(n + 2)], "<b>%d</b> ligger mellan %d och %d." % (n, n - 1, n + 1))

    def ord_():
        n = ri(1, top)
        if coin():
            return mcq("Vilket tal är <b>%s</b>?" % C.ord_(n), str(n), [str(n + 1), str(n - 1) if n > 1 else str(n + 2), str(int(str(n)[::-1])) if n > 10 and n % 10 and int(str(n)[::-1]) != n else str(n + 10)], "%s skrivs <b>%d</b>." % (C.ord_(n).capitalize(), n))
        w = [C.ord_(x) for x in (n + 1, n - 1 if n > 1 else n + 2, n + 10 if n + 10 <= top else n + 2)]
        return mcq("Hur skrivs %d med bokstäver?" % n, C.ord_(n), w, "%d skrivs <b>%s</b>." % (n, C.ord_(n)))

    def linje():
        if lv == 1:
            v = ri(1, 19)
            if v < 10 and coin():
                pic = P(tallinje(0, 10, 1, [(v, "?")], labels=[0, 5, 10]), "tallinje", lg=True)
            else:
                pic = P(tallinje(0, 20, 1, [(v, "?")], labels=[0, 5, 10, 15, 20]), "tallinje", lg=True)
        else:
            v = ri(1, 99)
            if v % 10 == 0:
                return None
            lo = v // 10 * 10 - ch([0, 10])
            lo = max(0, min(lo, 80))
            pic = P(tallinje(lo, lo + 20, 1, [(v, "?")], labels=[lo, lo + 10, lo + 20]), "tallinje", lg=True)
        st = 1
        return mcq("Vilket tal pekar pilen på?" + pic, str(v), [str(v + st), str(v - st), str(v + 2 * st) if v + 2 * st <= top else str(v - 2 * st)], "Räkna strecken från närmaste tal: <b>%d</b>." % v)

    if lv == 1:
        sets = [("Räkna saker", [(antal, 20)]), ("Tiorutor", [(ruta, 20)]), ("Före, efter och mellan", [(granne, 20)]), ("Tal med bokstäver", [(ord_, 20)]), ("Tallinjen", [(linje, 20)])]
        return unit("tal-till-20", "T", "Tal till 20: räkna, läsa och skriva tal", "Tal till 20",
                    "Naturliga tal och deras egenskaper samt hur talen kan delas upp och hur de kan användas för att ange antal och ordning.",
                    "Arbetsblad om tal till 20 för årskurs 1: räkna saker, tiorutor, talet före och efter, tal med bokstäver och tallinjen. 100 uppgifter med facit.",
                    "Räkna fem i taget", "En full tioruta är tio.", sets,
                    ["Räkna en sak i taget och peka. Du kan också räkna fem i taget.", "En tioruta har plats för 10. Två tiorutor rymmer 20.", "Talet efter är ett mer. Talet före är ett mindre."],
                    [("Vilket tal kommer efter 13?", ["Ett mer än 13"], "14"), ("En full tioruta och 4 till", ["10 + 4"], "14")],
                    [["Räknar samma sak två gånger", "Peka på varje sak en gång"], ["Skriver 12 som 21", "Tolv är ett tiotal och två ental: 12"], ["Talet före 10 är 11", "Talet före är ett mindre: 9"]],
                    [("Hur kan jag räkna snabbare?", "Gör grupper om fem eller tio."), ("Vad är en tioruta?", "En ruta med tio platser, två rader med fem."), ("Vilket tal kommer efter 19?", "20, tjugo.")])
    sets = [("Tiotal och ental i bild", [(block, 20)]), ("Före, efter och mellan", [(granne, 20)]), ("Tal med bokstäver", [(ord_, 20)]), ("Tallinjen", [(linje, 20)]), ("Blandat", [(block, 10), (granne, 10)])]
    return unit("tal-till-100", "T", "Tal till 100: läsa, skriva och placera tal", "Tal till 100",
                "Naturliga tal och deras egenskaper samt hur talen kan delas upp och hur de kan användas för att ange antal och ordning. Positionssystemet för tal.",
                "Arbetsblad om tal till 100 för årskurs 2: tiotal och ental i bild, talet före och efter, tal med bokstäver och tallinjen. 100 uppgifter med facit.",
                "47 = 4 tiotal och 7 ental", "Tiotalssiffran står först.", sets,
                ["Ett tvåsiffrigt tal består av tiotal och ental. I 47 är 4 tiotal och 7 ental.", "Talet efter är ett mer och talet före ett mindre.", "På tallinjen står talen i ordning. Räkna strecken från ett känt tal."],
                [("4 tiotal och 7 ental", ["40 + 7"], "47"), ("Talet före 60", ["Ett mindre än 60"], "59")],
                [["Skriver 47 som 74", "Tiotalen först: 47"], ["Talet efter 39 är 310", "Efter 39 kommer 40"], ["Räknar fel steg på tallinjen", "Se hur mycket varje streck är värt"]],
                [("Vad betyder tiotal?", "Tio stycken tillsammans. 3 tiotal är 30."), ("Vilket tal kommer efter 99?", "100, hundra."), ("Hur skriver man 70 med bokstäver?", "sjuttio")])


# ============================================================ talraden till 100 (åk 1)
def talraden(lv):
    def fortsatt():
        n = ri(1, 95)
        st = ch([1, 1, 2, 10])
        if n + 4 * st > 100:
            return None
        seq = [n + st * i for i in range(4)]
        return mcq("Fortsätt räkna: %s, … Vilket tal kommer sedan?" % ", ".join(map(str, seq)), str(n + 4 * st), [str(n + 3 * st + 1) if st > 1 else str(n + 5), str(n + 5 * st) if n + 5 * st <= 100 else str(n + 3 * st), str(n + 4 * st + 10) if n + 4 * st + 10 <= 100 else str(n + 4 * st - 1)],
                   "Det ökar med %d varje gång: <b>%d</b>." % (st, n + 4 * st))

    def bak():
        n = ri(6, 100)
        seq = [n - i for i in range(4)]
        return mcq("Räkna baklänges: %s, … Vilket tal kommer sedan?" % ", ".join(map(str, seq)), str(n - 4), [str(n - 3), str(n - 5), str(n + 1)], "Ett mindre varje gång: <b>%d</b>." % (n - 4))

    def saknas():
        n = ri(1, 96)
        i = ri(1, 3)
        seq = [str(n + j) if j != i else "__" for j in range(5)]
        return mcq("Vilket tal saknas: %s?" % ", ".join(seq), str(n + i), [str(n + i + 1), str(n + i - 1), str(n + i + 10) if n + i + 10 <= 100 else str(n + i + 2)], "Talen står i ordning. Det saknade talet är <b>%d</b>." % (n + i))

    def tiotal():
        e = ri(0, 9)
        t = ri(0, 5)
        seq = [10 * (t + j) + e for j in range(4)]
        if seq[-1] + 10 > 100:
            return None
        return mcq("Hoppa tio i taget: %s, … Vilket tal kommer sedan?" % ", ".join(map(str, seq)), str(seq[-1] + 10), [str(seq[-1] + 1), str(seq[-1] + 11), str(seq[-1] + 20) if seq[-1] + 20 <= 100 else str(seq[-1] - 10)], "Tiotalssiffran ökar med 1: <b>%d</b>." % (seq[-1] + 10))

    def hundra():
        n = ri(11, 99)
        k = ri(0, 2)
        if k == 0:
            return mcq("Vilket tal är tio mer än %d?" % n, str(n + 10), [str(n + 1), str(n - 10), str(n + 11)], "Tiotalssiffran ökar med 1: <b>%d</b>." % (n + 10)) if n + 10 <= 100 else None
        if k == 1:
            return mcq("Vilket tal är tio mindre än %d?" % n, str(n - 10), [str(n - 1), str(n + 10) if n + 10 <= 100 else str(n - 11), str(n - 9)], "Tiotalssiffran minskar med 1: <b>%d</b>." % (n - 10))
        return mcq("Vilket tal kommer efter %d?" % n, str(n + 1), [str(n - 1), str(n + 10) if n + 10 <= 100 else str(n + 2), str(n + 2)], "Ett mer: <b>%d</b>." % (n + 1))

    sets = [("Räkna framåt", [(fortsatt, 20)]), ("Räkna baklänges", [(bak, 20)]), ("Vilket tal saknas?", [(saknas, 20)]), ("Tio i taget", [(tiotal, 20)]), ("Tio mer och tio mindre", [(hundra, 20)])]
    return unit("talraden-till-100", "T", "Talraden till 100: räkna framåt och baklänges", "Talraden till 100",
                "Naturliga tal och deras egenskaper samt hur de kan användas för att ange antal och ordning. Mönster i talraden.",
                "Arbetsblad om talraden till 100 för årskurs 1: räkna framåt och baklänges, vilket tal saknas, tio i taget och tio mer och tio mindre. 100 uppgifter med facit.",
                "Efter 29 kommer 30", "När entalen tar slut blir det ett nytt tiotal.", sets,
                ["Talraden fortsätter med samma mönster: 21, 22, 23 … 29, 30.", "När du räknar baklänges blir talet ett mindre varje gång.", "Tio i taget: tiotalssiffran ökar med ett, 14, 24, 34."],
                [("Fortsätt: 27, 28, 29", ["Efter 29 kommer ett nytt tiotal"], "30"), ("Tio mer än 46", ["Tiotalssiffran 4 blir 5"], "56")],
                [["Efter 29 kommer 20", "Efter 29 kommer 30"], ["Tio mer än 46 är 47", "Tio mer ändrar tiotalssiffran: 56"], ["Hoppar över ett tal", "Säg talen högt och peka"]],
                [("Varför är talraden viktig?", "Den hjälper dig att räkna och se mönster i talen."), ("Hur räknar jag tio i taget?", "Behåll entalssiffran och öka tiotalssiffran."), ("Vad kommer efter 99?", "100.")])


# ============================================================ jämföra tal
def jamfora(lv):
    top = 20 if lv == 1 else 100

    def tecken():
        a, b = ri(0, top), ri(0, top)
        if coin() and a != b:
            b = a if ri(0, 4) == 0 else b
        r = "<" if a < b else ">" if a > b else "="
        return mcq("Vilket tecken ska stå i rutan? %d □ %d" % (a, b), r.replace("<", "&lt;").replace(">", "&gt;"), [x.replace("<", "&lt;").replace(">", "&gt;") for x in ("<", ">", "=", "+") if x != r][:3],
                   "%s. Svar: <b>%d %s %d</b>." % ("Lika mycket" if a == b else "%d är %s än %d" % (a, "mindre" if a < b else "större", b), a, r.replace("<", "&lt;").replace(">", "&gt;"), b))

    def storst():
        xs = sh(set(ri(1, top) for _ in range(6)))[:4]
        if len(xs) < 4:
            return None
        if coin():
            return MQ("Vilket tal är störst:", str(max(xs)), [str(x) for x in xs if x != max(xs)], "<b>%d</b> är störst." % max(xs))
        return MQ("Vilket tal är minst:", str(min(xs)), [str(x) for x in xs if x != min(xs)], "<b>%d</b> är minst." % min(xs))

    def flest():
        k1, k2 = sh(KINDS)[:2]
        a, b = ri(2, 10), ri(2, 10)
        if a == b:
            return None
        pic = P(KP.two_groups_svg(a, k1, b, k2, "och"), "%s och %s" % (sak(a, k1), sak(b, k2)))
        more = k1 if a > b else k2
        if coin():
            return mcq("Vilka finns det flest av?" + pic, pl(more), [pl(k2 if more == k1 else k1), "lika många", "det går inte att se"], "Räkna: %s och %s. Flest är det <b>%s</b>." % (sak(a, k1), sak(b, k2), pl(more)))
        return mcq("Hur många fler %s än %s är det?" % (pl(more), pl(k2 if more == k1 else k1)) + pic, str(abs(a - b)), [str(a + b), str(max(a, b)), str(abs(a - b) + 1)], "%d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))

    def ordna():
        xs = sh(set(ri(1, top) for _ in range(5)))[:3]
        if len(xs) < 3:
            return None
        r = ", ".join(map(str, sorted(xs)))
        w = [", ".join(map(str, sorted(xs, reverse=True))), ", ".join(map(str, xs)) if xs != sorted(xs) else ", ".join(map(str, [xs[1], xs[0], xs[2]])), ", ".join(map(str, [sorted(xs)[0], sorted(xs)[2], sorted(xs)[1]]))]
        return mcq("Skriv talen %s i ordning. Börja med det minsta." % lista(xs), r, w, "Minst först: <b>%s</b>." % r)

    def skillnad():
        a, b = ri(1, top), ri(1, top)
        if a == b:
            return None
        return mcq("Hur mycket större är %d än %d?" % (max(a, b), min(a, b)), str(abs(a - b)), [str(a + b) if a + b <= top * 2 else str(abs(a - b) + 2), str(abs(a - b) + 1), str(abs(a - b) - 1) if abs(a - b) > 1 else str(abs(a - b) + 3)], "%d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))

    def narmast():
        n = ri(11, 99)
        if n % 10 == 5 or n % 10 == 0:
            return None
        r = int(round(n / 10.0)) * 10
        return mcq("Vilket tiotal ligger närmast %d?" % n, str(r), [str(r + 10) if r + 10 <= 100 else str(r - 20), str(r - 10), str(n // 10 * 10 + 5)], "%d ligger närmare %d. Svar: <b>%d</b>." % (n, r, r))

    if lv == 1:
        sets = [("Större, mindre eller lika", [(tecken, 20)]), ("Störst och minst", [(storst, 20)]), ("Flest och färre", [(flest, 20)]), ("Ordna talen", [(ordna, 20)]), ("Hur många fler?", [(skillnad, 20)])]
        slug, title = "jamfora-tal", "Jämföra tal: större än, mindre än och lika med"
    else:
        sets = [("Större, mindre eller lika", [(tecken, 20)]), ("Störst och minst", [(storst, 20)]), ("Ordna talen", [(ordna, 20)]), ("Närmaste tiotal", [(narmast, 20)]), ("Hur mycket större?", [(skillnad, 20)])]
        slug, title = "jamfora-och-ordna-tal", "Jämföra och ordna tal till 100"
    return unit(slug, "T", title, "Jämföra tal" if lv == 1 else "Jämföra och ordna tal",
                "Naturliga tal och deras egenskaper samt hur de kan användas för att ange antal och ordning. Symbolerna för större än, mindre än och lika med.",
                "Arbetsblad om att jämföra tal för årskurs %d: tecknen &lt;, &gt; och =, störst och minst, ordna tal%s. 100 uppgifter med facit." % (lv, " och hur många fler" if lv == 1 else ", närmaste tiotal och skillnader"),
                "Öppna sidan mot det större talet", "5 < 8 betyder 5 är mindre än 8.", sets,
                ["&lt; betyder mindre än och &gt; betyder större än. = betyder lika mycket.", "Jämför först tiotalen, sedan entalen: 38 &lt; 41 eftersom 3 tiotal är mindre än 4 tiotal.", "Skillnaden mellan två tal är hur mycket större det ena är."],
                [("7 □ 12", ["7 är mindre än 12"], "7 &lt; 12"), ("Ordna 15, 9, 12", ["Minst först"], "9, 12, 15")],
                [["Vänder på tecknet", "Den öppna sidan mot det större talet: 7 &lt; 12"], ["Tror att 29 är större än 31 för att 9 är stort", "Jämför tiotalen först: 2 &lt; 3"], ["Ordnar från störst när det står minst", "Läs frågan noga"]],
                [("Hur kommer jag ihåg tecknen?", "Tänk att tecknet är en mun som vill äta det större talet."), ("Vad betyder lika med?", "Att det är lika mycket på båda sidor."), ("Hur jämför jag två tal?", "Titta först på tiotalen. Är de lika jämför du entalen.")])


# ============================================================ talkamrater (åk 1)
def talkamrater(lv):
    def tio():
        a = ri(0, 10)
        pic = P(KP.tenframe_svg(a, 1, ch(KINDS + ["dot"])), "tioruta med %d saker" % a)
        return mcq("Hur många fler behövs för att det ska bli 10?" + pic, str(10 - a), [str(a), str(10 - a + 1), str(10 - a - 1) if a < 10 else "2"], "%d + %d = 10. Svar: <b>%d</b>." % (a, 10 - a, 10 - a))

    def bond():
        w = ri(3, 10 if coin() else 20)
        a = ri(1, w - 1)
        k = ri(0, 1)
        pic = P(KP.bond_svg(w, a, "?") if k == 0 else KP.bond_svg("?", a, w - a), "talkamrater")
        if k == 0:
            return mcq("Vilket tal saknas?" + pic, str(w - a), [str(w + a), str(w - a + 1), str(a)] if a != w - a else [str(w + a), str(a + 1), str(a - 1)], "%d och %d är talkamrater till %d. Svar: <b>%d</b>." % (a, w - a, w, w - a))
        return mcq("Vilket tal saknas överst?" + pic, str(w), [str(abs(w - 2 * a)) if w != 2 * a else str(w + 2), str(w + 1), str(w - 1)], "%d + %d = <b>%d</b>." % (a, w - a, w))

    def saknas():
        w = ch([5, 6, 7, 8, 9, 10, 10, 10])
        a = ri(0, w)
        return mcq("%d + □ = %d. Vilket tal står i rutan?" % (a, w), str(w - a), [str(w + a), str(w - a + 1), str(a)] if a != w - a else [str(w + a), str(a + 1), str(abs(a - 1))], "%d + %d = %d. Svar: <b>%d</b>." % (a, w - a, w, w - a))

    def tjugo():
        a = ri(1, 19)
        return mcq("Hur mycket fattas från %d till 20?" % a, str(20 - a), [str(10 - a % 10) if a % 10 and 10 - a % 10 != 20 - a else str(20 - a + 1), str(20 - a + 1), str(20 - a - 1)], "%d + %d = 20. Svar: <b>%d</b>." % (a, 20 - a, 20 - a))

    def dela():
        w = ri(4, 10)
        a = ri(1, w - 1)
        k1 = ch(KINDS)
        pic = P(KP.row_svg(w, k1), sak(w, k1))
        return mcq("Här är %s. %d ligger i en låda. Hur många ligger utanför lådan?" % (sak(w, k1), a) + pic, str(w - a), [str(w + a), str(a) if a != w - a else str(a + 1), str(w - a + 1)], "%d − %d = <b>%d</b>." % (w, a, w - a))

    sets = [("Tiokamrater", [(tio, 20)]), ("Tal i delar", [(bond, 20)]), ("Vilket tal saknas?", [(saknas, 20)]), ("Kamrater till 20", [(tjugo, 19), (saknas, 1)]), ("Dela upp", [(dela, 20)])]
    return unit("talkamrater", "T", "Talkamrater: tiokamrater och tal i delar", "Talkamrater",
                "Hur talen kan delas upp och hur de kan användas för att ange antal. Del av helhet.",
                "Arbetsblad om talkamrater för årskurs 1: tiokamrater, dela upp tal, saknade tal och kamrater till 20. 100 uppgifter med facit.",
                "7 och 3 är tiokamrater", "Två tal som tillsammans blir 10.", sets,
                ["Talkamrater är två tal som tillsammans blir ett visst tal. 6 och 4 är tiokamrater.", "Ett tal kan delas upp på många sätt: 8 = 5 + 3 = 6 + 2 = 4 + 4.", "Kan du tiokamraterna kan du också räkna till 20: 13 + 7 = 20."],
                [("6 och ? blir 10", ["6 + 4 = 10"], "4"), ("Dela upp 8", ["5 och 3", "4 och 4"], "Flera sätt")],
                [["Tror att 6 och 5 blir 10", "6 + 4 = 10"], ["Glömmer att 0 och 10 också är kamrater", "0 + 10 = 10"], ["Räknar alla i stället för de som fattas", "Räkna bara de tomma rutorna"]],
                [("Varför ska jag kunna tiokamraterna?", "De gör det lätt att räkna förbi 10."), ("Hur många tiokamrater finns det?", "0 och 10, 1 och 9, 2 och 8, 3 och 7, 4 och 6 och 5 och 5."), ("Vad är en del?", "En bit av hela talet.")])


# ============================================================ addition och subtraktion till 10, 20, 100
def addition10(lv):
    def bild():
        k1 = ch(KINDS)
        a, b = ri(1, 6), ri(1, 5)
        if a + b > 10:
            return None
        pic = P(KP.two_groups_svg(a, k1, b, k1, "+"), "%s plus %s" % (sak(a, k1), sak(b, k1)))
        return mcq("Hur många %s är det tillsammans?" % pl(k1) + pic, str(a + b), [str(a + b + 1), str(a + b - 1), str(max(a, b))], "%d + %d = <b>%d</b>." % (a, b, a + b))

    def tal():
        a, b = ri(0, 9), ri(1, 9)
        if a + b > 10:
            return None
        return mcq("%d + %d = ?" % (a, b), str(a + b), [str(a + b + 1), str(a + b - 1) if a + b > 1 else "3", str(abs(a - b)) if abs(a - b) not in (a + b, a + b + 1, a + b - 1) else str(a + b + 2)], "%d + %d = <b>%d</b>." % (a, b, a + b))

    def linje():
        a, b = ri(0, 7), ri(1, 5)
        if a + b > 10:
            return None
        pic = P(KP.hop_line_svg(a, b, 0, 10, 40), "tallinje med hopp", lg=True)
        return mcq("Börja på %d och hoppa %d steg. Var hamnar du?" % (a, b) + pic, str(a + b), [str(a + b + 1), str(a + b - 1), str(b)], "%d + %d = <b>%d</b>." % (a, b, a + b))

    def text_():
        nm = K().name()
        k = ch(KINDS)
        a, b = ri(1, 6), ri(1, 5)
        if a + b > 10:
            return None
        return mcq("%s har %s. %s får %d till. Hur många har %s nu?" % (nm, sak(a, k), nm, b, nm), str(a + b), [str(a + b + 1), str(abs(a - b)) if a != b else str(a + b - 1), str(a + b - 1)], "%d + %d = <b>%d</b>." % (a, b, a + b))

    def tarning():
        a, b = ri(1, 6), ri(1, 4)
        if a + b > 10:
            return None
        pic = P(KP.dice_svg([a, b]), "två tärningar")
        return mcq("Hur många prickar är det tillsammans?" + pic, str(a + b), [str(a + b + 1), str(a + b - 1), str(a * b) if a * b != a + b else str(a + b + 2)], "%d + %d = <b>%d</b>." % (a, b, a + b))

    sets = [("Plus med bilder", [(bild, 20)]), ("Plus med tärningar", [(tarning, 20)]), ("Plus på tallinjen", [(linje, 20)]), ("Räkna plus", [(tal, 20)]), ("Berättelser", [(text_, 20)])]
    return unit("addition-till-10", "T", "Addition till 10: plus med bilder och tal", "Addition till 10",
                "Centrala metoder för beräkningar med naturliga tal vid huvudräkning. Additionens innebörd och samband.",
                "Arbetsblad om addition till 10 för årskurs 1: plus med bilder, tärningar, tallinjen, räkna plus och berättelser. 100 uppgifter med facit.",
                "Plus betyder att det blir fler", "Börja med det största talet och räkna vidare.", sets,
                ["Plus (+) betyder att vi lägger till. Det blir fler.", "Börja på det största talet och räkna vidare: 6 + 3, säg 6 och räkna 7, 8, 9.", "Ordningen spelar ingen roll: 2 + 5 är lika mycket som 5 + 2."],
                [("4 + 3", ["Börja på 4", "Räkna 5, 6, 7"], "7"), ("2 + 6", ["Börja på 6", "Räkna 7, 8"], "8")],
                [["Räknar startsiffran två gånger", "Börja på 4 och räkna nästa: 5, 6, 7"], ["4 + 3 = 1", "Plus blir fler: 7"], ["Glömmer att 0 inte ändrar", "5 + 0 = 5"]],
                [("Vad betyder likhetstecknet?", "Att det är lika mycket på båda sidor."), ("Måste jag räkna på fingrarna?", "Det går bra i början. Sedan lär du dig många svar utantill."), ("Vad händer om man adderar 0?", "Inget, talet blir detsamma.")])


def subtraktion10(lv):
    def bild():
        k1 = ch(KINDS)
        n, k = ri(3, 10), ri(1, 9)
        if k >= n:
            return None
        pic = P(KP.crossed_row_svg(n, k1, k), "%s, %d är överstrukna" % (sak(n, k1), k))
        return mcq("Några %s är borta. Hur många är kvar?" % pl(k1) + pic, str(n - k), [str(n + k) if n + k <= 12 else str(n - k + 2), str(k), str(n - k + 1)] if k != n - k else [str(n), str(k + 1), str(n - k - 1)], "%d − %d = <b>%d</b>." % (n, k, n - k))

    def tal():
        n, k = ri(1, 10), ri(0, 9)
        if k > n:
            return None
        return mcq("%d − %d = ?" % (n, k), str(n - k), [str(n + k) if n + k != n - k else str(n - k + 1), str(n - k + 1), str(n - k - 1) if n - k else "2"], "%d − %d = <b>%d</b>." % (n, k, n - k))

    def linje():
        a, b = ri(3, 10), ri(1, 5)
        if b > a:
            return None
        pic = P(KP.hop_line_svg(a, -b, 0, 10, 40), "tallinje med hopp bakåt", lg=True)
        return mcq("Börja på %d och hoppa %d steg bakåt. Var hamnar du?" % (a, b) + pic, str(a - b), [str(a + b) if a + b <= 12 else str(a - b + 2), str(a - b + 1), str(b) if b != a - b else str(a - b - 1)], "%d − %d = <b>%d</b>." % (a, b, a - b))

    def text_():
        nm = K().name()
        k = ch(KINDS)
        a, b = ri(3, 10), ri(1, 9)
        if b >= a:
            return None
        v = ch(["ger bort", "tappar", "äter upp"]) if k == "apple" else ch(["ger bort", "tappar"])
        return mcq("%s har %s. %s %s %d. Hur många har %s kvar?" % (nm, sak(a, k), nm, v, b, nm), str(a - b), [str(a + b), str(a - b + 1), str(b)] if b != a - b else [str(a + b), str(a - b + 1), str(a)], "%d − %d = <b>%d</b>." % (a, b, a - b))

    def saknas():
        n = ri(2, 10)
        k = ri(1, n)
        return mcq("%d − □ = %d. Vilket tal står i rutan?" % (n, n - k), str(k), [str(n + n - k) if n + n - k <= 20 else str(k + 2), str(k + 1), str(n - k) if n - k != k else str(k - 1) if k > 1 else "3"], "%d − %d = %d. Svar: <b>%d</b>." % (n, k, n - k, k))

    sets = [("Minus med bilder", [(bild, 20)]), ("Minus på tallinjen", [(linje, 20)]), ("Räkna minus", [(tal, 20)]), ("Vilket tal saknas?", [(saknas, 20)]), ("Berättelser", [(text_, 20)])]
    return unit("subtraktion-till-10", "T", "Subtraktion till 10: minus med bilder och tal", "Subtraktion till 10",
                "Centrala metoder för beräkningar med naturliga tal vid huvudräkning. Subtraktionens innebörd och samband med addition.",
                "Arbetsblad om subtraktion till 10 för årskurs 1: minus med bilder, tallinjen, räkna minus, saknade tal och berättelser. 100 uppgifter med facit.",
                "Minus betyder att det blir färre", "Räkna bakåt från det stora talet.", sets,
                ["Minus (−) betyder att vi tar bort. Det blir färre.", "Räkna bakåt: 8 − 3, säg 7, 6, 5.", "Kontrollera med plus: 8 − 3 = 5 eftersom 5 + 3 = 8."],
                [("9 − 4", ["Räkna bakåt 4 steg från 9: 8, 7, 6, 5"], "5"), ("7 − 7", ["Allt tas bort"], "0")],
                [["9 − 4 = 13", "Minus blir färre: 5"], ["Räknar 9 som första steget bakåt", "Första steget bakåt från 9 är 8"], ["Byter plats på talen", "Det stora talet står först"]],
                [("Hur kontrollerar jag ett minus?", "Lägg ihop svaret och det du tog bort. Då ska du få det första talet."), ("Kan svaret bli 0?", "Ja, om du tar bort allt."), ("Vad betyder kvar?", "Det som finns efter att något tagits bort.")])


def addsub20(lv):
    def plus():
        a, b = ri(2, 9), ri(2, 9)
        if a + b <= 10 and coin():
            return None
        return mcq("%d + %d = ?" % (a, b), str(a + b), [str(a + b + 1), str(a + b - 1), str(a + b + 10) if a + b + 10 <= 20 else str(a + b - 10)], "Gör en tia först: %d + %d = 10, sedan %d till: <b>%d</b>." % (a, 10 - a, b - (10 - a), a + b) if a + b > 10 else "%d + %d = <b>%d</b>." % (a, b, a + b))

    def minus():
        a = ri(11, 20)
        b = ri(2, 9)
        if b > a:
            return None
        return mcq("%d − %d = ?" % (a, b), str(a - b), [str(a - b + 1), str(a - b - 1), str(a - b + 10) if a - b + 10 <= 20 else str(a + b) if a + b <= 20 else str(a - b + 2)], "Ta först bort ner till 10, sedan resten: <b>%d</b>." % (a - b) if a - 10 < b else "%d − %d = <b>%d</b>." % (a, b, a - b))

    def tiotal():
        a, b = ri(1, 9), ri(1, 9)
        if coin():
            if a + b > 9:
                return None
            return mcq("1%d + %d = ?" % (a, b), str(10 + a + b), [str(a + b), str(10 + a + b + 1), str(20 + a + b) if 20 + a + b <= 29 else str(10 + a + b - 1)], "Entalen: %d + %d = %d. Tiotalet följer med: <b>%d</b>." % (a, b, a + b, 10 + a + b)) if 10 + a + b <= 20 else None
        if b > a:
            a, b = b, a
        return mcq("1%d − %d = ?" % (a, b), str(10 + a - b), [str(a - b), str(10 + a - b + 1), str(10 + a + b) if 10 + a + b <= 20 else str(10 + a - b - 1)], "Entalen: %d − %d = %d. Tiotalet är kvar: <b>%d</b>." % (a, b, a - b, 10 + a - b))

    def saknas():
        a, b = ri(2, 10), ri(2, 10)
        if a + b > 20:
            return None
        if coin():
            return mcq("%d + □ = %d. Vilket tal står i rutan?" % (a, a + b), str(b), [str(a + b + a) if a + b + a <= 20 else str(b + 2), str(b + 1), str(b - 1)], "%d + %d = %d. Svar: <b>%d</b>." % (a, b, a + b, b))
        return mcq("□ − %d = %d. Vilket tal står i rutan?" % (a, b), str(a + b), [str(abs(b - a)) if a != b else str(a + b + 2), str(a + b + 1), str(a + b - 1)], "%d + %d = %d. Svar: <b>%d</b>." % (b, a, a + b, a + b))

    def text_():
        nm = K().name()
        k = ch(KINDS)
        a, b = ri(5, 12), ri(3, 9)
        if coin() and a + b <= 20:
            return mcq("%s plockar %s på morgonen och %d på eftermiddagen. Hur många plockar %s sammanlagt?" % (nm, sak(a, k), b, nm) if k in ("flower", "apple") else "%s har %s. %s hittar %d till. Hur många har %s nu?" % (nm, sak(a, k), nm, b, nm), str(a + b), [str(a + b + 1), str(a - b) if a > b else str(a + b - 1), str(a + b - 1)], "%d + %d = <b>%d</b>." % (a, b, a + b))
        a = ri(11, 20)
        b = ri(2, 9)
        return mcq("Det finns %s i en skål. %s tar %d. Hur många finns kvar?" % (sak(a, k), nm, b), str(a - b), [str(a + b) if a + b <= 20 else str(a - b + 2), str(a - b + 1), str(a - b - 1)], "%d − %d = <b>%d</b>." % (a, b, a - b))

    sets = [("Plus över tio", [(plus, 20)]), ("Minus under tio", [(minus, 20)]), ("Räkna med tiotalet", [(tiotal, 20)]), ("Vilket tal saknas?", [(saknas, 20)]), ("Berättelser", [(text_, 20)])]
    return unit("addition-och-subtraktion-till-20", "T", "Addition och subtraktion till 20: över tiotalet", "Addition och subtraktion till 20",
                "Centrala metoder för beräkningar med naturliga tal vid huvudräkning. Additionens och subtraktionens samband. Tiotalsövergång.",
                "Arbetsblad om addition och subtraktion till 20 för årskurs 1: plus över tio, minus under tio, räkna med tiotalet, saknade tal och berättelser. 100 uppgifter med facit.",
                "Gör en tia först", "8 + 5 = 8 + 2 + 3 = 13", sets,
                ["När du räknar över 10 kan du göra en tia först: 8 + 5 = 8 + 2 + 3 = 10 + 3 = 13.", "Vid minus kan du gå ner till 10 först: 14 − 6 = 14 − 4 − 2 = 10 − 2 = 8.", "Plus och minus hör ihop: 13 − 5 = 8 eftersom 8 + 5 = 13."],
                [("7 + 6", ["7 + 3 = 10", "10 + 3"], "13"), ("15 − 7", ["15 − 5 = 10", "10 − 2"], "8")],
                [["7 + 6 = 12", "Gör en tia: 7 + 3 + 3 = 13"], ["15 − 7 = 12", "Räkna bakåt förbi 10: 8"], ["14 + 3 = 44", "Bara entalen läggs ihop: 17"]],
                [("Vad betyder att göra en tia?", "Att först fylla upp till 10 och sedan lägga till resten."), ("Hur kontrollerar jag minus?", "Räkna plus baklänges."), ("Vilka svar ska jag kunna utantill?", "Dubblorna och tiokamraterna är bra att börja med.")])


def addsub100(lv):
    def tiotal():
        a, b = ri(1, 9) * 10, ri(1, 9) * 10
        if coin():
            if a + b > 100:
                return None
            return mcq("%d + %d = ?" % (a, b), str(a + b), [str(a + b + 10) if a + b + 10 <= 100 else str(a + b - 20), str(a // 10 + b // 10), str(a + b - 10)], "%d tiotal + %d tiotal = %d tiotal = <b>%d</b>." % (a // 10, b // 10, (a + b) // 10, a + b))
        if b > a:
            a, b = b, a
        if a == b:
            return None
        return mcq("%d − %d = ?" % (a, b), str(a - b), [str(a - b + 10), str(a - b - 10) if a - b > 10 else str(a + b) if a + b <= 100 else str(a - b + 20), str((a - b) // 10)], "%d tiotal − %d tiotal = <b>%d</b>." % (a // 10, b // 10, a - b))

    def utan():
        a, b = ri(11, 88), ri(11, 88)
        if a % 10 + b % 10 >= 10 or a + b > 99:
            return None
        return mcq("%d + %d = ?" % (a, b), str(a + b), [str(a + b + 10), str(a + b - 10), str(a + b + 1)], "Tiotal för sig: %d. Ental för sig: %d. Svar: <b>%d</b>." % (a // 10 * 10 + b // 10 * 10, a % 10 + b % 10, a + b))

    def med():
        a, b = ri(11, 79), ri(5, 49)
        if a % 10 + b % 10 < 10 or a + b > 100:
            return None
        return mcq("%d + %d = ?" % (a, b), str(a + b), [str(a + b - 10), str(a + b + 10) if a + b + 10 <= 100 else str(a + b - 1), str(a + b + 1)], "Entalen blir %d, alltså ett tiotal till. Svar: <b>%d</b>." % (a % 10 + b % 10, a + b))

    def minus():
        a, b = ri(21, 99), ri(5, 49)
        if b >= a:
            return None
        v = a - b
        w = [str(v + 10) if v + 10 <= 100 else str(v - 2), str(v - 10) if v > 10 else str(v + 1), str(abs(a % 10 - b % 10) + (a // 10 - b // 10) * 10) if a % 10 < b % 10 and abs(a % 10 - b % 10) + (a // 10 - b // 10) * 10 != v else str(v + 1)]
        return mcq("%d − %d = ?" % (a, b), str(v), w, "Ta bort tiotalen och sedan entalen: <b>%d</b>." % v)

    def saknas():
        a, b = ri(10, 60), ri(5, 39)
        if a + b > 100:
            return None
        if coin():
            return mcq("%d + □ = %d. Vilket tal står i rutan?" % (a, a + b), str(b), [str(b + 10), str(b + 1), str(a + b + a) if a + b + a <= 100 else str(b - 1)], "%d − %d = <b>%d</b>." % (a + b, a, b))
        return mcq("%d − □ = %d. Vilket tal står i rutan?" % (a + b, a), str(b), [str(b + 10), str(b - 1), str(a)] if a != b else [str(b + 10), str(b - 1), str(b + 1)], "%d − %d = %d. Svar: <b>%d</b>." % (a + b, b, a, b))

    def hundra():
        a = ri(1, 19) * 5
        return mcq("Hur mycket fattas från %d till 100?" % a, str(100 - a), [str(110 - a) if a % 10 else str(100 - a + 10), str(100 - a + 5), str(90 - a) if a < 90 else str(100 - a - 5)], "%d + %d = 100. Svar: <b>%d</b>." % (a, 100 - a, 100 - a))

    if lv == 2 and False:
        pass
    return dict(tiotal=tiotal, utan=utan, med=med, minus=minus, saknas=saknas, hundra=hundra)


def huvudrakning(lv):
    m = addsub100(lv)

    def dubbel():
        a = ri(6, 50)
        if coin():
            return mcq("Vad är dubbelt så mycket som %d?" % a, str(2 * a), [str(a + 2), str(2 * a + 10) if 2 * a + 10 <= 100 else str(2 * a - 2), str(2 * a + 1)], "%d + %d = <b>%d</b>." % (a, a, 2 * a))
        b = 2 * a
        return mcq("Vad är hälften av %d?" % b, str(a), [str(b - 2), str(a + 5), str(a - 1)], "%d + %d = %d. Hälften är <b>%d</b>." % (a, a, b, a))

    sets = [("Hela tiotal", [(m["tiotal"], 20)]), ("Hundrakamrater", [(m["hundra"], 19), (m["tiotal"], 1)]), ("Plus utan tiotalsövergång", [(m["utan"], 20)]),
            ("Dubbelt och hälften", [(dubbel, 20)]), ("Vilket tal saknas?", [(m["saknas"], 20)])]
    return unit("huvudrakning", "T", "Huvudräkning: tiotal, hundrakamrater och dubblor", "Huvudräkning",
                "Centrala metoder för beräkningar med naturliga tal vid huvudräkning. Additionens och subtraktionens samband.",
                "Arbetsblad om huvudräkning för årskurs 2: räkna med hela tiotal, hundrakamrater, plus utan tiotalsövergång, dubbelt och hälften och saknade tal. 100 uppgifter med facit.",
                "Tiotal för sig, ental för sig", "30 + 40 är som 3 + 4 fast tiotal.", sets,
                ["Hela tiotal räknar du som ental: 30 + 40 = 70 eftersom 3 + 4 = 7.", "Hundrakamrater är tal som tillsammans blir 100, till exempel 35 och 65.", "Dela upp i tiotal och ental: 34 + 25 = 50 + 9 = 59."],
                [("30 + 40", ["3 tiotal + 4 tiotal"], "70"), ("34 + 25", ["30 + 20 = 50", "4 + 5 = 9"], "59")],
                [["30 + 40 = 7", "Det är tiotal: 70"], ["35 och 75 blir 100", "35 + 65 = 100"], ["34 + 25 = 95", "Tiotal med tiotal: 59"]],
                [("Varför räkna i huvudet?", "Det går snabbt och hjälper dig att se om ett svar är rimligt."), ("Vad är en hundrakamrat till 40?", "60."), ("Hur räknar jag dubbelt?", "Lägg till talet en gång till.")])


def addsub_till_100(lv):
    m = addsub100(lv)

    def text_():
        nm = K().name()
        k = ri(0, 3)
        if k == 0:
            a, b = ri(20, 60), ri(12, 39)
            return mcq("%s har %d klistermärken och får %d till. Hur många har %s nu?" % (nm, a, b, nm), str(a + b), [str(a + b + 10), str(a + b - 10), str(a - b) if a > b else str(a + b + 1)], "%d + %d = <b>%d</b>." % (a, b, a + b)) if a + b <= 100 else None
        if k == 1:
            a, b = ri(40, 99), ri(12, 39)
            return mcq("En bok har %d sidor. %s har läst %d. Hur många sidor är kvar?" % (a, nm, b), str(a - b), [str(a + b) if a + b <= 100 else str(a - b + 1), str(a - b + 10), str(a - b - 10)], "%d − %d = <b>%d</b>." % (a, b, a - b))
        if k == 2:
            a, b = ri(20, 60), ri(15, 39)
            return mcq("Det är %d elever i matsalen. %d till kommer in. Hur många elever är det nu?" % (a, b), str(a + b), [str(a + b + 10), str(a + b - 1), str(a + b - 10)], "%d + %d = <b>%d</b>." % (a, b, a + b)) if a + b <= 100 else None
        a, b = ri(50, 99), ri(12, 45)
        return mcq("En hylla rymmer %d böcker. Det står %d böcker där. Hur många fler får plats?" % (a, b), str(a - b), [str(a + b) if a + b <= 100 else str(a - b + 2), str(a - b + 10), str(a - b - 1)], "%d − %d = <b>%d</b>." % (a, b, a - b))

    sets = [("Plus med tiotalsövergång", [(m["med"], 20)]), ("Minus", [(m["minus"], 20)]), ("Blandade tal", [(m["utan"], 10), (m["minus"], 10)]),
            ("Vilket tal saknas?", [(m["saknas"], 20)]), ("Berättelser", [(text_, 20)])]
    return unit("addition-och-subtraktion-till-100", "T", "Addition och subtraktion till 100", "Addition och subtraktion till 100",
                "Centrala metoder för beräkningar med naturliga tal vid huvudräkning och skriftliga metoder. Additionens och subtraktionens samband.",
                "Arbetsblad om addition och subtraktion till 100 för årskurs 2: plus med tiotalsövergång, minus, blandade tal, saknade tal och berättelser. 100 uppgifter med facit.",
                "Räkna tiotal och ental för sig", "Blir entalen 10 eller fler får du ett tiotal till.", sets,
                ["Räkna tiotalen för sig och entalen för sig: 47 + 26 = 60 + 13 = 73.", "Vid minus kan du ta bort tiotalen först och sedan entalen: 63 − 28 = 43 − 8 = 35.", "Kontrollera med det motsatta räknesättet: 35 + 28 = 63."],
                [("47 + 26", ["40 + 20 = 60", "7 + 6 = 13", "60 + 13"], "73"), ("63 − 28", ["63 − 20 = 43", "43 − 8"], "35")],
                [["47 + 26 = 613", "60 + 13 = 73"], ["63 − 28 = 45", "Du kan inte ta 3 − 8 baklänges: 35"], ["Kontrollerar inte svaret", "Räkna tillbaka med plus"]],
                [("Hur vet jag om det blir ett nytt tiotal?", "Om entalen tillsammans blir 10 eller mer."), ("Måste jag ställa upp?", "Nej, i årskurs 2 räknar du mest i huvudet eller med bilder."), ("Hur kontrollerar jag?", "Gör det motsatta räknesättet.")])


# ============================================================ problemlösning
def problem(lv):
    top = 20 if lv == 1 else 100

    def plus():
        nm = K().name()
        k = ch(KINDS)
        a = ri(2, top // 2 if lv == 2 else 10)
        b = ri(2, top - a)
        if a + b > top:
            return None
        return mcq("%s har %s. %s får %d till. Hur många har %s nu?" % (nm, sak(a, k), nm, b, nm), str(a + b), [str(a + b + 1), str(abs(a - b)) if a != b else str(a + b - 1), str(a + b - 1)], "%d + %d = <b>%d</b>." % (a, b, a + b))

    def minus():
        nm = K().name()
        k = ch(KINDS)
        a = ri(5, top)
        b = ri(1, a - 1)
        return mcq("Det finns %s. %s tar %d. Hur många är kvar?" % (sak(a, k), nm, b), str(a - b), [str(a + b) if a + b <= top else str(a - b + 2), str(a - b + 1), str(b) if b != a - b else str(a - b - 1)], "%d − %d = <b>%d</b>." % (a, b, a - b))

    def fler():
        n1, n2 = K().two()
        a, b = ri(2, top - 2), ri(2, top - 2)
        if a == b:
            return None
        k = ch(KINDS)
        hi, lo = (n1, n2) if a > b else (n2, n1)
        return mcq("%s har %s och %s har %s. Hur många fler har %s?" % (n1, sak(a, k), n2, sak(b, k), hi), str(abs(a - b)), [str(a + b) if a + b <= top * 2 else str(abs(a - b) + 2), str(max(a, b)), str(abs(a - b) + 1)], "%d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))

    def tva():
        nm = K().name()
        a, b, c = ri(3, top // 2), ri(1, top // 4 + 1), ri(1, top // 4 + 1)
        if a + b - c < 0 or a + b > top:
            return None
        return mcq("På en buss sitter %d personer. Vid en hållplats kliver %d på och %d av. Hur många sitter på bussen nu?" % (a, b, c), str(a + b - c), [str(a + b + c) if a + b + c <= top + 5 else str(a + b - c + 1), str(a - b + c) if a - b + c >= 0 and a - b + c != a + b - c else str(a + b - c + 2), str(a + b - c - 1) if a + b - c else "2"], "%d + %d − %d = <b>%d</b>." % (a, b, c, a + b - c))

    def ben():
        k = ri(0, 2)
        if k == 0:
            n = ri(2, 5 if lv == 1 else 10)
            return mcq("Det står %d hundar i en park. Hur många ben har hundarna tillsammans?" % n, str(4 * n), [str(n + 4), str(2 * n), str(4 * n + 4)], "Varje hund har 4 ben. %s = <b>%d</b>." % (" + ".join(["4"] * n), 4 * n))
        if k == 1:
            n = ri(2, 6 if lv == 1 else 10)
            return mcq("%d barn har två vantar var. Hur många vantar är det?" % n, str(2 * n), [str(n + 2), str(n), str(2 * n + 2)], "%s = <b>%d</b>." % (" + ".join(["2"] * n), 2 * n))
        n = ri(2, 4 if lv == 1 else 10)
        return mcq("En cykel har 2 hjul. Hur många hjul har %d cyklar?" % n, str(2 * n), [str(n + 2), str(n), str(2 * n + 1)], "%s = <b>%d</b>." % (" + ".join(["2"] * n), 2 * n))

    sets = [("Plus i vardagen", [(plus, 20)]), ("Minus i vardagen", [(minus, 20)]), ("Hur många fler?", [(fler, 20)]), ("Två steg", [(tva, 20)]), ("Rita och räkna", [(ben, 12), (plus, 4), (minus, 4)])]
    return unit("problemlosning", "P", "Problemlösning: berättelser med plus och minus", "Problemlösning",
                "Strategier för matematisk problemlösning i vardagliga situationer. Matematisk formulering av frågeställningar utifrån enkla vardagliga situationer.",
                "Arbetsblad om problemlösning för årskurs %d: berättelser med plus och minus, hur många fler, två steg och rita och räkna. 100 uppgifter med facit." % lv,
                "Läs, rita och räkna", "Tänk: blir det fler eller färre?", sets,
                ["Läs berättelsen noga. Vad vet du och vad ska du ta reda på?", "Rita en bild om det hjälper. Fundera på om det blir fler (plus) eller färre (minus).", "Hur många fler räknar du med minus: det största minus det minsta."],
                [("Ali har 8 kulor och får 5 till", ["Det blir fler: 8 + 5"], "13"), ("Maja har 12 och Olle 7. Hur många fler har Maja?", ["12 − 7"], "5")],
                [["Plus när det blir färre", "Tar någon bort blir det minus"], ["Hur många fler räknas med plus", "Hur många fler är skillnaden: minus"], ["Glömmer andra steget", "Läs hela berättelsen igen"]],
                [("Vad gör jag om jag inte förstår?", "Läs igen och rita en bild."), ("Hur vet jag om det är plus eller minus?", "Blir det fler är det plus, blir det färre är det minus."), ("Får jag använda fingrarna eller saker?", "Ja, det är ett bra sätt att lösa problem.")])


# ============================================================ dubbelt och hälften (åk 1)
def dubbelt(lv):
    def dub():
        n = ri(1, 10)
        k = ch(KINDS)
        if coin():
            pic = P(KP.two_groups_svg(n, k, n, k, "+"), "%s plus %s" % (sak(n, k), sak(n, k)))
            return mcq("Hur många blir det om antalet dubblas?" + pic, str(2 * n), [str(n + 1), str(2 * n + 1), str(n)], "%d + %d = <b>%d</b>." % (n, n, 2 * n))
        return mcq("Vad är dubbelt så mycket som %d?" % n, str(2 * n), [str(n + 2), str(2 * n + 1), str(2 * n - 1) if 2 * n > 1 else "3"], "Dubbelt är talet två gånger: %d + %d = <b>%d</b>." % (n, n, 2 * n))

    def halv():
        n = ri(1, 10)
        k = ch(KINDS)
        if coin():
            pic = P(KP.row_svg(2 * n, k), sak(2 * n, k))
            return mcq("Dela %s i två lika stora högar. Hur många blir det i varje?" % pl(k) + pic, str(n), [str(2 * n), str(n + 1), str(n - 1) if n > 1 else "3"], "%d + %d = %d, så hälften är <b>%d</b>." % (n, n, 2 * n, n))
        return mcq("Vad är hälften av %d?" % (2 * n), str(n), [str(2 * n - 2) if 2 * n - 2 != n else "4", str(n + 1), str(4 * n) if 4 * n <= 40 else str(n + 2)], "%d + %d = %d. Hälften är <b>%d</b>." % (n, n, 2 * n, n))

    def nara():
        n = ri(2, 9)
        return mcq("Du vet att %d + %d = %d. Vad är %d + %d?" % (n, n, 2 * n, n, n + 1), str(2 * n + 1), [str(2 * n), str(2 * n + 2), str(n + 1)], "Ett mer än dubbelt: %d + 1 = <b>%d</b>." % (2 * n, 2 * n + 1))

    def tarning():
        n = ri(1, 6)
        pic = P(KP.dice_svg([n, n]), "två lika tärningar")
        return mcq("Två tärningar visar lika. Hur många prickar är det tillsammans?" + pic, str(2 * n), [str(n), str(2 * n + 1), str(2 * n - 1) if n > 1 else "3"], "Dubbelt %d är <b>%d</b>." % (n, 2 * n))

    def udda():
        n = ri(1, 20)
        r = "Jämnt" if n % 2 == 0 else "Udda"
        return mcq("Kan %d delas i två lika stora delar utan rest? Är talet jämnt eller udda?" % n, r, ["Udda" if r == "Jämnt" else "Jämnt", "Både jämnt och udda", "Varken jämnt eller udda"], "%s. Svar: <b>%s</b>." % ("%d = %d + %d" % (n, n // 2, n // 2) if n % 2 == 0 else "Det blir en över", r))

    sets = [("Dubbelt", [(dub, 20)]), ("Hälften", [(halv, 20)]), ("Dubblor med tärningar", [(tarning, 6), (dub, 14)]), ("Nästan dubbelt", [(nara, 8), (halv, 12)]), ("Jämnt eller udda", [(udda, 20)])]
    return unit("dubbelt-och-halften", "T", "Dubbelt och hälften: dubblor och att dela lika", "Dubbelt och hälften",
                "Centrala metoder för beräkningar med naturliga tal vid huvudräkning. Delning av helheter och antal i lika stora delar.",
                "Arbetsblad om dubbelt och hälften för årskurs 1: dubblor, hälften, tärningar, nästan dubbelt och jämna och udda tal. 100 uppgifter med facit.",
                "Dubbelt av 6 är 12", "Hälften av 12 är 6.", sets,
                ["Dubbelt betyder två gånger så många: dubbelt av 4 är 4 + 4 = 8.", "Hälften betyder att dela i två lika stora delar: hälften av 8 är 4.", "Kan du dubblorna kan du räkna nästan-dubblor: 6 + 7 = 6 + 6 + 1 = 13."],
                [("Dubbelt av 7", ["7 + 7"], "14"), ("Hälften av 10", ["5 + 5 = 10"], "5")],
                [["Dubbelt av 7 är 9", "Dubbelt är 7 + 7 = 14"], ["Hälften av 10 är 2", "Två lika delar: 5 och 5"], ["7 är jämnt", "7 kan inte delas lika: udda"]],
                [("Vad är ett jämnt tal?", "Ett tal som kan delas i två lika stora delar: 2, 4, 6, 8 …"), ("Vad är dubblor?", "Plus med två lika tal, som 5 + 5."), ("Hur hjälper dubblor mig?", "De gör det lätt att räkna nästan-dubblor.")])


# ============================================================ udda och jämna tal (åk 2)
def udda(lv):
    def vilket():
        xs = sh(set(ri(1, 99) for _ in range(8)))
        j = [x for x in xs if x % 2 == 0]
        u = [x for x in xs if x % 2]
        if coin():
            if not j or len(u) < 3:
                return None
            return MQ("Vilket tal är jämnt:", str(j[0]), [str(x) for x in u], "Jämna tal slutar på 0, 2, 4, 6 eller 8: <b>%d</b>." % j[0])
        if not u or len(j) < 3:
            return None
        return MQ("Vilket tal är udda:", str(u[0]), [str(x) for x in j], "Udda tal slutar på 1, 3, 5, 7 eller 9: <b>%d</b>." % u[0])

    def nasta():
        n = ri(1, 97)
        if coin():
            v = n + 1 if n % 2 else n + 2
            return mcq("Vilket är nästa jämna tal efter %d?" % n, str(v), [str(n + 1) if n % 2 == 0 else str(n + 2), str(v + 2), str(v - 2) if v - 2 > n else str(v + 4)], "Jämna tal: hoppa till nästa tal som slutar på 0, 2, 4, 6 eller 8: <b>%d</b>." % v)
        v = n + 1 if n % 2 == 0 else n + 2
        return mcq("Vilket är nästa udda tal efter %d?" % n, str(v), [str(n + 1) if n % 2 else str(n + 2), str(v + 2), str(v + 4)], "Udda tal slutar på 1, 3, 5, 7 eller 9: <b>%d</b>." % v)

    def summa():
        a, b = ri(1, 40), ri(1, 40)
        r = "jämn" if (a + b) % 2 == 0 else "udda"
        return mcq("Är summan %d + %d jämn eller udda?" % (a, b), r, ["udda" if r == "jämn" else "jämn", "både jämn och udda", "det går inte att säga"], "%d + %d = %d. Det är <b>%s</b>." % (a, b, a + b, r))

    def rakna():
        lo = ri(1, 80)
        hi = lo + ri(5, 15)
        if hi > 100:
            return None
        j = sum(1 for x in range(lo, hi + 1) if x % 2 == 0)
        return mcq("Hur många jämna tal finns det från %d till %d?" % (lo, hi), str(j), [str(j + 1), str(j - 1), str(hi - lo + 1)], "De jämna talen är %s: <b>%d</b>." % (", ".join(str(x) for x in range(lo, hi + 1) if x % 2 == 0), j))

    def par():
        k = ch(KINDS)
        n = ri(3, 20)
        pic = P(KP.array_svg(2, n // 2, k) if n % 2 == 0 else KP.row_svg(n, k, 5), sak(n, k))
        r = "jämnt" if n % 2 == 0 else "udda"
        return mcq("Det finns %s. Kan de stå två och två utan att någon blir över? Är antalet jämnt eller udda?" % sak(n, k) + pic, r, ["udda" if r == "jämnt" else "jämnt", "både och", "inget av dem"], "%d %s. Antalet är <b>%s</b>." % (n, "kan delas i par" if n % 2 == 0 else "ger en över", r))

    sets = [("Udda eller jämnt?", [(vilket, 20)]), ("Nästa udda eller jämna tal", [(nasta, 20)]), ("Två och två", [(par, 20)]), ("Summor", [(summa, 20)]), ("Räkna jämna tal", [(rakna, 20)])]
    return unit("udda-och-jamna-tal", "T", "Udda och jämna tal: känna igen och räkna", "Udda och jämna tal",
                "Naturliga tal och deras egenskaper. Jämna och udda tal.",
                "Arbetsblad om udda och jämna tal för årskurs 2: känna igen udda och jämna tal, nästa jämna tal, par, summor och att räkna jämna tal. 100 uppgifter med facit.",
                "Jämna tal slutar på 0, 2, 4, 6, 8", "Udda tal slutar på 1, 3, 5, 7, 9.", sets,
                ["Ett jämnt tal kan delas i två lika stora delar. Saker kan stå två och två utan att någon blir över.", "Titta på entalssiffran: 0, 2, 4, 6, 8 ger jämnt och 1, 3, 5, 7, 9 ger udda.", "Jämnt + jämnt och udda + udda blir jämnt. Jämnt + udda blir udda."],
                [("Är 46 jämnt?", ["Entalssiffran är 6"], "Ja"), ("7 + 9", ["Udda + udda"], "16, jämnt")],
                [["Tror att 30 är udda för att 3 är udda", "Titta på entalssiffran: 0 ger jämnt"], ["Udda + udda blir udda", "Udda + udda blir jämnt: 3 + 5 = 8"], ["Är 0 udda?", "0 är ett jämnt tal"]],
                [("Är 0 jämnt?", "Ja, 0 är ett jämnt tal."), ("Varför spelar entalssiffran roll?", "Alla tiotal är jämna, så bara entalen avgör."), ("Var används udda och jämnt?", "Till exempel på husnummer: jämna på ena sidan gatan och udda på den andra.")])


# ============================================================ tiotal och ental (åk 2)
def tiotal(lv):
    def antal():
        n = ri(11, 99)
        t, e = divmod(n, 10)
        if coin():
            return mcq("Hur många tiotal finns det i %d?" % n, str(t), [str(e) if e != t else str(t + 1), str(n), str(t + 1) if e != t + 1 else str(t - 1)], "%d = %d tiotal och %d ental. Svar: <b>%d</b>." % (n, t, e, t))
        return mcq("Hur många ental finns det i %d?" % n, str(e), [str(t) if e != t else str(e + 1), str(n), str(e + 1) if t != e + 1 else str(e + 2)], "%d = %d tiotal och %d ental. Svar: <b>%d</b>." % (n, t, e, e))

    def bygg():
        t, e = ri(1, 9), ri(0, 9)
        n = 10 * t + e
        return mcq("%d tiotal och %d ental. Vilket tal är det?" % (t, e), str(n), [str(10 * e + t) if e else str(n + 1), str(t + e), "%d%d" % (t, e + 1) if e < 9 else str(n - 1)], "%d tiotal är %d och %d ental till: <b>%d</b>." % (t, 10 * t, e, n))

    def utv():
        n = ri(11, 99)
        t, e = divmod(n, 10)
        if e == 0:
            return None
        return mcq("Vilket sätt att dela upp %d är rätt?" % n, "%d + %d" % (10 * t, e), ["%d + %d" % (t, e), "%d + %d" % (10 * e, t), "%d + %d" % (10 * t, 10 * e)], "%d = <b>%d + %d</b>." % (n, 10 * t, e))

    def bild():
        t, e = ri(1, 9), ri(0, 9)
        n = 10 * t + e
        pic = P(basemat(0, t, e), "%d tiotal och %d ental" % (t, e))
        return mcq("Vilket tal visar tiostavarna och entalskuberna?" + pic, str(n), [str(10 * e + t) if e and e != t else str(n + 10) if n + 10 < 100 else str(n - 10), str(t + e), str(n + 1)], "%d tiostavar och %d kuber: <b>%d</b>." % (t, e, n))

    def tabell():
        n = ri(10, 99)
        t, e = divmod(n, 10)
        if coin():
            return mcq("Vilken siffra står på tiotalens plats i %d?" % n, str(t), [str(e) if e != t else str(t + 1), str(t + 1) if e != t + 1 else str(t + 2), str(t - 1) if t > 1 else str(t + 3)], "Tiotalssiffran står först: <b>%d</b>." % t)
        return mcq("Vad är siffran %d värd i talet %d?" % (t, n), str(10 * t), [str(t), str(t + e) if t + e != 10 * t else str(100), str(10 * t + 10)], "Siffran %d står på tiotalens plats och är värd <b>%d</b>." % (t, 10 * t))

    sets = [("Tiostavar och kuber", [(bild, 20)]), ("Tiotal och ental", [(antal, 20)]), ("Bygg talet", [(bygg, 20)]), ("Dela upp talet", [(utv, 20)]), ("Siffrans värde", [(tabell, 20)])]
    return unit("tiotal-och-ental", "T", "Tiotal och ental: positionssystemet till 100", "Tiotal och ental",
                "Positionssystemet för tal. Hur talen kan delas upp i tiotal och ental och hur siffrornas värde beror på var de står.",
                "Arbetsblad om tiotal och ental för årskurs 2: tiostavar och kuber, tiotal och ental i ett tal, bygg tal, dela upp tal och siffrans värde. 100 uppgifter med facit.",
                "58 = 50 + 8", "Siffran 5 är värd 50 eftersom den står på tiotalens plats.", sets,
                ["I ett tvåsiffrigt tal visar den första siffran tiotal och den andra ental.", "58 betyder 5 tiotal och 8 ental. Det är 50 + 8.", "Samma siffra kan vara värd olika mycket: i 35 är 3 värd 30 men i 53 är 3 värd 3."],
                [("6 tiotal och 4 ental", ["60 + 4"], "64"), ("Dela upp 72", ["7 tiotal = 70", "2 ental = 2"], "70 + 2")],
                [["Skriver 6 tiotal och 4 ental som 46", "Tiotalen först: 64"], ["Tror att 5 i 58 är värd 5", "Den står på tiotalens plats: 50"], ["Glömmer 0 i 40", "4 tiotal och 0 ental skrivs 40"]],
                [("Varför står tiotalen först?", "Det är så vårt positionssystem fungerar. Platsen bestämmer värdet."), ("Hur många ental är ett tiotal?", "10."), ("Vad är en tiostav?", "En stav av 10 kuber som visar ett tiotal.")])


# ============================================================ multiplikation och delning (åk 2)
def multiplikation(lv):
    def grupper():
        g, n = ri(2, 5), ch([2, 3, 4, 5, 10])
        if g * n > 30 and n != 10:
            return None
        k = ch(KINDS)
        pic = P(KP.groups_svg([(n, k)] * g) if n <= 5 else A.groups(g, n), "%d grupper med %d i varje" % (g, n))
        return mcq("Det är %d grupper med %d i varje. Hur många är det sammanlagt?" % (g, n) + pic, str(g * n), [str(g + n), str(g * n + n), str(g * n - n)], "%s = %d · %d = <b>%d</b>." % (" + ".join([str(n)] * g), g, n, g * n))

    def upprepad():
        g, n = ri(2, 6), ch([2, 5, 10, 3, 4])
        q = " + ".join([str(n)] * g)
        return mcq("Vilken multiplikation är samma sak som %s?" % q, "%d · %d" % (g, n), ["%d · %d" % (g + 1, n), "%d + %d" % (g, n), "%d · %d" % (g, n + 1)], "%d stycken %d: <b>%d · %d</b> = %d." % (g, n, g, n, g * n))

    def tabell():
        n = ch([2, 5, 10])
        g = ri(1, 10)
        return mcq("%d · %d = ?" % (g, n), str(g * n), [str(g * n + n), str(g * n - n) if g > 1 else str(g + n), str(g + n) if g + n != g * n else str(g * n + 1)], "Räkna %d-hopp %d gånger: <b>%d</b>." % (n, g, g * n))

    def rader():
        r, c = ri(2, 5), ri(2, 6)
        pic = P(A.dots(r, c), "%d rader med %d prickar" % (r, c))
        return mcq("Hur många prickar är det?" + pic, str(r * c), [str(r + c), str(r * c + c), str(r * c - 1)], "%d rader med %d i varje: %d · %d = <b>%d</b>." % (r, c, r, c, r * c))

    def text_():
        n = ch([2, 5, 10])
        g = ri(2, 9)
        sak_ = {2: ("par strumpor", "strumpor", 2), 5: ("handar", "fingrar", 5), 10: ("tiokronor", "kronor", 10)}[n]
        if n == 2:
            return mcq("%s har %d par strumpor. Hur många strumpor är det?" % (K().name(), g), str(2 * g), [str(g + 2), str(g), str(2 * g + 2)], "%d · 2 = <b>%d</b>." % (g, 2 * g))
        if n == 5:
            return mcq("%d barn håller upp en hand var. Hur många fingrar är det?" % g, str(5 * g), [str(g + 5), str(5 * g + 5), str(10 * g)], "%d · 5 = <b>%d</b>." % (g, 5 * g))
        return mcq("%s har %d tiokronor. Hur många kronor är det?" % (K().name(), g), str(10 * g), [str(g + 10), str(g), str(10 * g + 10)], "%d · 10 = <b>%d kr</b>." % (g, 10 * g))

    sets = [("Lika stora grupper", [(grupper, 20)]), ("Upprepad addition", [(upprepad, 20)]), ("Rader och kolumner", [(rader, 20)]), ("2-, 5- och 10-hopp", [(tabell, 20)]), ("Berättelser", [(text_, 20)])]
    return unit("multiplikation", "T", "Multiplikation: lika stora grupper och upprepad addition", "Multiplikation",
                "Multiplikationens innebörd som upprepad addition och lika stora grupper. Centrala metoder för beräkningar vid huvudräkning.",
                "Arbetsblad om multiplikation för årskurs 2: lika stora grupper, upprepad addition, rader och kolumner, 2-, 5- och 10-hopp och berättelser. 100 uppgifter med facit.",
                "3 · 4 = 4 + 4 + 4", "Antal grupper gånger antal i varje grupp.", sets,
                ["Multiplikation är upprepad addition: 3 · 4 betyder tre fyror, 4 + 4 + 4 = 12.", "Tänk på lika stora grupper: 3 påsar med 4 kakor i varje är 3 · 4 = 12 kakor.", "Hoppa på tallinjen: 2-hopp, 5-hopp och 10-hopp."],
                [("4 grupper med 5 i varje", ["5 + 5 + 5 + 5"], "4 · 5 = 20"), ("6 · 2", ["2, 4, 6, 8, 10, 12"], "12")],
                [["3 · 4 = 7", "3 · 4 = 4 + 4 + 4 = 12"], ["Grupperna är olika stora", "Multiplikation kräver lika stora grupper"], ["Räknar ett hopp för lite", "Räkna hoppen på fingrarna"]],
                [("Vad betyder tecknet ·?", "Gånger, alltså multiplikation."), ("Spelar ordningen roll?", "Nej, 3 · 4 = 4 · 3 = 12."), ("Vilka tabeller ska jag börja med?", "2:ans, 5:ans och 10:ans tabell.")])


def delning(lv):
    def dela():
        p, n = ri(2, 5), ri(2, 6)
        k = ch(KINDS)
        pic = P(KP.row_svg(p * n, k, 10), sak(p * n, k), lg=p * n > 10)
        return mcq("%s ska delas lika mellan %d barn. Hur många får var och en?" % (cap1(sak(p * n, k)), p) + pic, str(n), [str(p), str(n + 1), str(p * n - p)] if p != n else [str(n + 1), str(n - 1), str(p * n)], "%d delat på %d är %d eftersom %d · %d = %d. Svar: <b>%d</b>." % (p * n, p, n, p, n, p * n, n))

    def innehall():
        n, g = ch([2, 5, 10]), ri(2, 8)
        return mcq("Du har %d kakor och lägger %d i varje påse. Hur många påsar blir det?" % (n * g, n), str(g), [str(n * g - n), str(g + 1), str(n)] if n != g else [str(g + 1), str(g - 1), str(n * g)], "%d : %d = %d eftersom %d · %d = %d. Svar: <b>%d påsar</b>." % (n * g, n, g, g, n, n * g, g))

    def tal():
        n, g = ch([2, 5, 10]), ri(1, 10)
        return mcq("%d : %d = ?" % (n * g, n), str(g), [str(g + 1), str(n * g - n) if n * g - n != g else str(g + 2), str(n)] if n != g else [str(g + 1), str(g - 1), str(n * g)], "%d · %d = %d, så %d : %d = <b>%d</b>." % (g, n, n * g, n * g, n, g))

    def halv():
        n = ri(1, 25)
        k = ri(0, 1)
        if k == 0:
            return mcq("%s och %s delar lika på %d kulor. Hur många får var och en?" % K().two() + "" if False else "Två syskon delar lika på %d kulor. Hur många får var och en?" % (2 * n), str(n), [str(2 * n - 2) if 2 * n - 2 != n else str(n + 2), str(n + 1), str(n - 1) if n > 1 else str(n + 3)], "Hälften av %d är <b>%d</b>." % (2 * n, n))
        g = ri(3, 4)
        m = ri(1, 6)
        return mcq("%d vänner delar lika på %d jordgubbar. Hur många får var och en?" % (g, g * m), str(m), [str(g * m - g), str(m + 1), str(g)] if m != g and g * m - g != m else [str(m + 1), str(m + 2), str(g * m)], "%d : %d = <b>%d</b>." % (g * m, g, m))

    def bild():
        p, n = ri(2, 4), ri(2, 5)
        k = ch(KINDS)
        pic = P(KP.groups_svg([(n, k)] * p), "%d grupper med %d i varje" % (p, n))
        return mcq("%s är fördelade i lika stora grupper. Hur många grupper är det och hur många i varje?" % cap1(sak(p * n, k)) + pic, "%d grupper med %d" % (p, n), ["%d grupper med %d" % (n, p) if n != p else "%d grupper med %d" % (p + 1, n), "%d grupper med %d" % (p, n + 1), "%d grupper med %d" % (1, p * n)], "Räkna grupperna och sakerna i en grupp: <b>%d grupper med %d</b>." % (p, n))

    sets = [("Dela lika", [(dela, 20)]), ("Hur många grupper?", [(innehall, 20)]), ("Dela i tvåor, femmor och tior", [(tal, 20)]), ("Dela mellan vänner", [(halv, 20)]), ("Grupper i bild", [(bild, 20)])]
    return unit("delning", "T", "Delning: dela lika och dela i grupper", "Delning",
                "Divisionens innebörd som delning i lika stora delar och som innehåll. Samband mellan multiplikation och division.",
                "Arbetsblad om delning för årskurs 2: dela lika, hur många grupper, dela i tvåor, femmor och tior, dela mellan vänner och grupper i bild. 100 uppgifter med facit.",
                "Dela lika så att alla får lika många", "12 : 3 = 4 eftersom 3 · 4 = 12.", sets,
                ["Dela lika betyder att alla får lika många. 12 kakor delat på 3 barn ger 4 kakor var.", "Du kan också fråga hur många grupper det blir: 12 kakor i påsar med 3 i varje ger 4 påsar.", "Delning och gånger hör ihop: 12 : 3 = 4 eftersom 3 · 4 = 12."],
                [("15 kulor delas lika på 3", ["3 · 5 = 15"], "5 var"), ("20 i påsar om 5", ["5 · 4 = 20"], "4 påsar")],
                [["Delar ut olika många", "Alla ska få lika många"], ["12 : 3 = 9", "Dela, inte minus: 12 : 3 = 4"], ["Blandar ihop antal grupper och antal i varje", "Läs frågan noga"]],
                [("Vad betyder tecknet :?", "Delat med, alltså division."), ("Kan det bli rest?", "Ja, om det inte går jämnt ut. Det lär du dig mer om i årskurs 3."), ("Hur kontrollerar jag?", "Multiplicera svaret med antalet grupper.")])


def cap1(s):
    return s[0].upper() + s[1:]


# ============================================================ halvor och fjärdedelar (åk 2)
def brak(lv):
    NAMN = {(1, 2): "en halv", (1, 3): "en tredjedel", (2, 3): "två tredjedelar", (1, 4): "en fjärdedel", (2, 4): "två fjärdedelar", (3, 4): "tre fjärdedelar"}

    def del_():
        a, b = ch(list(NAMN))
        col = ch(["#f4a261", "#7fb3d5", "#81b29a", "#e07a5f", "#f2c94c"])
        pic = P(A.pie(b, a, col=col) if coin() else A.bar_frac(b, a, col=col), "figur i %d lika delar, %d färgade" % (b, a))
        return mcq("Hur stor del är färgad?" + pic, NAMN[(a, b)], [v for k, v in NAMN.items() if k != (a, b) and k[1] != b][:2] + [v for k, v in NAMN.items() if k != (a, b) and k[1] == b][:1] or ["en hel"], "Figuren är delad i %d lika delar och %d är färgad%s: <b>%s</b>." % (b, a, "e" if a > 1 else "", NAMN[(a, b)]))

    def lika():
        b = ch([2, 3, 4])
        ok = coin()
        if ok:
            pic = P(A.bar_frac(b, 1), "remsa i %d lika delar" % b)
        else:
            s = []
            ws = [ri(30, 80) for _ in range(b)]
            x = 6
            for i, w in enumerate(ws):
                s.append("<rect x='%d' y='6' width='%d' height='40' fill='%s' stroke='%s' stroke-width='2'/>" % (x, w, "#7fb3d5" if i == 0 else "#ffffff", INK))
                x += w
            if max(ws) - min(ws) < 15:
                return None
            pic = P(wrap(x + 6, 52, "".join(s), "remsa i olika stora delar"), "remsa i olika stora delar")
        name = {2: "halvor", 3: "tredjedelar", 4: "fjärdedelar"}[b]
        r = "Ja, delarna är lika stora" if ok else "Nej, delarna är inte lika stora"
        return mcq("Är remsan delad i %s?" % name + pic, r, ["Nej, delarna är inte lika stora" if ok else "Ja, delarna är lika stora", "Ja, det finns %d delar" % b if not ok else "Nej, det finns för många delar", "Det går inte att se"], "För att det ska vara %s måste alla delar vara lika stora. <b>%s</b>." % (name, r))

    def antal():
        b = ch([2, 4, 2, 3])
        n = b * ri(1, 10)
        name = {2: "Hälften", 3: "En tredjedel", 4: "En fjärdedel"}[b]
        return mcq("%s av %d är?" % (name, n), str(n // b), [str(n - n // b), str(n // b + 1), str(n * 2) if n * 2 <= 40 else str(n // b + 2)], "Dela %d i %d lika delar: <b>%d</b>." % (n, b, n // b))

    def pizza():
        b = ch([2, 4])
        n = ri(1, b)
        nm = K().name()
        if b == 2:
            return mcq("En pizza delas i 2 lika bitar. %s äter %d bit%s. Hur stor del av pizzan äter %s?" % (nm, n, "ar" if n > 1 else "", nm), "en halv" if n == 1 else "en hel", ["en fjärdedel", "två halvor" if n == 1 else "en halv", "tre fjärdedelar"], "%d av 2 bitar: <b>%s</b>." % (n, "en halv" if n == 1 else "en hel"))
        r = {1: "en fjärdedel", 2: "två fjärdedelar", 3: "tre fjärdedelar", 4: "en hel"}[n]
        return mcq("En pizza delas i 4 lika bitar. %s äter %d bit%s. Hur stor del av pizzan äter %s?" % (nm, n, "ar" if n > 1 else "", nm), r, [x for x in ("en fjärdedel", "två fjärdedelar", "tre fjärdedelar", "en hel", "en halv") if x != r][:3], "%d av 4 lika bitar: <b>%s</b>." % (n, r))

    def jamfor():
        P_ = [("en halv", "en fjärdedel", "en halv"), ("en tredjedel", "en halv", "en halv"), ("en fjärdedel", "en tredjedel", "en tredjedel"), ("tre fjärdedelar", "en halv", "tre fjärdedelar")]
        a, b, r = ch(P_)
        return mcq("Vilket är mest av samma pizza: %s eller %s?" % (a, b), r, [b if r == a else a, "lika mycket", "det går inte att säga"], "Ju färre delar pizzan delas i, desto större är varje del. <b>%s</b> är mest." % cap1(r))

    sets = [("Hur stor del är färgad?", [(del_, 20)]), ("Lika stora delar", [(lika, 20)]), ("Del av ett antal", [(antal, 20)]), ("Pizzabitar", [(pizza, 8), (del_, 12)]), ("Jämför delar", [(jamfor, 4), (lika, 8), (pizza, 8)])]
    return unit("halvor-och-fjardedelar", "T", "Halvor, tredjedelar och fjärdedelar", "Halvor och fjärdedelar",
                "Del av helhet och del av antal. Hur delar kan benämnas och uttryckas som enkla bråk.",
                "Arbetsblad om halvor och fjärdedelar för årskurs 2: hur stor del är färgad, lika stora delar, del av ett antal, pizzabitar och att jämföra delar. 100 uppgifter med facit.",
                "Lika stora delar", "En fjärdedel är en av fyra lika stora delar.", sets,
                ["En halv är en av två lika stora delar. En fjärdedel är en av fyra lika stora delar.", "Delarna måste vara lika stora. Annars är det inte halvor eller fjärdedelar.", "Hälften av 8 är 4. En fjärdedel av 8 är 2."],
                [("Hälften av 10", ["Dela i 2 lika delar"], "5"), ("En fjärdedel av 12", ["Dela i 4 lika delar"], "3")],
                [["Två olika stora bitar är halvor", "Halvor måste vara lika stora"], ["En fjärdedel är mer än en halv", "Fler delar gör varje del mindre"], ["En fjärdedel av 12 är 4", "12 delat i 4 delar: 3"]],
                [("Varför är en fjärdedel mindre än en halv?", "Om något delas i fyra delar blir varje bit mindre än om det delas i två."), ("Vad är två fjärdedelar?", "Lika mycket som en halv."), ("Var används halvor?", "Till exempel när man delar en frukt eller ett äpple.")])


# ============================================================ mönster
def monster(lv):
    top = 20 if lv == 1 else 100
    SH = ["circle", "square", "triangle"]
    COL = ["red", "blue", "yellow", "green"]
    NAMN = {"circle": "cirkel", "square": "kvadrat", "triangle": "triangel"}
    FARG = {"red": "röd", "blue": "blå", "yellow": "gul", "green": "grön"}

    def figur():
        unit_ = [(ch(SH), ch(COL)) for _ in range(ri(2, 3))]
        if len(set(unit_)) < 2:
            return None
        seq = (unit_ * 4)[:ri(5, 7)]
        nxt = unit_[len(seq) % len(unit_)]
        s = [KP.shape(k, 26 + i * 44, 28, 16, c) for i, (k, c) in enumerate(seq)]
        x = 26 + len(seq) * 44
        s.append("<rect x='%d' y='10' width='36' height='36' fill='none' stroke='%s' stroke-width='1.6' stroke-dasharray='4 3'/>" % (x - 18, RED) + text(x, 34, "?", 18, col=RED))
        pic = P(wrap(x + 30, 56, "".join(s), "mönster"), "mönster med figurer")
        name = lambda t: "%s %s" % ({"röd": "röd", "blå": "blå", "gul": "gul", "grön": "grön"}[FARG[t[1]]], NAMN[t[0]])
        opts = list(set(unit_) | {(ch(SH), ch(COL)) for _ in range(5)})
        w = [name(o) for o in opts if o != nxt]
        return mcq("Vad kommer sedan i mönstret?" + pic, name(nxt), w, "Mönstret upprepar %s. Nästa är en <b>%s</b>." % (" – ".join(name(t) for t in unit_), name(nxt)))

    def tal():
        st = ch([1, 2, 5, 10] if lv == 2 else [1, 2, 3, 5])
        n = ri(0, top - 5 * st)
        seq = [n + st * i for i in range(4)]
        return mcq("Vilket tal kommer sedan: %s, …?" % ", ".join(map(str, seq)), str(n + 4 * st), [str(n + 4 * st + 1), str(n + 3 * st + 1) if st > 1 else str(n + 6), str(n + 5 * st) if n + 5 * st <= top else str(n + 4 * st - 1)], "Det ökar med %d varje gång: <b>%d</b>." % (st, n + 4 * st))

    def bak():
        st = ch([1, 2, 5, 10] if lv == 2 else [1, 2])
        n = ri(5 * st, top)
        seq = [n - st * i for i in range(4)]
        return mcq("Vilket tal kommer sedan: %s, …?" % ", ".join(map(str, seq)), str(n - 4 * st), [str(n - 4 * st + 1), str(n - 3 * st), str(n - 5 * st) if n - 5 * st >= 0 else str(n - 4 * st + 2)], "Det minskar med %d varje gång: <b>%d</b>." % (st, n - 4 * st))

    def lucka():
        st = ch([1, 2, 5, 10] if lv == 2 else [1, 2, 5])
        n = ri(0, top - 4 * st)
        i = ri(1, 3)
        seq = [str(n + st * j) if j != i else "__" for j in range(5)]
        return mcq("Vilket tal saknas: %s?" % ", ".join(seq), str(n + st * i), [str(n + st * i + 1), str(n + st * i - 1) if n + st * i else "1", str(n + st * (i + 1)) if st > 1 else str(n + i + 2)], "Det ökar med %d. Svar: <b>%d</b>." % (st, n + st * i))

    def regel():
        st = ch([2, 3, 5, 10] if lv == 2 else [2, 3, 5])
        n = ri(0, top - 4 * st)
        seq = [n + st * i for i in range(4)]
        return mcq("Vilken är regeln i talföljden %s?" % ", ".join(map(str, seq)), "Öka med %d" % st, ["Öka med %d" % (st + 1), "Minska med %d" % st, "Öka med %d" % (st * 2)], "Skillnaden mellan talen är %d: <b>öka med %d</b>." % (st, st))

    sets = [("Mönster med figurer", [(figur, 20)]), ("Talföljder framåt", [(tal, 20)]), ("Talföljder bakåt", [(bak, 20)]), ("Vilket tal saknas?", [(lucka, 20)]), ("Hitta regeln", [(regel, 20)])]
    return unit("monster", "A", "Mönster: figurmönster och talföljder", "Mönster",
                "Mönster i talföljder och enkla geometriska mönster. Hur mönster kan beskrivas, konstrueras och uttryckas.",
                "Arbetsblad om mönster för årskurs %d: mönster med figurer, talföljder framåt och bakåt, saknade tal och att hitta regeln. 100 uppgifter med facit." % lv,
                "Hitta det som upprepas", "Talföljder ökar eller minskar lika mycket varje gång.", sets,
                ["I ett figurmönster upprepas samma del om och om igen. Hitta delen som upprepas.", "I en talföljd ändras talen på samma sätt varje gång, till exempel med 2 eller 5.", "Hitta regeln genom att räkna skillnaden mellan två tal som står bredvid varandra."],
                [("2, 4, 6, 8, …", ["Det ökar med 2"], "10"), ("röd, blå, röd, blå, …", ["röd – blå upprepas"], "röd")],
                [["Tittar bara på de två sista", "Kontrollera regeln på alla tal"], ["Glömmer att mönstret kan minska", "Talföljder kan gå bakåt också"], ["Tar fel form i mönstret", "Säg mönstret högt"]],
                [("Var finns mönster?", "I tapeter, tyger, pärlband och i talraden."), ("Kan ett mönster vara oändligt?", "Ja, det kan fortsätta hur länge som helst."), ("Vad är en talföljd?", "Tal som står i en viss ordning efter en regel.")])


# ============================================================ pengar
def pengar(lv):
    MYNT = [1, 2, 5, 10]

    def rakna():
        items = [ch(MYNT) for _ in range(ri(2, 4))] if lv == 1 else [ch([20, 50]) for _ in range(ri(0, 2))] + [ch(MYNT) for _ in range(ri(2, 4))]
        t = sum(items)
        if t > (20 if lv == 1 else 100):
            return None
        pic = P(B.pengar_svg(items), "pengar")
        return mcq("Hur mycket pengar är det?" + pic, kr(t), [kr(t + 1), kr(t - 1) if t > 1 else kr(t + 2), kr(len(items))], "Lägg ihop: %s = <b>%s</b>." % (" + ".join(str(x) for x in sorted(items, reverse=True)), kr(t)))

    def mynt():
        a, b = sh(MYNT + ([20] if lv == 1 else [20, 50, 100]))[:2]
        r = kr(max(a, b))
        return mcq("Vilket är mest värt, %s eller %s?" % (kr(a), kr(b)), r, [kr(min(a, b)), "lika mycket", "det går inte att säga"], "%s är mer än %s." % (kr(max(a, b)), kr(min(a, b))))

    def kopa():
        nm = K().name()
        top = 20 if lv == 1 else 100
        p1 = ri(2, top // 2)
        p2 = ri(2, top - p1)
        sak1, sak2 = sh(["en penna", "ett suddgummi", "en boll", "en glass", "en bok", "ett äpple", "en banan", "en tidning"])[:2]
        return mcq("%s köper %s för %s och %s för %s. Hur mycket kostar det tillsammans?" % (nm, sak1, kr(p1), sak2, kr(p2)), kr(p1 + p2), [kr(p1 + p2 + 1), kr(abs(p1 - p2)) if p1 != p2 else kr(p1 + p2 - 1), kr(p1 + p2 + 10) if p1 + p2 + 10 <= top else kr(p1 + p2 - 2)], "%d + %d = <b>%s</b>." % (p1, p2, kr(p1 + p2)))

    def vaxel():
        nm = K().name()
        pay = ch([10, 20]) if lv == 1 else ch([20, 50, 100])
        p = ri(1, pay - 1)
        return mcq("%s köper en sak för %s och betalar med %s. Hur mycket får %s tillbaka?" % (nm, kr(p), kr(pay), nm), kr(pay - p), [kr(p), kr(pay - p + 1), kr(pay - p - 1) if pay - p > 1 else kr(pay - p + 2)] if p != pay - p else [kr(p + 1), kr(pay), kr(p - 1)], "%d − %d = <b>%s</b>." % (pay, p, kr(pay - p)))

    def racker():
        nm = K().name()
        top = 20 if lv == 1 else 100
        h = ri(3, top)
        p = ri(2, top)
        if h == p:
            return None
        r = "Ja" if h >= p else "Nej"
        return mcq("%s har %s. En leksak kostar %s. Räcker pengarna?" % (nm, kr(h), kr(p)), r, ["Nej" if r == "Ja" else "Ja", "Precis", "Det går inte att säga"], "%s %s %s. <b>%s</b>." % (kr(h), "är mer än" if h > p else "är mindre än", kr(p), r))

    sets = [("Räkna pengar", [(rakna, 20)]), ("Mynt och sedlar", [(mynt, 8), (rakna, 12)]), ("Handla", [(kopa, 20)]), ("Växel tillbaka", [(vaxel, 20)]), ("Räcker pengarna?", [(racker, 20)])]
    return unit("pengar", "T", "Pengar: mynt, sedlar och att handla" if lv == 2 else "Pengar: räkna mynt och handla", "Pengar",
                "Naturliga tal och deras användning i vardagliga situationer. Mynt och sedlar och att räkna med pengar.",
                "Arbetsblad om pengar för årskurs %d: räkna mynt%s, handla, växel tillbaka och räcker pengarna. 100 uppgifter med facit." % (lv, " och sedlar" if lv == 2 else ""),
                "Börja med det som är mest värt", "Räkna sedan vidare med de mindre mynten.", sets,
                ["Svenska mynt är 1 kr, 2 kr, 5 kr och 10 kr. Sedlar är bland annat 20 kr, 50 kr och 100 kr.", "Räkna pengar genom att börja med det som är mest värt och räkna vidare.", "Växel tillbaka räknar du med minus: betalt minus priset."],
                [("10 kr, 5 kr och 2 kr", ["10 + 5 + 2"], "17 kr"), ("Betalar 20 kr för 13 kr", ["20 − 13"], "7 kr")],
                [["Räknar antalet mynt", "Räkna vad mynten är värda"], ["Ett stort mynt är alltid mest värt", "Titta på siffran på myntet"], ["Växel med plus", "Växel räknas med minus"]],
                [("Vilka mynt finns i Sverige?", "1 krona, 2 kronor, 5 kronor och 10 kronor."), ("Vad är växel?", "Pengarna du får tillbaka när du betalar för mycket."), ("Hur räknar jag snabbt?", "Börja med de största mynten och sedlarna.")])


# ============================================================ klockan
def klockan(lv):
    MIN = [0, 30] if lv == 1 else [0, 15, 30, 45]

    def las():
        h, m = ri(1, 12), ch(MIN)
        pic = P(klocka(h, m), "analog klocka", lg=False)
        r = klocka_ord(h, m)
        others = set()
        for hh, mm in [(h % 12 + 1, m), (h, (m + 30) % 60), ((h - 2) % 12 + 1, m), (h, (m + 15) % 60), (h % 12 + 1, (m + 30) % 60)]:
            if mm in MIN:
                others.add(klocka_ord(hh, mm))
        return mcq("Vad är klockan?" + pic, r, [o for o in others if o != r], "Den korta visaren visar timmen och den långa minuterna: <b>%s</b>." % r)

    def digital():
        h, m = ri(1, 12), ch(MIN)
        r = klocka_ord(h, m)
        return mcq("Klockan är %s. Hur säger man det?" % hm(h, m), r, [klocka_ord(h % 12 + 1, m), klocka_ord(h, (m + 30) % 60) if (m + 30) % 60 in MIN else klocka_ord((h - 2) % 12 + 1, m), klocka_ord((h - 2) % 12 + 1, m) if lv == 2 else klocka_ord(h % 12 + 1, (m + 30) % 60)], "%s skrivs <b>%s</b> i ord." % (hm(h, m), r))

    def senare():
        h, m = ri(1, 11), ch(MIN)
        d = ch([1, 2, 3])
        r = klocka_ord(h + d, m)
        return mcq("Klockan är %s. Vad är klockan om %d timm%s?" % (klocka_ord(h, m), d, "e" if d == 1 else "ar"), r, [klocka_ord(h, m), klocka_ord((h + d) % 12 + 1, m), klocka_ord(h + d, (m + 30) % 60)], "%d timm%s senare: <b>%s</b>." % (d, "e" if d == 1 else "ar", r))

    def visare():
        k = ri(0, 2)
        if k == 0:
            return mcq("Vilken visare visar timmarna?", "den korta visaren", ["den långa visaren", "båda visarna", "ingen visare"], "<b>Den korta visaren</b> visar timmarna.")
        if k == 1:
            h = ri(1, 12)
            return mcq("Klockan är %s. Var pekar den långa visaren?" % klocka_ord(h, 0), "på 12", ["på %d" % h if h != 12 else "på 6", "på 6" if h != 6 else "på 3", "på 1" if h != 1 else "på 9"], "Vid hel timme pekar den långa visaren <b>på 12</b>.")
        h = ri(1, 12)
        return mcq("Klockan är %s. Var pekar den långa visaren?" % klocka_ord(h, 30), "på 6", ["på 12", "på %d" % (h % 12 + 1) if h % 12 + 1 != 6 else "på 3", "på 3" if h % 12 + 1 != 3 else "på 9"], "Vid halv pekar den långa visaren <b>på 6</b>.")

    def dygn():
        P_ = [("Hur många minuter är en timme?", "60", ["100", "30", "24"]), ("Hur många timmar är ett dygn?", "24", ["12", "60", "7"]), ("Hur många dagar är en vecka?", "7", ["5", "12", "30"]),
              ("Hur många minuter är en halvtimme?", "30", ["50", "15", "60"]), ("Hur många minuter är en kvart?", "15", ["25", "30", "45"]), ("Vilken dag kommer efter måndag?", "tisdag", ["söndag", "onsdag", "fredag"]),
              ("Vilken dag kommer före lördag?", "fredag", ["söndag", "torsdag", "måndag"]), ("Vilken månad kommer efter maj?", "juni", ["april", "juli", "mars"]), ("Hur många månader är ett år?", "12", ["10", "7", "24"]),
              ("Vilken dag kommer efter söndag?", "måndag", ["lördag", "tisdag", "fredag"]), ("Vilken månad kommer före december?", "november", ["januari", "oktober", "juni"]), ("Vilken månad är årets första?", "januari", ["december", "mars", "februari"])]
        q, r, w = ch(P_)
        return mcq(q, r, w, "<b>%s</b>." % r)

    if lv == 1:
        sets = [("Läs av klockan", [(las, 20)]), ("Klockan med ord", [(digital, 20)]), ("Senare", [(senare, 20)]), ("Visarna", [(visare, 20)]), ("Dagar, veckor och månader", [(dygn, 10), (senare, 10)])]
    else:
        sets = [("Läs av klockan", [(las, 20)]), ("Klockan med ord", [(digital, 20)]), ("Senare", [(senare, 20)]), ("Visarna", [(visare, 8), (las, 12)]), ("Dagar, veckor och månader", [(dygn, 10), (las, 10)])]
    return unit("klockan", "G", "Klockan: hela och halva timmar" if lv == 1 else "Klockan: hel, halv och kvart", "Klockan",
                "Mätning av tid. Klockan, analog och digital tid samt tidsenheter som minut, timme, dygn, vecka, månad och år.",
                "Arbetsblad om klockan för årskurs %d: läs av klockan%s, klockan med ord, vad är klockan senare och dagar, veckor och månader. 100 uppgifter med facit." % (lv, " vid hel och halv timme" if lv == 1 else " vid hel, halv och kvart"),
                "Kort visare timmar, lång visare minuter", "Halv fyra betyder 3.30.", sets,
                ["Den korta visaren visar timmarna och den långa visaren minuterna.", "När den långa visaren pekar på 12 är det hel timme. På 6 är det halv: halv fyra betyder 3.30.",
                 "Kvart över tre är 3.15 och kvart i fyra är 3.45." if lv == 2 else "En timme är 60 minuter och en halvtimme är 30 minuter."],
                [("Kort visare på 5, lång på 12", ["Hel timme"], "klockan fem"), ("Kort visare mellan 7 och 8, lång på 6", ["Halv till nästa timme"], "halv åtta")],
                [["Halv fyra är 4.30", "Halv fyra är 3.30, en halvtimme innan fyra"], ["Blandar ihop visarna", "Den korta visar timmar"], ["Läser fel timme vid halv", "Den korta visaren har gått förbi talet: titta på talet innan"]],
                [("Varför säger man halv fyra om 3.30?", "Det är en halvtimme kvar till fyra."), ("Hur många minuter är en timme?", "60."), ("Vad betyder kvart?", "En fjärdedels timme, 15 minuter.")])


# ============================================================ längd och vikt (åk 1) / längd (åk 2)
def langd1(lv):
    def penna():
        ls = sh([3, 4, 5, 6, 7, 8])[:3]
        labs = ["A", "B", "C"]
        pic = P(KP.pencils_svg(ls, labs), "tre pennor att jämföra")
        if coin():
            i = ls.index(max(ls))
            return mcq("Vilken penna är längst?" + pic, labs[i], [l for l in labs if l != labs[i]] + ["lika långa"], "Penna <b>%s</b> är längst." % labs[i])
        i = ls.index(min(ls))
        return mcq("Vilken penna är kortast?" + pic, labs[i], [l for l in labs if l != labs[i]] + ["lika långa"], "Penna <b>%s</b> är kortast." % labs[i])

    def torn():
        hs = sh([2, 3, 4, 5, 6, 7])[:3]
        labs = ["A", "B", "C"]
        pic = P(KP.towers_svg(hs, labs), "tre torn av kuber")
        if coin():
            i = hs.index(max(hs))
            return mcq("Vilket torn är högst?" + pic, labs[i], [l for l in labs if l != labs[i]] + ["lika höga"], "Torn <b>%s</b> har flest kuber och är högst." % labs[i])
        i = ri(0, 2)
        return mcq("Hur många kuber högt är torn %s?" % labs[i] + pic, str(hs[i]), [str(hs[i] + 1), str(hs[i] - 1), str(sum(hs))], "Räkna kuberna: <b>%d</b>." % hs[i])

    def vag():
        k1, k2 = sh(KINDS)[:2]
        t = ch(["left", "right"])
        pic = P(KP.balance_svg((k1, 1), (k2, 1), t), "en våg")
        heavy = k1 if t == "left" else k2
        sing = lambda k: "%s %s" % (SAK[k][2], SAK[k][0])
        return mcq("Vad är tyngst?" + pic, sing(heavy), [sing(k2 if heavy == k1 else k1), "lika tunga", "det går inte att se"], "Den tyngre sidan av vågen går ner: <b>%s</b>." % sing(heavy))

    def matt():
        a = ri(0, 6)
        b = a + ri(2, 9)
        if b > 15:
            return None
        pic = P(B.linjal(a, b, "linjal"), "linjal", lg=True)
        return mcq("Hur lång är remsan?" + pic, "%d cm" % (b - a), ["%d cm" % b, "%d cm" % (b - a + 1), "%d cm" % (b - a - 1)], "%d − %d = <b>%d cm</b>." % (b, a, b - a)) if a else mcq("Hur lång är remsan?" + pic, "%d cm" % b, ["%d cm" % (b + 1), "%d cm" % (b - 1), "%d cm" % (b + 2)], "Remsan börjar på 0 och slutar på %d: <b>%d cm</b>." % (b, b))

    def ord_():
        P_ = [("Vad är längst?", "en buss", ["en bil", "en cykel", "en sko"]), ("Vad är tyngst?", "en elefant", ["en hund", "en katt", "en mus"]), ("Vad är kortast?", "en myra", ["en katt", "en häst", "en hund"]),
              ("Vad är lättast?", "en fjäder", ["en sten", "en bok", "en väska"]), ("Vad är högst?", "ett hus", ["ett bord", "en stol", "en säng"]), ("Vad rymmer mest?", "en hink", ["en kopp", "en sked", "ett glas"]),
              ("Vad rymmer minst?", "en sked", ["en hink", "en kastrull", "ett badkar"]), ("Vilket ord betyder motsatsen till lång?", "kort", ["hög", "tung", "bred"]), ("Vilket ord betyder motsatsen till tung?", "lätt", ["kort", "smal", "låg"])]
        q, r, w = ch(P_)
        return mcq(q, r, w, "<b>%s</b>." % cap1(r))

    sets = [("Längst och kortast", [(penna, 20)]), ("Högst och kuber", [(torn, 20)]), ("Tyngst och lättast", [(vag, 20)]), ("Mät med linjal", [(matt, 20)]), ("Jämför saker", [(ord_, 8), (penna, 6), (vag, 6)])]
    return unit("langd-och-vikt", "G", "Längd och vikt: jämföra och mäta", "Längd och vikt",
                "Jämförelser och uppskattningar av matematiska storheter. Mätning av längd och massa med icke-standardiserade och standardiserade enheter.",
                "Arbetsblad om längd och vikt för årskurs 1: längst och kortast, högst, tyngst och lättast, mät med linjal och jämför saker. 100 uppgifter med facit.",
                "Lägg sakerna bredvid varandra", "Den tyngre sidan av vågen går ner.", sets,
                ["För att jämföra längder lägger du sakerna bredvid varandra med samma början.", "Du kan mäta med kuber, gem eller en linjal. En linjal mäter i centimeter (cm).", "En balansvåg visar vad som är tyngst: den tunga sidan går ner."],
                [("Remsa från 0 till 7 på linjalen", ["Läs där remsan slutar"], "7 cm"), ("Vågen lutar åt äpplet", ["Den tunga sidan går ner"], "Äpplet är tyngst")],
                [["Börjar mäta på 1 i stället för 0", "Börja alltid på 0"], ["Tror att stort alltid är tyngst", "En stor ballong kan vara lätt"], ["Jämför utan samma början", "Ställ sakerna på samma linje"]],
                [("Vad är en centimeter?", "Ett mått på längd, ungefär lika brett som en lillfinger."), ("Hur fungerar en balansvåg?", "Den sida som är tyngst sjunker ner."), ("Kan man mäta med kuber?", "Ja, men kuberna måste vara lika stora.")])


def langd2(lv):
    omv = lim(maker(B.u16, "omvandla"), 100)
    matt = maker(B.u16, "matt")
    enhet = maker(B.u16, "enhet")
    jamf = lim(maker(B.u16, "jamfor"), 200)

    def m_cm():
        m, c = ri(1, 3), ri(5, 95)
        if coin():
            return mcq("Hur många centimeter är %d m?" % m, "%d cm" % (100 * m), ["%d cm" % (10 * m), "%d cm" % m, "%d cm" % (1000 * m) if 1000 * m < 2000 else "%d cm" % (100 * m + 10)], "1 m = 100 cm. %d m = <b>%d cm</b>." % (m, 100 * m))
        a, b = ri(20, 95), ri(20, 95)
        if a == b:
            return None
        return mcq("Hur mycket längre är %d cm än %d cm?" % (max(a, b), min(a, b)), "%d cm" % abs(a - b), ["%d cm" % (a + b), "%d cm" % (abs(a - b) + 10), "%d cm" % (abs(a - b) + 1)], "%d − %d = <b>%d cm</b>." % (max(a, b), min(a, b), abs(a - b)))

    def text_():
        nm = K().name()
        a, b = ri(10, 60), ri(10, 39)
        if a + b > 100:
            return None
        k = ri(0, 1)
        if k == 0:
            return mcq("%s hoppar %d cm och sedan %d cm till. Hur långt hoppar %s sammanlagt?" % (nm, a, b, nm), "%d cm" % (a + b), ["%d cm" % abs(a - b), "%d cm" % (a + b + 10), "%d cm" % (a + b - 1)], "%d + %d = <b>%d cm</b>." % (a, b, a + b))
        return mcq("Ett snöre är %d cm långt. %s klipper av %d cm. Hur långt är snöret nu?" % (a + b, nm, b), "%d cm" % a, ["%d cm" % (a + 2 * b), "%d cm" % (a + 10), "%d cm" % (a - 1)], "%d − %d = <b>%d cm</b>." % (a + b, b, a))

    sets = [("Mät med linjal", [(matt, 20)]), ("Meter och centimeter", [(m_cm, 20)]), ("Välj rätt enhet", [(enhet, 12), (m_cm, 8)]), ("Jämför längder", [(m_cm, 10), (jamf, 10)]), ("Längd i vardagen", [(text_, 20)])]
    return unit("langd", "G", "Längd: centimeter och meter", "Längd",
                "Jämförelser, uppskattningar och mätningar av längd med standardiserade måttenheter. Måttenheterna centimeter och meter.",
                "Arbetsblad om längd för årskurs 2: mät med linjal, meter och centimeter, välj rätt enhet, jämför längder och längd i vardagen. 100 uppgifter med facit.",
                "1 m = 100 cm", "Börja alltid mäta på 0.", sets,
                ["Längd mäts i centimeter (cm) och meter (m). 1 meter är 100 centimeter.", "Lägg linjalen så att 0 är vid ena änden och läs av vid andra änden.", "Korta saker mäts i cm, som en penna. Långa saker mäts i m, som ett rum."],
                [("Remsa från 0 till 9", ["Läs av vid slutet"], "9 cm"), ("2 m i cm", ["1 m = 100 cm"], "200 cm")],
                [["Mäter från 1 på linjalen", "Börja på 0"], ["1 m = 10 cm", "1 m = 100 cm"], ["Mäter en dörr i cm", "Längre saker mäts oftast i meter"]],
                [("Hur lång är en meter?", "Ungefär ett stort steg för en vuxen."), ("Hur lång är en centimeter?", "Ungefär så bred som en nagel."), ("Vilket mätredskap använder jag?", "Linjal för korta saker och måttband för långa.")])


# ============================================================ geometri
def figurer1(lv):
    F = {"circle": "cirkel", "square": "kvadrat", "rectangle": "rektangel", "triangle": "triangel"}
    HORN = {"circle": 0, "square": 4, "rectangle": 4, "triangle": 3}

    def namn():
        k = ch(list(F))
        pic = P(KP.one_shape_svg(k, ch(["blue", "red", "yellow", "green"]), 40, ri(0, 30) if k != "circle" else 0), "en geometrisk figur")
        return mcq("Vad heter figuren?" + pic, F[k], [v for kk, v in F.items() if kk != k], "Det är en <b>%s</b>." % F[k])

    def horn():
        k = ch(list(F))
        if coin():
            return mcq("Hur många hörn har en %s?" % F[k], str(HORN[k]), [str(x) for x in (0, 3, 4, 5, 6) if x != HORN[k]], "En %s har <b>%d</b> hörn." % (F[k], HORN[k]))
        return mcq("Hur många sidor har en %s?" % F[k], str(HORN[k]), [str(x) for x in (0, 3, 4, 5, 6) if x != HORN[k]], "En %s har <b>%d</b> sidor%s." % (F[k], HORN[k], ", den är rund" if k == "circle" else ""))

    def rakna():
        items = []
        target = ch(list(F))
        n = ri(1, 5)
        for _ in range(n):
            items.append((target, ch(["blue", "red", "yellow", "green"])))
        for _ in range(ri(3, 7)):
            items.append((ch([k for k in F if k != target]), ch(["blue", "red", "yellow", "green"])))
        sh_ = sh(items)
        pic = P(KP.shapes_mix_svg(sh_, ri(1, 999), 5, 3), "många figurer")
        plur = {"circle": "cirklar", "square": "kvadrater", "rectangle": "rektanglar", "triangle": "trianglar"}[target]
        return mcq("Hur många %s finns det?" % plur + pic, str(n), [str(n + 1), str(n - 1) if n > 1 else str(n + 2), str(len(items))], "Räkna bara %s: <b>%d</b>." % (plur, n))

    def egenskap():
        P_ = [("Vilken figur har inga hörn?", "cirkel", ["triangel", "kvadrat", "rektangel"]), ("Vilken figur har tre sidor?", "triangel", ["kvadrat", "cirkel", "rektangel"]),
              ("Vilken figur har fyra lika långa sidor?", "kvadrat", ["rektangel", "triangel", "cirkel"]), ("Vilken figur är rund?", "cirkel", ["kvadrat", "triangel", "rektangel"]),
              ("En figur har fyra hörn och två långa och två korta sidor. Vad heter den?", "rektangel", ["kvadrat", "triangel", "cirkel"]), ("Vilken figur har tre hörn?", "triangel", ["kvadrat", "rektangel", "cirkel"])]
        q, r, w = ch(P_)
        return mcq(q, r, w, "<b>%s</b>." % cap1(r))

    def saker():
        P_ = [("ett hjul", "cirkel"), ("en klocka", "cirkel"), ("en tallrik", "cirkel"), ("ett fönster", "kvadrat"), ("en dörr", "rektangel"), ("en bok", "rektangel"),
              ("en pizzabit", "triangel"), ("en vägskylt med varning", "triangel"), ("en sedel", "rektangel"), ("en servett", "kvadrat"), ("en mobil", "rektangel"), ("ett mynt", "cirkel")]
        s, r = ch(P_)
        return mcq("Vilken figur liknar %s mest?" % s, r, [v for v in F.values() if v != r], "%s liknar en <b>%s</b>." % (cap1(s), r))

    sets = [("Vad heter figuren?", [(namn, 20)]), ("Hörn och sidor", [(horn, 8), (egenskap, 6), (namn, 6)]), ("Räkna figurer", [(rakna, 20)]), ("Figurer runt omkring oss", [(saker, 12), (rakna, 8)]), ("Blandat", [(namn, 10), (rakna, 10)])]
    return unit("geometriska-figurer", "G", "Geometriska figurer: cirkel, triangel, kvadrat och rektangel", "Geometriska figurer",
                "Grundläggande geometriska objekt, däribland punkter, linjer, sträckor, fyrhörningar, trianglar och cirklar. Konstruktion av geometriska objekt.",
                "Arbetsblad om geometriska figurer för årskurs 1: cirkel, triangel, kvadrat och rektangel, hörn och sidor, räkna figurer och figurer runt omkring oss. 100 uppgifter med facit.",
                "En triangel har tre hörn", "En kvadrat har fyra lika långa sidor.", sets,
                ["En cirkel är rund och har inga hörn.", "En triangel har tre hörn och tre sidor.", "En kvadrat och en rektangel har fyra hörn. I en kvadrat är alla sidor lika långa."],
                [("Hur många hörn har en rektangel?", ["Räkna hörnen"], "4"), ("Vad liknar ett hjul?", ["Det är runt"], "en cirkel")],
                [["En kvadrat är en cirkel", "En kvadrat har fyra hörn"], ["En triangel har fyra hörn", "Tri betyder tre: tre hörn"], ["En kvadrat som står på spetsen är inte en kvadrat", "Den är fortfarande en kvadrat"]],
                [("Är en kvadrat en rektangel?", "Ja, en kvadrat är en särskild rektangel där alla sidor är lika långa."), ("Varför har en cirkel inga hörn?", "Den är helt rund."), ("Var hittar jag figurer?", "Överallt: fönster, hjul, skyltar och böcker.")])


def figurer2(lv):
    namn = maker(B.u18, "namn")
    horn = maker(B.u18, "horn")
    egen = maker(B.u18, "egenskap")
    knamn = maker(B.u19, "namn")
    ksak = maker(B.u19, "sak")
    sets = [("Känn igen figurer", [(namn, 20)]), ("Sidor och hörn", [(horn, 20)]), ("Figurernas egenskaper", [(egen, 8), (maker(B.u18, "begrepp"), 6), (maker(B.u18, "rakna"), 6)]), ("Känn igen kroppar", [(knamn, 20)]), ("Kroppar i vardagen", [(ksak, 20)])]
    return unit("geometriska-figurer-och-kroppar", "G", "Geometriska figurer och kroppar", "Figurer och kroppar",
                "Grundläggande geometriska objekt, däribland fyrhörningar, trianglar, cirklar, klot, kuber, rätblock och cylindrar, och deras inbördes relationer.",
                "Arbetsblad om geometriska figurer och kroppar för årskurs 2: känn igen figurer, sidor och hörn, egenskaper, kroppar och kroppar i vardagen. 100 uppgifter med facit.",
                "Figurer är platta, kroppar är rumsliga", "En kub har sex sidoytor.", sets,
                ["Figurer är platta: triangel, kvadrat, rektangel, cirkel. De har sidor och hörn.", "Kroppar är tredimensionella: klot, kub, rätblock, cylinder, kon och pyramid.", "En kub har 6 sidoytor som alla är kvadrater. En boll är ett klot."],
                [("Hur många hörn har en femhörning?", ["Fem betyder 5"], "5"), ("Vilken kropp liknar en burk?", ["Rund med två lika ändar"], "en cylinder")],
                [["En kub är en kvadrat", "En kvadrat är platt, en kub är en kropp"], ["En boll är en cirkel", "En boll är ett klot"], ["Räknar ett hörn två gånger", "Sätt en prick på varje hörn du räknar"]],
                [("Vad är skillnaden på en figur och en kropp?", "En figur är platt. En kropp har också djup."), ("Vilken kropp kan rulla?", "Klot, cylinder och kon."), ("Vad är en sidoyta?", "En platt yta på en kropp.")])


def symmetri(lv):
    vilken = maker(B.u20, "vilken")
    fyll = maker(B.u20, "fyll")
    bok = maker(B.u20, "bokstav")
    lin = maker(B.u20, "linjer")
    sets = [("Är figuren symmetrisk?", [(vilken, 20)]), ("Rita klart figuren", [(fyll, 20)]), ("Symmetriska bokstäver", [(bok, 20)]), ("Antal symmetrilinjer", [(lin, 12), (bok, 8)]), ("Blandat", [(vilken, 10), (fyll, 10)])]
    return unit("symmetri", "G", "Symmetri: spegelbild och symmetrilinje", "Symmetri",
                "Symmetri, till exempel i bilder och i naturen, och hur symmetri kan konstrueras.",
                "Arbetsblad om symmetri för årskurs 2: är figuren symmetrisk, rita klart en spegelbild, symmetriska bokstäver och antal symmetrilinjer. 100 uppgifter med facit.",
                "Båda halvorna är spegelbilder", "Vik längs linjen så passar halvorna.", sets,
                ["En figur är symmetrisk om du kan vika den så att båda halvorna passar precis.", "Linjen du viker längs heter symmetrilinje.", "Spegelbilden ligger lika långt från linjen men på andra sidan."],
                [("Är bokstaven A symmetrisk?", ["Vik den lodrätt i mitten"], "Ja"), ("Hur många symmetrilinjer har en kvadrat?", ["Två raka och två diagonala"], "4")],
                [["Flyttar halvan i stället för att spegla", "Det som är nära linjen ska vara nära linjen på andra sidan"], ["Tror att alla bokstäver är symmetriska", "F och G har ingen symmetrilinje"], ["Glömmer diagonalerna i en kvadrat", "En kvadrat har 4 symmetrilinjer"]],
                [("Var finns symmetri?", "I fjärilar, löv, ansikten och byggnader."), ("Hur testar jag symmetri?", "Vik papperet eller ställ en spegel på linjen."), ("Har en cirkel symmetrilinjer?", "Ja, oändligt många.")])


def lagesord(lv):
    SCEN = {"above": "ovanför bordet", "below": "under bordet", "beside": "bredvid bordet"}
    BOX = {"front": "framför lådan", "behind": "bakom lådan", "beside": "bredvid lådan", "above": "ovanför lådan"}
    sing = lambda k: "%s %s" % ("Äpplet" if k == "apple" else "Hjärtat" if k == "heart" else cap1(SAK[k][0]) + ("n" if SAK[k][0][-1] in "aeiouyåäö" else "en"), "")

    def bef(k):
        s = SAK[k][0]
        if SAK[k][2] == "ett":
            return s + "t"
        return s + ("n" if s[-1] in "aeiouyåäö" else "en")

    def bord():
        k = ch(KINDS)
        rel = ch(list(SCEN))
        pic = P(KP.table_scene_svg(k, rel), "ett bord och %s %s" % (SAK[k][2], SAK[k][0]))
        return mcq("Var är %s?" % bef(k) + pic, SCEN[rel], [v for r, v in SCEN.items() if r != rel] + ["inuti bordet"], "%s är <b>%s</b>." % (cap1(bef(k)), SCEN[rel]))

    def lada():
        k = ch(KINDS)
        rel = ch(list(BOX))
        pic = P(KP.box_scene_svg(k, rel), "en låda och %s %s" % (SAK[k][2], SAK[k][0]))
        return mcq("Var är %s?" % bef(k) + pic, BOX[rel], [v for r, v in BOX.items() if r != rel], "%s är <b>%s</b>." % (cap1(bef(k)), BOX[rel]))

    def hylla():
        ks = sh(KINDS)[:3]
        pic = P(KP.shelf_svg(ks), "en hylla med tre saker")
        i = ri(0, 2)
        pos = ["överst", "i mitten", "nederst"][i]
        return mcq("Vad står %s på hyllan?" % pos + pic, SAK[ks[i]][2] + " " + SAK[ks[i]][0], [SAK[x][2] + " " + SAK[x][0] for x in ks if x != ks[i]] + ["ingenting"], "%s står <b>%s</b> %s." % (cap1(SAK[ks[i]][2] + " " + SAK[ks[i]][0]), "", pos) if False else "Det som står %s är <b>%s %s</b>." % (pos, SAK[ks[i]][2], SAK[ks[i]][0]))

    def rad():
        ks = sh(KINDS)[:4]
        pic = P(KP.kinds_row_svg(ks), "fyra saker på rad")
        i = ri(0, 3)
        if coin():
            pos = "längst till vänster" if i == 0 else "längst till höger" if i == 3 else None
            if pos is None:
                return None
            return mcq("Vad är %s?" % pos + pic, SAK[ks[i]][2] + " " + SAK[ks[i]][0], [SAK[x][2] + " " + SAK[x][0] for x in ks if x != ks[i]], "Det som är %s är <b>%s %s</b>." % (pos, SAK[ks[i]][2], SAK[ks[i]][0]))
        if i == 3:
            return None
        return mcq("Vad är direkt till höger om %s?" % bef(ks[i]) + pic, SAK[ks[i + 1]][2] + " " + SAK[ks[i + 1]][0], [SAK[x][2] + " " + SAK[x][0] for x in ks if x != ks[i + 1]], "Till höger om %s är <b>%s %s</b>." % (bef(ks[i]), SAK[ks[i + 1]][2], SAK[ks[i + 1]][0]))

    if lv == 1:
        ord_ = maker(B.u21, "ord_")
        sets = [("Ovanför, under och bredvid", [(bord, 20)]), ("Framför och bakom", [(lada, 20)]), ("Överst och nederst", [(hylla, 20)]), ("Vänster och höger", [(rad, 20)]), ("Lägesord", [(ord_, 6), (bord, 7), (lada, 7)])]
        slug, title, short = "lagesord", "Lägesord: ovanför, under, bredvid, framför och bakom", "Lägesord"
        meta = "Arbetsblad om lägesord för årskurs 1: ovanför, under och bredvid, framför och bakom, överst och nederst och vänster och höger. 100 uppgifter med facit."
    else:
        gr = maker(B.u21, "granne")
        st = maker(B.u21, "steg")
        ins = maker(B.u21, "instruktion")
        ord_ = maker(B.u21, "ord_")
        sets = [("Lägesord", [(lada, 6), (ord_, 6), (rad, 8)]), ("Vad finns bredvid?", [(gr, 20)]), ("Följ stegen", [(st, 20)]), ("Skriv instruktionen", [(ins, 20)]), ("Blandat", [(bord, 6), (gr, 7), (st, 7)])]
        slug, title, short = "lagesord-och-programmering", "Lägesord och programmering: instruktioner i rutnät", "Lägesord och programmering"
        meta = "Arbetsblad om lägesord och programmering för årskurs 2: lägesord, vad finns bredvid, följ stegen i ett rutnät och skriv instruktioner. 100 uppgifter med facit."
    return unit(slug, "G", title, short,
                "Vanliga lägesord för att beskriva föremåls läge i rummet." + (" Hur entydiga stegvisa instruktioner kan konstrueras, beskrivas och följas som grund för programmering." if lv == 2 else ""),
                meta, "Lägesord säger var något är", "Ovanför, under, bredvid, framför, bakom.", sets,
                ["Lägesord beskriver var något är: ovanför, under, bredvid, framför, bakom, mellan.", "Till vänster och till höger ser du på bilden från ditt håll.",
                 "En instruktion säger hur du ska gå, ett steg i taget, till exempel 2 steg åt höger." if lv == 2 else "Överst är högst upp och nederst är längst ner."],
                [("Bollen ligger på bordet", ["Bollen är högre upp än bordet"], "ovanpå bordet"), ("Katten är bakom lådan", ["Lådan skymmer katten"], "bakom")],
                [["Blandar ihop vänster och höger", "Titta på bilden från ditt håll"], ["Framför och bakom byter plats", "Det som syns först är framför"], ["Räknar startrutan som ett steg", "Första steget går till nästa ruta"]],
                [("Vad betyder bredvid?", "Vid sidan av."), ("Vad är en instruktion?", "En tydlig beskrivning av hur man ska göra."), ("Varför ska man lära sig lägesord?", "För att kunna beskriva var saker finns och förstå vägbeskrivningar.")])


# ============================================================ tabeller och diagram
def diagram(lv):
    las = lim(maker(B.u22, "las"), 100)
    mest = lim(maker(B.u22, "mest"), 100)
    skill = lim(maker(B.u22, "skillnad"), 100)
    strk = lim(maker(B.u22, "streckr"), 100)
    tabl = lim(maker(B.u22, "tabell"), 100)
    tot = lim(maker(B.u22, "totalt"), 100)

    def streck_():
        n = ri(1, 20)
        pic = P(streck(n), "streckräkning med %d streck" % n)
        return mcq("Hur många streck är det?" + pic, str(n), [str(n + 1), str(n - 1) if n > 1 else str(n + 2), str(n + 5)], "Varje grupp är 5 streck. Svar: <b>%d</b>." % n)

    def bild():
        ks = sh(KINDS)[:3]
        ns = [ri(1, 8) for _ in ks]
        if len(set(ns)) < 3:
            return None
        s = []
        for r, (k, n) in enumerate(zip(ks, ns)):
            for i in range(n):
                s.append(KP.obj(k, 30 + i * 30, 26 + r * 36, 12))
        pic = P(wrap(30 + 8 * 30 + 10, 26 + 3 * 36, "".join(s), "bilddiagram"), "bilddiagram")
        k = ri(0, 2)
        if k == 0:
            i = ns.index(max(ns))
            return mcq("Bilddiagrammet visar saker i ett klassrum. Vad finns det flest av?" + pic, pl(ks[i]), [pl(x) for x in ks if x != ks[i]] + ["lika många"], "Den längsta raden: <b>%s</b>." % pl(ks[i]))
        if k == 1:
            i = ri(0, 2)
            return mcq("Bilddiagrammet visar saker. Hur många %s är det?" % pl(ks[i]) + pic, str(ns[i]), [str(ns[i] + 1), str(ns[i] - 1) if ns[i] > 1 else str(ns[i] + 2), str(sum(ns))], "Räkna raden: <b>%d</b>." % ns[i])
        return mcq("Bilddiagrammet visar saker. Hur många saker är det sammanlagt?" + pic, str(sum(ns)), [str(sum(ns) + 1), str(sum(ns) - 1), str(max(ns))], "%s = <b>%d</b>." % (" + ".join(map(str, ns)), sum(ns)))

    if lv == 1:
        sets = [("Streckräkning", [(streck_, 20)]), ("Bilddiagram", [(bild, 20)]), ("Läs av stapeldiagram", [(lim(las, 20), 20)]), ("Mest och minst", [(lim(mest, 20), 20)]), ("Blandat", [(bild, 10), (lim(skill, 20), 10)])]
    else:
        sets = [("Streckräkning och tabeller", [(strk, 10), (tabl, 10)]), ("Läs av stapeldiagram", [(las, 20)]), ("Mest och minst", [(mest, 20)]), ("Jämför staplarna", [(skill, 20)]), ("Totalt", [(tot, 10), (bild, 10)])]
    return unit("tabeller-och-diagram", "S", "Tabeller och diagram: streckräkning och stapeldiagram", "Tabeller och diagram",
                "Enkla tabeller och diagram och hur de kan användas för att sortera data och beskriva resultat från enkla undersökningar.",
                "Arbetsblad om tabeller och diagram för årskurs %d: streckräkning, bilddiagram, stapeldiagram, mest och minst%s. 100 uppgifter med facit." % (lv, " och att jämföra staplar" if lv == 2 else ""),
                "Den högsta stapeln är flest", "Streck räknas fem i taget.", sets,
                ["Streckräkning: gör ett streck för varje sak. Det femte strecket dras snett över de fyra.", "I ett stapeldiagram visar höjden på stapeln hur många det är.", "Den högsta stapeln visar det som är vanligast."],
                [("Två hela femgrupper och tre streck", ["5 + 5 + 3"], "13"), ("Stapeln når 7", ["Läs på skalan till vänster"], "7")],
                [["Räknar femgruppen som 4", "Det sneda strecket räknas också: 5"], ["Läser av stapeln fel", "Följ toppen rakt åt vänster till skalan"], ["Tror att bredast stapel är flest", "Höjden avgör"]],
                [("Varför gör man streckräkning?", "Det går snabbt att räkna när man räknar fem i taget."), ("Vad är ett stapeldiagram?", "Ett diagram där staplar visar hur många det är."), ("Vad är ett bilddiagram?", "Ett diagram där bilder visar antal.")])


def slump(lv):
    sak_ = maker(B.u23, "sakert")
    pase = maker(B.u23, "pasen")
    tarn = lim(maker(B.u23, "tarning"), 12)
    ratt = maker(B.u23, "rattvist")
    sets = [("Säkert, möjligt eller omöjligt", [(sak_, 10), (pase, 10)]), ("Dra en kula", [(pase, 20)]), ("Tärningar", [(tarn, 20)]), ("Är spelet rättvist?", [(ratt, 20)]), ("Blandat", [(pase, 6), (tarn, 7), (maker(B.u23, "forsok"), 7)])]
    return unit("slump-och-chans", "S", "Slump och chans: säkert, möjligt eller omöjligt", "Slump och chans",
                "Slumpmässiga händelser i experiment och spel. Säkert, möjligt och omöjligt.",
                "Arbetsblad om slump och chans för årskurs 2: säkert, möjligt eller omöjligt, dra en kula, tärningar och rättvisa spel. 100 uppgifter med facit.",
                "Säkert, möjligt eller omöjligt", "Fler kulor av en färg ger större chans.", sets,
                ["Något som alltid händer är säkert. Något som kan hända är möjligt. Något som aldrig kan hända är omöjligt.", "Finns det fler röda kulor än blå i en påse är det större chans att dra en röd.", "En tärning har sex sidor. Varje sida har lika stor chans."],
                [("Slå 7 med en vanlig tärning", ["Tärningen har bara 1–6"], "omöjligt"), ("8 röda och 2 blå kulor", ["Fler röda"], "Störst chans för röd")],
                [["Tror att 6 är svårast att slå", "Alla sidor har lika stor chans"], ["Möjligt betyder säkert", "Möjligt betyder att det kan hända"], ["Glömmer att räkna alla kulor", "Räkna varje färg"]],
                [("Vad betyder chans?", "Hur troligt det är att något händer."), ("Är ett spel rättvist?", "Om alla har lika stor chans att vinna."), ("Kan man veta vad tärningen visar?", "Nej, det är slumpen som bestämmer.")])


UNITS = {"tal-till-20": tal, "tal-till-100": tal, "talraden-till-100": talraden, "jamfora-tal": jamfora, "jamfora-och-ordna-tal": jamfora, "talkamrater": talkamrater,
         "addition-till-10": addition10, "subtraktion-till-10": subtraktion10, "addition-och-subtraktion-till-20": addsub20, "problemlosning": problem,
         "dubbelt-och-halften": dubbelt, "monster": monster, "pengar": pengar, "klockan": klockan, "langd-och-vikt": langd1, "geometriska-figurer": figurer1,
         "lagesord": lagesord, "tabeller-och-diagram": diagram, "tiotal-och-ental": tiotal, "udda-och-jamna-tal": udda, "huvudrakning": huvudrakning,
         "addition-och-subtraktion-till-100": addsub_till_100, "multiplikation": multiplikation, "delning": delning, "halvor-och-fjardedelar": brak,
         "langd": langd2, "geometriska-figurer-och-kroppar": figurer2, "symmetri": symmetri, "lagesord-och-programmering": lagesord, "slump-och-chans": slump}
