# -*- coding: utf-8 -*-
"""Sverige årskurs 3: tal och räkning — 単元 1〜12。se_a3.py から使う。"""
import math
from se_common import (num, kr, u, ord_, mcq, NB, Kids, hon, Hon, wrap, text, line, table,
                       positionstabell, basemat, tallinje, uppstallning, INK, GREEN, FILL, RED, BLUE)

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


def unit(slug, dom, sort, title, short, std, meta, kb, ks, sets, think, ex, mist, faq):
    return dict(slug=slug, dom=dom, sort=sort, title=title, short=short, std=std, meta=meta, kb=kb, ks=ks,
                sets=sets, think=think, ex=ex, mist=mist, faq=faq)


def cap(s):
    return s[0].upper() + s[1:]


def fr(a, b):
    return "<span class='fr'><span class='fn'>%d</span><span class='fd'>%d</span></span>" % (a, b)


def lt(a, b):
    return "&lt;" if a < b else ("&gt;" if a > b else "=")


# ============================================================ 1. Tal till 1 000
def u1():
    def n3():
        return ri(101, 999)

    def ordform():
        n = n3()
        h, t, e = n // 100, n // 10 % 10, n % 10
        sw = [h * 100 + e * 10 + t, t * 100 + h * 10 + e, h * 10 + e]
        if R.random() < 0.5:
            return mcq("Vilket tal skrivs <b>%s</b>?" % ord_(n), num(n), [num(x) for x in sw if x != n] + [num(n + 10), num(n + 100)],
                       "%s = %d hundratal, %d tiotal och %d ental: <b>%s</b>." % (cap(ord_(n)), h, t, e, num(n)))
        return mcq("Hur skrivs talet <b>%s</b> med bokstäver?" % num(n), ord_(n), [ord_(x) for x in sw if 0 < x < 1000 and x != n] + [ord_(n + 1), ord_(n + 10)],
                   "%s skrivs <b>%s</b>." % (num(n), ord_(n)))

    def block():
        h, t, e = ri(1, 7), ri(0, 9), ri(0, 9)
        n = h * 100 + t * 10 + e
        return mcq("Vilket tal visar bilden?" + basemat(h, t, e), num(n),
                   [num(h * 100 + e * 10 + t), num(h + t * 10 + e * 100), num(h * 10 + t + e), num(n + 10), num(n - 1)],
                   "%d hundratal = %d, %d tiotal = %d och %d ental = %d. Tillsammans <b>%s</b>." % (h, h * 100, t, t * 10, e, e, num(n)))

    def varde():
        n = n3()
        ds = str(n)
        i = ri(0, 2)
        d = int(ds[i])
        if d == 0 or ds.count(ds[i]) > 1:
            return None
        v = d * 10 ** (2 - i)
        plats = ["hundratalsplatsen", "tiotalsplatsen", "entalsplatsen"]
        if R.random() < 0.55:
            return mcq("Vilket värde har siffran <b>%d</b> i talet <b>%s</b>?" % (d, num(n)), num(v),
                       [num(d * 10 ** k) for k in range(3) if k != 2 - i] + [num(d * 1000)],
                       "Siffran %d står på %s. Den är värd <b>%s</b>." % (d, plats[i], num(v)))
        return mcq("På vilken plats står siffran <b>%d</b> i talet <b>%s</b>?" % (d, num(n)), plats[i],
                   [p for p in plats if p != plats[i]] + ["tusentalsplatsen"],
                   "I %s står hundratalen först, sedan tiotalen och sist entalen. Siffran %d står på <b>%s</b>." % (num(n), d, plats[i]))

    def utvecklad():
        h, t, e = ri(1, 9), ri(0, 9), ri(0, 9)
        n = h * 100 + t * 10 + e
        k = ri(0, 2)
        if k == 0:
            if not (t and e):
                return None
            return mcq("%s + %s + %s = ?" % (num(h * 100), num(t * 10), num(e)), num(n), [num(h + t + e), num(h * 100 + e * 10 + t), num(h * 10 + t + e)],
                       "Hundratal %d, tiotal %d, ental %d: <b>%s</b>." % (h, t, e, num(n)))
        if k == 1:
            if t and e:
                return None
            wrong = [num(h * 10 + (t or e)), num(h * 100 + (t or e) * (1 if t else 10)), num(h * 1000 + (t or e))]
            return mcq("Vilket tal har %d hundratal, %d tiotal och %d ental?" % (h, t, e), num(n), wrong,
                       "Saknas tiotal eller ental skriver du en nolla på den platsen: <b>%s</b>." % num(n))
        if not (t and e):
            return None
        return mcq("Hur skrivs <b>%s</b> i utvecklad form?" % num(n), "%s + %s + %s" % (num(h * 100), num(t * 10), num(e)),
                   ["%d + %d + %d" % (h, t, e), "%s + %s + %s" % (num(h * 100), num(e * 10), num(t)), "%s + %s + %s" % (num(h * 10), num(t * 100), num(e))],
                   "%s = %s + %s + %s." % (num(n), num(h * 100), num(t * 10), num(e)))

    def tabell():
        n = n3()
        return mcq("Vilket tal står i positionstabellen?" + positionstabell(n), num(n),
                   [num(int(str(n)[::-1])), num(n + 100) if n < 900 else num(n - 100), num(n + 1)],
                   "Hundratal %s, tiotal %s, ental %s: <b>%s</b>." % (str(n)[0], str(n)[1], str(n)[2], num(n)))

    def tusen():
        k = ri(0, 2)
        if k == 0:
            n = ri(1, 9) * 100
            return mcq("Hur mycket fattas från %s till %s?" % (num(n), num(1000)), num(1000 - n), [num(1000 - n + 100), num(n), num(1000 - n - 100) if n < 900 else num(10)],
                       "%s + %s = %s. Det fattas <b>%s</b>." % (num(n), num(1000 - n), num(1000), num(1000 - n)))
        if k == 1:
            n = ri(90, 99) * 10
            return mcq("Du räknar tiotal: %s, %s, … Vilket tal kommer efter %s?" % (num(n - 20), num(n - 10), num(n)), num(n + 10), [num(n + 1), num(n + 100), num(n - 10)],
                       "%s + 10 = <b>%s</b>." % (num(n), num(n + 10)))
        a = ri(1, 9)
        return mcq("Hur många tiotal finns det i %s?" % num(a * 100), num(a * 10), [str(a), num(a * 100), num(a * 10 + 10)],
                   "1 hundratal = 10 tiotal, så %d hundratal = <b>%s tiotal</b>." % (a, num(a * 10)))

    sets = [("Läsa och skriva tal", [(ordform, 20)]),
            ("Hundratal, tiotal och ental", [(block, 14), (tabell, 6)]),
            ("Siffrans värde", [(varde, 20)]),
            ("Utvecklad form", [(utvecklad, 16), (tusen, 4)]),
            ("Blandat", [(ordform, 6), (varde, 6), (block, 4), (tusen, 4)])]
    return unit("tal-till-1000", "T", 1, "Tal till 1 000: hundratal, tiotal och ental", "Tal till 1 000",
                "Naturliga tal och hur de kan delas upp. Hur positionssystemet används för att beskriva naturliga tal: ental, tiotal, hundratal och tusental.",
                "Arbetsblad om tal till 1 000 för årskurs 3: läsa och skriva tal, hundratal, tiotal och ental, siffrans värde och utvecklad form. 100 uppgifter med facit.",
                "Hundratal, tiotal, ental", "Var siffran står bestämmer vad den är värd.", sets,
                ["Ett tresiffrigt tal har hundratal, tiotal och ental. Läs från vänster: först hundratalen, sedan tiotalen och sist entalen.",
                 "Siffrans värde beror på var den står. I talet 472 är siffran 7 värd 70, eftersom den står på tiotalsplatsen.",
                 "Finns det inga tiotal eller ental skriver du en nolla: 5 hundratal och 8 ental blir 508."],
                [("3 hundratal, 6 tiotal och 2 ental", ["300 + 60 + 2"], "362"), ("fyrahundrafem", ["4 hundratal, 0 tiotal och 5 ental"], "405")],
                [["fyrahundrafem skrivs 45", "Tiotalsplatsen är tom, skriv en nolla: 405"], ["Siffran 7 i 472 är värd 7", "Den står på tiotalsplatsen och är värd 70"],
                 ["fyrahundrafem skrivs 4005", "Ett tresiffrigt tal har bara tre platser: 405"]],
                [("Vad är skillnaden mellan siffra och tal?", "Siffrorna är 0–9. Ett tal kan bestå av flera siffror, till exempel 472."),
                 ("Vilket är det största tresiffriga talet?", "999. Ett mer är 1 000 (ettusen)."),
                 ("Varför är nollan viktig?", "Nollan visar att en plats är tom. 508 och 58 är olika tal.")])


