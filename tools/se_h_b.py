# -*- coding: utf-8 -*-
"""Sverige årskurs 7–9: algebra（uttryck, ekvationer, mönster och formler, parenteser, olikheter, kvadreringsreglerna, ekvationssystem, x²）"""
import math
from fractions import Fraction as F
from se_h import (gen, MQ, lista, ri, ch, sh, cap, fr, fq, d, par, sg, M, MN, rd, sup, unit, tab, K, num, kr, NB, MIN, coin, expr, kosy, RED, BLUE, GREEN, figure)


def nz(a, b):
    while True:
        v = ri(a, b)
        if v:
            return v


def X(k, v="x"):
    return expr([(k, v)])


# ============================================================ algebraiska uttryck
def uttryck(lv):
    def forenkla():
        a, b, c = nz(-9, 12), nz(-9, 12), nz(-15, 15)
        v = ch(["x", "a", "y", "n"])
        k = ri(0, 2)
        if k == 0:
            q = "%s + %s" % (X(a, v), X(b, v)) if b > 0 else "%s − %s" % (X(a, v), X(-b, v))
            r = X(a + b, v)
            return M("Förenkla %s." % q, r, [X(a * b, v) if a * b != a + b else X(a + b + 1, v), "%s%s" % (X(a + b, v), sup(2)), X(a - b, v)], "Lägg ihop termerna med %s: <b>%s</b>." % (v, r)) if a + b else None
        if k == 1:
            q = expr([(a, v), (c, ""), (b, v)])
            r = expr([(a + b, v), (c, "")])
            return M("Förenkla %s." % q, r, [expr([(a + b + c, v)]), expr([(a + b, v), (-c, "")]), expr([(a, v), (b + c, v)])], "Lägg ihop %s-termerna för sig och talen för sig: <b>%s</b>." % (v, r)) if a + b and a + b + c else None
        m = ri(2, 9)
        q = "%d · %s" % (m, X(a, v)) if a > 0 else "%d · (%s)" % (m, X(a, v))
        return M("Förenkla %s." % q, X(m * a, v), [X(m + a, v) if m + a else X(m * a + 1, v), "%d%s" % (m, X(a, v)) if a > 0 else X(-m * a, v), "%s%s" % (X(m * a, v), sup(2))], "%d · %d = %d: <b>%s</b>." % (m, a, m * a, X(m * a, v)))

    def varde():
        x = nz(-6, 9)
        a, b = nz(-7, 9), nz(-12, 15)
        k = ri(0, 3)
        if k == 0:
            q, v = expr([(a, "x"), (b, "")]), a * x + b
            e = "%s · %s %s %d = <b>%s</b>." % (sg(a), par(x), "+" if b > 0 else "−", abs(b), d(v))
            w = [a + x + b, a * (x + b), -v]
        elif k == 1:
            q, v = "x² %s %d" % ("+" if b > 0 else "−", abs(b)), x * x + b
            e = "%s² = %d, sedan %d %s %d = <b>%s</b>." % (par(x), x * x, x * x, "+" if b > 0 else "−", abs(b), d(v))
            w = [2 * x + b, -x * x + b, x + b]
        elif k == 2:
            q, v = "%d(x %s %d)" % (abs(a) + 1, "+" if b > 0 else "−", abs(b)), (abs(a) + 1) * (x + b)
            e = "Parentesen först: %s %s %d = %d. Sedan %d · %s = <b>%s</b>." % (sg(x), "+" if b > 0 else "−", abs(b), x + b, abs(a) + 1, par(x + b), d(v))
            w = [(abs(a) + 1) * x + b, abs(a) + 1 + x + b, -v]
        else:
            y = nz(-5, 6)
            q, v = "3x − 2y" if coin() else "2x + 3y", None
            v = 3 * x - 2 * y if q == "3x − 2y" else 2 * x + 3 * y
            e = "Sätt in x = %s och y = %s: <b>%s</b>." % (sg(x), sg(y), d(v))
            w = [3 * x + 2 * y if q == "3x − 2y" else 2 * x - 3 * y, x + y, v + 6]
            return MN("Vad är värdet av %s om x = %s och y = %s?" % (q, sg(x), sg(y)), v, w, e)
        return MN("Vad är värdet av %s om x = %s?" % (q, sg(x)), v, w, e)

    def multin():
        a, b, c = ri(2, 9), nz(-9, 9), nz(-9, 9)
        if coin():
            q = "%d(x %s %d)" % (a, "+" if b > 0 else "−", abs(b))
            r = expr([(a, "x"), (a * b, "")])
            return M("Multiplicera in: %s." % q, r, [expr([(a, "x"), (b, "")]), expr([(a, "x"), (-a * b, "")]), expr([(a + b, "x")])], "Multiplicera båda termerna med %d: <b>%s</b>." % (a, r))
        q = "%s − %d(x %s %d)" % (expr([(c, "x")]), a, "+" if b > 0 else "−", abs(b))
        r = expr([(c - a, "x"), (-a * b, "")])
        return M("Förenkla %s." % q, r, [expr([(c - a, "x"), (a * b, "")]), expr([(c + a, "x"), (-a * b, "")]), expr([(c - a, "x"), (-b, "")])], "Minus framför parentesen byter tecken: %s %s = <b>%s</b>." % (expr([(c, "x")]), expr([(-a, "x"), (-a * b, "")]).replace("−", "− ", 1) if False else "− %s" % expr([(a, "x"), (a * b, "")]), r)) if c != a else None

    def skriv():
        nm, g = K().next()
        n = ri(2, 9)
        hon = "hon" if g == "f" else "han"
        opts = [("%s är x år. %s mamma är %d gånger så gammal. Hur gammal är mamman?" % (nm, "Hennes" if g == "f" else "Hans", n), "%dx" % n, ["x + %d" % n, "x − %d" % n, "%d − x" % n]),
                ("En biljett kostar x kr. %s köper %d biljetter och betalar %d kr för programmet. Vad kostar det?" % (nm, n, n * 5), "%dx + %d" % (n, n * 5), ["%d(x + %d)" % (n, n * 5), "x + %d" % (n + n * 5), "%dx" % (n + n * 5)]),
                ("%s har x kr och köper en tröja för %d kr. Hur mycket har %s kvar?" % (nm, n * 25, hon), "x − %d" % (n * 25), ["%d − x" % (n * 25), "x + %d" % (n * 25), "%dx" % (n * 25)]),
                ("En rektangel är x cm bred och %d cm längre än den är bred. Vad är längden?" % n, "x + %d" % n, ["%dx" % n, "x − %d" % n, "2x + %d" % n]),
                ("%d personer delar lika på x kr. Hur mycket får var och en?" % n, "x/%d" % n, ["%dx" % n, "%d/x" % n, "x − %d" % n]),
                ("Ett tal x dubbleras och sedan läggs %d till. Vilket uttryck passar?" % n, "2x + %d" % n, ["2(x + %d)" % n, "x² + %d" % n, "x + %d" % (2 * n)])]
        q, r, w = ch(opts)
        return M(q, r, w, "Uttrycket <b>%s</b> beskriver situationen." % r)

    def figur():
        a, b = ri(2, 6), ri(1, 9)
        k = ri(0, 2)
        if k == 0:
            pts = {"A": (0, 0), "B": (5, 0), "C": (5, 3), "D": (0, 3)}
            fig = figure(pts, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], [("A", "B", "%dx" % a), ("B", "C", "x + %d" % b)], [("A", "B", "D")], W=300, H=180, label="rektangel med sidorna %dx och x + %d" % (a, b))
            r = expr([(2 * a + 2, "x"), (2 * b, "")])
            return M("Skriv ett förenklat uttryck för omkretsen av rektangeln.<div class='qfig'>%s</div>" % fig, r, [expr([(a + 1, "x"), (b, "")]), expr([(2 * a + 2, "x"), (b, "")]), "%dx²" % (a * 2) if False else expr([(a, "x²"), (a * b, "x")])], "O = 2 · %dx + 2(x + %d) = %dx + 2x + %d = <b>%s</b>." % (a, b, 2 * a, 2 * b, r))
        if k == 1:
            pts = {"A": (0, 0), "B": (4, 0), "C": (1.5, 3)}
            fig = figure(pts, [("A", "B"), ("B", "C"), ("C", "A")], [("A", "B", "%dx" % a), ("B", "C", "x + %d" % b), ("C", "A", "%dx − %d" % (a + 1, 1))], W=300, H=190, label="triangel")
            r = expr([(2 * a + 2, "x"), (b - 1, "")])
            return M("Skriv ett förenklat uttryck för omkretsen av triangeln.<div class='qfig'>%s</div>" % fig, r, [expr([(2 * a + 2, "x"), (b + 1, "")]), expr([(2 * a + 1, "x"), (b - 1, "")]), expr([(a + 2, "x"), (b, "")])], "%dx + x + %d + %dx − 1 = <b>%s</b>." % (a, b, a + 1, r))
        pts = {"A": (0, 0), "B": (5, 0), "C": (5, 3), "D": (0, 3)}
        fig = figure(pts, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")], [("A", "B", "x + %d" % b), ("B", "C", "%d" % a)], [("A", "B", "D")], W=300, H=180, label="rektangel med sidorna x + %d och %d" % (b, a))
        r = expr([(a, "x"), (a * b, "")])
        return M("Skriv ett förenklat uttryck för arean av rektangeln.<div class='qfig'>%s</div>" % fig, r, [expr([(a, "x"), (b, "")]), expr([(1, "x"), (a * b, "")]), expr([(2, "x"), (2 * b + 2 * a, "")])], "A = %d(x + %d) = <b>%s</b>." % (a, b, r))

    sets = [("Förenkla uttryck", [(forenkla, 20)]), ("Värdet av ett uttryck", [(varde, 20)]), ("Multiplicera in", [(multin, 20)]),
            ("Skriv ett uttryck", [(skriv, 12), (figur, 8)]), ("Uttryck för omkrets och area", [(figur, 12), (forenkla, 8)])]
    return unit("algebraiska-uttryck", "A", "Algebraiska uttryck: förenkla, beräkna och tolka", "Algebraiska uttryck",
                "Innebörden av variabelbegreppet och dess användning i algebraiska uttryck, formler och ekvationer. Algebraiska uttryck som beskriver vardagliga och matematiska situationer.",
                "Arbetsblad om algebraiska uttryck för årskurs 7: förenkla, beräkna värdet, multiplicera in och skriv uttryck för omkrets och area. 100 uppgifter med facit.",
                "Lägg bara ihop termer av samma sort", "3x + 2 kan inte förenklas mer.", sets,
                ["En variabel är en bokstav som står för ett tal. 4x betyder 4 · x.",
                 "Förenkla genom att lägga ihop termer av samma sort: 3x + 5 + 2x = 5x + 5. x-termer och tal kan inte läggas ihop.",
                 "Värdet av ett uttryck får du genom att sätta in talet i stället för variabeln: om x = 3 blir 4x − 1 = 4 · 3 − 1 = 11."],
                [("Förenkla 3x + 5 + 2x − 1", ["x-termer: 3x + 2x = 5x", "Tal: 5 − 1 = 4"], "5x + 4"), ("Multiplicera in 4(x − 3)", ["4 · x = 4x", "4 · 3 = 12"], "4x − 12")],
                [["3x + 2 = 5x", "x-termer och tal läggs inte ihop: 3x + 2"], ["4(x − 3) = 4x − 3", "Båda termerna multipliceras: 4x − 12"], ["x · x = 2x", "x · x = x²"]],
                [("Varför kan man inte lägga ihop 3x och 2?", "3x är tre stycken x och 2 är bara ett tal. Det är som att lägga ihop 3 äpplen och 2 kronor."),
                 ("Vad betyder 2x²?", "2 · x · x. Bara x upphöjs, inte 2."), ("Hur kontrollerar jag en förenkling?", "Sätt in ett tal för x i båda uttrycken. De ska ge samma värde.")])


# ============================================================ ekvationer
def ekvationer(lv):
    def ett():
        x, a, b = nz(-9, 15), ri(2, 9), nz(-20, 30)
        c = a * x + b
        q = "%s = %s" % (expr([(a, "x"), (b, "")]), d(c))
        return M("Lös ekvationen %s." % q, "x = %s" % d(x), ["x = %s" % d(v) for v in (x + 1, -x, F(c + b, a) if F(c + b, a) != x else x + 2, c - b)],
                 "%s båda leden: %dx = %s. Dela med %d: <b>x = %s</b>." % ("Subtrahera %d från" % b if b > 0 else "Addera %d till" % -b, a, d(c - b), a, d(x)))

    def bada():
        x = nz(-8, 12)
        a, c = ri(3, 12), ri(1, 9)
        if a == c:
            return None
        if a < c:
            a, c = c, a
        b = nz(-15, 15)
        dd = (a - c) * x + b
        q = "%s = %s" % (expr([(a, "x"), (b, "")]), expr([(c, "x"), (dd, "")]))
        return M("Lös ekvationen %s." % q, "x = %s" % d(x), ["x = %s" % sg(F(dd - b, a + c)) if F(dd - b, a + c) != x else "x = %s" % d(x + 1), "x = %s" % d(-x), "x = %s" % d(x + 2), "x = %s" % d(dd - b)],
                 "Samla x på ena sidan: %dx = %s. Dela med %d: <b>x = %s</b>." % (a - c, d(dd - b), a - c, d(x)))

    def parentes():
        x = nz(-6, 10)
        a, b, c = ri(2, 6), nz(-8, 8), nz(-10, 20)
        r = a * (x + b) + c
        q = "%d(x %s %d) %s %d = %s" % (a, "+" if b > 0 else "−", abs(b), "+" if c > 0 else "−", abs(c), d(r))
        return M("Lös ekvationen %s." % q, "x = %s" % d(x), ["x = %s" % sg(v) for v in ((F(r - c, a) - b) * -1 if (F(r - c, a) - b) * -1 != x else x + 3, F(r - c - b, a) if F(r - c - b, a) != x else x - 2, x + 1, -x)],
                 "Multiplicera in: %s = %s. Lös: <b>x = %s</b>." % (expr([(a, "x"), (a * b + c, "")]), d(r), d(x)))

    def brak_():
        x = ri(1, 12)
        a = ch([2, 3, 4, 5, 6])
        x = x * a
        b = nz(-9, 9)
        c = F(x, a) + b
        q = "x/%d %s %d = %s" % (a, "+" if b > 0 else "−", abs(b), d(c))
        return M("Lös ekvationen %s." % q, "x = %s" % d(x), ["x = %s" % d(v) for v in (c - b, (c + b) * a if (c + b) * a != x else x + a, x + a, F(x, a))],
                 "%s: x/%d = %s. Multiplicera med %d: <b>x = %s</b>." % ("Subtrahera %d" % b if b > 0 else "Addera %d" % -b, a, d(c - b), a, d(x)))

    def text_():
        nm = K().name()
        k = ri(0, 4)
        if k == 0:
            x, n, p = ri(15, 80), ri(3, 8), ri(20, 90)
            return M("%s köper %d likadana tröjor och en mössa för %s. Det kostar totalt %s. Vad kostar en tröja?" % (nm, n, kr(p), kr(n * x + p)), kr(x), [kr(x + p), kr((n * x + p) // n), kr(x - 5)],
                     "%dx + %d = %d ger %dx = %d och <b>x = %d kr</b>." % (n, p, n * x + p, n, n * x, x))
        if k == 1:
            x = ri(5, 40)
            s = 3 * x + 3
            return M("Summan av tre tal som följer på varandra är %d. Vilket är det minsta talet?" % s, str(x), [str(x + 1), str(s // 3 + 1), str(x - 1)], "x + (x + 1) + (x + 2) = 3x + 3 = %d ger <b>x = %d</b>." % (s, x))
        if k == 2:
            b, extra = ri(4, 15), ri(2, 10)
            o = 2 * b + 2 * (b + extra)
            return M("En rektangel har omkretsen %d cm. Längden är %d cm längre än bredden. Hur bred är rektangeln?" % (o, extra), "%d cm" % b, ["%d cm" % (b + extra), "%d cm" % (o // 4), "%d cm" % (o // 2 - extra)],
                     "2x + 2(x + %d) = %d ger 4x + %d = %d och <b>x = %d cm</b>." % (extra, o, 2 * extra, o, b)) if o // 4 != b else None
        if k == 3:
            y = ri(4, 15)
            m = ri(3, 5)
            t = ri(2, 6)
            f = m * y
            return M("%s mamma är %d gånger så gammal som %s. Om %d år är summan av deras åldrar %d. Hur gammal är %s nu?" % (gen(nm), m, nm, t, f + y + 2 * t, nm), "%d år" % y, ["%d år" % (y + t), "%d år" % ((f + y + 2 * t) // (m + 1)) if (f + y + 2 * t) // (m + 1) != y else "%d år" % (y - 1), "%d år" % f],
                     "x + %dx + %d = %d ger %dx = %d och <b>x = %d</b>." % (m, 2 * t, f + y + 2 * t, m + 1, (m + 1) * y, y))
        a, b = ri(150, 400), ri(30, 90)
        c, dd = ri(400, 900), ri(10, 25)
        if b <= dd or (c - a) % (b - dd):
            return None
        x = (c - a) // (b - dd)
        return M("Mobilabonnemang A kostar %s plus %s per månad. B kostar %s plus %s per månad. Efter hur många månader kostar de lika mycket?" % (kr(a), kr(b), kr(c), kr(dd)), "%d månader" % x, ["%d månader" % (x + 1), "%d månader" % (x * 2), "%d månader" % ((c + a) // (b + dd))] if (c + a) // (b + dd) not in (x, x + 1, 2 * x) else ["%d månader" % (x + 1), "%d månader" % (x * 2), "%d månader" % (x + 3)],
                 "%d + %dx = %d + %dx ger %dx = %d och <b>x = %d</b>." % (a, b, c, dd, b - dd, c - a, x))

    if lv == 7:
        sets = [("Ekvationer i ett steg", [(ett, 20)]), ("Ekvationer i två steg", [(ett, 10), (brak_, 10)]), ("x på båda sidor", [(bada, 20)]),
                ("Ekvationer med bråk", [(brak_, 20)]), ("Ställ upp och lös", [(text_, 20)])]
    else:
        sets = [("Ekvationer i två steg", [(ett, 20)]), ("x på båda sidor", [(bada, 20)]), ("Ekvationer med parenteser", [(parentes, 20)]),
                ("Ekvationer med bråk", [(brak_, 20)]), ("Ställ upp och lös", [(text_, 20)])]
    return unit("ekvationer", "A", "Ekvationer: lös och ställ upp ekvationer" if lv == 7 else "Ekvationer: parenteser, bråk och x på båda sidor", "Ekvationer",
                "Innebörden av variabelbegreppet och dess användning i algebraiska uttryck, formler och ekvationer. Metoder för ekvationslösning. Ekvationer som beskriver vardagliga och matematiska situationer.",
                "Arbetsblad om ekvationer för årskurs %d: ekvationer i två steg, x på båda sidor%s, bråk och problem där du ställer upp en ekvation. 100 uppgifter med facit." % (lv, ", parenteser" if lv == 8 else ""),
                "Gör samma sak i båda leden", "Kontrollera genom att sätta in svaret.", sets,
                ["En ekvation är som en våg i balans. Gör du samma sak i båda leden är den fortfarande i balans.",
                 "Ta först bort talet som läggs till eller dras bort, dela sedan med koefficienten: 3x + 7 = 22 ger 3x = 15 och x = 5.",
                 "Står x på båda sidor samlar du x-termerna på den ena sidan: 5x − 4 = 2x + 11 ger 3x = 15 och x = 5."],
                [("3x + 7 = 22", ["Subtrahera 7: 3x = 15", "Dela med 3"], "x = 5"), ("5x − 4 = 2x + 11", ["Subtrahera 2x: 3x − 4 = 11", "Addera 4: 3x = 15"], "x = 5")],
                [["3x + 7 = 22 ger 3x = 29", "Subtrahera 7, inte addera: 3x = 15"], ["Delar bara en term med 3", "Hela leden delas: 3x = 15 ger x = 5"], ["2(x + 3) = 2x + 3", "Multiplicera in i båda termerna: 2x + 6"]],
                [("Vad är ett led?", "Det som står på ena sidan om likhetstecknet."), ("Hur vet jag att svaret är rätt?", "Sätt in värdet i ekvationen. Om vänster led och höger led blir lika är svaret rätt."),
                 ("Hur ställer jag upp en ekvation?", "Kalla det du söker för x, skriv ett uttryck för det som är lika och sätt likhetstecken.")])


# ============================================================ mönster och formler
def monster(lv):
    def nterm():
        a, k = ri(-5, 12), ri(2, 9)
        seq = [a + k * i for i in range(1, 5)]
        r = expr([(k, "n"), (a, "")])
        return M("En talföljd börjar %s, … Vilken formel ger term nummer n?" % ", ".join(sg(x) for x in seq), r, [expr([(k, "n")]), expr([(1, "n"), (k, "")]), expr([(k, "n"), (seq[0], "")])], "Differensen är %d, så formeln börjar med %dn. %d · 1 + %s = %s: <b>%s</b>." % (k, k, k, par(a) if a < 0 else str(a), sg(seq[0]), r))

    def term():
        a, k = ri(-5, 12), ri(2, 9)
        n = ri(10, 100)
        seq = [a + k * i for i in range(1, 5)]
        v = a + k * n
        return MN("Talföljden %s, … fortsätter på samma sätt. Vilket tal står på plats %d?" % (", ".join(sg(x) for x in seq), n), v, [seq[0] * n, k * n, v + k], "Formeln är %s. Med n = %d: <b>%s</b>." % (expr([(k, "n"), (a, "")]), n, num(v)))

    def figur():
        k, a = ri(2, 5), ri(0, 4)
        xs = [k * i + a for i in range(1, 4)]
        n = ri(8, 40)
        from se_m_b import dots_fig
        fig = dots_fig(xs)
        if coin():
            r = expr([(k, "n"), (a, "")])
            return M("Figurerna växer på samma sätt. Vilken formel ger antalet rutor i figur n?<div class='qfig'>%s</div>" % fig, r, [expr([(xs[0], "n")]) if xs[0] != k else expr([(k + 1, "n")]), expr([(1, "n"), (k, "")]), expr([(k, "n"), (a + 1, "")])], "Det blir %d fler rutor varje gång. Figur 1 har %d: <b>%s</b>." % (k, xs[0], r))
        return MN("Figurerna växer på samma sätt. Hur många rutor har figur %d?<div class='qfig'>%s</div>" % (n, fig), k * n + a, [xs[0] * n, k * n, k * n + a + k], "Formeln är %s. %d · %d + %d = <b>%d</b>." % (expr([(k, "n"), (a, "")]), k, n, a, k * n + a))

    def formel():
        k = ri(0, 3)
        if k == 0:
            n = ri(3, 30)
            return MN("En taxi kostar 45 kr i grundavgift och 12 kr per kilometer. Formeln är K = 45 + 12s. Vad kostar en resa på %d km?" % n, 45 + 12 * n, [57 * n, 45 + n, 12 * n], "K = 45 + 12 · %d = <b>%d kr</b>." % (n, 45 + 12 * n), "kr")
        if k == 1:
            b, h = ri(3, 20), ri(2, 16)
            return MN("Arean av en triangel är A = bh/2. Vad är A om b = %d cm och h = %d cm?" % (b, h), F(b * h, 2), [b * h, b + h, 2 * b * h], "A = %d · %d / 2 = <b>%s cm²</b>." % (b, h, d(F(b * h, 2))), "cm²")
        if k == 2:
            v, t = ri(3, 25) * 5, ri(2, 6)
            return MN("Sträckan är s = v · t. Hur långt kommer en bil på %d timmar med farten %d km/h?" % (t, v), v * t, [v + t, v * t * 2, v // t if v % t == 0 else v * t + v], "s = %d · %d = <b>%d km</b>." % (v, t, v * t), "km")
        n = ri(3, 12)
        return MN("Antalet tändstickor i figur n är 3n + 1. Hur många tändstickor behövs till figur %d?" % n, 3 * n + 1, [3 * n, 4 * n, 3 * (n + 1)], "3 · %d + 1 = <b>%d</b>." % (n, 3 * n + 1), "stickor")

    def baklanges():
        k, a = ri(2, 9), ri(-5, 10)
        n = ri(6, 40)
        v = k * n + a
        return MN("Formeln %s ger talen i en talföljd. Vilket nummer n har talet %s?" % (expr([(k, "n"), (a, "")]), num(v)), n, [n + 1, v // k, n - 1] if v // k not in (n, n + 1, n - 1) else [n + 1, n - 1, n + 2], "%s = %d ger %dn = %d och <b>n = %d</b>." % (expr([(k, "n"), (a, "")]), v, k, v - a, n))

    sets = [("Fortsätt talföljden", [(term, 20)]), ("Formel för talföljder", [(nterm, 20)]), ("Växande figurer", [(figur, 20)]),
            ("Använd en formel", [(formel, 20)]), ("Baklänges med formler", [(baklanges, 12), (nterm, 8)])]
    return unit("monster-och-formler", "A", "Mönster och formler: talföljder och växande figurer", "Mönster och formler",
                "Hur algebraiska uttryck, formler och ekvationer kan användas för att beskriva mönster och generalisera. Talföljder och geometriska mönster.",
                "Arbetsblad om mönster och formler för årskurs 7: talföljder, formel för term nummer n, växande figurer och att använda formler. 100 uppgifter med facit.",
                "Differensen blir talet framför n", "5, 8, 11, 14 … har formeln 3n + 2.", sets,
                ["I en talföljd där det ökar lika mycket varje gång heter ökningen differensen.",
                 "Differensen står framför n i formeln. Sedan justerar du så att n = 1 ger första talet: 5, 8, 11, … har differensen 3, och 3 · 1 + 2 = 5, alltså 3n + 2.",
                 "Med formeln kan du räkna ut vilket tal som helst utan att skriva hela talföljden: term nummer 50 är 3 · 50 + 2 = 152."],
                [("Formel för 5, 8, 11, 14, …", ["Differensen är 3: 3n", "3 · 1 = 3, och 5 − 3 = 2"], "3n + 2"), ("Term nummer 50 i 3n + 2", ["3 · 50 + 2"], "152")],
                [["Formeln för 5, 8, 11 är n + 3", "Det ökar med 3 varje gång: 3n + 2"], ["Term 50 är 50 · 5", "Använd formeln: 3 · 50 + 2 = 152"], ["Glömmer att kontrollera med n = 1", "3 · 1 + 2 = 5 stämmer med första talet"]],
                [("Vad betyder n?", "n är numret på termen eller figuren: 1, 2, 3, …"), ("Kan differensen vara negativ?", "Ja. 20, 17, 14, … har differensen −3 och formeln −3n + 23."),
                 ("Varför vill man ha en formel?", "Den beskriver hela mönstret och gör att du kan räkna ut stora figurnummer snabbt.")])


# ============================================================ parenteser och faktorisering
def parenteser(lv):
    def multin():
        a = nz(-6, 7)
        b, c = nz(-9, 9), nz(-9, 9)
        v = ch(["x", "a", "y"])
        if coin():
            q = "%s(%s)" % (sg(a) if a != -1 else "−", expr([(b, v), (c, "")]))
            r = expr([(a * b, v), (a * c, "")])
            return M("Multiplicera in: %s." % q, r, [expr([(a * b, v), (c, "")]), expr([(a * b, v), (-a * c, "")]), expr([(a + b, v), (a + c, "")])], "Båda termerna multipliceras med %s: <b>%s</b>." % (sg(a), r))
        m = ri(2, 6)
        q = "%s(%s)" % (X(m, v), expr([(b, v), (c, "")]))
        r = expr([(m * b, v + "²"), (m * c, v)])
        return M("Multiplicera in: %s." % q, r, [expr([(m * b, v), (m * c, v)]), expr([(m * b, v + "²"), (c, v)]), expr([(m * b, v + "²"), (m * c, "")])], "%s · %s = %s och %s · %s = %s: <b>%s</b>." % (X(m, v), X(b, v), X(m * b, v + "²"), X(m, v), sg(c), X(m * c, v), r))

    def minus():
        a, b, c = nz(-9, 12), nz(-9, 9), nz(-9, 9)
        q = "%s − (%s)" % (expr([(a, "x")]), expr([(b, "x"), (c, "")]))
        r = expr([(a - b, "x"), (-c, "")])
        return M("Förenkla %s." % q, r, [expr([(a - b, "x"), (c, "")]), expr([(a + b, "x"), (-c, "")]), expr([(a + b, "x"), (c, "")])], "Minus framför parentesen byter tecken på alla termer i den: %s %s = <b>%s</b>." % (expr([(a, "x")]), expr([(-b, "x"), (-c, "")]).replace(MIN, "− ", 1) if expr([(-b, "x"), (-c, "")]).startswith(MIN) else "+ " + expr([(-b, "x"), (-c, "")]), r)) if a != b else None

    def tva():
        a, b = nz(-9, 9), nz(-9, 9)
        q = "(x %s %d)(x %s %d)" % ("+" if a > 0 else "−", abs(a), "+" if b > 0 else "−", abs(b))
        r = expr([(1, "x²"), (a + b, "x"), (a * b, "")])
        return M("Multiplicera ihop %s." % q, r, [expr([(1, "x²"), (a * b, "")]), expr([(1, "x²"), (a * b, "x"), (a + b, "")]), expr([(1, "x²"), (a + b, "x"), (-a * b, "")])], "x · x + x · %s + %s · x + %s · %s = <b>%s</b>." % (par(b), par(a), par(a), par(b), r)) if a + b and a != b else None

    def bryt():
        g = ri(2, 9)
        a, b = nz(-9, 9), nz(-9, 9)
        if math.gcd(a, b) != 1:
            return None
        v = ch(["x", "a", "y"])
        if coin():
            q = expr([(g * a, v), (g * b, "")])
            r = "%d(%s)" % (g, expr([(a, v), (b, "")]))
            return M("Bryt ut den största gemensamma faktorn: %s." % q, r, ["%d(%s)" % (g, expr([(a, v), (g * b, "")])), "%s(%s)" % (v, expr([(g * a, ""), (g * b, "")])) if False else "%d(%s)" % (g * 2, expr([(F(a, 2), v), (F(b, 2), "")])) if a % 2 == 0 and b % 2 == 0 else "%d(%s)" % (g, expr([(a, v), (-b, "")])), "%d%s(%s)" % (g, v, expr([(a, ""), (b, "")])) if False else "%d(%s)" % (g, expr([(a + 1, v), (b, "")]))], "Båda termerna är delbara med %d: <b>%s</b>." % (g, r))
        q = expr([(g * a, v + "²"), (g * b, v)])
        r = "%s(%s)" % (X(g, v), expr([(a, v), (b, "")]))
        return M("Faktorisera %s så långt det går." % q, r, ["%d(%s)" % (g, expr([(a, v + "²"), (b, v)])), "%s(%s)" % (v, expr([(g * a, v), (g * b, "")])), "%s(%s)" % (X(g, v), expr([(a, v), (g * b, "")]))], "Både %d och %s är gemensamma: <b>%s</b>." % (g, v, r))

    def blandat():
        a, b, c, e = ri(2, 6), nz(-6, 6), ri(2, 6), nz(-6, 6)
        q = "%d(x %s %d) + %d(x %s %d)" % (a, "+" if b > 0 else "−", abs(b), c, "+" if e > 0 else "−", abs(e))
        r = expr([(a + c, "x"), (a * b + c * e, "")])
        return M("Förenkla %s." % q, r, [expr([(a + c, "x"), (b + e, "")]), expr([(a * c, "x"), (a * b + c * e, "")]), expr([(a + c, "x"), (a * b - c * e, "")])], "%s + %s = <b>%s</b>." % (expr([(a, "x"), (a * b, "")]), expr([(c, "x"), (c * e, "")]), r)) if a * b + c * e != b + e else None

    sets = [("Multiplicera in", [(multin, 20)]), ("Minus framför parentes", [(minus, 20)]), ("Två parenteser", [(tva, 20)]),
            ("Bryt ut och faktorisera", [(bryt, 20)]), ("Förenkla uttryck", [(blandat, 12), (minus, 8)])]
    return unit("parenteser-och-faktorisering", "A", "Parenteser och faktorisering: multiplicera in och bryt ut", "Parenteser och faktorisering",
                "Innebörden av variabelbegreppet och dess användning i algebraiska uttryck. Metoder för att förenkla uttryck: multiplicera in i parenteser och bryta ut gemensamma faktorer.",
                "Arbetsblad om parenteser och faktorisering för årskurs 8: multiplicera in, minus framför parentes, multiplicera två parenteser och bryt ut gemensam faktor. 100 uppgifter med facit.",
                "a(b + c) = ab + ac", "Att bryta ut är att multiplicera in baklänges.", sets,
                ["Multiplicera talet framför parentesen med varje term i den: 3(x + 4) = 3x + 12.",
                 "Minus framför en parentes byter tecken på alla termer: 5 − (x − 2) = 5 − x + 2 = 7 − x.",
                 "Två parenteser: varje term i den första multipliceras med varje term i den andra: (x + 2)(x + 3) = x² + 3x + 2x + 6 = x² + 5x + 6."],
                [("(x + 2)(x + 3)", ["x · x + x · 3 + 2 · x + 2 · 3", "x² + 3x + 2x + 6"], "x² + 5x + 6"), ("Faktorisera 6x + 15", ["Gemensam faktor 3"], "3(2x + 5)")],
                [["3(x + 4) = 3x + 4", "Båda termerna: 3x + 12"], ["5 − (x − 2) = 3 − x", "Tecknen byts: 5 − x + 2 = 7 − x"], ["(x + 2)(x + 3) = x² + 6", "Glöm inte mitten: x² + 5x + 6"]],
                [("Hur kontrollerar jag en faktorisering?", "Multiplicera in igen. Du ska få tillbaka uttrycket du började med."),
                 ("Vad är en gemensam faktor?", "Ett tal eller en variabel som alla termer kan delas med."), ("Varför är faktorisering bra?", "Det förenklar bråk och hjälper dig att lösa ekvationer.")])


# ============================================================ formler
def formler(lv):
    def berakna():
        k = ri(0, 4)
        if k == 0:
            c = ch([-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40])
            f = F(9, 5) * c + 32
            return M("Formeln F = 1,8C + 32 räknar om grader Celsius till grader Fahrenheit. Vad är %s °C i Fahrenheit?" % sg(c), "%s °F" % d(f), ["%s °F" % d(v) for v in (F(9, 5) * c, F(9, 5) * (c + 32), c + 32)], "F = 1,8 · %s + 32 = <b>%s °F</b>." % (par(c), d(f)))
        if k == 1:
            b, h = ri(3, 15), ri(2, 12)
            a2 = ri(2, 10)
            return MN("Arean av en parallelltrapets är A = (a + b)h/2. Beräkna A om a = %d cm, b = %d cm och h = %d cm." % (a2, b, h), F((a2 + b) * h, 2), [(a2 + b) * h, a2 + b * h, F(a2 + b * h, 2)], "A = (%d + %d) · %d / 2 = <b>%s cm²</b>." % (a2, b, h, d(F((a2 + b) * h, 2))), "cm²")
        if k == 2:
            m, v = ri(40, 90), ri(15, 19) * 10
            bmi = F(m * 10000, v * v)
            return M("BMI beräknas med formeln BMI = m/l², där m är vikten i kg och l längden i meter. Beräkna BMI för en person som väger %d kg och är %s m lång. Avrunda till heltal." % (m, d(F(v, 100))), rd(bmi, 0), [rd(F(m * 100, v), 0), rd(bmi + 3, 0), rd(F(m * 10000, v * v * 2), 0)], "%d / %s² ≈ <b>%s</b>." % (m, d(F(v, 100)), rd(bmi, 0)))
        if k == 3:
            n = ri(3, 12)
            return MN("Vinkelsumman i en månghörning är S = 180(n − 2), där n är antalet hörn. Vad är vinkelsumman i en %d-hörning?" % n, 180 * (n - 2), [180 * n, 180 * (n - 1), 360 * (n - 2)], "S = 180 · (%d − 2) = <b>%s°</b>." % (n, num(180 * (n - 2))), "°")
        t = ri(2, 10)
        return MN("En sten faller s = 5t² meter på t sekunder. Hur långt faller den på %d sekunder?" % t, 5 * t * t, [10 * t, 25 * t, (5 * t) ** 2], "s = 5 · %d² = 5 · %d = <b>%d m</b>." % (t, t * t, 5 * t * t), "m")

    def losut():
        P = [("s = vt", "t", "t = s/v", ["t = sv", "t = v/s", "t = s − v"]), ("A = bh", "h", "h = A/b", ["h = Ab", "h = b/A", "h = A − b"]),
             ("O = 2πr", "r", "r = O/2π", ["r = 2πO", "r = O − 2π", "r = 2π/O"]), ("y = kx + m", "m", "m = y − kx", ["m = y + kx", "m = kx − y", "m = y/kx"]),
             ("y = kx + m", "x", "x = (y − m)/k", ["x = y/k − m", "x = (y + m)/k", "x = k(y − m)"]), ("P = 2a + 2b", "a", "a = (P − 2b)/2", ["a = P − 2b", "a = P/2 + b", "a = (P + 2b)/2"]),
             ("U = RI", "I", "I = U/R", ["I = UR", "I = R/U", "I = U − R"]), ("F = ma", "a", "a = F/m", ["a = Fm", "a = m/F", "a = F − m"]),
             ("V = abc", "c", "c = V/ab", ["c = Vab", "c = ab/V", "c = V − ab"]), ("K = 50 + 8x", "x", "x = (K − 50)/8", ["x = K/8 − 50", "x = (K + 50)/8", "x = 8(K − 50)"]),
             ("A = bh/2", "b", "b = 2A/h", ["b = A/2h", "b = Ah/2", "b = 2Ah"]), ("v = s/t", "s", "s = vt", ["s = v/t", "s = t/v", "s = v + t"])]
        f, v, r, w = ch(P)
        return M("Lös ut %s ur formeln %s." % (v, f), r, w, "Gör samma sak i båda leden tills %s står ensamt: <b>%s</b>." % (v, r))

    def baklanges():
        k = ri(0, 2)
        if k == 0:
            v, t = ri(3, 20) * 5, ri(2, 8)
            return MN("Formeln s = vt gäller. En cyklist åker %d km på %d timmar. Vilken är farten?" % (v * t // 5 if False else v * t, t), v, [v * t * t, v * t - t, v + t], "v = s/t = %d/%d = <b>%d km/h</b>." % (v * t, t, v), "km/h")
        if k == 1:
            b, h = ri(3, 15), ri(2, 12)
            return MN("En triangel har arean %s cm² och basen %d cm. Hur hög är den? Använd A = bh/2." % (d(F(b * h, 2)), b), h, [F(b * h, 2 * b), b * h, h * 2], "h = 2A/b = %s/%d = <b>%d cm</b>." % (num(b * h), b, h), "cm")
        x = ri(3, 30)
        return MN("En hantverkare tar K = 350 + 450x kronor, där x är antalet timmar. Räkningen blev %s. Hur många timmar arbetade hantverkaren?" % kr(350 + 450 * x), x, [x + 1, F(350 + 450 * x, 450), x - 1], "350 + 450x = %d ger 450x = %d och <b>x = %d</b>." % (350 + 450 * x, 450 * x, x), "timmar")

    def tolka():
        P = [("K = 30 + 2x är kostnaden i kr för x minuter. Vad betyder talet 30?", "En fast avgift på 30 kr", ["30 minuter", "Priset per minut", "Den högsta kostnaden"]),
             ("K = 30 + 2x är kostnaden i kr för x minuter. Vad betyder talet 2?", "Priset per minut är 2 kr", ["En fast avgift på 2 kr", "2 minuter gratis", "Kostnaden dubbleras"]),
             ("V = 1 000 − 25t är vattnet i liter i en tank efter t minuter. Vad betyder 25?", "Det rinner ut 25 liter per minut", ["Tanken rymmer 25 liter", "Det tar 25 minuter", "Det fylls på 25 liter per minut"]),
             ("V = 1 000 − 25t är vattnet i liter i en tank efter t minuter. Vad betyder 1 000?", "Tanken har 1 000 liter från början", ["Det rinner ut 1 000 liter per minut", "Det tar 1 000 minuter", "Tanken är tom"]),
             ("L = 12 + 0,5v är längden i cm av en planta efter v veckor. Vad betyder 0,5?", "Plantan växer 0,5 cm per vecka", ["Plantan är 0,5 cm från början", "Det tar 0,5 veckor", "Plantan krymper"]),
             ("L = 12 + 0,5v är längden i cm av en planta efter v veckor. Hur lång var plantan från början?", "12 cm", ["0,5 cm", "12,5 cm", "6 cm"]),
             ("P = 400n − 1 500 är vinsten i kr när en klass säljer n lotter. Hur många lotter måste de sälja för att inte gå med förlust?", "Minst 4 lotter", ["Minst 3 lotter", "Minst 1 500 lotter", "Minst 400 lotter"]),
             ("T = 20 − 6h är temperaturen i °C på höjden h km. Vad betyder 6?", "Det blir 6 grader kallare per km", ["Det är 6 °C på marken", "Det blir 6 grader varmare per km", "Det är 6 km högt"]),
             ("T = 20 − 6h är temperaturen i °C på höjden h km. Vilken temperatur är det på 3 km höjd?", "2 °C", ["−18 °C", "14 °C", "42 °C"]),
             ("A = s² är arean av en kvadrat. Vad händer med arean om sidan dubbleras?", "Den blir fyra gånger så stor", ["Den blir dubbelt så stor", "Den blir lika stor", "Den blir åtta gånger så stor"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    sets = [("Beräkna med formler", [(berakna, 20)]), ("Lös ut en variabel", [(losut, 12), (baklanges, 8)]), ("Räkna baklänges", [(baklanges, 20)]),
            ("Tolka formler", [(tolka, 10), (berakna, 10)]), ("Blandade formler", [(berakna, 10), (baklanges, 10)])]
    return unit("formler", "A", "Formler: beräkna, lös ut och tolka", "Formler",
                "Innebörden av variabelbegreppet och dess användning i algebraiska uttryck, formler och ekvationer. Hur formler kan användas för att beskriva och lösa problem i vardagliga och matematiska situationer.",
                "Arbetsblad om formler för årskurs 8: beräkna med formler, lös ut en variabel, räkna baklänges och tolka vad talen i en formel betyder. 100 uppgifter med facit.",
                "Sätt in de tal du vet och räkna", "Lös ut en variabel på samma sätt som i en ekvation.", sets,
                ["En formel visar hur storheter hänger ihop, till exempel s = v · t för sträcka, fart och tid.",
                 "Sätt in de värden du vet och räkna ut det som saknas: v = 60 km/h och t = 3 h ger s = 60 · 3 = 180 km.",
                 "Att lösa ut en variabel är som att lösa en ekvation. Ur s = vt får du t = s/v genom att dela båda leden med v."],
                [("Lös ut t ur s = vt", ["Dela båda leden med v"], "t = s/v"), ("Beräkna A = bh/2 för b = 8 och h = 5", ["A = 8 · 5 / 2"], "20")],
                [["t = s · v", "Dela med v: t = s/v"], ["Sätter in i fel enhet", "Kontrollera att alla värden har rätt enhet först"], ["I K = 30 + 2x är 30 priset per minut", "30 är den fasta avgiften, 2 är priset per minut"]],
                [("Vad är skillnaden på en formel och en ekvation?", "En formel gäller allmänt för många värden. En ekvation har ett eller några bestämda värden som lösning."),
                 ("Måste jag kunna formlerna utantill?", "På proven får du ofta ett formelblad, men det är bra att förstå vad de betyder."), ("Varför skriver man bh i stället för b · h?", "Det är kortare. Två bokstäver bredvid varandra betyder gånger.")])


# ============================================================ olikheter
def olikheter(lv):
    def tecken():
        a, b = nz(-20, 20), nz(-20, 20)
        if a == b:
            return None
        if coin():
            fa, fb = F(ri(1, 9), ch([2, 3, 4, 5])), F(ri(1, 9), ch([2, 3, 4, 5]))
            if fa == fb:
                return None
            r = "<" if fa < fb else ">"
            return M("Vilket tecken ska stå i rutan? %s □ %s" % (fq(fa), fq(fb)), r, [">" if r == "<" else "<", "=", "≥" if r == ">" else "≤"], "%s ≈ %s och %s ≈ %s, alltså <b>%s</b>." % (fq(fa), rd(fa, 2), fq(fb), rd(fb, 2), r))
        r = "<" if a < b else ">"
        return M("Vilket tecken ska stå i rutan? %s □ %s" % (sg(a), sg(b)), r, [">" if r == "<" else "<", "=", "≥" if r == ">" else "≤"], "%s ligger till %s om %s på tallinjen: <b>%s %s %s</b>." % (sg(a), "vänster" if a < b else "höger", sg(b), sg(a), r, sg(b)))

    def los():
        a, x0 = ri(2, 9), nz(-8, 12)
        b = nz(-15, 15)
        c = a * x0 + b
        op = ch(["<", ">", "≤", "≥"])
        q = "%s %s %s" % (expr([(a, "x"), (b, "")]), op, d(c))
        opp = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}[op]
        return M("Lös olikheten %s." % q, "x %s %s" % (op, d(x0)), ["x %s %s" % (opp, d(x0)), "x %s %s" % (op, d(x0 + 1)), "x %s %s" % (op, sg(F(c + b, a)) if F(c + b, a) != x0 else d(-x0))],
                 "Som en ekvation: %dx %s %s ger <b>x %s %s</b>." % (a, op, d(c - b), op, d(x0)))

    def neg():
        a, x0 = ri(2, 6), nz(-6, 8)
        b = nz(-12, 12)
        c = -a * x0 + b
        op = ch(["<", ">"])
        opp = {"<": ">", ">": "<"}[op]
        q = "%s %s %s" % (expr([(-a, "x"), (b, "")]), op, d(c))
        return M("Lös olikheten %s." % q, "x %s %s" % (opp, d(x0)), ["x %s %s" % (op, d(x0)), "x %s %s" % (opp, d(-x0)) if x0 else "x %s 1" % opp, "x %s %s" % (op, d(-x0)) if x0 else "x %s −1" % op],
                 "%s ger %s. Delar du med ett negativt tal vänds tecknet: <b>x %s %s</b>." % (q, "%s %s %s" % (expr([(-a, "x")]), op, d(c - b)), opp, d(x0)))

    def heltal():
        lo, hi = nz(-8, 5), ri(1, 10)
        hi = lo + hi
        a = ch(["<", "≤"])
        b = ch(["<", "≤"])
        vals = [v for v in range(lo - 1, hi + 2) if (v > lo if a == "<" else v >= lo) and (v < hi if b == "<" else v <= hi)]
        if not vals or len(vals) > 12:
            return None
        n = len(vals)
        return MN("Hur många heltal x uppfyller %s %s x %s %s?" % (sg(lo), a, b, sg(hi)), n, [n + 1, n - 1 if n > 1 else n + 2, hi - lo + 1 if hi - lo + 1 not in (n, n + 1, n - 1) else n + 3], "Heltalen är %s: <b>%d stycken</b>." % (", ".join(sg(v) for v in vals), n), "")

    def text_():
        nm = K().name()
        k = ri(0, 2)
        if k == 0:
            p, b = ri(15, 60), ri(150, 600)
            x = b // p
            return MN("%s har %s och vill köpa biljetter som kostar %s styck. Hur många biljetter kan %s köpa som mest?" % (nm, kr(b), kr(p), nm), x, [x + 1, x - 1, F(b, p) if F(b, p).denominator == 1 and F(b, p) != x else x + 2], "%dx ≤ %d ger x ≤ %s. Största heltalet är <b>%d</b>." % (p, b, rd(F(b, p), 1), x), "biljetter")
        if k == 1:
            f, per = ri(100, 300), ri(20, 60)
            g = ri(500, 1500)
            x = (g - f) // per
            return MN("En hyrbil kostar %s plus %s per mil. Kostnaden får vara högst %s. Hur många mil kan man köra som mest?" % (kr(f), kr(per), kr(g)), x, [x + 1, g // per, x - 1] if g // per not in (x, x + 1, x - 1) else [x + 1, x - 1, x + 2], "%d + %dx ≤ %d ger x ≤ %s. Som mest <b>%d mil</b>." % (f, per, g, rd(F(g - f, per), 1), x), "mil")
        a, b = ri(60, 85), ri(3, 5)
        tot = ri(a * (b + 1) + 1, 100 * (b + 1) - 1) if a * (b + 1) + 1 < 100 * (b + 1) else None
        if not tot:
            return None
        nmin = tot - a * b
        if nmin > 100 or nmin < 0:
            return None
        return MN("På %d prov har %s fått %d poäng i snitt. Hur många poäng behövs minst på nästa prov för att snittet ska bli minst %s?" % (b, nm, a, rd(F(tot, b + 1), 1)), nmin, [nmin - 1, nmin + 5, tot // (b + 1)] if tot // (b + 1) not in (nmin, nmin - 1, nmin + 5) else [nmin - 1, nmin + 5, nmin + 2], "Summan ska bli minst %d. %d − %d · %d = <b>%d</b>." % (tot, tot, b, a, nmin), "poäng") if F(tot, b + 1).denominator in (1, 2, 5, 10) else None

    sets = [("Större än och mindre än", [(tecken, 20)]), ("Lös olikheter", [(los, 20)]), ("Dela med ett negativt tal", [(neg, 20)]),
            ("Heltalslösningar", [(heltal, 20)]), ("Olikheter i vardagen", [(text_, 20)])]
    return unit("olikheter", "A", "Olikheter: större än, mindre än och lösningar", "Olikheter",
                "Innebörden av variabelbegreppet och dess användning i algebraiska uttryck, formler, ekvationer och olikheter. Metoder för lösning av enkla olikheter.",
                "Arbetsblad om olikheter för årskurs 8: tecknen &lt;, &gt;, ≤ och ≥, lös olikheter, dela med ett negativt tal, heltalslösningar och vardagsproblem. 100 uppgifter med facit.",
                "Vänd tecknet vid division med minus", "Annars löser du olikheter som ekvationer.", sets,
                ["< betyder mindre än, > större än. ≤ betyder mindre än eller lika med och ≥ större än eller lika med.",
                 "Lös en olikhet som en ekvation: 3x + 2 < 14 ger 3x < 12 och x < 4. Lösningen är alla tal mindre än 4.",
                 "Multiplicerar eller dividerar du med ett negativt tal vänds tecknet: −2x < 6 ger x > −3."],
                [("3x + 2 < 14", ["3x < 12", "x < 4"], "x < 4"), ("−2x ≥ 8", ["Dela med −2 och vänd tecknet"], "x ≤ −4")],
                [["−2x < 6 ger x < −3", "Tecknet vänds: x > −3"], ["x < 4 betyder bara x = 3", "Alla tal mindre än 4, till exempel 3,9 och −10"], ["−5 > −2", "−5 ligger längre till vänster: −5 < −2"]],
                [("Hur kommer jag ihåg vilket tecken som är vilket?", "Den öppna sidan pekar mot det större talet: 3 < 5."),
                 ("Varför vänds tecknet?", "2 < 3, men −2 > −3. När du multiplicerar med −1 byter talen plats på tallinjen."), ("Hur skriver jag lösningen?", "Som en olikhet med x ensamt, till exempel x ≥ 2.")])


# ============================================================ kvadreringsreglerna
def kvadrering(lv):
    def plus():
        a = ri(1, 9)
        m = ri(1, 4)
        v = "x" if m == 1 else "%dx" % m
        if coin():
            q = "(%s + %d)²" % (v, a)
            r = expr([(m * m, "x²"), (2 * m * a, "x"), (a * a, "")])
            return M("Utveckla %s." % q, r, [expr([(m * m, "x²"), (a * a, "")]), expr([(m * m, "x²"), (m * a, "x"), (a * a, "")]), expr([(m, "x²"), (2 * m * a, "x"), (a * a, "")]) if m > 1 else expr([(1, "x²"), (2 * a, "x"), (2 * a, "")])], "(a + b)² = a² + 2ab + b²: <b>%s</b>." % r)
        q = "(%s − %d)²" % (v, a)
        r = expr([(m * m, "x²"), (-2 * m * a, "x"), (a * a, "")])
        return M("Utveckla %s." % q, r, [expr([(m * m, "x²"), (-a * a, "")]), expr([(m * m, "x²"), (-2 * m * a, "x"), (-a * a, "")]), expr([(m * m, "x²"), (2 * m * a, "x"), (a * a, "")])], "(a − b)² = a² − 2ab + b²: <b>%s</b>." % r)

    def konj():
        a = ri(1, 12)
        m = ri(1, 3)
        v = "x" if m == 1 else "%dx" % m
        r = expr([(m * m, "x²"), (-a * a, "")])
        return M("Förenkla (%s + %d)(%s − %d)." % (v, a, v, a), r, [expr([(m * m, "x²"), (a * a, "")]), expr([(m * m, "x²"), (-2 * m * a, "x"), (-a * a, "")]), expr([(m * m, "x²"), (-2 * a, "")])], "Konjugatregeln (a + b)(a − b) = a² − b²: <b>%s</b>." % r)

    def fakt():
        a = ri(1, 10)
        k = ri(0, 2)
        if k == 0:
            q = expr([(1, "x²"), (2 * a, "x"), (a * a, "")])
            return M("Faktorisera %s." % q, "(x + %d)²" % a, ["(x + %d)²" % (2 * a), "(x + %d)(x − %d)" % (a, a), "(x − %d)²" % a], "%s = x² + 2 · %d · x + %d²: <b>(x + %d)²</b>." % (q, a, a, a))
        if k == 1:
            q = expr([(1, "x²"), (-2 * a, "x"), (a * a, "")])
            return M("Faktorisera %s." % q, "(x − %d)²" % a, ["(x + %d)²" % a, "(x + %d)(x − %d)" % (a, a), "(x − %d)²" % (2 * a)], "%s = x² − 2 · %d · x + %d²: <b>(x − %d)²</b>." % (q, a, a, a))
        q = expr([(1, "x²"), (-a * a, "")])
        return M("Faktorisera %s." % q, "(x + %d)(x − %d)" % (a, a), ["(x − %d)²" % a, "(x + %d)²" % a, "(x − %d)(x − %d)" % (a * a, 1) if a > 1 else "x(x − 1)"], "Konjugatregeln baklänges: <b>(x + %d)(x − %d)</b>." % (a, a))

    def smart():
        k = ri(0, 2)
        b = ri(1, 4)
        a = ch([20, 30, 40, 50, 60, 70, 80, 90, 100])
        if k == 0:
            n = a + b
            return MN("Beräkna %d² med kvadreringsregeln." % n, n * n, [a * a + b * b, a * a + a * b + b * b, n * n + 10], "(%d + %d)² = %d + %d + %d = <b>%s</b>." % (a, b, a * a, 2 * a * b, b * b, num(n * n)))
        if k == 1:
            n = a - b
            return MN("Beräkna %d² med kvadreringsregeln." % n, n * n, [a * a - b * b, a * a - a * b + b * b, n * n - 10], "(%d − %d)² = %d − %d + %d = <b>%s</b>." % (a, b, a * a, 2 * a * b, b * b, num(n * n)))
        return MN("Beräkna %d · %d med konjugatregeln." % (a + b, a - b), a * a - b * b, [a * a + b * b, a * a - 2 * b, a * a], "(%d + %d)(%d − %d) = %d − %d = <b>%s</b>." % (a, b, a, b, a * a, b * b, num(a * a - b * b)))

    def ekv():
        a, b = ri(1, 8), ri(1, 8)
        if coin():
            c = ri(1, 9)
            # (x + a)² − x² = c  → 2ax + a² = c
            x = F(c - a * a, 2 * a)
            if x.denominator != 1:
                return None
            return M("Lös ekvationen (x + %d)² − x² = %d." % (a, c), "x = %s" % d(x), ["x = %s" % d(v) for v in (x + 1, -x if x else 1, F(c, 2 * a) if F(c, 2 * a) != x else x - 1, c - a)], "(x + %d)² − x² = %dx + %d. %dx + %d = %d ger <b>x = %s</b>." % (a, 2 * a, a * a, 2 * a, a * a, c, d(x)))
        x = nz(-6, 6)
        # (x + a)(x − a) = x² + b·x + c ... use (x+a)² = x² + k
        k = 2 * a * x + a * a
        return M("Lös ekvationen (x + %d)² = x² %s %d." % (a, "+" if k >= 0 else "−", abs(k)), "x = %s" % d(x), ["x = %s" % d(v) for v in (x + 1, -x, F(k, 2 * a), k - a * a)], "x² + %dx + %d = x² %s %d ger %dx = %s och <b>x = %s</b>." % (2 * a, a * a, "+" if k >= 0 else "−", abs(k), 2 * a, d(k - a * a), d(x)))

    sets = [("Första och andra kvadreringsregeln", [(plus, 20)]), ("Konjugatregeln", [(konj, 20)]), ("Faktorisera", [(fakt, 20)]),
            ("Räkna smart", [(smart, 20)]), ("Ekvationer och blandat", [(ekv, 12), (plus, 8)])]
    return unit("kvadreringsreglerna", "A", "Kvadreringsreglerna och konjugatregeln", "Kvadreringsreglerna",
                "Metoder för att förenkla algebraiska uttryck. Kvadreringsreglerna och konjugatregeln, att utveckla och faktorisera uttryck samt använda dem i ekvationer och huvudräkning.",
                "Arbetsblad om kvadreringsreglerna för årskurs 9: (a + b)², (a − b)², konjugatregeln, faktorisering, smart huvudräkning och ekvationer. 100 uppgifter med facit.",
                "(a + b)² = a² + 2ab + b²", "(a + b)(a − b) = a² − b²", sets,
                ["Första kvadreringsregeln: (a + b)² = a² + 2ab + b². Andra: (a − b)² = a² − 2ab + b².",
                 "Konjugatregeln: (a + b)(a − b) = a² − b². Mittermerna tar ut varandra.",
                 "Reglerna fungerar baklänges när du faktoriserar: x² + 6x + 9 = (x + 3)², x² − 25 = (x + 5)(x − 5)."],
                [("(x + 4)²", ["x² + 2 · 4 · x + 4²"], "x² + 8x + 16"), ("51²", ["(50 + 1)² = 2 500 + 100 + 1"], "2 601")],
                [["(x + 4)² = x² + 16", "Glöm inte dubbla produkten: x² + 8x + 16"], ["(x − 3)² = x² − 6x − 9", "Sista termen är alltid plus: + 9"], ["x² − 9 = (x − 3)²", "x² − 9 = (x + 3)(x − 3)"]],
                [("Varför heter det dubbla produkten?", "Mittermen 2ab är produkten a · b två gånger."), ("Hur vet jag vilken regel jag ska använda?", "Två lika parenteser i kvadrat: kvadreringsregel. Samma termer med + och −: konjugatregeln."),
                 ("Var används reglerna?", "När du förenklar uttryck, löser ekvationer och räknar smart i huvudet, till exempel 49 · 51.")])


# ============================================================ ekvationssystem
def ekvsystem(lv):
    def sys_(a, b, c, dd, e, f):
        def t(p, q, r):
            return "%s = %s" % (expr([(p, "x"), (q, "y")]), d(r))
        return "<span class='sys'>%s<br>%s</span>" % (t(a, b, c), t(dd, e, f))

    def gen():
        x, y = nz(-6, 8), nz(-6, 8)
        a, b, dd, e = nz(-5, 5), nz(-5, 5), nz(-5, 5), nz(-5, 5)
        if a * e - b * dd == 0:
            return None
        return x, y, a, b, a * x + b * y, dd, e, dd * x + e * y

    def ans(x, y):
        return "x = %s, y = %s" % (d(x), d(y))

    def wrong(x, y):
        return [ans(y, x), ans(x, -y), ans(-x, y), ans(x + 1, y - 1)]

    def subst():
        x, y = nz(-6, 8), nz(-6, 8)
        k, m = nz(-4, 5), nz(-9, 9)
        if y != k * x + m:
            y = k * x + m
        a, b = nz(-4, 5), nz(-4, 5)
        c = a * x + b * y
        q = "<span class='sys'>y = %s<br>%s = %s</span>" % (expr([(k, "x"), (m, "")]), expr([(a, "x"), (b, "y")]), d(c))
        if a + b * k == 0:
            return None
        return M("Lös ekvationssystemet med substitutionsmetoden:<br>%s" % q, ans(x, y), wrong(x, y), "Sätt in y = %s i den andra: %s = %s ger x = %s. Då är y = %s. <b>%s</b>." % (expr([(k, "x"), (m, "")]), expr([(a + b * k, "x"), (b * m, "")]), d(c), d(x), d(y), ans(x, y)))

    def addm():
        x, y = nz(-6, 8), nz(-6, 8)
        a, b, e = nz(-5, 5), ri(1, 5), nz(-5, 5)
        dd = -a if coin() else a
        if dd == a:
            e = -b if e == b else e
        q = sys_(a, b, a * x + b * y, dd, e if dd != a else -b, dd * x + (e if dd != a else -b) * y)
        ee = e if dd != a else -b
        if a * ee - b * dd == 0:
            return None
        return M("Lös ekvationssystemet med additionsmetoden:<br>%s" % q, ans(x, y), wrong(x, y), "%s ekvationerna så att en variabel försvinner. Det ger <b>%s</b>." % ("Addera" if dd == -a else "Subtrahera", ans(x, y)))

    def kontroll():
        g = gen()
        if not g:
            return None
        x, y, a, b, c, dd, e, f = g
        return M("Vilket talpar är en lösning till ekvationssystemet?<br>%s" % sys_(a, b, c, dd, e, f), ans(x, y), wrong(x, y), "Sätt in talparen i båda ekvationerna. Bara x = %s och y = %s stämmer i båda: <b>%s</b>." % (d(x), d(y), ans(x, y)))

    def grafisk():
        k1, m1 = nz(-2, 2), nz(-3, 3)
        k2 = nz(-2, 2)
        if k1 == k2:
            return None
        x = nz(-3, 3)
        y = k1 * x + m1
        m2 = y - k2 * x
        if not (-5 <= y <= 5 and -5 <= m2 <= 5):
            return None
        fig = kosy([(k1, m1, BLUE, ""), (k2, m2, RED, "")], (), -5, 5, 22, "två räta linjer som skär varandra")
        return M("Linjerna %s och %s är ritade. Vilken är lösningen till ekvationssystemet?<div class='qfig'>%s</div>" % (lin(k1, m1), lin(k2, m2), fig), ans(x, y), wrong(x, y), "Lösningen är skärningspunkten (%s, %s): <b>%s</b>." % (d(x), d(y), ans(x, y)))

    def text_():
        k = ri(0, 3)
        if k == 0:
            v, b = ri(15, 45), ri(10, 35)
            n1, n2, m1, m2 = ri(2, 5), ri(2, 4), ri(2, 4), ri(2, 5)
            if n1 * m2 == n2 * m1:
                return None
            return M("%d vuxenbiljetter och %d barnbiljetter kostar %s. %d vuxenbiljetter och %d barnbiljetter kostar %s. Vad kostar en vuxenbiljett?" % (n1, n2, kr(n1 * v * 5 + n2 * b * 5), m1, m2, kr(m1 * v * 5 + m2 * b * 5)), kr(v * 5), [kr(b * 5), kr(v * 5 + 10), kr((n1 * v * 5 + n2 * b * 5) // (n1 + n2))],
                     "Ställ upp %dx + %dy = %d och %dx + %dy = %d. Lösningen är x = %d och y = %d: <b>%s</b>." % (n1, n2, n1 * v * 5 + n2 * b * 5, m1, m2, m1 * v * 5 + m2 * b * 5, v * 5, b * 5, kr(v * 5)))
        if k == 1:
            a, b = ri(10, 60), ri(5, 40)
            return M("Summan av två tal är %d och skillnaden är %d. Vilket är det största talet?" % (a + b + b, a), str(a + b), [str(b), str((a + 2 * b) // 2), str(a)], "x + y = %d och x − y = %d. Addera: 2x = %d, <b>x = %d</b>." % (a + 2 * b, a, 2 * (a + b), a + b)) if (a + 2 * b) // 2 != a + b else None
        if k == 2:
            h, c = ri(5, 20), ri(5, 20)
            return M("På en gård finns höns och kor, totalt %d djur med %d ben. Hur många kor finns det?" % (h + c, 2 * h + 4 * c), "%d kor" % c, ["%d kor" % h, "%d kor" % ((2 * h + 4 * c) // 4), "%d kor" % (c + 2)] if h != c and (2 * h + 4 * c) // 4 not in (h, c, c + 2) else ["%d kor" % (c + 1), "%d kor" % (c + 2), "%d kor" % (c - 1)],
                     "h + k = %d och 2h + 4k = %d. Det ger <b>k = %d</b>." % (h + c, 2 * h + 4 * c, c))
        a, b = ri(8, 25), ri(3, 9)
        n1, n2 = ri(2, 6), ri(2, 6)
        return M("%d äpplen och %d päron kostar %s. Ett päron kostar %s mer än ett äpple. Vad kostar ett äpple?" % (n1, n2, kr(n1 * a + n2 * (a + b)), kr(b)), kr(a), [kr(a + b), kr((n1 * a + n2 * (a + b)) // (n1 + n2)), kr(a - 1)] if (n1 * a + n2 * (a + b)) // (n1 + n2) not in (a, a + b, a - 1) else [kr(a + b), kr(a + 2), kr(a - 1)],
                 "y = x + %d. %dx + %d(x + %d) = %d ger %dx = %d och <b>x = %d kr</b>." % (b, n1, n2, b, n1 * a + n2 * (a + b), n1 + n2, (n1 + n2) * a, a))

    from se_h import lin
    sets = [("Substitutionsmetoden", [(subst, 20)]), ("Additionsmetoden", [(addm, 20)]), ("Kontrollera lösningen", [(kontroll, 20)]),
            ("Grafisk lösning", [(grafisk, 20)]), ("Ekvationssystem i vardagen", [(text_, 20)])]
    return unit("ekvationssystem", "A", "Ekvationssystem: substitution, addition och grafisk lösning", "Ekvationssystem",
                "Metoder för ekvationslösning. Linjära ekvationssystem med två obekanta och hur de kan lösas algebraiskt och grafiskt samt användas för att lösa problem.",
                "Arbetsblad om ekvationssystem för årskurs 9: substitutionsmetoden, additionsmetoden, kontrollera lösningen, grafisk lösning och problem i vardagen. 100 uppgifter med facit.",
                "Två ekvationer, två obekanta", "Lösningen är punkten där linjerna skär varandra.", sets,
                ["Ett ekvationssystem är två ekvationer som ska gälla samtidigt. Lösningen är ett talpar (x, y).",
                 "Substitutionsmetoden: lös ut en variabel ur den ena ekvationen och sätt in i den andra.",
                 "Additionsmetoden: addera eller subtrahera ekvationerna så att en variabel försvinner. Grafiskt är lösningen skärningspunkten mellan två linjer."],
                [("y = 2x + 1 och 3x + y = 11", ["3x + 2x + 1 = 11", "5x = 10, x = 2", "y = 2 · 2 + 1 = 5"], "x = 2, y = 5"), ("x + y = 10 och x − y = 4", ["Addera: 2x = 14", "x = 7, y = 3"], "x = 7, y = 3")],
                [["Bestämmer bara x", "Sätt in x för att få y också"], ["Byter plats på x och y", "Kontrollera i båda ekvationerna"], ["Lösningen är där en linje skär y-axeln", "Lösningen är där linjerna skär varandra"]],
                [("Kan ett ekvationssystem sakna lösning?", "Ja, om linjerna är parallella skär de aldrig varandra."), ("Vilken metod är bäst?", "Substitution när en variabel redan står ensam, annars ofta addition."),
                 ("Hur kontrollerar jag svaret?", "Sätt in x och y i båda ekvationerna. Båda ska stämma.")])


# ============================================================ ekvationer med x²
def x2(lv):
    def ren():
        a = ri(1, 15)
        k = ri(0, 2)
        if k == 0:
            return M("Lös ekvationen x² = %d." % (a * a), "x = ±%d" % a, ["x = %d" % a, "x = ±%d" % (a * a // 2) if a > 1 else "x = ±2", "x = %d" % (2 * a)], "Både %d² och (−%d)² är %d: <b>x = ±%d</b>." % (a, a, a * a, a))
        if k == 1:
            m = ri(2, 5)
            return M("Lös ekvationen %dx² = %d." % (m, m * a * a), "x = ±%d" % a, ["x = ±%d" % (m * a), "x = %d" % a, "x = ±%d" % (a * a)], "Dela med %d: x² = %d. <b>x = ±%d</b>." % (m, a * a, a))
        c = ri(1, 30)
        return M("Lös ekvationen x² + %d = %d." % (c, a * a + c), "x = ±%d" % a, ["x = ±%d" % (a + 1), "x = %d" % a, "x = ±%s" % rd((a * a + 2 * c) ** 0.5, 1)], "x² = %d ger <b>x = ±%d</b>." % (a * a, a))

    def ungef():
        n = ri(2, 99)
        if int(n ** 0.5) ** 2 == n:
            return None
        v = n ** 0.5
        return M("Lös ekvationen x² = %d. Svara med en decimal." % n, "x ≈ ±%s" % rd(v, 1), ["x ≈ ±%s" % rd(v + 0.1, 1), "x ≈ %s" % rd(v, 1), "x ≈ ±%s" % rd(F(n, 2), 1)], "x = ±√%d ≈ <b>±%s</b>." % (n, rd(v, 1)))

    def noll():
        a, b = nz(-9, 9), nz(-9, 9)
        if a == b:
            return None
        if coin():
            return M("Lös ekvationen x(x %s %d) = 0." % ("+" if a > 0 else "−", abs(a)), "x₁ = 0, x₂ = %s" % d(-a), ["x₁ = 0, x₂ = %s" % d(a), "x = %s" % d(-a), "x₁ = 1, x₂ = %s" % d(-a)], "En produkt är noll om någon faktor är noll: x = 0 eller x %s %d = 0. <b>x₁ = 0, x₂ = %s</b>." % ("+" if a > 0 else "−", abs(a), d(-a)))
        lo, hi = sorted([-a, -b])
        return M("Lös ekvationen (x %s %d)(x %s %d) = 0." % ("+" if a > 0 else "−", abs(a), "+" if b > 0 else "−", abs(b)), "x₁ = %s, x₂ = %s" % (d(lo), d(hi)), ["x₁ = %s, x₂ = %s" % tuple(map(d, sorted([a, b]))), "x₁ = %s, x₂ = %s" % tuple(map(d, sorted([-a, b]))) if a != -b else "x = %s" % d(a * b), "x = %s" % d(a * b)],
                 "Någon parentes måste vara noll: <b>x₁ = %s, x₂ = %s</b>." % (d(lo), d(hi)))

    def faktor():
        a = ri(1, 9)
        m = ri(1, 9)
        k = ri(0, 1)
        if k == 0:
            return M("Lös ekvationen x² − %dx = 0." % a, "x₁ = 0, x₂ = %d" % a, ["x = %d" % a, "x₁ = 0, x₂ = −%d" % a, "x = ±%d" % a], "Bryt ut x: x(x − %d) = 0. <b>x₁ = 0, x₂ = %d</b>." % (a, a))
        return M("Lös ekvationen x² + %dx = 0." % m, "x₁ = −%d, x₂ = 0" % m, ["x = −%d" % m, "x₁ = 0, x₂ = %d" % m, "x = ±%d" % m], "Bryt ut x: x(x + %d) = 0. <b>x₁ = −%d, x₂ = 0</b>." % (m, m))

    def text_():
        k = ri(0, 3)
        a = ri(3, 20)
        if k == 0:
            return M("En kvadratisk gräsmatta har arean %d m². Hur lång är en sida?" % (a * a), "%d m" % a, ["%d m" % (a * a // 4), "%d m" % (2 * a), "%d m" % (a + 1)], "x² = %d ger x = %d. En längd kan inte vara negativ: <b>%d m</b>." % (a * a, a, a))
        if k == 1:
            return M("Ett tal multiplicerat med sig självt blir %d. Vilket tal kan det vara?" % (a * a), "%d eller −%d" % (a, a), ["bara %d" % a, "%d eller −%d" % (a * a // 2, a * a // 2) if a > 1 else "2 eller −2", "%d" % (2 * a)], "x² = %d ger <b>x = ±%d</b>." % (a * a, a))
        if k == 2:
            b = ri(2, 6)
            return M("En rektangel är %d gånger så lång som den är bred. Arean är %d cm². Hur bred är den?" % (b, b * a * a), "%d cm" % a, ["%d cm" % (b * a), "%d cm" % (a * a), "%d cm" % (a + b)], "%dx² = %d ger x² = %d och <b>x = %d cm</b>." % (b, b * a * a, a * a, a))
        t = ri(2, 6)
        return M("En sten släpps från en höjd av %d m. Höjden efter t sekunder är h = %d − 5t². Efter hur många sekunder når stenen marken?" % (5 * t * t, 5 * t * t), "%d s" % t, ["%d s" % (t * t), "%d s" % (5 * t), "%d s" % (t + 1)], "0 = %d − 5t² ger t² = %d och <b>t = %d s</b>." % (5 * t * t, t * t, t))

    sets = [("Ekvationer av typen x² = a", [(ren, 20)]), ("Ungefärliga lösningar", [(ungef, 20)]), ("Nollproduktmetoden", [(noll, 20)]),
            ("Bryt ut x", [(faktor, 12), (noll, 8)]), ("Ekvationer med x² i vardagen", [(text_, 20)])]
    return unit("ekvationer-med-x2", "A", "Ekvationer med x²: kvadratrötter och nollprodukt", "Ekvationer med x²",
                "Metoder för ekvationslösning. Enkla andragradsekvationer som löses med kvadratrötter eller genom faktorisering och nollproduktmetoden.",
                "Arbetsblad om ekvationer med x² för årskurs 9: x² = a, ungefärliga lösningar, nollproduktmetoden, bryt ut x och problem med area. 100 uppgifter med facit.",
                "x² = 25 ger x = ±5", "En produkt är noll om någon faktor är noll.", sets,
                ["x² = 25 har två lösningar: x = 5 och x = −5, eftersom båda i kvadrat blir 25. Man skriver x = ±5.",
                 "Om talet inte är en kvadrat får du en ungefärlig lösning: x² = 20 ger x = ±√20 ≈ ±4,5.",
                 "Nollproduktmetoden: om (x − 3)(x + 2) = 0 måste x − 3 = 0 eller x + 2 = 0, alltså x = 3 eller x = −2."],
                [("x² + 7 = 56", ["x² = 49", "x = ±7"], "x = ±7"), ("x² − 6x = 0", ["x(x − 6) = 0", "x = 0 eller x = 6"], "x₁ = 0, x₂ = 6")],
                [["x² = 25 ger x = 5", "Glöm inte den negativa lösningen: x = ±5"], ["x² − 6x = 0 ger x = 6", "x = 0 är också en lösning"], ["En sida kan vara −7 m", "En längd är positiv, välj den positiva lösningen"]],
                [("Har alla ekvationer med x² två lösningar?", "Nej. x² = 0 har en lösning och x² = −4 saknar reella lösningar."),
                 ("Får jag dela med x?", "Nej, då försvinner lösningen x = 0. Bryt ut x i stället."), ("Vad betyder x₁ och x₂?", "De två lösningarna. Indexen 1 och 2 skiljer dem åt.")])


UNITS = {"algebraiska-uttryck": uttryck, "ekvationer": ekvationer, "monster-och-formler": monster, "parenteser-och-faktorisering": parenteser,
         "formler": formler, "olikheter": olikheter, "kvadreringsreglerna": kvadrering, "ekvationssystem": ekvsystem, "ekvationer-med-x2": x2}
