# -*- coding: utf-8 -*-
"""Sverige gymnasiet: Matematik nivå 2c（Gy25）"""
import math
from fractions import Fraction as F
from se_g import (take, nz, xp, pol, U, graf, gen, MQ, lista, ri, ch, sh, cap, fr, fq, d, par, sg, M, MN, rd, sup, tab, K, num, kr, NB, MIN, coin, expr, lin,
                  kosy, kurve, figure, fig, wrap, text, line, INK, GREEN, FILL, RED, BLUE)
import se_h_b as HB
import se_h_d as HD


def fl(x, k=2):
    return rd(F(x).limit_denominator(10 ** 9), k)


def sol(a, b):
    a, b = sorted([a, b])
    return "x₁ = %s, x₂ = %s" % (sg(a), sg(b)) if a != b else "x = %s" % sg(a)


# ============================================================ ekvationssystem
def system():
    m = {n: take(HB.ekvsystem, 9, n) for n in ("subst", "addm", "kontroll", "grafisk", "text_")}
    sets = [("Substitutionsmetoden", [(m["subst"], 20)]), ("Additionsmetoden", [(m["addm"], 20)]), ("Grafisk lösning", [(m["grafisk"], 20)]),
            ("Kontrollera lösningar", [(m["kontroll"], 20)]), ("Modellera med ekvationssystem", [(m["text_"], 20)])]
    return U("ekvationssystem", "AF", "Linjära ekvationssystem: algebraiska och grafiska metoder", "Ekvationssystem",
             "Linjära ekvationssystem med två obekanta och metoder för att lösa dem algebraiskt och grafiskt.",
             "Uppgifter om linjära ekvationssystem för Matematik 2c: substitutionsmetoden, additionsmetoden, grafisk lösning, kontroll och modellering. 100 uppgifter med facit.",
             "Lösningen = linjernas skärningspunkt", "Eliminera en variabel i taget.", sets,
             ["Ett linjärt ekvationssystem består av två ekvationer som ska gälla samtidigt.",
              "Substitutionsmetoden: lös ut en variabel och sätt in. Additionsmetoden: addera ekvationerna så att en variabel försvinner.",
              "Grafiskt är lösningen skärningspunkten. Parallella linjer ger ingen lösning och sammanfallande linjer oändligt många."],
             [("x + y = 7 och 2x − y = 5", ["Addera: 3x = 12", "x = 4, y = 3"], "x = 4, y = 3")],
             [["Glömmer att räkna ut den andra variabeln", "Sätt in x för att få y"], ["Multiplicerar bara ena ledet", "Multiplicera hela ekvationen"], ["Svarar med bara en punkt för parallella linjer", "Parallella linjer har ingen skärningspunkt"]],
             [("Hur många lösningar kan ett system ha?", "En, ingen eller oändligt många."), ("Vilken metod är bäst?", "Substitution när en variabel redan är ensam, annars addition."), ("Var används ekvationssystem?", "När två villkor ska gälla samtidigt, till exempel pris och antal.")])


def kvadrering():
    m = {n: take(HB.kvadrering, 9, n) for n in ("plus", "konj", "fakt", "smart", "ekv")}
    sets = [("Kvadreringsreglerna", [(m["plus"], 20)]), ("Konjugatregeln", [(m["konj"], 20)]), ("Faktorisera", [(m["fakt"], 20)]), ("Räkna smart", [(m["smart"], 20)]), ("Ekvationer", [(m["ekv"], 20)])]
    return U("kvadreringsreglerna-och-konjugatregeln", "AF", "Kvadreringsreglerna och konjugatregeln", "Kvadrerings- och konjugatregeln",
             "Konjugatregeln och kvadreringsreglerna för att förenkla uttryck, faktorisera och lösa ekvationer.",
             "Uppgifter om kvadreringsreglerna och konjugatregeln för Matematik 2c: utveckla, faktorisera, räkna smart och lösa ekvationer. 100 uppgifter med facit.",
             "(a + b)² = a² + 2ab + b²", "(a + b)(a − b) = a² − b²", sets,
             ["(a + b)² = a² + 2ab + b² och (a − b)² = a² − 2ab + b².", "Konjugatregeln: (a + b)(a − b) = a² − b².", "Reglerna används baklänges för att faktorisera: x² − 10x + 25 = (x − 5)²."],
             [("(2x − 3)²", ["4x² − 2 · 2x · 3 + 9"], "4x² − 12x + 9")],
             [["(a + b)² = a² + b²", "Glöm inte 2ab"], ["(x − 4)² = x² − 16", "x² − 8x + 16"], ["x² + 9 = (x + 3)(x − 3)", "Det gäller x² − 9"]],
             [("Varför heter det konjugat?", "a + b och a − b kallas konjugat till varandra."), ("Hur ser jag om något är en kvadrat?", "Första och sista termen ska vara kvadrater och mittermen dubbla produkten."), ("Var används reglerna?", "Vid förenkling, ekvationslösning och kvadratkomplettering.")])


