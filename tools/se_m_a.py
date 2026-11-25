# -*- coding: utf-8 -*-
"""Sverige åk 4–6: tal och räkning（talet lv = 4, 5, 6）"""
from fractions import Fraction as F
import se_m as S
from se_m import num, kr, M, fr, fq, d, ri, ch, sh, cap, unit, tab, PLATS, DEC, MAXN
from se_common import uppstallning, tallinje, positionstabell, ord_, Hon, hon


def K():
    return S.K


# ============================================================ tal och positionssystemet
def tal(lv):
    mx = MAXN[lv]
    lo = 1000 if lv == 4 else 10000

    def n_():
        return ri(lo, mx)

    def varde():
        n = n_()
        s = str(n)
        i = ri(0, len(s) - 1)
        dg = int(s[i])
        if dg == 0 or s.count(s[i]) > 1:
            return None
        p = len(s) - 1 - i
        v = dg * 10 ** p
        return M("Vilket värde har siffran <b>%d</b> i talet <b>%s</b>?" % (dg, num(n)), num(v),
                 [num(dg * 10 ** k) for k in sh([x for x in range(max(0, p - 2), p + 3) if x != p])],
                 "Siffran %d står på %splatsen och är värd <b>%s</b>." % (dg, PLATS[p], num(v)))

    def plats():
        n = n_()
        s = str(n)
        i = ri(0, len(s) - 1)
        dg = int(s[i])
        if s.count(s[i]) > 1:
            return None
        p = len(s) - 1 - i
        return M("På vilken plats står siffran <b>%d</b> i talet <b>%s</b>?" % (dg, num(n)), PLATS[p] + "splatsen",
                 [PLATS[k] + "splatsen" for k in sh([x for x in range(max(0, p - 2), min(6, p + 2) + 1) if x != p])],
                 "Räkna från höger: ental, tiotal, hundratal, tusental … Siffran %d står på <b>%splatsen</b>." % (dg, PLATS[p]))

    def utvecklad():
        n = n_()
        s = str(n)
        parts = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
        if len(parts) < 3:
            return None
        good = " + ".join(num(x) for x in parts)
        w1 = " + ".join(num(x // 10 if x >= 10 else x) for x in parts)
        w2 = " + ".join(num(x * 10) for x in parts)
        w3 = " + ".join(c for c in s if c != "0")
        if R0():
            return M("Hur skrivs <b>%s</b> i utvecklad form?" % num(n), good, [w1, w2, w3],
                     "%s = <b>%s</b>." % (num(n), good))
        return M("%s = ?" % good, num(n), [num(int(s[::-1])), num(n * 10), num(n // 10), num(n + 10 ** (len(s) - 2))],
                 "Lägg ihop värdena plats för plats: <b>%s</b>." % num(n))

    def jamfor():
        a = n_()
        k = ri(1, len(str(a)) - 1)
        xs = {a}
        while len(xs) < 4:
            b = a + ch([-1, 1]) * ri(1, 9) * 10 ** ri(0, k)
            if lo <= b <= mx:
                xs.add(b)
        xs = sh(sorted(xs))
        big = R0()
        g = max(xs) if big else min(xs)
        return M("Vilket tal är <b>%s</b>? %s" % ("störst" if big else "minst", ", ".join(num(x) for x in xs)), num(g),
                 [num(x) for x in xs if x != g], "Jämför siffrorna från vänster. Den första siffran som skiljer avgör: <b>%s</b>." % num(g))

    def mer():
        n = n_()
        st = 10 ** ri(1, len(str(n)) - 1)
        up = R0()
        v = n + st if up else n - st
        if not lo <= v <= mx:
            return None
        return M("Vilket tal är %s %s än %s?" % (num(st), "mer" if up else "mindre", num(n)), num(v),
                 [num(x) for x in (n + (st // 10 if st > 10 else st * 10) * (1 if up else -1), n + st * 10 * (1 if up else -1), n - st if up else n + st, v + 1) if x > 0],
                 "Siffran på %splatsen ändras med 1: <b>%s</b>." % (PLATS[len(str(st)) - 1], num(v)))

    def ord_tal():
        if lv == 6 and R0():
            a, b = ri(1, 9), ri(1, 9)
            v = a * 1000000 + b * 100000
            return M("Hur skrivs %d,%d miljoner med siffror?" % (a, b), num(v), [num(a * 1000000 + b * 10000), num(a * 100000 + b * 10000), num(a * 1000000 + b * 1000)],
                     "1 miljon = 1 000 000. %d,%d miljoner = %d miljoner och %d hundratusen = <b>%s</b>." % (a, b, a, b, num(v)))
        n = ri(lo, min(mx, 999999))
        s = str(n)
        if "0" not in s[1:] and R0():
            return None
        w = [n + 9 * 10 ** (len(s) - 2) if s[1] == "0" else n * 10, int(s.replace("0", "")) if "0" in s else n + 10, n // 10 * 10 + (n % 10 + 1) % 10]
        return M("Skriv med siffror: <i>%s</i>" % ord_(n), num(n), [num(x) for x in w + [n + 1000]],
                 "%s = <b>%s</b>." % (cap(ord_(n)), num(n)))

    def linje():
        st = ch([100, 1000] if lv == 4 else [1000, 10000] if lv == 5 else [10000, 100000])
        a = ri(1, 8) * st * 10
        if a + 10 * st > mx:
            return None
        k = ri(1, 9)
        v = a + k * st
        pic = tallinje(a, a + 10 * st, st, [(v, "A")], labels=[a, a + 10 * st], width=400)
        return M(pic + "Vilket tal visar pilen A?", num(v), [num(a + k * st // 10), num(v + st), num(v - st), num(a + k)],
                 "Varje streck är %s. Pilen står %d streck efter %s: <b>%s</b>." % (num(st), k, num(a), num(v)))

    def decimal_plats():
        i, f = ri(1, 99), ri(1, 999)
        s = str(f).rjust(3, "0").rstrip("0")
        if len(s) < 2:
            return None
        x = F(i) + F(int(s), 10 ** len(s))
        k = ri(0, len(s) - 1)
        dg = int(s[k])
        if dg == 0 or s.count(s[k]) > 1 or str(i).count(s[k]):
            return None
        v = F(dg, 10 ** (k + 1))
        return M("Vilket värde har siffran <b>%d</b> i talet <b>%s</b>?" % (dg, d(x)), d(v),
                 [d(F(dg, 10 ** j)) for j in range(1, 4) if j != k + 1] + [str(dg), num(dg * 10)],
                 "Siffran %d står på %splatsen: <b>%s</b>." % (dg, {0: "tiondel", 1: "hundradel", 2: "tusendel"}[k], d(v)))

    if lv == 6:
        sets = [("Siffrans värde", [(varde, 14), (plats, 6)]), ("Decimaltalens positioner", [(decimal_plats, 20)]),
                ("Utvecklad form och miljoner", [(utvecklad, 12), (ord_tal, 8)]), ("Jämföra och ordna", [(jamfor, 12), (mer, 8)]),
                ("Tallinjen", [(linje, 20)])]
    else:
        sets = [("Siffrans värde", [(varde, 20)]), ("Platser i talet", [(plats, 20)]),
                ("Utvecklad form och talord", [(utvecklad, 12), (ord_tal, 8)]), ("Jämföra och ordna", [(jamfor, 12), (mer, 8)]),
                ("Tallinjen", [(linje, 20)])]
    top = {4: "100 000", 5: "1 miljon", 6: "10 miljoner"}[lv]
    return unit("tal-och-positionssystemet", "T", "Tal och positionssystemet: tal upp till %s" % top, "Tal och positionssystemet",
                "Positionssystemet för naturliga tal%s. Hur talen kan delas upp, jämföras och ordnas." % (" och tal i decimalform" if lv == 6 else ""),
                "Arbetsblad om positionssystemet för årskurs %d: siffrans värde, platser i talet, utvecklad form, jämföra och ordna tal och tallinjen, med tal upp till %s. 100 uppgifter med facit." % (lv, top),
                "Platsen bestämmer värdet", "Varje plats är 10 gånger så mycket som platsen till höger.", sets,
                ["I positionssystemet är varje plats värd 10 gånger mer än platsen till höger: ental, tiotal, hundratal, tusental, tiotusental, hundratusental och miljontal.",
                 "Siffrans värde beror på var den står. I talet 47 382 är siffran 7 värd 7 000.",
                 "Jämför två tal genom att börja från vänster. Den första siffran som skiljer sig avgör vilket tal som är störst."
                 + (" Till höger om decimalkommat kommer tiondelar, hundradelar och tusendelar." if lv == 6 else "")],
                [("Vilket värde har siffran 6 i 36 405?", ["6 står på tusentalsplatsen"], "6 000"), ("1 000 mer än 49 520", ["Tusentalssiffran ökar med 1: 9 + 1 = 10", "Växla till tiotusental"], "50 520")],
                [["Siffran 6 i 36 405 är värd 6", "Den står på tusentalsplatsen och är värd 6 000"],
                 ["50 102 är större än 50 120 för att den slutar på 2", "Jämför från vänster: tiotalen 0 &lt; 2"],
                 ["Glömmer nollan: fyrtiotusenfem skrivs 4 005", "40 005"]],
                [("Varför skriver man mellanrum i stora tal?", "Mellanrummet delar talet i grupper om tre siffror, så det blir lättare att läsa: 1 250 000."),
                 ("Vad är en miljon?", "Tusen tusen, alltså 1 000 000."),
                 ("Vilken plats kommer efter hundratusental?", "Miljontal. 1 000 000 är ett miljontal.")])


def R0():
    return S.R.random() < 0.5


# ============================================================ avrundning och överslag
def avr(n, p):
    return int(F(n, p) + F(1, 2)) * p if n >= 0 else -avr(-n, p)


def avrundning(lv):
    mx = MAXN[lv]

    def avrunda():
        p = ch([10, 100, 1000] + ([10000] if lv >= 5 else []) + ([100000] if lv == 6 else []))
        n = ri(p + 1, min(mx, p * 1000))
        if n % p == 0 or avr(n, p) == avr(n, p * 10) and False:
            return None
        r = avr(n, p)
        lo_, hi_ = n // p * p, n // p * p + p
        name = {10: "tiotal", 100: "hundratal", 1000: "tusental", 10000: "tiotusental", 100000: "hundratusental"}[p]
        nxt = str(n)[-len(str(p)) + 1] if p > 1 else "0"
        return M("Avrunda <b>%s</b> till närmaste %s." % (num(n), name), num(r),
                 [num(lo_ if r == hi_ else hi_), num(avr(n, p // 10)) if p > 10 else num(n // 10 * 10 + 10), num(avr(n, p * 10))],
                 "Titta på siffran till höger om %splatsen: %s. %s Svar: <b>%s</b>." % (name, nxt, "0–4 avrundas nedåt." if int(nxt) < 5 else "5–9 avrundas uppåt.", num(r)))

    def dec_avr():
        k = ch([1, 2]) if lv == 6 else 1
        n = ri(101, 9999) if k == 1 else ri(1001, 99999)
        x = F(n, 10 ** k)
        r = F(int(x * 10 ** (k - 1) + F(1, 2)), 10 ** (k - 1))
        tgt = "heltal" if k == 1 else "tiondel"
        if x == r:
            return None
        w = [r + F(1, 10 ** (k - 1)), r - F(1, 10 ** (k - 1)), F(int(x * 10 ** (k - 1)), 10 ** (k - 1)) if int(x * 10 ** (k - 1)) != r * 10 ** (k - 1) else r + F(2, 10 ** (k - 1)), x]
        return M("Avrunda <b>%s</b> till närmaste %s." % (d(x), tgt), d(r), [d(v) for v in w],
                 "Titta på %s. Svar: <b>%s</b>." % ("tiondelssiffran" if k == 1 else "hundradelssiffran", d(r)))

    def overslag():
        p = 100 if lv == 4 else ch([100, 1000])
        a, b = ri(p * 2, p * 60), ri(p * 2, p * 40)
        op = ch("+-×") if lv >= 5 else ch("+-")
        if op == "×":
            a, b = ri(21, 98), ri(11, 89)
            ra, rb = avr(a, 10), avr(b, 10)
            est = ra * rb
            return M("Gör ett överslag: ungefär hur mycket är %d × %d?" % (a, b), "ungefär " + num(est),
                     ["ungefär " + num(x) for x in (est * 10, est // 10, ra * rb + ra * 10, ra + rb)],
                     "Avrunda till tiotal: %d × %d = <b>%s</b>." % (ra, rb, num(est)))
        if op == "-" and a < b:
            a, b = b, a
        ra, rb = avr(a, p), avr(b, p)
        est = ra + rb if op == "+" else ra - rb
        if est <= 0:
            return None
        sym = "+" if op == "+" else "−"
        return M("Gör ett överslag: ungefär hur mycket är %s %s %s?" % (num(a), sym, num(b)), "ungefär " + num(est),
                 ["ungefär " + num(x) for x in (est + p, est - p, est + 2 * p, est * 10) if x > 0],
                 "Avrunda: %s %s %s = <b>%s</b>." % (num(ra), sym, num(rb), num(est)))

    def rimligt():
        a, b = ri(1200, 8900), ri(1100, 5900)
        if lv == 6 and R0():
            a, b = ri(12, 89), ri(11, 49)
            s = a * b
            w = [s * 10, s // 10, s + 1000, a * b // 100 + a]
            return M("%d × %d. Vilket svar är rimligt? Gör ett överslag först." % (a, b), num(s), [num(x) for x in w if x > 0],
                     "Överslag: %d × %d = %s. Bara <b>%s</b> ligger nära." % (avr(a, 10), avr(b, 10), num(avr(a, 10) * avr(b, 10)), num(s)))
        s = a + b
        w = [s + 1000, s - 1000, a + b // 10, s * 10]
        return M("%s + %s. Vilket svar är rimligt? Gör ett överslag först." % (num(a), num(b)), num(s), [num(x) for x in w if x > 0],
                 "Överslag: %s + %s = %s. Bara <b>%s</b> ligger nära." % (num(avr(a, 1000)), num(avr(b, 1000)), num(avr(a, 1000) + avr(b, 1000)), num(s)))

    def handla():
        n = K().name()
        it = sh([("en cykel", 1990, 4990), ("en surfplatta", 1490, 3990), ("en tältsäng", 390, 990), ("ett par skridskor", 490, 1290),
                 ("en jacka", 590, 1490), ("ett par hörlurar", 290, 990), ("en fotboll", 149, 399), ("ett tält", 990, 2990)])[:3]
        p = [ri(a, b) // 10 * 10 - 1 for _, a, b in it]
        tot = sum(p)
        est = sum(avr(x, 100) for x in p)
        have = avr(tot, 1000) + ch([-1000, 1000])
        if have <= 0:
            return None
        ok = tot <= have
        return M("%s har %s och vill köpa %s. Räcker pengarna? Gör ett överslag." % (
            n, kr(have), ", ".join("%s för %s" % (w, kr(x)) for (w, _, _), x in zip(it, p))),
            "Ja" if ok else "Nej", ["Nej" if ok else "Ja", "Det går inte att veta utan miniräknare", "Bara om allt kostar lika mycket"],
            "Överslag: ungefär %s. Det är %s än %s, så svaret är <b>%s</b>." % (kr(est), "mindre" if ok else "mer", kr(have), "ja" if ok else "nej"))

    sets = [("Avrunda heltal", [(avrunda, 20)]),
            ("Avrunda decimaltal" if lv >= 5 else "Avrunda stora tal", [(dec_avr, 20)] if lv >= 5 else [(avrunda, 20)]),
            ("Överslagsräkning", [(overslag, 20)]),
            ("Är svaret rimligt?", [(rimligt, 20)]),
            ("Överslag när du handlar", [(handla, 20)])]
    return unit("avrundning-och-overslag", "T", "Avrundning och överslagsräkning", "Avrundning och överslag",
                "Metoder för beräkningar vid överslagsräkning. Rimlighetsbedömning vid uppskattningar och beräkningar.",
                "Arbetsblad om avrundning och överslag för årskurs %d: avrunda till tiotal, hundratal och tusental%s, gör överslag, bedöm om svaret är rimligt och räkna ungefär när du handlar. 100 uppgifter med facit." % (lv, ", avrunda decimaltal" if lv >= 5 else ""),
                "Titta på siffran till höger", "0–4 avrundas nedåt, 5–9 avrundas uppåt.", sets,
                ["När du avrundar tittar du på siffran till höger om den plats du avrundar till. Är den 0–4 avrundar du nedåt, är den 5–9 avrundar du uppåt.",
                 "Ett överslag är en snabb räkning med avrundade tal. 4 870 + 2 190 ≈ 5 000 + 2 000 = 7 000.",
                 "Jämför ditt exakta svar med överslaget. Ligger de långt ifrån varandra har du troligen räknat fel."],
                [("Avrunda 36 482 till närmaste tusental", ["Hundratalssiffran är 4", "4 avrundas nedåt"], "36 000"),
                 ("Ungefär 48 × 21", ["48 ≈ 50 och 21 ≈ 20", "50 × 20"], "ungefär 1 000")],
                [["36 482 avrundat till tusental blir 37 000", "Hundratalssiffran 4 avrundas nedåt: 36 000"],
                 ["Avrundar i flera steg: 3 449 → 3 450 → 3 500", "Titta bara på siffran till höger: 3 400"],
                 ["Tror att ett överslag är exakt", "Ett överslag ger ett ungefärligt svar, ≈"]],
                [("Vad betyder ≈?", "Ungefär lika med. 4 870 ≈ 5 000."),
                 ("Till vilken plats ska jag avrunda vid överslag?", "Till en plats som ger enkla tal att räkna med, ofta den första siffran."),
                 ("Varför ska man göra överslag?", "För att snabbt se om svaret på miniräknaren eller i uppställningen är rimligt.")])


# ============================================================ addition och subtraktion
def nocarry(a, b):
    r, p = 0, 1
    while a or b:
        r += ((a % 10 + b % 10) % 10) * p
        a //= 10
        b //= 10
        p *= 10
    return r


def smallbig(a, b):
    r, p = 0, 1
    while a or b:
        r += abs(a % 10 - b % 10) * p
        a //= 10
        b //= 10
        p *= 10
    return r


def addsub(lv):
    hi = {4: 9999, 5: 99999, 6: 99999}[lv]

    def add():
        a, b = ri(hi // 10, hi * 6 // 10), ri(hi // 20, hi * 3 // 10)
        s = a + b
        return M("Räkna: %s + %s = ?" % (num(a), num(b)), num(s), [num(x) for x in (nocarry(a, b), s + 10, s - 100, s + 1000) if x != s],
                 "Ställ upp med ental under ental och glöm inte minnessiffrorna. Svar: <b>%s</b>." % num(s))

    def sub():
        a = ri(hi // 5, hi)
        b = ri(hi // 20, a - hi // 20)
        dd = a - b
        return M("Räkna: %s − %s = ?" % (num(a), num(b)), num(dd), [num(x) for x in (smallbig(a, b), dd + 10, dd - 100, dd + 1000) if x != dd and x > 0],
                 "Växla när siffran överst är för liten. Kontroll: %s + %s = %s. Svar: <b>%s</b>." % (num(dd), num(b), num(a), num(dd)))

    def bild():
        a = ri(hi // 5, hi)
        b = ri(hi // 20, a - hi // 20)
        if R0():
            s = a + b
            return M(uppstallning([str(a), str(b)], "+") + "Vad blir summan?", num(s), [num(nocarry(a, b)), num(s + 100), num(s - 10)],
                     "Addera kolumn för kolumn från höger, med minnessiffror. Svar: <b>%s</b>." % num(s))
        dd = a - b
        return M(uppstallning([str(a), str(b)], "−") + "Vad blir skillnaden?", num(dd), [num(smallbig(a, b)), num(dd + 100), num(dd + 10)],
                 "Subtrahera kolumn för kolumn från höger och växla när det behövs. Svar: <b>%s</b>." % num(dd))

    def noll():
        z = ch([1000, 10000, 5000, 20000, 3000]) if lv >= 5 else ch([1000, 2000, 5000, 3000])
        b = ri(z // 10, z - 11)
        dd = z - b
        return M("%s − %s = ?" % (num(z), num(b)), num(dd), [num(x) for x in (smallbig(z, b), dd + 10, dd - 10, dd + 100) if x > 0 and x != dd],
                 "Räkna uppåt från %s till %s, eller växla över nollorna. Svar: <b>%s</b>." % (num(b), num(z), num(dd)))

    def decimal():
        k = ch([1, 2]) if lv == 6 else 1
        a, b = F(ri(105, 9999), 10 ** k), F(ri(105, 4999), 10 ** k)
        if R0():
            s = a + b
            w = [s + F(1, 10 ** k), s + 1, F(nocarry(int(a * 10 ** k), int(b * 10 ** k)), 10 ** k)]
            return M("%s + %s = ?" % (d(a), d(b)), d(s), [d(x) for x in w],
                     "Ställ upp med komma under komma. Svar: <b>%s</b>." % d(s))
        if a < b:
            a, b = b, a
        dd = a - b
        w = [dd + F(1, 10 ** k), dd + 1, F(smallbig(int(a * 10 ** k), int(b * 10 ** k)), 10 ** k)]
        return M("%s − %s = ?" % (d(a), d(b)), d(dd), [d(x) for x in w if x > 0],
                 "Ställ upp med komma under komma och växla vid behov. Svar: <b>%s</b>." % d(dd))

    def text_():
        n, g = K().next()
        k = ri(0, 3)
        if k == 0:
            a, b = ri(1200, 4800), ri(800, 3900)
            return M("En familj kör %s km på sommarlovet och %s km på höstlovet. Hur långt kör de totalt?" % (num(a), num(b)), num(a + b) + " km",
                     [num(x) + " km" for x in (nocarry(a, b), a - b if a > b else b - a, a + b + 100)], "%s + %s = <b>%s km</b>." % (num(a), num(b), num(a + b)))
        if k == 1:
            a = ri(5000, hi)
            b = ri(1000, a - 500)
            return M("En skola samlar in %s kr till en skolresa. Resan kostar %s kr. Hur mycket fattas?" % (num(b), num(a)), kr(a - b),
                     [kr(x) for x in (smallbig(a, b), a + b, a - b + 100) if x != a - b], "%s − %s = <b>%s</b>." % (num(a), num(b), kr(a - b)))
        if k == 2:
            y1 = ri(1900, 1990)
            y2 = ri(2000, 2025)
            return M("Ett hus byggdes år %d. Hur gammalt var huset år %d?" % (y1, y2), "%d år" % (y2 - y1), ["%d år" % x for x in (y2 - y1 + 10, y2 - y1 - 10, y2 - y1 + 100)],
                     "%d − %d = <b>%d år</b>." % (y2, y1, y2 - y1))
        a, b, c = ri(1500, 4000), ri(800, 2500), ri(300, 1500)
        return M("På en konsert sitter %s personer på parkett, %s på läktaren och %s på balkongen. Hur många är det sammanlagt?" % (num(a), num(b), num(c)),
                 num(a + b + c), [num(x) for x in (a + b, a + b + c + 1000, a + b + c - 100)], "%s + %s + %s = <b>%s</b>." % (num(a), num(b), num(c), num(a + b + c)))

    sets = [("Addition", [(add, 20)]), ("Subtraktion", [(sub, 20)]), ("Uppställning", [(bild, 12), (noll, 8)]),
            ("Decimaltal" if lv >= 5 else "Växla över nollor", [(decimal, 20)] if lv >= 5 else [(noll, 12), (bild, 8)]),
            ("Textuppgifter", [(text_, 20)])]
    return unit("addition-och-subtraktion", "T", "Addition och subtraktion med uppställning", "Addition och subtraktion",
                "Metoder för beräkningar med naturliga tal%s vid huvudräkning och skriftliga metoder. Rimlighetsbedömning." % (" och tal i decimalform" if lv >= 5 else ""),
                "Arbetsblad om addition och subtraktion för årskurs %d: uppställning med minnessiffror och växling, subtraktion över nollor%s och textuppgifter. 100 uppgifter med facit." % (lv, ", decimaltal" if lv >= 5 else ""),
                "Samma plats under varandra", "Ental under ental%s." % (", komma under komma" if lv >= 5 else ""), sets,
                ["Ställ upp talen så att samma plats står under varandra: ental under ental, tiotal under tiotal och så vidare." + (" Med decimaltal står komma under komma." if lv >= 5 else ""),
                 "Vid addition blir det en minnessiffra när summan i en kolumn är 10 eller mer. Vid subtraktion växlar du från platsen till vänster när siffran överst är för liten.",
                 "Kontrollera subtraktion med addition och gör ett överslag för att se om svaret är rimligt."],
                [("4 586 + 2 739", ["6 + 9 = 15, skriv 5, minnessiffra 1", "8 + 3 + 1 = 12", "5 + 7 + 1 = 13", "4 + 2 + 1 = 7"], "7 325"),
                 ("5 000 − 1 368", ["Växla: 5 000 = 4 tusental, 9 hundratal, 9 tiotal, 10 ental", "10 − 8 = 2, 9 − 6 = 3, 9 − 3 = 6, 4 − 1 = 3"], "3 632")],
                [["5 000 − 1 368 = 4 368 (tar minsta från största)", "Växla över nollorna: 3 632"], ["Glömmer minnessiffran", "Skriv den ovanför nästa kolumn"],
                 ["Ställer 3,5 + 12,25 med 5 under 5", "Komma under komma: 3,50 + 12,25 = 15,75"]],
                [("Hur kontrollerar jag en subtraktion?", "Addera svaret och det du tog bort. Då ska du få talet du började med."),
                 ("Måste jag skriva nollor i decimaltal?", "Det hjälper: 3,5 = 3,50. Då står alla siffror på rätt plats."),
                 ("Vad gör jag när det står nollor i talet överst?", "Växla från närmaste plats som inte är noll, ett steg i taget.")])


# ============================================================ multiplikation
def mult(lv):
    def tabell():
        a, b = ri(3, 9), ri(3, 12)
        p = a * b
        return M("%d × %d = ?" % (a, b), str(p), [str(p + a), str(p - b), str(p + 1), str(a + b)], "%d × %d = <b>%d</b>." % (a, b, p))

    def tio():
        n = ri(3, 999) if lv >= 5 else ri(3, 99)
        t = ch([10, 100, 1000] if lv >= 5 else [10, 100])
        if lv == 6 and R0():
            x = F(ri(11, 999), ch([10, 100]))
            return M("%s × %s = ?" % (d(x), num(t)), d(x * t), [d(x * t * 10), d(x * t / 10), d(x + t)],
                     "Vid × %s flyttas siffrorna %d steg åt vänster: <b>%s</b>." % (num(t), len(str(t)) - 1, d(x * t)))
        return M("%s × %s = ?" % (num(n), num(t)), num(n * t), [num(n * t * 10), num(n * t // 10) if n * t // 10 != n else num(n * t * 100), num(n + t)],
                 "Vid × %s flyttas siffrorna %d steg åt vänster och nollor fyller på: <b>%s</b>." % (num(t), len(str(t)) - 1, num(n * t)))

    def en_siffra():
        a, b = ri(23, 999 if lv == 4 else 9999), ri(3, 9)
        p = a * b
        w = [nocarry_mul(a, b), p + b, p - 10 * b, p + 100]
        return M("%s × %d = ?" % (num(a), b), num(p), [num(x) for x in w if x != p and x > 0],
                 "Multiplicera varje siffra med %d och lägg till minnessiffrorna. Svar: <b>%s</b>." % (b, num(p)))

    def tva_siffror():
        a, b = ri(12, 99 if lv == 5 else 999), ri(12, 99)
        p = a * b
        w = [a * (b // 10) + a * (b % 10), p + a, p - 10 * a, a * (b // 10) * 10 + b % 10]
        return M("%s × %d = ?" % (num(a), b), num(p), [num(x) for x in w if x != p],
                 "%s × %d = %s och %s × %d = %s. %s + %s = <b>%s</b>." % (num(a), b // 10 * 10, num(a * (b // 10) * 10), num(a), b % 10, num(a * (b % 10)),
                                                                         num(a * (b // 10) * 10), num(a * (b % 10)), num(p)))

    def dec_mul():
        x = F(ri(11, 99), 10) if R0() else F(ri(101, 999), 100)
        b = ri(2, 9)
        p = x * b
        return M("%s × %d = ?" % (d(x), b), d(p), [d(p * 10), d(p / 10), d(p + F(1, 10)), d(x + b)],
                 "Räkna utan komma, sedan lika många decimaler som i %s: <b>%s</b>." % (d(x), d(p)))

    def text_():
        n = K().name()
        k = ri(0, 3)
        if k == 0:
            a, b = ri(12, 48), ri(15, 35)
            return M("En aula har %d rader med %d stolar i varje. Hur många stolar finns det?" % (a, b), num(a * b), [num(x) for x in (a + b, a * b + a, a * b - b, a * (b - 1))],
                     "%d × %d = <b>%s</b>." % (a, b, num(a * b)))
        if k == 1:
            p, m = ri(15, 99), ri(3, 9) if lv == 4 else ri(12, 30)
            return M("En biljett till simhallen kostar %s. %s köper %d biljetter till klassen. Vad kostar de?" % (kr(p), n, m), kr(p * m),
                     [kr(x) for x in (p + m, p * m + p, p * m - m, p * (m + 1))], "%d × %d = <b>%s</b>." % (m, p, kr(p * m)))
        if k == 2:
            w = ri(3, 9) if lv == 4 else ri(12, 52)
            return M("En vecka har 7 dagar. Hur många dagar är %d veckor?" % w, str(7 * w), [str(7 * w + 7), str(w + 7), str(7 * w - 1)], "%d × 7 = <b>%d</b>." % (w, 7 * w))
        if lv == 6:
            x = F(ri(15, 89), 10)
            m = ri(3, 8)
            return M("Ett paket smör kostar %s kr. Vad kostar %d paket?" % (d(x, 2), m), d(x * m, 2) + " kr", [d(v, 2) + " kr" for v in (x * m * 10 / 10 + 1, x + m, x * (m - 1))],
                     "%d × %s = <b>%s kr</b>." % (m, d(x, 2), d(x * m, 2)))
        a = ri(105, 450)
        return M("En buss kör %d km varje dag. Hur långt kör den på 6 dagar?" % a, num(6 * a) + " km", [num(x) + " km" for x in (a + 6, 6 * a - 100, 6 * a + 60)],
                 "6 × %d = <b>%s km</b>." % (a, num(6 * a)))

    if lv == 4:
        sets = [("Tabellerna", [(tabell, 20)]), ("Gånger 10 och 100", [(tio, 20)]), ("Multiplikation med ensiffrigt tal", [(en_siffra, 20)]),
                ("Blandat", [(en_siffra, 10), (tio, 5), (tabell, 5)]), ("Textuppgifter", [(text_, 20)])]
    elif lv == 5:
        sets = [("Gånger 10, 100 och 1 000", [(tio, 20)]), ("Multiplikation med ensiffrigt tal", [(en_siffra, 20)]), ("Tvåsiffriga faktorer", [(tva_siffror, 20)]),
                ("Decimaltal gånger heltal", [(dec_mul, 20)]), ("Textuppgifter", [(text_, 20)])]
    else:
        sets = [("Gånger 10, 100 och 1 000", [(tio, 20)]), ("Större multiplikationer", [(tva_siffror, 20)]), ("Decimaltal gånger heltal", [(dec_mul, 20)]),
                ("Blandat", [(en_siffra, 10), (tva_siffror, 10)]), ("Textuppgifter", [(text_, 20)])]
    return unit("multiplikation", "T", "Multiplikation: uppställning och gånger 10, 100 och 1 000", "Multiplikation",
                "Metoder för beräkningar med naturliga tal%s vid huvudräkning och skriftliga metoder. De fyra räknesättens egenskaper och samband." % (" och enkla tal i decimalform" if lv >= 5 else ""),
                "Arbetsblad om multiplikation för årskurs %d: tabellerna, gånger 10, 100 och 1 000, uppställning%s och textuppgifter. 100 uppgifter med facit." % (lv, ", tvåsiffriga faktorer och decimaltal" if lv >= 5 else " med ensiffrigt tal"),
                "Dela upp och lägg ihop", "34 × 6 = 30 × 6 + 4 × 6", sets,
                ["Vid gånger 10 flyttas alla siffror ett steg åt vänster: 36 × 10 = 360. Vid gånger 100 två steg och vid gånger 1 000 tre steg.",
                 "Vid uppställning multiplicerar du varje siffra från höger och lägger till minnessiffran. 347 × 6: 7 × 6 = 42, skriv 2 och minns 4.",
                 "Med två siffror delar du upp: 47 × 23 = 47 × 20 + 47 × 3 = 940 + 141 = 1 081." + (" Med decimaltal räknar du utan komma och sätter sedan in lika många decimaler: 2,4 × 3 = 7,2." if lv >= 5 else "")],
                [("347 × 6", ["7 × 6 = 42, skriv 2, minns 4", "4 × 6 + 4 = 28, skriv 8, minns 2", "3 × 6 + 2 = 20"], "2 082"),
                 ("47 × 23", ["47 × 20 = 940", "47 × 3 = 141", "940 + 141"], "1 081")],
                [["347 × 6 = 1 862 (glömmer minnessiffrorna)", "Lägg till minnessiffran varje gång: 2 082"], ["47 × 23 = 47 × 2 + 47 × 3", "Tvåan är 2 tiotal: 47 × 20"],
                 ["2,4 × 3 = 72", "En decimal i 2,4 ger en decimal i svaret: 7,2"]],
                [("Spelar ordningen någon roll?", "Nej. 6 × 347 = 347 × 6. Välj den ordning som är lättast."),
                 ("Hur kontrollerar jag svaret?", "Gör ett överslag: 347 × 6 ≈ 350 × 6 = 2 100."),
                 ("Varför blir det en nolla vid gånger 10?", "Varje siffra blir tio gånger så mycket värd och flyttar ett steg åt vänster. Entalsplatsen blir tom, och där skriver vi 0.")])


def nocarry_mul(a, b):
    r, p = 0, 1
    while a:
        r += ((a % 10) * b % 10) * p
        a //= 10
        p *= 10
    return r


# ============================================================ division
def div(lv):
    def tabell():
        a, b = ri(3, 9), ri(3, 12)
        return M("%d : %d = ?" % (a * b, a), str(b), [str(b + 1), str(b - 1), str(a * b - a), str(a)], "%d × %d = %d, så %d : %d = <b>%d</b>." % (a, b, a * b, a * b, a, b))

    def kort():
        b = ri(3, 9)
        q = ri(12, 999 if lv == 4 else 9999)
        a = b * q
        w = [q + 1, q - 1, q * 10, int(str(q)[::-1]) if str(q)[::-1] != str(q) else q + 10]
        return M("Räkna med kort division: %s : %d = ?" % (num(a), b), num(q), [num(x) for x in w if x > 0 and x != q],
                 "Dela siffra för siffra från vänster och för resten vidare. Kontroll: %d × %s = %s. Svar: <b>%s</b>." % (b, num(q), num(a), num(q)))

    def rest():
        b = ri(3, 9)
        q = ri(11, 199)
        r = ri(1, b - 1)
        a = b * q + r
        return M("%s : %d = ?" % (num(a), b), "%s rest %d" % (num(q), r),
                 ["%s rest %d" % (num(q + 1), r), "%s rest %d" % (num(q), r + b) if r + b < 10 else "%s rest %d" % (num(q - 1), r + b), "%s" % num(q), "%s rest %d" % (num(q), b - r) if b - r != r else "%s rest %d" % (num(q), r + 1)],
                 "%d × %s = %s och %d blir över. Svar: <b>%s rest %d</b>." % (b, num(q), num(b * q), r, num(q), r))

    def tio():
        t = ch([10, 100, 1000] if lv >= 5 else [10, 100])
        if lv >= 5 and R0():
            n = ri(11, 9999)
            x = F(n, t)
            if x.denominator == 1:
                return None
            return M("%s : %s = ?" % (num(n), num(t)), d(x), [d(x * 10), d(x / 10), num(n - t) if n > t else d(x * 100)],
                     "Vid : %s flyttas siffrorna %d steg åt höger: <b>%s</b>." % (num(t), len(str(t)) - 1, d(x)))
        q = ri(3, 999)
        return M("%s : %s = ?" % (num(q * t), num(t)), num(q), [num(q * 10) if q * 10 != q * t else num(q * 100), num(q // 10) if q >= 10 else num(q + 10), num(q * t - t)],
                 "Vid : %s tar du bort %d nollor: <b>%s</b>." % (num(t), len(str(t)) - 1, num(q)))

    def tvasiffrig():
        b = ri(12, 25)
        q = ri(12, 99)
        a = b * q
        return M("%s : %d = ?" % (num(a), b), str(q), [str(q + 1), str(q - 1), str(q + 10), str(q - 10)],
                 "Pröva: %d × %d = %s. Svar: <b>%d</b>." % (b, q, num(a), q))

    def dec_div():
        b = ri(2, 8)
        x = F(ri(11, 999), 10) * b if R0() else F(ri(11, 99), 100) * b
        q = x / b
        return M("%s : %d = ?" % (d(x), b), d(q), [d(q * 10), d(q / 10), d(q + F(1, 10)), d(x - b) if x > b else d(q * 2)],
                 "Dela som vanligt och sätt kommat i svaret rakt ovanför kommat i talet. Svar: <b>%s</b>." % d(q))

    def text_():
        n = K().name()
        k = ri(0, 3)
        if k == 0:
            b, q = ri(3, 9), ri(24, 180)
            return M("%d elever delar lika på %s kr som de har tjänat på en loppis. Hur mycket får var och en?" % (b, num(b * q)), kr(q),
                     [kr(x) for x in (q + 1, b * q - b, q * 10)], "%s : %d = <b>%s</b>." % (num(b * q), b, kr(q)))
        if k == 1:
            per = ch([4, 5, 6, 8])
            tot = ri(40, 400)
            q, r = divmod(tot, per)
            if r == 0:
                return None
            return M("%d elever ska åka bil till en match. I varje bil får %d elever plats. Hur många bilar behövs?" % (tot, per), str(q + 1),
                     [str(q), "%d rest %d" % (q, r), str(q + 2)], "%d : %d = %d rest %d. De som blir över behöver också en bil: <b>%d bilar</b>." % (tot, per, q, r, q + 1))
        if k == 2:
            dd = ri(3, 9)
            km = dd * ri(15, 120)
            return M("En familj cyklar %d km på %d dagar. De cyklar lika långt varje dag. Hur långt cyklar de per dag?" % (km, dd), "%d km" % (km // dd),
                     ["%d km" % x for x in (km - dd, km // dd + 1, km * dd)], "%d : %d = <b>%d km</b>." % (km, dd, km // dd))
        per = ch([6, 8, 10, 12])
        tot = per * ri(5, 40)
        return M("Ägg packas i kartonger med %d i varje. Hur många kartonger blir det av %d ägg?" % (per, tot), str(tot // per),
                 [str(tot // per + 1), str(tot - per), str(tot // per * 10)], "%d : %d = <b>%d</b>." % (tot, per, tot // per))

    if lv == 4:
        sets = [("Division och tabellerna", [(tabell, 20)]), ("Kort division", [(kort, 20)]), ("Division med rest", [(rest, 20)]),
                ("Dela med 10 och 100", [(tio, 20)]), ("Textuppgifter", [(text_, 20)])]
    elif lv == 5:
        sets = [("Kort division", [(kort, 20)]), ("Division med rest", [(rest, 20)]), ("Dela med 10, 100 och 1 000", [(tio, 20)]),
                ("Dela med tvåsiffriga tal", [(tvasiffrig, 20)]), ("Textuppgifter", [(text_, 20)])]
    else:
        sets = [("Kort division", [(kort, 20)]), ("Dela med 10, 100 och 1 000", [(tio, 20)]), ("Dela med tvåsiffriga tal", [(tvasiffrig, 20)]),
                ("Decimaltal i division", [(dec_div, 20)]), ("Textuppgifter", [(text_, 20)])]
    return unit("division", "T", "Division: kort division, rest och tvåsiffriga nämnare" if lv >= 5 else "Division: kort division och division med rest", "Division",
                "Metoder för beräkningar med naturliga tal%s vid huvudräkning och skriftliga metoder. Sambandet mellan multiplikation och division." % (" och tal i decimalform" if lv == 6 else ""),
                "Arbetsblad om division för årskurs %d: kort division, division med rest, dela med 10, 100 och 1 000%s och textuppgifter. 100 uppgifter med facit." % (lv, ", dela med tvåsiffriga tal" if lv >= 5 else ""),
                "Division är multiplikation baklänges", "Kontrollera: kvoten × nämnaren = täljaren.", sets,
                ["I kort division delar du siffra för siffra från vänster. Det som blir över förs vidare till nästa siffra.",
                 "Kontrollera med multiplikation: 852 : 4 = 213, eftersom 4 × 213 = 852.",
                 "Ibland går det inte jämnt ut. 47 : 5 = 9 rest 2. I en textuppgift måste du tänka på vad resten betyder, till exempel att det behövs en bil till."],
                [("852 : 4", ["8 : 4 = 2", "5 : 4 = 1, 1 över", "12 : 4 = 3"], "213"), ("Hur många bilar för 27 elever, 4 per bil?", ["27 : 4 = 6 rest 3", "3 elever behöver en bil till"], "7 bilar")],
                [["852 : 4 = 23 (hoppar över en siffra)", "Varje siffra ger en siffra i svaret: 213"], ["Resten är större än nämnaren", "Resten måste vara mindre än det du delar med"],
                 ["Svarar 6 bilar för 27 elever", "Resten behöver också plats: 7 bilar"]],
                [("Vad heter talen i en division?", "I 12 : 3 = 4 är 12 täljare, 3 nämnare och 4 kvot."),
                 ("Vad är kort division?", "En skriftlig metod där du delar siffra för siffra och skriver det som blir över som en liten siffra framför nästa."),
                 ("Kan man dela med 0?", "Nej, division med 0 går inte.")])


# ============================================================ prioriteringsregler
def prioritering(lv):
    def ga():
        a, b, c = ri(2, 20), ri(2, 9), ri(2, 9)
        k = ri(0, 3)
        if k == 0:
            v, w = a + b * c, (a + b) * c
            q = "%d + %d × %d" % (a, b, c)
        elif k == 1:
            if a * 2 <= b * c:
                a = b * c + ri(1, 20)
            v, w = a - b * c, (a - b) * c
            q = "%d − %d × %d" % (a, b, c)
        elif k == 2:
            v, w = a * b + c, a * (b + c)
            q = "%d × %d + %d" % (a, b, c)
        else:
            v, w = b * c - a if b * c > a else None, None
            if v is None:
                return None
            w = b * (c - a) if c > a else b * c + a
            q = "%d × %d − %d" % (b, c, a)
        return M("%s = ?" % q, num(v), [num(x) for x in (w, v + 1, a + b + c) if x is not None and x >= 0],
                 "Multiplikation före addition och subtraktion. Svar: <b>%s</b>." % num(v))

    def par():
        a, b, c = ri(2, 15), ri(2, 9), ri(2, 9)
        if R0():
            v, w = (a + b) * c, a + b * c
            q = "(%d + %d) × %d" % (a, b, c)
        else:
            if a <= b:
                a, b = b + ri(1, 9), a
            v, w = (a - b) * c, a - b * c
            q = "(%d − %d) × %d" % (a, b, c)
        return M("%s = ?" % q, num(v), [num(x) for x in (w, v + c, a + b + c) if x >= 0], "Räkna parentesen först. Svar: <b>%s</b>." % num(v))

    def divi():
        b, q = ri(2, 9), ri(2, 9)
        a = b * q
        c = ri(2, 20)
        if R0():
            v, w = c + a // b, None
            w = (c + a) // b if (c + a) % b == 0 else c + a - b
            s = "%d + %d : %d" % (c, a, b)
        else:
            v = a // b - c if a // b > c else None
            if v is None:
                return None
            s = "%d : %d − %d" % (a, b, c)
            w = a // (b - c) if b > c and a % (b - c) == 0 else a - b - c
        return M("%s = ?" % s, num(v), [num(x) for x in (w, v + 1, v + b) if x is not None and x >= 0],
                 "Division före addition och subtraktion. Svar: <b>%s</b>." % num(v))

    def ratt():
        a, b, c = ri(2, 10), ri(2, 9), ri(2, 9)
        v = a + b * c
        good = "%d + %d × %d = %d" % (a, b, c, v)
        bad = ["%d + %d × %d = %d" % (a, b, c, (a + b) * c), "(%d + %d) × %d = %d" % (a, b, c, v), "%d + %d × %d = %d" % (a, b, c, a * b + c) if a * b + c != v else "%d × %d + %d = %d" % (b, c, a, v + 1)]
        return M("Vilken uträkning av %d + %d × %d är rätt?" % (a, b, c), good, bad, "Multiplikationen räknas först: %d × %d = %d, sedan %d + %d = <b>%d</b>." % (b, c, b * c, a, b * c, v))

    def satt():
        a, b, c, t = ri(2, 9), ri(2, 9), ri(2, 9), None
        t = (a + b) * c
        good = "(%d + %d) × %d = %d" % (a, b, c, t)
        bad = ["%d + %d × %d = %d" % (a, b, c, t), "%d + (%d × %d) = %d" % (a, b, c, t), "%d × (%d + %d) = %d" % (a, b, c, t) if a * (b + c) != t else "%d + %d + %d = %d" % (a, b, c, t)]
        return M("Var ska parentesen stå för att det ska bli %d? Talen är %d, %d och %d." % (t, a, b, c), good, bad, "(%d + %d) × %d = %d × %d = <b>%d</b>." % (a, b, c, a + b, c, t))

    def text_():
        n = K().name()
        a, b, c = ri(2, 6), ri(12, 40), ri(5, 30)
        v = a * b + c
        return M("%s köper %d böcker för %d kr styck och en penna för %d kr. Vilket uttryck visar hur mycket det kostar?" % (n, a, b, c),
                 "%d × %d + %d = %d" % (a, b, c, v), ["(%d + %d) × %d = %d" % (a, b, c, (a + b) * c), "%d × (%d + %d) = %d" % (a, b, c, a * (b + c)), "%d + %d + %d = %d" % (a, b, c, a + b + c)],
                 "Böckerna kostar %d × %d och sedan läggs pennan till: <b>%d kr</b>." % (a, b, v))

    sets = [("Multiplikation först", [(ga, 20)]), ("Parenteser", [(par, 20)]), ("Division först", [(divi, 20)]),
            ("Rätt uträkning", [(ratt, 10), (satt, 10)]), ("Uttryck i vardagen", [(text_, 20)])]
    return unit("prioriteringsregler", "T", "Prioriteringsregler: räkneordning och parenteser", "Prioriteringsregler",
                "De fyra räknesättens egenskaper och samband samt användning i olika situationer. Räkneordning och parenteser.",
                "Arbetsblad om prioriteringsregler för årskurs %d: multiplikation och division före addition och subtraktion, parenteser först och uttryck i vardagen. 100 uppgifter med facit." % lv,
                "Parentes, × och :, + och −", "Räkna i rätt ordning, inte bara från vänster.", sets,
                ["Prioriteringsreglerna säger i vilken ordning du räknar: först det som står inom parentes, sedan multiplikation och division, sist addition och subtraktion.",
                 "3 + 4 × 5 = 3 + 20 = 23. Men (3 + 4) × 5 = 7 × 5 = 35.",
                 "Står bara addition och subtraktion, eller bara multiplikation och division, räknar du från vänster till höger."],
                [("3 + 4 × 5", ["4 × 5 = 20", "3 + 20"], "23"), ("(12 − 4) × 3", ["Parentesen först: 8", "8 × 3"], "24")],
                [["3 + 4 × 5 = 35", "Multiplikationen först: 23"], ["Glömmer parentesen", "Det inom parentes räknas först"],
                 ["20 − 8 : 2 = 6", "Division först: 20 − 4 = 16"]],
                [("Varför finns prioriteringsregler?", "Så att alla får samma svar på samma uttryck."),
                 ("Räknar miniräknaren rätt?", "De flesta miniräknare följer prioriteringsreglerna, men kontrollera alltid med ett överslag."),
                 ("Vad betyder en parentes?", "Att det som står inom den ska räknas först.")])


# ============================================================ negativa tal
def negativa(lv):
    def sg(n):
        return ("−%d" % -n) if n < 0 else str(n)

    def temp():
        a = ri(-15, 10)
        ch_ = ri(3, 15)
        up = R0()
        v = a + ch_ if up else a - ch_
        return M("Det är %s °C. Temperaturen %s med %d grader. Vad blir temperaturen?" % (sg(a), "stiger" if up else "sjunker", ch_), "%s °C" % sg(v),
                 ["%s °C" % sg(x) for x in (a - ch_ if up else a + ch_, -v if v else 1, v + 1, abs(a) + ch_)],
                 "Räkna på termometern: %s %s %d = <b>%s °C</b>." % (sg(a), "+" if up else "−", ch_, sg(v)))

    def ordna():
        xs = sorted(set(ri(-20, 20) for _ in range(4)))
        if len(xs) < 4 or not any(x < 0 for x in xs):
            return None
        xs = sh(xs)
        up = R0()
        g = sorted(xs, reverse=not up)
        f = lambda ys: ", ".join(sg(y) for y in ys)
        w = sorted(xs, key=abs, reverse=not up)
        return M("Ordna talen %s %s." % (f(xs), "från minst till störst" if up else "från störst till minst"), f(g),
                 [f(g[::-1]), f(w), f(xs) if xs != g else f(g[1:] + g[:1])], "Ju längre till vänster på tallinjen, desto mindre tal. Rätt: <b>%s</b>." % f(g))

    def jamfor():
        a, b = ri(-20, 5), ri(-20, 5)
        if a == b or (a >= 0 and b >= 0):
            return None
        good = "%s %s %s" % (sg(a), "&lt;" if a < b else "&gt;", sg(b))
        bad = ["%s %s %s" % (sg(a), "&gt;" if a < b else "&lt;", sg(b)), "%s = %s" % (sg(a), sg(b)), "%s %s %s" % (sg(b), "&lt;" if a < b else "&gt;", sg(a))]
        return M("Vilket är rätt? (%s och %s)" % (sg(a), sg(b)), good, bad, "Talet som ligger längst till höger på tallinjen är störst. Rätt: <b>%s</b>." % good)

    def skillnad():
        a, b = ri(1, 15), ri(-15, -1)
        k = ch(["dag", "natt"])
        return M("På dagen är det %d °C och på natten %s °C. Hur många grader skiljer det?" % (a, sg(b)), "%d grader" % (a - b),
                 ["%d grader" % x for x in (a + b if a + b > 0 else abs(a + b) + 1, abs(b), a, a - b + 1)],
                 "Från %s upp till 0 är det %d grader och sedan %d grader till: <b>%d grader</b>." % (sg(b), -b, a, a - b))

    def linje():
        lo = ri(-10, -5)
        v = ri(lo + 1, lo + 9)
        pic = tallinje(lo, lo + 10, 1, [(v, "A")], labels=[lo, lo + 5, lo + 10], width=380)
        return M(pic + "Vilket tal visar pilen A?", sg(v), [sg(x) for x in (-v, v + 1, v - 1, lo - (v - lo))],
                 "Varje streck är 1. Räkna från %s: <b>%s</b>." % (sg(lo), sg(v)))

    def rakna():
        a, b = ri(-12, 12), ri(1, 15)
        left = R0()
        if left:
            v = a - b
            q = "%s − %d" % (sg(a), b)
            w = [a + b, -(a + b), b - a]
        else:
            a = ri(-15, -1)
            v = a + b
            q = "%s + %d" % (sg(a), b)
            w = [a - b, -(a + b) if a + b else 1, b - a]
        return M("%s = ?" % q, sg(v), [sg(x) for x in w + [v + 1]], "Gå %d steg %s på tallinjen från %s: <b>%s</b>." % (b, "åt vänster" if left else "åt höger", sg(a), sg(v)))

    sets = [("Temperatur", [(temp, 20)]), ("Tallinjen", [(linje, 20)]), ("Jämföra negativa tal", [(jamfor, 12), (ordna, 8)]),
            ("Räkna med negativa tal", [(rakna, 20)]), ("Skillnad mellan temperaturer", [(skillnad, 14), (temp, 6)])]
    return unit("negativa-tal", "T", "Negativa tal: tallinjen och temperatur", "Negativa tal",
                "Negativa tal och hur de kan användas i vardagliga situationer, till exempel temperatur. Tallinjen med negativa tal.",
                "Arbetsblad om negativa tal för årskurs %d: tallinjen, temperatur, jämföra och ordna negativa tal och räkna med negativa tal. 100 uppgifter med facit." % lv,
                "Till vänster om noll", "Ju längre till vänster, desto mindre tal.", sets,
                ["Negativa tal är mindre än noll. De står till vänster om noll på tallinjen och skrivs med minustecken: −5.",
                 "−3 är större än −8, eftersom −3 ligger längre till höger. Tänk på en termometer: −3 °C är varmare än −8 °C.",
                 "När du lägger till går du åt höger på tallinjen och när du drar bort går du åt vänster. −4 + 6 = 2."],
                [("Det är −4 °C och blir 7 grader varmare", ["Gå 7 steg uppåt från −4", "−4 + 7"], "3 °C"), ("Skillnaden mellan 5 °C och −3 °C", ["3 till noll, 5 till"], "8 grader")],
                [["−8 är större än −3 eftersom 8 &gt; 3", "−3 ligger längre till höger: −3 &gt; −8"], ["−4 + 7 = −11", "Gå åt höger: 3"],
                 ["Skillnaden mellan 5 °C och −3 °C är 2 grader", "Räkna över noll: 8 grader"]],
                [("Var används negativa tal?", "Till exempel för temperatur under noll, för höjd under havsytan och när man har lånat pengar."),
                 ("Är noll negativt?", "Nej, noll är varken positivt eller negativt."),
                 ("Hur skriver man minus fem?", "Med ett minustecken före talet: −5.")])


UNITS = {"tal-och-positionssystemet": tal, "avrundning-och-overslag": avrundning, "addition-och-subtraktion": addsub,
         "multiplikation": mult, "division": div, "prioriteringsregler": prioritering, "negativa-tal": negativa}
