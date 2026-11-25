# -*- coding: utf-8 -*-
"""Sverige årskurs 3: samband, mätning, geometri, statistik — 単元 13〜23。se_a3.py から使う。"""
import math
import random
from se_common import (fig, num, kr, u, mcq, NB, Kids, hon, Hon, klocka_ord, hm, klocka, stapel, streck, wrap, text, line,
                       INK, GREEN, FILL, RED, BLUE)
import se_a3a as A

R = None
K = None


def setup(rnd):
    global R, K
    R = rnd
    K = Kids(rnd)


def ri(a, b):
    return R.randint(a, b)


def ch(xs):
    return R.choice(list(xs))


def sh(xs):
    xs = list(xs)
    R.shuffle(xs)
    return xs


unit = A.unit
cap = A.cap


# ============================================================ 13. Dubbelt och hälften
def u13():
    def dubbelt():
        n = ri(6, 250) if R.random() < 0.6 else ri(11, 49)
        return mcq("Vad är dubbelt så mycket som %s?" % num(n), num(2 * n), [num(n + 2), num(n // 2) if n > 3 else num(n + 1), num(2 * n + 10), num(2 * n - 1)],
                   "Dubbelt = två gånger: %s + %s = <b>%s</b>." % (num(n), num(n), num(2 * n)))

    def halften():
        n = ri(3, 250) * 2
        return mcq("Vad är hälften av %s?" % num(n), num(n // 2), [num(n * 2), num(n - 2), num(n // 2 + 5), num(n // 2 - 1)],
                   "Hälften = dela i två lika delar: %s : 2 = <b>%s</b>, eftersom %s + %s = %s." % (num(n), num(n // 2), num(n // 2), num(n // 2), num(n)))

    def recept():
        p = ch([2, 4])
        ing = sh([("dl mjöl", ri(2, 6)), ("ägg", ri(1, 3)), ("dl mjölk", ri(2, 5)), ("msk socker", ri(1, 4)), ("g smör", ch([50, 75, 100]))])[0]
        more = R.random() < 0.6
        q_ = p * 2 if more else p // 2
        if not more and ing[1] % 2:
            return None
        ans = ing[1] * 2 if more else ing[1] // 2
        un = ing[0]
        return mcq("Ett recept på pannkakor för %d personer behöver %d %s. %s behövs för %d personer?" % (p, ing[1], un, "Hur många ägg" if un == "ägg" else "Hur mycket", q_), "%d %s" % (ans, un),
                   ["%d %s" % (x, un) for x in (ing[1] + 2, ing[1], ans + 1, ing[1] * 3) if x != ans],
                   "%d personer är %s så många. Då behövs %s: <b>%d %s</b>." % (q_, "dubbelt" if more else "hälften", "dubbelt så mycket" if more else "hälften så mycket", ans, un))

    def jamfor():
        a, b = K.two()
        n = ri(4, 60)
        k = ri(0, 1)
        thing = ch(["kort", "kulor", "klistermärken", "pärlor"])
        if k == 0:
            return mcq("%s har %d %s. %s har dubbelt så många. Hur många har %s?" % (a, n, thing, b, b), str(2 * n), [str(n + 2), str(n // 2) if n > 2 else str(n + 1), str(3 * n)],
                       "Dubbelt så många som %d: %d + %d = <b>%d</b>." % (n, n, n, 2 * n))
        n2 = n * 2
        return mcq("%s har %d %s. %s har hälften så många. Hur många har %s?" % (a, n2, thing, b, b), str(n), [str(n2 * 2), str(n2 - 2), str(n + 2)],
                   "Hälften av %d är <b>%d</b>." % (n2, n))

    def prop():
        k = ri(0, 2)
        if k == 0:
            per, n = ch([3, 4, 5, 6, 8]), ri(2, 6)
            return mcq("I en påse finns %d bullar. Hur många bullar finns i %d påsar?" % (per, n), str(per * n), [str(per + n), str(per * n - per), str(per * n + per)],
                       "1 påse → %d, %d påsar → %d × %d = <b>%d</b>." % (per, n, n, per, per * n))
        if k == 1:
            p, n = ch([5, 10, 15, 20]), ri(2, 5)
            return mcq("En biljett kostar %s. Vad kostar %d biljetter?" % (kr(p), n), kr(p * n), [kr(p + n), kr(p * n - p), kr(p * (n + 1))],
                       "%d × %d = <b>%d kr</b>." % (n, p, p * n))
        d, t = ch([2, 3, 4]), ri(2, 5)
        return mcq("En sköldpadda går %d meter varje minut. Hur långt går den på %d minuter?" % (d, t), "%d meter" % (d * t),
                   ["%d meter" % x for x in (d + t, d * t + d, d * t - 1)], "%d minuter × %d meter = <b>%d meter</b>." % (t, d, d * t))

    def halv_mangd():
        n = ch([4, 6, 8, 10, 12, 20, 30, 40, 50, 60, 100, 200])
        un = ch(["cm", "kr", "minuter", "liter"])
        ans = n // 2
        q = {"cm": "Ett band är %d cm långt. Det klipps i två lika långa delar. Hur lång är varje del?" % n,
             "kr": "Två syskon delar lika på %d kr. Hur mycket får var och en?" % n,
             "minuter": "En promenad tar %d minuter. Hur lång tid tar halva promenaden?" % n,
             "liter": "En tunna rymmer %d liter. Hur mycket är hälften?" % n}[un]
        return mcq(q, "%d %s" % (ans, un), ["%d %s" % (x, un) for x in (n * 2, n - 2, ans + 2)],
                   "%d : 2 = <b>%d %s</b>." % (n, ans, un))

    sets = [("Dubbelt", [(dubbelt, 20)]),
            ("Hälften", [(halften, 20)]),
            ("Dubbelt så många, hälften så många", [(jamfor, 14), (halv_mangd, 6)]),
            ("Recept", [(recept, 20)]),
            ("Proportionella samband", [(prop, 20)])]
    return unit("dubbelt-och-halften", "F", 13, "Dubbelt och hälften: proportionella samband", "Dubbelt och hälften",
                "Olika proportionella samband, däribland dubbelt och hälften. Del av helhet i vardagliga situationer som recept och priser.",
                "Arbetsblad om dubbelt och hälften för årskurs 3: dubbelt av ett tal, hälften av ett tal, dubbelt så många, recept och enkla proportionella samband. 100 uppgifter med facit.",
                "Dubbelt = 2 gånger", "Hälften = dela i två lika delar.", sets,
                ["Dubbelt betyder två gånger så mycket: dubbelt av 35 är 35 + 35 = 70.",
                 "Hälften betyder att dela i två lika stora delar: hälften av 70 är 35. Hälften och dubbelt är varandras motsats.",
                 "I ett recept ändras alla ingredienser lika mycket. För dubbelt så många personer tar du dubbelt av allt."],
                [("Dubbelt av 46", ["40 + 40 = 80", "6 + 6 = 12", "80 + 12"], "92"), ("Hälften av 86", ["Hälften av 80 är 40", "Hälften av 6 är 3"], "43")],
                [["Dubbelt av 46 är 48 (lägger till 2)", "Dubbelt = 46 + 46 = 92"], ["Hälften av 70 är 140", "Hälften är mindre: 35"],
                 ["Dubblar bara mjölet i receptet", "Alla ingredienser ska dubblas"]],
                [("Hur räknar jag dubbelt av stora tal?", "Dela upp talet: dubbelt av 236 = dubbelt av 200 + dubbelt av 36 = 400 + 72 = 472."),
                 ("Har alla tal en hälft?", "Jämna tal kan delas i två lika stora hela tal. Hälften av 7 är 3 och en halv."),
                 ("Vad är ett proportionellt samband?", "När den ena saken blir dubbelt så stor blir den andra också dubbelt så stor, som antal påsar och antal bullar.")])


# ============================================================ 14. Pengar
COIN = {1: (12, "#d6d6d6"), 2: (14, "#d6d6d6"), 5: (15, "#e0b84c"), 10: (16, "#e0b84c")}
NOTE = {20: "#c9a6d8", 50: "#f6c47a", 100: "#9fc3e8", 200: "#a5d6a7", 500: "#f0a3a3"}


def pengar_svg(items):
    s, x = [], 6
    for c in sorted([c for c in items if c >= 20], reverse=True):
        s.append("<rect x='%d' y='6' width='74' height='38' rx='4' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, NOTE[c], INK)
                 + text(x + 37, 31, "%d%skr" % (c, NB), 14))
        x += 82
    for c in sorted([c for c in items if c < 20], reverse=True):
        r, col = COIN[c]
        s.append("<circle cx='%d' cy='25' r='%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x + 18, r, col, INK) + text(x + 18, 29, "%d%skr" % (c, NB), 9))
        x += 40
    return wrap(x + 4, 50, "".join(s), "pengar: sammanlagt %d kr" % sum(items))


def u14():
    def raekna():
        items = [ch([20, 50, 100]) for _ in range(ri(1, 2))] + [ch([1, 2, 5, 10]) for _ in range(ri(2, 4))]
        t = sum(items)
        return mcq(pengar_svg(items) + "Hur mycket pengar är det?", kr(t), [kr(t + 10), kr(t - 1), kr(t + 5), kr(len(items))],
                   "Börja med sedlarna och lägg sedan till mynten: <b>%s</b>." % kr(t))

    def vaxel():
        n = K.name()
        p = ri(12, 95)
        g = ch([x for x in (20, 50, 100) if x > p])
        return mcq("%s köper en bok för %s och betalar med en %s-lapp. Hur mycket får %s tillbaka?" % (n, kr(p), num(g), n), kr(g - p),
                   [kr(g - p + 10), kr(p), kr(g - p - 1) if g - p > 1 else kr(g - p + 2), kr(g + p)],
                   "%d − %d = <b>%d kr</b>." % (g, p, g - p))

    def minst():
        t = ri(13, 99)
        left, cnt = t, 0
        for c in (50, 20, 10, 5, 2, 1):
            cnt += left // c
            left %= c
        return mcq("Du ska betala exakt %s. Vilket är det minsta antalet sedlar och mynt du behöver? (sedlar 20 kr och 50 kr, mynt 1, 2, 5 och 10 kr)" % kr(t),
                   str(cnt), [str(cnt + 1), str(cnt - 1) if cnt > 1 else str(cnt + 2), str(t // 10 + t % 10)],
                   "Ta största möjliga först: %s. Det blir <b>%d</b> stycken." % (" + ".join(str(c) for c in _greedy(t)), cnt))

    def handla():
        n = K.name()
        it = sh([("en saft", 15), ("en bulle", 18), ("en macka", 25), ("en banan", 6), ("ett äpple", 5), ("en kaffe", 22), ("en kaka", 12)])[:ri(2, 3)]
        t = sum(p for _, p in it)
        ps = ["%s för %s" % (w, kr(p)) for w, p in it]
        lst = ", ".join(ps[:-1]) + " och " + ps[-1]
        return mcq("På fiket köper %s %s. Vad kostar det tillsammans?" % (n, lst), kr(t), [kr(t + 10), kr(t - 5), kr(max(p for _, p in it))],
                   "%s = <b>%s</b>." % (" + ".join(str(p) for _, p in it), kr(t)))

    def racker():
        n, g = K.next()
        have = ch([20, 50, 100, 200])
        a, b = ri(8, have // 2 + 10), ri(8, have // 2 + 10)
        if a + b == have:
            return None
        ok = a + b <= have
        return mcq("%s har %s. %s vill köpa en leksak för %s och en bok för %s. Räcker pengarna?" % (n, kr(have), Hon(g), kr(a), kr(b)),
                   "Ja, det blir %s över" % kr(have - a - b) if ok else "Nej, det fattas %s" % kr(a + b - have),
                   ["Nej, det fattas %s" % kr(abs(have - a - b)) if ok else "Ja, det blir %s över" % kr(abs(a + b - have)),
                    "Ja, det blir %s över" % kr(have - a) if have > a else "Nej, det fattas %s" % kr(a), "Det går inte att veta"],
                   "%d + %d = %d kr. %s" % (a, b, a + b, "Det är mindre än %d kr." % have if ok else "Det är mer än %d kr." % have))

    def billigast():
        items = sh([("pennor", ri(3, 9)), ("suddgummin", ri(3, 9)), ("linjaler", ri(3, 9)), ("block", ri(3, 9))])
        k = ri(2, 4)
        a, b = items[0], items[1]
        if a[1] == b[1]:
            return None
        return mcq("En penna kostar %s och ett suddgummi kostar %s. Hur mycket mer kostar %d pennor än %d suddgummin?" % (kr(a[1]), kr(b[1]), k, k) if a[1] > b[1] else
                   "Ett suddgummi kostar %s och en penna kostar %s. Hur mycket mer kostar %d suddgummin än %d pennor?" % (kr(b[1]), kr(a[1]), k, k),
                   kr(k * abs(a[1] - b[1])), [kr(abs(a[1] - b[1])), kr(k * (a[1] + b[1])), kr(k * abs(a[1] - b[1]) + k)],
                   "%d × %d = %d, %d × %d = %d. Skillnaden är <b>%s</b>." % (k, max(a[1], b[1]), k * max(a[1], b[1]), k, min(a[1], b[1]), k * min(a[1], b[1]), kr(k * abs(a[1] - b[1]))))

    sets = [("Räkna pengar", [(raekna, 20)]),
            ("Handla på fiket", [(handla, 20)]),
            ("Växel tillbaka", [(vaxel, 20)]),
            ("Räcker pengarna?", [(racker, 14), (billigast, 6)]),
            ("Minsta antal sedlar och mynt", [(minst, 12), (raekna, 4), (vaxel, 4)])]
    return unit("pengar", "T", 14, "Pengar: räkna, handla och växel tillbaka", "Pengar",
                "Naturliga tal och deras användning i vardagliga situationer. Beräkningar med pengar, sedlar och mynt.",
                "Arbetsblad om pengar för årskurs 3: räkna sedlar och mynt, handla, växel tillbaka, räcker pengarna och minsta antal sedlar och mynt. 100 uppgifter med facit.",
                "Sedlar först, sedan mynt", "Växel tillbaka = det du betalar − priset.", sets,
                ["I Sverige finns mynten 1, 2, 5 och 10 kronor och sedlarna 20, 50, 100, 200, 500 och 1 000 kronor.",
                 "Räkna pengar genom att börja med det största värdet: först sedlarna, sedan mynten.",
                 "Växel tillbaka räknar du med subtraktion: betalar du 50 kr för något som kostar 34 kr får du 50 − 34 = 16 kr tillbaka. Du kan också räkna uppåt från 34 till 50."],
                [("100 kr + 20 kr + 10 kr + 5 kr + 2 kr", ["100 + 20 = 120", "120 + 10 + 5 + 2 = 137"], "137 kr"),
                 ("Du betalar 50 kr för en bok som kostar 34 kr", ["Räkna uppåt: 34 → 40 (6), 40 → 50 (10)"], "16 kr tillbaka")],
                [["Räknar antalet mynt i stället för värdet", "Varje mynt har sitt värde: 5 kr + 5 kr = 10 kr"],
                 ["50 − 34 = 24", "50 − 34 = 16"], ["Glömmer skriva kr", "Svara med enhet: 16 kr"]],
                [("Finns det öre i Sverige?", "Nej, inte som mynt. Priser kan stå i öre, men du betalar kontant med hela kronor."),
                 ("Hur räknar jag växel lättast?", "Räkna uppåt från priset till det du betalade."),
                 ("Vilka sedlar finns?", "20, 50, 100, 200, 500 och 1 000 kronor.")])


def _greedy(t):
    out = []
    for c in (50, 20, 10, 5, 2, 1):
        while t >= c:
            out.append(c)
            t -= c
    return out


# ============================================================ 15. Klockan och tid
def u15():
    def analog():
        h, m = ri(1, 12), ch(range(0, 60, 5))
        good = klocka_ord(h, m)
        w = [klocka_ord(m // 5 if m else 12, (h % 12) * 5)]
        w += [klocka_ord(h - 1 if h > 1 else 12, m), klocka_ord(h, (m + 30) % 60), klocka_ord(h % 12 + 1, (60 - m) % 60)]
        return mcq(klocka(h, m) + "Vad är klockan?", cap(good), [cap(x) for x in w if x and x != good],
                   "Den korta visaren visar timmen och den långa visaren minuterna. Klockan är <b>%s</b>." % good)

    def digital():
        em = R.random() < 0.5
        h, m = (ri(1, 10) if em else ri(6, 11)), ch(range(0, 60, 5))
        hh = h + 12 if em else h
        good = hm(hh, m)
        w = [hm(h if em else h + 12, m), hm((hh + 1) % 24, m), hm(hh - 1, m), hm(hh, (m + 30) % 60)]
        part = "på eftermiddagen" if em and h < 6 else "på kvällen" if em else "på förmiddagen" if h >= 9 else "på morgonen"
        return mcq("Klockan är %s %s. Hur skrivs det digitalt?" % (klocka_ord(hh, m), part), good, [x for x in w if x != good],
                   "%s %s = <b>%s</b>.%s" % (cap(klocka_ord(hh, m)), part, good, " Efter klockan 12 lägger du till 12 timmar." if em else ""))

    def langd():
        h1, m1 = ri(8, 18), ch(range(0, 60, 5))
        d = ch([15, 20, 25, 30, 35, 40, 45, 50, 55, 65, 70, 75, 80, 85, 90, 95, 105])
        t = h1 * 60 + m1 + d
        h2, m2 = t // 60, t % 60
        f = lambda x: "%d minuter" % x if x < 60 else ("1 timme" + (" %d minuter" % (x - 60) if x > 60 else "") if x < 120 else "2 timmar" + (" %d minuter" % (x - 120) if x > 120 else ""))
        act = ch(["Filmen", "Matchen", "Utflykten", "Lektionen", "Konserten"])
        w = [f(d + 10), f(d - 10) if d > 10 else f(d + 20), f(abs(m2 - m1)) if abs(m2 - m1) not in (0, d) else f(d + 40), f(d + 60)]
        return mcq("%s börjar %s och slutar %s. Hur lång tid tar den?" % (act, hm(h1, m1), hm(h2, m2)), f(d), w,
                   "Räkna från %s till %s: <b>%s</b>." % (hm(h1, m1), hm(h2, m2), f(d)))

    def senare():
        h, m = ri(7, 19), ch(range(0, 60, 5))
        d = ch([10, 15, 20, 25, 30, 35, 40, 45, 50])
        t = h * 60 + m + d
        good = hm(t // 60, t % 60)
        w = [hm(h, (m + d) % 60), hm(t // 60 + 1, t % 60), hm(t // 60, (t % 60 + 10) % 60), hm(h + 1, m)]
        return mcq("Klockan är %s. Vad är klockan om %d minuter?" % (hm(h, m), d), good, [x for x in w if x != good],
                   "%s + %d minuter = <b>%s</b>." % (hm(h, m), d, good))

    def enheter():
        k = ri(0, 7)
        opts = [("Hur många minuter är en timme?", "60", ["100", "30", "24"]),
                ("Hur många timmar är ett dygn?", "24", ["12", "60", "7"]),
                ("Hur många dagar är en vecka?", "7", ["5", "10", "30"]),
                ("Hur många minuter är en kvart?", "15", ["25", "4", "45"]),
                ("Hur många sekunder är en minut?", "60", ["100", "10", "30"]),
                ("Hur många månader är ett år?", "12", ["10", "52", "365"])]
        if k < 6:
            q, a, w = opts[k]
            return mcq(q, a, w, "Svar: <b>%s</b>." % a)
        if k == 6:
            n = ri(2, 5)
            return mcq("Hur många minuter är %d timmar?" % n, str(60 * n), [str(100 * n), str(60 + n), str(30 * n)],
                       "1 timme = 60 minuter. %d × 60 = <b>%d</b>." % (n, 60 * n))
        n = ri(2, 4)
        return mcq("Hur många dagar är %d veckor?" % n, str(7 * n), [str(7 + n), str(5 * n), str(10 * n)],
                   "1 vecka = 7 dagar. %d × 7 = <b>%d</b>." % (n, 7 * n))

    sets = [("Läs av klockan", [(analog, 20)]),
            ("Analogt och digitalt", [(digital, 20)]),
            ("Hur lång tid?", [(langd, 20)]),
            ("Vad är klockan sedan?", [(senare, 20)]),
            ("Tidsenheter", [(enheter, 10), (analog, 5), (langd, 5)])]
    return unit("klockan-och-tid", "G", 15, "Klockan och tid: analog och digital tid", "Klockan och tid",
                "Jämförelse, uppskattning och mätning av tid med vanliga måttenheter. Analog och digital tid, timmar, minuter och sekunder.",
                "Arbetsblad om klockan för årskurs 3: läs av analog klocka, kvart över och halv, digital tid, hur lång tid och tidsenheter. 100 uppgifter med facit.",
                "Halv fyra är 3.30", "Halv betyder en halvtimme kvar till nästa hel timme.", sets,
                ["Den korta visaren visar timmen och den långa visaren minuterna. Mellan två siffror på klockan är det 5 minuter.",
                 "På svenska säger vi halv fyra när klockan är 3.30. Det är en halvtimme kvar till fyra. Fem i halv fyra är 3.25 och fem över halv fyra är 3.35.",
                 "Digitalt skrivs tiden med 24 timmar: halv fyra på eftermiddagen är 15.30. Räkna tid genom att hoppa till nästa hel timme först."],
                [("Hur lång tid är det från 9.40 till 10.15?", ["9.40 → 10.00 = 20 minuter", "10.00 → 10.15 = 15 minuter"], "35 minuter"),
                 ("Kvart i sju på kvällen digitalt", ["Kvart i sju = 6.45", "Kvällen: 6 + 12 = 18"], "18.45")],
                [["Halv fyra = 4.30", "Halv fyra = 3.30, en halvtimme kvar till fyra"], ["Blandar ihop visarna", "Den korta visaren är timvisaren"],
                 ["9.40 till 10.15 = 75 minuter (räknar som vanliga tal)", "En timme har 60 minuter: 35 minuter"]],
                [("Varför säger man halv fyra om 3.30?", "På svenska räknar vi halvtimmen fram mot nästa timme: halvvägs till fyra."),
                 ("Vad betyder 15.30?", "Halv fyra på eftermiddagen. Efter 12 fortsätter digitala klockor med 13, 14, 15 …"),
                 ("Hur många minuter är en halvtimme?", "30 minuter. En kvart är 15 minuter.")])


# ============================================================ 16. Längd
LANGD_OBJ = [("en myra", "mm"), ("en nagel", "mm"), ("en penna", "cm"), ("ett suddgummi", "cm"), ("en sko", "cm"), ("en bok", "cm"),
             ("ett klassrum", "m"), ("en fotbollsplan", "m"), ("ett hus", "m"), ("en buss", "m"),
             ("vägen från Stockholm till Uppsala", "km"), ("en cykeltur till grannstaden", "km"), ("ett maratonlopp", "km"),
             ("ett myggbett", "mm"), ("en gaffel", "cm"), ("en gymnastiksal", "m")]


def linjal(a, b, label="linjal"):
    """linjal 0–15 cm med en färgad remsa från a till b (cm)"""
    s = []
    k = 26
    x0 = 12
    s.append("<rect x='%d' y='40' width='%d' height='34' fill='#f7f1d7' stroke='%s' stroke-width='1.5'/>" % (x0 - 6, 15 * k + 12, INK))
    for i in range(15 * 2 + 1):
        x = x0 + i * k / 2.0
        L = 14 if i % 2 == 0 else 8
        s.append(line(x, 40, x, 40 + L, INK, 1.4 if i % 2 == 0 else 1))
        if i % 2 == 0:
            s.append(text(x, 68, str(i // 2), 11, weight=400))
    s.append("<rect x='%.1f' y='14' width='%.1f' height='18' rx='3' fill='#81b29a' stroke='%s' stroke-width='1.5'/>" % (x0 + a * k, (b - a) * k, INK))
    s.append(text(x0 + 15 * k + 2, 70, "cm", 10, anchor="end", weight=400))
    return wrap(15 * k + 26, 82, "".join(s), label, lg=True)


def u16():
    def omvandla():
        k = ri(0, 5)
        if k == 0:
            n = ri(1, 9)
            return mcq("%d m = ? cm" % n, "%d cm" % (100 * n), ["%d cm" % (10 * n), "%s cm" % num(1000 * n), "%d cm" % (n + 100)],
                       "1 m = 100 cm. %d m = <b>%d cm</b>." % (n, 100 * n))
        if k == 1:
            n = ri(2, 9)
            return mcq("%d dm = ? cm" % n, "%d cm" % (10 * n), ["%d cm" % (100 * n), "%d cm" % n, "%d cm" % (n + 10)],
                       "1 dm = 10 cm. %d dm = <b>%d cm</b>." % (n, 10 * n))
        if k == 2:
            n = ri(2, 15)
            return mcq("%d cm = ? mm" % n, "%d mm" % (10 * n), ["%d mm" % (100 * n), "%d mm" % n, "%d mm" % (n + 10)],
                       "1 cm = 10 mm. %d cm = <b>%d mm</b>." % (n, 10 * n))
        if k == 3:
            n = ri(2, 9)
            return mcq("%d km = ? m" % n, "%s m" % num(1000 * n), ["%d m" % (100 * n), "%s m" % num(10000 * n), "%d m" % (10 * n)],
                       "1 km = 1 000 m. %d km = <b>%s m</b>." % (n, num(1000 * n)))
        if k == 4:
            n = ri(1, 5)
            return mcq("%d mil = ? km" % n, "%d km" % (10 * n), ["%d km" % (100 * n), "%s km" % num(1000 * n), "%d km" % n],
                       "1 mil = 10 km. %d mil = <b>%d km</b>." % (n, 10 * n))
        n = ri(2, 9) * 100
        return mcq("%d cm = ? m" % n, "%d m" % (n // 100), ["%d m" % (n // 10), "%d m" % n, "%d m" % (n // 1000 or 1 + n // 100)],
                   "100 cm = 1 m. %d cm = <b>%d m</b>." % (n, n // 100))

    def blandad():
        m, c = ri(1, 4), ri(5, 95)
        if c % 10 == 0 and R.random() < 0.5:
            return None
        return mcq("%d m %d cm = ? cm" % (m, c), "%d cm" % (100 * m + c), ["%d cm" % (10 * m + c), "%d cm" % (m + c), "%d cm" % (100 * m + c * 10) if c < 10 else "%s cm" % num(1000 * m + c)],
                   "%d m = %d cm. %d + %d = <b>%d cm</b>." % (m, 100 * m, 100 * m, c, 100 * m + c))

    def enhet():
        obj, unit_ = ch(LANGD_OBJ)
        return mcq("Vilken enhet passar bäst när du mäter längden av %s?" % obj, unit_, [x for x in ("mm", "cm", "m", "km") if x != unit_],
                   "%s mäts bäst i <b>%s</b>." % (cap(obj), unit_))

    def matt():
        a = ri(0, 5)
        b = a + ri(2, 9)
        if b > 15:
            return None
        if a == 0:
            return mcq(linjal(a, b) + "Hur lång är den gröna remsan?", "%d cm" % b, ["%d cm" % (b + 1), "%d cm" % (b - 1), "%d mm" % b],
                       "Remsan börjar vid 0 och slutar vid %d. Den är <b>%d cm</b>." % (b, b))
        return mcq(linjal(a, b) + "Hur lång är den gröna remsan?", "%d cm" % (b - a), ["%d cm" % b, "%d cm" % a, "%d cm" % (b - a + 1)],
                   "Remsan börjar vid %d och slutar vid %d. %d − %d = <b>%d cm</b>." % (a, b, b, a, b - a))

    def jamfor():
        a = ri(1, 4) * 100 + ri(1, 9) * 10
        m = ri(1, 4)
        if a == m * 100:
            return None
        big = "%d cm" % a if a > m * 100 else "%d m" % m
        return mcq("Vilket är längst: %d cm eller %d m?" % (a, m), big, ["%d m" % m if big != "%d m" % m else "%d cm" % a, "De är lika långa", "Det går inte att jämföra"],
                   "%d m = %d cm. %d cm %s %d cm, så <b>%s</b> är längst." % (m, m * 100, a, "&gt;" if a > m * 100 else "&lt;", m * 100, big))

    def text_():
        n, g = K.next()
        k = ri(0, 2)
        if k == 0:
            a, b = ri(1, 3), ri(20, 90)
            return mcq("%s hoppar längd. Första hoppet är %d m och andra hoppet är %d cm längre. Hur långt är andra hoppet?" % (n, a, b),
                       "%d cm" % (100 * a + b), ["%d cm" % (a + b), "%d m" % (a + b), "%d cm" % (10 * a + b)],
                       "%d m = %d cm. %d + %d = <b>%d cm</b>." % (a, 100 * a, 100 * a, b, 100 * a + b))
        if k == 1:
            a = ri(110, 160)
            b = ri(110, 160)
            if a == b:
                return None
            return mcq("%s är %d cm lång och %s kompis är %d cm lång. Hur stor är skillnaden i längd?" % (n, a, hennes(g), b), "%d cm" % abs(a - b),
                       ["%d cm" % (a + b), "%d cm" % max(a, b), "%d cm" % (abs(a - b) + 10)], "%d − %d = <b>%d cm</b>." % (max(a, b), min(a, b), abs(a - b)))
        d = ri(2, 6)
        return mcq("Ett band är %d m långt. Det klipps i bitar som är 50 cm långa. Hur många bitar blir det?" % d, str(2 * d), [str(d), str(50 * d), str(d + 2)],
                   "1 m = 2 bitar på 50 cm. %d m ger <b>%d bitar</b>." % (d, 2 * d))

    sets = [("Omvandla enheter", [(omvandla, 20)]),
            ("Meter och centimeter", [(blandad, 12), (jamfor, 8)]),
            ("Mät med linjal", [(matt, 20)]),
            ("Välj rätt enhet", [(enhet, 12), (omvandla, 8)]),
            ("Textuppgifter", [(text_, 20)])]
    return unit("langd", "G", 16, "Längd: mm, cm, dm, m, km och mil", "Längd",
                "Jämförelse, uppskattning och mätning av längd med vanliga nutida och äldre måttenheter: millimeter, centimeter, decimeter, meter, kilometer och mil.",
                "Arbetsblad om längd för årskurs 3: omvandla mm, cm, dm, m, km och mil, mät med linjal, välj rätt enhet och jämför längder. 100 uppgifter med facit.",
                "1 m = 10 dm = 100 cm", "1 cm = 10 mm, 1 km = 1 000 m, 1 mil = 10 km", sets,
                ["Längd mäts i millimeter (mm), centimeter (cm), decimeter (dm), meter (m), kilometer (km) och mil.",
                 "1 cm = 10 mm, 1 dm = 10 cm, 1 m = 100 cm, 1 km = 1 000 m och 1 mil = 10 km. Mil är en svensk enhet för långa vägar.",
                 "När du mäter med linjal börjar du vid 0. Börjar föremålet vid ett annat tal räknar du skillnaden."],
                [("2 m 35 cm = ? cm", ["2 m = 200 cm", "200 + 35"], "235 cm"), ("Remsan börjar vid 3 cm och slutar vid 9 cm", ["9 − 3"], "6 cm")],
                [["2 m = 20 cm", "1 m = 100 cm, så 2 m = 200 cm"], ["Läser av slutet på linjalen när remsan inte börjar vid 0", "Räkna slutet − början"],
                 ["1 mil = 1 km", "1 mil = 10 km"]],
                [("Hur lång är en mil?", "10 km. Det är en gammal svensk enhet som fortfarande används för långa avstånd."),
                 ("Vilken enhet ska jag välja?", "Små saker i mm eller cm, rum och hus i m och långa vägar i km eller mil."),
                 ("Hur mycket är en decimeter?", "10 cm, ungefär så bred som en vuxens handflata.")])


def hennes(g):
    return "hennes" if g == "f" else "hans"


# ============================================================ 17. Massa och volym
VIKT_OBJ = [("ett äpple", "2 hg", ["2 kg", "2 g", "20 kg"]), ("en mjölkkartong", "1 kg", ["1 g", "10 kg", "1 hg"]),
            ("en katt", "4 kg", ["4 g", "40 kg", "4 hg"]), ("ett gem", "1 g", ["1 kg", "1 hg", "10 kg"]),
            ("en vuxen människa", "70 kg", ["7 kg", "700 kg", "70 hg"]), ("en mobiltelefon", "2 hg", ["2 kg", "20 g", "20 kg"]),
            ("en påse mjöl", "2 kg", ["2 g", "20 kg", "2 hg"]), ("en cykel", "12 kg", ["12 g", "120 kg", "12 hg"])]
VOL_OBJ = [("ett badkar", "200 l", ["200 dl", "2 l", "20 dl"]), ("ett glas", "2 dl", ["2 l", "20 l", "2 ml"]),
           ("en tesked", "5 ml", ["5 l", "5 dl", "50 l"]), ("en hink", "10 l", ["10 dl", "10 ml", "100 l"]),
           ("en mjölkkartong", "1 l", ["1 dl", "10 l", "1 ml"]), ("en kaffekopp", "2 dl", ["2 l", "20 l", "2 ml"])]


def u17():
    def omv_massa():
        k = ri(0, 3)
        if k == 0:
            n = ri(1, 9)
            return mcq("%d kg = ? g" % n, "%s g" % num(1000 * n), ["%d g" % (100 * n), "%d g" % (10 * n), "%s g" % num(10000 * n)],
                       "1 kg = 1 000 g. %d kg = <b>%s g</b>." % (n, num(1000 * n)))
        if k == 1:
            n = ri(1, 9)
            return mcq("%d kg = ? hg" % n, "%d hg" % (10 * n), ["%d hg" % (100 * n), "%d hg" % n, "%s hg" % num(1000 * n)],
                       "1 kg = 10 hg. %d kg = <b>%d hg</b>." % (n, 10 * n))
        if k == 2:
            n = ri(2, 9)
            return mcq("%d hg = ? g" % n, "%d g" % (100 * n), ["%d g" % (10 * n), "%s g" % num(1000 * n), "%d g" % n],
                       "1 hg = 100 g. %d hg = <b>%d g</b>." % (n, 100 * n))
        n = ri(1, 4) * 1000 + ch([0, 500])
        return mcq("%s g = ? kg" % num(n), "%s kg" % (num(n // 1000) if n % 1000 == 0 else "%d,5" % (n // 1000)), ["%d kg" % (n // 100), "%d kg" % (n // 10), "%s kg" % num(n)],
                   "1 000 g = 1 kg. %s g = <b>%s kg</b>." % (num(n), num(n // 1000) if n % 1000 == 0 else "%d,5" % (n // 1000)))

    def omv_vol():
        k = ri(0, 3)
        if k == 0:
            n = ri(1, 9)
            return mcq("%d l = ? dl" % n, "%d dl" % (10 * n), ["%d dl" % (100 * n), "%d dl" % n, "%s dl" % num(1000 * n)],
                       "1 l = 10 dl. %d l = <b>%d dl</b>." % (n, 10 * n))
        if k == 1:
            n = ri(2, 9) * 10
            return mcq("%d dl = ? l" % n, "%d l" % (n // 10), ["%d l" % n, "%d l" % (n * 10), "%d l" % (n // 10 + 1)],
                       "10 dl = 1 l. %d dl = <b>%d l</b>." % (n, n // 10))
        if k == 2:
            n = ri(1, 5)
            return mcq("%d l = ? ml" % n, "%s ml" % num(1000 * n), ["%d ml" % (100 * n), "%d ml" % (10 * n), "%d ml" % n],
                       "1 l = 1 000 ml. %d l = <b>%s ml</b>." % (n, num(1000 * n)))
        n = ri(2, 9)
        return mcq("%d dl = ? cl" % n, "%d cl" % (10 * n), ["%d cl" % (100 * n), "%d cl" % n, "%d cl" % (n + 10)],
                   "1 dl = 10 cl. %d dl = <b>%d cl</b>." % (n, 10 * n))

    def uppskatta():
        if R.random() < 0.55:
            obj, a, w = ch(VIKT_OBJ)
            return mcq(ch(["Ungefär hur mycket väger %s?", "Vilken vikt är rimlig för %s?"]) % obj, a, w, "%s väger ungefär <b>%s</b>." % (cap(obj), a))
        obj, a, w = ch(VOL_OBJ)
        return mcq(ch(["Ungefär hur mycket rymmer %s?", "Vilken volym är rimlig för %s?"]) % obj, a, w, "%s rymmer ungefär <b>%s</b>." % (cap(obj), a))

    def jamfor():
        k = ri(0, 1)
        if k == 0:
            a = ri(3, 18) * 100
            b = ri(1, 2)
            if a == b * 1000:
                return None
            big = "%s g" % num(a) if a > 1000 * b else "%d kg" % b
            return mcq("Vilket väger mest: %s g eller %d kg?" % (num(a), b), big, ["%d kg" % b if big != "%d kg" % b else "%s g" % num(a), "De väger lika mycket", "Det går inte att jämföra"],
                       "%d kg = %s g. Därför väger <b>%s</b> mest." % (b, num(1000 * b), big))
        a, b = ri(3, 25), ri(1, 3)
        if a == 10 * b:
            return None
        big = "%d dl" % a if a > 10 * b else "%d l" % b
        return mcq("Vilket är mest: %d dl eller %d l?" % (a, b), big, ["%d l" % b if big != "%d l" % b else "%d dl" % a, "De är lika mycket", "Det går inte att jämföra"],
                   "%d l = %d dl. Därför är <b>%s</b> mest." % (b, 10 * b, big))

    def text_():
        n, g = K.next()
        k = ri(0, 3)
        if k == 0:
            l, d = ri(1, 3), ch([2, 5])
            return mcq("En kanna rymmer %d l saft. Hur många glas på %d dl kan du fylla?" % (l, d), str(10 * l // d), [str(l * d), str(10 * l), str(10 * l // d + 1)],
                       "%d l = %d dl. %d : %d = <b>%d glas</b>." % (l, 10 * l, 10 * l, d, 10 * l // d)) if (10 * l) % d == 0 else None
        if k == 1:
            a, b = ri(2, 7), ri(2, 7)
            if a + b >= 10:
                return None
            return mcq("%s köper %d hg ost och %d hg skinka. Hur mycket väger det tillsammans?" % (n, a, b), "%d hg" % (a + b),
                       ["%d kg" % (a + b), "%d g" % (a + b), "%d hg" % (a * b)], "%d + %d = <b>%d hg</b>." % (a, b, a + b))
        if k == 2:
            p, w = ri(2, 5), ch([2, 3, 4])
            return mcq("En påse potatis väger %d kg. Hur mycket väger %d påsar?" % (w, p), "%d kg" % (w * p), ["%d kg" % (w + p), "%d hg" % (w * p), "%d kg" % (w * p + w)],
                       "%d × %d = <b>%d kg</b>." % (p, w, w * p))
        l = ri(2, 5)
        d = ri(2, 9)
        return mcq("Det finns %d l mjölk. %s häller upp %d dl. Hur mycket mjölk är kvar?" % (l, n, d), "%d dl" % (10 * l - d), ["%d dl" % (l - d) if l > d else "%d l" % (l - 1), "%d dl" % (10 * l + d), "%d l" % l],
                   "%d l = %d dl. %d − %d = <b>%d dl</b>." % (l, 10 * l, 10 * l, d, 10 * l - d))

    sets = [("Kilogram, hektogram och gram", [(omv_massa, 20)]),
            ("Liter, deciliter och milliliter", [(omv_vol, 20)]),
            ("Uppskatta", [(uppskatta, 20)]),
            ("Jämför", [(jamfor, 20)]),
            ("Textuppgifter", [(text_, 20)])]
    return unit("massa-och-volym", "G", 17, "Massa och volym: kg, hg, g, l, dl och ml", "Massa och volym",
                "Jämförelse, uppskattning och mätning av massa och volym med vanliga måttenheter: kilogram, hektogram, gram, liter, deciliter, centiliter och milliliter.",
                "Arbetsblad om massa och volym för årskurs 3: kg, hg och g, l, dl, cl och ml, uppskatta vikt och volym, jämför och textuppgifter. 100 uppgifter med facit.",
                "1 kg = 10 hg = 1 000 g", "1 l = 10 dl = 1 000 ml", sets,
                ["Massa (vikt) mäts i kilogram (kg), hektogram (hg) och gram (g). 1 kg = 10 hg = 1 000 g.",
                 "Volym mäts i liter (l), deciliter (dl), centiliter (cl) och milliliter (ml). 1 l = 10 dl = 100 cl = 1 000 ml.",
                 "Jämför bara när enheterna är samma. Gör om till samma enhet först: 1 kg är mer än 800 g."],
                [("3 l = ? dl", ["1 l = 10 dl", "3 × 10"], "30 dl"), ("Vilket väger mest: 800 g eller 1 kg?", ["1 kg = 1 000 g", "1 000 &gt; 800"], "1 kg")],
                [["800 g väger mer än 1 kg eftersom 800 &gt; 1", "Gör om: 1 kg = 1 000 g"], ["1 l = 100 dl", "1 l = 10 dl"],
                 ["1 hg = 10 g", "1 hg = 100 g"]],
                [("Vad är ett hekto?", "Ett hektogram, 100 gram. I affären säger man ofta ett hekto godis."),
                 ("Är massa och vikt samma sak?", "I vardagen säger vi vikt. I matematiken heter det massa och mäts i kg och g."),
                 ("Hur mycket är en deciliter?", "En tiondel av en liter. Ett vanligt glas rymmer ungefär 2 dl.")])


# ============================================================ 18. Geometriska figurer
def poly(cx, cy, r, n, rot=-90, col="#cfe6d6"):
    pts = ["%.1f,%.1f" % (cx + r * math.cos(math.radians(rot + i * 360.0 / n)), cy + r * math.sin(math.radians(rot + i * 360.0 / n))) for i in range(n)]
    return "<polygon points='%s' fill='%s' stroke='%s' stroke-width='2'/>" % (" ".join(pts), col, INK)


def figur(kind, cx=50, cy=50, col="#cfe6d6"):
    if kind == "triangel":
        return poly(cx, cy + 6, 40, 3, col=col)
    if kind == "kvadrat":
        return "<rect x='%d' y='%d' width='64' height='64' fill='%s' stroke='%s' stroke-width='2'/>" % (cx - 32, cy - 32, col, INK)
    if kind == "rektangel":
        return "<rect x='%d' y='%d' width='84' height='46' fill='%s' stroke='%s' stroke-width='2'/>" % (cx - 42, cy - 23, col, INK)
    if kind == "cirkel":
        return "<circle cx='%d' cy='%d' r='36' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, col, INK)
    if kind == "femhörning":
        return poly(cx, cy + 3, 40, 5, col=col)
    if kind == "sexhörning":
        return poly(cx, cy, 40, 6, rot=0, col=col)
    if kind == "romb":
        return "<polygon points='%d,%d %d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy - 40, cx + 28, cy, cx, cy + 40, cx - 28, cy, col, INK)
    raise ValueError(kind)


FIG = {"triangel": (3, 3), "kvadrat": (4, 4), "rektangel": (4, 4), "cirkel": (0, 0), "femhörning": (5, 5), "sexhörning": (6, 6), "romb": (4, 4)}


def u18():
    def namn():
        k = ch(list(FIG))
        col = ch(["#cfe6d6", "#f6d8ae", "#c9dcf2", "#f2c4c4"])
        return mcq(wrap(100, 100, figur(k, col=col), "en figur") + "Vad heter figuren?", k, [x for x in sh(FIG) if x != k],
                   "Figuren är en <b>%s</b>." % k)

    def horn():
        k = ch([x for x in FIG if x != "cirkel"])
        s, h = FIG[k]
        what = ch(["hörn", "sidor"])
        n = h if what == "hörn" else s
        c = 1 if R.random() < 0.4 else ri(2, 4)
        if c == 1:
            return mcq("Hur många %s har en %s?" % (what, k), str(n), [str(n + 1), str(n - 1), str(n + 2)],
                       "En %s har %d sidor och %d hörn." % (k, s, h))
        pl = {"triangel": "trianglar", "kvadrat": "kvadrater", "rektangel": "rektanglar", "femhörning": "femhörningar", "sexhörning": "sexhörningar", "romb": "romber"}[k]
        return mcq("Hur många %s har %d %s tillsammans?" % (what, c, pl), str(c * n), [str(c * n + c), str(c + n), str(c * n - n), str(n)],
                   "En %s har %d %s. %d × %d = <b>%d</b>." % (k, n, what, c, n, c * n))

    def egenskap():
        opts = [("Vilken figur har 4 lika långa sidor och 4 räta vinklar?", "kvadrat", ["rektangel", "romb", "triangel"]),
                ("Vilken figur har inga hörn?", "cirkel", ["triangel", "kvadrat", "femhörning"]),
                ("Vilken figur har 3 sidor?", "triangel", ["kvadrat", "cirkel", "femhörning"]),
                ("Vilken figur har 4 räta vinklar men inte alla sidor lika långa?", "rektangel", ["kvadrat", "romb", "triangel"]),
                ("Vilken figur har 6 hörn?", "sexhörning", ["femhörning", "kvadrat", "triangel"]),
                ("Vilken figur har 5 sidor?", "femhörning", ["sexhörning", "rektangel", "triangel"]),
                ("Vilken figur har 4 lika långa sidor men inga räta vinklar?", "romb", ["kvadrat", "rektangel", "triangel"]),
                ("Vilken figur är inte en fyrhörning?", "triangel", ["kvadrat", "rektangel", "romb"]),
                ("Vilken figur är en fyrhörning?", "rektangel", ["triangel", "cirkel", "femhörning"]),
                ("Vilken figur har lika många hörn som sidor, nämligen 5?", "femhörning", ["sexhörning", "kvadrat", "cirkel"])]
        q, a, w = ch(opts)
        return mcq(q, a, w, "Rätt svar är <b>%s</b>." % a)

    def rakna():
        kinds = sh(["triangel", "kvadrat", "cirkel", "rektangel"])
        target = kinds[0]
        cnt = ri(2, 5)
        items = [target] * cnt + [ch(kinds[1:]) for _ in range(ri(3, 5))]
        items = sh(items)
        s = []
        cols = ["#cfe6d6", "#f6d8ae", "#c9dcf2", "#f2c4c4"]
        for i, k in enumerate(items):
            g = figur(k, 50, 50, ch(cols))
            s.append("<g transform='translate(%d,%d) scale(0.55)'>%s</g>" % ((i % 5) * 62, (i // 5) * 62, g))
        rows = (len(items) + 4) // 5
        pic = wrap(5 * 62, rows * 62, "".join(s), "olika figurer")
        pl = {"triangel": "trianglar", "kvadrat": "kvadrater", "cirkel": "cirklar", "rektangel": "rektanglar"}[target]
        return mcq(pic + "Hur många %s finns det?" % pl, str(cnt), [str(cnt + 1), str(cnt - 1), str(len(items))],
                   "Räkna bara %s: <b>%d</b>." % (pl, cnt))

    def begrepp():
        opts = [("Vad kallas en rak linje med två ändpunkter?", "en sträcka", ["en linje", "en punkt", "en cirkel"]),
                ("Vad kallas hörnet där två sidor möts i en kvadrat?", "en rät vinkel", ["en sträcka", "en mittpunkt", "en diameter"]),
                ("Hur många räta vinklar har en rektangel?", "4", ["2", "3", "0"]),
                ("Hur många räta vinklar har en kvadrat?", "4", ["2", "1", "0"]),
                ("Vad är en linje?", "rak och utan slut åt båda hållen", ["rak med två ändpunkter", "en böjd kurva", "en punkt"]),
                ("En kvadrat är också en …", "rektangel", ["triangel", "cirkel", "femhörning"]),
                ("Vad kallas en figur med 4 sidor?", "fyrhörning", ["triangel", "femhörning", "cirkel"]),
                ("Vad kallas en figur med 8 sidor?", "åttahörning", ["sexhörning", "femhörning", "fyrhörning"])]
        q, a, w = ch(opts)
        return mcq(q, a, w, "Rätt svar: <b>%s</b>." % a)

    def omkrets():
        k = ch(["kvadrat", "rektangel", "triangel"])
        if k == "kvadrat":
            a = ri(2, 12)
            return mcq("En kvadrat har sidan %d cm. Hur lång är det runt hela kvadraten?" % a, "%d cm" % (4 * a), ["%d cm" % (2 * a), "%d cm" % (a * a) if a * a != 4 * a else "%d cm" % (3 * a), "%d cm" % (a + 4)],
                       "Fyra lika långa sidor: %d + %d + %d + %d = <b>%d cm</b>." % (a, a, a, a, 4 * a))
        if k == "rektangel":
            a, b = ri(5, 15), ri(2, 8)
            if a == b:
                return None
            return mcq("En rektangel är %d cm lång och %d cm bred. Hur lång är det runt hela rektangeln?" % (a, b), "%d cm" % (2 * a + 2 * b),
                       ["%d cm" % (a + b), "%d cm" % (a * b) if a * b != 2 * (a + b) else "%d cm" % (a + b + 1), "%d cm" % (2 * a + b)],
                       "%d + %d + %d + %d = <b>%d cm</b>." % (a, b, a, b, 2 * (a + b)))
        a, b, c = ri(3, 9), ri(3, 9), ri(3, 9)
        if a + b <= c or a + c <= b or b + c <= a:
            return None
        return mcq("En triangel har sidorna %d cm, %d cm och %d cm. Hur lång är det runt hela triangeln?" % (a, b, c), "%d cm" % (a + b + c),
                   ["%d cm" % (a + b), "%d cm" % (a * b), "%d cm" % (a + b + c + 1)], "%d + %d + %d = <b>%d cm</b>." % (a, b, c, a + b + c))

    sets = [("Känn igen figurer", [(namn, 20)]),
            ("Sidor och hörn", [(horn, 20)]),
            ("Figurernas egenskaper", [(egenskap, 10), (begrepp, 8), (namn, 2)]),
            ("Räkna figurer", [(rakna, 20)]),
            ("Runt figuren", [(omkrets, 14), (horn, 6)])]
    return unit("geometriska-figurer", "G", 18, "Geometriska figurer: trianglar, fyrhörningar och cirklar", "Geometriska figurer",
                "Grundläggande geometriska objekt, däribland punkter, linjer, sträckor, fyrhörningar, trianglar och cirklar, samt deras egenskaper.",
                "Arbetsblad om geometriska figurer för årskurs 3: triangel, kvadrat, rektangel, romb, femhörning och cirkel, sidor och hörn, räta vinklar och längden runt en figur. 100 uppgifter med facit.",
                "Räkna sidor och hörn", "En figur har lika många hörn som sidor.", sets,
                ["En triangel har 3 sidor och 3 hörn. En fyrhörning har 4 sidor och 4 hörn. En femhörning har 5 och en sexhörning har 6.",
                 "En kvadrat har 4 lika långa sidor och 4 räta vinklar. En rektangel har 4 räta vinklar, och motstående sidor är lika långa. En kvadrat är en sorts rektangel.",
                 "En cirkel har inga hörn. En sträcka är rak och har två ändpunkter. En linje fortsätter utan slut åt båda hållen."],
                [("Hur många hörn har en sexhörning?", ["Lika många som sidorna"], "6"), ("Längden runt en kvadrat med sidan 5 cm", ["5 + 5 + 5 + 5"], "20 cm")],
                [["En kvadrat är inte en rektangel", "En kvadrat har 4 räta vinklar, så den är en rektangel"], ["Räknar en cirkels kant som ett hörn", "En cirkel har inga hörn"],
                 ["Runt en rektangel 8 cm och 3 cm: 8 + 3 = 11 cm", "Alla fyra sidor: 8 + 3 + 8 + 3 = 22 cm"]],
                [("Vad är en rät vinkel?", "Ett hörn som ser ut som hörnet på ett papper. Det är 90 grader."),
                 ("Är en romb samma sak som en kvadrat?", "Båda har 4 lika långa sidor, men kvadraten har också räta vinklar."),
                 ("Vad heter längden runt en figur?", "Den heter omkrets. Du räknar ut den genom att lägga ihop alla sidor.")])


# ============================================================ 19. Geometriska kroppar
import de_common as _D

KROPP = {"klot": "kugel", "kub": "wuerfel", "rätblock": "quader", "cylinder": "zylinder", "kon": "kegel", "pyramid": "pyramide"}
YTOR = {"kub": (6, 12, 8), "rätblock": (6, 12, 8), "pyramid": (5, 8, 5)}
SAKER = [("en fotboll", "klot"), ("en apelsin", "klot"), ("en tärning", "kub"), ("en sockerbit", "kub"), ("ett mjölkpaket", "rätblock"),
         ("en tegelsten", "rätblock"), ("en skokartong", "rätblock"), ("en konservburk", "cylinder"), ("ett ljus", "cylinder"), ("en toarulle", "cylinder"),
         ("en glasstrut", "kon"), ("en trafikkon", "kon"), ("ett tält", "pyramid"), ("en jordglob", "klot"),
         ("en pingisboll", "klot"), ("en pärla", "klot"), ("en tändsticksask", "rätblock"), ("ett kylskåp", "rätblock"), ("en tvål", "rätblock"),
         ("ett rör", "cylinder"), ("en stock", "cylinder"), ("en partyhatt", "kon"), ("en strut med popcorn", "kon"), ("pyramiderna i Egypten", "pyramid"),
         ("en isbit", "kub"), ("en byggkloss med sex lika stora kvadratiska sidor", "kub")]


def kropp_svg(k, col="#cfe6d6", r=34):
    return _D.solid_svg(KROPP[k], r, col).replace("ein Körper", "en geometrisk kropp")


def art(k):
    return "ett" if k in ("klot", "rätblock") else "en"


def u19():
    def namn():
        k = ch(list(KROPP))
        return mcq(kropp_svg(k, ch(["#cfe6d6", "#f6d8ae", "#c9dcf2", "#f2c4c4"]), ch([28, 32, 36])) + "Vad heter kroppen?", k, [x for x in sh(KROPP) if x != k], "Kroppen är %s <b>%s</b>." % (art(k), k))

    def sak():
        obj, k = ch(SAKER)
        return mcq(ch(["Vilken geometrisk kropp liknar %s?", "Vilken form har %s?"]) % obj, k, [x for x in sh(KROPP) if x != k], "%s liknar %s <b>%s</b>." % (cap(obj), art(k), k))

    def rakna():
        k = ch(list(YTOR))
        f, e, v = YTOR[k]
        what = ch(["sidoytor", "kanter", "hörn"])
        n = {"sidoytor": f, "kanter": e, "hörn": v}[what]
        c = 1 if R.random() < 0.3 else ri(2, 5)
        if c == 1:
            return mcq(kropp_svg(k) + "Hur många %s har %s %s?" % (what, art(k), k), str(n), [str(x) for x in (f, e, v, n + 1, n - 1, n + 2) if x != n],
                       "%s %s har %d sidoytor, %d kanter och %d hörn." % (cap(art(k)), k, f, e, v))
        pl = {"kub": "kuber", "rätblock": "rätblock", "pyramid": "pyramider"}[k]
        return mcq("Hur många %s har %d %s tillsammans?" % (what, c, pl), str(c * n), [str(c * n + c), str(c + n), str(c * n - n), str(n)],
                   "%s %s har %d %s. %d × %d = <b>%d</b>." % (cap(art(k)), k, n, what, c, n, c * n))

    def egenskap():
        opts = [("Vilken kropp kan rulla åt alla håll?", "klot", ["kub", "cylinder", "pyramid"]),
                ("Vilken kropp har bara kvadrater som sidoytor?", "kub", ["rätblock", "pyramid", "cylinder"]),
                ("Vilken kropp har en spets och en rund bottenyta?", "kon", ["pyramid", "cylinder", "klot"]),
                ("Vilken kropp har två runda plana ytor?", "cylinder", ["kon", "klot", "kub"]),
                ("Vilken kropp har inga kanter och inga hörn?", "klot", ["kub", "kon", "pyramid"]),
                ("Vilken kropp har en kvadrat som botten och trianglar som sidor?", "pyramid", ["kub", "kon", "rätblock"]),
                ("Vilken kropp har 6 sidoytor som är rektanglar?", "rätblock", ["kub", "pyramid", "cylinder"]),
                ("Vilken kropp kan både rulla och stå stadigt på en plan yta, men har ingen spets?", "cylinder", ["klot", "kon", "kub"])]
        q, a, w = ch(opts)
        return mcq(q, a, w, "Rätt svar: <b>%s</b>." % a)

    def yta():
        k = ch(["kub", "rätblock", "pyramid", "cylinder", "kon"])
        a = {"kub": "kvadrat", "rätblock": "rektangel", "pyramid": "triangel", "cylinder": "cirkel", "kon": "cirkel"}[k]
        extra = {"pyramid": " (på sidorna)", "cylinder": " (överst och underst)", "kon": " (botten)"}.get(k, "")
        return mcq("Vilken figur ser du om du ritar runt en sidoyta på %s %s%s?" % (art(k), k, extra), a, [x for x in ("kvadrat", "rektangel", "triangel", "cirkel") if x != a],
                   "%s %s har sidoytor som är <b>%s</b>%s." % (cap(art(k)), k, {"kvadrat": "kvadrater", "rektangel": "rektanglar", "triangel": "trianglar", "cirkel": "cirklar"}[a],
                                                          " (en kub är också en sorts rätblock)" if k == "kub" else ""))

    sets = [("Känn igen kroppar", [(namn, 20)]),
            ("Kroppar i vardagen", [(sak, 20)]),
            ("Sidoytor, kanter och hörn", [(rakna, 20)]),
            ("Kropparnas egenskaper", [(egenskap, 8), (yta, 5), (rakna, 7)]),
            ("Blandat", [(namn, 5), (sak, 5), (rakna, 10)])]
    return unit("geometriska-kroppar", "G", 19, "Geometriska kroppar: klot, kub, rätblock, cylinder, kon och pyramid", "Geometriska kroppar",
                "Grundläggande geometriska objekt, däribland klot, koner, cylindrar och rätblock samt deras inbördes relationer och egenskaper.",
                "Arbetsblad om geometriska kroppar för årskurs 3: klot, kub, rätblock, cylinder, kon och pyramid, kroppar i vardagen, sidoytor, kanter och hörn. 100 uppgifter med facit.",
                "Sidoytor, kanter och hörn", "En kub har 6 sidoytor, 12 kanter och 8 hörn.", sets,
                ["En kropp är tredimensionell, den har längd, bredd och höjd. Exempel: klot (en boll), kub (en tärning), rätblock (ett mjölkpaket), cylinder (en burk), kon (en glasstrut) och pyramid.",
                 "En sidoyta är en plan yta på kroppen. En kant är där två sidoytor möts. Ett hörn är där kanterna möts.",
                 "En kub och ett rätblock har 6 sidoytor, 12 kanter och 8 hörn. En pyramid med kvadratisk botten har 5 sidoytor, 8 kanter och 5 hörn."],
                [("En tärning", ["6 kvadratiska sidoytor"], "kub"), ("Kanter på ett rätblock", ["4 upptill, 4 nertill, 4 på sidorna"], "12")],
                [["Blandar ihop kub och kvadrat", "En kvadrat är platt. En kub är en kropp med 6 kvadrater"], ["Räknar bara kanterna man ser", "Räkna även de dolda kanterna: 12"],
                 ["Säger att ett klot är en cirkel", "Cirkeln är platt. Klotet är runt åt alla håll"]],
                [("Vad är skillnaden mellan en figur och en kropp?", "En figur är platt, till exempel en kvadrat. En kropp har tre dimensioner, till exempel en kub."),
                 ("Är en kub ett rätblock?", "Ja. En kub är ett rätblock där alla sidoytor är kvadrater."),
                 ("Har en cylinder några kanter?", "Den har två böjda kanter där de runda ytorna möter den buktiga sidan, men inga hörn.")])


# ============================================================ 20. Symmetri
import gen_de_mathe_k3_achsensymmetrie as SY


def _sv(s):
    return s.replace("vier Figuren A bis D", "fyra figurer A till D").replace("halbe Figur mit Spiegelachse", "halv figur med symmetrilinje")


def u20():
    SY.R = random.Random(R.random())

    def vilken():
        hs = [SY.half() for _ in range(4)]
        if not all(hs):
            return None
        good = SY.mirror(hs[0])
        bads = [SY.broken(SY.mirror(hs[1])), SY.shifted(hs[2]), SY.broken(SY.mirror(hs[3]))]
        if not all(bads) or any(b == SY.mirror({(x, y) for x, y in b if x < 3}) for b in bads):
            return None
        figs = bads + [good]
        SY.R.shuffle(figs)
        k = figs.index(good)
        return mcq(_sv(SY.four(figs)) + "Vilken figur är symmetrisk kring den röda linjen?", "ABCD"[k], ["ABCD"[i] for i in range(4) if i != k],
                   "Bara i figur %s är rutorna på båda sidor lika långt från linjen, som en spegelbild." % "ABCD"[k])

    def fyll():
        h = SY.half()
        if not h:
            return None
        good = SY.mirror(h)
        sh_ = SY.shifted(h)
        near = SY.broken(good)
        flipped = set(h) | {(SY.COLS - 1 - x, SY.ROWS - 1 - y) for x, y in h}
        opts = [good, sh_, near, flipped]
        if not near or len({frozenset(o) for o in opts}) < 4:
            return None
        pic = _sv(wrap(SY.COLS * SY.Q + 20, SY.ROWS * SY.Q + 20, SY.grid(10, 10, h), "halv figur med symmetrilinje"))
        SY.R.shuffle(opts)
        k = opts.index(good)
        return mcq(pic + "Så ser den vänstra halvan ut. Vilken bild visar hela den symmetriska figuren?" + _sv(SY.four(opts)), "ABCD"[k],
                   ["ABCD"[i] for i in range(4) if i != k], "Varje ruta speglas i linjen: lika långt bort, på andra sidan. Rätt är <b>%s</b>." % "ABCD"[k])

    LOD = list("AHIMOTUVWXY")
    VAG = list("BCDEK")
    INGA = list("FGJLNPQRSZ")

    def bokstav():
        kind = ch(["lod", "lod", "vag", "inte"])
        if kind == "lod":
            a = ch(LOD)
            w = R.sample(INGA, 3)
            return mcq("Vilken bokstav har en <b>lodrät</b> symmetrilinje? %s" % ", ".join(sorted([a] + w)), a, w,
                       "Viker du %s längs en lodrät linje i mitten passar halvorna precis. Svar: <b>%s</b>." % (a, a))
        if kind == "vag":
            a = ch(VAG)
            w = R.sample(INGA, 3)
            return mcq("Vilken bokstav har en <b>vågrät</b> symmetrilinje? %s" % ", ".join(sorted([a] + w)), a, w,
                       "Den övre och den undre halvan av %s passar precis. Svar: <b>%s</b>." % (a, a))
        a = ch(INGA)
        w = R.sample(LOD + VAG, 3)
        return mcq("Vilken bokstav är <b>inte</b> symmetrisk? %s" % ", ".join(sorted([a] + w)), a, w,
                   "%s har ingen symmetrilinje. De andra kan vikas så att halvorna passar. Svar: <b>%s</b>." % (a, a))

    def punkt():
        kind = ch(["sida", "avstand", "ruta"])
        if kind == "sida":
            n = ri(1, 6)
            side = ch(["till vänster", "till höger"])
            other = "till höger" if side == "till vänster" else "till vänster"
            ans = "%d rutor %s om linjen" % (n, other) if n > 1 else "1 ruta %s om linjen" % other
            rr = lambda k, s: ("%d rutor %s om linjen" % (k, s)) if k > 1 else ("1 ruta %s om linjen" % s)
            return mcq("En punkt ligger %s %s om en lodrät symmetrilinje. Var ligger spegelpunkten?" % ("%d rutor" % n if n > 1 else "1 ruta", side), ans,
                       [rr(n, side), rr(n + 1, other), rr(2 * n, other)], "Spegelpunkten ligger lika långt från linjen, men på andra sidan: <b>%s</b>." % ans)
        if kind == "avstand":
            n = ri(1, 7)
            return mcq("En punkt ligger %d rutor från symmetrilinjen. Hur långt är det mellan punkten och spegelpunkten?" % n if n > 1 else
                       "En punkt ligger 1 ruta från symmetrilinjen. Hur långt är det mellan punkten och spegelpunkten?",
                       "%d rutor" % (2 * n), ["%d rutor" % x for x in (n + 1, 2 * n + 2, 3 * n)] + (["1 ruta"] if n == 1 else ["%d rutor" % n]),
                       "%d till linjen och %d till på andra sidan: <b>%d rutor</b>." % (n, n, 2 * n))
        x = ri(0, 2)
        y = ri(0, SY.ROWS - 1)
        mx = SY.COLS - 1 - x
        s = SY.grid(10, 10, {(x, y)})
        for i in range(SY.COLS):
            s += text(10 + i * SY.Q + SY.Q / 2.0, 10 + SY.ROWS * SY.Q + 14, str(i + 1), 10, weight=400)
        pic = wrap(SY.COLS * SY.Q + 20, SY.ROWS * SY.Q + 30, s, "rutnät med en ruta och symmetrilinje")
        return mcq(pic + "I vilken kolumn hamnar spegelbilden av den färgade rutan? (Kolumnerna är numrerade nedtill.)", "kolumn %d" % (mx + 1),
                   ["kolumn %d" % c for c in (x + 4, mx, mx + 2 if mx + 2 <= SY.COLS else x + 1, x + 1) if c != mx + 1 and 1 <= c <= SY.COLS],
                   "Rutan ligger %d rutor från linjen. Spegelbilden ligger lika långt på andra sidan: <b>kolumn %d</b>." % (3 - x, mx + 1))

    LINJER = [("en kvadrat", "4"), ("en rektangel som inte är en kvadrat", "2"), ("en liksidig triangel", "3"), ("en cirkel", "oändligt många"),
              ("ett hjärta", "1"), ("en fjäril", "1"), ("en regelbunden sexhörning", "6"), ("bokstaven H", "2"), ("bokstaven A", "1"),
              ("bokstaven F", "ingen"), ("siffran 8", "2"), ("siffran 3", "1")]

    def linjer():
        thing, ans = ch(LINJER)
        near = {"4": ["2", "8"], "2": ["4", "1"], "3": ["1", "6"], "oändligt många": ["1", "4"], "1": ["2", "ingen"], "6": ["3", "12"], "ingen": ["1", "2"]}[ans]
        rest = [x for x in ["ingen", "1", "2", "3", "4", "6", "oändligt många"] if x != ans]
        return mcq("Hur många symmetrilinjer har %s?" % thing, ans, near + sh(rest),
                   "%s har <b>%s</b> symmetrilinje%s." % (cap(thing), ans, "" if ans in ("1", "ingen") else "r"))

    sets = [("Är figuren symmetrisk?", [(vilken, 20)]),
            ("Rita klart figuren", [(fyll, 20)]),
            ("Symmetriska bokstäver", [(bokstav, 20)]),
            ("Spegelpunkter", [(punkt, 20)]),
            ("Antal symmetrilinjer", [(linjer, 10), (bokstav, 4), (punkt, 6)])]
    return unit("symmetri", "G", 20, "Symmetri: symmetrilinje och spegelbild", "Symmetri",
                "Symmetri, till exempel i bilder och i naturen, och hur symmetri kan konstrueras.",
                "Arbetsblad om symmetri för årskurs 3: symmetriska figurer, rita klart en spegelbild, symmetriska bokstäver, spegelpunkter och antal symmetrilinjer. 100 uppgifter med facit.",
                "Lika långt på båda sidor", "Spegelbilden ligger lika långt från linjen.", sets,
                ["En figur är symmetrisk om du kan vika den längs en linje så att båda halvorna passar precis. Linjen heter symmetrilinje.",
                 "När du speglar en punkt ligger spegelbilden lika långt från symmetrilinjen, fast på andra sidan.",
                 "En figur kan ha flera symmetrilinjer. En kvadrat har 4 och en cirkel har oändligt många."],
                [("En punkt ligger 3 rutor till vänster om linjen", ["Spegelbilden ligger lika långt bort", "på andra sidan"], "3 rutor till höger"),
                 ("Symmetrilinjer i en rektangel", ["En lodrät och en vågrät"], "2")],
                [["Flyttar halvan i stället för att spegla den", "Spegla: det som är närmast linjen hamnar närmast linjen"],
                 ["Tror att diagonalen i en rektangel är en symmetrilinje", "Viker du längs diagonalen passar inte halvorna"],
                 ["Räknar avståndet till spegelpunkten som 3 rutor", "3 till linjen + 3 till = 6 rutor"]],
                [("Var finns symmetri i naturen?", "En fjäril, ett löv och många blommor är nästan symmetriska."),
                 ("Hur kan jag testa symmetri?", "Vik papperet längs linjen eller ställ en spegel på linjen."),
                 ("Vad betyder lodrät och vågrät?", "Lodrät går rakt upp och ner. Vågrät går rakt åt sidan, som vattenytan.")])


# ============================================================ 21. Lägesord och stegvisa instruktioner
SAK = ["boll", "bok", "katt", "hund", "äpple", "stol", "lampa", "nyckel", "sko", "mössa"]
SAKF = {"boll": "bollen", "bok": "boken", "katt": "katten", "hund": "hunden", "äpple": "äpplet", "stol": "stolen",
        "lampa": "lampan", "nyckel": "nyckeln", "sko": "skon", "mössa": "mössan"}


def karta(cells, start=None, n=5):
    Q = 46
    s = []
    for i in range(n + 1):
        s.append(line(10, 10 + i * Q, 10 + n * Q, 10 + i * Q, "#9bb", 1))
        s.append(line(10 + i * Q, 10, 10 + i * Q, 10 + n * Q, "#9bb", 1))
    for (x, y), w in cells.items():
        s.append(text(10 + x * Q + Q / 2.0, 10 + y * Q + Q / 2.0 + 5, w, 12))
    if start:
        x, y = start
        s.append("<circle cx='%.1f' cy='%.1f' r='15' fill='none' stroke='%s' stroke-width='2.5'/>" % (10 + x * Q + Q / 2.0, 10 + y * Q + Q / 2.0, RED))
    return wrap(n * Q + 20, n * Q + 20, "".join(s), "rutnät med saker", lg=True)


def u21():
    def board(k=6):
        pos = R.sample([(x, y) for x in range(5) for y in range(5)], k)
        things = R.sample(SAK, k)
        return dict(zip(pos, things))

    def granne():
        b = board()
        rel = ch([("till vänster om", (-1, 0)), ("till höger om", (1, 0)), ("ovanför", (0, -1)), ("under", (0, 1))])
        cands = [(p, w) for p, w in b.items() if (p[0] + rel[1][0], p[1] + rel[1][1]) in b]
        if not cands:
            return None
        (x, y), w = ch(cands)
        ans = b[(x + rel[1][0], y + rel[1][1])]
        return mcq(karta(b) + "Vad finns direkt %s %s?" % (rel[0], SAKF[w]), ans, [v for v in b.values() if v not in (ans, w)],
                   "Gå en ruta %s från %s. Där finns en <b>%s</b>." % ({"till vänster om": "åt vänster", "till höger om": "åt höger", "ovanför": "uppåt", "under": "nedåt"}[rel[0]], SAKF[w], ans)
                   if ans not in ("äpple",) else "Gå en ruta från %s. Där finns ett <b>äpple</b>." % SAKF[w])

    def steg():
        b = board()
        sx, sy = ri(0, 4), ri(0, 4)
        targets = [(p, w) for p, w in b.items() if p != (sx, sy)]
        (tx, ty), w = ch(targets)
        dx, dy = tx - sx, ty - sy
        if dx == 0 or dy == 0:
            return None
        ins = "%d steg %s och %d steg %s" % (abs(dx), "åt höger" if dx > 0 else "åt vänster", abs(dy), "nedåt" if dy > 0 else "uppåt")
        return mcq(karta(b, (sx, sy)) + "Börja i den röda ringen. Gå %s. Vad hittar du?" % ins, w, [v for v in b.values() if v != w and v != b.get((sx, sy))],
                   "Följ stegen ruta för ruta. Du hamnar vid <b>%s</b>." % SAKF[w])

    def instruktion():
        b = board()
        sx, sy = ri(0, 4), ri(0, 4)
        targets = [(p, w) for p, w in b.items() if p != (sx, sy) and p[0] != sx and p[1] != sy]
        if not targets:
            return None
        (tx, ty), w = ch(targets)
        dx, dy = tx - sx, ty - sy
        f = lambda a, c: "%d %s, %d %s" % (abs(a), "höger" if a > 0 else "vänster", abs(c), "ner" if c > 0 else "upp")
        good = f(dx, dy)
        w_ = [f(-dx, dy), f(dx, -dy), f(dy if dy else 1, dx) if abs(dx) != abs(dy) else f(dx + (1 if dx > 0 else -1), dy)]
        return mcq(karta(b, (sx, sy)) + "Vilken instruktion tar dig från den röda ringen till %s?" % SAKF[w], good, w_,
                   "Räkna rutorna åt sidan och sedan upp eller ner: <b>%s</b>." % good)

    def ord_():
        opts = [("Katten sitter på stolen. Var är stolen?", "under katten", ["ovanpå katten", "bredvid katten", "framför katten"]),
                ("Boken ligger under bordet. Var är bordet?", "ovanför boken", ["under boken", "bredvid boken", "bakom boken"]),
                ("Ali står framför Maja. Vem står bakom?", "Maja", ["Ali", "båda", "ingen"]),
                ("Lampan hänger ovanför bordet. Vad är under lampan?", "bordet", ["taket", "lampan", "golvet ovanför"]),
                ("Saga sitter mellan Nils och Ebba. Vem sitter i mitten?", "Saga", ["Nils", "Ebba", "ingen"]),
                ("Du står vänd mot tavlan och vänder dig ett halvt varv. Vart tittar du nu?", "bort från tavlan", ["mot tavlan", "åt vänster", "åt höger"]),
                ("Du tittar framåt och vänder dig ett kvarts varv åt höger. Vart pekar din högra arm nu?", "bakåt", ["framåt", "åt vänster", "uppåt"]),
                ("Hunden ligger bredvid sängen. Vad betyder bredvid?", "vid sidan av", ["ovanpå", "under", "inuti"])]
        q, a, w = ch(opts)
        return mcq(q, a, w, "Rätt svar: <b>%s</b>." % a)

    def program():
        x, y = ri(1, 3), ri(1, 3)
        moves = [ch(["höger", "vänster", "upp", "ner"]) for _ in range(ri(3, 5))]
        d = {"höger": (1, 0), "vänster": (-1, 0), "upp": (0, 1), "ner": (0, -1)}
        px, py = x, y
        for m in moves:
            px += d[m][0]
            py += d[m][1]
        good = "(%d, %d)" % (px, py)
        w = ["(%d, %d)" % (px + 1, py), "(%d, %d)" % (px, py + 1), "(%d, %d)" % (py, px) if px != py else "(%d, %d)" % (px - 1, py)]
        return mcq("En robot står på (%d, %d). Den första siffran är steg åt höger och den andra steg uppåt. Roboten följer programmet: %s. Var står roboten nu?" % (x, y, ", ".join(moves)),
                   good, w, "Följ varje steg: höger och vänster ändrar den första siffran, upp och ner den andra. Roboten står på <b>%s</b>." % good)

    sets = [("Lägesord", [(ord_, 8), (granne, 12)]),
            ("Vad finns bredvid?", [(granne, 20)]),
            ("Följ stegen", [(steg, 20)]),
            ("Skriv instruktionen", [(instruktion, 20)]),
            ("Programmera en robot", [(program, 20)])]
    return unit("lagesord-och-stegvisa-instruktioner", "G", 21, "Lägesord och stegvisa instruktioner", "Lägesord och instruktioner",
                "Vanliga lägesord för att beskriva föremåls läge i rummet. Hur entydiga stegvisa instruktioner kan konstrueras, beskrivas och följas som grund för programmering.",
                "Arbetsblad om lägesord och programmering för årskurs 3: till vänster om, under och bredvid, följ steg i ett rutnät, skriv instruktioner och programmera en robot. 100 uppgifter med facit.",
                "Ett steg i taget", "En instruktion måste vara tydlig och gå i rätt ordning.", sets,
                ["Lägesord beskriver var något är: ovanför, under, bredvid, framför, bakom, mellan, till vänster om och till höger om.",
                 "I ett rutnät går du ett steg i taget. Räkna rutorna åt höger eller vänster och upp eller ner.",
                 "Ett program är en lista med tydliga instruktioner i rätt ordning. Ändrar du ordningen eller ett steg kan roboten hamna fel."],
                [("Från ringen: 2 steg åt höger och 1 steg nedåt", ["Räkna 2 rutor åt höger", "Räkna 1 ruta nedåt"], "Du hamnar på rätt ruta"),
                 ("Robot på (1, 2): höger, höger, upp", ["(2, 2)", "(3, 2)", "(3, 3)"], "(3, 3)")],
                [["Blandar ihop vänster och höger", "Höger är den hand du skriver med för de flesta. Kontrollera med bilden"],
                 ["Räknar startrutan som ett steg", "Första steget går till nästa ruta"], ["Hoppar över ett steg i programmet", "Följ varje steg i ordning"]],
                [("Vad är en instruktion?", "En tydlig beskrivning av vad man ska göra, till exempel gå 2 steg åt höger."),
                 ("Vad har det här med programmering att göra?", "En dator följer instruktioner steg för steg, precis som roboten."),
                 ("Är till vänster om alltid samma sak?", "Det beror på hur man står. På en bild menar vi vänster som du ser den.")])


# ============================================================ 22. Tabeller och diagram
DJUR = ["hund", "katt", "kanin", "häst", "fisk", "hamster"]
FRUKT = ["äpple", "banan", "päron", "apelsin", "kiwi"]
SPORT = ["fotboll", "simning", "dans", "hockey", "ridning", "innebandy"]


def u22():
    def data(k=4, lo=2, hi=12):
        cat = ch([("djur", DJUR, "Favoritdjur"), ("frukt", FRUKT, "Favoritfrukt"), ("sport", SPORT, "Favoritsport")])
        names = R.sample(cat[1], k)
        vals = [ri(lo, hi) for _ in range(k)]
        if len(set(vals)) < k:
            return None
        return cat, list(zip(names, vals))

    def las():
        d = data()
        if not d:
            return None
        cat, dv = d
        n, v = ch(dv)
        return mcq(stapel(dv, "antal") + "%s. Hur många valde %s?" % (cat[2], n), str(v), [str(v + 1), str(v - 1), str(max(x for _, x in dv) + (1 if v != max(x for _, x in dv) else 2))],
                   "Stapeln för %s når upp till <b>%d</b>." % (n, v))

    def mest():
        d = data()
        if not d:
            return None
        cat, dv = d
        most = R.random() < 0.6
        a = (max if most else min)(dv, key=lambda t: t[1])[0]
        return mcq(stapel(dv, "antal") + "%s. Vilket valdes %s?" % (cat[2], "flest gånger" if most else "minst antal gånger"), a, [n for n, _ in dv if n != a],
                   "Den %s stapeln är <b>%s</b>." % ("högsta" if most else "lägsta", a))

    def skillnad():
        d = data()
        if not d:
            return None
        cat, dv = d
        (a, x), (b, y) = R.sample(dv, 2)
        if x == y:
            return None
        big, sm = (a, x) if x > y else (b, y), (b, y) if x > y else (a, x)
        return mcq(stapel(dv, "antal") + "Hur många fler valde %s än %s?" % (big[0], sm[0]), str(big[1] - sm[1]), [str(big[1] + sm[1]), str(big[1]), str(big[1] - sm[1] + 1)],
                   "%d − %d = <b>%d</b>." % (big[1], sm[1], big[1] - sm[1]))

    def totalt():
        d = data(3, 2, 9)
        if not d:
            return None
        cat, dv = d
        t = sum(v for _, v in dv)
        rows = "".join("<tr><td>%s</td><td>%d</td></tr>" % (n, v) for n, v in dv)
        tab = "<table class='sn-table' style='width:auto'><thead><tr><th>%s</th><th>Antal</th></tr></thead><tbody>%s</tbody></table>" % (cat[0].capitalize(), rows)
        return mcq(tab + "Hur många elever svarade totalt?", str(t), [str(t + 1), str(t - 2), str(max(v for _, v in dv))],
                   "%s = <b>%d</b>." % (" + ".join(str(v) for _, v in dv), t))

    def streckr():
        n = ri(6, 23)
        thing = ch(["bilar", "cyklar", "fåglar", "bussar"])
        return mcq(fig(streck(n)) + "Eleverna räknade %s med streck. Hur många %s såg de?" % (thing, thing), str(n), [str(n + 1), str(n - 1), str(n // 5 + n % 5)],
                   "Varje knippe är 5. %d knippen = %d, plus %d streck: <b>%d</b>." % (n // 5, 5 * (n // 5), n % 5, n))

    def tabell():
        d = data(4, 3, 15)
        if not d:
            return None
        cat, dv = d
        rows = "".join("<tr><td>%s</td><td>%d</td></tr>" % (n, v) for n, v in dv)
        tab = "<table class='sn-table' style='width:auto'><thead><tr><th>%s</th><th>Antal elever</th></tr></thead><tbody>%s</tbody></table>" % (cat[0].capitalize(), rows)
        n, v = ch(dv)
        return mcq(tab + "Vilket diagram stämmer med tabellen för %s?" % n if False else tab + "Hur många elever valde %s?" % n, str(v),
                   [str(x) for _, x in dv if x != v], "Läs raden för %s: <b>%d</b>." % (n, v))

    sets = [("Läs av stapeldiagram", [(las, 20)]),
            ("Mest och minst", [(mest, 20)]),
            ("Jämför staplarna", [(skillnad, 20)]),
            ("Streckräkning och tabeller", [(streckr, 10), (tabell, 10)]),
            ("Totalt och blandat", [(totalt, 10), (las, 4), (skillnad, 6)])]
    return unit("tabeller-och-diagram", "S", 22, "Tabeller och diagram: streckräkning och stapeldiagram", "Tabeller och diagram",
                "Enkla tabeller och diagram och hur de kan användas för att sortera data och beskriva resultat från enkla undersökningar.",
                "Arbetsblad om tabeller och diagram för årskurs 3: streckräkning, tabeller, läs av stapeldiagram, mest och minst och jämför. 100 uppgifter med facit.",
                "Läs rubriken och axlarna", "Stapelns höjd visar antalet.", sets,
                ["I en undersökning samlar du in svar. Med streckräkning gör du ett streck för varje svar. Vart femte streck går tvärs över de fyra första.",
                 "I en tabell står svaren i rader. I ett stapeldiagram visar höjden på stapeln hur många som svarade.",
                 "Läs alltid rubriken och skalan på axeln först. Skillnaden mellan två staplar räknar du med subtraktion."],
                [("Hund 8, katt 5", ["Hur många fler valde hund?", "8 − 5"], "3"), ("Streckräkning: 3 knippen och 2 streck", ["3 × 5 = 15", "15 + 2"], "17")],
                [["Läser av stapelns bredd", "Det är höjden som visar antalet"], ["Räknar ett femknippe som 4", "Ett knippe är 5 streck"],
                 ["Adderar när frågan är hur många fler", "Fler betyder skillnaden: subtrahera"]],
                [("Varför använder man diagram?", "I ett diagram ser man snabbt vad som är mest och minst."),
                 ("Vad är streckräkning?", "Ett snabbt sätt att räkna medan man samlar in svar. Varje svar blir ett streck."),
                 ("Vad är skillnaden mellan tabell och diagram?", "En tabell visar talen. Ett diagram visar samma tal som en bild.")])


# ============================================================ 23. Slump och sannolikhet
def pase(counts):
    col = {"röd": "#e07a5f", "blå": "#6a9fd4", "gul": "#f2c94c", "grön": "#81b29a"}
    s = ["<path d='M20 30 Q10 120 40 140 L150 140 Q180 120 170 30 Z' fill='#f3ead7' stroke='%s' stroke-width='2'/>" % INK]
    i = 0
    for c, n in counts:
        for _ in range(n):
            s.append("<circle cx='%d' cy='%d' r='9' fill='%s' stroke='%s'/>" % (42 + (i % 6) * 21, 50 + (i // 6) * 20, col[c], INK))
            i += 1
    return wrap(190, 150, "".join(s), "en påse med kulor")


PLC = {"röd": "röda", "blå": "blå", "gul": "gula", "grön": "gröna"}


def u23():
    def sakert():
        opts = [("Du slår en vanlig tärning. Att du får ett tal mellan 1 och 6 är …", "säkert"),
                ("Du slår en vanlig tärning. Att du får 7 är …", "omöjligt"),
                ("Du slår en vanlig tärning. Att du får en sexa är …", "möjligt"),
                ("Du singlar slant. Att du får krona är …", "möjligt"),
                ("Du slår en vanlig tärning. Att du får ett tal som är mindre än 10 är …", "säkert"),
                ("Att solen går upp i morgon är …", "säkert"),
                ("Du drar en kula ur en påse med bara blå kulor. Att du får en blå kula är …", "säkert"),
                ("Du drar en kula ur en påse med bara blå kulor. Att du får en röd kula är …", "omöjligt"),
                ("Du drar ett kort ur en kortlek. Att du får ett hjärter är …", "möjligt"),
                ("I en påse finns 3 röda och 2 blå kulor. Att du drar en grön kula är …", "omöjligt"),
                ("I en påse finns 3 röda och 2 blå kulor. Att du drar en röd kula är …", "möjligt")]
        q, a = ch(opts)
        return mcq(q, a, [x for x in ("säkert", "möjligt", "omöjligt") if x != a] + ["det går inte att säga"],
                   "Svaret är <b>%s</b>." % a)

    def pasen():
        cs = R.sample(["röd", "blå", "gul", "grön"], 3)
        ns = R.sample(range(1, 9), 3)
        counts = list(zip(cs, ns))
        most = R.random() < 0.6
        a = (max if most else min)(counts, key=lambda t: t[1])[0]
        return mcq(pase(counts) + "Du drar en kula utan att titta. %s" % ("Vilken färg får du troligast?" if most else "Vilken färg är det minst troligt att du får?"), a,
                   [c for c, _ in counts if c != a] + ["alla är lika troliga"],
                   "Det finns flest %s kulor, så <b>%s</b> är troligast." % (PLC[a], a) if most else
                   "Det finns minst %s kulor, så <b>%s</b> är minst troligt." % (PLC[a], a))

    def tarning():
        k = ri(0, 3)
        if k == 0:
            n = ri(1, 4)
            big = R.random() < 0.5
            good = ", ".join(str(i) for i in (range(n + 1, 7) if big else range(1, n)))
            if not good:
                return None
            w = [", ".join(str(i) for i in range(n, 7)), ", ".join(str(i) for i in range(1, n + 1)), ", ".join(str(i) for i in range(n + 2, 7)), ", ".join(str(i) for i in range(n + 1, 8))]
            return mcq("Du slår en vanlig tärning. Vilka tal kan du få som är %s än %d?" % ("större" if big else "mindre", n), good, [x for x in w if x != good],
                       "Tärningen har talen 1–6. Talen %s än %d är <b>%s</b>." % ("större" if big else "mindre", n, good))
        if k == 1:
            return mcq("Du slår en tärning. Vilket är troligast: ett jämnt tal eller ett udda tal?", "lika troligt", ["jämnt tal", "udda tal", "det går inte att få jämnt tal"],
                       "Jämna: 2, 4, 6. Udda: 1, 3, 5. Tre av varje, alltså <b>lika troligt</b>.")
        if k == 2:
            a, b = ri(1, 6), ri(1, 6)
            return mcq("Du slår två tärningar och får %d och %d. Vad blir summan?" % (a, b), str(a + b), [str(a * b) if a * b != a + b else str(a + b + 1), str(a + b - 1), str(abs(a - b) + 1)],
                       "%d + %d = <b>%d</b>." % (a, b, a + b))
        s = ri(2, 12)
        ways = len([(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == s])
        return mcq("Du slår två tärningar. Kan summan bli %d?" % s if s <= 12 else "", "ja" if ways else "nej", ["nej" if ways else "ja", "bara med en tärning", "bara om du slår tre gånger"],
                   "Minsta summan är 1 + 1 = 2 och största är 6 + 6 = 12. %d är <b>%s</b>." % (s, "möjligt" if ways else "omöjligt"))

    def rattvist():
        k = ri(0, 2)
        if k == 0:
            r, b = ri(2, 6), ri(2, 6)
            fair = r == b
            return mcq("I en påse finns %d röda och %d blå kulor. Du vinner på röd och kompisen vinner på blå. Är spelet rättvist?" % (r, b),
                       "ja" if fair else "nej", ["ja" if not fair else "nej", "bara om man drar två gånger", "det beror på vem som börjar"],
                       "Spelet är rättvist bara om det finns lika många av varje. Här är det <b>%s</b>." % ("rättvist" if fair else "inte rättvist"))
        if k == 1:
            return mcq("Du och en kompis singlar slant. Du vinner på krona och kompisen på klave. Är spelet rättvist?", "ja", ["nej", "bara om man singlar två gånger", "det beror på vem som singlar"],
                       "Krona och klave är lika troliga. Spelet är <b>rättvist</b>.")
        n = ri(1, 5)
        return mcq("Du vinner om tärningen visar %s. Kompisen vinner om den visar något annat. Vem har störst chans?" % (", ".join(str(i) for i in range(1, n + 1)) if n > 1 else "1"),
                   "du" if n > 3 else ("kompisen" if n < 3 else "lika stor chans"), [x for x in ("du", "kompisen", "lika stor chans", "ingen kan vinna") if x != ("du" if n > 3 else ("kompisen" if n < 3 else "lika stor chans"))],
                   "Du vinner på %d tal och kompisen på %d tal." % (n, 6 - n))

    def forsok():
        n = ri(20, 60)
        r = ri(1, 4)
        tot = 4
        cnt = [ri(2, 10) for _ in range(3)]
        cs = ["röd", "blå", "gul"]
        best = cs[cnt.index(max(cnt))]
        if cnt.count(max(cnt)) > 1:
            return None
        rows = "".join("<tr><td>%s</td><td>%d</td></tr>" % (c, x) for c, x in zip(cs, cnt))
        tab = "<table class='sn-table' style='width:auto'><thead><tr><th>Färg</th><th>Antal gånger</th></tr></thead><tbody>%s</tbody></table>" % rows
        return mcq(tab + "Klassen drog en kula ur en påse %d gånger och lade tillbaka den varje gång. Vilken färg finns det troligen flest av i påsen?" % sum(cnt),
                   best, [c for c in cs if c != best] + ["det går inte att gissa"], "%s kom flest gånger, så det finns troligen flest %s kulor." % (cap(best), {"röd": "röda", "blå": "blå", "gul": "gula"}[best]))

    sets = [("Säkert, möjligt eller omöjligt", [(sakert, 10), (pasen, 10)]),
            ("Dra en kula", [(pasen, 20)]),
            ("Tärningar", [(tarning, 20)]),
            ("Är spelet rättvist?", [(rattvist, 20)]),
            ("Experiment", [(forsok, 20)])]
    return unit("slump-och-sannolikhet", "S", 23, "Slump och sannolikhet: säkert, möjligt och omöjligt", "Slump och sannolikhet",
                "Slumpmässiga händelser i experiment och spel. Säkert, möjligt och omöjligt, och vad som är mest troligt.",
                "Arbetsblad om slump och sannolikhet för årskurs 3: säkert, möjligt och omöjligt, dra kulor ur en påse, tärningar, rättvisa spel och experiment. 100 uppgifter med facit.",
                "Säkert, möjligt, omöjligt", "Det som det finns flest av är troligast.", sets,
                ["En händelse kan vara säker (den händer alltid), möjlig (den kan hända) eller omöjlig (den kan aldrig hända).",
                 "Finns det fler röda än blå kulor i en påse är det troligare att du drar en röd. Men du kan fortfarande få en blå.",
                 "Ett spel är rättvist när alla har lika stor chans att vinna. En tärning har sex tal som är lika troliga."],
                [("Påse: 6 röda, 2 blå", ["Fler röda än blå"], "Röd är troligast"), ("Tärning: få 7", ["Tärningen har bara 1–6"], "omöjligt")],
                [["Tror att man alltid får den färg det finns flest av", "Den är troligast, men inte säker"],
                 ["Tror att 6 är svårare att få än 3 på en tärning", "Alla tal på tärningen är lika troliga"],
                 ["Tror att ett spel är rättvist för att båda får spela", "Rättvist betyder lika stor chans att vinna"]],
                [("Vad betyder slump?", "Att man inte kan veta i förväg vad som händer, till exempel vilket tal tärningen visar."),
                 ("Vad betyder troligast?", "Det som har störst chans att hända."),
                 ("Kan man vinna på ett orättvist spel?", "Ja, men det är mindre troligt för den som har sämre chans.")])


UNITS = [u13, u14, u15, u16, u17, u18, u19, u20, u21, u22, u23]
