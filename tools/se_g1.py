# -*- coding: utf-8 -*-
"""Sverige gymnasiet: Matematik nivå 1c（Gy25）"""
import math
from fractions import Fraction as F
from se_g import (take, nz, xp, pol, U, graf, gen, MQ, lista, ri, ch, sh, cap, fr, fq, d, par, sg, M, MN, rd, sup, tab, K, num, kr, NB, MIN, coin, expr, lin,
                  kosy, kurve, figure, fig, wrap, text, line, INK, GREEN, FILL, RED, BLUE)
import se_h_a as HA
import se_h_b as HB
import se_h_c as HC
import se_h_e as HE


# ============================================================ potenser och rötter
def potenser():
    lagar = take(HA.potenser, 8, "lagar")
    tio = take(HA.potenser, 8, "tio")

    def rot():
        b = ch([2, 3, 4, 5, 10])
        n = ch([2, 3, 4])
        v = b ** n
        if v > 10000:
            return None
        k = ri(0, 1)
        if k == 0:
            return MN("Beräkna %s%s." % (num(v), sup("1/%d" % n)), b, [F(v, n), v ** 2 if v < 100 else b + 1, b * n], "a<sup>1/%d</sup> är det tal som upphöjt till %d ger a: %d%s = %s. Svar: <b>%d</b>." % (n, n, b, sup(n), num(v), b))
        m = ri(2, 3)
        if n == 2 and m == 2:
            m = 3
        r = b ** m
        return MN("Beräkna %s%s." % (num(v), sup("%d/%d" % (m, n))), r, [b, F(v * m, n), b ** (m + 1)], "%s%s = (%s%s)%s = %d%s = <b>%s</b>." % (num(v), sup("%d/%d" % (m, n)), num(v), sup("1/%d" % n), sup(m), b, sup(m), num(r)))

    def neg():
        b = ch([2, 3, 4, 5, 10])
        e = ri(1, 4)
        v = F(1, b ** e)
        return M("Skriv %d%s som ett bråk." % (b, sup(-e)), fq(v), [d(-(b ** e)), fq(F(1, b * e)) if b * e != b ** e else fq(v * 2), fq(F(b, e)) if F(b, e) != v else fq(v / 2)], "En negativ exponent betyder 1 delat med potensen: 1/%d%s = <b>%s</b>." % (b, sup(e), fq(v)))

    def forenkla():
        a, b, c = ri(2, 6), ri(2, 6), ri(1, 4)
        k = ri(0, 2)
        if k == 0:
            return M("Förenkla (x%s)%s · x%s." % (sup(a), sup(b), sup(c)), xp(a * b + c) if a * b + c < 6 else "x" + sup(a * b + c), ["x" + sup(a + b + c), "x" + sup(a * b * c), "x" + sup(a * b - c)], "(x%s)%s = x%s. Sedan x%s · x%s = <b>x%s</b>." % (sup(a), sup(b), sup(a * b), sup(a * b), sup(c), sup(a * b + c)))
        if k == 1:
            if a + b <= c:
                return None
            return M("Förenkla x%s · x%s / x%s." % (sup(a), sup(b), sup(c)), "x" + sup(a + b - c), ["x" + sup(a * b - c), "x" + sup(a + b + c), "x" + sup(F(a * b, c)) if F(a * b, c).denominator == 1 and a * b // c != a + b - c else "x" + sup(a + b - c + 1)], "%d + %d − %d = %d: <b>x%s</b>." % (a, b, c, a + b - c, sup(a + b - c)))
        m = ri(2, 5)
        return M("Förenkla (%dx%s)%s." % (m, sup(a), sup(2)), "%dx%s" % (m * m, sup(2 * a)), ["%dx%s" % (m * 2, sup(2 * a)), "%dx%s" % (m * m, sup(a + 2)), "%dx%s" % (m, sup(2 * a))], "Båda faktorerna upphöjs: %d² · x%s = <b>%dx%s</b>." % (m, sup(2 * a), m * m, sup(2 * a)))

    sets = [("Potenslagar", [(lagar, 20)]), ("Negativa exponenter", [(neg, 12), (tio, 8)]), ("Rötter som potenser", [(rot, 20)]), ("Förenkla uttryck", [(forenkla, 20)]), ("Blandat", [(forenkla, 10), (lagar, 10)])]
    return U("potenser-och-rotter", "AF", "Potenser och rötter: potenslagar och rationella exponenter", "Potenser och rötter",
             "Potensregler för heltal och rationella exponenter. Hantering av potensuttryck och rötter.",
             "Uppgifter om potenser och rötter för Matematik 1c: potenslagar, negativa exponenter, rötter som potenser med rationella exponenter och att förenkla uttryck. 100 uppgifter med facit.",
             "a^(1/n) = n:te roten ur a", "a^m · a^n = a^(m+n) och (a^m)^n = a^(mn).", sets,
             ["Potenslagarna: aᵐ · aⁿ = aᵐ⁺ⁿ, aᵐ/aⁿ = aᵐ⁻ⁿ och (aᵐ)ⁿ = aᵐⁿ. Dessutom a⁰ = 1 och a⁻ⁿ = 1/aⁿ.",
              "En rot kan skrivas som en potens: √a = a<sup>1/2</sup> och ∛a = a<sup>1/3</sup>.",
              "a<sup>m/n</sup> = (a<sup>1/n</sup>)ᵐ. Ta roten först så blir talen mindre: 8<sup>2/3</sup> = 2² = 4."],
             [("Beräkna 27<sup>2/3</sup>", ["27<sup>1/3</sup> = 3", "3² = 9"], "9"), ("Förenkla (x³)² · x", ["x⁶ · x"], "x⁷")],
             [["a² · a³ = a⁶", "Addera exponenterna: a⁵"], ["2⁻³ = −8", "2⁻³ = 1/8"], ["16<sup>1/2</sup> = 8", "16<sup>1/2</sup> = √16 = 4"]],
             [("Vad betyder en exponent som är ett bråk?", "Nämnaren anger roten och täljaren potensen."), ("Varför är a⁰ = 1?", "aⁿ/aⁿ = 1 och enligt lagen aⁿ⁻ⁿ = a⁰."), ("Gäller lagarna för negativa baser?", "Ja för heltalsexponenter, men rötter ur negativa tal kräver försiktighet.")])


# ============================================================ algebra och faktorisering
def algebra():
    multin = take(HB.parenteser, 8, "multin")
    minus = take(HB.parenteser, 8, "minus")
    tva = take(HB.parenteser, 8, "tva")
    bryt = take(HB.parenteser, 8, "bryt")

    def brak():
        a = ri(2, 9)
        b = nz(-9, 9)
        g = ri(2, 6)
        if coin():
            q = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%d</span></span>" % (expr([(g * a, "x"), (g * b, "")]), g)
            r = expr([(a, "x"), (b, "")])
            return M("Förenkla %s." % q, r, [expr([(g * a, "x"), (b, "")]), expr([(a, "x"), (g * b, "")]), expr([(a * g, "")]) + "x" if False else expr([(a + b, "x")])], "Bryt ut %d i täljaren och förkorta: <b>%s</b>." % (g, r))
        q = "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (expr([(1, "x²"), (b, "x")]), "x")
        r = expr([(1, "x"), (b, "")])
        return M("Förenkla %s, x ≠ 0." % q, r, [expr([(1, "x²"), (b, "")]), expr([(1, "x"), (b, "x")]), expr([(1, "x²"), (b, "x")]) if False else expr([(b, "x"), (1, "")])], "Bryt ut x i täljaren och förkorta med x: <b>%s</b>." % r)

    def varde():
        a, b = nz(-5, 5), nz(-9, 9)
        x = nz(-5, 5)
        q = "(x %s %d)² − %s" % ("+" if a > 0 else "−", abs(a), expr([(b, "x")]))
        v = (x + a) ** 2 - b * x
        return MN("Beräkna värdet av %s då x = %s." % (q, sg(x)), v, [x * x + a * a - b * x, (x + a) * 2 - b * x, v + 2 * a * x if 2 * a * x else v + 1], "(%s %s %d)² − %s · %s = %d − %s = <b>%s</b>." % (sg(x), "+" if a > 0 else "−", abs(a), sg(b), par(x), (x + a) ** 2, par(b * x), d(v)))

    sets = [("Multiplicera in", [(multin, 20)]), ("Minus framför parentes", [(minus, 20)]), ("Multiplicera parenteser", [(tva, 20)]), ("Faktorisera", [(bryt, 20)]), ("Förkorta och beräkna", [(brak, 10), (varde, 10)])]
    return U("algebra-och-faktorisering", "AF", "Algebra: multiplicera, faktorisera och förenkla uttryck", "Algebra och faktorisering",
             "Hantering av algebraiska uttryck: multiplicering av uttryck, faktorisering och förenkling av rationella uttryck.",
             "Uppgifter om algebra för Matematik 1c: multiplicera in, minus framför parentes, multiplicera parenteser, faktorisera och förkorta uttryck. 100 uppgifter med facit.",
             "Faktorisera = bryt ut det gemensamma", "Kontrollera genom att multiplicera in igen.", sets,
             ["Multiplicera in: varje term i den ena parentesen multipliceras med varje term i den andra.",
              "Faktorisera genom att bryta ut den största gemensamma faktorn: 6x² + 9x = 3x(2x + 3).",
              "Ett bråk med uttryck kan förkortas om täljare och nämnare har en gemensam faktor: (4x + 8)/4 = x + 2."],
             [("(x + 3)(x − 5)", ["x² − 5x + 3x − 15"], "x² − 2x − 15"), ("Faktorisera 10x² − 15x", ["Gemensamt: 5x"], "5x(2x − 3)")],
             [["(4x + 8)/4 = x + 8", "Båda termerna delas med 4: x + 2"], ["−(x − 3) = −x − 3", "Tecknen byts: −x + 3"], ["Bryter inte ut hela faktorn", "Bryt ut den största gemensamma faktorn"]],
             [("Varför faktoriserar man?", "För att förenkla bråk och lösa ekvationer, till exempel med nollproduktmetoden."), ("Får man förkorta termer?", "Nej, bara faktorer. (x + 2)/2 är inte x + 1."),
              ("Hur kontrollerar jag?", "Multiplicera in faktoriseringen. Du ska få tillbaka uttrycket.")])


# ============================================================ ekvationer och formler
def ekvationer():
    bada = take(HB.ekvationer, 8, "bada")
    paren = take(HB.ekvationer, 8, "parentes")
    brak_ = take(HB.ekvationer, 8, "brak_")
    losut = take(HB.formler, 8, "losut")
    bak = take(HB.formler, 8, "baklanges")

    def namnare():
        x = nz(-9, 12)
        a, b = ri(2, 6), ri(2, 6)
        if a == b:
            return None
        c = F(x, a) + F(x, b)
        if c.denominator != 1:
            return None
        return M("Lös ekvationen x/%d + x/%d = %s." % (a, b, d(c)), "x = %s" % d(x), ["x = %s" % sg(c * (a + b) / 2) if c * (a + b) / 2 != x else "x = %s" % d(x + 1), "x = %s" % sg(c * a * b), "x = %s" % d(-x) if x else "x = 1"],
                 "Multiplicera med %d: %dx + %dx = %s, alltså %dx = %s och <b>x = %s</b>." % (a * b, b, a, d(c * a * b), a + b, d(c * a * b), d(x)))

    sets = [("x i båda leden", [(bada, 20)]), ("Ekvationer med parenteser", [(paren, 20)]), ("Ekvationer med bråk", [(brak_, 10), (namnare, 10)]), ("Lös ut en variabel", [(losut, 12), (bak, 8)]), ("Formler i tillämpningar", [(bak, 12), (namnare, 8)])]
    return U("ekvationer-och-formler", "AF", "Ekvationer och formler: lös linjära ekvationer och lös ut variabler", "Ekvationer och formler",
             "Formelhantering och linjära ekvationer. Algebraiska metoder för att lösa ekvationer och för att skriva om formler.",
             "Uppgifter om ekvationer och formler för Matematik 1c: x i båda leden, parenteser, bråk, lösa ut en variabel och formler i tillämpningar. 100 uppgifter med facit.",
             "Samma operation i båda leden", "Multiplicera bort nämnarna först.", sets,
             ["Lös linjära ekvationer genom att göra samma sak i båda leden tills x står ensamt.",
              "Finns det bråk kan du multiplicera båda leden med minsta gemensamma nämnaren.",
              "Att lösa ut en variabel ur en formel är samma sak som att lösa en ekvation med bokstäver."],
             [("x/2 + x/3 = 10", ["Multiplicera med 6: 3x + 2x = 60", "5x = 60"], "x = 12"), ("Lös ut r ur A = πr²", ["r² = A/π"], "r = √(A/π)")],
             [["Multiplicerar bara ena termen med nämnaren", "Alla termer i båda leden multipliceras"], ["Glömmer att byta tecken när termen flyttas", "Subtrahera från båda leden"], ["Delar med noll", "Kontrollera att du inte delar med något som kan vara 0"]],
             [("Hur kontrollerar jag en lösning?", "Sätt in den i ursprungsekvationen."), ("Kan en linjär ekvation sakna lösning?", "Ja, till exempel x + 1 = x + 2."), ("Varför lösa ut variabler?", "För att kunna räkna ut den storhet du söker direkt.")])


# ============================================================ funktioner
def funktioner():
    def varde():
        a, b, c = nz(-3, 3), nz(-6, 6), nz(-9, 9)
        x = nz(-4, 5)
        f = pol({2: a, 1: b, 0: c})
        v = a * x * x + b * x + c
        return MN("f(x) = %s. Beräkna f(%s)." % (f, sg(x)), v, [a * x * x - b * x + c, -a * x * x + b * x + c, (a * x) ** 2 + b * x + c if a != 1 and a != -1 else v + 2], "f(%s) = %s · %s² %s %s · %s %s %d = <b>%s</b>." % (sg(x), sg(a), par(x), "+" if b > 0 else "−", d(abs(b)), par(x), "+" if c > 0 else "−", abs(c), d(v)))

    def dv():
        k = ri(0, 3)
        if k == 0:
            a = ri(-5, 3)
            b = a + ri(3, 8)
            m, kk = nz(-3, 3), nz(-2, 2)
            ys = sorted([kk * a + m, kk * b + m])
            return M("Funktionen f(x) = %s har definitionsmängden %s ≤ x ≤ %s. Vilken är värdemängden?" % (expr([(kk, "x"), (m, "")]), sg(a), sg(b)), "%s ≤ y ≤ %s" % (sg(ys[0]), sg(ys[1])),
                     ["%s ≤ y ≤ %s" % (sg(a), sg(b)), "%s ≤ y ≤ %s" % (sg(ys[0] - 1), sg(ys[1] + 1)), "%s ≤ y ≤ %s" % (sg(-ys[1]), sg(-ys[0]))], "f(%s) = %s och f(%s) = %s. Värdemängden är <b>%s ≤ y ≤ %s</b>." % (sg(a), sg(kk * a + m), sg(b), sg(kk * b + m), sg(ys[0]), sg(ys[1])))
        if k == 1:
            c = nz(-5, 5)
            return M("Vilken är värdemängden för f(x) = x² %s %d?" % ("+" if c > 0 else "−", abs(c)), "y ≥ %s" % sg(c), ["y ≤ %s" % sg(c), "alla reella tal", "y ≥ 0" if c else "y ≥ 1"], "x² är aldrig negativt, så minsta värdet är %s: <b>y ≥ %s</b>." % (sg(c), sg(c)))
        if k == 2:
            p = ch([10, 12, 15, 20, 25])
            n = ch([20, 30, 40, 50])
            return M("En biljett kostar %d kr. Kostnaden K(x) kr för x biljetter är K(x) = %dx. Högst %d biljetter finns. Vilken är en rimlig definitionsmängd?" % (p, p, n), "x = 0, 1, 2, …, %d" % n, ["0 ≤ x ≤ %d" % (p * n), "alla reella tal", "x ≥ %d" % n], "Antalet biljetter är ett heltal från 0 till %d: <b>x = 0, 1, 2, …, %d</b>." % (n, n))
        a = nz(-6, 6)
        return M("För vilka x är funktionen f(x) = √(x %s %d) definierad?" % ("+" if a > 0 else "−", abs(a)), "x ≥ %s" % sg(-a), ["x ≥ %s" % sg(a), "x > 0", "x ≤ %s" % sg(-a)], "Under rottecknet får det inte vara negativt: x %s %d ≥ 0 ger <b>x ≥ %s</b>." % ("+" if a > 0 else "−", abs(a), sg(-a)))

    def graflas():
        a, c = ch([1, -1, F(1, 2), -F(1, 2)]), nz(-3, 3)
        h = nz(-2, 2)
        f = lambda x: a * (x - h) ** 2 + c
        pic = graf(f, (-5, 5, 1), (-6, 6, 1), (), "graf till en funktion")
        k = ri(0, 1)
        if k == 0:
            x = ri(-2, 2) + h
            if not -5 <= x <= 5 or abs(f(x)) > 6 or F(f(x)).denominator != 1:
                return None
            return MN("Grafen visar y = f(x). Läs av f(%s)." % sg(x) + pic, F(f(x)), [F(f(x)) + 1, x, -F(f(x)) if f(x) else 2], "Gå till x = %s och läs av y: <b>%s</b>." % (sg(x), d(F(f(x)))))
        return M("Grafen visar y = f(x). Vilket är %s värde?" % ("funktionens minsta" if a > 0 else "funktionens största") + pic, "y = %s" % sg(c), ["y = %s" % sg(h) if h != c else "y = %s" % sg(c + 1), "y = %s" % sg(-c), "y = 0" if c else "y = 1"], "Vändpunkten ligger i (%s, %s). %s är <b>y = %s</b>." % (sg(h), sg(c), "Minsta värdet" if a > 0 else "Största värdet", sg(c)))

    def los():
        k, m = nz(-4, 4), nz(-8, 8)
        x = nz(-6, 6)
        a = k * x + m
        if abs(a) > 5 or abs(k) > 3:
            return None
        pic = kosy([(k, m, BLUE, "")], [], -6, 6, 20, "graf till f")
        return M("Grafen visar f(x) = %s. Lös ekvationen f(x) = %s grafiskt." % (expr([(k, "x"), (m, "")]), sg(a)) + pic, "x = %s" % sg(x), ["x = %s" % sg(a), "x = %s" % sg(-x), "x = %s" % sg(x + 1)], "Gå från y = %s vågrätt till linjen och läs av x: <b>x = %s</b>." % (sg(a), sg(x)))

    def ord_():
        P = [("Vad betyder f(3) = 7?", "Funktionens värde är 7 när x = 3", ["Funktionens värde är 3 när x = 7", "f gånger 3 är 7", "Grafen skär y-axeln i 7"]),
             ("Vad är definitionsmängden?", "Alla x-värden som funktionen är definierad för", ["Alla y-värden funktionen kan anta", "Funktionens största värde", "Var grafen skär x-axeln"]),
             ("Vad är värdemängden?", "Alla y-värden som funktionen kan anta", ["Alla x-värden funktionen är definierad för", "Funktionens nollställen", "Funktionens lutning"]),
             ("Vilket samband är inte en funktion av x?", "x² + y² = 25", ["y = 3x − 1", "y = x²", "y = 2ˣ"]),
             ("Vad är ett nollställe till f?", "Ett x där f(x) = 0", ["Värdet f(0)", "Ett x där f(x) är störst", "Var grafen skär y-axeln"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    sets = [("Funktionsvärden", [(varde, 20)]), ("Definitions- och värdemängd", [(dv, 20)]), ("Läs av grafen", [(graflas, 20)]), ("Lös f(x) = a grafiskt", [(los, 20)]), ("Begrepp", [(ord_, 5), (varde, 8), (dv, 7)])]
    return U("funktioner", "AF", "Funktioner: funktionsvärde, definitionsmängd och värdemängd", "Funktioner",
             "Begreppen funktion, definitionsmängd och värdemängd samt olika representationer av funktioner. Funktionsvärden och grafiska metoder för att lösa ekvationer av typen f(x) = a.",
             "Uppgifter om funktioner för Matematik 1c: funktionsvärden, definitionsmängd och värdemängd, läsa av grafer och lösa f(x) = a grafiskt. 100 uppgifter med facit.",
             "Varje x ger exakt ett f(x)", "Definitionsmängd x-värden, värdemängd y-värden.", sets,
             ["En funktion ger exakt ett värde f(x) för varje x i definitionsmängden.",
              "Definitionsmängden är de x-värden man får använda. Värdemängden är de y-värden funktionen kan anta.",
              "f(x) = a löser du grafiskt genom att dra en vågrät linje y = a och läsa av x där den skär grafen."],
             [("f(x) = 2x² − 3. Beräkna f(−2)", ["2 · 4 − 3"], "5"), ("f(x) = √(x − 4)", ["x − 4 ≥ 0"], "Definitionsmängd x ≥ 4")],
             [["f(−2) med −2² = −4", "(−2)² = 4"], ["Blandar ihop definitions- och värdemängd", "Definitionsmängden gäller x, värdemängden y"], ["Läser av y i stället för x", "Lösningen till f(x) = a är x-värdet"]],
             [("Vad skiljer en funktion från en ekvation?", "En funktion beskriver ett samband. En ekvation är ett påstående om likhet som har lösningar."), ("Kan två x ge samma y?", "Ja, men ett x får bara ge ett y."), ("Vilka representationer finns?", "Ord, formel, tabell och graf.")])


# ============================================================ linjära funktioner
def linjara():
    km = take(HC.linjara, 9, "km")
    tva = take(HC.linjara, 9, "tva")
    gr = take(HC.ratalinjen, 9, "graf")
    tvaR = take(HC.ratalinjen, 9, "tva")
    kp = take(HC.ratalinjen, 9, "kpunkt")
    sk = take(HC.ratalinjen, 9, "skarning")

    def vinkelrat():
        k = ch([F(2), F(3), F(-2), F(1, 2), F(-1, 3), F(4), F(-1, 4), F(2, 3), F(-3, 2), F(1), F(-1)])
        m = nz(-6, 6)
        k2 = -1 / k
        return M("Vilket k-värde har en linje som är vinkelrät mot %s?" % lin(k, m), "k = %s" % sg(k2), ["k = %s" % sg(-k2), "k = %s" % sg(k) if k != k2 else "k = 0", "k = %s" % sg(1 / k2) if 1 / k2 != k2 and 1 / k2 != -k2 else "k = 2"], "För vinkelräta linjer gäller k₁ · k₂ = −1: %s · %s = −1. <b>k = %s</b>." % (par(k), par(k2), sg(k2)))

    sets = [("k- och m-värde", [(km, 10), (tva, 10)]), ("Räta linjen från graf", [(gr, 20)]), ("Bestäm linjens ekvation", [(tvaR, 10), (kp, 10)]), ("Skärningspunkter", [(sk, 20)]), ("Parallella och vinkelräta linjer", [(vinkelrat, 20)])]
    return U("linjara-funktioner", "AF", "Linjära funktioner: räta linjen, skärning och vinkelräta linjer", "Linjära funktioner",
             "Linjära funktioner och räta linjens ekvation. Parallella och vinkelräta linjer samt skärningspunkter.",
             "Uppgifter om linjära funktioner för Matematik 1c: k- och m-värde, linjens ekvation från graf och punkter, skärningspunkter och vinkelräta linjer. 100 uppgifter med facit.",
             "y = kx + m och k₁ · k₂ = −1", "Parallella linjer har samma k-värde.", sets,
             ["En rät linje har ekvationen y = kx + m. k = Δy/Δx är lutningen och m skärningen med y-axeln.",
              "Parallella linjer har samma k-värde. Vinkelräta linjer har k₁ · k₂ = −1.",
              "Skärningspunkten mellan två linjer får du genom att sätta uttrycken lika."],
             [("Genom (2, 1) och (4, 7)", ["k = 6/2 = 3", "1 = 3 · 2 + m, m = −5"], "y = 3x − 5"), ("Vinkelrät mot y = 2x + 1", ["k₂ = −1/2"], "k = −1/2")],
             [["Vinkelrät mot k = 2 ger k = −2", "k₂ = −1/2"], ["k = Δx/Δy", "k = Δy/Δx"], ["Skärning med x-axeln: sätt x = 0", "Sätt y = 0"]],
             [("Vad betyder Δ?", "Skillnad eller förändring, till exempel Δy = y₂ − y₁."), ("Har en lodrät linje ett k-värde?", "Nej, dess ekvation är x = a."), ("Hur hittar jag m?", "Sätt in en punkt i y = kx + m.")])


# ============================================================ linjära olikheter
def olikheter():
    los = take(HB.olikheter, 8, "los")
    neg = take(HB.olikheter, 8, "neg")
    hel = take(HB.olikheter, 8, "heltal")

    def graf_():
        k1, m1, k2, m2 = nz(-2, 2), nz(-3, 3), nz(-2, 2), nz(-3, 3)
        if k1 == k2:
            return None
        x = F(m2 - m1, k1 - k2)
        if x.denominator != 1 or abs(x) > 4 or abs(k1 * x + m1) > 5:
            return None
        pic = kosy([(k1, m1, BLUE, "f"), (k2, m2, RED, "g")], [], -6, 6, 20, "två linjer f och g")
        r = "x > %s" % sg(x) if k1 > k2 else "x < %s" % sg(x)
        return M("Graferna till f(x) = %s och g(x) = %s visas. För vilka x är f(x) > g(x)?" % (expr([(k1, "x"), (m1, "")]), expr([(k2, "x"), (m2, "")])) + pic, r, ["x < %s" % sg(x) if k1 > k2 else "x > %s" % sg(x), "x > %s" % sg(k1 * x + m1) if k1 * x + m1 != x else "x > %s" % sg(x + 1), "x = %s" % sg(x)],
                 "Linjerna skär varandra i x = %s. f ligger över g när <b>%s</b>." % (sg(x), r))

    def dubbel():
        a = nz(-5, 5)
        lo, hi = ri(-9, 0), ri(1, 12)
        b = ri(2, 4)
        return M("Lös olikheten %d ≤ %s ≤ %d." % (lo * b + a, expr([(b, "x"), (a, "")]), hi * b + a), "%s ≤ x ≤ %s" % (sg(lo), sg(hi)), ["%s ≤ x ≤ %s" % (sg(lo * b), sg(hi * b)), "%s ≤ x ≤ %s" % (sg(lo + a), sg(hi + a)) if a else "%s ≤ x ≤ %s" % (sg(lo - 1), sg(hi + 1)), "%s ≤ x ≤ %s" % (sg(hi), sg(lo)) if False else "x ≥ %s" % sg(lo)],
                 "Subtrahera %s och dela med %d i alla tre leden: <b>%s ≤ x ≤ %s</b>." % (sg(a), b, sg(lo), sg(hi)))

    sets = [("Lös olikheter", [(los, 20)]), ("Multiplicera med negativa tal", [(neg, 20)]), ("Dubbla olikheter", [(dubbel, 20)]), ("Grafisk lösning", [(graf_, 20)]), ("Heltalslösningar", [(hel, 20)])]
    return U("linjara-olikheter", "AF", "Linjära olikheter: algebraisk och grafisk lösning", "Linjära olikheter",
             "Linjära olikheter och metoder för att lösa dem algebraiskt och grafiskt.",
             "Uppgifter om linjära olikheter för Matematik 1c: lösa olikheter, negativa koefficienter, dubbla olikheter, grafisk lösning och heltalslösningar. 100 uppgifter med facit.",
             "Vänd tecknet vid division med negativt", "f(x) > g(x) där grafen till f ligger över g.", sets,
             ["Lös en olikhet som en ekvation, men vänd tecknet när du multiplicerar eller dividerar med ett negativt tal.",
              "En dubbel olikhet som 1 ≤ 2x + 3 ≤ 11 löser du genom att göra samma sak i alla tre leden.",
              "Grafiskt: f(x) > g(x) där grafen till f ligger ovanför grafen till g."],
             [("−3x + 2 < 14", ["−3x < 12", "Dela med −3 och vänd tecknet"], "x > −4"), ("1 ≤ 2x + 3 ≤ 11", ["−2 ≤ 2x ≤ 8"], "−1 ≤ x ≤ 4")],
             [["Glömmer att vända tecknet", "Delar du med −3 vänds &lt; till &gt;"], ["Läser av y i stället för x", "Svaret gäller x-värden"], ["Gör olika saker i leden", "Samma operation i alla led"]],
             [("Hur skriver jag svaret?", "Som en olikhet för x, till exempel x > −4."), ("Kan en olikhet sakna lösning?", "Ja, till exempel x + 1 < x."), ("Vad betyder ≤?", "Mindre än eller lika med.")])


# ============================================================ exponentialfunktioner
def exponential():
    def ca():
        C = ri(2, 50) * 100
        a = ch([F(102, 100), F(105, 100), F(11, 10), F(12, 10), F(15, 10), F(2), F(9, 10), F(8, 10), F(95, 100), F(97, 100), F(3), F(1, 2)])
        p = (a - 1) * 100
        k = ri(0, 1)
        if k == 0:
            return M("y = %s · %s<sup>x</sup>. Vad betyder talet %s?" % (num(C), d(a), d(a)), ("En ökning med %s %% per tidsenhet" % d(p)) if p > 0 else ("En minskning med %s %% per tidsenhet" % d(-p)),
                     ["En ökning med %s %% per tidsenhet" % d(a * 100) if a > 1 else "En ökning med %s %% per tidsenhet" % d(-p), "Startvärdet är %s" % d(a), "En minskning med %s %% per tidsenhet" % d(a * 100) if a < 1 else "En minskning med %s %% per tidsenhet" % d(p)],
                     "Förändringsfaktorn är %s = %s %%. Det är <b>%s</b>." % (d(a), d(a * 100), ("en ökning med %s %%" % d(p)) if p > 0 else ("en minskning med %s %%" % d(-p))))
        x = ri(1, 4)
        v = C * a ** x
        if v.denominator != 1 and (v * 100).denominator != 1:
            return M("y = %s · %s<sup>x</sup>. Beräkna y då x = %d. Avrunda till heltal." % (num(C), d(a), x), rd(v, 0), [rd(C * a * x, 0), rd(v * a, 0), rd(C + a ** x, 0)], "%s · %s%s ≈ <b>%s</b>." % (num(C), d(a), sup(x), rd(v, 0)))
        return MN("y = %s · %s<sup>x</sup>. Beräkna y då x = %d." % (num(C), d(a), x), v, [C * a * x, v * a, C + a ** x], "%s · %s%s = <b>%s</b>." % (num(C), d(a), sup(x), d(v)))

    def tvapkt():
        C = ri(2, 20) * 10
        a = ch([2, 3, F(1, 2), F(3, 2), 4, F(1, 4)])
        x1 = ri(1, 2)
        y0, y1 = C, C * F(a) ** x1
        if F(y1).denominator != 1:
            return None
        r = "y = %s · %s<sup>x</sup>" % (num(C), d(a) if F(a).denominator in (1, 2, 4) else fq(a))
        return M("En exponentialfunktion går genom (0, %s) och (%d, %s). Vilken är funktionen?" % (num(y0), x1, d(y1)), r, ["y = %s · %s<sup>x</sup>" % (num(C), d(F(a) * 2) if F(a) * 2 != a else d(F(a) + 1)), "y = %s · %s<sup>x</sup>" % (d(y1), d(a)), "y = %s + %s<sup>x</sup>" % (num(C), d(a))],
                 "C = %s (värdet då x = 0). a%s = %s/%s, så a = %s. <b>%s</b>." % (num(C), sup(x1), d(y1), num(C), d(a), r))

    def vaxt():
        nm = ch(["En stad", "En bakteriekultur", "Ett sparkonto", "En kanin­population"])
        C = ri(10, 90) * 100
        p = ch([2, 3, 4, 5, 6, 8, 10, 12, 15])
        n = ri(2, 15)
        v = C * (1 + F(p, 100)) ** n
        return M("%s har värdet %s och ökar med %d %% per år. Vilket värde har den efter %d år? Avrunda till heltal." % (nm, num(C), p, n), rd(v, 0), [rd(C * (1 + F(p * n, 100)), 0), rd(C * (1 + F(p, 100)) ** (n - 1), 0), rd(C * (1 + F(p, 10)) ** n, 0) if p < 10 else rd(v * 2, 0)], "%s · %s%s ≈ <b>%s</b>." % (num(C), d(1 + F(p, 100)), sup(n), rd(v, 0)))

    def halv():
        m = ch([64, 80, 96, 120, 160, 200, 240, 320, 400, 640, 800])
        T = ch([2, 3, 4, 5, 6, 8, 10, 12, 30])
        n = ri(1, 4)
        return MN("En mängd på %d g halveras var %d:e timme. Hur mycket finns kvar efter %d timmar?" % (m, T, n * T), F(m, 2 ** n), [F(m, 2 * n), m - F(m, 2) * n if m - F(m, 2) * n > 0 else F(m, 2 ** (n + 1)), F(m, 2 ** (n - 1)) if n > 1 else F(m, 4)], "%d timmar = %d halveringar: %d · 0,5%s = <b>%s g</b>." % (n * T, n, m, sup(n), d(F(m, 2 ** n))), "g")

    def graf_():
        C = ch([1, 2, 3, 4, 5])
        a = ch([2, 3, F(1, 2), F(1, 3), F(3, 2)])
        f = lambda x: C * float(a) ** x
        pic = graf(f, (-3, 3, 1), (0, 12, 1), [(0, C, "")], "graf till en exponentialfunktion")
        r = "y = %d · %s<sup>x</sup>" % (C, d(a))
        return M("Vilken funktion visas i grafen?" + pic, r, ["y = %d · %s<sup>x</sup>" % (C, d(1 / F(a))), "y = %d · %s<sup>x</sup>" % (C + 1, d(a)), "y = %s · x + %d" % (d(a), C)], "Grafen skär y-axeln i %d och %s med faktorn %s för varje steg: <b>%s</b>." % (C, "växer" if a > 1 else "avtar", d(a), r))

    sets = [("Tolka y = C · aˣ", [(ca, 20)]), ("Bestäm funktionen", [(tvapkt, 20)]), ("Exponentiell tillväxt", [(vaxt, 20)]), ("Halveringstid", [(halv, 20)]), ("Grafer", [(graf_, 10), (ca, 10)])]
    return U("exponentialfunktioner", "AF", "Exponentialfunktioner: y = C · aˣ, tillväxt och halveringstid", "Exponentialfunktioner",
             "Exponentialfunktioner och deras egenskaper. Förändringsfaktor och exponentiell förändring i realistiska situationer.",
             "Uppgifter om exponentialfunktioner för Matematik 1c: tolka y = C · aˣ, bestäm funktionen från punkter, exponentiell tillväxt, halveringstid och grafer. 100 uppgifter med facit.",
             "y = C · aˣ", "C är startvärdet och a förändringsfaktorn.", sets,
             ["En exponentialfunktion har formen y = C · aˣ, där C är startvärdet och a förändringsfaktorn.",
              "a > 1 ger tillväxt och 0 < a < 1 ger avtagande. a = 1,05 betyder en ökning med 5 % per tidsenhet.",
              "Vid halvering är a = 0,5 för varje halveringstid."],
             [("y = 500 · 1,2ˣ, x = 2", ["500 · 1,44"], "720"), ("(0, 3) och (1, 6)", ["C = 3", "a = 6/3 = 2"], "y = 3 · 2ˣ")],
             [["a = 1,05 betyder 105 % ökning", "Det betyder 5 % ökning"], ["Multiplicerar C med a · x", "Det är a upphöjt till x"], ["Tror att grafen kan bli negativ", "C · aˣ är alltid positiv om C > 0"]],
             [("Vad är skillnaden mot linjär funktion?", "Linjärt ökar lika mycket, exponentiellt med lika många procent."), ("Varför skär grafen y-axeln i C?", "a⁰ = 1, så y = C när x = 0."), ("Var används exponentialfunktioner?", "Ränta, befolkning, radioaktivt sönderfall och smittspridning.")])


# ============================================================ potensekvationer
def potensekv():
    def xn():
        n = ch([2, 3, 4, 5])
        b = ri(2, 6) if n > 2 else ri(2, 15)
        v = b ** n
        if v > 10000:
            return None
        r = ("x = ±%d" % b) if n % 2 == 0 else ("x = %d" % b)
        return M("Lös ekvationen x%s = %s." % (sup(n), num(v)), r, ["x = %d" % b if n % 2 == 0 else "x = ±%d" % b, "x = %s" % d(F(v, n)) if F(v, n).denominator == 1 else "x = %d" % (b + 1), "x = %d" % (b * b) if n > 2 else "x = ±%d" % (v // 2)],
                 "x = %s<sup>1/%d</sup> = %d%s." % (num(v), n, b, " Jämn exponent ger två lösningar: <b>%s</b>" % r if n % 2 == 0 else ": <b>%s</b>" % r))

    def koef():
        n = ch([2, 3])
        b = ri(2, 6)
        m = ri(2, 8)
        r = ("x = ±%d" % b) if n == 2 else ("x = %d" % b)
        return M("Lös ekvationen %dx%s = %s." % (m, sup(n), num(m * b ** n)), r, ["x = %d" % (m * b), "x = %s" % ("±%d" % (b * b) if n == 2 else "%d" % (b * b)), "x = %d" % b if n == 2 else "x = ±%d" % b], "Dela med %d: x%s = %s. <b>%s</b>." % (m, sup(n), num(b ** n), r))

    def dec():
        n = ch([3, 4, 5, 6, 8, 10])
        a = F(ch([105, 108, 110, 112, 115, 120, 125, 150, 200]), 100)
        target = ch(["fördubblats", "ökat"])
        x = float(a) ** (1.0 / n)
        return M("Ett värde har %s med faktorn %s på %d år. Lös x%s = %s för att få den årliga förändringsfaktorn. Svara med tre decimaler." % ("vuxit" if target == "ökat" else "ändrats", d(a), n, sup(n), d(a)), rd(F(x).limit_denominator(10 ** 9), 3), [rd(F(float(a) / n).limit_denominator(10 ** 9), 3), rd(F(x + 0.01).limit_denominator(10 ** 9), 3), rd(F(float(a) ** n).limit_denominator(10 ** 9), 3) if float(a) ** n < 100 else rd(F(1 + (float(a) - 1) / n).limit_denominator(10 ** 9), 3)],
                 "x = %s<sup>1/%d</sup> ≈ <b>%s</b>." % (d(a), n, rd(F(x).limit_denominator(10 ** 9), 3)))

    def rotx():
        b = ri(2, 12)
        if coin():
            return M("Lös ekvationen √x = %d." % b, "x = %d" % (b * b), ["x = %d" % (2 * b), "x = %s" % rd(F(b ** 0.5).limit_denominator(10 ** 6), 2), "x = ±%d" % (b * b)], "Kvadrera båda leden: <b>x = %d</b>." % (b * b))
        return M("Lös ekvationen x<sup>1/3</sup> = %d." % b, "x = %s" % num(b ** 3), ["x = %d" % (3 * b), "x = %d" % (b * b), "x = %s" % rd(F(b ** (1 / 3.0)).limit_denominator(10 ** 6), 2)], "Upphöj båda leden till 3: <b>x = %s</b>." % num(b ** 3))

    def potfn():
        k = ri(2, 6)
        a = ch([2, 3, -1])
        x = ri(2, 5)
        if a == -1:
            return MN("y = %d · x<sup>−1</sup>. Beräkna y då x = %d." % (k * 12, x), F(k * 12, x), [k * 12 * x, F(-k * 12, x), F(k * 12, x * x)], "y = %d/%d = <b>%s</b>." % (k * 12, x, d(F(k * 12, x)) if F(k * 12, x).denominator in (1, 2, 4, 5) else fq(F(k * 12, x))))
        return MN("y = %d · x%s. Beräkna y då x = %d." % (k, sup(a), x), k * x ** a, [(k * x) ** a, k * a * x, k + x ** a], "y = %d · %d%s = <b>%s</b>." % (k, x, sup(a), num(k * x ** a)))

    sets = [("Ekvationen xⁿ = a", [(xn, 20)]), ("Med koefficient", [(koef, 20)]), ("Rötter och rationella exponenter", [(rotx, 20)]), ("Förändringsfaktor per år", [(dec, 20)]), ("Potensfunktioner", [(potfn, 20)])]
    return U("potensekvationer", "AF", "Potensekvationer och potensfunktioner", "Potensekvationer",
             "Potensekvationer och potensfunktioner. Lösning av ekvationer av typen xⁿ = a med algebraiska och digitala metoder.",
             "Uppgifter om potensekvationer för Matematik 1c: xⁿ = a, ekvationer med koefficient, rötter som potenser, årlig förändringsfaktor och potensfunktioner. 100 uppgifter med facit.",
             "xⁿ = a ger x = a^(1/n)", "Jämn exponent ger två lösningar, ±.", sets,
             ["En potensekvation har den obekanta i basen: xⁿ = a. Den löses med x = a<sup>1/n</sup>.",
              "Om n är jämnt finns två reella lösningar, x = ±a<sup>1/n</sup>. Om n är udda finns en.",
              "Används ofta för att hitta en årlig förändringsfaktor: om något ökar med faktorn 1,5 på 6 år är den årliga faktorn 1,5<sup>1/6</sup> ≈ 1,070."],
             [("x⁴ = 81", ["x = ±81<sup>1/4</sup>"], "x = ±3"), ("5x³ = 40", ["x³ = 8"], "x = 2")],
             [["x² = 49 ger bara x = 7", "x = ±7"], ["x³ = 27 ger x = 9", "x = 27<sup>1/3</sup> = 3"], ["Blandar ihop potens- och exponentialekvation", "I potensekvationen står x i basen"]],
             [("Vad är skillnaden mot exponentialekvation?", "I aˣ = b står x i exponenten och man behöver logaritmer (Matematik 2c)."), ("Hur räknar jag a<sup>1/n</sup> på räknaren?", "Skriv a^(1/n)."), ("Kan xⁿ = −8 ha lösning?", "Ja om n är udda: x³ = −8 ger x = −2.")])


# ============================================================ förändringsfaktor i flera steg
def forandring():
    ff = take(HC.forandring, 8, "ff")
    anv = take(HC.forandring, 8, "anvand")
    ens = take(HC.forandring, 8, "enheter")
    urs = take(HC.forandring, 8, "ursprung")

    def flera():
        ps = [ch([5, 10, 15, 20, 25, 30, 40, 50]) * ch([1, -1]) for _ in range(ri(2, 3))]
        f = F(1)
        for p in ps:
            f *= 1 + F(p, 100)
        tot = (f - 1) * 100
        desc = lista(("ökar med %d %%" % p) if p > 0 else ("minskar med %d %%" % -p) for p in ps)
        r = ("%s %%" % d(tot)) if (tot * 100).denominator == 1 else rd(tot, 2) + " %"
        return M("Ett pris %s, i den ordningen. Vilken är den totala procentuella förändringen?" % desc, ("+" if tot > 0 else "") + r, ["%+d %%" % sum(ps), ("+" if tot < 0 else "−") + (r.lstrip("−")), "%s %%" % d(f * 100)],
                 "Total förändringsfaktor %s = %s, alltså <b>%s%s</b>." % (" · ".join(d(1 + F(p, 100)) for p in ps), d(f), "+" if tot > 0 else "", r))

    sets = [("Förändringsfaktor", [(ff, 20)]), ("Räkna med förändringsfaktor", [(anv, 20)]), ("Förändringar i flera steg", [(flera, 20)]), ("Ursprungligt värde", [(urs, 20)]), ("Procentenheter", [(ens, 20)])]
    return U("forandringsfaktor", "AF", "Förändringsfaktor: procentuell förändring i flera steg", "Förändringsfaktor",
             "Förändringsfaktor och beräkningar av förändringar i flera steg. Procent och procentenheter i samhälle och privatekonomi.",
             "Uppgifter om förändringsfaktor för Matematik 1c: förändringsfaktor, förändringar i flera steg, ursprungligt värde och procentenheter. 100 uppgifter med facit.",
             "Multiplicera förändringsfaktorerna", "+10 % och −10 % ger 0,99, alltså −1 %.", sets,
             ["Förändringsfaktorn är nytt värde delat med gammalt värde. +12 % ger 1,12 och −12 % ger 0,88.",
              "Vid flera förändringar multiplicerar du faktorerna: +20 % och sedan −20 % ger 1,2 · 0,8 = 0,96.",
              "Det ursprungliga värdet får du genom att dela det nya värdet med förändringsfaktorn."],
             [("+25 % och sedan −20 %", ["1,25 · 0,80 = 1,00"], "Ingen förändring"), ("Efter 20 % rabatt 640 kr", ["640/0,80"], "800 kr")],
             [["+20 % och −20 % tar ut varandra", "1,2 · 0,8 = 0,96"], ["Adderar procentsatserna", "Multiplicera förändringsfaktorerna"], ["Drar av procent från det nya priset", "Dela med förändringsfaktorn"]],
             [("Varför kan man inte addera procent?", "Den andra förändringen räknas på ett nytt värde."), ("Vad är en procentenhet?", "Skillnaden mellan två procentsatser."), ("Hur räknar jag snabbt?", "Skriv förändringsfaktorerna och multiplicera på räknaren.")])


# ============================================================ trigonometri
def trigonometri():
    def tri(a, b, labs):
        pts = [(0, 0), (a * 150.0 / max(a, b), 0), (a * 150.0 / max(a, b), b * 150.0 / max(a, b))]
        P = [(x, 170 - y) for x, y in pts]
        import tr_g
        import re as _re
        s = tr_g.poly(P, labs, ("", "", ""), "", "rätvinklig triangel", rights=[1])
        return fig(_re.sub(r"aria-label='[^']*'", "aria-label='rätvinklig triangel'", s, count=1))

    def sida():
        v = ri(15, 75)
        h = ri(4, 30)
        k = ri(0, 2)
        t = math.radians(v)
        if k == 0:
            x = h * math.sin(t)
            return M("I en rätvinklig triangel är hypotenusan %d cm och en vinkel %d°. Hur lång är kateten mitt emot vinkeln? Avrunda till en decimal." % (h, v), rd(F(x).limit_denominator(10 ** 9), 1) + NB + "cm", [rd(F(h * math.cos(t)).limit_denominator(10 ** 9), 1) + NB + "cm", rd(F(h * math.tan(t)).limit_denominator(10 ** 9), 1) + NB + "cm", rd(F(h / math.sin(t)).limit_denominator(10 ** 9), 1) + NB + "cm"],
                     "Motstående katet = hypotenusa · sin v = %d · sin %d° ≈ <b>%s cm</b>." % (h, v, rd(F(x).limit_denominator(10 ** 9), 1)))
        if k == 1:
            x = h * math.cos(t)
            return M("I en rätvinklig triangel är hypotenusan %d cm och en vinkel %d°. Hur lång är kateten närmast vinkeln? Avrunda till en decimal." % (h, v), rd(F(x).limit_denominator(10 ** 9), 1) + NB + "cm", [rd(F(h * math.sin(t)).limit_denominator(10 ** 9), 1) + NB + "cm", rd(F(h * math.tan(t)).limit_denominator(10 ** 9), 1) + NB + "cm", rd(F(h / math.cos(t)).limit_denominator(10 ** 9), 1) + NB + "cm"],
                     "Närliggande katet = hypotenusa · cos v = %d · cos %d° ≈ <b>%s cm</b>." % (h, v, rd(F(x).limit_denominator(10 ** 9), 1)))
        x = h * math.tan(t)
        return M("I en rätvinklig triangel är den närliggande kateten %d cm och vinkeln %d°. Hur lång är den motstående kateten? Avrunda till en decimal." % (h, v), rd(F(x).limit_denominator(10 ** 9), 1) + NB + "cm", [rd(F(h * math.sin(t)).limit_denominator(10 ** 9), 1) + NB + "cm", rd(F(h / math.tan(t)).limit_denominator(10 ** 9), 1) + NB + "cm", rd(F(h * math.cos(t)).limit_denominator(10 ** 9), 1) + NB + "cm"],
                 "Motstående = närliggande · tan v = %d · tan %d° ≈ <b>%s cm</b>." % (h, v, rd(F(x).limit_denominator(10 ** 9), 1)))

    def vinkel():
        a, b = ri(3, 15), ri(3, 15)
        if a == b:
            return None
        v = math.degrees(math.atan2(b, a))
        pic = tri(a, b, ["%d cm" % a, "%d cm" % b, ""])
        R_ = lambda x: rd(F(x).limit_denominator(10 ** 9), 1) + "°"
        return M("Kateterna är %d cm och %d cm. Hur stor är vinkeln v vid den vänstra spetsen? Avrunda till en decimal." % (a, b) + pic, R_(v), [R_(90 - v), R_(math.degrees(math.atan2(a, b)) + 3), R_(math.degrees(math.asin(min(1, b / float(a + b)))))],
                 "tan v = %d/%d, v = tan⁻¹(%d/%d) ≈ <b>%s</b>." % (b, a, b, a, R_(v)))

    def def_():
        a, b, c = ch([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37), (11, 60, 61), (28, 45, 53), (33, 56, 65), (13, 84, 85), (16, 63, 65)])
        if coin():
            a, b = b, a
        k = ri(0, 2)
        name, val, w = [("sin v", fr(a, c), [fr(b, c), fr(a, b), fr(c, a)]), ("cos v", fr(b, c), [fr(a, c), fr(b, a), fr(c, b)]), ("tan v", fr(a, b), [fr(b, a), fr(a, c), fr(b, c)])][k]
        return M("En rätvinklig triangel har sidorna %d, %d och %d. Vinkeln v ligger mitt emot sidan %d. Vad är %s?" % (a, b, c, a, name), val, w, "sin = motstående/hypotenusa, cos = närliggande/hypotenusa, tan = motstående/närliggande: <b>%s = %s</b>." % (name, val))

    def tillamp():
        k = ri(0, 2)
        if k == 0:
            L, v = ri(4, 12), ri(55, 80)
            h = L * math.sin(math.radians(v))
            return M("En %d m lång stege lutar mot en vägg och bildar vinkeln %d° med marken. Hur högt upp når den? Avrunda till en decimal." % (L, v), rd(F(h).limit_denominator(10 ** 9), 1) + NB + "m", [rd(F(L * math.cos(math.radians(v))).limit_denominator(10 ** 9), 1) + NB + "m", rd(F(L * math.tan(math.radians(v))).limit_denominator(10 ** 9), 1) + NB + "m", rd(F(L).limit_denominator(1), 1) + NB + "m"],
                     "h = %d · sin %d° ≈ <b>%s m</b>." % (L, v, rd(F(h).limit_denominator(10 ** 9), 1)))
        if k == 1:
            dd, v = ri(20, 80), ri(15, 60)
            h = dd * math.tan(math.radians(v))
            return M("Från en punkt %d m från ett torn ser du toppen under vinkeln %d°. Hur högt är tornet? Avrunda till heltal." % (dd, v), rd(F(h).limit_denominator(10 ** 9), 0) + NB + "m", [rd(F(dd * math.sin(math.radians(v))).limit_denominator(10 ** 9), 0) + NB + "m", rd(F(dd / math.tan(math.radians(v))).limit_denominator(10 ** 9), 0) + NB + "m", rd(F(dd * math.cos(math.radians(v))).limit_denominator(10 ** 9), 0) + NB + "m"],
                     "h = %d · tan %d° ≈ <b>%s m</b>." % (dd, v, rd(F(h).limit_denominator(10 ** 9), 0)))
        L, hh = ri(20, 200), ri(2, 15)
        v = math.degrees(math.asin(hh / float(L)))
        return M("En väg är %d m lång och stiger %d m. Vilken vinkel bildar vägen med marken? Avrunda till en decimal." % (L, hh), rd(F(v).limit_denominator(10 ** 9), 1) + "°", [rd(F(math.degrees(math.acos(hh / float(L)))).limit_denominator(10 ** 9), 1) + "°", rd(F(math.degrees(math.atan(hh / float(L))) + 0.6).limit_denominator(10 ** 9), 1) + "°", rd(F(hh * 100.0 / L).limit_denominator(10 ** 9), 1) + "°"],
                 "sin v = %d/%d, v = sin⁻¹(%d/%d) ≈ <b>%s°</b>." % (hh, L, hh, L, rd(F(v).limit_denominator(10 ** 9), 1)))

    sets = [("Sinus, cosinus och tangens", [(def_, 20)]), ("Beräkna sidor", [(sida, 20)]), ("Beräkna vinklar", [(vinkel, 20)]), ("Tillämpningar", [(tillamp, 20)]), ("Blandat", [(sida, 10), (vinkel, 10)])]
    return U("trigonometri", "TV", "Trigonometri: sinus, cosinus och tangens i rätvinkliga trianglar", "Trigonometri",
             "Definitioner av sinus, cosinus och tangens samt arcusfunktioner. Beräkning av sträckor och vinklar i rätvinkliga trianglar.",
             "Uppgifter om trigonometri för Matematik 1c: sinus, cosinus och tangens, beräkna sidor och vinklar i rätvinkliga trianglar och tillämpningar. 100 uppgifter med facit.",
             "sin = mots/hyp, cos = när/hyp", "tan = motstående/närliggande.", sets,
             ["I en rätvinklig triangel med vinkeln v: sin v = motstående katet/hypotenusa, cos v = närliggande katet/hypotenusa och tan v = motstående/närliggande.",
              "Söker du en sida multiplicerar du: motstående = hypotenusa · sin v.",
              "Söker du en vinkel använder du arcusfunktionerna sin⁻¹, cos⁻¹ eller tan⁻¹ på räknaren."],
             [("Hypotenusa 10, vinkel 30°. Motstående katet?", ["10 · sin 30° = 10 · 0,5"], "5"), ("Kateter 3 och 4. Vinkel mot 3?", ["tan v = 3/4", "v = tan⁻¹(0,75)"], "36,9°")],
             [["Räknaren står i radianer", "Kontrollera att räknaren är inställd på grader"], ["Blandar ihop motstående och närliggande", "Motstående ligger mitt emot vinkeln"], ["sin v = 0,5 ger v = 0,5°", "Använd sin⁻¹: v = 30°"]],
             [("Vad är arcus?", "Den omvända funktionen: om sin v = 0,5 är v = arcsin 0,5 = 30°."), ("Gäller detta i alla trianglar?", "Definitionerna gäller rätvinkliga trianglar. Andra trianglar behandlas med sinus- och cosinussatsen i nivå 3c."), ("Hur minns jag?", "SOH CAH TOA eller rita triangeln och markera sidorna.")])


# ============================================================ vektorer
def vektorer():
    def v(a, b):
        return "(%s, %s)" % (sg(a), sg(b))

    def add():
        a, b, c, e = nz(-8, 8), nz(-8, 8), nz(-8, 8), nz(-8, 8)
        if coin():
            return M("u = %s och w = %s. Beräkna u + w." % (v(a, b), v(c, e)), v(a + c, b + e), [v(a - c, b - e), v(a + e, b + c), v(a * c, b * e)], "Addera komponentvis: <b>%s</b>." % v(a + c, b + e))
        return M("u = %s och w = %s. Beräkna u − w." % (v(a, b), v(c, e)), v(a - c, b - e), [v(a + c, b + e), v(c - a, e - b), v(a - e, b - c)], "Subtrahera komponentvis: <b>%s</b>." % v(a - c, b - e))

    def skalar():
        a, b = nz(-6, 6), nz(-6, 6)
        k = nz(-4, 4)
        if k == 1:
            return None
        m = ri(2, 3)
        c, e = nz(-5, 5), nz(-5, 5)
        if coin():
            return M("u = %s. Beräkna %s · u." % (v(a, b), sg(k)), v(k * a, k * b), [v(k * a, b), v(k + a, k + b), v(-k * a, -k * b)], "Multiplicera båda komponenterna med %s: <b>%s</b>." % (sg(k), v(k * a, k * b)))
        return M("u = %s och w = %s. Beräkna %du − w." % (v(a, b), v(c, e), m), v(m * a - c, m * b - e), [v(m * (a - c), m * (b - e)), v(m * a + c, m * b + e), v(a - m * c, b - m * e)], "%du = %s. Sedan minus w: <b>%s</b>." % (m, v(m * a, m * b), v(m * a - c, m * b - e)))

    def langd():
        a, b, c = ch([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (12, 16, 20)])
        sa, sb = ch([1, -1]), ch([1, -1])
        if coin():
            a, b = b, a
        if coin():
            return MN("Beräkna längden |u| av u = %s." % v(sa * a, sb * b), c, [a + b, abs(sa * a + sb * b), c * c], "|u| = √(%s² + %s²) = √%d = <b>%d</b>." % (par(sa * a), par(sb * b), c * c, c))
        x, y = nz(-5, 5), nz(-5, 5)
        return MN("Hur långt är det mellan punkterna A%s och B%s?" % (v(x, y), v(x + sa * a, y + sb * b)), c, [a + b, c + 1, abs(a - b)], "AB = %s. |AB| = √(%d² + %d²) = <b>%d</b>." % (v(sa * a, sb * b), a, b, c))

    def punkter():
        x1, y1, x2, y2 = nz(-6, 6), nz(-6, 6), nz(-6, 6), nz(-6, 6)
        return M("Vilken vektor går från A%s till B%s?" % (v(x1, y1), v(x2, y2)), v(x2 - x1, y2 - y1), [v(x1 - x2, y1 - y2), v(x2 + x1, y2 + y1), v(y2 - y1, x2 - x1)], "AB = B − A = <b>%s</b>." % v(x2 - x1, y2 - y1)) if (x1, y1) != (x2, y2) else None

    def bild():
        a, b = nz(-4, 4), nz(-4, 4)
        x0, y0 = ri(-2, 1), ri(-2, 1)
        if not (-5 <= x0 + a <= 5 and -5 <= y0 + b <= 5):
            return None
        pic = kosy([], [(x0, y0, "A"), (x0 + a, y0 + b, "B")], -5, 5, 22, "två punkter A och B")
        return M("Vilka koordinater har vektorn AB i figuren?" + pic, v(a, b), [v(b, a), v(-a, -b), v(x0 + a, y0 + b)], "Från A till B: %s steg i x-led och %s steg i y-led. <b>%s</b>." % (sg(a), sg(b), v(a, b)))

    sets = [("Addera och subtrahera", [(add, 20)]), ("Multiplikation med tal", [(skalar, 20)]), ("Vektorns längd", [(langd, 20)]), ("Vektor mellan punkter", [(punkter, 20)]), ("Vektorer i koordinatsystem", [(bild, 20)])]
    return U("vektorer", "TV", "Vektorer i koordinatform: addition, längd och skalär", "Vektorer",
             "Vektorer i koordinatform: addition, subtraktion, absolutbelopp och multiplikation med skalär. Sträckor i koordinatsystem.",
             "Uppgifter om vektorer för Matematik 1c: addera och subtrahera vektorer, multiplikation med tal, vektorns längd, vektor mellan punkter och vektorer i koordinatsystem. 100 uppgifter med facit.",
             "|(a, b)| = √(a² + b²)", "Räkna komponent för komponent.", sets,
             ["En vektor har storlek och riktning. I koordinatform skrivs den (a, b): a steg i x-led och b steg i y-led.",
              "Addition och subtraktion görs komponentvis: (1, 2) + (3, −1) = (4, 1). Multiplikation med ett tal multiplicerar båda komponenterna.",
              "Längden (absolutbeloppet) är |(a, b)| = √(a² + b²). Vektorn från A till B är B − A."],
             [("(2, −3) + (−5, 4)", ["2 − 5 = −3", "−3 + 4 = 1"], "(−3, 1)"), ("|(6, −8)|", ["√(36 + 64) = √100"], "10")],
             [["AB = A − B", "AB = B − A"], ["|(3, 4)| = 7", "√(9 + 16) = 5"], ["2 · (1, 3) = (2, 3)", "Båda komponenterna: (2, 6)"]],
             [("Vad är skillnaden mellan punkt och vektor?", "En punkt är ett läge. En vektor är en förflyttning som kan börja var som helst."), ("Vad är en skalär?", "Ett vanligt tal, till exempel 3 eller −2."), ("Var används vektorer?", "I fysik för krafter och hastigheter, och i datorgrafik.")])


# ============================================================ sannolikhet
def sannolikhet():
    tva = take(HE.sannolikhet, 9, "tvasteg")
    mynt = take(HE.sannolikhet, 9, "mynt")
    komp = take(HE.sannolikhet, 9, "komplement")

    def beroende():
        P = [("Du drar två kort ur en kortlek och lägger tillbaka det första.", "Oberoende"), ("Du drar två kort ur en kortlek utan att lägga tillbaka.", "Beroende"),
             ("Du kastar en tärning två gånger.", "Oberoende"), ("Du tar två godisbitar ur en påse och äter den första.", "Beroende"),
             ("Det regnar i Stockholm och det regnar i Uppsala samma dag.", "Beroende"), ("Du singlar en slant och kastar en tärning.", "Oberoende"),
             ("Två personer i samma familj blir förkylda samma vecka.", "Beroende"), ("Två olika lotter i två olika lotterier ger vinst.", "Oberoende")]
        q, r = ch(P)
        return M("%s Är händelserna beroende eller oberoende?" % q, r, ["Oberoende" if r == "Beroende" else "Beroende", "Varken eller", "Det går inte att avgöra"], "<b>%s</b>: %s." % (r, "utfallet i det första påverkar inte det andra" if r == "Oberoende" else "det första påverkar sannolikheten för det andra"))

    def minst():
        p = ch([F(1, 10), F(1, 5), F(1, 4), F(3, 10), F(2, 5), F(1, 20), F(1, 6)])
        n = ri(2, 6)
        v = 1 - (1 - p) ** n
        return M("Sannolikheten att en lampa går sönder ett år är %s. Du har %d lampor som går sönder oberoende av varandra. Vad är sannolikheten att minst en går sönder? Avrunda till tre decimaler." % (d(p), n), rd(v, 3), [rd(p * n, 3), rd((1 - p) ** n, 3), rd(1 - (1 - p) ** (n - 1), 3)], "P(minst en) = 1 − P(ingen) = 1 − %s%s ≈ <b>%s</b>." % (d(1 - p), sup(n), rd(v, 3)))

    def risk():
        p = ch([F(1, 100), F(2, 100), F(5, 100), F(1, 1000), F(3, 1000)])
        n = ch([10, 20, 50, 100])
        v = 1 - (1 - p) ** n
        return M("Risken att ett system fallerar en viss dag är %s %%. Hur stor är risken att det fallerar minst en gång på %d dagar? Avrunda till heltal procent." % (d(p * 100), n), rd(v * 100, 0) + NB + "%", [rd(p * n * 100, 0) + NB + "%" if rd(p * n * 100, 0) != rd(v * 100, 0) else rd(v * 100 + 2, 0) + NB + "%", rd((1 - p) ** n * 100, 0) + NB + "%", rd(p * 100, 0) + NB + "%" if rd(p * 100, 0) != rd(v * 100, 0) else "0 %"],
                 "1 − %s%s ≈ %s, alltså <b>%s %%</b>." % (d(1 - p), sup(n), rd(v, 3), rd(v * 100, 0)))

    sets = [("Flera steg", [(tva, 20)]), ("Beroende och oberoende", [(beroende, 8), (tva, 12)]), ("Komplementhändelse", [(komp, 20)]), ("Minst en", [(minst, 12), (mynt, 8)]), ("Risk och säkerhet", [(risk, 20)])]
    return U("sannolikhet", "SS", "Sannolikhet: flera steg, beroende händelser och risk", "Sannolikhet",
             "Beroende och oberoende händelser, komplementhändelser och sannolikheter i flera steg. Tillämpningar inom spel samt risk- och säkerhetsbedömningar.",
             "Uppgifter om sannolikhet för Matematik 1c: flera steg, beroende och oberoende händelser, komplementhändelse, minst en och risk. 100 uppgifter med facit.",
             "P(minst en) = 1 − P(ingen)", "Oberoende: multiplicera sannolikheterna.", sets,
             ["Vid oberoende händelser multiplicerar du sannolikheterna: P(A och B) = P(A) · P(B).",
              "Vid beroende händelser ändras sannolikheten i andra steget, till exempel när du drar utan återläggning.",
              "Sannolikheten för minst en gång räknas enklast med komplementet: 1 − P(ingen gång)."],
             [("Två sexor i rad", ["1/6 · 1/6"], "1/36"), ("Minst en sexa på tre kast", ["1 − (5/6)³"], "≈ 0,421")],
             [["Adderar sannolikheter i flera steg", "Multiplicera längs grenarna"], ["Risk 1 % per dag ger 30 % på 30 dagar", "1 − 0,99³⁰ ≈ 26 %"], ["Glömmer att en kula är borta", "Utan återläggning ändras nämnaren"]],
             [("Vad betyder oberoende?", "Att det ena inte påverkar det andra."), ("Varför används komplementet?", "Det är ofta mycket enklare att räkna ut att något aldrig händer."), ("Hur används sannolikhet i samhället?", "Vid försäkringar, säkerhetsbedömningar och medicinska tester.")])


# ============================================================ statistik och källkritik
def statistik():
    P = [("En undersökning visar att personer som äter mer glass oftare drunknar. Vad är den bästa förklaringen?", "Båda ökar på sommaren, det är ett samband men inte ett orsakssamband", ["Glass orsakar drunkning", "Undersökningen är fel räknad", "Drunkning gör att man äter glass"]),
         ("Vad är skillnaden mellan korrelation och kausalitet?", "Korrelation är ett samband, kausalitet betyder att det ena orsakar det andra", ["Det är samma sak", "Kausalitet är ett svagt samband", "Korrelation betyder alltid orsak"]),
         ("En tidning frågar sina läsare på nätet om de gillar tidningen. Vad är problemet med urvalet?", "Urvalet är inte slumpmässigt, de som svarar är redan läsare", ["För många svarar", "Frågan är för kort", "Inget problem"]),
         ("Vad betyder att ett resultat är statistiskt signifikant?", "Det är osannolikt att resultatet beror på slumpen", ["Resultatet är viktigt för samhället", "Alla i populationen har svarat", "Resultatet är exakt rätt"]),
         ("En undersökning med 12 personer visar att en ny metod fungerar. Vad bör man vara försiktig med?", "Urvalet är litet och resultatet kan bero på slumpen", ["Att 12 är ett jämnt tal", "Inget, 12 räcker alltid", "Att metoden är ny"]),
         ("Vad är ett stickprov?", "En del av populationen som undersöks", ["Hela populationen", "Ett fel i mätningen", "Ett diagram"]),
         ("Vilket är ett exempel på en systematisk felkälla?", "En våg som alltid visar 1 kg för mycket", ["En slumpmässig avrundning", "Att olika personer svarar olika", "Ett stort urval"]),
         ("Varför väljer man ett slumpmässigt urval?", "För att urvalet ska bli representativt för populationen", ["För att det går snabbare", "För att få fler svar", "För att slippa räkna"]),
         ("En graf över arbetslöshet har en y-axel som börjar på 7 %. Vad bör man tänka på?", "Förändringarna ser större ut än de är", ["Arbetslösheten är 0 %", "Grafen visar inget", "Det finns inga felkällor"]),
         ("Korrelationskoefficienten är 0,05. Vad betyder det?", "Det finns nästan inget linjärt samband", ["Det finns ett starkt samband", "Det ena orsakar det andra", "Alla punkter ligger på en linje"]),
         ("Korrelationskoefficienten är −0,9. Vad betyder det?", "Ett starkt negativt samband", ["Inget samband", "Ett svagt positivt samband", "Ett orsakssamband"]),
         ("Vad är ett bortfall i en enkätundersökning?", "Personer i urvalet som inte svarar", ["Frågor som är för svåra", "Ett fel i diagrammet", "Personer som svarar två gånger"])]

    def begrepp():
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    def urval():
        N = ch([400, 600, 800, 1000, 1200, 1500, 2000])
        n = ch([50, 80, 100, 120, 150, 200])
        x = ri(n // 10, n // 2)
        v = F(x, n) * N
        return M("I ett slumpmässigt urval av %d elever på en skola med %s elever svarade %d att de cyklar till skolan. Ungefär hur många på hela skolan cyklar?" % (n, num(N), x), rd(v, 0), [str(x), rd(v * 2, 0), rd(F(x * 100, n), 0)], "Andelen är %d/%d ≈ %s. %s · %s ≈ <b>%s</b>." % (x, n, rd(F(x, n), 3), rd(F(x, n), 3), num(N), rd(v, 0)))

    def andel():
        a = ri(20, 80)
        b = ri(20, 80)
        n1, n2 = ch([200, 400, 500, 1000]), ch([200, 400, 500, 1000])
        pa, pb = F(a * 100, n1), F(b * 100, n2)
        if pa == pb or (pa * 10).denominator != 1 or (pb * 10).denominator != 1:
            return None
        hi = "Skola A" if pa > pb else "Skola B"
        return M("I skola A har %d av %d elever cykel och i skola B %d av %d. Var är andelen störst?" % (a, n1, b, n2), hi, ["Skola B" if hi == "Skola A" else "Skola A", "Lika stor", "Den skola som har flest elever med cykel"],
                 "A: %s %%, B: %s %%. Jämför andelar, inte antal: <b>%s</b>." % (d(pa), d(pb), hi.lower()))

    sets = [("Korrelation, urval och felkällor", [(begrepp, 12), (urval, 8)]), ("Urval och skattning", [(urval, 20)]), ("Jämför andelar", [(andel, 20)]), ("Granska undersökningar", [(urval, 10), (andel, 10)]), ("Blandat", [(urval, 10), (andel, 10)])]
    return U("statistik-och-kallkritik", "SS", "Statistik: urval, korrelation och kritisk granskning", "Statistik och källkritik",
             "Statistiska begrepp i samhälle och vetenskap, till exempel signifikans, korrelation, kausalitet, urval och felkällor. Kritisk granskning av fakta och statistik.",
             "Uppgifter om statistik och källkritik för Matematik 1c: korrelation och kausalitet, urval och skattning, jämföra andelar och felkällor. 100 uppgifter med facit.",
             "Korrelation är inte kausalitet", "Ett samband betyder inte att det ena orsakar det andra.", sets,
             ["Korrelation betyder att två variabler samvarierar. Kausalitet betyder att den ena orsakar den andra.",
              "Ett stickprov ska vara slumpmässigt och tillräckligt stort för att representera populationen.",
              "Granska alltid statistik: Vem har gjort undersökningen? Hur stort är urvalet? Finns det bortfall eller systematiska fel?"],
             [("30 av 120 i urvalet, skolan har 800 elever", ["30/120 = 0,25", "0,25 · 800"], "≈ 200"), ("Glass och drunkning", ["Båda beror på sommarvärmen"], "Inget orsakssamband")],
             [["Ett samband bevisar orsak", "Det kan finnas en tredje faktor"], ["Jämför antal i stället för andel", "Räkna andelen i procent"], ["Tror att stort urval alltid är bra", "Det måste också vara slumpmässigt"]],
             [("Vad är en population?", "Hela gruppen som undersökningen gäller."), ("Vad är en tredje variabel?", "En faktor som påverkar båda storheterna och skapar ett skensamband."), ("Hur stort ska ett urval vara?", "Det beror på hur noggrant svar man behöver. Större urval ger mindre slumpfel.")])


# ============================================================ ränta och amortering
def privatekonomi():
    import se_h_c as HC_
    enkel = take(HC_.ranta, 9, "enkel")
    rpr = take(HC_.ranta, 9, "rpr")
    lan = take(HC_.ranta, 9, "lan")
    jf = take(HC_.ranta, 9, "jamfor")

    def amort():
        L = ri(5, 40) * 10000
        n = ch([5, 10, 20, 25])
        r = ch([3, 4, 5, 6])
        a = F(L, n)
        y = ri(2, n - 1)
        rest = L - a * (y - 1)
        ranta = rest * F(r, 100)
        if a.denominator != 1 or ranta.denominator != 1:
            return None
        return MN("Ett lån på %s amorteras med lika stora belopp varje år i %d år. Räntan är %d %%. Hur mycket ränta betalas år %d?" % (kr(L), n, r, y), ranta, [L * F(r, 100), rest * F(r, 100) + a * F(r, 100), a * F(r, 100)], "Skulden vid början av år %d: %s − %d · %s = %s. Ränta: %s · %s = <b>%s kr</b>." % (y, num(L), y - 1, num(a), num(rest), num(rest), d(F(r, 100)), num(ranta)), "kr")

    def kalkyl():
        P = [("I ett kalkylprogram står ett belopp i A1 och räntesatsen 4 % ska läggas till. Vilken formel ger nytt belopp?", "=A1*1,04", ["=A1+4", "=A1*4", "=A1*0,04"]),
             ("Ett sparande växer med 3 % per år. A2 innehåller förra årets värde. Vilken formel ska stå i A3?", "=A2*1,03", ["=A2+3", "=A2*0,03", "=A2*3"]),
             ("En skuld i B2 minskar med en amortering på 2 000 kr. Vilken formel ger ny skuld i B3?", "=B2-2000", ["=B2*2000", "=B2+2000", "=2000-B2"]),
             ("Räntan är 5 % av skulden i C2. Vilken formel ger räntan?", "=C2*0,05", ["=C2*5", "=C2+0,05", "=C2*1,05"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    def kredit():
        p = ri(5, 30) * 1000
        r = ch([15, 18, 20, 24])
        m = ri(3, 12)
        v = p * F(r, 100) * F(m, 12)
        return MN("Du handlar för %s på kredit med %d %% årsränta och betalar efter %d månader. Hur mycket ränta blir det?" % (kr(p), r, m), v, [p * F(r, 100), p * F(r, 100) * m, v / 2], "%s · %s · %d/12 = <b>%s kr</b>." % (num(p), d(F(r, 100)), m, d(v)), "kr") if v.denominator == 1 else None

    sets = [("Ränta på sparande", [(enkel, 10), (rpr, 10)]), ("Lån och amortering", [(amort, 20)]), ("Lån och kredit", [(lan, 10), (kredit, 10)]), ("Kalkylprogram", [(kalkyl, 4), (rpr, 8), (jf, 8)]), ("Blandat", [(amort, 10), (enkel, 10)])]
    return U("ranta-och-amortering", "PT", "Privatekonomi: ränta, ränta på ränta och amortering", "Ränta och amortering",
             "Kalkylprogram för beräkningar av ränta och amortering. Privatekonomi och matematiska modeller i realistiska situationer.",
             "Uppgifter om ränta och amortering för Matematik 1c: ränta på sparande, ränta på ränta, lån, rak amortering, kredit och formler i kalkylprogram. 100 uppgifter med facit.",
             "Ränta på skulden som är kvar", "Rak amortering: lika stor amortering varje år.", sets,
             ["Ränta på ränta: belopp · (1 + r)ⁿ. Ett kalkylprogram räknar år för år med en formel som =A2*1,04.",
              "Vid rak amortering betalar du lika stor del av lånet varje år. Räntan räknas på den skuld som är kvar och minskar därför år för år.",
              "Kredit och avbetalning kan ha hög ränta. Jämför alltid den effektiva räntan."],
             [("Lån 100 000 kr, 10 år, 5 %. Ränta år 3", ["Skuld: 100 000 − 2 · 10 000 = 80 000", "80 000 · 0,05"], "4 000 kr"), ("5 000 kr, 3 %, 4 år", ["5 000 · 1,03⁴"], "≈ 5 628 kr")],
             [["Räknar ränta på hela lånet varje år", "Räntan räknas på kvarvarande skuld"], ["=A1*4 för 4 % ränta", "Förändringsfaktorn 1,04: =A1*1,04"], ["Amortering = ränta", "Amortering minskar skulden, ränta är en kostnad"]],
             [("Vad är rak amortering?", "Lika stor amortering varje period, så att skulden minskar jämnt."), ("Vad är ett annuitetslån?", "Ett lån där summan av ränta och amortering är lika stor varje period."), ("Varför använda kalkylprogram?", "Det räknar många perioder snabbt och visar hur skulden förändras.")])


UNITS = {"potenser-och-rotter": potenser, "algebra-och-faktorisering": algebra, "ekvationer-och-formler": ekvationer, "funktioner": funktioner,
         "linjara-funktioner": linjara, "linjara-olikheter": olikheter, "exponentialfunktioner": exponential, "potensekvationer": potensekv,
         "forandringsfaktor": forandring, "trigonometri": trigonometri, "vektorer": vektorer, "sannolikhet": sannolikhet,
         "statistik-och-kallkritik": statistik, "ranta-och-amortering": privatekonomi}