# ============================================================ andragradsekvationer
def andragrad():
    def pq():
        a, b = nz(-9, 9), nz(-9, 9)
        if a == b:
            return None
        p, q = -(a + b), a * b
        return M("Lös ekvationen %s = 0 med pq-formeln." % pol({2: 1, 1: p, 0: q}), sol(a, b), [sol(-a, -b), sol(a, -b) if a != -b else "x = %s" % sg(a), "x = %s" % sg(-F(p, 2))], "x = %s ± √(%s² − %s) = %s ± %s. <b>%s</b>." % (sg(-F(p, 2)), par(F(p, 2)), par(q), sg(-F(p, 2)), d(abs(F(a - b, 2))), sol(a, b)))

    def irr():
        p, q = nz(-8, 8), nz(-15, 10)
        D = F(p * p, 4) - q
        if D <= 0 or int(D) == D and int(math.isqrt(int(D))) ** 2 == D:
            return None
        x1, x2 = -p / 2.0 - math.sqrt(D), -p / 2.0 + math.sqrt(D)
        r = "x₁ ≈ %s, x₂ ≈ %s" % (fl(x1), fl(x2))
        return M("Lös ekvationen %s = 0. Avrunda till två decimaler." % pol({2: 1, 1: p, 0: q}), r, ["x₁ ≈ %s, x₂ ≈ %s" % (fl(-x2), fl(-x1)), "x ≈ %s" % fl(x2), "x₁ ≈ %s, x₂ ≈ %s" % (fl(-p / 2.0 - D), fl(-p / 2.0 + D))], "x = %s ± √%s: <b>%s</b>." % (sg(-F(p, 2)), d(D) if (D * 100).denominator == 1 else fq(D), r))

    def nollp():
        a, b = nz(-9, 9), nz(-9, 9)
        k = ri(0, 1)
        if k == 0:
            return M("Lös ekvationen %s = 0." % pol({2: 1, 1: -a}), sol(0, a), ["x = %s" % sg(a), sol(0, -a), "x = ±%d" % abs(a)], "Bryt ut x: x(x %s %d) = 0. <b>%s</b>." % ("−" if a > 0 else "+", abs(a), sol(0, a)))
        m = ri(2, 4)
        if a == b:
            return None
        return M("Lös ekvationen %d(x %s %d)(x %s %d) = 0." % (m, "−" if a > 0 else "+", abs(a), "−" if b > 0 else "+", abs(b)), sol(a, b), [sol(-a, -b), sol(m * a, m * b), "x = %s" % sg(a * b)], "En produkt är noll om någon faktor är noll: <b>%s</b>." % sol(a, b))

    def anorm():
        m = ri(2, 5)
        a, b = nz(-6, 6), nz(-6, 6)
        if a == b:
            return None
        return M("Lös ekvationen %s = 0." % pol({2: m, 1: -m * (a + b), 0: m * a * b}), sol(a, b), [sol(-a, -b), sol(m * a, m * b) if m * a != m * b else "x = 0", "x = %s" % sg(F(a + b, 2))], "Dela med %d: %s = 0. pq-formeln ger <b>%s</b>." % (m, pol({2: 1, 1: -(a + b), 0: a * b}), sol(a, b)))

    def antal():
        p, q = nz(-8, 8), ri(-15, 20)
        D = F(p * p, 4) - q
        r = "två lösningar" if D > 0 else "en lösning" if D == 0 else "inga reella lösningar"
        return M("Hur många reella lösningar har %s = 0?" % pol({2: 1, 1: p, 0: q}), r, [x for x in ("två lösningar", "en lösning", "inga reella lösningar", "oändligt många lösningar") if x != r], "Under rottecknet: (p/2)² − q = %s. %s ger <b>%s</b>." % (d(D) if (D * 100).denominator == 1 else fq(D), "Positivt" if D > 0 else "Noll" if D == 0 else "Negativt", r))

    def text_():
        a = ri(3, 12)
        b = a + ri(2, 8)
        k = ri(0, 1)
        if k == 0:
            return M("En rektangel är %d cm längre än den är bred och har arean %d cm². Hur bred är den?" % (b - a, a * b), "%d cm" % a, ["%d cm" % b, "%d cm" % (a * b // (b - a)) if a * b // (b - a) not in (a, b) else "%d cm" % (a + 1), "%d cm" % (a - 1)], "x(x + %d) = %d ger %s = 0 och x = %d (den positiva lösningen): <b>%d cm</b>." % (b - a, a * b, pol({2: 1, 1: b - a, 0: -a * b}), a, a))
        n = ri(4, 15)
        return M("Produkten av två heltal som följer på varandra är %d. Vilka kan talen vara (positiva)?" % (n * (n + 1)), "%d och %d" % (n, n + 1), ["%d och %d" % (n - 1, n), "%d och %d" % (n + 1, n + 2), "%d och %d" % (2 * n, n // 2 + 1)], "x(x + 1) = %d ger %s = 0 och x = %d: <b>%d och %d</b>." % (n * (n + 1), pol({2: 1, 1: 1, 0: -n * (n + 1)}), n, n, n + 1))

    sets = [("pq-formeln", [(pq, 20)]), ("Ungefärliga lösningar", [(irr, 20)]), ("Nollproduktmetoden", [(nollp, 20)]), ("Antal lösningar", [(antal, 10), (anorm, 10)]), ("Problemlösning", [(text_, 20)])]
    return U("andragradsekvationer", "AF", "Andragradsekvationer: pq-formeln och nollproduktmetoden", "Andragradsekvationer",
             "Andragradsekvationer och metoder för att lösa dem, bland annat pq-formeln, faktorisering och nollproduktmetoden.",
             "Uppgifter om andragradsekvationer för Matematik 2c: pq-formeln, ungefärliga lösningar, nollproduktmetoden, antal lösningar och problemlösning. 100 uppgifter med facit.",
             "x = −p/2 ± √((p/2)² − q)", "Formen x² + px + q = 0 krävs.", sets,
             ["Skriv ekvationen på formen x² + px + q = 0. Dela med koefficienten framför x² om den inte är 1.",
              "pq-formeln: x = −p/2 ± √((p/2)² − q). Uttrycket under rottecknet avgör antalet lösningar.",
              "Saknas konstanttermen kan du bryta ut x och använda nollproduktmetoden: x(x − 5) = 0 ger x = 0 eller x = 5."],
             [("x² − 6x + 8 = 0", ["x = 3 ± √(9 − 8)"], "x₁ = 2, x₂ = 4"), ("2x² + 4x − 6 = 0", ["Dela med 2: x² + 2x − 3 = 0", "x = −1 ± 2"], "x₁ = −3, x₂ = 1")],
             [["Använder pq utan att dela med a", "Dela först så att x² står ensamt"], ["Fel tecken på −p/2", "p = −6 ger −p/2 = 3"], ["Delar med x och tappar x = 0", "Bryt ut x i stället"]],
             [("Vad betyder ett negativt tal under rottecknet?", "Att ekvationen saknar reella lösningar."), ("Varför heter den pq-formeln?", "För att ekvationen skrivs x² + px + q = 0."), ("Kan man alltid faktorisera?", "Nej, men pq-formeln fungerar alltid.")])


# ============================================================ andragradsfunktioner
def andragradsfn():
    def sym():
        a, b = nz(-6, 6), nz(-6, 6)
        if a == b:
            return None
        s = F(a + b, 2)
        f = pol({2: 1, 1: -(a + b), 0: a * b})
        k = ri(0, 2)
        if k == 0:
            return M("Bestäm symmetrilinjen till y = %s." % f, "x = %s" % sg(s), ["x = %s" % sg(-s), "x = %s" % sg(a * b), "x = %s" % sg(a + b)], "Symmetrilinjen ligger mitt mellan nollställena %s och %s: <b>x = %s</b>." % (sg(a), sg(b), sg(s)))
        if k == 1:
            y = (s - a) * (s - b)
            return M("Bestäm extrempunkten till y = %s." % f, "(%s, %s)" % (sg(s), sg(y)), ["(%s, %s)" % (sg(-s), sg(y)), "(%s, %s)" % (sg(s), sg(-y)), "(0, %s)" % sg(a * b)], "x = %s. y(%s) = %s. Minimipunkt <b>(%s, %s)</b>." % (sg(s), sg(s), sg(y), sg(s), sg(y)))
        return M("Bestäm nollställena till f(x) = %s." % f, sol(a, b), [sol(-a, -b), "x = %s" % sg(s), sol(a, -b) if a != -b else "x = 0"], "f(x) = 0 ger <b>%s</b>." % sol(a, b))

    def maxmin():
        a = ch([1, -1, 2, -2])
        h, k = nz(-4, 4), nz(-6, 6)
        f = pol({2: a, 1: -2 * a * h, 0: a * h * h + k})
        typ = "minimipunkt" if a > 0 else "maximipunkt"
        return M("Har y = %s en maximi- eller minimipunkt, och var ligger den?" % f, "%s i (%s, %s)" % (cap(typ), sg(h), sg(k)), ["%s i (%s, %s)" % ("Maximipunkt" if a > 0 else "Minimipunkt", sg(h), sg(k)), "%s i (%s, %s)" % (cap(typ), sg(-h), sg(k)), "%s i (%s, %s)" % (cap(typ), sg(h), sg(a * h * h + k))],
                 "Koefficienten för x² är %s, alltså %s. x = %s ger y = %s: <b>%s i (%s, %s)</b>." % (sg(a), "en minimipunkt" if a > 0 else "en maximipunkt", sg(h), sg(k), typ, sg(h), sg(k)))

    def graflas():
        a = ch([1, -1])
        h, k = nz(-3, 3), nz(-4, 4)
        f = lambda x: a * (x - h) ** 2 + k
        pic = graf(f, (-5, 5, 1), (-7, 7, 1), [(h, k, "")], "parabel")
        q = ri(0, 1)
        if q == 0:
            return M("Grafen visar en andragradsfunktion. Vilken är symmetrilinjen?" + pic, "x = %s" % sg(h), ["x = %s" % sg(k), "x = %s" % sg(-h), "y = %s" % sg(k)], "Symmetrilinjen går lodrätt genom vändpunkten: <b>x = %s</b>." % sg(h))
        r = "y = %s" % pol({2: a, 1: -2 * a * h, 0: a * h * h + k})
        return M("Vilken funktion visas i grafen?" + pic, r, ["y = %s" % pol({2: -a, 1: 2 * a * h, 0: -a * h * h + k}), "y = %s" % pol({2: a, 1: 2 * a * h, 0: a * h * h + k}), "y = %s" % pol({2: a, 1: -2 * a * h, 0: a * h * h - k})],
                 "Vändpunkt (%s, %s) och %s: y = %s(x %s %d)² %s %d = <b>%s</b>." % (sg(h), sg(k), "öppnar uppåt" if a > 0 else "öppnar nedåt", "" if a > 0 else "−", "−" if h > 0 else "+", abs(h), "+" if k > 0 else "−", abs(k), r[4:]))

    def ysk():
        a, b, c = nz(-3, 3), nz(-6, 6), nz(-9, 9)
        return M("Var skär grafen till y = %s y-axeln?" % pol({2: a, 1: b, 0: c}), "(0, %s)" % sg(c), ["(%s, 0)" % sg(c), "(0, %s)" % sg(a), "(0, %s)" % sg(b)], "Sätt x = 0: y = %s. <b>(0, %s)</b>." % (sg(c), sg(c)))

    def till():
        v = ri(10, 30)
        g = 5
        t = F(v, 2 * g)
        hmax = F(v * v, 4 * g)
        k = ri(0, 1)
        if k == 0:
            return MN("En boll kastas uppåt. Höjden är h(t) = %dt − 5t² meter efter t sekunder. Hur högt når bollen?" % v, hmax, [F(v * v, 2 * g), v, hmax / 2], "Maximum vid t = %s: h = %d · %s − 5 · %s² = <b>%s m</b>." % (d(t) if (t * 100).denominator == 1 else fq(t), v, d(t) if (t * 100).denominator == 1 else fq(t), par(t) if (t * 100).denominator == 1 else fq(t), d(hmax) if (hmax * 100).denominator == 1 else rd(hmax, 2)), "m") if (hmax * 100).denominator == 1 else None
        L = ri(20, 80) * 2
        x = F(L, 4)
        A = x * x
        return MN("Ett staket på %d m ska omge en rektangulär hage. Vilken är den största arean hagen kan få?" % L, A, [F(L * L, 8), F(L * L, 4), A / 2], "A(x) = x(%s − x) är störst när x = %s: <b>%s m²</b>." % (d(F(L, 2)), d(x), d(A)), "m²")

    sets = [("Symmetrilinje, extrempunkt och nollställen", [(sym, 20)]), ("Maximi- eller minimipunkt", [(maxmin, 20)]), ("Läs av grafen", [(graflas, 20)]), ("Skärning med y-axeln", [(ysk, 8), (sym, 12)]), ("Tillämpningar", [(till, 20)])]
    return U("andragradsfunktioner", "AF", "Andragradsfunktioner: symmetrilinje, extrempunkt och nollställen", "Andragradsfunktioner",
             "Egenskaper hos andragradsfunktioner: symmetrilinje, extrempunkt och nollställen, samt tillämpningar.",
             "Uppgifter om andragradsfunktioner för Matematik 2c: symmetrilinje, extrempunkt, nollställen, läsa av grafer och tillämpningar. 100 uppgifter med facit.",
             "Symmetrilinjen mitt mellan nollställena", "Positiv x²-koefficient ger minimipunkt.", sets,
             ["Grafen till y = ax² + bx + c är en parabel. Om a > 0 har den en minimipunkt, om a < 0 en maximipunkt.",
              "Symmetrilinjen ligger mitt mellan nollställena. Extrempunkten ligger på symmetrilinjen.",
              "Grafen skär y-axeln i (0, c)."],
             [("y = x² − 6x + 5", ["Nollställen 1 och 5", "Symmetrilinje x = 3", "y(3) = −4"], "Minimipunkt (3, −4)")],
             [["Symmetrilinjen är y = …", "Den är lodrät: x = …"], ["Positiv a ger maximum", "Positiv a ger minimum"], ["Glömmer att räkna ut y i extrempunkten", "Sätt in x i funktionen"]],
             [("Hur hittar jag extrempunkten utan nollställen?", "Symmetrilinjen är x = −b/(2a)."), ("Vad är en parabel?", "Grafen till en andragradsfunktion."), ("Var används andragradsfunktioner?", "Kastbanor, area och vinstberäkningar.")])


# ============================================================ logaritmer
def logaritmer():
    def lgv():
        e = ri(-4, 6)
        v = F(10) ** e
        if coin():
            a, b = ri(-3, 5), ri(1, 5)
            va, vb = F(10) ** a, F(10) ** b
            if coin():
                return M("Beräkna lg %s + lg %s." % (d(va), d(vb)), sg(a + b), [sg(a * b) if a * b != a + b else sg(a + b + 1), d(va + vb) if va + vb != a + b else sg(a - b), sg(a - b) if a - b != a + b else sg(a + b - 1)], "lg %s = %s och lg %s = %s: <b>%s</b>." % (d(va), sg(a), d(vb), sg(b), sg(a + b)))
            return M("Beräkna lg %s − lg %s." % (d(va), d(vb)), sg(a - b), [sg(a + b) if a + b != a - b else sg(a - b + 1), sg(b - a) if b != a else sg(a - b - 1), d(va - vb) if va - vb not in (a - b, a + b, b - a) else sg(a - b + 2)], "lg %s = %s och lg %s = %s: <b>%s</b>." % (d(va), sg(a), d(vb), sg(b), sg(a - b)))
        return M("Beräkna lg %s." % d(v), sg(e), [d(v / 10) if v >= 1 else sg(-e), sg(e + 1), sg(-e) if e else "1"], "lg %s är exponenten: 10%s = %s. <b>%s</b>." % (d(v), sup(e), d(v), sg(e)))

    def bas():
        b = ch([2, 3, 4, 5])
        e = ri(-2, 5)
        v = F(b) ** e
        return M("Beräkna log<sub>%d</sub> %s." % (b, fq(v) if v.denominator != 1 else num(v)), sg(e), [sg(e + 1), sg(-e) if e else "1", d(F(v, b)) if v.denominator == 1 and v % b == 0 and F(v, b) != e else sg(e - 1)], "%d%s = %s, alltså <b>%s</b>." % (b, sup(e), fq(v) if v.denominator != 1 else num(v), sg(e)))

    def lagar():
        k = ri(0, 3)
        a, b = ri(2, 9), ri(2, 9)
        if k == 0:
            return M("Skriv som en logaritm: lg %d + lg %d." % (a, b), "lg %d" % (a * b), ["lg %d" % (a + b), "lg %d · lg %d" % (a, b), "lg %d" % (a * b * 10)], "lg a + lg b = lg(ab): <b>lg %d</b>." % (a * b))
        if k == 1:
            return M("Skriv som en logaritm: lg %d − lg %d." % (a * b, b), "lg %d" % a, ["lg %d" % (a * b - b), "lg %d / lg %d" % (a * b, b), "lg %d" % (a * b * b)], "lg a − lg b = lg(a/b): <b>lg %d</b>." % a)
        if k == 2:
            n = ri(2, 5)
            return M("Skriv %d · lg %d som en logaritm." % (n, a), "lg %s" % num(a ** n), ["lg %d" % (a * n), "lg %d" % (a + n), "%d lg %d" % (a, n)], "n · lg a = lg aⁿ: <b>lg %s</b>." % num(a ** n))
        x = ri(1, 4)
        return MN("Förenkla lg %s + lg %d." % (num(10 ** x * a), 1), x + 0 if False else None, [], "") if False else M("Förenkla lg 100 + lg %s." % num(10 ** x), sg(x + 2), [sg(2 * x), num(100 + 10 ** x), sg(x * 2 + 2)], "lg 100 = 2 och lg %s = %d: <b>%d</b>." % (num(10 ** x), x, x + 2))

    def rak():
        v = ri(2, 999)
        if v in (10, 100):
            return None
        return M("Beräkna lg %d med räknaren. Avrunda till tre decimaler." % v, fl(math.log10(v), 3), [fl(math.log(v), 3), fl(math.log10(v) + 1, 3), fl(v / 10.0, 3) if v < 1000 else fl(math.log10(v) - 1, 3)], "lg %d ≈ <b>%s</b>. Kontroll: 10 upphöjt till svaret ger %d." % (v, fl(math.log10(v), 3), v))

    def def_():
        e = ri(-3, 6)
        b = ch([2, 10, 3, 5])
        y = b ** e if e >= 0 else F(1, b ** -e)
        if coin():
            return M("Skriv %d%s = %s med logaritmer." % (b, sup(e), fq(y) if F(y).denominator != 1 else num(y)), ("lg %s = %s" if b == 10 else "log<sub>%d</sub> %%s = %%s" % b) % (fq(y) if F(y).denominator != 1 else num(y), sg(e)),
                     [("lg %s = %s" if b == 10 else "log<sub>%d</sub> %%s = %%s" % b) % (sg(e), fq(y) if F(y).denominator != 1 else num(y)), "log<sub>%s</sub> %d = %s" % (fq(y) if F(y).denominator != 1 else num(y), b, sg(e)), ("lg %s = %s" if b == 10 else "log<sub>%d</sub> %%s = %%s" % b) % (fq(y) if F(y).denominator != 1 else num(y), sg(e + 1))],
                     "log<sub>b</sub> y = x betyder bˣ = y.")
        return M("Vad betyder lg x = %s?" % sg(e), "x = 10%s" % sup(e), ["x = %s · 10" % sg(e), "x = %s%s" % (sg(e), sup(10)), "x = lg 10%s" % sup(e)], "Logaritmen är exponenten: lg x = %s betyder <b>x = 10%s</b>." % (sg(e), sup(e)))

    sets = [("Tiologaritmer", [(lgv, 20)]), ("Logaritmer med andra baser", [(bas, 20)]), ("Logaritmlagarna", [(lagar, 20)]), ("Definitionen", [(def_, 20)]), ("Logaritmer med räknare", [(rak, 20)])]
    return U("logaritmer", "AF", "Logaritmer: definition, tiologaritmer och logaritmlagar", "Logaritmer",
             "Logaritmer och logaritmlagar. Logaritmens definition och sambandet med potenser.",
             "Uppgifter om logaritmer för Matematik 2c: tiologaritmer, logaritmer med andra baser, logaritmlagarna, definitionen och beräkningar med räknare. 100 uppgifter med facit.",
             "lg x = a betyder 10ᵃ = x", "Logaritmen är en exponent.", sets,
             ["Tiologaritmen lg x är den exponent som 10 ska upphöjas till för att bli x: lg 1 000 = 3.",
              "Logaritmlagarna: lg a + lg b = lg(ab), lg a − lg b = lg(a/b) och lg aⁿ = n · lg a.",
              "Med andra baser: log₂ 8 = 3 eftersom 2³ = 8."],
             [("lg 0,01", ["0,01 = 10⁻²"], "−2"), ("lg 4 + lg 25", ["lg(4 · 25) = lg 100"], "2")],
             [["lg 1 000 = 1 000", "lg 1 000 = 3"], ["lg(a + b) = lg a + lg b", "Det gäller lg(ab)"], ["lg 0 = 0", "lg 0 är inte definierat. lg 1 = 0"]],
             [("Varför behövs logaritmer?", "För att lösa ekvationer där den obekanta står i exponenten."), ("Vad är ln?", "Den naturliga logaritmen med basen e, som du möter i nivå 3c."), ("Kan logaritmen vara negativ?", "Ja, för tal mellan 0 och 1.")])


# ============================================================ exponentialekvationer
def expekv():
    def tio():
        v = F(ri(2, 999), ch([1, 10, 100]))
        x = math.log10(float(v))
        return M("Lös ekvationen 10<sup>x</sup> = %s. Avrunda till tre decimaler." % d(v), "x ≈ %s" % fl(x, 3), ["x ≈ %s" % fl(float(v) / 10, 3), "x ≈ %s" % fl(math.log(float(v)), 3), "x ≈ %s" % fl(x + 1, 3)], "x = lg %s ≈ <b>%s</b>." % (d(v), fl(x, 3)))

    def ax():
        a = ch([2, 3, 5, 1.5, 1.05, 1.1, 0.8, 0.5])
        b = ch([10, 20, 50, 100, 3, 7])
        if a < 1:
            b = ch([0.1, 0.2, 0.3, 0.5])
        x = math.log10(b) / math.log10(a)
        A = d(F(a).limit_denominator(100))
        B = d(F(b).limit_denominator(100))
        return M("Lös ekvationen %s<sup>x</sup> = %s. Avrunda till två decimaler." % (A, B), "x ≈ %s" % fl(x), ["x ≈ %s" % fl(b / a), "x ≈ %s" % fl(math.log10(b) - math.log10(a)), "x ≈ %s" % fl(b ** (1.0 / a)) if a > 1 else "x ≈ %s" % fl(-x)],
                 "Logaritmera: x · lg %s = lg %s, alltså x = lg %s / lg %s ≈ <b>%s</b>." % (A, B, B, A, fl(x)))

    def fordubbling():
        p = ch([2, 3, 4, 5, 6, 7, 8, 10, 12])
        x = math.log10(2) / math.log10(1 + p / 100.0)
        return M("Ett belopp växer med %d %% per år. Efter hur många år har det fördubblats? Avrunda till en decimal." % p, "%s år" % fl(x, 1), ["%s år" % fl(100.0 / p / 2, 1), "%s år" % fl(x * 2, 1), "%s år" % fl(100.0 / p, 1)], "1,%02d<sup>x</sup> = 2 ger x = lg 2 / lg %s ≈ <b>%s år</b>." % (p, d(1 + F(p, 100)), fl(x, 1)) if p < 10 else "%s<sup>x</sup> = 2 ger x = lg 2 / lg %s ≈ <b>%s år</b>." % (d(1 + F(p, 100)), d(1 + F(p, 100)), fl(x, 1)))

    def till():
        C = ri(2, 20) * 1000
        p = ch([5, 10, 15, 20, 25])
        T = ri(C // 4, C // 2)
        x = math.log10(float(T) / C) / math.log10(1 - p / 100.0)
        return M("En bil värd %s minskar i värde med %d %% per år. Efter hur många år är den värd %s? Avrunda till en decimal." % (kr(C * 10), p, kr(T * 10)), "%s år" % fl(x, 1), ["%s år" % fl(x * 1.5, 1), "%s år" % fl((C - T) * 100.0 / (p * C), 1), "%s år" % fl(-x, 1)], "%s · %s<sup>x</sup> = %s ger x = lg(%s) / lg %s ≈ <b>%s år</b>." % (num(C * 10), d(1 - F(p, 100)), num(T * 10), fl(float(T) / C, 3), d(1 - F(p, 100)), fl(x, 1)))

    def skillnad():
        P = [("x³ = 20", "Potensekvation", "x = 20<sup>1/3</sup>"), ("3<sup>x</sup> = 20", "Exponentialekvation", "x = lg 20 / lg 3"), ("x⁵ = 100", "Potensekvation", "x = 100<sup>1/5</sup>"),
             ("5<sup>x</sup> = 100", "Exponentialekvation", "x = lg 100 / lg 5"), ("1,2<sup>x</sup> = 3", "Exponentialekvation", "x = lg 3 / lg 1,2"), ("x<sup>1,2</sup> = 3", "Potensekvation", "x = 3<sup>1/1,2</sup>")]
        q, typ, r = ch(P)
        return M("Hur löser du ekvationen %s?" % q, r, [x[2] for x in P if x[2] != r and x[0] != q][:3], "%s: <b>%s</b>." % (typ, r))

    sets = [("10ˣ = a", [(tio, 20)]), ("aˣ = b", [(ax, 20)]), ("Fördubblingstid", [(fordubbling, 9), (ax, 11)]), ("Värdeminskning", [(till, 20)]), ("Potens- eller exponentialekvation?", [(skillnad, 6), (tio, 7), (till, 7)])]
    return U("exponentialekvationer", "AF", "Exponentialekvationer: lös med logaritmer", "Exponentialekvationer",
             "Exponentialekvationer och metoder för att lösa dem med logaritmer. Likheter och skillnader mellan exponential- och potensekvationer.",
             "Uppgifter om exponentialekvationer för Matematik 2c: 10ˣ = a, aˣ = b, fördubblingstid, värdeminskning och skillnaden mot potensekvationer. 100 uppgifter med facit.",
             "aˣ = b ger x = lg b / lg a", "Logaritmera båda leden.", sets,
             ["I en exponentialekvation står den obekanta i exponenten: aˣ = b.",
              "Logaritmera båda leden: x · lg a = lg b, alltså x = lg b / lg a.",
              "I en potensekvation står den obekanta i basen: xⁿ = b. Den löses med x = b<sup>1/n</sup>."],
             [("2ˣ = 50", ["x = lg 50 / lg 2"], "≈ 5,64"), ("1,05ˣ = 2", ["x = lg 2 / lg 1,05"], "≈ 14,2")],
             [["x = lg(b/a)", "x = lg b / lg a"], ["Använder potensmetoden på aˣ = b", "x står i exponenten: logaritmera"], ["Avrundar för tidigt", "Avrunda först i slutet"]],
             [("Kan jag använda ln i stället för lg?", "Ja, x = ln b / ln a ger samma svar."), ("Vad är fördubblingstid?", "Tiden det tar för ett värde att bli dubbelt så stort vid konstant procentuell ökning."), ("Hur kontrollerar jag?", "Sätt in svaret: aˣ ska bli b.")])


# ============================================================ rotekvationer
def rotekv():
    def enkel():
        b = ri(1, 12)
        a = nz(-20, 20)
        x = b * b - a
        return M("Lös ekvationen √(x %s %d) = %d." % ("+" if a > 0 else "−", abs(a), b), "x = %s" % sg(x), ["x = %s" % sg(b - a), "x = %s" % sg(b * b + a), "x = %s" % sg(x + 1)], "Kvadrera: x %s %d = %d, <b>x = %s</b>." % ("+" if a > 0 else "−", abs(a), b * b, sg(x)))

    def koef():
        m = ri(2, 5)
        b = ri(2, 10)
        a = nz(-10, 10)
        if (b * b - a) % m:
            return None
        x = (b * b - a) // m
        return M("Lös ekvationen √(%s) = %d." % (expr([(m, "x"), (a, "")]), b), "x = %s" % sg(x), ["x = %s" % sg(F(b - a, m)) if F(b - a, m) != x else "x = %s" % sg(x + 2), "x = %s" % sg(b * b - a), "x = %s" % sg(x + 1)], "Kvadrera: %s = %d ger <b>x = %s</b>." % (expr([(m, "x"), (a, "")]), b * b, sg(x)))

    def falsk():
        r = ri(1, 9)
        s = nz(-9, 9)
        if s == r or s < 0 and False:
            return None
        # x = √(x + c) med lösningarna till x² − x − c = 0
        a1, a2 = r, -ri(1, 9)
        c = -a1 * a2
        if a1 + a2 != 1:
            return None
        return M("Lös ekvationen x = √(x + %d)." % c, "x = %d" % a1, [sol(a1, a2), "x = %d" % a2, "x = %d" % c], "Kvadrera: x² = x + %d ger x = %d eller x = %d. Prövning: x = %d ger %d = √%d stämmer inte. <b>x = %d</b>." % (c, a1, a2, a2, a2, a2 + c, a1))

    def falsk2():
        b = ri(1, 8)
        r = ri(b + 2, b + 10)
        t = 2 * b + 1 - r
        a = b * b - r * t
        if a < 1 or a > 60:
            return None
        r1, r2 = F(t), F(r)
        return M("Lös ekvationen √(x + %d) = x − %d." % (a, b), "x = %d" % r, [sol(t, r), "x = %s" % sg(t), "x = %d" % (r + 1)],
                 "Kvadrera: x + %d = (x − %d)² ger %s = 0 med rötterna %s och %d. Prövning: x = %s ger ett negativt högerled. <b>x = %d</b>." % (a, b, pol({2: 1, 1: -(2 * b + 1), 0: b * b - a}), sg(t), r, sg(t), r))

    def ingen():
        a = ri(1, 9)
        b = nz(-9, -1)
        return M("Hur många lösningar har √(x + %d) = %s?" % (a, sg(b)), "Ingen lösning", ["En lösning, x = %d" % (b * b - a), "Två lösningar", "Oändligt många"], "En kvadratrot är aldrig negativ, så det finns <b>ingen lösning</b>.")

    sets = [("Kvadrera båda leden", [(enkel, 20)]), ("Med koefficient", [(koef, 20)]), ("Prövning och falska rötter", [(falsk2, 20)]), ("Blandade rotekvationer", [(enkel, 7), (koef, 7), (falsk, 3), (ingen, 3)]), ("Prövning", [(falsk2, 14), (falsk, 3), (ingen, 3)])]
    return U("rotekvationer", "AF", "Rotekvationer: kvadrera och pröva lösningen", "Rotekvationer",
             "Rotekvationer och metoder för att lösa dem, inklusive kontroll av falska rötter.",
             "Uppgifter om rotekvationer för Matematik 2c: kvadrera båda leden, ekvationer med koefficient, prövning och falska rötter. 100 uppgifter med facit.",
             "Kvadrera och pröva alltid", "Kvadrering kan ge falska rötter.", sets,
             ["Isolera rottecknet och kvadrera båda leden: √(x + 3) = 5 ger x + 3 = 25 och x = 22.",
              "När du kvadrerar kan du få falska rötter. Pröva därför alltid lösningarna i den ursprungliga ekvationen.",
              "En kvadratrot är aldrig negativ. √(x + 1) = −2 saknar lösning."],
             [("√(2x + 1) = 3", ["2x + 1 = 9"], "x = 4"), ("√(x + 2) = x", ["x + 2 = x²", "x = 2 eller x = −1", "x = −1 stämmer inte"], "x = 2")],
             [["Kvadrerar bara ena termen", "Kvadrera hela ledet"], ["Prövar inte lösningen", "Sätt in och kontrollera"], ["√(x + 1) = −2 ger x = 3", "En rot kan inte vara negativ"]],
             [("Varför uppstår falska rötter?", "Både 3 och −3 har kvadraten 9. Kvadreringen tappar information om tecknet."), ("Vad är prövning?", "Att sätta in svaret i den ursprungliga ekvationen."), ("Var finns rotekvationer?", "I fysikformler, till exempel för pendlar och fritt fall.")])


# ============================================================ standardavvikelse och percentiler
def spridning():
    def data(n, lo, hi):
        return [ri(lo, hi) for _ in range(n)]

    def sd():
        xs = data(ri(4, 6), 2, 20)
        m = F(sum(xs), len(xs))
        if (m * 10).denominator != 1:
            return None
        v = sum((x - m) ** 2 for x in xs) / len(xs)
        s = math.sqrt(float(v))
        return M("Beräkna standardavvikelsen (population) för %s. Avrunda till en decimal." % lista(str(x) for x in xs), fl(s, 1), [fl(float(v), 1), fl(s * math.sqrt(len(xs) / (len(xs) - 1.0)), 1) if fl(s * math.sqrt(len(xs) / (len(xs) - 1.0)), 1) != fl(s, 1) else fl(s + 0.5, 1), fl(max(xs) - min(xs), 1)],
                 "Medelvärdet är %s. Medelvärdet av kvadrerade avvikelser är %s. Roten ur ger <b>%s</b>." % (d(m), fl(float(v), 2), fl(s, 1)))

    def jamfor():
        a = [ri(18, 22) for _ in range(5)]
        b = [ri(10, 30) for _ in range(5)]
        sa = math.sqrt(sum((x - sum(a) / 5.0) ** 2 for x in a) / 5)
        sb = math.sqrt(sum((x - sum(b) / 5.0) ** 2 for x in b) / 5)
        if abs(sa - sb) < 1:
            return None
        nm1, nm2 = K().two()
        r = nm1 if sa < sb else nm2
        return M("%s: %s. %s: %s. Vems resultat har minst standardavvikelse?" % (nm1, lista(map(str, a)), nm2, lista(map(str, b))), r, [nm2 if r == nm1 else nm1, "Lika", "Den som har högst medelvärde"], "Standardavvikelsen är ungefär %s respektive %s. Minst spridning: <b>%s</b>." % (fl(sa, 1), fl(sb, 1), r))

    def percentil():
        n = ch([20, 40, 50, 80, 100, 200, 300, 500])
        p = ch([10, 25, 50, 75, 90])
        r = n * p // 100
        if coin():
            return M("I en grupp på %d personer ligger en person på %d:e percentilen. Ungefär hur många har ett högre värde?" % (n, p), str(n - r), [str(r), str(100 - p) if 100 - p != n - r else str(n - r + 5), str(n - r + n // 10)], "%d %% har lägre värde, alltså %d %% högre: %d %% av %d = <b>%d</b>." % (p, 100 - p, 100 - p, n, n - r))
        return M("I en grupp på %d personer ligger en person på %d:e percentilen. Ungefär hur många har ett lägre värde?" % (n, p), str(r), [str(n - r), str(p), str(r + n // 10)], "%d %% av %d = <b>%d</b>." % (p, n, r))

    def tolka():
        P = [("Vad visar standardavvikelsen?", "Hur mycket värdena i genomsnitt avviker från medelvärdet", ["Det vanligaste värdet", "Skillnaden mellan största och minsta", "Medelvärdet"]),
             ("Två klasser har samma medelvärde men olika standardavvikelse. Vad betyder det?", "Resultaten är olika utspridda", ["Klasserna är lika bra", "Klassen med större standardavvikelse har högre resultat", "Det går inte att jämföra"]),
             ("Vad är medianen uttryckt som percentil?", "50:e percentilen", ["25:e percentilen", "75:e percentilen", "100:e percentilen"]),
             ("Vad är skillnaden mellan populations- och stickprovsstandardavvikelse?", "Stickprovets delar med n − 1 i stället för n", ["Ingen skillnad", "Populationens delar med n − 1", "Stickprovets använder medianen"]),
             ("Om alla värden ökar med 5, vad händer med standardavvikelsen?", "Den är oförändrad", ["Den ökar med 5", "Den fördubblas", "Den blir 0"]),
             ("Om alla värden fördubblas, vad händer med standardavvikelsen?", "Den fördubblas", ["Den är oförändrad", "Den ökar med 2", "Den halveras"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    def bredd():
        xs = sorted(data(ri(7, 11), 1, 50))
        n = len(xs)
        lo, hi = xs[:n // 2], xs[(n + 1) // 2:]

        def med(v):
            k = len(v)
            return F(v[k // 2]) if k % 2 else F(v[k // 2 - 1] + v[k // 2], 2)
        q1, q3 = med(lo), med(hi)
        return MN("Bestäm kvartilavståndet för %s." % lista(map(str, xs)), q3 - q1, [xs[-1] - xs[0], q3, med(xs)], "Nedre kvartilen %s, övre kvartilen %s: %s − %s = <b>%s</b>." % (d(q1), d(q3), d(q3), d(q1), d(q3 - q1)))

    sets = [("Standardavvikelse", [(sd, 20)]), ("Jämför spridning", [(jamfor, 20)]), ("Percentiler", [(percentil, 20)]), ("Kvartilavstånd", [(bredd, 20)]), ("Tolka spridningsmått", [(tolka, 6), (sd, 7), (bredd, 7)])]
    return U("standardavvikelse-och-percentiler", "SS", "Lägesmått och spridningsmått: standardavvikelse och percentiler", "Standardavvikelse och percentiler",
             "Lägesmått och spridningsmått, till exempel percentiler och standardavvikelse, och beräkningar med digitala verktyg.",
             "Uppgifter om standardavvikelse och percentiler för Matematik 2c: beräkna standardavvikelse, jämför spridning, percentiler, kvartilavstånd och tolkning. 100 uppgifter med facit.",
             "σ = roten ur medelkvadratavvikelsen", "Liten standardavvikelse = små avvikelser.", sets,
             ["Standardavvikelsen σ mäter hur mycket värdena avviker från medelvärdet: σ = √(Σ(x − x̄)²/n).",
              "För ett stickprov delar man med n − 1 i stället för n. Räknaren eller kalkylprogrammet gör beräkningen.",
              "En percentil anger hur stor andel av värdena som ligger under: 90:e percentilen har 90 % under sig."],
             [("Standardavvikelse för 2, 4, 6", ["x̄ = 4", "(4 + 0 + 4)/3 = 8/3", "√(8/3)"], "≈ 1,6")],
             [["Glömmer att dra roten ur", "Variansen är σ², ta roten ur"], ["Tror att percentil = procent rätt", "Percentil anger andel med lägre värde"], ["Delar med n − 1 för en population", "Population: n, stickprov: n − 1"]],
             [("Vad är varians?", "Kvadraten på standardavvikelsen."), ("När används standardavvikelse?", "När man vill beskriva spridning kring medelvärdet, till exempel i mätningar."), ("Vad är en kvartil?", "25:e och 75:e percentilen.")])


# ============================================================ normalfördelning
def normal():
    R = [(1, 68), (2, 95), (3, 99.7)]

    def inom():
        mu = ri(10, 200)
        s = ri(2, 20)
        k, p = ch(R)
        pp = d(F(p).limit_denominator(10)) if p != int(p) else str(p)
        return M("En normalfördelning har medelvärdet %d och standardavvikelsen %d. Hur stor andel ligger mellan %d och %d?" % (mu, s, mu - k * s, mu + k * s), "ungefär %s %%" % pp, ["ungefär %s %%" % x for x in ("68", "95", "99,7", "50") if x != pp][:3], "Intervallet är medelvärdet ± %d standardavvikelse%s: <b>ungefär %s %%</b>." % (k, "" if k == 1 else "r", pp))

    def over():
        mu = ri(50, 180)
        s = ri(3, 15)
        k = ch([1, 2])
        p = {1: "16", 2: "2,5"}[k]
        if coin():
            return M("Längden är normalfördelad med medelvärdet %d cm och standardavvikelsen %d cm. Hur stor andel är längre än %d cm?" % (mu, s, mu + k * s), "ungefär %s %%" % p, ["ungefär %s %%" % x for x in ("16", "2,5", "34", "47,5", "50") if x != p][:3], "Utanför ±%dσ ligger %s %%, hälften på varje sida: <b>ungefär %s %%</b>." % (k, "32" if k == 1 else "5", p))
        return M("Vikten är normalfördelad med medelvärdet %d g och standardavvikelsen %d g. Hur stor andel väger mindre än %d g?" % (mu, s, mu - k * s), "ungefär %s %%" % p, ["ungefär %s %%" % x for x in ("16", "2,5", "34", "68", "50") if x != p][:3], "Under μ − %dσ ligger <b>ungefär %s %%</b>." % (k, p))

    def mellan():
        mu = ri(20, 100)
        s = ri(2, 10)
        opts = [((mu, mu + s), "34"), ((mu - s, mu), "34"), ((mu, mu + 2 * s), "47,5"), ((mu + s, mu + 2 * s), "13,5"), ((mu - 2 * s, mu + s), "81,5"), ((mu, 10 ** 6), "50")]
        (a, b), p = ch(opts)
        if b == 10 ** 6:
            return M("Ett normalfördelat material har medelvärdet %d. Hur stor andel är större än %d?" % (mu, mu), "50 %", ["34 %", "68 %", "95 %"], "Normalfördelningen är symmetrisk kring medelvärdet: <b>50 %</b>.")
        return M("Ett normalfördelat material har μ = %d och σ = %d. Hur stor andel ligger mellan %d och %d?" % (mu, s, a, b), "ungefär %s %%" % p, ["ungefär %s %%" % x for x in ("34", "47,5", "13,5", "81,5", "68") if x != p][:3], "Använd 68–95–99,7-regeln och symmetrin: <b>ungefär %s %%</b>." % p)

    def antal():
        n = ch([200, 400, 500, 1000, 2000])
        mu, s = ri(20, 80), ri(2, 8)
        k, p = ch([(1, F(68, 100)), (2, F(95, 100))])
        v = n * p
        return MN("%s personer mättes. Värdena är normalfördelade med μ = %d och σ = %d. Ungefär hur många har ett värde mellan %d och %d?" % (num(n), mu, s, mu - k * s, mu + k * s), v, [n * (1 - p), v / 2, n * F(50, 100)], "%s %% av %s ≈ <b>%s</b>." % (d(p * 100), num(n), d(v)), "personer") if v.denominator == 1 else None

    def kurva():
        P = [("Hur ser en normalfördelningskurva ut?", "Symmetrisk och klockformad", ["Rak och stigande", "Störst i kanterna", "Skev åt höger"]),
             ("Var ligger medelvärdet i en normalfördelning?", "I mitten, där kurvan är högst", ["Längst till vänster", "Där kurvan är lägst", "Det går inte att säga"]),
             ("Vad händer med kurvan om standardavvikelsen ökar?", "Den blir bredare och lägre", ["Den blir smalare och högre", "Den flyttas åt höger", "Inget"]),
             ("Vad händer med kurvan om medelvärdet ökar?", "Den flyttas åt höger", ["Den blir bredare", "Den blir lägre", "Den flyttas åt vänster"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    sets = [("68–95–99,7-regeln", [(inom, 20)]), ("Större eller mindre än", [(over, 20)]), ("Mellan två värden", [(mellan, 20)]), ("Antal i ett material", [(antal, 20)]), ("Normalfördelningskurvan", [(kurva, 4), (inom, 8), (mellan, 8)])]
    return U("normalfordelning", "SS", "Normalfördelning: 68–95–99,7-regeln", "Normalfördelning",
             "Normalfördelning och enklare beräkningar på normalfördelat material.",
             "Uppgifter om normalfördelning för Matematik 2c: 68–95–99,7-regeln, större eller mindre än, mellan två värden, antal och kurvans form. 100 uppgifter med facit.",
             "68 % inom ±σ, 95 % inom ±2σ", "Kurvan är symmetrisk kring medelvärdet.", sets,
             ["Många mätvärden, som längd och vikt, är ungefär normalfördelade. Kurvan är klockformad och symmetrisk kring medelvärdet μ.",
              "Ungefär 68 % av värdena ligger inom μ ± σ, 95 % inom μ ± 2σ och 99,7 % inom μ ± 3σ.",
              "Använd symmetrin: mellan μ och μ + σ ligger 34 %, och över μ + σ ligger 16 %."],
             [("μ = 170, σ = 6. Andel över 176?", ["176 = μ + σ", "(100 − 68)/2"], "16 %"), ("Mellan μ − 2σ och μ + σ", ["47,5 % + 34 %"], "81,5 %")],
             [["Över μ + σ är 32 %", "32 % är utanför på båda sidor, 16 % på en sida"], ["Glömmer symmetrin", "Halva andelen på varje sida"], ["Använder regeln på skeva fördelningar", "Den gäller normalfördelat material"]],
             [("Varför är normalfördelningen vanlig?", "Många små slumpmässiga effekter tillsammans ger ofta en normalfördelning."), ("Vad är σ?", "Standardavvikelsen."), ("Hur räknar jag mer exakt?", "Med en tabell eller digitala verktyg som räknar ut arean under kurvan.")])


# ============================================================ regression och korrelation
def regression():
    def r_():
        r = F(ri(-98, 98), 100)
        if 25 <= abs(r) * 100 <= 35 or 65 <= abs(r) * 100 <= 75:
            return None
        if r >= F(7, 10):
            ans = "Starkt positivt samband"
        elif r >= F(3, 10):
            ans = "Måttligt positivt samband"
        elif r > F(-3, 10):
            ans = "Inget eller mycket svagt samband"
        elif r > F(-7, 10):
            ans = "Måttligt negativt samband"
        else:
            ans = "Starkt negativt samband"
        allo = ["Starkt positivt samband", "Måttligt positivt samband", "Inget eller mycket svagt samband", "Måttligt negativt samband", "Starkt negativt samband"]
        return M("Korrelationskoefficienten är r = %s. Vad beskriver det?" % sg(d(r)) if False else "Korrelationskoefficienten är r = %s. Vad beskriver det?" % (d(r) if r >= 0 else MIN + d(-r)), ans, sh([a for a in allo if a != ans])[:3], "r nära ±1 betyder starkt samband, nära 0 inget linjärt samband: <b>%s</b>." % ans.lower())

    def predik():
        k = F(ri(5, 40), 10)
        m = ri(-20, 50)
        x = ri(5, 40)
        y = k * x + m
        nm = ch([("antal timmar träning per vecka", "x", "resultat"), ("temperatur i °C", "x", "glassförsäljning i kg"), ("ålder i år", "x", "längd i cm")])
        return MN("En regressionslinje är y = %s, där x är %s och y är %s. Vad förutsäger modellen när x = %d?" % ("%sx %s %d" % (d(k), "+" if m >= 0 else "−", abs(m)), nm[0], nm[2], x), y, [k * x, y + k, k + x + m], "y = %s · %d %s %d = <b>%s</b>." % (d(k), x, "+" if m >= 0 else "−", abs(m), d(y)))

    def tolka_k():
        k = F(ri(5, 50), 10)
        m = ri(10, 100)
        return M("Regressionslinjen y = %s beskriver vikt y (kg) för en hund som funktion av ålder x (månader). Vad betyder %s?" % ("%sx + %d" % (d(k), m), d(k)), "Vikten ökar i genomsnitt med %s kg per månad" % d(k), ["Hunden väger %s kg vid födseln" % d(k), "Vikten ökar med %d kg per månad" % m, "Hunden är %s månader gammal" % d(k)], "Lutningen k = %s anger ökningen per månad: <b>%s kg per månad</b>." % (d(k), d(k)))

    def extrapol():
        P = [("En regressionslinje bygger på barn mellan 2 och 10 år. Varför är det osäkert att använda den för 30-åringar?", "Modellen gäller bara inom det undersökta intervallet", ["Linjen är fel räknad", "30 är ett jämnt tal", "Vuxna har ingen längd"]),
             ("Vad betyder r² = 0,81?", "81 % av variationen i y förklaras av modellen", ["Lutningen är 0,81", "81 % av punkterna ligger på linjen", "Sambandet är negativt"]),
             ("Varför betyder ett starkt samband inte att x orsakar y?", "Det kan finnas en tredje faktor som påverkar båda", ["Korrelationen är alltid fel", "Det betyder alltid orsak", "Linjen är för brant"]),
             ("Vad gör en regressionslinje?", "Den beskriver sambandet med den linje som passar punkterna bäst", ["Den går genom alla punkter", "Den visar medelvärdet", "Den ritas för hand"]),
             ("Ett punktdiagram visar punkter som bildar en bågform. Vad gäller?", "En linjär modell passar dåligt", ["r är nära 1", "Sambandet är linjärt", "Det finns inget samband alls"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    def punkter():
        k = ch([1, -1, 2, -2])
        m = ri(-2, 3)
        xs = list(range(-3, 4))
        pts = [(x, k * x + m + ch([-1, 0, 0, 1]), "") for x in xs]
        if any(abs(y) > 5 for _, y, _ in pts):
            return None
        pic = kosy([], pts, -5, 5, 20, "punktdiagram")
        r = "positiv korrelation" if k > 0 else "negativ korrelation"
        return M("Vilken sorts korrelation visar punktdiagrammet?" + pic, r, ["negativ korrelation" if k > 0 else "positiv korrelation", "ingen korrelation", "korrelation r = 0"], "Punkterna %s från vänster till höger: <b>%s</b>." % ("stiger" if k > 0 else "sjunker", r))

    sets = [("Korrelationskoefficient", [(r_, 20)]), ("Förutsäg med regressionslinje", [(predik, 20)]), ("Tolka lutningen", [(tolka_k, 20)]), ("Punktdiagram", [(punkter, 20)]), ("Modellens begränsningar", [(extrapol, 5), (predik, 8), (r_, 7)])]
    return U("regression-och-korrelation", "SS", "Regression och korrelation: regressionslinje och r-värde", "Regression och korrelation",
             "Regressionsanalys och korrelationskoefficient med digitala metoder. Korrelation och kausalitet samt modellers begränsningar.",
             "Uppgifter om regression och korrelation för Matematik 2c: korrelationskoefficient, förutsägelser med regressionslinje, tolka lutningen, punktdiagram och modellens begränsningar. 100 uppgifter med facit.",
             "r nära ±1 = starkt linjärt samband", "Korrelation är inte orsak.", sets,
             ["Korrelationskoefficienten r ligger mellan −1 och 1. Nära 1 är ett starkt positivt samband, nära −1 ett starkt negativt och nära 0 inget linjärt samband.",
              "En regressionslinje y = kx + m beräknas med digitala verktyg. k anger hur mycket y i genomsnitt ändras när x ökar med 1.",
              "Använd modellen försiktigt utanför de x-värden den bygger på."],
             [("y = 2,5x + 10, x = 8", ["2,5 · 8 + 10"], "30")],
             [["r = 0,9 betyder 90 % av punkterna på linjen", "Det betyder ett starkt linjärt samband"], ["Extrapolerar långt utanför data", "Modellen gäller inom det undersökta området"], ["Tror att samband betyder orsak", "Det kan finnas en tredje faktor"]],
             [("Hur beräknar jag r?", "Med räknare eller kalkylprogram, till exempel funktionen KORREL."), ("Vad är regressionsanalys?", "Att anpassa en matematisk modell till data."), ("Måste modellen vara linjär?", "Nej, det finns även exponentiella och andra modeller.")])


# ============================================================ logik och bevis
def logik():
    def pil():
        P = [("x = 3", "x² = 9", "⇒"), ("x² = 9", "x = 3", "⇐"), ("x + 2 = 5", "x = 3", "⇔"), ("ABCD är en kvadrat", "ABCD är en rektangel", "⇒"), ("ett tal är delbart med 10", "talet är delbart med 5", "⇒"),
             ("en triangel har tre lika sidor", "triangeln har tre lika vinklar", "⇔"), ("x > 5", "x > 3", "⇒"), ("x > 3", "x > 5", "⇐"), ("2x = 8", "x = 4", "⇔"), ("ett tal är jämnt", "talet är delbart med 4", "⇐"),
             ("det regnar", "marken är blöt", "⇒"), ("x = −2", "x² = 4", "⇒"), ("n är ett primtal större än 2", "n är udda", "⇒"), ("a = b", "a + 1 = b + 1", "⇔")]
        a, b, k = ri(2, 9), ri(1, 9), ri(1, 4)
        P += [("x = %d" % a, "x² = %d" % (a * a), "⇒"), ("x² = %d" % (a * a), "x = −%d" % a, "⇐"), ("x + %d = %d" % (b, a + b), "x = %d" % a, "⇔"), ("x > %d" % a, "x > %d" % (a - k), "⇒"),
              ("x &lt; %d" % a, "x &lt; %d" % (a - k), "⇐"), ("%dx = %d" % (a, a * b), "x = %d" % b, "⇔"), ("n är delbart med %d" % (2 * a), "n är delbart med %d" % a, "⇒"), ("n är delbart med %d" % a, "n är delbart med %d" % (a * b + a), "⇐")]
        p, q, r = ch(P)
        return M("Vilket tecken ska stå mellan påståendena: <i>%s</i> □ <i>%s</i>?" % (p, q), r, [x for x in ("⇒", "⇐", "⇔", "=") if x != r], "%s. Svar: <b>%s</b>." % ({"⇒": "Det första medför det andra, men inte omvänt", "⇐": "Det andra medför det första, men inte omvänt", "⇔": "Påståendena är ekvivalenta"}[r], r))

    def motex():
        P = [("Alla primtal är udda.", "2"), ("Om x² = 16 så är x = 4.", "x = −4"), ("Summan av två udda tal är udda.", "3 + 5 = 8"), ("Alla fyrhörningar med fyra lika sidor är kvadrater.", "en romb som inte är en kvadrat"),
             ("Om ab = 0 så är a = 0.", "a = 3 och b = 0"), ("Kvadraten på ett tal är alltid större än talet.", "0,5² = 0,25"), ("Alla tal som är delbara med 3 är delbara med 6.", "9")]
        stmt, r = ch(P)
        w = [x[1] for x in P if x[1] != r]
        return M("Vilket är ett motexempel till påståendet: <i>%s</i>" % stmt, r, sh(w)[:3], "<b>%s</b> visar att påståendet är falskt." % r)

    def begrepp():
        P = [("Vad är en definition?", "En beskrivning av vad ett begrepp betyder", ["Ett påstående som bevisas", "Ett exempel", "En gissning"]),
             ("Vad är en sats?", "Ett påstående som har bevisats", ["En definition", "En gissning som inte bevisats", "Ett motexempel"]),
             ("Vad är ett bevis?", "En logisk kedja av slutsatser som visar att något är sant", ["Ett exempel som stämmer", "En mätning", "En definition"]),
             ("Räcker det med tio exempel för att bevisa ett påstående om alla heltal?", "Nej, det behövs ett allmänt bevis", ["Ja, tio exempel räcker", "Ja, om exemplen är stora", "Nej, det behövs hundra exempel"]),
             ("Vad betyder p ⇔ q?", "p gäller om och endast om q gäller", ["p medför q men inte omvänt", "p och q är falska", "q medför p men inte omvänt"]),
             ("Vad räcker för att visa att ett påstående är falskt?", "Ett enda motexempel", ["Två exempel", "Ett bevis", "En definition"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    def bevis():
        P = [("n är ett heltal. Visa att n(n + 1) alltid är jämnt. Vilket argument är korrekt?", "Ett av två på varandra följande heltal är jämnt", ["n är alltid jämnt", "n + 1 är alltid jämnt", "Det stämmer för n = 2"]),
             ("Summan av två jämna tal 2a och 2b är 2(a + b). Vad visar det?", "Att summan av två jämna tal är jämn", ["Att alla tal är jämna", "Att a + b är jämnt", "Ingenting"]),
             ("Varför är (2n + 1)² alltid udda?", "Den blir 4n² + 4n + 1 = 2(2n² + 2n) + 1", ["Den blir 4n² + 1", "För att 2n + 1 är jämnt", "Det stämmer för n = 1"]),
             ("Vinkelsumman i en triangel är 180°. Varför är vinkelsumman i en fyrhörning 360°?", "Den kan delas i två trianglar med en diagonal", ["Den har fyra räta vinklar", "360 = 4 · 90", "Det går inte att visa"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    def sant():
        a = ri(2, 9)
        P = [("Om x = %d så är x² = %d." % (a, a * a), "Sant"), ("Om x² = %d så är x = %d." % (a * a, a), "Falskt"), ("x² = %d ⇔ x = %d eller x = −%d" % (a * a, a, a), "Sant"),
             ("x > %d ⇒ x > %d" % (a, a - 1), "Sant"), ("x > %d ⇒ x > %d" % (a, a + 1), "Falskt"), ("2x = %d ⇔ x = %d" % (2 * a, a), "Sant"), ("x · %d = 0 ⇒ x = 0" % a, "Sant"), ("x² > 0 för alla x", "Falskt")]
        q, r = ch(P)
        return M("Är påståendet sant eller falskt? <i>%s</i>" % q, r, ["Falskt" if r == "Sant" else "Sant", "Sant bara för positiva x", "Det går inte att avgöra"], "<b>%s</b>." % r)

    sets = [("Implikation och ekvivalens", [(pil, 20)]), ("Sant eller falskt", [(sant, 20)]), ("Motexempel", [(motex, 7), (pil, 13)]), ("Definition, sats och bevis", [(begrepp, 6), (bevis, 4), (sant, 10)]), ("Blandat", [(pil, 10), (sant, 10)])]
    return U("logik-och-bevis", "LG", "Logik och bevis: implikation, ekvivalens och motexempel", "Logik och bevis",
             "Begreppen implikation och ekvivalens samt skillnaden mellan definition, sats och bevis.",
             "Uppgifter om logik och bevis för Matematik 2c: implikation och ekvivalens, sant eller falskt, motexempel och definition, sats och bevis. 100 uppgifter med facit.",
             "p ⇒ q: om p så q", "p ⇔ q: p om och endast om q.", sets,
             ["p ⇒ q betyder att om p är sant så är q sant. Det säger inget om det omvända.",
              "p ⇔ q betyder att p och q är ekvivalenta: båda pilarna gäller.",
              "Ett påstående om alla fall bevisas med ett allmänt resonemang. Ett enda motexempel räcker för att visa att det är falskt."],
             [("x = 3 och x² = 9", ["x = 3 ⇒ x² = 9", "Men x² = 9 ger också x = −3"], "x = 3 ⇒ x² = 9")],
             [["Skriver ⇔ när bara ⇒ gäller", "Kontrollera båda riktningarna"], ["Tror att exempel bevisar", "Exempel visar inte att det gäller alltid"], ["Blandar ihop sats och definition", "En sats bevisas, en definition bestäms"]],
             [("Vad är ett motsägelsebevis?", "Man antar motsatsen och visar att det leder till något omöjligt (nivå 5)."), ("Varför är bevis viktiga?", "De visar att något gäller i alla fall, inte bara i de exempel man prövat."), ("Vad är ett axiom?", "Ett grundantagande som inte bevisas.")])


# ============================================================ geometriska satser
def satser():
    def rand():
        v = ri(20, 80)
        k = ri(0, 2)
        if k == 0:
            return MN("En randvinkel står på samma båge som medelpunktsvinkeln %d°. Hur stor är randvinkeln?" % (2 * v), v, [2 * v, 4 * v if 4 * v < 360 else 180 - v, 180 - 2 * v], "Randvinkeln är hälften av medelpunktsvinkeln: <b>%d°</b>." % v, "°")
        if k == 1:
            return MN("En randvinkel är %d°. Hur stor är medelpunktsvinkeln på samma båge?" % v, 2 * v, [v, 180 - v, F(v, 2)], "Medelpunktsvinkeln är dubbelt så stor: <b>%d°</b>." % (2 * v), "°")
        return M("En triangel är inskriven i en cirkel och en sida är en diameter. Hur stor är vinkeln mitt emot diametern?", "90°", ["180°", "60°", "45°"], "Randvinkeln på en halvcirkel (Thales sats): <b>90°</b>.") if v == 20 else MN("Två randvinklar står på samma båge. Den ena är %d°. Hur stor är den andra?" % v, v, [2 * v, 180 - v, F(v, 2)], "Randvinklar på samma båge är lika stora: <b>%d°</b>." % v, "°")

    def yttre():
        a, b = ri(25, 85), ri(25, 85)
        return MN("I en triangel är två vinklar %d° och %d°. Hur stor är yttervinkeln vid det tredje hörnet?" % (a, b), a + b, [180 - a - b, 360 - a - b, a + b - 10], "Yttervinkelsatsen: yttervinkeln är summan av de två motstående inre vinklarna: <b>%d°</b>." % (a + b), "°")

    def likf():
        a, b = ri(2, 9), ri(2, 9)
        k = ch([2, 3, F(3, 2), F(5, 2)])
        return MN("Två trianglar är likformiga med skalfaktorn %s. En sida i den lilla är %d cm och arean är %d cm². Vad är den stora triangelns area?" % (d(k), a, b), b * k * k, [b * k, b * k ** 3, b + k], "Areaskalan är skalfaktorn i kvadrat: %d · %s² = <b>%s cm²</b>." % (b, d(k), d(b * k * k)), "cm²")

    def pyt():
        x1, y1 = nz(-6, 6), nz(-6, 6)
        a, b, c = ch([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15)])
        sa, sb = ch([1, -1]), ch([1, -1])
        x2, y2 = x1 + sa * a, y1 + sb * b
        k = ri(0, 1)
        if k == 0:
            return MN("Beräkna avståndet mellan (%s, %s) och (%s, %s)." % (sg(x1), sg(y1), sg(x2), sg(y2)), c, [a + b, c * c, abs(a - b) + c], "d = √((%s)² + (%s)²) = √%d = <b>%d</b>." % (sg(x2 - x1), sg(y2 - y1), c * c, c))
        return M("Vilken är mittpunkten på sträckan mellan (%s, %s) och (%s, %s)?" % (sg(x1), sg(y1), sg(x2), sg(y2)), "(%s, %s)" % (sg(F(x1 + x2, 2)), sg(F(y1 + y2, 2))), ["(%s, %s)" % (sg(F(x2 - x1, 2)), sg(F(y2 - y1, 2))), "(%s, %s)" % (sg(x1 + x2), sg(y1 + y2)), "(%s, %s)" % (sg(F(y1 + y2, 2)), sg(F(x1 + x2, 2)))], "Medelvärdet av koordinaterna: <b>(%s, %s)</b>." % (sg(F(x1 + x2, 2)), sg(F(y1 + y2, 2))))

    def vinkelsumma():
        n = ri(5, 12)
        return MN("Hur stor är vinkelsumman i en %d-hörning?" % n, 180 * (n - 2), [180 * n, 360 * (n - 2), 180 * (n - 1)], "Den kan delas i %d trianglar: %d · 180° = <b>%s°</b>." % (n - 2, n - 2, num(180 * (n - 2))), "°")

    sets = [("Randvinkelsatsen", [(rand, 20)]), ("Yttervinkelsatsen", [(yttre, 20)]), ("Likformighet", [(likf, 20)]), ("Pythagoras i koordinatsystem", [(pyt, 20)]), ("Blandade satser", [(vinkelsumma, 7), (rand, 7), (pyt, 6)])]
    return U("geometriska-satser", "LG", "Geometriska satser: randvinklar, yttervinklar och likformighet", "Geometriska satser",
             "Geometriska satser om vinklar och likformighet samt Pythagoras sats i koordinatsystem. Definition, sats och bevis.",
             "Uppgifter om geometriska satser för Matematik 2c: randvinkelsatsen, yttervinkelsatsen, likformighet, avstånds- och mittpunktsformeln och vinkelsummor. 100 uppgifter med facit.",
             "Randvinkeln = halva medelpunktsvinkeln", "Yttervinkeln = summan av motstående vinklar.", sets,
             ["Randvinkelsatsen: en randvinkel är hälften så stor som medelpunktsvinkeln på samma båge. En randvinkel på en halvcirkel är rät (Thales sats).",
              "Yttervinkelsatsen: en yttervinkel i en triangel är lika stor som summan av de två motstående inre vinklarna.",
              "Avståndsformeln d = √((x₂ − x₁)² + (y₂ − y₁)²) bygger på Pythagoras sats."],
             [("Medelpunktsvinkel 140°", ["Randvinkeln är hälften"], "70°"), ("Avstånd (1, 2) till (4, 6)", ["√(3² + 4²)"], "5")],
             [["Randvinkeln = medelpunktsvinkeln", "Randvinkeln är hälften"], ["Mittpunkt = skillnaden/2", "Mittpunkt = summan/2"], ["Areaskala = längdskala", "Areaskala = längdskala²"]],
             [("Vad är en randvinkel?", "En vinkel med spetsen på cirkeln och vars ben skär cirkeln."), ("Hur bevisas yttervinkelsatsen?", "Yttervinkeln och den intilliggande vinkeln bildar 180°, liksom triangelns tre vinklar."), ("Vad är Thales sats?", "Att en triangel inskriven i en halvcirkel är rätvinklig.")])


UNITS = {"ekvationssystem": system, "kvadreringsreglerna-och-konjugatregeln": kvadrering, "andragradsekvationer": andragrad, "andragradsfunktioner": andragradsfn,
         "logaritmer": logaritmer, "exponentialekvationer": expekv, "rotekvationer": rotekv, "standardavvikelse-och-percentiler": spridning,
         "normalfordelning": normal, "regression-och-korrelation": regression, "logik-och-bevis": logik, "geometriska-satser": satser}