# ============================================================ 2. Jämföra och ordna tal
def u2():
    def jamfor():
        a = ri(100, 999)
        b = a + ch([1, 10, 100, -1, -10, -100, 9, 90, -9, -90])
        if not 100 <= b <= 999 or a == b:
            return None
        r = lt(a, b)
        good = "%s %s %s" % (num(a), r, num(b))
        bad = ["%s %s %s" % (num(a), o, num(b)) for o in ("&lt;", "&gt;", "=") if o != r] + ["%s %s %s" % (num(b), r, num(a))]
        return mcq("Vilket är rätt? (%s och %s)" % (num(a), num(b)), good, bad,
                   "Jämför först hundratalen. Är de lika jämför du tiotalen. Rätt är <b>%s</b>." % good)

    def ordna():
        base = ri(1, 8) * 100
        xs = sorted(set([base + ri(0, 99), base + ri(0, 99), base + ri(100, 199), base + ri(0, 9) * 10 + ri(0, 9), ri(100, 999)]))
        if len(xs) < 4:
            return None
        xs = sh(xs)[:4]
        up = R.random() < 0.5
        g = sorted(xs, reverse=not up)
        f = lambda ys: ", ".join(num(y) for y in ys)
        w = list(g)
        w[1], w[2] = w[2], w[1]
        return mcq("Ordna talen %s %s." % (f(xs), "från minst till störst" if up else "från störst till minst"), f(g),
                   [f(g[::-1]), f(w), f(xs) if xs != g else f(w[::-1])], "Rätt ordning: <b>%s</b>." % f(g))

    def granne():
        n = ri(101, 998)
        k = ri(0, 3)
        if k == 0:
            return mcq("Vilket tal kommer direkt efter %s?" % num(n), num(n + 1), [num(n - 1), num(n + 10), num(n + 2)],
                       "Talet efter är 1 mer: <b>%s</b>." % num(n + 1))
        if k == 1:
            return mcq("Vilket tal kommer direkt före %s?" % num(n), num(n - 1), [num(n + 1), num(n - 10), num(n - 2)],
                       "Talet före är 1 mindre: <b>%s</b>." % num(n - 1))
        if k == 2:
            if n > 889:
                return None
            return mcq("Vilket tal är 10 mer än %s?" % num(n), num(n + 10), [num(n + 1), num(n + 100), num(n - 10)],
                       "Tiotalssiffran ökar med 1: <b>%s</b>." % num(n + 10))
        if n > 899:
            return None
        return mcq("Vilket tal är 100 mer än %s?" % num(n), num(n + 100), [num(n + 10), num(n + 1000) if False else num(n + 1), num(n - 100) if n > 199 else num(n + 200)],
                   "Hundratalssiffran ökar med 1: <b>%s</b>." % num(n + 100))

    def linje():
        lo = ri(1, 8) * 100
        k = ri(0, 1)
        if k == 0:
            v = lo + ri(1, 9) * 10
            pic = tallinje(lo, lo + 100, 10, [(v, "A")], labels=[lo, lo + 100], width=400)
            return mcq(pic + "Vilket tal visar pilen A?", num(v), [num(lo + (v - lo) // 10), num(v + 10), num(v - 10), num(lo + 10 * (v - lo))],
                       "Varje streck är 10 steg. Pilen står på %d:e strecket efter %s: <b>%s</b>." % ((v - lo) // 10, num(lo), num(v)))
        lo = ri(0, 9) * 100
        v = lo + ri(1, 9) * 100 // 10 * 1
        v = lo + 50 if R.random() < 0.3 else lo + ri(1, 9) * 10
        pic = tallinje(lo, lo + 100, 10, [(v, "B")], labels=[lo, lo + 50, lo + 100], width=400)
        return mcq(pic + "Vilket tal visar pilen B?", num(v), [num(v + 10), num(v - 10), num(v + 5)],
                   "Mitt emellan %s och %s ligger %s. Räkna tiotal därifrån: <b>%s</b>." % (num(lo), num(lo + 100), num(lo + 50), num(v)))

    def storst():
        ds = sh(range(1, 10))[:3]
        big = int("".join(str(d) for d in sorted(ds, reverse=True)))
        small = int("".join(str(d) for d in sorted(ds)))
        others = [int("".join(str(d) for d in p)) for p in (ds, ds[::-1], [ds[1], ds[0], ds[2]])]
        if R.random() < 0.5:
            return mcq("Vilket är det <b>största</b> talet du kan skriva med siffrorna %s (varje siffra en gång)?" % ", ".join(map(str, ds)), num(big),
                       [num(x) for x in others + [small] if x != big], "Lägg den största siffran på hundratalsplatsen: <b>%s</b>." % num(big))
        return mcq("Vilket är det <b>minsta</b> talet du kan skriva med siffrorna %s (varje siffra en gång)?" % ", ".join(map(str, ds)), num(small),
                   [num(x) for x in others + [big] if x != small], "Lägg den minsta siffran på hundratalsplatsen: <b>%s</b>." % num(small))

    def mellan():
        a = ri(100, 900)
        b = a + ri(20, 90)
        c = ri(a + 1, b - 1)
        w = [a - ri(1, 30), b + ri(1, 30), b + 100 if b < 899 else a - 100]
        return mcq("Vilket tal ligger mellan %s och %s?" % (num(a), num(b)), num(c), [num(x) for x in w if 0 < x < 1000],
                   "%s är större än %s och mindre än %s." % (num(c), num(a), num(b)))

    sets = [("Större än och mindre än", [(jamfor, 20)]),
            ("Talet före och efter", [(granne, 20)]),
            ("Tallinjen", [(linje, 20)]),
            ("Ordna tal", [(ordna, 12), (storst, 8)]),
            ("Blandat", [(jamfor, 5), (mellan, 6), (ordna, 4), (storst, 5)])]
    return unit("jamfora-och-ordna-tal", "T", 2, "Jämföra och ordna tal till 1 000", "Jämföra och ordna tal",
                "Naturliga tal och hur de kan användas för att ange antal och ordning. Tal på tallinjen och jämförelse med större än och mindre än.",
                "Arbetsblad om att jämföra och ordna tal för årskurs 3: större än och mindre än, talet före och efter, 10 och 100 mer, tallinjen och att ordna tal. 100 uppgifter med facit.",
                "Jämför hundratalen först", "Är hundratalen lika jämför du tiotalen och sedan entalen.", sets,
                ["Jämför två tal plats för plats från vänster. Först hundratalen, sedan tiotalen och sist entalen.",
                 "Tecknet &lt; betyder mindre än och &gt; betyder större än. Den öppna sidan pekar alltid mot det större talet: 356 &lt; 365.",
                 "På tallinjen blir talen större åt höger. Räkna vad varje streck är värt innan du läser av."],
                [("Jämför 487 och 478", ["Hundratalen är lika (4)", "Tiotalen: 8 är större än 7"], "487 &gt; 478"),
                 ("Talet 10 mer än 395", ["9 tiotal + 1 tiotal = 10 tiotal = 1 hundratal"], "405")],
                [["398 &gt; 412 för att 9 är större än 1", "Jämför hundratalen först: 3 &lt; 4, så 398 &lt; 412"],
                 ["10 mer än 395 är 3105", "395 + 10 = 405"],
                 ["Varje streck på tallinjen är 1", "Läs vad strecken är värda: här 10"]],
                [("Hur kommer jag ihåg &lt; och &gt;?", "Spetsen pekar mot det mindre talet och den öppna sidan mot det större."),
                 ("Vad betyder att ordna från minst till störst?", "Du börjar med det minsta talet och slutar med det största."),
                 ("Hur hittar jag 100 mer?", "Öka hundratalssiffran med 1. Tiotalen och entalen är kvar: 245 → 345.")])


# ============================================================ 3. Avrundning, överslag och rimlighet
def avr(n, p):
    return int(math.floor(n / float(p) + 0.5)) * p


def u3():
    def tiotal():
        n = ri(11, 994)
        if n % 10 == 0:
            return None
        r = avr(n, 10)
        lo, hi = n // 10 * 10, n // 10 * 10 + 10
        return mcq("Avrunda <b>%s</b> till närmaste tiotal." % num(n), num(r), [num(lo if r == hi else hi), num(avr(n, 100)), num(n // 10)],
                   "%s ligger mellan %s och %s. Entalssiffran är %d, så du avrundar %s: <b>%s</b>." % (
                       num(n), num(lo), num(hi), n % 10, "uppåt" if n % 10 >= 5 else "nedåt", num(r)))

    def hundratal():
        n = ri(101, 949)
        if n % 100 == 0 or avr(n, 100) == avr(n, 10):
            return None
        r = avr(n, 100)
        lo, hi = n // 100 * 100, n // 100 * 100 + 100
        return mcq("Avrunda <b>%s</b> till närmaste hundratal." % num(n), num(r), [num(lo if r == hi else hi), num(avr(n, 10)), num(n // 100)],
                   "Titta på tiotalssiffran: %d. %s Svar: <b>%s</b>." % (n // 10 % 10, "5 eller mer avrundas uppåt." if n // 10 % 10 >= 5 else "Mindre än 5 avrundas nedåt.", num(r)))

    def overslag():
        a, b = ri(110, 590), ri(110, 390)
        if a % 100 in range(40, 61) or b % 100 in range(40, 61):
            return None
        op = ch("+-")
        if op == "-" and a < b:
            a, b = b, a
        ra, rb = avr(a, 100), avr(b, 100)
        est = ra + rb if op == "+" else ra - rb
        if est <= 0:
            return None
        w = [est + 100, est - 100 if est > 100 else est + 200, (a + b if op == "+" else a - b)]
        sym = "+" if op == "+" else "−"
        return mcq("Gör ett överslag: ungefär hur mycket är %s %s %s?" % (num(a), sym, num(b)), "ungefär " + num(est),
                   ["ungefär " + num(x) for x in w[:2]] + ["ungefär " + num(est + 300)],
                   "Avrunda till hundratal: %s %s %s = <b>%s</b>." % (num(ra), sym, num(rb), num(est)))

    def rimligt():
        a, b = ri(120, 480), ri(110, 480)
        s = a + b
        w = [s + 100, s - 100, s + 10 * ri(2, 5)]
        if R.random() < 0.5:
            w = [a + b // 10, s * 10 if s * 10 < 10000 else s + 300, s - 200]
        return mcq("%s + %s. Vilket svar är rimligt? Gör ett överslag först." % (num(a), num(b)), num(s), [num(x) for x in w if x > 0],
                   "Överslag: %s + %s = %s. Bara <b>%s</b> ligger nära.%s" % (num(avr(a, 100)), num(avr(b, 100)), num(avr(a, 100) + avr(b, 100)), num(s),
                                                                         ""))

    def handla():
        k = K.name()
        items = sh([("en bok", 89, 149), ("ett spel", 190, 290), ("en tröja", 149, 249), ("en boll", 79, 129), ("ett par skor", 290, 490), ("en ryggsäck", 199, 349)])[:2]
        p = [ri(lo, hi) for _, lo, hi in items]
        if any(x % 100 in range(40, 61) for x in p):
            return None
        tot = p[0] + p[1]
        est = avr(p[0], 100) + avr(p[1], 100)
        return mcq("%s köper %s för %s och %s för %s. Ungefär hur mycket kostar det tillsammans?" % (k, items[0][0], kr(p[0]), items[1][0], kr(p[1])),
                   "ungefär " + kr(est), ["ungefär " + kr(x) for x in (est + 100, est - 100 if est > 100 else est + 200, est + 200)],
                   "Avrunda till hundratal: %s + %s = <b>%s</b>. (Exakt: %s.)" % (kr(avr(p[0], 100)), kr(avr(p[1], 100)), kr(est), kr(tot)))

    def racker():
        k = K.name()
        have = ri(3, 9) * 100
        a, b = ri(100, 400), ri(100, 400)
        tot = a + b
        if abs(tot - have) < 30 or abs(tot - have) > 250:
            return None
        ok = tot <= have
        return mcq("%s har %s. %s vill köpa två saker som kostar %s och %s. Räcker pengarna?" % (k, kr(have), k, kr(a), kr(b)),
                   "Ja" if ok else "Nej", ["Nej" if ok else "Ja", "Det går inte att veta", "Bara till den ena, aldrig till båda" if ok else "Ja, det blir pengar över"],
                   "%s + %s = %s. Det är %s än %s, så svaret är <b>%s</b>." % (kr(a), kr(b), kr(tot), "mindre" if ok else "mer", kr(have), "ja" if ok else "nej"))

    sets = [("Avrunda till tiotal", [(tiotal, 20)]),
            ("Avrunda till hundratal", [(hundratal, 20)]),
            ("Överslagsräkning", [(overslag, 20)]),
            ("Är svaret rimligt?", [(rimligt, 14), (racker, 6)]),
            ("Överslag i vardagen", [(handla, 12), (racker, 4), (tiotal, 2), (hundratal, 2)])]
    return unit("overslagsrakning-och-rimlighet", "T", 3, "Avrundning, överslagsräkning och rimlighet", "Överslagsräkning",
                "Metoder för beräkningar med naturliga tal vid överslagsräkning. Rimlighetsbedömning vid uppskattningar och beräkningar.",
                "Arbetsblad om överslagsräkning för årskurs 3: avrunda till tiotal och hundratal, gör överslag, bedöm om svaret är rimligt och räkna ungefär när du handlar. 100 uppgifter med facit.",
                "Avrunda och räkna ungefär", "Ett överslag visar om svaret är rimligt.", sets,
                ["Avrunda till närmaste tiotal: titta på entalssiffran. 0–4 avrundas nedåt, 5–9 avrundas uppåt. 47 blir 50 och 43 blir 40.",
                 "Avrunda till närmaste hundratal: titta på tiotalssiffran. 362 blir 400 och 328 blir 300.",
                 "Ett överslag är en snabb räkning med avrundade tal. Jämför ditt svar med överslaget. Ligger de långt ifrån varandra har du troligen räknat fel."],
                [("Ungefär hur mycket är 298 + 403?", ["298 ≈ 300 och 403 ≈ 400", "300 + 400 = 700"], "ungefär 700"),
                 ("Avrunda 365 till närmaste tiotal", ["Entalssiffran är 5", "5 avrundas uppåt"], "370")],
                [["45 avrundat till tiotal blir 40", "5 avrundas uppåt: 50"], ["362 avrundat till hundratal blir 360", "Till hundratal: titta på tiotalet: 400"],
                 ["Svaret 1 701 för 298 + 403 kontrolleras inte", "Överslaget är 700, så 1 701 kan inte stämma"]],
                [("Vad betyder tecknet ≈?", "Det betyder ungefär lika med: 298 ≈ 300."),
                 ("När ska jag göra ett överslag?", "Innan eller efter du räknar exakt. Då ser du om svaret är rimligt."),
                 ("Är ett överslag samma sak som en gissning?", "Nej. Ett överslag är en beräkning med avrundade tal. En gissning har ingen beräkning.")])


# ============================================================ 4. Huvudräkning
def u4():
    def kamrater():
        k = ri(0, 2)
        if k == 0:
            a = ri(1, 9)
            return mcq("Vilket tal är tiokamrat till %d? %d + ? = 10" % (a, a), str(10 - a), [str(a), str(11 - a), str(10 + a)],
                       "%d + %d = 10. Svar: <b>%d</b>." % (a, 10 - a, 10 - a))
        if k == 1:
            a = ri(1, 9) * 10
            return mcq("Vilket tal är hundrakamrat till %d? %d + ? = 100" % (a, a), num(100 - a), [num(a), num(110 - a), num(100 - a + 1)],
                       "%d + %d = 100. Svar: <b>%d</b>." % (a, 100 - a, 100 - a))
        a = ri(11, 89)
        if a % 10 == 0:
            return None
        return mcq("%d + ? = 100" % a, num(100 - a), [num(110 - a), num(90 - a), num(10 - a % 10 + (10 - a // 10) * 10)],
                   "Från %d till %d är det %d, och sedan %d till 100. %d + %d = <b>%d</b>." % (a, (a // 10 + 1) * 10, (a // 10 + 1) * 10 - a, 100 - (a // 10 + 1) * 10,
                                                                                    (a // 10 + 1) * 10 - a, 100 - (a // 10 + 1) * 10, 100 - a))

    def add100():
        a, b = ri(12, 68), ri(11, 39)
        if a % 10 + b % 10 < 10 or a + b > 100:
            return None
        s = a + b
        return mcq("%d + %d = ?" % (a, b), str(s), [str(s - 10), str(s + 10), str(a // 10 * 10 + b // 10 * 10 + (a % 10 + b % 10) % 10)],
                   "Tiotal: %d + %d = %d. Ental: %d + %d = %d. %d + %d = <b>%d</b>." % (a // 10 * 10, b // 10 * 10, a // 10 * 10 + b // 10 * 10, a % 10, b % 10, a % 10 + b % 10,
                                                                                a // 10 * 10 + b // 10 * 10, a % 10 + b % 10, s))

    def sub100():
        a, b = ri(31, 99), ri(12, 29)
        if a % 10 >= b % 10 or a - b < 5:
            return None
        d = a - b
        wrong = (a // 10 - b // 10) * 10 + (b % 10 - a % 10)
        return mcq("%d − %d = ?" % (a, b), str(d), [str(wrong), str(d + 10), str(d - 10) if d > 10 else str(d + 2)],
                   "Ta först bort %d: %d − %d = %d. Ta sedan bort %d: %d − %d = <b>%d</b>." % (b // 10 * 10, a, b // 10 * 10, a - b // 10 * 10, b % 10, a - b // 10 * 10, b % 10, d))

    def hela():
        k = ri(0, 3)
        if k == 0:
            a, b = ri(1, 6) * 100, ri(1, 3) * 100
            return mcq("%s + %s = ?" % (num(a), num(b)), num(a + b), [num(a + b + 100), num(a // 100 + b // 100), num(a + b - 100)],
                       "%d hundratal + %d hundratal = %d hundratal: <b>%s</b>." % (a // 100, b // 100, (a + b) // 100, num(a + b)))
        if k == 1:
            a, b = ri(2, 9) * 100 + ri(1, 9) * 10, ri(1, 4) * 10
            if a % 100 < b:
                return None
            return mcq("%s − %s = ?" % (num(a), num(b)), num(a - b), [num(a - b * 10), num(a + b), num(a - b - 10)],
                       "Ta bort %d tiotal: <b>%s</b>." % (b // 10, num(a - b)))
        if k == 2:
            a, b = ri(1, 7) * 100 + ri(1, 9) * 10, ri(1, 2) * 100 + ri(1, 9) * 10
            if (a + b) // 100 > 9:
                return None
            return mcq("%s + %s = ?" % (num(a), num(b)), num(a + b), [num(a + b - 100), num(a + b + 10), num(a + b + 100)],
                       "Hundratal: %d + %d. Tiotal: %d + %d. Tillsammans <b>%s</b>." % (a // 100 * 100, b // 100 * 100, a % 100, b % 100, num(a + b)))
        a = ri(3, 9) * 100
        b = ri(1, 9) * 10 + ri(1, 2) * 100
        if b >= a:
            return None
        return mcq("%s − %s = ?" % (num(a), num(b)), num(a - b), [num(a - b + 100), num(a - b - 10) if a - b > 10 else num(a - b + 20), num(a - b + 20)],
                   "%s − %s = %s, sedan − %d = <b>%s</b>." % (num(a), num(b // 100 * 100), num(a - b // 100 * 100), b % 100, num(a - b)))

    def smart():
        k = ri(0, 2)
        if k == 0:
            a = ri(21, 89)
            t = ch([9, 19, 29, 99])
            if a + t > 200:
                return None
            return mcq("Räkna smart: %d + %d = ?" % (a, t), num(a + t), [num(a + t + 1), num(a + t - 1), num(a + t + 10)],
                       "%d är 1 mindre än %d. %d + %d − 1 = <b>%s</b>." % (t, t + 1, a, t + 1, num(a + t)))
        if k == 1:
            a = ri(40, 99)
            t = ch([9, 19, 29])
            if a <= t:
                return None
            return mcq("Räkna smart: %d − %d = ?" % (a, t), num(a - t), [num(a - t - 1), num(a - t + 10), num(a - t - 2)],
                       "Ta bort %d och lägg tillbaka 1: %d − %d + 1 = <b>%s</b>." % (t + 1, a, t + 1, num(a - t)))
        xs = sh([ri(11, 39), ri(1, 9)])
        c = 10 - xs[1] % 10 if xs[1] % 10 else 5
        c = (10 - xs[0] % 10) if xs[0] % 10 else 5
        tot = xs[0] + xs[1] + c
        return mcq("Räkna smart: %d + %d + %d = ?" % (xs[0], xs[1], c), num(tot), [num(tot + 10), num(tot - 10), num(tot + 1)],
                   "Börja med tiokamraterna: %d + %d = %d. Lägg till %d: <b>%s</b>." % (xs[0], c, xs[0] + c, xs[1], num(tot)))

    def text_():
        n, g = K.next()
        k = ri(0, 2)
        if k == 0:
            a, b = ri(25, 65), ri(15, 34)
            return mcq("%s har %d klistermärken. %s får %d till. Hur många har %s nu?" % (n, a, Hon(g), b, hon(g)), str(a + b), [str(a + b - 10), str(a - b), str(a + b + 10)],
                       "%d + %d = <b>%d</b>." % (a, b, a + b))
        if k == 1:
            a, b = ri(50, 99), ri(13, 39)
            return mcq("Det finns %d kanelbullar på fikat. %d blir uppätna. Hur många är kvar?" % (a, b), str(a - b), [str(a + b), str(a - b + 10), str(a - b - 10)],
                       "%d − %d = <b>%d</b>." % (a, b, a - b))
        a = ri(120, 380)
        b = ri(1, 4) * 100
        return mcq("En bok har %d sidor. %s har läst %d sidor. Hur många sidor är kvar?" % (a + b, n, b), num(a), [num(a + b), num(a - 100), num(a + 10)],
                   "%s − %s = <b>%s</b>." % (num(a + b), num(b), num(a)))

    sets = [("Tiokamrater och hundrakamrater", [(kamrater, 20)]),
            ("Addition till 100", [(add100, 20)]),
            ("Subtraktion till 100", [(sub100, 20)]),
            ("Hela tiotal och hundratal", [(hela, 20)]),
            ("Räkna smart och problem", [(smart, 10), (text_, 10)])]
    return unit("huvudrakning", "T", 4, "Huvudräkning: addition och subtraktion", "Huvudräkning",
                "Metoder för beräkningar med naturliga tal vid huvudräkning. De fyra räknesättens egenskaper och samband samt användning i olika situationer.",
                "Arbetsblad om huvudräkning för årskurs 3: tiokamrater och hundrakamrater, addition och subtraktion till 100, hela tiotal och hundratal och att räkna smart. 100 uppgifter med facit.",
                "Dela upp talen", "Räkna tiotal för sig och ental för sig.", sets,
                ["Dela upp talen i tiotal och ental. 47 + 25: 40 + 20 = 60, 7 + 5 = 12, 60 + 12 = 72.",
                 "Vid subtraktion kan du ta bort tiotalen först och sedan entalen. 63 − 28: 63 − 20 = 43, 43 − 8 = 35.",
                 "Tiokamrater (3 och 7) och hundrakamrater (30 och 70) gör det lättare att räkna. 9 är nästan 10: 46 + 9 = 46 + 10 − 1 = 55."],
                [("47 + 25", ["40 + 20 = 60", "7 + 5 = 12", "60 + 12 = 72"], "72"),
                 ("63 − 28", ["63 − 20 = 43", "43 − 8 = 35"], "35")],
                [["63 − 28 = 45 (8 − 3 i stället för 3 − 8)", "Du kan inte ta 8 från 3. Räkna 63 − 20 = 43, 43 − 8 = 35"],
                 ["47 + 25 = 62 (glömmer tiotalet från 7 + 5)", "7 + 5 = 12 är ett tiotal och 2 ental: 72"],
                 ["46 + 9: lägger till 10 men glömmer att ta bort 1", "46 + 10 − 1 = 55"]],
                [("Vad är tiokamrater?", "Två tal som tillsammans blir 10, till exempel 4 och 6."),
                 ("Måste jag skriva upp när jag räknar i huvudet?", "Nej, men det är bra att skriva delsvaren om talen är stora."),
                 ("Hur kan jag kontrollera en subtraktion?", "Räkna baklänges med addition: 35 + 28 = 63. Då stämmer 63 − 28 = 35.")])


# ============================================================ 5. Addition med uppställning
def u5():
    def pair(carry):
        while True:
            a, b = ri(105, 699), ri(105, 399)
            if a + b > 999:
                continue
            c1 = a % 10 + b % 10 >= 10
            c2 = a // 10 % 10 + b // 10 % 10 + (1 if c1 else 0) >= 10
            n = c1 + c2
            if n == carry:
                return a, b

    def nocarry(a, b):
        """vanligt fel: glömmer minnessiffran"""
        r, p = 0, 1
        x, y = a, b
        while x or y:
            r += ((x % 10 + y % 10) % 10) * p
            x //= 10
            y //= 10
            p *= 10
        return r

    def ber():
        a, b = pair(ch([0, 1, 1, 2]))
        s = a + b
        w = [nocarry(a, b), s + 10, s - 10, s + 100]
        return mcq("Räkna med uppställning: %s + %s = ?" % (num(a), num(b)), num(s), [num(x) for x in w if x != s],
                   "Ental, tiotal, hundratal. Glöm inte minnessiffran när summan blir 10 eller mer. Svar: <b>%s</b>." % num(s))

    def bild():
        a, b = pair(ch([1, 2]))
        s = a + b
        pic = uppstallning([str(a), str(b)], "+")
        return mcq(pic + "Vad blir summan?", num(s), [num(nocarry(a, b)), num(s + 100), num(s - 10)],
                   "Entalen: %d + %d = %d. Tiotalen och hundratalen på samma sätt, med minnessiffran. Svar: <b>%s</b>." % (a % 10, b % 10, a % 10 + b % 10, num(s)))

    def minne():
        a, b = pair(ch([1, 2]))
        e = a % 10 + b % 10
        if e < 10:
            return None
        return mcq("Du räknar %s + %s med uppställning. Entalen blir %d + %d = %d. Vad skriver du under strecket och vad blir minnessiffran?" % (num(a), num(b), a % 10, b % 10, e),
                   "%d under strecket, minnessiffra 1" % (e % 10), ["%d under strecket, ingen minnessiffra" % e, "1 under strecket, minnessiffra %d" % (e % 10), "0 under strecket, minnessiffra 1"],
                   "%d = 1 tiotal och %d ental. Skriv %d och lägg 1 som minnessiffra över tiotalen." % (e, e % 10, e % 10))

    def text_():
        n = K.name()
        k = ri(0, 2)
        a, b = pair(ch([1, 1, 2]))
        s = a + b
        if k == 0:
            q = "I skolan finns %s elever på lågstadiet och %s elever på mellanstadiet. Hur många elever är det tillsammans?" % (num(a), num(b))
        elif k == 1:
            q = "%s cyklar %s meter till affären och sedan %s meter till biblioteket. Hur långt cyklar %s?" % (n, num(a), num(b), n)
        else:
            q = "På en loppis säljs %s böcker på lördagen och %s på söndagen. Hur många böcker säljs totalt?" % (num(a), num(b))
        unitw = " meter" if k == 1 else ""
        return mcq(q, num(s) + unitw, [num(x) + unitw for x in (nocarry(a, b), s + 10, a - b if a > b else b - a)],
                   "%s + %s = <b>%s</b>%s." % (num(a), num(b), num(s), unitw))

    def ruta():
        a, b = pair(ch([0, 1]))
        s = a + b
        pos = ri(0, 2)
        d = int(str(b)[pos])
        bs = str(b)[:pos] + "□" + str(b)[pos + 1:]
        w = [(d + 1) % 10, (d + 9) % 10, (d + 2) % 10, (10 - d) % 10]
        return mcq("Vilken siffra ska stå i rutan? %s + %s = %s" % (num(a), bs, num(s)), str(d), [str(x) for x in w if x != d],
                   "Räkna %s − %s = %s. Siffran i rutan är <b>%d</b>." % (num(s), num(a), num(b), d))

    def tre():
        xs = [ri(101, 299), ri(101, 299), ri(11, 299)]
        s = sum(xs)
        if s > 999:
            return None
        return mcq("%s + %s + %s = ?" % tuple(num(x) for x in xs), num(s), [num(s + 10), num(s - 100), num(s - 10)],
                   "Ställ upp alla tre talen och addera ental, tiotal och hundratal. Svar: <b>%s</b>." % num(s))

    sets = [("Uppställning utan växling", [(lambda: (lambda a, b: mcq("%s + %s = ?" % (num(a), num(b)), num(a + b), [num(a + b + 10), num(a + b + 100), num(a + b - 1)],
                                                                         "Addera ental, tiotal och hundratal var för sig: <b>%s</b>." % num(a + b)))(*pair(0)), 20)]),
            ("Med minnessiffra", [(bild, 14), (minne, 6)]),
            ("Räkna med uppställning", [(ber, 16), (tre, 4)]),
            ("Siffran i rutan", [(ruta, 20)]),
            ("Textuppgifter", [(text_, 20)])]
    return unit("addition-med-uppstallning", "T", 5, "Addition med uppställning och minnessiffra", "Addition med uppställning",
                "Metoder för beräkningar med naturliga tal vid skriftliga metoder. Addition med tal upp till 1 000 och växling.",
                "Arbetsblad om addition med uppställning för årskurs 3: addition utan och med växling, minnessiffra, saknad siffra och textuppgifter. 100 uppgifter med facit.",
                "Ental under ental", "Blir det 10 eller mer skriver du en minnessiffra.", sets,
                ["Ställ upp talen så att ental står under ental, tiotal under tiotal och hundratal under hundratal.",
                 "Börja alltid med entalen. Blir summan 10 eller mer växlar du 10 ental mot 1 tiotal och skriver 1 som minnessiffra ovanför tiotalen.",
                 "Gör samma sak med tiotalen. Kontrollera med ett överslag: 378 + 245 är ungefär 400 + 200 = 600."],
                [("378 + 245", ["Ental: 8 + 5 = 13, skriv 3, minnessiffra 1", "Tiotal: 7 + 4 + 1 = 12, skriv 2, minnessiffra 1", "Hundratal: 3 + 2 + 1 = 6"], "623"),
                 ("406 + 352", ["6 + 2 = 8", "0 + 5 = 5", "4 + 3 = 7"], "758")],
                [["378 + 245 = 513 (glömmer minnessiffrorna)", "Minnessiffran räknas med: 623"], ["Skriver 13 under entalen", "Skriv 3 och lägg 1 som minnessiffra"],
                 ["Ställer 45 under 378 fel: 4 under 3", "Ental under ental: 5 under 8"]],
                [("Vad är en minnessiffra?", "När entalen blir 10 eller mer växlar du 10 ental mot 1 tiotal. Ettan skrivs ovanför tiotalen så att du minns den."),
                 ("Måste jag börja med entalen?", "Ja. Annars vet du inte om du får en minnessiffra till tiotalen."),
                 ("Hur kontrollerar jag svaret?", "Gör ett överslag, eller räkna subtraktion baklänges: 623 − 245 = 378.")])


# ============================================================ 6. Subtraktion med uppställning
def u6():
    def pair(borrow):
        while True:
            a = ri(201, 999)
            b = ri(101, a - 50) if a > 160 else 0
            if not b:
                continue
            b1 = a % 10 < b % 10
            b2 = a // 10 % 10 - (1 if b1 else 0) < b // 10 % 10
            if b1 + b2 == borrow:
                return a, b

    def smallbig(a, b):
        """vanligt fel: tar minsta från största i varje kolumn"""
        r, p = 0, 1
        x, y = a, b
        while x or y:
            r += abs(x % 10 - y % 10) * p
            x //= 10
            y //= 10
            p *= 10
        return r

    def utan():
        a, b = pair(0)
        return mcq("%s − %s = ?" % (num(a), num(b)), num(a - b), [num(a - b + 10), num(a - b - 100) if a - b > 100 else num(a - b + 100), num(a + b) if a + b < 1000 else num(a - b + 1)],
                   "Subtrahera ental, tiotal och hundratal var för sig: <b>%s</b>." % num(a - b))

    def ber():
        a, b = pair(ch([1, 1, 2]))
        d = a - b
        return mcq("Räkna med uppställning: %s − %s = ?" % (num(a), num(b)), num(d), [num(x) for x in (smallbig(a, b), d + 10, d - 10, d + 100) if x != d],
                   "Räcker inte entalen växlar du 1 tiotal till 10 ental. Svar: <b>%s</b>." % num(d))

    def bild():
        a, b = pair(ch([1, 2]))
        d = a - b
        pic = uppstallning([str(a), str(b)], "−")
        return mcq(pic + "Vad blir skillnaden?", num(d), [num(x) for x in (smallbig(a, b), d + 100, d + 10) if x != d],
                   "Kontrollera med addition: %s + %s = %s. Svar: <b>%s</b>." % (num(d), num(b), num(a), num(d)))

    def vaxla():
        a, b = pair(ch([1, 2]))
        if a % 10 >= b % 10:
            return None
        t = a // 10 % 10
        if t == 0:
            return None
        return mcq("Du räknar %s − %s. %d − %d går inte. Vad gör du?" % (num(a), num(b), a % 10, b % 10),
                   "Växlar 1 tiotal till 10 ental: %d − %d = %d" % (a % 10 + 10, b % 10, a % 10 + 10 - b % 10),
                   ["Räknar %d − %d = %d i stället" % (b % 10, a % 10, b % 10 - a % 10), "Skriver 0 och går vidare", "Växlar 1 hundratal till 10 ental: %d − %d" % (a % 10 + 10, b % 10) if False else "Lägger till 10 på svaret"],
                   "Ta ett tiotal och växla det till 10 ental. Då har du %d ental: %d − %d = %d. Tiotalssiffran blir %d." % (a % 10 + 10, a % 10 + 10, b % 10, a % 10 + 10 - b % 10, t - 1))

    def noll():
        h = ri(3, 9)
        a = h * 100 + ch([0, 0, 1, 2, 4, 5])
        b = ri(101, a - 50)
        if b % 10 <= a % 10 or b // 10 % 10 == 0:
            return None
        d = a - b
        return mcq("%s − %s = ?" % (num(a), num(b)), num(d), [num(x) for x in (smallbig(a, b), d + 100, d - 10 if d > 10 else d + 20) if x != d],
                   "Det finns inga tiotal att växla. Växla 1 hundratal till 10 tiotal och sedan 1 tiotal till 10 ental. Svar: <b>%s</b>." % num(d))

    def text_():
        n = K.name()
        a, b = pair(ch([1, 1, 2]))
        d = a - b
        k = ri(0, 2)
        if k == 0:
            q = "%s har %s. %s köper en cykelhjälm för %s. Hur mycket pengar har %s kvar?" % (n, kr(a), n, kr(b), n)
            unitf = kr
        elif k == 1:
            q = "Ett tåg har %s platser. %s platser är upptagna. Hur många platser är lediga?" % (num(a), num(b))
            unitf = num
        else:
            q = "Klassen vill samla %s burkar till pant. De har samlat %s burkar. Hur många burkar fattas?" % (num(a), num(b))
            unitf = num
        return mcq(q, unitf(d), [unitf(x) for x in (smallbig(a, b), d + 10, a + b if a + b < 1000 else d + 100) if x != d],
                   "%s − %s = <b>%s</b>." % (num(a), num(b), unitf(d)))

    def kontroll():
        a, b = pair(ch([1, 2]))
        d = a - b
        return mcq("%s − %s = %s. Vilken addition kan du använda för att kontrollera svaret?" % (num(a), num(b), num(d)),
                   "%s + %s = %s" % (num(d), num(b), num(a)), ["%s + %s = %s" % (num(a), num(b), num(a + b)) if a + b < 1000 else "%s + %s" % (num(a), num(d)),
                                                             "%s − %s = %s" % (num(a), num(d), num(b)), "%s + %s" % (num(d), num(a))],
                   "Skillnaden plus det du tog bort ska bli talet du började med: <b>%s + %s = %s</b>." % (num(d), num(b), num(a)))

    sets = [("Utan växling", [(utan, 20)]),
            ("Växla tiotal", [(vaxla, 8), (bild, 12)]),
            ("Räkna med uppställning", [(ber, 20)]),
            ("Nollor och kontroll", [(noll, 12), (kontroll, 8)]),
            ("Textuppgifter", [(text_, 20)])]
    return unit("subtraktion-med-uppstallning", "T", 6, "Subtraktion med uppställning och växling", "Subtraktion med uppställning",
                "Metoder för beräkningar med naturliga tal vid skriftliga metoder. Subtraktion med tal upp till 1 000, växling och kontroll med addition.",
                "Arbetsblad om subtraktion med uppställning för årskurs 3: subtraktion utan och med växling, nollor i talet, kontroll med addition och textuppgifter. 100 uppgifter med facit.",
                "Växla när det inte räcker", "1 tiotal blir 10 ental, 1 hundratal blir 10 tiotal.", sets,
                ["Ställ upp talen med ental under ental. Det största talet står överst.",
                 "Börja med entalen. Räcker inte entalen växlar du 1 tiotal till 10 ental. Stryk över tiotalssiffran och skriv en siffra mindre.",
                 "Kontrollera med addition: skillnaden + det du tog bort = talet du började med."],
                [("652 − 278", ["2 − 8 går inte: växla, 12 − 8 = 4", "4 − 7 går inte: växla, 14 − 7 = 7", "5 − 2 = 3"], "374"),
                 ("500 − 136", ["Växla 1 hundratal till 10 tiotal", "Växla 1 tiotal till 10 ental: 10 − 6 = 4", "9 − 3 = 6, 4 − 1 = 3"], "364")],
                [["652 − 278 = 426 (8 − 2 i stället för 2 − 8)", "Växla: 12 − 8 = 4. Svar 374"], ["Glömmer att tiotalssiffran blir en mindre", "Stryk och skriv en mindre efter växlingen"],
                 ["Ställer det mindre talet överst", "Det tal du tar bort från står överst"]],
                [("Vad betyder att växla?", "Du byter 1 tiotal mot 10 ental (eller 1 hundratal mot 10 tiotal). Talets värde är detsamma."),
                 ("Vad gör jag om det står en nolla?", "Växla från nästa plats: 1 hundratal blir 10 tiotal, och sedan 1 tiotal till 10 ental."),
                 ("Hur vet jag att svaret är rätt?", "Lägg ihop svaret och talet du tog bort. Då ska du få det första talet.")])


# ============================================================ 7. Multiplikation och tabellerna
def dots(rows, cols, col="#e07a5f"):
    s = []
    for r in range(rows):
        for c in range(cols):
            s.append("<circle cx='%d' cy='%d' r='8' fill='%s' stroke='%s' stroke-width='1'/>" % (16 + c * 24, 16 + r * 24, col, INK))
    return wrap(cols * 24 + 10, rows * 24 + 10, "".join(s), "%d rader med %d prickar" % (rows, cols))


def groups(g, n):
    s = []
    for i in range(g):
        x0 = 6 + i * 74
        s.append("<rect x='%d' y='6' width='66' height='66' rx='10' fill='#f7f3e3' stroke='%s' stroke-width='1.5'/>" % (x0, INK))
        for j in range(n):
            s.append("<circle cx='%d' cy='%d' r='6' fill='#6a9fd4' stroke='%s'/>" % (x0 + 13 + (j % 4) * 13, 19 + (j // 4) * 14, INK))
    return wrap(g * 74 + 8, 78, "".join(s), "%d grupper med %d i varje" % (g, n))


def u7():
    def tabell():
        a = ch([2, 3, 4, 5, 10, 2, 3, 4, 5, 6, 7, 8, 9])
        b = ri(1, 10)
        p = a * b
        return mcq("%d × %d = ?" % (b, a), str(p), [str(p + a), str(p - a) if p > a else str(p + 2 * a), str(a + b), str(p + 1)],
                   "%d gånger %d är <b>%d</b>." % (b, a, p))

    def grupper():
        g, n = ri(2, 5), ri(2, 8)
        return mcq(groups(g, n) + "Hur många prickar finns det? Vilken multiplikation passar?", "%d × %d = %d" % (g, n, g * n),
                   ["%d + %d = %d" % (g, n, g + n), "%d × %d = %d" % (g, n, g * n + n), "%d × %d = %d" % (g, g, g * g) if g != n else "%d × %d = %d" % (g, n + 1, g * (n + 1))],
                   "%d grupper med %d i varje: %d × %d = <b>%d</b>." % (g, n, g, n, g * n))

    def rader():
        r, c = ri(2, 6), ri(3, 8)
        if r == c:
            return None
        return mcq(dots(r, c) + "Hur många prickar är det?", str(r * c), [str(r + c), str(r * c + c), str(r * c - r)],
                   "%d rader med %d prickar: %d × %d = <b>%d</b>." % (r, c, r, c, r * c))

    def upprepad():
        a, b = ri(2, 6), ri(3, 9)
        s = " + ".join([str(b)] * a)
        return mcq("Vilken multiplikation är samma som %s?" % s, "%d × %d" % (a, b), ["%d × %d" % (a, a), "%d + %d" % (a, b), "%d × %d" % (b, b), "%d × %d" % (a + 1, b)],
                   "%d står %d gånger: <b>%d × %d</b> = %d." % (b, a, a, b, a * b))

    def kommutativ():
        a, b = ri(2, 9), ri(2, 9)
        if a == b:
            return None
        return mcq("%d × %d = %d. Vad är då %d × %d?" % (a, b, a * b, b, a), str(a * b), [str(a * b + a), str(a + b), str(a * b - b)],
                   "Ordningen spelar ingen roll i multiplikation: %d × %d = %d × %d = <b>%d</b>." % (a, b, b, a, a * b))

    def saknas():
        a = ch([2, 3, 4, 5, 6, 10])
        b = ri(2, 10)
        return mcq("? × %d = %d" % (a, a * b), str(b), [str(b + 1), str(b - 1), str(a * b - a), str(a)],
                   "Vilket tal gånger %d blir %d? %d × %d = %d. Svar: <b>%d</b>." % (a, a * b, b, a, a * b, b))

    def text_():
        n = K.name()
        k = ri(0, 3)
        if k == 0:
            g, m = ri(3, 8), ch([4, 5, 6])
            q, ans, e = "%s köper %d paket med %d bullar i varje. Hur många bullar blir det?" % (n, g, m), g * m, "%d × %d = <b>%d</b>." % (g, m, g * m)
        elif k == 1:
            g = ri(3, 9)
            q, ans, e = "En cykel har 2 hjul. Hur många hjul har %d cyklar?" % g, 2 * g, "%d × 2 = <b>%d</b>." % (g, 2 * g)
        elif k == 2:
            g = ri(2, 9)
            q, ans, e = "En spindel har 8 ben. Hur många ben har %d spindlar?" % g, 8 * g, "%d × 8 = <b>%d</b>." % (g, 8 * g)
        else:
            g, p = ri(2, 6), ch([5, 10])
            q, ans, e = "En glass kostar %s. %s köper %d glassar. Hur mycket kostar det?" % (kr(p), n, g), g * p, "%d × %d = <b>%d</b> kr." % (g, p, g * p)
            return mcq(q, kr(ans), [kr(ans + p), kr(g + p), kr(ans - p)], e)
        return mcq(q, str(ans), [str(ans + 2), str(ans - 2) if ans > 4 else str(ans + 4), str(ans + ans // max(g, 1)), str(g + ans // g)], e)

    sets = [("Lika stora grupper", [(grupper, 10), (upprepad, 10)]),
            ("Rader och kolumner", [(rader, 14), (kommutativ, 6)]),
            ("Tabellerna 2, 3, 4, 5 och 10", [(lambda: (lambda a, b: mcq("%d × %d = ?" % (b, a), str(a * b), [str(a * b + a), str(a + b), str(a * b - 1), str(a * b - a) if a * b > a else str(a * b + 2)],
                                                                         "%d × %d = <b>%d</b>." % (b, a, a * b)))(ch([2, 3, 4, 5, 10]), ri(2, 10)), 20)]),
            ("Hela tabellen och saknat tal", [(tabell, 12), (saknas, 8)]),
            ("Textuppgifter", [(text_, 20)])]
    return unit("multiplikation-och-tabellerna", "T", 7, "Multiplikation: lika stora grupper och tabellerna", "Multiplikation",
                "De fyra räknesättens egenskaper och samband. Multiplikation som upprepad addition och lika stora grupper. Multiplikationstabellerna.",
                "Arbetsblad om multiplikation för årskurs 3: lika stora grupper, upprepad addition, rader och kolumner, tabellerna 2–10 och textuppgifter. 100 uppgifter med facit.",
                "Lika stora grupper", "4 × 3 = 3 + 3 + 3 + 3", sets,
                ["Multiplikation är upprepad addition med lika stora grupper. 4 × 3 betyder 4 grupper med 3 i varje: 3 + 3 + 3 + 3 = 12.",
                 "Ordningen spelar ingen roll: 4 × 3 = 3 × 4. Kan du den ena vet du den andra.",
                 "Lär dig tabellerna. 2-tabellen är dubbelt, 4-tabellen är dubbelt av dubbelt, 5-tabellen slutar på 0 eller 5 och 10-tabellen slutar på 0."],
                [("4 × 3", ["3 + 3 + 3 + 3"], "12"), ("6 × 5", ["5-tabellen: 5, 10, 15, 20, 25, 30"], "30")],
                [["4 × 3 = 7 (adderar i stället)", "4 grupper med 3: 12"], ["6 × 5 = 35", "Räkna i 5-tabellen: 30"],
                 ["Tror att 3 × 8 och 8 × 3 är olika", "Båda blir 24"]],
                [("Vilken tabell ska jag lära mig först?", "Börja med 2, 5 och 10. Sedan 4 (dubbelt av 2) och 3."),
                 ("Vad betyder tecknet ×?", "Det betyder gånger. 4 × 3 läses fyra gånger tre."),
                 ("Hur kan jag räkna 9 × 6?", "10 × 6 = 60, och ta bort en sexa: 60 − 6 = 54.")])


# ============================================================ 8. Division
def u8():
    def dela():
        n, g = ri(2, 10), ch([2, 3, 4, 5])
        t = n * g
        name = K.name()
        return mcq("%s delar %d kulor lika mellan %d kompisar. Hur många kulor får var och en?" % (name, t, g), str(n), [str(t - g), str(n + 1), str(g), str(n - 1) if n > 2 else str(n + 2)],
                   "%d : %d = <b>%d</b>, eftersom %d × %d = %d." % (t, g, n, g, n, t))

    def innehall():
        g, n = ri(2, 9), ch([2, 3, 4, 5, 6])
        t = g * n
        return mcq("%d ägg läggs i kartonger med %d ägg i varje. Hur många kartonger behövs?" % (t, n), str(g), [str(g + 1), str(t - n), str(n)] if g != n else [str(g + 1), str(t - n), str(g - 1)],
                   "Hur många %d:or ryms i %d? %d : %d = <b>%d</b>." % (n, t, t, n, g))

    def tab():
        a = ch([2, 3, 4, 5, 10, 6, 7, 8, 9])
        b = ri(1, 10)
        return mcq("%d : %d = ?" % (a * b, a), str(b), [str(b + 1), str(b - 1) if b > 1 else str(b + 2), str(a * b - a), str(a)],
                   "%d × %d = %d, alltså %d : %d = <b>%d</b>." % (b, a, a * b, a * b, a, b))

    def samband():
        a, b = ri(2, 9), ri(2, 9)
        if a == b:
            return None
        p = a * b
        return mcq("%d × %d = %d. Vilken division hör ihop med den?" % (a, b, p), "%d : %d = %d" % (p, a, b),
                   ["%d : %d = %d" % (p, a, a), "%d : %d = %d" % (a, b, p), "%d : %d = %d" % (p, b, b)],
                   "Multiplikation och division hör ihop: %d : %d = %d och %d : %d = %d." % (p, a, b, p, b, a))

    def rest():
        d = ch([2, 3, 4, 5])
        q = ri(2, 9)
        r = ri(1, d - 1)
        t = d * q + r
        return mcq("%d : %d = ?" % (t, d), "%d rest %d" % (q, r), ["%d rest %d" % (q + 1, r), "%d rest %d" % (q, r + d) if r + d < 10 else "%d" % q, "%d rest %d" % (q - 1, r + d)],
                   "%d × %d = %d och %d kvar. Svar: <b>%d rest %d</b>." % (d, q, d * q, r, q, r))

    def rest_text():
        n = K.name()
        d, q = ch([3, 4, 5]), ri(3, 8)
        r = ri(1, d - 1)
        t = d * q + r
        return mcq("%s har %d pepparkakor och lägger %d på varje fat. Hur många fat blir fulla och hur många pepparkakor blir över?" % (n, t, d),
                   "%d fat, %d över" % (q, r), ["%d fat, %d över" % (q + 1, 0), "%d fat, %d över" % (q, d - r) if d - r != r else "%d fat, %d över" % (q - 1, r + d), "%d fat, %d över" % (q - 1, r)],
                   "%d : %d = %d rest %d. <b>%d fulla fat och %d över</b>." % (t, d, q, r, q, r))

    def bild():
        g, n = ri(2, 4), ri(2, 6)
        return mcq(groups(g, n) + "%d prickar delas i %d lika stora grupper. Vilken division visar bilden?" % (g * n, g), "%d : %d = %d" % (g * n, g, n),
                   ["%d : %d = %d" % (g * n, n, n), "%d − %d = %d" % (g * n, g, g * n - g), "%d × %d = %d" % (g, n, g * n)] if g != n else ["%d − %d = %d" % (g * n, g, g * n - g), "%d × %d = %d" % (g, n, g * n), "%d : %d = %d" % (g * n, g, n + 1)],
                   "%d delat i %d grupper ger %d i varje: <b>%d : %d = %d</b>." % (g * n, g, n, g * n, g, n))

    sets = [("Dela lika", [(dela, 14), (bild, 6)]),
            ("Hur många grupper?", [(innehall, 20)]),
            ("Division och multiplikation", [(tab, 12), (samband, 8)]),
            ("Division med rest", [(rest, 20)]),
            ("Textuppgifter", [(rest_text, 10), (dela, 5), (innehall, 5)])]
    return unit("division", "T", 8, "Division: dela lika och division med rest", "Division",
                "De fyra räknesättens egenskaper och samband. Division som delning och innehållsdivision, sambandet med multiplikation och division med rest.",
                "Arbetsblad om division för årskurs 3: dela lika, hur många grupper, sambandet mellan multiplikation och division, division med rest och textuppgifter. 100 uppgifter med facit.",
                "Dela i lika stora delar", "12 : 3 = 4 eftersom 3 × 4 = 12", sets,
                ["Division betyder att dela lika. 12 : 3 kan betyda 12 delat på 3 personer (4 var) eller hur många 3:or det finns i 12 (4 stycken).",
                 "Division är multiplikation baklänges. Kan du 3 × 4 = 12 vet du att 12 : 3 = 4 och 12 : 4 = 3.",
                 "Ibland går det inte jämnt ut. 14 : 4 = 3 rest 2, eftersom 3 × 4 = 12 och det blir 2 över. Resten är alltid mindre än talet du delar med."],
                [("15 : 3", ["3 × 5 = 15"], "5"), ("17 : 5", ["5 × 3 = 15", "17 − 15 = 2"], "3 rest 2")],
                [["15 : 3 = 12 (subtraherar)", "Hur många 3:or i 15? 5"], ["17 : 5 = 2 rest 7", "Resten måste vara mindre än 5: 3 rest 2"],
                 ["Tror att 12 : 3 och 3 : 12 är samma sak", "Ordningen spelar roll i division"]],
                [("Vad betyder tecknet : ?", "Det betyder delat med. 12 : 3 läses tolv delat med tre."),
                 ("Vad är en rest?", "Det som blir över när det inte går jämnt ut."),
                 ("Hur kontrollerar jag en division?", "Multiplicera svaret med talet du delade med och lägg till resten. 3 × 5 + 2 = 17.")])


# ============================================================ 9. Problemlösning
def u9():
    def tvasteg():
        n, g = K.next()
        k = ri(0, 3)
        if k == 0:
            a, b, c = ri(30, 80), ri(10, 30), ri(5, 25)
            if a - b - c <= 0:
                return None
            return mcq("%s har %d kr. %s köper en tidning för %d kr och en glass för %d kr. Hur mycket har %s kvar?" % (n, a, Hon(g), b, c, hon(g)),
                       kr(a - b - c), [kr(a - b), kr(a - b + c), kr(b + c)], "%d − %d − %d = <b>%d kr</b>." % (a, b, c, a - b - c))
        if k == 1:
            p, m, extra = ri(3, 6), ch([4, 5, 6]), ri(2, 9)
            return mcq("I en klass sitter eleverna vid %d bord med %d elever vid varje bord. %d elever sitter i soffan. Hur många elever är det?" % (p, m, extra),
                       str(p * m + extra), [str(p * m), str(p + m + extra), str(p * m - extra)], "%d × %d + %d = <b>%d</b>." % (p, m, extra, p * m + extra))
        if k == 2:
            a = ri(12, 40)
            b = a + ri(5, 20)
            return mcq("Maja har %d kort. Olle har %d fler kort än Maja. Hur många kort har de tillsammans?" % (a, b - a),
                       str(a + b), [str(b), str(a + b - a), str(2 * a)] if b != 2 * a else [str(b), str(a + b + 1), str(a + b - 1)],
                       "Olle har %d + %d = %d kort. Tillsammans %d + %d = <b>%d</b>." % (a, b - a, b, a, b, a + b))
        x, y = ri(2, 6), ch([10, 20])
        z = ri(3, 9)
        return mcq("%s köper %d böcker för %d kr styck och en penna för %d kr. Vad kostar det?" % (n, x, y, z), kr(x * y + z), [kr(x * y), kr(x + y + z), kr(y + z)],
                   "%d × %d + %d = <b>%d kr</b>." % (x, y, z, x * y + z))

    def jamfor():
        a, b = K.two()
        x, y = ri(20, 90), ri(20, 90)
        if x == y:
            return None
        big, sm = max(x, y), min(x, y)
        w = a if x > y else b
        return mcq("%s har %d pärlor och %s har %d pärlor. Hur många fler pärlor har %s?" % (a, x, b, y, w), str(big - sm), [str(x + y), str(big), str(big - sm + 10)],
                   "Skillnaden: %d − %d = <b>%d</b>." % (big, sm, big - sm))

    def baklanges():
        n, g = K.next()
        start = ri(20, 60)
        f, s = ri(5, 20), ri(5, 20)
        end = start + f - s
        if end <= 0:
            return None
        return mcq("%s hade några kulor. %s vann %d kulor och förlorade sedan %d. Nu har %s %d kulor. Hur många hade %s från början?" % (n, Hon(g), f, s, hon(g), end, hon(g)),
                   str(start), [str(end + f + s), str(end - f + s + 2 * f), str(end)] if end + f + s != start else [str(start + 2), str(end), str(start - 2)],
                   "Räkna baklänges: %d + %d − %d = <b>%d</b>." % (end, s, f, start))

    def system():
        k = ri(0, 2)
        if k == 0:
            m, c = ri(2, 4), ri(2, 4)
            return mcq("Du har %d olika tröjor och %d olika byxor. Hur många olika sätt kan du klä dig på?" % (m, c), str(m * c), [str(m + c), str(m * c + 1), str(m * c - 1)],
                       "Varje tröja kan kombineras med varje byxa: %d × %d = <b>%d</b>." % (m, c, m * c))
        if k == 1:
            h = ri(3, 8)
            return mcq("På en gård finns hönor och kor. Det finns %d djur och %d ben. Hur många kor finns det?" % (h + 2, 2 * h + 8), "2", ["%d" % h, "4", "%d" % (h + 2)],
                       "Om alla vore hönor blir det %d ben. Varje ko har 2 ben extra. %d − %d = 4 extra ben, alltså <b>2 kor</b>." % (2 * (h + 2), 2 * h + 8, 2 * (h + 2)))
        t = ri(3, 7)
        return mcq("%d barn hälsar på varandra. Alla tar alla i hand en gång. Hur många handslag blir det?" % t, str(t * (t - 1) // 2), [str(t * (t - 1)), str(t), str(t * (t - 1) // 2 + 1)],
                   "Den första hälsar på %d, nästa på %d och så vidare: %s = <b>%d</b>." % (t - 1, t - 2, " + ".join(str(i) for i in range(t - 1, 0, -1)), t * (t - 1) // 2))

    def fraga():
        n = K.name()
        p, s = ri(25, 60), ri(10, 30)
        opts = [("Hur mycket kostar det tillsammans?", "addition"), ("Hur mycket dyrare är bollen?", "subtraktion")]
        qq, ans = ch(opts)
        return mcq("En boll kostar %d kr och en kortlek kostar %d kr. Frågan är: <i>%s</i> Vilket räknesätt passar?" % (p, s, qq), ans,
                   [x for x in ("addition", "subtraktion", "multiplikation", "division") if x != ans],
                   "%s → <b>%s</b>." % ("Tillsammans betyder att lägga ihop" if ans == "addition" else "Hur mycket dyrare betyder skillnaden", ans))

    def tabellprob():
        d, m = ri(2, 9), ch([3, 4, 5, 10])
        return mcq("En kanelbulle kostar %d kr. Vad kostar %d kanelbullar?" % (d, m), kr(m * d), [kr(d + m), kr(m * d + d), kr(m * d - d)],
                   "%d × %d = <b>%d kr</b>." % (m, d, m * d))

    sets = [("Problem i två steg", [(tvasteg, 20)]),
            ("Jämför och hitta skillnaden", [(jamfor, 14), (tabellprob, 6)]),
            ("Räkna baklänges", [(baklanges, 20)]),
            ("Välj räknesätt", [(fraga, 8), (tvasteg, 12)]),
            ("Tänk systematiskt", [(system, 14), (jamfor, 6)])]
    return unit("problemlosning", "P", 9, "Problemlösning: textuppgifter och strategier", "Problemlösning",
                "Strategier för matematisk problemlösning i enkla situationer. Matematisk formulering av frågeställningar utifrån vardagliga situationer.",
                "Arbetsblad om problemlösning för årskurs 3: problem i två steg, hitta skillnaden, räkna baklänges, välj räknesätt och tänk systematiskt. 100 uppgifter med facit.",
                "Läs, rita, räkna, svara", "Vad vet du? Vad ska du ta reda på?", sets,
                ["Läs uppgiften två gånger. Vad vet du och vad ska du ta reda på?",
                 "Rita en bild eller skriv upp talen. Bestäm vilket räknesätt som passar. Ibland behöver du räkna i två steg.",
                 "Kontrollera om svaret är rimligt och svara med en hel mening."],
                [("Ali har 45 kr. Han köper en glass för 18 kr och en dricka för 12 kr. Hur mycket har han kvar?", ["45 − 18 = 27", "27 − 12 = 15"], "15 kr"),
                 ("3 tröjor och 2 byxor. Hur många olika sätt att klä sig?", ["Varje tröja med varje byxa", "3 × 2"], "6")],
                [["Räknar bara första steget", "Läs frågan igen. Två köp ska båda dras bort"], ["Hur många fler? Adderar talen", "Fler betyder skillnaden: subtrahera"],
                 ["Svarar utan enhet", "Skriv enheten: 15 kr"]],
                [("Hur vet jag vilket räknesätt jag ska välja?", "Tillsammans och fler till: addition. Kvar och skillnad: subtraktion. Lika många i varje grupp: multiplikation eller division."),
                 ("Vad betyder att räkna baklänges?", "Du börjar med slutet och gör det omvända: det som lades till drar du bort."),
                 ("Får jag rita?", "Ja. En bild hjälper dig att förstå uppgiften.")])


# ============================================================ 10. Enkla bråk
NAMN = {2: "en halv", 3: "en tredjedel", 4: "en fjärdedel", 5: "en femtedel", 6: "en sjättedel", 8: "en åttondel", 10: "en tiondel"}
PL = {2: "halvor", 3: "tredjedelar", 4: "fjärdedelar", 5: "femtedelar", 6: "sjättedelar", 8: "åttondelar", 10: "tiondelar"}
SG = {2: "halv", 3: "tredjedel", 4: "fjärdedel", 5: "femtedel", 6: "sjättedel", 8: "åttondel", 10: "tiondel"}
TAL = {1: "en", 2: "två", 3: "tre", 4: "fyra", 5: "fem", 6: "sex", 7: "sju", 8: "åtta", 9: "nio"}


def bnamn(a, b):
    if a == 1:
        return NAMN[b]
    return "%s %s" % (TAL[a], PL[b])


def bar_frac(n, k, w=300, h=40, col="#7fb3d5"):
    s = []
    cw = w / float(n)
    for i in range(n):
        s.append("<rect x='%.1f' y='6' width='%.1f' height='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (6 + i * cw, cw, h, col if i < k else "#ffffff", INK))
    return wrap(w + 12, h + 12, "".join(s), "remsa i %d lika delar, %d färgade" % (n, k))


def pie(n, k, r=58, col="#f4a261"):
    cx = cy = r + 6
    s = []
    for i in range(n):
        a0 = -math.pi / 2 + 2 * math.pi * i / n
        a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>"
                 % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r, cx + r * math.cos(a1), cy + r * math.sin(a1), col if i < k else "#ffffff", INK))
    return wrap(2 * r + 12, 2 * r + 12, "".join(s), "cirkel i %d lika delar, %d färgade" % (n, k))


def u10():
    def bild():
        n = ch([2, 3, 4, 5, 6, 8, 10])
        k = ri(1, n - 1)
        pic = pie(n, k) if R.random() < 0.5 else bar_frac(n, k)
        return mcq(pic + "Hur stor del är färgad?", fr(k, n), [fr(n - k, n) if n - k != k else fr(k, n + 1), fr(k, n - k) if n - k != k else fr(k + 1, n), fr(n, k) if n != k else fr(1, n)],
                   "Figuren har %d lika stora delar. %d är färgade: <b>%s</b>." % (n, k, bnamn(k, n)))

    def namn():
        n = ch([2, 3, 4, 5, 6, 8, 10])
        k = ri(1, min(n - 1, 9))
        return mcq("Hur skrivs %s som bråk?" % bnamn(k, n), fr(k, n), [fr(n, k), fr(k, n + 1), fr(k + 1, n) if k + 1 < n else fr(1, n + 2)],
                   "Nämnaren (under strecket) visar hur många delar det helt har: %d. Täljaren visar hur många delar: %d." % (n, k))

    def antal():
        n = ch([2, 3, 4, 5, 10])
        m = ri(2, 6) if n != 10 else ri(1, 3)
        t = n * m
        thing = ch(["äpplen", "kulor", "bullar", "pennor", "kakor"])
        return mcq(("Vad är hälften av %d %s?" % (t, thing)) if n == 2 else ("Vad är %s av %d %s?" % (NAMN[n], t, thing)), "%d %s" % (m, thing), ["%d %s" % (x, thing) for x in (t - n, m + 1, n) if x != m and x > 0],
                   "Dela %d i %d lika delar: %d : %d = <b>%d</b>." % (t, n, t, n, m))

    def jamfor():
        a, b = sh([2, 3, 4, 5, 6, 8, 10])[:2]
        big = min(a, b)
        return mcq("Vilket är störst, %s eller %s?" % (fr(1, a), fr(1, b)), fr(1, big), [fr(1, max(a, b)), "De är lika stora", "Det går inte att jämföra"],
                   "Ju fler delar det helt delas i, desto mindre blir varje del. %s är större än %s." % (fr(1, big), fr(1, max(a, b))))

    def hel():
        n = ch([2, 3, 4, 5, 6, 8, 10])
        return mcq("Hur många %s behövs för att få en hel?" % PL[n], str(n), [str(n - 1), str(n + 1), str(2 * n)],
                   "%s = 1. Det behövs <b>%d</b> %s." % (fr(n, n), n, PL[n]))

    def lika():
        n = ch([3, 4, 5, 6])
        k = ri(1, n - 1)
        # två bilder: lika delar eller inte
        good = bar_frac(n, k)
        return mcq(good + "Figuren är delad i %d lika stora delar. Hur stor del är <b>inte</b> färgad?" % n, fr(n - k, n),
                   [fr(k, n), fr(n - k, k) if n - k != k else fr(1, n + 1), fr(n, n - k) if n != n - k else fr(1, n)],
                   "%d av %d delar är vita: <b>%s</b>." % (n - k, n, bnamn(n - k, n)))

    def text_():
        n, g = K.next()
        p = ch([2, 3, 4])
        t = ch([x for x in (6, 8, 12, 16, 20, 24) if x % p == 0])
        sak, best, bit = ch([("en pizza", "pizzan", "bitar"), ("en tårta", "tårtan", "bitar"), ("en chokladkaka", "chokladkakan", "rutor"), ("ett bröd", "brödet", "skivor")])
        del_ = ("halva " + best) if p == 2 else ("%s av %s" % (NAMN[p], best))
        return mcq("%s är delad i %d lika stora %s. %s äter %s. Hur många %s äter %s?" % (cap(sak), t, bit, n, del_, bit, hon(g)), str(t // p),
                   [str(p), str(t - t // p), str(t // p + 1)], "%d : %d = <b>%d</b>." % (t, p, t // p))

    sets = [("Färgad del", [(bild, 20)]),
            ("Skriva bråk", [(namn, 14), (hel, 6)]),
            ("Del av antal", [(antal, 14), (text_, 6)]),
            ("Jämföra stambråk", [(jamfor, 20)]),
            ("Blandat", [(lika, 8), (bild, 4), (antal, 4), (text_, 4)])]
    return unit("enkla-brak", "T", 10, "Enkla bråk: del av helhet och del av antal", "Enkla bråk",
                "Del av helhet och del av antal. Hur delarna kan benämnas och uttryckas som enkla bråk samt hur enkla bråk kan användas för att beskriva och jämföra tal.",
                "Arbetsblad om enkla bråk för årskurs 3: halv, tredjedel, fjärdedel och tiondel, färgad del, del av antal och att jämföra bråk. 100 uppgifter med facit.",
                "Lika stora delar", "Nämnaren visar hur många delar det helt har.", sets,
                ["Ett bråk visar en del av något som är delat i lika stora delar. I bråket 3/4 är 4 nämnaren (alla delar) och 3 täljaren (delarna vi tar).",
                 "Del av antal: en fjärdedel av 12 får du genom att dela 12 i 4 lika delar. 12 : 4 = 3.",
                 "Ju fler delar det helt delas i, desto mindre blir varje del. En halv är större än en fjärdedel."],
                [("En fjärdedel av 12", ["12 : 4 = 3"], "3"), ("Vilket är störst: en tredjedel eller en femtedel?", ["3 delar är större än 5 delar"], "en tredjedel")],
                [["En femtedel är större än en tredjedel eftersom 5 &gt; 3", "Fler delar ger mindre bitar: en tredjedel är större"],
                 ["Räknar delarna fast de inte är lika stora", "Bråk kräver lika stora delar"], ["En fjärdedel av 12 är 8", "12 : 4 = 3"]],
                [("Vad heter delarna i ett bråk?", "Talet över strecket heter täljare och talet under strecket heter nämnare."),
                 ("Är en halv alltid lika mycket?", "Nej, en halv pizza är mer än en halv kaka. Det beror på hur stort det hela är."),
                 ("Hur många fjärdedelar är en hel?", "Fyra fjärdedelar.")])


# ============================================================ 11. Likheter och likhetstecknet
def u11():
    def saknas_add():
        a, b = ri(5, 60), ri(5, 40)
        s = a + b
        if R.random() < 0.5:
            return mcq("%d + □ = %d. Vilket tal ska stå i rutan?" % (a, s), str(b), [str(s + a) if s + a < 200 else str(b + 2), str(b + 1), str(b - 1)],
                       "%d − %d = %d. Kontroll: %d + %d = %d." % (s, a, b, a, b, s))
        return mcq("□ + %d = %d. Vilket tal ska stå i rutan?" % (b, s), str(a), [str(s + b) if s + b < 200 else str(a + 2), str(a + 10), str(a - 1)],
                   "%d − %d = <b>%d</b>." % (s, b, a))

    def saknas_sub():
        a = ri(30, 99)
        b = ri(5, a - 5)
        d = a - b
        if R.random() < 0.5:
            return mcq("%d − □ = %d" % (a, d), str(b), [str(a + d) if a + d < 200 else str(b + 2), str(b + 1), str(d)] if d != b else [str(b + 1), str(b - 1), str(a)],
                       "Hur mycket ska tas bort från %d för att få %d? %d − %d = <b>%d</b>." % (a, d, a, d, b))
        return mcq("□ − %d = %d" % (b, d), str(a), [str(d - b) if d > b else str(a + 10), str(a + 1), str(a - 10)],
                   "Talet i rutan är %d + %d = <b>%d</b>." % (d, b, a))

    def balans():
        a, b, c = ri(2, 20), ri(2, 20), ri(2, 20)
        d = a + b - c
        if d <= 0 or d == c:
            return None
        return mcq("%d + %d = %d + □" % (a, b, c), str(d), [str(a + b), str(a + b + c), str(d + 1)],
                   "Vänster sida är %d. Höger sida måste också bli %d: %d + <b>%d</b> = %d." % (a + b, a + b, c, d, a + b))

    def sant():
        a, b = ri(2, 30), ri(2, 30)
        k = ri(0, 3)
        if k == 0:
            c = a + b
            st, ok = "%d + %d = %d" % (a, b, c), True
        elif k == 1:
            c, dd = ri(2, 30), 0
            d = a + b - c
            if d <= 0:
                return None
            ok = R.random() < 0.5
            if not ok:
                d += ch([1, -1, 2])
                if d <= 0:
                    return None
            st = "%d + %d = %d + %d" % (a, b, c, d)
        elif k == 2:
            st, ok = "%d = %d + %d" % (a + b, a, b), True
        else:
            st, ok = "%d + %d = %d + %d" % (a, b, a + b, ri(1, 9)), False
        return mcq("Är likheten sann eller falsk? <b>%s</b>" % st, "sann" if ok else "falsk", ["falsk" if ok else "sann", "Det går inte att veta", "Bara om man räknar från höger"],
                   "Räkna ut båda sidorna. Är de lika stora är likheten sann. Här är den <b>%s</b>." % ("sann" if ok else "falsk"))

    def betydelse():
        a, b = ri(3, 9), ri(3, 9)
        s = a + b
        return mcq("%d + %d = □ + 5. Vilket svar ger en sann likhet?" % (a, b), str(s - 5), [str(s), str(s + 5), str(s - 4)],
                   "Likhetstecknet betyder att båda sidorna är lika mycket. %d + %d = %d, och %d + 5 = %d. Svar: <b>%d</b>." % (a, b, s, s - 5, s, s - 5)) if s > 6 else None

    def mult():
        a = ch([2, 3, 4, 5, 10])
        b = ri(2, 10)
        if R.random() < 0.5:
            return mcq("%d × □ = %d" % (a, a * b), str(b), [str(a * b - a), str(b + 1), str(a)] if a != b else [str(b + 1), str(b - 1), str(a * b - a)],
                       "%d × %d = %d. Svar: <b>%d</b>." % (a, b, a * b, b))
        return mcq("%d : □ = %d" % (a * b, b), str(a), [str(a * b - b), str(a + 1), str(b * 2)] if a != b else [str(a + 1), str(a - 1), str(a * b - b)],
                   "%d : %d = %d. Svar: <b>%d</b>." % (a * b, a, b, a))

    def symbol():
        n = K.name()
        a, b = ri(10, 40), ri(5, 30)
        return mcq("%s har några kort. %s får %d kort till och har sedan %d kort. Vilken likhet passar?" % (n, n, b, a + b),
                   "□ + %d = %d" % (b, a + b), ["%d + %d = □" % (a + b, b), "□ − %d = %d" % (b, a + b), "%d − □ = %d" % (b, a + b)],
                   "Antalet från början är okänt (□). □ + %d = %d, så □ = <b>%d</b>." % (b, a + b, a))

    sets = [("Saknat tal i addition", [(saknas_add, 20)]),
            ("Saknat tal i subtraktion", [(saknas_sub, 20)]),
            ("Båda sidor lika mycket", [(balans, 14), (betydelse, 6)]),
            ("Sant eller falskt?", [(sant, 20)]),
            ("Multiplikation och okända tal", [(mult, 12), (symbol, 8)])]
    return unit("likheter-och-likhetstecknet", "A", 11, "Likheter och likhetstecknet: saknade tal", "Likheter",
                "Matematiska likheter och likhetstecknets innebörd. Obekanta tal och hur de kan betecknas med en symbol.",
                "Arbetsblad om likheter för årskurs 3: likhetstecknets betydelse, saknat tal i addition och subtraktion, sant eller falskt och okända tal i en ruta. 100 uppgifter med facit.",
                "= betyder lika mycket", "Båda sidorna av likhetstecknet är lika stora.", sets,
                ["Likhetstecknet = betyder att det är lika mycket på båda sidor. Det betyder inte bara att svaret kommer.",
                 "I 8 + 4 = □ + 5 är vänster sida 12. Då måste höger sida också vara 12: □ = 7.",
                 "En ruta □ är ett okänt tal. Hitta det genom att räkna baklänges: □ + 6 = 15 ger □ = 15 − 6 = 9."],
                [("8 + 4 = □ + 5", ["Vänster sida: 12", "12 − 5 = 7"], "7"), ("□ − 7 = 9", ["9 + 7 = 16"], "16")],
                [["8 + 4 = □ + 5, svarar 12", "Höger sida ska också bli 12: 7 + 5"], ["□ − 7 = 9, svarar 2", "Talet i rutan är 9 + 7 = 16"],
                 ["Tror att 10 = 6 + 4 är fel för att svaret står först", "Likheten kan skrivas åt båda hållen"]],
                [("Vad betyder rutan □?", "Ett tal vi inte vet än. Det kallas ett obekant tal."),
                 ("Kan svaret stå till vänster?", "Ja. 10 = 6 + 4 är en sann likhet."),
                 ("Hur kontrollerar jag?", "Sätt in talet i rutan och räkna båda sidorna. De ska bli lika.")])


# ============================================================ 12. Mönster och talföljder
SHAPES = {"cirkel": lambda x, y, c: "<circle cx='%d' cy='%d' r='12' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y, c, INK),
          "kvadrat": lambda x, y, c: "<rect x='%d' y='%d' width='24' height='24' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x - 12, y - 12, c, INK),
          "triangel": lambda x, y, c: "<polygon points='%d,%d %d,%d %d,%d' fill='%s' stroke='%s' stroke-width='1.5'/>" % (x, y - 13, x - 13, y + 11, x + 13, y + 11, c, INK)}
COLS_ = {"röd": "#e07a5f", "blå": "#6a9fd4", "gul": "#f2c94c", "grön": "#81b29a"}


def mpic(seq, blank=True):
    s = []
    for i, (sh_, c) in enumerate(seq):
        s.append(SHAPES[sh_](22 + i * 34, 22, COLS_[c]))
    if blank:
        x = 22 + len(seq) * 34
        s.append("<rect x='%d' y='8' width='28' height='28' fill='none' stroke='%s' stroke-width='1.5' stroke-dasharray='4 3'/>" % (x - 14, RED))
        s.append(text(x, 28, "?", 16, col=RED))
    return wrap((len(seq) + 1) * 34 + 12, 44, "".join(s), "ett mönster med figurer")


def u12():
    def fortsatt():
        st = ch([2, 3, 4, 5, 10, 20, 25, 50, 100])
        a = ri(0, 30) * (1 if st < 10 else 5)
        up = R.random() < 0.7
        if not up:
            a = a + st * 7
        xs = [a + i * st * (1 if up else -1) for i in range(5)]
        if min(xs) < 0 or max(xs) > 1000:
            return None
        nxt = xs[-1] + st * (1 if up else -1)
        if nxt < 0:
            return None
        return mcq("Hur fortsätter talföljden? %s, ?" % ", ".join(num(x) for x in xs), num(nxt),
                   [num(nxt + st), num(xs[-1] + 1) if up else num(xs[-1] - 1), num(nxt - st) if nxt - st >= 0 else num(nxt + 2 * st)],
                   "Talen %s med %d varje gång: <b>%s</b>." % ("ökar" if up else "minskar", st, num(nxt)))

    def regel():
        st = ch([2, 3, 4, 5, 6, 10, 20, 50])
        a = ri(1, 50)
        up = R.random() < 0.6
        if not up:
            a += 6 * st
        xs = [a + i * st * (1 if up else -1) for i in range(5)]
        if min(xs) < 0:
            return None
        ans = "%s med %d" % ("öka" if up else "minska", st)
        w = ["%s med %d" % ("öka" if up else "minska", x) for x in (st + 1, st - 1 if st > 2 else st + 2)] + ["%s med %d" % ("minska" if up else "öka", st)]
        return mcq("Vilken är regeln i talföljden %s?" % ", ".join(num(x) for x in xs), cap(ans), [cap(x) for x in w],
                   "%s − %s = %d. Regeln är: <b>%s</b>." % (num(max(xs[1], xs[0])), num(min(xs[1], xs[0])), st, ans))

    def lucka():
        st = ch([3, 4, 5, 6, 7, 8, 9, 10, 25])
        a = ri(1, 40)
        xs = [a + i * st for i in range(6)]
        k = ri(1, 4)
        ans = xs[k]
        sh_ = [num(x) if i != k else "?" for i, x in enumerate(xs)]
        return mcq("Vilket tal saknas? %s" % ", ".join(sh_), num(ans), [num(ans + 1), num(ans - 1), num(ans + st)],
                   "Talen ökar med %d. %s + %d = <b>%s</b>." % (st, num(xs[k - 1]), st, num(ans)))

    def figur():
        names = sh(list(SHAPES))
        cols = sh(list(COLS_))
        L = ri(2, 3)
        unitp = [(names[i % len(names)], cols[i]) for i in range(L)]
        if L == 2 and R.random() < 0.5:
            unitp = [(names[0], cols[0]), (names[0], cols[0]), (names[1], cols[1])]
            L = 3
        n = ri(L * 2, L * 2 + L - 1)
        seq = [unitp[i % L] for i in range(n)]
        ans = unitp[n % L]
        def nm(p):
            return "%s %s" % (p[1], p[0])
        w = [nm(p) for p in sorted(set(unitp)) if p != ans] + [nm((ans[0], c)) for c in COLS_ if c != ans[1]]
        return mcq(mpic(seq) + "Vilken figur kommer sedan?", nm(ans), w,
                   "Mönstret upprepas efter %d figurer. Nästa figur är <b>%s</b>." % (L, nm(ans)))

    def vaxande():
        a, st = ri(1, 5), ri(2, 4)
        xs = [a + i * st for i in range(4)]
        s = []
        x = 8
        for i, v in enumerate(xs):
            for j in range(v):
                s.append("<rect x='%d' y='%d' width='10' height='10' fill='%s' stroke='%s'/>" % (x + (j % 3) * 11, 60 - (j // 3) * 11, FILL, GREEN))
            s.append(text(x + 16, 86, "Figur %d" % (i + 1), 11, weight=400))
            x += 60
        pic = wrap(x + 4, 92, "".join(s), "växande mönster med kvadrater")
        n5 = a + 4 * st
        return mcq(pic + "Hur många kvadrater har figur 5?", str(n5), [str(n5 + st), str(n5 - 1), str(xs[-1] + 1)],
                   "Varje figur har %d kvadrater fler. Figur 4 har %d, figur 5 har %d + %d = <b>%d</b>." % (st, xs[-1], xs[-1], st, n5))

    def jamna():
        k = ri(0, 2)
        n = ri(10, 99)
        if k == 0:
            ev = n % 2 == 0
            return mcq("Är %d ett jämnt eller udda tal?" % n, "jämnt" if ev else "udda", ["udda" if ev else "jämnt", "både jämnt och udda", "varken jämnt eller udda"],
                       "Entalssiffran är %d. Tal som slutar på 0, 2, 4, 6 eller 8 är jämna. %d är <b>%s</b>." % (n % 10, n, "jämnt" if ev else "udda"))
        xs = sh([ri(10, 99) * 2, ri(5, 49) * 2 + 1, ri(5, 49) * 2 + 1, ri(5, 49) * 2 + 1])
        if k == 1:
            ev = [x for x in xs if x % 2 == 0][0]
            return mcq("Vilket tal är jämnt?", num(ev), [num(x) for x in xs if x != ev], "%s slutar på %d och är jämnt." % (num(ev), ev % 10))
        a, b = ri(1, 30) * 2 + 1, ri(1, 30) * 2 + 1
        return mcq("Två udda tal läggs ihop: %d + %d. Blir summan jämn eller udda?" % (a, b), "jämn", ["udda", "det beror på talen", "noll"],
                   "%d + %d = %d. Udda + udda blir alltid <b>jämnt</b>." % (a, b, a + b))

    sets = [("Fortsätt talföljden", [(fortsatt, 20)]),
            ("Hitta regeln", [(regel, 20)]),
            ("Vilket tal saknas?", [(lucka, 20)]),
            ("Geometriska mönster", [(figur, 12), (vaxande, 8)]),
            ("Jämna och udda tal", [(jamna, 12), (fortsatt, 4), (lucka, 4)])]
    return unit("monster-och-talfoljder", "A", 12, "Mönster och talföljder", "Mönster och talföljder",
                "Hur enkla mönster i talföljder och enkla geometriska mönster kan konstrueras, beskrivas och uttryckas. Jämna och udda tal.",
                "Arbetsblad om mönster för årskurs 3: fortsätt talföljder, hitta regeln, saknade tal, mönster med figurer, växande mönster och jämna och udda tal. 100 uppgifter med facit.",
                "Hitta regeln", "Hur mycket ökar eller minskar talen?", sets,
                ["I en talföljd ändras talen efter en regel. Räkna skillnaden mellan två tal som står bredvid varandra: 5, 9, 13, 17 ökar med 4.",
                 "Kontrollera regeln på alla tal innan du fortsätter.",
                 "I ett geometriskt mönster upprepas en grupp figurer. Hitta gruppen som upprepas, till exempel röd cirkel, blå kvadrat, röd cirkel, blå kvadrat."],
                [("5, 9, 13, 17, ?", ["Talen ökar med 4", "17 + 4"], "21"), ("80, 70, 60, ?", ["Talen minskar med 10"], "50")],
                [["Tittar bara på de två första talen", "Kontrollera regeln på alla tal"], ["5, 9, 13, 17, svarar 18", "Ökar med 4: 21"],
                 ["Tror att 0 är ett udda tal", "0 är ett jämnt tal"]],
                [("Vad är en talföljd?", "Tal som kommer i en bestämd ordning efter en regel."),
                 ("Vilka tal är jämna?", "Tal som slutar på 0, 2, 4, 6 eller 8. De går att dela i två lika stora delar."),
                 ("Kan ett mönster minska?", "Ja, till exempel 50, 45, 40, 35, där talen minskar med 5.")])


UNITS = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12]
