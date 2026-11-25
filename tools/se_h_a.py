# -*- coding: utf-8 -*-
"""Sverige årskurs 7–9: tal（negativa tal, prioriteringsregler, delbarhet, bråk, decimaltal, potenser, grundpotensform, reella tal）"""
import math
from fractions import Fraction as F
from se_h import (MQ, lista, ri, ch, sh, cap, fr, fq, d, par, sg, M, MN, rd, sup, unit, tab, K, num, kr, NB, MIN, coin)


def nz(a, b):
    while True:
        v = ri(a, b)
        if v:
            return v


# ============================================================ negativa tal
def negativa(lv):
    def addsub():
        a, b = nz(-20, 20), ri(1, 20)
        k = ri(0, 3)
        if k == 0:
            q, v, w = "%s + %d" % (sg(a), b), a + b, [a - b, -(a + b), abs(a) + b]
        elif k == 1:
            q, v, w = "%s − %d" % (sg(a), b), a - b, [a + b, -(a - b), b - abs(a)]
        elif k == 2:
            q, v, w = "%s + (−%d)" % (sg(a), b), a - b, [a + b, -(a - b), abs(a - b) + 1]
        else:
            q, v, w = "%s − (−%d)" % (sg(a), b), a + b, [a - b, -(a + b), -a - b + 1]
        return MN("Beräkna %s." % q, v, w, "%s = <b>%s</b>. Två minustecken bredvid varandra blir plus." % (q, d(v)) if k == 3 else "%s = <b>%s</b>." % (q, d(v)))

    def muldiv():
        a, b = nz(-12, 12), nz(-12, 12)
        if a > 0 and b > 0:
            a = -a
        if coin():
            q, v = "%s · %s" % (sg(a), par(b)), a * b
            return MN("Beräkna %s." % q, v, [-v, a + b, abs(a) + abs(b)], "Olika tecken ger minus, lika tecken ger plus: %s = <b>%s</b>." % (q, d(v)))
        p = a * b
        q, v = "%s : %s" % (sg(p), par(b)), a
        return MN("Beräkna %s." % q, v, [-v, p - b, b], "Olika tecken ger minus, lika tecken ger plus: %s = <b>%s</b>." % (q, d(v)))

    def blandat():
        a, b, c = nz(-15, 15), nz(-9, 9), nz(-9, 9)
        k = ri(0, 2)
        if k == 0:
            q, v, w = "%s + %s · %s" % (sg(a), par(b), par(c)), a + b * c, [(a + b) * c, a - b * c, a + b + c]
        elif k == 1:
            q, v, w = "%s − %s · %s" % (sg(a), par(b), par(c)), a - b * c, [(a - b) * c, a + b * c, a - b - c]
        else:
            q, v, w = "(%s + %s) · %s" % (sg(a), par(b), par(c)), (a + b) * c, [a + b * c, -(a + b) * c, (a - b) * c]
        return MN("Beräkna %s." % q, v, w, "Multiplikation före addition och subtraktion, parentes först: %s = <b>%s</b>." % (q, d(v)))

    def ordning():
        xs = sh(set([nz(-30, 30) for _ in range(6)]))[:4]
        if len(xs) < 4:
            return None
        k = ri(0, 2)
        s = lista(sg(x) for x in xs)
        if k == 0:
            return M("Vilket tal är minst: %s?" % s, sg(min(xs)), [sg(x) for x in xs if x != min(xs)], "På tallinjen ligger <b>%s</b> längst till vänster." % sg(min(xs)))
        if k == 1:
            return M("Vilket tal är störst: %s?" % s, sg(max(xs)), [sg(x) for x in xs if x != max(xs)], "På tallinjen ligger <b>%s</b> längst till höger." % sg(max(xs)))
        a, b = sorted(xs[:2])
        return MN("Hur långt är det mellan %s och %s på tallinjen?" % (sg(a), sg(b)), b - a, [abs(a + b), b + a + 1 if b - a != b + a + 1 else b - a + 2, b - a - 2], "%s − %s = <b>%s</b>." % (sg(b), par(a), d(b - a)))

    def vardag():
        nm = K().name()
        k = ri(0, 3)
        if k == 0:
            t, dt = ri(-12, 4), ri(3, 15)
            return MN("På morgonen var det %s °C. Till eftermiddagen steg temperaturen %d grader. Vilken temperatur var det då?" % (sg(t), dt), t + dt, [t - dt, -(t + dt), abs(t) + dt], "%s + %d = <b>%s</b>." % (sg(t), dt, d(t + dt)), "°C")
        if k == 1:
            t, dt = ri(-5, 8), ri(6, 18)
            return MN("Klockan 18 var det %s °C. Under natten sjönk temperaturen %d grader. Hur kallt var det på natten?" % (sg(t), dt), t - dt, [t + dt, dt - t, -(t + dt)], "%s − %d = <b>%s</b>." % (sg(t), dt, d(t - dt)), "°C")
        if k == 2:
            s0, u = ri(50, 400), ri(100, 600)
            if u <= s0:
                u += s0
            return MN("%s har %s på kontot och köper något för %s med kortet. Hur mycket finns på kontot efter köpet?" % (nm, kr(s0), kr(u)), s0 - u, [u - s0, s0 + u, -(s0 + u)], "%d − %d = <b>%s</b>. Kontot är övertrasserat." % (s0, u, d(s0 - u)), "kr")
        a, b = ri(-25, -3), ri(2, 20)
        return MN("Lägsta temperaturen i januari var %s °C och högsta var %s °C. Hur stor var skillnaden?" % (sg(a), sg(b)), b - a, [b + a, abs(a) - b if abs(a) != b else b - a + 2, b - a + 10], "%d − (%s) = %d + %d = <b>%d</b>." % (b, sg(a), b, -a, b - a), "grader")

    sets = [("Addition och subtraktion", [(addsub, 20)]), ("Multiplikation och division", [(muldiv, 20)]),
            ("Blandade beräkningar", [(blandat, 20)]), ("Ordna och jämför", [(ordning, 20)]), ("Negativa tal i vardagen", [(vardag, 20)])]
    return unit("negativa-tal", "T", "Negativa tal: räkna med plus och minus", "Negativa tal",
                "Negativa tal och deras egenskaper samt hur de kan användas. Metoder för beräkningar med negativa tal i huvudräkning, skriftliga metoder och med digitala verktyg.",
                "Arbetsblad om negativa tal för årskurs 7: addition och subtraktion, multiplikation och division, prioriteringsregler och temperatur. 100 uppgifter med facit.",
                "Två minus bredvid varandra blir plus", "Lika tecken ger plus, olika tecken ger minus.", sets,
                ["Tänk på tallinjen. Att addera ett positivt tal är att gå åt höger, att subtrahera är att gå åt vänster: −3 + 5 = 2.",
                 "Att subtrahera ett negativt tal är samma sak som att addera: 4 − (−6) = 4 + 6 = 10.",
                 "Vid multiplikation och division ger två lika tecken plus och två olika tecken minus: (−4) · (−3) = 12, (−4) · 3 = −12."],
                [("−8 + 3", ["Börja på −8 och gå 3 steg åt höger"], "−5"), ("5 − (−7)", ["Minus minus blir plus: 5 + 7"], "12"), ("(−6) · (−4)", ["Lika tecken ger plus"], "24")],
                [["−8 + 3 = −11", "Gå åt höger på tallinjen: −8 + 3 = −5"], ["5 − (−7) = −2", "5 − (−7) = 5 + 7 = 12"], ["(−6) · (−4) = −24", "Lika tecken ger plus: 24"]],
                [("Vilket tal är störst, −2 eller −9?", "−2, eftersom det ligger längre till höger på tallinjen."),
                 ("Varför blir minus gånger minus plus?", "Att ta bort en skuld är som att få pengar. Mönstret 3 · (−2) = −6, 2 · (−2) = −4, 1 · (−2) = −2, 0 · (−2) = 0 fortsätter med (−1) · (−2) = 2."),
                 ("Var används negativa tal?", "Till exempel för temperatur under noll, höjd under havsytan och skulder.")])


# ============================================================ prioriteringsregler
def prioritering(lv):
    def mult():
        a, b, c = ri(2, 30), ri(2, 9), ri(2, 9)
        k = ri(0, 3)
        if k == 0:
            q, v, w = "%d + %d · %d" % (a, b, c), a + b * c, [(a + b) * c, a + b + c, a * b + c]
        elif k == 1:
            if a < b * c:
                a += b * c
            q, v, w = "%d − %d · %d" % (a, b, c), a - b * c, [(a - b) * c, a - b - c, b * c - a]
        elif k == 2:
            q, v, w = "%d · %d + %d · %d" % (b, c, c, a % 9 + 2), b * c + c * (a % 9 + 2), [(b * c + c) * (a % 9 + 2), b * (c + c) * (a % 9 + 2), b + c + c + a % 9 + 2]
        else:
            p = b * c
            q, v, w = "%d + %d : %d" % (a, p, b), a + c, [(a + p) // b if (a + p) % b == 0 else a + p, a + p + b, a + p - b]
        return MN("Beräkna %s." % q, v, w, "Multiplikation och division före addition och subtraktion: %s = <b>%s</b>." % (q, d(v)))

    def parentes():
        a, b, c = ri(2, 20), ri(2, 15), ri(2, 9)
        k = ri(0, 3)
        if k == 0:
            q, v, w = "(%d + %d) · %d" % (a, b, c), (a + b) * c, [a + b * c, a * c + b, a + b + c]
        elif k == 1:
            if a <= b:
                a, b = b + 1, a
            q, v, w = "%d · (%d − %d)" % (c, a, b), c * (a - b), [c * a - b, c * a + b, a - b + c]
        elif k == 2:
            s = (a + b) * c
            q, v, w = "%d : (%d + %d)" % (s, a, b), c, [s // a + b if s % a == 0 else s - a - b, s // a if s % a == 0 else c + 1, c + a]
        else:
            q, v, w = "%d − (%d − %d)" % (a + b + c, a + c, c), a + b + c - a, [a + b + c - a - 2 * c, b - c if b != c else b + 1, a + b]
        return MN("Beräkna %s." % q, v, w, "Räkna parentesen först: %s = <b>%s</b>." % (q, d(v)))

    def potens():
        a, b, c = ri(2, 9), ri(2, 9), ri(2, 5)
        k = ri(0, 3)
        if k == 0:
            q, v, w = "%d + %d²" % (a, b), a + b * b, [(a + b) ** 2, a + 2 * b, a * a + b * b]
        elif k == 1:
            q, v, w = "%d · %d²" % (c, b), c * b * b, [(c * b) ** 2, c * 2 * b, c + b * b]
        elif k == 2:
            q, v, w = "(%d + %d)²" % (a, b), (a + b) ** 2, [a * a + b * b, 2 * (a + b), a + b * b]
        else:
            if a * a <= b:
                a += 3
            q, v, w = "%d² − %d · %d" % (a, b, c), a * a - b * c, [(a * a - b) * c, 2 * a - b * c, a * a + b * c]
        return MN("Beräkna %s." % q, v, w, "Potenser först, sedan multiplikation och sist addition och subtraktion: %s = <b>%s</b>." % (q, d(v)))

    def neg():
        a, b, c = ri(2, 9), ri(2, 9), ri(2, 9)
        k = ri(0, 3)
        if k == 0:
            q, v, w = "−%d²" % a, -a * a, [a * a, -2 * a, 2 * a]
            e = "Bara %d upphöjs: −%d² = −(%d · %d) = <b>%s</b>." % (a, a, a, a, d(v))
        elif k == 1:
            q, v, w = "(−%d)²" % a, a * a, [-a * a, -2 * a, 2 * a]
            e = "Hela parentesen upphöjs: (−%d) · (−%d) = <b>%d</b>." % (a, a, a * a)
        elif k == 2:
            q, v, w = "−%d + %d · (−%d)" % (a, b, c), -a - b * c, [(-a + b) * -c, -a + b * c, a - b * c]
            e = "Multiplikationen först: %d · (−%d) = −%d. Sedan −%d − %d = <b>%s</b>." % (b, c, b * c, a, b * c, d(v))
        else:
            q, v, w = "(−%d − %d) · %d" % (a, b, c), -(a + b) * c, [(a + b) * c, -a - b * c, (b - a) * c if b != a else -c]
            e = "Parentesen först: −%d − %d = −%d. Sedan −%d · %d = <b>%s</b>." % (a, b, a + b, a + b, c, d(v))
        return MN("Beräkna %s." % q, v, w, e)

    def ord_():
        a, b, c = ri(3, 20), ri(2, 15), ri(2, 9)
        k = ri(0, 3)
        if k == 0:
            return M("Addera %d och %d och multiplicera summan med %d. Vilket uttryck passar?" % (a, b, c), "(%d + %d) · %d" % (a, b, c), ["%d + %d · %d" % (a, b, c), "%d · %d + %d" % (a, c, b), "%d · (%d + %d)" % (a, b, c)], "Summan ska räknas först, alltså en parentes: <b>(%d + %d) · %d</b> = %d." % (a, b, c, (a + b) * c))
        if k == 1:
            return M("Multiplicera %d med %d och dra sedan bort produkten från %d. Vilket uttryck passar?" % (b, c, a + b * c), "%d − %d · %d" % (a + b * c, b, c), ["(%d − %d) · %d" % (a + b * c, b, c), "%d · %d − %d" % (b, c, a + b * c), "%d − %d − %d" % (a + b * c, b, c)], "Produkten dras bort: <b>%d − %d · %d</b> = %d." % (a + b * c, b, c, a))
        if k == 2:
            nm = K().name()
            return MN("%s köper %d glassar för %s styck och en dricka för %s. Hur mycket kostar det?" % (nm, c, kr(b + 10), kr(a + 5)), c * (b + 10) + a + 5, [(c + 1) * (b + 10), c * (b + 10 + a + 5), c + b + 10 + a + 5], "%d · %d + %d = <b>%d kr</b>." % (c, b + 10, a + 5, c * (b + 10) + a + 5), "kr")
        n, p, m = ri(3, 6), ri(25, 60), ri(2, 4)
        return MN("%d kompisar delar lika på %d pizzor som kostar %s styck. Hur mycket betalar var och en?" % (n, m * n, kr(p)), m * p, [m * n * p, p // n if p % n == 0 else p + n, m * p + n], "(%d · %d) : %d = %d : %d = <b>%d kr</b>." % (m * n, p, n, m * n * p, n, m * p), "kr")

    sets = [("Multiplikation före addition", [(mult, 20)]), ("Parenteser", [(parentes, 20)]), ("Potenser", [(potens, 20)]),
            ("Negativa tal och potenser", [(neg, 20)]), ("Skriv och beräkna", [(ord_, 20)])]
    return unit("prioriteringsregler", "T", "Prioriteringsregler: parentes, potens, gånger och delat", "Prioriteringsregler",
                "Metoder för beräkningar med reella tal i huvudräkning, skriftliga metoder och med digitala verktyg. Prioriteringsreglerna vid beräkningar med parenteser, potenser och de fyra räknesätten.",
                "Arbetsblad om prioriteringsregler för årskurs 7: multiplikation före addition, parenteser, potenser och negativa tal. 100 uppgifter med facit.",
                "Parentes, potens, · och :, + och −", "Räkna från vänster till höger inom varje steg.", sets,
                ["Räkna i den här ordningen: först parenteser, sedan potenser, sedan multiplikation och division och sist addition och subtraktion.",
                 "Inom samma steg räknar du från vänster till höger: 20 − 8 + 3 = 12 + 3 = 15.",
                 "Se upp med −3² och (−3)². I −3² är det bara 3 som upphöjs, så −3² = −9. I (−3)² upphöjs hela parentesen, så (−3)² = 9."],
                [("4 + 3 · 5", ["Multiplikation först: 3 · 5 = 15", "4 + 15"], "19"), ("(4 + 3)²", ["Parentesen först: 7", "7² = 49"], "49")],
                [["4 + 3 · 5 = 35", "Multiplikation först: 4 + 15 = 19"], ["−3² = 9", "−3² = −(3 · 3) = −9"], ["(4 + 3)² = 4² + 3² = 25", "Räkna parentesen först: 7² = 49"]],
                [("Hur kommer jag ihåg ordningen?", "Parentes, potens, gånger och delat, plus och minus."),
                 ("Vad gör jag om det bara finns plus och minus?", "Räkna från vänster till höger."),
                 ("Räknar miniräknaren rätt?", "En vanlig miniräknare följer prioriteringsreglerna, men du måste skriva parenteser där de behövs.")])


# ============================================================ delbarhet och primtal
PRIM = [p for p in range(2, 100) if all(p % k for k in range(2, int(p ** 0.5) + 1))]


def fakt(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out


def fs(fs_):
    return " · ".join(str(x) for x in fs_)


def delbarhet(lv):
    def regel():
        k = ch([2, 3, 4, 5, 9, 10])
        cand = [n for n in (ri(100, 9999) for _ in range(40))]
        yes = [n for n in cand if n % k == 0]
        no = [n for n in cand if n % k]
        if not yes or len(no) < 3:
            return None
        a = yes[0]
        why = {2: "slutar på en jämn siffra", 3: "har en siffersumma som är delbar med 3", 4: "har de två sista siffrorna delbara med 4",
               5: "slutar på 0 eller 5", 9: "har en siffersumma som är delbar med 9", 10: "slutar på 0"}[k]
        return MQ("Vilket tal är delbart med %d:" % k, num(a), [num(x) for x in no[:3]], "<b>%s</b> %s." % (num(a), why))

    def primtal():
        if coin():
            ps = [p for p in PRIM if p > 10]
            p = ch(ps)
            cs = [n for n in range(11, 100) if n not in PRIM and n % 2 and n % 5]
            return MQ("Vilket av talen är ett primtal:", str(p), [str(x) for x in sh(cs)[:3]], "<b>%d</b> är bara delbart med 1 och sig självt. De andra går att dela, till exempel %s." % (p, ", ".join("%d = %s" % (x, fs(fakt(x))) for x in sh(cs)[:1])))
        n = ch([n for n in range(21, 100) if n not in PRIM and n % 2])
        f = fakt(n)
        return M("Talet %d är inte ett primtal. Varför?" % n, "%d = %s" % (n, fs(f)) if len(f) == 2 else "%d = %d · %d" % (n, f[0], n // f[0]),
                 ["%d är udda" % n, "%d slutar på %d" % (n, n % 10), "%d är större än 20" % n], "Ett primtal har bara två delare. %d kan delas upp i faktorer: <b>%s</b>." % (n, fs(f)))

    def faktor():
        base = sh([2, 2, 2, 3, 3, 5, 7, 11])
        f = sorted(base[:ri(3, 4)])
        n = 1
        for x in f:
            n *= x
        if n > 1000:
            return None
        w = [fs(sorted(f[:-1] + [f[-1] + 2])), "%d · %d" % (f[0], n // f[0]), fs(sorted(f + [2]))]
        return M("Skriv %d som en produkt av primtal." % n, fs(f), w, "Dela med primtal tills det tar slut: %d = <b>%s</b>." % (n, fs(f)))

    def sgd():
        g = ch([2, 3, 4, 5, 6, 8, 9, 10, 12, 15])
        a, b = ri(2, 9), ri(2, 9)
        if math.gcd(a, b) != 1 or a == b:
            return None
        x, y = g * a, g * b
        if coin():
            return MN("Vilken är den största gemensamma delaren till %d och %d?" % (x, y), g, [g * 2 if (x % (2 * g) == 0 and y % (2 * g) == 0) else g + 1, x * y // g, min(x, y) - g, math.gcd(x, y) // 2 or 1], "Både %d och %d är delbara med %d, och inget större tal delar båda: <b>%d</b>." % (x, y, g, g))
        l = x * y // g
        return MN("Vilken är den minsta gemensamma multipeln till %d och %d?" % (x, y), l, [x * y, l * 2, x + y], "Multiplerna av %d: %d, %d, … Den första som också är en multipel av %d är <b>%d</b>." % (max(x, y), max(x, y), 2 * max(x, y), min(x, y), l))

    def text_():
        k = ri(0, 2)
        if k == 0:
            a, b = ch([(12, 18), (16, 24), (20, 30), (24, 36), (18, 27), (15, 25), (28, 42), (30, 45), (32, 48), (36, 54), (40, 60)])
            g = math.gcd(a, b)
            return MN("I en påse finns %d röda och %d blå kulor. De ska delas i så många påsar som möjligt med lika många röda och lika många blå i varje. Hur många påsar blir det?" % (a, b), g, [a + b, math.gcd(a, b) // 2 if g % 2 == 0 else g + 1, a * b // g], "Antalet påsar ska dela både %d och %d. Största gemensamma delaren är <b>%d</b>." % (a, b, g), "påsar")
        if k == 1:
            a, b = ch([(4, 6), (6, 8), (6, 9), (8, 12), (10, 15), (12, 18), (9, 12), (15, 20), (10, 12), (6, 10)])
            l = a * b // math.gcd(a, b)
            return MN("En buss går var %d:e minut och en annan var %d:e minut. Båda går klockan 8.00. Efter hur många minuter går de samtidigt igen?" % (a, b), l, [a * b if a * b != l else l + a, a + b, abs(a - b) if a != b else a], "Minsta gemensamma multipeln av %d och %d är <b>%d</b>." % (a, b, l), "minuter")
        a, b = ch([(8, 12), (6, 15), (12, 20), (9, 15), (10, 25), (14, 21), (16, 20), (18, 24)])
        l = a * b // math.gcd(a, b)
        return MN("Korv säljs i paket om %d och bröd i paket om %d. Hur många av varje behöver du minst för att det ska bli lika många?" % (a, b), l, [a * b, a + b, math.gcd(a, b)], "Minsta gemensamma multipeln av %d och %d är <b>%d</b>." % (a, b, l), "st")

    sets = [("Delbarhetsregler", [(regel, 20)]), ("Primtal", [(primtal, 20)]), ("Primtalsfaktorisering", [(faktor, 20)]),
            ("Gemensam delare och multipel", [(sgd, 20)]), ("Problem med delare och multipler", [(text_, 20)])]
    return unit("delbarhet-och-primtal", "T", "Delbarhet och primtal: faktorisera, delare och multipler", "Delbarhet och primtal",
                "Reella tal och deras egenskaper samt deras användning i vardagliga och matematiska situationer. Delbarhet, primtal och primtalsfaktorisering, gemensamma delare och multipler.",
                "Arbetsblad om delbarhet och primtal för årskurs 7: delbarhetsregler, primtal, primtalsfaktorisering, största gemensamma delare och minsta gemensamma multipel. 100 uppgifter med facit.",
                "Ett primtal har exakt två delare", "Varje heltal över 1 är en produkt av primtal.", sets,
                ["Ett tal är delbart med 3 om siffersumman är delbar med 3: 471 → 4 + 7 + 1 = 12, alltså delbart med 3.",
                 "Ett primtal har bara två delare, 1 och sig självt: 2, 3, 5, 7, 11, 13, … Talet 1 är inte ett primtal.",
                 "Primtalsfaktorisera genom att dela med primtal i tur och ordning: 60 = 2 · 2 · 3 · 5."],
                [("Primtalsfaktorisera 84", ["84 : 2 = 42, 42 : 2 = 21, 21 : 3 = 7"], "84 = 2 · 2 · 3 · 7"), ("Största gemensamma delaren till 24 och 36", ["24 = 2 · 2 · 2 · 3, 36 = 2 · 2 · 3 · 3", "Gemensamt: 2 · 2 · 3"], "12")],
                [["1 är ett primtal", "1 har bara en delare och är inte ett primtal"], ["Alla udda tal är primtal", "9 = 3 · 3 och 15 = 3 · 5 är udda men inte primtal"], ["84 = 4 · 21 är klart", "4 och 21 är inte primtal: 84 = 2 · 2 · 3 · 7"]],
                [("Vilket är det enda jämna primtalet?", "2. Alla andra jämna tal är delbara med 2."), ("Vad används största gemensamma delaren till?", "Till att förkorta bråk och dela upp saker i lika stora grupper."),
                 ("Vad används minsta gemensamma multipeln till?", "Till att hitta gemensam nämnare och lösa problem om saker som händer samtidigt.")])


# ============================================================ bråk
def brak(lv):
    def frq(a):
        return fq(a, mixed=True)

    def forkorta():
        a, b = ri(1, 9), ri(2, 12)
        if a >= b or math.gcd(a, b) != 1:
            return None
        k = ri(2, 8)
        if coin():
            return M("Förkorta %s så långt det går." % fr(a * k, b * k), fr(a, b), [fr(a * k // 2, b * k // 2) if k % 2 == 0 and k > 2 else fr(a + 1, b), fr(b, a) if a > 1 else fr(a, b + 1), fr(a * k - 1, b * k - 1) if a * k > 1 else fr(2, b)], "Dela täljare och nämnare med %d: <b>%s</b>." % (k, fr(a, b)))
        return M("Vilket bråk är lika mycket som %s?" % fr(a, b), fr(a * k, b * k), [fr(a + k, b + k), fr(a * k, b), fr(a, b * k)], "Förläng med %d: täljare och nämnare multipliceras med %d, <b>%s</b>." % (k, k, fr(a * k, b * k)))

    def addsub():
        b1, b2 = ch([(2, 3), (3, 4), (2, 5), (4, 6), (3, 5), (6, 8), (4, 5), (5, 6), (3, 8), (2, 7), (6, 9), (4, 10)])
        a1, a2 = ri(1, b1 - 1), ri(1, b2 - 1)
        if math.gcd(a1, b1) > 1 or math.gcd(a2, b2) > 1:
            return None
        x, y = F(a1, b1), F(a2, b2)
        if coin():
            v = x + y
            return M("Beräkna %s + %s." % (fr(a1, b1), fr(a2, b2)), frq(v), [fr(a1 + a2, b1 + b2), frq(F(a1 * a2, b1 * b2)), frq(v + F(1, v.denominator))], "Gör liknämnigt och addera täljarna: %s + %s = <b>%s</b>." % (fr(a1, b1), fr(a2, b2), frq(v)))
        if x < y:
            x, y, a1, b1, a2, b2 = y, x, a2, b2, a1, b1
        if x == y:
            return None
        v = x - y
        return M("Beräkna %s − %s." % (fr(a1, b1), fr(a2, b2)), frq(v), [fq(F(abs(a1 - a2), abs(b1 - b2))) if a1 != a2 and b1 != b2 else frq(v + F(1, 2)), frq(x + y), frq(v + F(1, v.denominator))], "Gör liknämnigt och subtrahera täljarna: %s − %s = <b>%s</b>." % (fr(a1, b1), fr(a2, b2), frq(v)))

    def mul():
        a1, b1, a2, b2 = ri(1, 7), ri(2, 9), ri(1, 7), ri(2, 9)
        if a1 >= b1 or a2 >= b2 or math.gcd(a1, b1) > 1 or math.gcd(a2, b2) > 1:
            return None
        x, y = F(a1, b1), F(a2, b2)
        if coin():
            v = x * y
            return M("Beräkna %s · %s." % (fr(a1, b1), fr(a2, b2)), fq(v), [fr(a1 + a2, b1 + b2), fq(F(a1 * b2, b1 * a2)), fq(F(a1 * a2, b1 + b2))], "Täljare gånger täljare och nämnare gånger nämnare: <b>%s</b>." % fq(v))
        v = x / y
        return M("Beräkna %s : %s." % (fr(a1, b1), fr(a2, b2)), frq(v), [fq(x * y), frq(1 / v), fr(a1 * a2, b1 * b2) if fq(x * y) != fr(a1 * a2, b1 * b2) else frq(v + 1)], "Multiplicera med det inverterade bråket: %s · %s = <b>%s</b>." % (fr(a1, b1), fr(b2, a2), frq(v)))

    def blandad():
        h, a, b = ri(1, 5), ri(1, 8), ri(2, 9)
        if a >= b or math.gcd(a, b) != 1:
            return None
        if coin():
            return M("Skriv %s i bråkform." % (str(h) + fr(a, b)), fr(h * b + a, b), [fr(h + a, b), fr(h * a + b, b), fr(h * b + a, h * b)], "%d hela är %s. %s + %s = <b>%s</b>." % (h, fr(h * b, b), fr(h * b, b), fr(a, b), fr(h * b + a, b)))
        return M("Skriv %s i blandad form." % fr(h * b + a, b), str(h) + fr(a, b), [str(h + 1) + fr(a, b), str(h) + fr(b - a, b) if b - a != a else str(h - 1 if h > 1 else h + 2) + fr(a, b), str(a) + fr(h, b) if a != h and h < b else str(h) + fr(a, b + 1)], "%d : %d = %d rest %d, alltså <b>%s</b>." % (h * b + a, b, h, a, str(h) + fr(a, b)))

    def text_():
        nm = K().name()
        k = ri(0, 3)
        if k == 0:
            a, b = ch([(1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 6), (5, 6), (3, 8), (5, 8)])
            t = b * ri(4, 30)
            return MN("%s har %s. %s spenderar %s av pengarna. Hur mycket spenderar %s?" % (nm, kr(t), cap(K().pool[0][0]) if False else nm, fr(a, b), nm), t * a // b, [t // b, t - t * a // b, t * b // a if t * b % a == 0 else t // a], "%s av %d = %d : %d · %d = <b>%d kr</b>." % (fr(a, b), t, t, b, a, t * a // b), "kr")
        if k == 1:
            a, b = ch([(1, 4), (1, 3), (2, 5), (3, 10), (1, 5), (1, 6)])
            c, e = ch([(1, 2), (1, 3), (1, 4), (2, 3)])
            v = F(a, b) + (1 - F(a, b)) * F(c, e)
            return M("En tårta delas. Först äter familjen %s av tårtan. Sedan äter de %s av det som är kvar. Hur stor del av tårtan har de ätit?" % (fr(a, b), fr(c, e)), fq(v), [fq(F(a, b) + F(c, e)) if F(a, b) + F(c, e) < 1 else fq(v + F(1, 12)), fq(F(a, b) * F(c, e)), fq(1 - v)],
                     "Kvar efter första gången: %s. %s av det är %s. Totalt %s + %s = <b>%s</b>." % (fq(1 - F(a, b)), fr(c, e), fq((1 - F(a, b)) * F(c, e)), fr(a, b), fq((1 - F(a, b)) * F(c, e)), fq(v)))
        if k == 2:
            a, b = ch([(3, 4), (2, 3), (1, 2), (3, 5), (5, 8)])
            n = ri(3, 12)
            v = F(a, b) * n
            return M("Ett recept för en kaka behöver %s dl socker. Hur mycket socker behövs till %d kakor?" % (fr(a, b), n), frq(v) + NB + "dl", [frq(v + F(1, b)) + NB + "dl", fq(F(a, b * n)) + NB + "dl", frq(F(a + n, b)) + NB + "dl"], "%d · %s = %s = <b>%s dl</b>." % (n, fr(a, b), fr(a * n, b), frq(v)))
        a, b = ch([(1, 2), (1, 3), (1, 4), (3, 4), (2, 3)])
        L = ri(2, 9)
        v = L / F(a, b)
        if v.denominator != 1:
            return None
        return MN("Hur många flaskor om %s liter kan fyllas med %d liter saft?" % (fr(a, b), L), v, [L * a // b if L * a % b == 0 else L + b, L * b + 1, v - 1], "%d : %s = %d · %s = <b>%s</b>." % (L, fr(a, b), L, fr(b, a), d(v)), "flaskor")

    sets = [("Förkorta och förläng", [(forkorta, 20)]), ("Addition och subtraktion", [(addsub, 20)]),
            ("Multiplikation och division", [(mul, 20)]), ("Blandad form", [(blandad, 20)]), ("Bråk i vardagen", [(text_, 20)])]
    return unit("brak", "T", "Bråk: förkorta, addera, multiplicera och dividera", "Bråk",
                "Rationella tal och deras egenskaper samt deras användning i vardagliga och matematiska situationer. Metoder för beräkningar med bråk i huvudräkning och skriftliga metoder.",
                "Arbetsblad om bråk för årskurs 7: förkorta och förläng, addition och subtraktion med olika nämnare, multiplikation, division och blandad form. 100 uppgifter med facit.",
                "Gör liknämnigt innan du adderar", "Vid division multiplicerar du med det inverterade bråket.", sets,
                ["Förkorta genom att dela täljare och nämnare med samma tal: 6/8 = 3/4. Värdet ändras inte.",
                 "För att addera eller subtrahera bråk behöver de samma nämnare: 1/3 + 1/4 = 4/12 + 3/12 = 7/12.",
                 "Multiplicera täljare med täljare och nämnare med nämnare: 2/3 · 3/5 = 6/15 = 2/5. Att dividera med ett bråk är att multiplicera med det inverterade bråket."],
                [("<span class='fr'><span class='fn'>1</span><span class='fd'>3</span></span> + <span class='fr'><span class='fn'>1</span><span class='fd'>4</span></span>", ["Gemensam nämnare 12: 4/12 + 3/12"], "7/12"),
                 ("<span class='fr'><span class='fn'>3</span><span class='fd'>4</span></span> : <span class='fr'><span class='fn'>1</span><span class='fd'>2</span></span>", ["3/4 · 2/1 = 6/4"], "1 1/2")],
                [["1/3 + 1/4 = 2/7", "Gör liknämnigt: 4/12 + 3/12 = 7/12"], ["2/3 · 3/5 = 6/5", "Nämnare gånger nämnare: 6/15 = 2/5"], ["3/4 : 1/2 = 3/8", "Multiplicera med 2/1: 6/4 = 1 1/2"]],
                [("Hur hittar jag en gemensam nämnare?", "Ta minsta gemensamma multipeln av nämnarna, eller multiplicera nämnarna med varandra."),
                 ("Varför blir det större när man delar med ett bråk?", "Att dela 3 med 1/2 frågar hur många halvor det finns i 3. Det är 6."),
                 ("Ska svaret alltid förkortas?", "Ja, förkorta så långt det går och skriv gärna tal större än 1 i blandad form.")])


# ============================================================ decimaltal
def decimaltal(lv):
    def tiopot():
        x = F(ri(11, 9999), ch([10, 100, 1000]))
        k = ch([10, 100, 1000])
        if coin():
            v = x * k
            return M("Beräkna %s · %s." % (d(x), num(k)), d(v), [d(x * k / 10), d(x * k * 10), d(x / k)], "Flytta decimaltecknet %d steg åt höger: <b>%s</b>." % (len(str(k)) - 1, d(v)))
        v = x / k
        return M("Beräkna %s : %s." % (d(x), num(k)), d(v), [d(v * 10), d(v / 10), d(x * k)], "Flytta decimaltecknet %d steg åt vänster: <b>%s</b>." % (len(str(k)) - 1, d(v)))

    def mult():
        a, b = F(ri(11, 99), 10), F(ri(2, 9), ch([1, 10]))
        if coin():
            a = F(ri(101, 999), 100)
        v = a * b
        return M("Beräkna %s · %s." % (d(a), d(b)), d(v), [d(v * 10), d(v / 10), d(a + b)], "Räkna utan decimaltecken och sätt sedan in lika många decimaler som i faktorerna: <b>%s</b>." % d(v))

    def div():
        b = F(ri(2, 9), ch([1, 10, 10]))
        v = F(ri(11, 99), ch([1, 10]))
        a = v * b
        return M("Beräkna %s : %s." % (d(a), d(b)), d(v), [d(v * 10), d(v / 10), d(a * b)], "Förläng så att nämnaren blir ett heltal: %s : %s. Svar: <b>%s</b>." % (d(a * 10 if b.denominator == 10 else a), d(b * 10 if b.denominator == 10 else b), d(v)))

    def avr():
        x = F(ri(10000, 999999), 1000)
        k = ri(0, 2)
        name = ["heltal", "tiondelar", "hundradelar"][k]
        v = rd(x, k)
        w = [rd(x + F(1, 10 ** k), k), rd(x - F(1, 10 ** k), k), d(int(x * 10 ** k) / F(10 ** k)) if d(int(x * 10 ** k) / F(10 ** k)) != v else rd(x, k + 1)]
        return M("Avrunda %s till %s." % (d(x), name), v, w, "Titta på siffran efter den sista du ska behålla: <b>%s</b>." % v)

    def text_():
        nm = K().name()
        k = ri(0, 3)
        if k == 0:
            p, m = F(ri(15, 99), 10), F(ri(5, 40), 10)
            v = p * m
            return M("Lösgodis kostar %s kr per hekto. %s köper %s hekto. Vad kostar det?" % (d(p), nm, d(m)), rd(v, 2) + NB + "kr", [rd(v * 10, 2) + NB + "kr", rd(p + m, 2) + NB + "kr", rd(v / 10, 2) + NB + "kr"], "%s · %s = <b>%s kr</b>." % (d(p), d(m), rd(v, 2)))
        if k == 1:
            L = F(ri(20, 60), 1) + F(ri(1, 9), 10)
            p = F(ri(175, 225), 10)
            v = L * p
            return M("Bensin kostar %s kr per liter. Hur mycket kostar %s liter? Avrunda till hela kronor." % (d(p), d(L)), rd(v, 0) + NB + "kr", [rd(v + 10, 0) + NB + "kr", rd(v / 10, 0) + NB + "kr", rd(L + p, 0) + NB + "kr"], "%s · %s ≈ <b>%s kr</b>." % (d(L), d(p), rd(v, 0)))
        if k == 2:
            n = ri(3, 8)
            t = F(ri(30, 200), 1) + F(ri(1, 9) * 10 + 5, 100)
            v = t / n
            if (v * 100).denominator != 1:
                return None
            return M("%d kompisar delar lika på en nota på %s kr. Hur mycket betalar var och en?" % (n, d(t)), d(v) + NB + "kr", [d(v * 10) + NB + "kr", d(t - n) + NB + "kr", d(v + 1) + NB + "kr"], "%s : %d = <b>%s kr</b>." % (d(t), n, d(v)))
        a, b = F(ri(110, 190), 100), F(ri(110, 190), 100)
        return M("%s är %s m lång och %s är %s m lång. Hur mycket längre är den längsta?" % (nm, d(max(a, b)), K().name(), d(min(a, b))), d(abs(a - b)) + NB + "m", [d(abs(a - b) * 10) + NB + "m", d(a + b) + NB + "m", d(abs(a - b) + F(1, 10)) + NB + "m"], "%s − %s = <b>%s m</b>." % (d(max(a, b)), d(min(a, b)), d(abs(a - b)))) if a != b else None

    sets = [("Gånger och delat med 10, 100 och 1 000", [(tiopot, 20)]), ("Multiplikation med decimaltal", [(mult, 20)]),
            ("Division med decimaltal", [(div, 20)]), ("Avrundning", [(avr, 20)]), ("Decimaltal i vardagen", [(text_, 20)])]
    return unit("decimaltal", "T", "Decimaltal: multiplicera, dividera och avrunda", "Decimaltal",
                "Rationella tal och deras egenskaper. Metoder för beräkningar med decimaltal i huvudräkning, skriftliga metoder och med digitala verktyg. Rimlighetsbedömning vid uppskattningar och beräkningar.",
                "Arbetsblad om decimaltal för årskurs 7: multiplikation och division med 10, 100 och 1 000, multiplikation och division med decimaltal, avrundning och vardagsproblem. 100 uppgifter med facit.",
                "Räkna först utan decimaltecken", "Gör ett överslag och kontrollera att svaret är rimligt.", sets,
                ["Gånger 10 flyttar decimaltecknet ett steg åt höger, delat med 10 ett steg åt vänster.",
                 "Vid multiplikation räknar du först utan decimaltecken. Svaret får lika många decimaler som faktorerna har tillsammans: 2,4 · 0,3 → 24 · 3 = 72 → 0,72.",
                 "Vid division med ett decimaltal kan du förlänga så att nämnaren blir ett heltal: 4,8 : 0,6 = 48 : 6 = 8."],
                [("2,4 · 0,3", ["24 · 3 = 72", "1 + 1 = 2 decimaler"], "0,72"), ("4,8 : 0,6", ["Förläng med 10: 48 : 6"], "8")],
                [["2,4 · 0,3 = 7,2", "Två decimaler totalt: 0,72"], ["4,8 : 0,6 = 0,8", "48 : 6 = 8. Att dela med ett tal mindre än 1 ger ett större svar"], ["3,46 avrundat till tiondelar är 3,4", "Siffran efter är 6, så avrunda uppåt: 3,5"]],
                [("Blir det alltid större när man multiplicerar?", "Nej. Multiplicerar du med ett tal mellan 0 och 1 blir det mindre: 8 · 0,5 = 4."),
                 ("Hur gör jag ett överslag?", "Avrunda till enkla tal: 4,9 · 21,3 ≈ 5 · 20 = 100."),
                 ("När avrundar jag uppåt?", "När siffran efter den sista du ska behålla är 5 eller större.")])


# ============================================================ potenser
def potenser(lv):
    def varde():
        b, e = ri(2, 10), ri(2, 5)
        if b ** e > 100000 or (b == 10 and e > 6):
            return None
        return MN("Beräkna %d%s." % (b, sup(e)), b ** e, [b * e, b ** (e - 1), b ** e + b], "%d%s = %s = <b>%s</b>." % (b, sup(e), " · ".join([str(b)] * e), num(b ** e)))

    def skriv():
        b, e = ri(2, 9), ri(3, 7)
        if coin():
            return M("Skriv %s i potensform." % " · ".join([str(b)] * e), "%d%s" % (b, sup(e)), ["%d%s" % (e, sup(b)) if e != b else "%d%s" % (b, sup(e + 1)), "%d · %d" % (b, e), "%d%s" % (b * e, sup(1)) if False else "%d%s" % (b, sup(e - 1))], "%d multipliceras med sig själv %d gånger: <b>%d%s</b>." % (b, e, b, sup(e)))
        n = 10 ** ri(2, 9)
        e = len(str(n)) - 1
        return M("Skriv %s som en tiopotens." % num(n), "10%s" % sup(e), ["10%s" % sup(e + 1), "10%s" % sup(e - 1), "%d%s" % (e, sup(10))], "%s har %d nollor: <b>10%s</b>." % (num(n), e, sup(e)))

    def rot():
        n = ri(2, 20)
        k = ri(0, 2)
        if k == 0:
            return MN("Beräkna √%d." % (n * n), n, [n * n // 2, n + 1, 2 * n], "%d · %d = %d, alltså √%d = <b>%d</b>." % (n, n, n * n, n * n, n))
        if k == 1:
            m = ri(3, 99)
            if int(m ** 0.5) ** 2 == m:
                return None
            lo = int(m ** 0.5)
            return M("Mellan vilka heltal ligger √%d?" % m, "%d och %d" % (lo, lo + 1), ["%d och %d" % (lo - 1, lo) if lo > 1 else "%d och %d" % (lo + 1, lo + 2), "%d och %d" % (lo + 1, lo + 2), "%d och %d" % (m // 2, m // 2 + 1)], "%d² = %d och %d² = %d, så √%d ligger mellan <b>%d och %d</b>." % (lo, lo * lo, lo + 1, (lo + 1) ** 2, m, lo, lo + 1))
        a = ri(2, 12)
        return MN("Beräkna √%d + √%d." % (a * a, (a + 1) ** 2), 2 * a + 1, [int(round((a * a + (a + 1) ** 2) ** 0.5)) if int(round((a * a + (a + 1) ** 2) ** 0.5)) != 2 * a + 1 else 2 * a + 3, a * a + (a + 1) ** 2, 2 * a], "√%d = %d och √%d = %d. %d + %d = <b>%d</b>." % (a * a, a, (a + 1) ** 2, a + 1, a, a + 1, 2 * a + 1))

    def lagar():
        a = ch(["a", "x", "2", "3", "5", "10"])
        m, n = ri(2, 9), ri(2, 7)
        k = ri(0, 3) if lv == 8 else ri(0, 1)
        if k == 0:
            return M("Skriv som en potens: %s%s · %s%s" % (a, sup(m), a, sup(n)), "%s%s" % (a, sup(m + n)), ["%s%s" % (a, sup(m * n)), "%s%s" % (a, sup(abs(m - n) or 1)) if m != n else "%s%s" % (a, sup(2 * m + 1)), "2%s%s" % (a, sup(m + n)) if a.isalpha() else "%d%s" % (int(a) ** 2, sup(m + n))], "Lika baser: addera exponenterna. %s%s · %s%s = %s%s = <b>%s%s</b>." % (a, sup(m), a, sup(n), a, sup("%d" % (m + n)) if False else "<sup>%d + %d</sup>" % (m, n), a, sup(m + n)))
        if k == 1:
            if m <= n:
                m, n = n + 1, m
            return M("Skriv som en potens: %s%s : %s%s" % (a, sup(m), a, sup(n)), "%s%s" % (a, sup(m - n)), ["%s%s" % (a, sup(m + n)), "%s%s" % (a, sup(m // n)) if m // n != m - n else "%s%s" % (a, sup(m * n)), "1%s" % sup(m - n)], "Lika baser: subtrahera exponenterna. %s<sup>%d − %d</sup> = <b>%s%s</b>." % (a, m, n, a, sup(m - n)))
        if k == 2:
            m, n = ri(2, 5), ri(2, 5)
            return M("Skriv som en potens: (%s%s)%s" % (a, sup(m), sup(n)), "%s%s" % (a, sup(m * n)), ["%s%s" % (a, sup(m + n)), "%s%s" % (a, sup(m ** n)) if m ** n != m * n else "%s%s" % (a, sup(m * n + 1)), "%s%s" % (a, sup(n))], "En potens upphöjd till en potens: multiplicera exponenterna, <b>%s%s</b>." % (a, sup(m * n)))
        b = ch([2, 3, 4, 5, 10])
        e = ri(-3, 0)
        v = F(1, b ** -e) if e < 0 else F(1)
        return M("Vad är %d%s?" % (b, sup(e)), fq(v), [d(-(b ** -e)) if e else "0", d(b * e) if e else str(b), fq(F(1, b * -e)) if e and F(1, b * -e) != v else "−1"], ("%d%s = 1/%d%s = <b>%s</b>." % (b, sup(e), b, sup(-e), fq(v))) if e else "Alla tal (utom 0) upphöjt till 0 är <b>1</b>.")

    def tio():
        e = ri(-6, 8)
        if e in (0, 1):
            return None
        v = F(10) ** e
        s = d(v)
        k = ri(0, 2)
        if k == 0:
            return M("Vilket tal är 10%s?" % sup(e), s, [d(v * 10), d(v / 10), d(10 * e) if e > 0 else d(-10 * -e)], ("10%s är en etta med %d nollor: <b>%s</b>." % (sup(e), e, s)) if e > 0 else ("10%s = 1 : 10%s, en etta på plats %d efter decimaltecknet: <b>%s</b>." % (sup(e), sup(-e), -e, s)))
        if k == 1:
            return M("Skriv %s som en tiopotens." % s, "10%s" % sup(e), ["10%s" % sup(-e), "10%s" % sup(e + 1), "10%s" % sup(e - 1)], "%s = <b>10%s</b>." % (s, sup(e)))
        m = ri(2, 9)
        return M("Beräkna %d · 10%s." % (m, sup(e)), d(m * v), [d(m * v * 10), d(m * v / 10), d(F(m) / v) if F(m) / v != m * v else d(m * v * 100)], "Flytta decimaltecknet %d steg åt %s: <b>%s</b>." % (abs(e), "höger" if e > 0 else "vänster", d(m * v)))

    if lv == 7:
        sets = [("Potensens värde", [(varde, 20)]), ("Potensform och tiopotenser", [(skriv, 20)]), ("Kvadratrötter", [(rot, 20)]),
                ("Multiplicera och dividera potenser", [(lagar, 20)]), ("Blandade potenser", [(varde, 7), (rot, 7), (skriv, 6)])]
        return unit("potenser-och-kvadratrotter", "T", "Potenser och kvadratrötter: bas, exponent och √", "Potenser och kvadratrötter",
                    "Tal i potensform för att uttrycka stora och små tal. Kvadrater och kvadratrötter. Metoder för beräkningar i huvudräkning, skriftliga metoder och med digitala verktyg.",
                    "Arbetsblad om potenser och kvadratrötter för årskurs 7: potensens värde, potensform, tiopotenser, kvadratrötter och enkla potenslagar. 100 uppgifter med facit.",
                    "5³ = 5 · 5 · 5 = 125", "Exponenten säger hur många gånger basen multipliceras.", sets,
                    ["I potensen 5³ är 5 basen och 3 exponenten. Det betyder 5 · 5 · 5 = 125, inte 5 · 3.",
                     "En tiopotens är 10 upphöjt till ett tal: 10⁴ = 10 000. Exponenten visar antalet nollor.",
                     "Kvadratroten ur ett tal är det positiva tal som multiplicerat med sig självt ger talet: √49 = 7 eftersom 7 · 7 = 49."],
                    [("Beräkna 2⁵", ["2 · 2 · 2 · 2 · 2"], "32"), ("Beräkna √81", ["9 · 9 = 81"], "9")],
                    [["5³ = 15", "5³ = 5 · 5 · 5 = 125"], ["√16 = 8", "4 · 4 = 16, alltså √16 = 4"], ["a² · a³ = a⁶", "Addera exponenterna: a⁵"]],
                    [("Vad är skillnaden mellan 3² och 2³?", "3² = 3 · 3 = 9 och 2³ = 2 · 2 · 2 = 8."), ("Har negativa tal en kvadratrot?", "Inte bland de reella talen. Inget tal multiplicerat med sig självt ger ett negativt tal."),
                     ("Varför skriver man i potensform?", "Det blir kortare och lättare att räkna med mycket stora och mycket små tal.")])
    sets = [("Potensens värde", [(varde, 20)]), ("Potenslagar", [(lagar, 20)]), ("Tiopotenser", [(tio, 20)]),
            ("Potensform", [(skriv, 20)]), ("Blandade uppgifter", [(lagar, 7), (tio, 7), (varde, 6)])]
    return unit("potenser", "T", "Potenser: potenslagar och tiopotenser med negativ exponent", "Potenser",
                "Tal i potensform för att uttrycka stora och små tal. Potenslagar för multiplikation och division av potenser med samma bas samt potens av potens. Tiopotenser med negativ exponent.",
                "Arbetsblad om potenser för årskurs 8: potensens värde, potenslagar, potens av potens, noll och negativa exponenter och tiopotenser. 100 uppgifter med facit.",
                "aᵐ · aⁿ = aᵐ⁺ⁿ", "Vid division subtraherar du exponenterna.", sets,
                ["Med samma bas adderar du exponenterna vid multiplikation: 2³ · 2⁴ = 2⁷. Vid division subtraherar du: 2⁷ : 2³ = 2⁴.",
                 "En potens av en potens: multiplicera exponenterna, (a²)³ = a⁶.",
                 "a⁰ = 1 och en negativ exponent betyder 1 delat med potensen: 10⁻³ = 1/10³ = 0,001."],
                [("2³ · 2⁴", ["Lika baser, addera 3 + 4"], "2⁷ = 128"), ("10⁻²", ["1 : 10² = 1 : 100"], "0,01")],
                [["2³ · 2⁴ = 2¹²", "Addera exponenterna: 2⁷"], ["10⁻² = −100", "10⁻² = 1/100 = 0,01"], ["5⁰ = 0", "5⁰ = 1"]],
                [("Varför är a⁰ = 1?", "a³ : a³ = 1, och enligt lagen är det a³⁻³ = a⁰."), ("Fungerar lagarna med olika baser?", "Nej, 2³ · 3² kan inte skrivas som en potens. Räkna ut var för sig: 8 · 9 = 72."),
                 ("Vad betyder 10⁻⁶?", "En miljondel: 0,000001.")])


# ============================================================ grundpotensform och prefix
def grundpotens(lv):
    def gp(m, e):
        return "%s · 10%s" % (d(m), sup(e))

    def stor():
        m = F(ri(11, 99), 10) if coin() else F(ri(101, 999), 100)
        e = ri(3, 9)
        n = m * 10 ** e
        return M("Skriv %s i grundpotensform." % num(int(n)), gp(m, e), [gp(m, e + 1), gp(m, e - 1), gp(m * 10, e - 1)], "Flytta decimaltecknet %d steg så att det blir ett tal mellan 1 och 10: <b>%s</b>." % (e, gp(m, e)))

    def liten():
        m = F(ri(11, 99), 10)
        e = -ri(2, 7)
        n = m * F(10) ** e
        return M("Skriv %s i grundpotensform." % d(n), gp(m, e), [gp(m, -e), gp(m, e + 1), gp(m, e - 1)], "Decimaltecknet flyttas %d steg åt höger, så exponenten blir %s: <b>%s</b>." % (-e, d(e), gp(m, e)))

    def tillbaka():
        m = F(ri(11, 99), 10)
        e = ch([-4, -3, -2, 3, 4, 5, 6])
        n = m * F(10) ** e
        return M("Skriv %s som ett vanligt tal." % gp(m, e), d(n), [d(n * 10), d(n / 10), d(m * 10 * e) if e > 0 else d(-m * e)], "Flytta decimaltecknet %d steg åt %s: <b>%s</b>." % (abs(e), "höger" if e > 0 else "vänster", d(n)))

    def prefix():
        P = [("kilo", "k", 3), ("mega", "M", 6), ("giga", "G", 9), ("milli", "m", -3), ("mikro", "µ", -6), ("nano", "n", -9)]
        nm, s, e = ch(P)
        unit_ = ch(["m", "g", "W", "byte"] if e > 0 else ["m", "g", "s"])
        if unit_ == "byte":
            s = s + "B"
        v = ri(2, 900)
        return M("Hur mycket är %d %s%s uttryckt i %s%s?" % (v, s if unit_ == "byte" else s, "" if unit_ == "byte" else unit_, "byte" if unit_ == "byte" else unit_, "" if True else ""),
                 gp(*norm(v, e)) + NB + ("byte" if unit_ == "byte" else unit_),
                 [gp(*norm(v, -e)) + NB + ("byte" if unit_ == "byte" else unit_), gp(*norm(v, e + 3)) + NB + ("byte" if unit_ == "byte" else unit_), gp(*norm(v, e - 3)) + NB + ("byte" if unit_ == "byte" else unit_)],
                 "%s betyder 10%s. %d · 10%s = <b>%s</b>." % (nm, sup(e), v, sup(e), gp(*norm(v, e))))

    def norm(v, e):
        v = F(v)
        while v >= 10:
            v /= 10
            e += 1
        return v, e

    def rakna():
        a, b = F(ri(2, 9)), F(ri(2, 9))
        e1, e2 = ri(2, 8), ri(-5, 6)
        if coin():
            m, e = norm(a * b, e1 + e2)
            return M("Beräkna (%s) · (%s) och svara i grundpotensform." % (gp(a, e1), gp(b, e2)), gp(m, e), [gp(*norm(a * b, e1 * e2)) if e1 * e2 != e1 + e2 else gp(m, e + 1), gp(m, e - 1), gp(*norm(a + b, e1 + e2))], "%s · %s = %s och 10%s · 10%s = 10%s: <b>%s</b>." % (d(a), d(b), d(a * b), sup(e1), sup(e2), sup(e1 + e2), gp(m, e)))
        A, B = gp(a, e1), gp(b, e1 + ri(1, 2))
        return M("Vilket tal är störst?", B, [A, gp(b, e1 - 1), gp(a, e1 - 2)], "Jämför först exponenterna. Störst exponent ger störst tal: <b>%s</b>." % B) if A != B else None

    sets = [("Stora tal", [(stor, 20)]), ("Små tal", [(liten, 20)]), ("Från grundpotensform till vanligt tal", [(tillbaka, 20)]),
            ("Prefix", [(prefix, 20)]), ("Räkna och jämför", [(rakna, 20)])]
    return unit("grundpotensform-och-prefix", "T", "Grundpotensform och prefix: stora och små tal", "Grundpotensform och prefix",
                "Tal i potensform för att uttrycka stora och små tal samt användning av prefix. Metoder för beräkningar med digitala verktyg och rimlighetsbedömning.",
                "Arbetsblad om grundpotensform och prefix för årskurs 8: skriv stora och små tal i grundpotensform, tillbaka till vanliga tal, prefix som kilo, mega och mikro. 100 uppgifter med facit.",
                "a · 10ⁿ där 1 ≤ a < 10", "Exponenten visar hur många steg decimaltecknet flyttas.", sets,
                ["Ett tal i grundpotensform skrivs som ett tal mellan 1 och 10 gånger en tiopotens: 45 000 = 4,5 · 10⁴.",
                 "Små tal får negativ exponent: 0,0032 = 3,2 · 10⁻³.",
                 "Prefix är tiopotenser med namn: kilo = 10³, mega = 10⁶, giga = 10⁹, milli = 10⁻³, mikro = 10⁻⁶ och nano = 10⁻⁹."],
                [("Skriv 45 000 i grundpotensform", ["4,5 är mellan 1 och 10", "Decimaltecknet flyttas 4 steg"], "4,5 · 10⁴"), ("Skriv 0,0032 i grundpotensform", ["3,2 är mellan 1 och 10", "3 steg åt höger"], "3,2 · 10⁻³")],
                [["45 000 = 45 · 10³", "45 är inte mellan 1 och 10: 4,5 · 10⁴"], ["0,0032 = 3,2 · 10³", "Små tal har negativ exponent: 3,2 · 10⁻³"], ["5 mm = 5 · 10³ m", "milli = 10⁻³: 5 · 10⁻³ m"]],
                [("Varför använder man grundpotensform?", "Mycket stora och små tal blir korta och lätta att jämföra, till exempel avståndet till solen 1,5 · 10¹¹ m."),
                 ("Hur visar miniräknaren grundpotensform?", "Ofta som 4.5E4, som betyder 4,5 · 10⁴."), ("Vad betyder µ?", "Det är den grekiska bokstaven my och betyder mikro, 10⁻⁶.")])


# ============================================================ reella tal
def reella(lv):
    def klass():
        k = ri(0, 4)
        a = ri(2, 30)

        def q(t, right, wrong):
            opts = sh([right] + wrong)
            return "%s %s?" % (t, ", ".join(opts[:-1]) + " och " + opts[-1])
        if k == 0:
            m = ch([n for n in range(2, 60) if int(n ** 0.5) ** 2 != n])
            r, w = "√%d" % m, ["√%d" % (a * a), fr(a, a + 1), d(F(ri(11, 99), 100))]
            return M(q("Vilket av talen är irrationellt:", r, w), r, w, "√%d går inte att skriva som ett bråk. Decimalerna tar aldrig slut och upprepas inte. <b>√%d</b> är irrationellt." % (m, m))
        if k == 1:
            r, w = "−%d" % a, [str(a + ri(0, 9)), fr(1, a), d(F(-ri(11, 99), 10))]
            return M(q("Vilket av talen är ett heltal men inte ett naturligt tal:", r, w), r, w, "De naturliga talen är 0, 1, 2, 3, … De hela talen har också med de negativa: <b>−%d</b>." % a)
        if k == 2:
            r = fr(a, a + 2) if math.gcd(a, a + 2) == 1 else d(F(a, 10))
            w = ["π", "√%d" % ch([2, 3, 5, 7, 11]), "√%d" % ch([13, 17, 19, 23, 29, 31])]
            return M(q("Vilket av talen är rationellt:", r, w), r, w, "Ett rationellt tal kan skrivas som ett bråk med heltal. Det kan inte π eller √ ur ett tal som inte är en kvadrat.")
        if k == 3:
            n = ch([2, 3, 5, 6, 7, 8, 10, 11])
            S_ = [("Alla heltal är rationella tal", ["Alla rationella tal är heltal", "√%d är ett rationellt tal" % n, "π = 3,14 exakt"]),
                  ("√%d är ett heltal" % (n * n), ["√%d är irrationellt" % (n * n), "√%d är ett rationellt tal" % n, "−%d är ett naturligt tal" % n]),
                  ("−%d är ett rationellt tal" % n, ["−%d är ett naturligt tal" % n, "√%d är ett heltal" % n, "%s är irrationellt" % fr(1, n)])]
            r, w = ch(S_)
            return M("Vilket påstående är sant?", r, w, "<b>%s</b>." % r)
        p = ch([(1, 3, "0,333…"), (2, 3, "0,666…"), (1, 9, "0,111…"), (4, 9, "0,444…"), (1, 6, "0,1666…"), (5, 9, "0,555…"), (7, 9, "0,777…"), (5, 6, "0,8333…"), (2, 9, "0,222…"), (8, 9, "0,888…"), (1, 11, "0,0909…"), (1, 12, "0,08333…")])
        return M("Vilket bråk är lika med det periodiska decimaltalet %s?" % p[2], fr(p[0], p[1]), [fr(p[0], 10), fr(p[0] * 3 if p[1] == 9 else p[0] + 1, p[1] + 1), fr(p[1], p[0] * 10)], "%d : %d = %s, alltså <b>%s</b>." % (p[0], p[1], p[2], fr(p[0], p[1])))

    def rotter():
        k = ri(0, 2)
        if k == 0:
            m = ri(2, 150)
            if int(m ** 0.5) ** 2 == m:
                return None
            lo = int(m ** 0.5)
            return M("Mellan vilka heltal ligger √%d?" % m, "%d och %d" % (lo, lo + 1), ["%d och %d" % (lo + 1, lo + 2), "%d och %d" % (lo - 1, lo) if lo > 1 else "%d och %d" % (lo + 2, lo + 3), "%d och %d" % (m // 2, m // 2 + 1) if m // 2 > lo + 2 else "%d och %d" % (lo + 3, lo + 4)], "%d² = %d och %d² = %d: <b>%d och %d</b>." % (lo, lo * lo, lo + 1, (lo + 1) ** 2, lo, lo + 1))
        if k == 1:
            m = ch([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24])
            v = m ** 0.5
            return M("Vad är √%d avrundat till en decimal?" % m, rd(v, 1), [rd(v + 0.1, 1), rd(v - 0.1, 1), rd(m / 2, 1) if rd(m / 2, 1) not in (rd(v, 1), rd(v + 0.1, 1), rd(v - 0.1, 1)) else rd(v + 0.3, 1)], "√%d ≈ %s, avrundat <b>%s</b>." % (m, rd(v, 3), rd(v, 1)))
        a, b = ri(2, 9), ri(2, 9)
        return MN("Beräkna √%d · √%d." % (a * a * b if False else a, a), a, [a * a, 2 * a, a + a * a], "√%d · √%d = √%d = <b>%d</b>." % (a, a, a * a, a))

    def ordna():
        vals = [("π", math.pi), ("√%d" % ri(2, 30), None), (d(F(ri(10, 60), 10)), None), (ch([fr(a, b) for a in range(1, 30) for b in range(2, 10) if math.gcd(a, b) == 1]), None)]
        out = []
        for s, v in vals:
            if v is None:
                if s.startswith("√"):
                    v = int(s[1:]) ** 0.5
                elif "fr" in s:
                    import re as _re
                    a, b = map(int, _re.findall(r">(\d+)<", s))
                    v = a / b
                else:
                    v = float(s.replace(",", "."))
            out.append((s, v))
        vs = [v for _, v in out]
        if len(set(round(v, 2) for v in vs)) < 4:
            return None
        k = coin()
        best = max(out, key=lambda t: t[1]) if k else min(out, key=lambda t: t[1])
        return M("Vilket tal är %s: %s?" % ("störst" if k else "minst", lista(s for s, _ in out)), best[0], [s for s, _ in out if s != best[0]], "Skriv talen som decimaltal: %s. %s är <b>%s</b>." % (", ".join("%s ≈ %s" % (s, rd(v, 2)) for s, v in out), "Störst" if k else "Minst", best[0]))

    def tallinje():
        m = ri(2, 80)
        if int(m ** 0.5) ** 2 == m:
            return None
        v = m ** 0.5
        lo = int(v)
        return M("Vilket tal är närmast √%d?" % m, d(F(int(v * 10 + 0.5), 10)), [d(F(lo, 1)) if F(lo) != F(int(v * 10 + 0.5), 10) else d(F(lo + 1)), d(F(m, 2)) if F(m, 2) != F(int(v * 10 + 0.5), 10) else d(F(m + 1, 2)), d(F(int(v * 10 + 0.5), 10) + F(5, 10))], "√%d ≈ %s. Närmast är <b>%s</b>." % (m, rd(v, 2), d(F(int(v * 10 + 0.5), 10))))

    def pi_():
        r = ri(2, 15)
        k = ri(0, 2)
        if k == 0:
            return M("Vilket av talen är π avrundat till två decimaler?", "3,14", ["3,15", "3,41", "3,12"], "π = 3,14159… Avrundat till två decimaler <b>3,14</b>.")
        if k == 1:
            return M("En cirkel har diametern %d cm. Vilket är ett exakt uttryck för omkretsen?" % (2 * r), "%dπ cm" % (2 * r), ["%dπ cm" % r, "%dπ cm" % (4 * r * r), "%dπ cm²" % (r * r)], "O = π · d = <b>%dπ cm</b>. Ett exakt svar behåller π." % (2 * r))
        return M("Vilket påstående om π är sant?", "π är ett irrationellt tal", ["π = 22/7 exakt", "π är ett heltal", "π har sju decimaler"], "Decimalerna i π tar aldrig slut och upprepas inte. <b>π är irrationellt</b>. 22/7 är bara en närmevärde.")

    sets = [("Talmängder", [(klass, 20)]), ("Kvadratrötter", [(rotter, 20)]), ("Ordna reella tal", [(ordna, 20)]),
            ("Tallinjen", [(tallinje, 20)]), ("π och exakta svar", [(pi_, 8), (rotter, 6), (klass, 6)])]
    return unit("reella-tal", "T", "Reella tal: rationella och irrationella tal", "Reella tal",
                "Reella tal och deras egenskaper samt deras användning i vardagliga och matematiska situationer. Naturliga tal, heltal, rationella och irrationella tal.",
                "Arbetsblad om reella tal för årskurs 9: naturliga tal, heltal, rationella och irrationella tal, kvadratrötter, periodiska decimaltal och π. 100 uppgifter med facit.",
                "Naturliga ⊂ hela ⊂ rationella ⊂ reella", "Irrationella tal kan inte skrivas som bråk.", sets,
                ["De naturliga talen är 0, 1, 2, 3, … De hela talen har också med de negativa talen.",
                 "Ett rationellt tal kan skrivas som ett bråk med heltal, till exempel 3/4, −2 och 0,333… = 1/3.",
                 "Ett irrationellt tal har oändligt många decimaler som inte upprepas, till exempel √2 och π. Alla dessa tal tillsammans är de reella talen."],
                [("Är √2 rationellt?", ["√2 = 1,41421356…", "Decimalerna upprepas aldrig"], "Nej, irrationellt"), ("Mellan vilka heltal ligger √40?", ["6² = 36 och 7² = 49"], "6 och 7")],
                [["0,333… är irrationellt", "0,333… = 1/3 är rationellt"], ["√9 är irrationellt", "√9 = 3 är ett heltal"], ["π = 3,14", "π ≈ 3,14 men har oändligt många decimaler"]],
                [("Är alla rotuttryck irrationella?", "Nej. √25 = 5. Bara rötter ur tal som inte är kvadrater (bland heltalen) är irrationella."),
                 ("Vilka tal är inte reella?", "Till exempel √(−1). Sådana tal läser man om på gymnasiet."), ("Är periodiska decimaltal rationella?", "Ja, de kan alltid skrivas som bråk: 0,666… = 2/3.")])


UNITS = {"negativa-tal": negativa, "prioriteringsregler": prioritering, "delbarhet-och-primtal": delbarhet, "brak": brak,
         "decimaltal": decimaltal, "potenser-och-kvadratrotter": potenser, "potenser": potenser, "grundpotensform-och-prefix": grundpotens,
         "reella-tal": reella}
