# -*- coding: utf-8 -*-
"""Sverige årskurs 7–9: sannolikhet och statistik（lägesmått, spridningsmått, diagram, sannolikhet, kombinatorik）och problemlösning"""
import math
import re
from fractions import Fraction as F
from se_h import (gen, MQ, lista, ri, ch, sh, cap, fr, fq, d, par, sg, M, MN, rd, sup, unit, tab, K, num, kr, NB, MIN, coin, expr,
                  wrap, text, line, fig, INK, GREEN, FILL, RED, BLUE)
from se_common import stapel
import tr_g


def rl(svg, label):
    return re.sub(r"aria-label='[^']*'", "aria-label='%s'" % label, svg, count=1)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def typv(xs):
    c = {}
    for x in xs:
        c[x] = c.get(x, 0) + 1
    m = max(c.values())
    t = [x for x, v in c.items() if v == m]
    return t[0] if len(t) == 1 and m > 1 else None


def dat(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def L(xs):
    return lista(d(x) for x in xs)


# ============================================================ lägesmått (åk 7)
def lagesmatt(lv):
    def medel():
        xs = dat(ri(4, 8), 2, 30)
        m = F(sum(xs), len(xs))
        if (m * 10).denominator != 1:
            return None
        return MN("Beräkna medelvärdet av %s." % L(xs), m, [median(xs), F(sum(xs), len(xs) + 1), max(xs) - min(xs)], "Summan är %d och antalet %d: %d/%d = <b>%s</b>." % (sum(xs), len(xs), sum(xs), len(xs), d(m)))

    def med():
        xs = dat(ri(5, 9), 1, 40)
        m = median(xs)
        if (m * 10).denominator != 1:
            return None
        return MN("Bestäm medianen av %s." % L(xs), m, [F(xs[len(xs) // 2]) if F(xs[len(xs) // 2]) != m else m + 1, F(sum(xs), len(xs)) if (F(sum(xs), len(xs)) * 10).denominator == 1 else m - 1, max(xs) - min(xs)], "Ordna talen: %s. Medianen är talet i mitten: <b>%s</b>." % (L(sorted(xs)), d(m)))

    def typ_():
        xs = dat(ri(6, 10), 1, 12)
        t = typv(xs)
        if t is None:
            return None
        return MN("Bestäm typvärdet av %s." % L(xs), t, [median(xs), max(xs), min(xs) if min(xs) != t else t + 1], "Det tal som finns flest gånger är <b>%d</b>." % t)

    def bredd():
        xs = dat(ri(5, 9), -10 if coin() else 0, 40)
        v = max(xs) - min(xs)
        return MN("Vad är variationsbredden för %s?" % L(xs), v, [max(xs), max(xs) + min(xs), median(xs)], "Största minus minsta: %s − %s = <b>%s</b>." % (d(max(xs)), par(min(xs)), d(v)))

    def text_():
        k = ri(0, 3)
        nm = K().name()
        if k == 0:
            xs = dat(ri(3, 5), 10, 25)
            m = ri(15, 22)
            n = len(xs) + 1
            nxt = m * n - sum(xs)
            if not 0 <= nxt <= 30:
                return None
            return MN("%s har fått poängen %s på prov. Vilken poäng behövs på nästa prov för att medelvärdet ska bli %d?" % (nm, L(xs), m), nxt, [m, m * n, nxt + 1], "Summan ska bli %d · %d = %d. %d − %d = <b>%d</b>." % (m, n, m * n, m * n, sum(xs), nxt), "poäng")
        if k == 1:
            xs = sorted(dat(6, 120, 300))
            return MN("Sex hus såldes för %s tusen kronor. Vilket lägesmått ger %s tusen kr?" % (L(xs), d(median(xs))), median(xs), [F(sum(xs), 6), xs[0], xs[-1]], "Det är talet mitt emellan de två mittersta: medianen <b>%s</b>." % d(median(xs))) if False else None
        if k == 2:
            xs = dat(ri(4, 7), 140, 190)
            m = F(sum(xs), len(xs))
            return M("Längderna i ett lag är %s cm. Vad är medellängden? Avrunda till heltal." % L(xs), rd(m, 0) + NB + "cm", [d(median(xs)) + NB + "cm" if d(median(xs)) != rd(m, 0) else rd(m + 2, 0) + NB + "cm", rd(m + 1, 0) + NB + "cm", d(max(xs) - min(xs)) + NB + "cm"], "%d/%d ≈ <b>%s cm</b>." % (sum(xs), len(xs), rd(m, 0)))
        lo = ri(1, 5)
        xs = [ri(20, 30) for _ in range(5)] + [ri(80, 150)]
        sh(xs)
        return M("Lönerna i ett litet företag är %s tusen kr. Vilket lägesmått beskriver en typisk lön bäst?" % L(xs), "Medianen, eftersom den höga lönen drar upp medelvärdet", ["Medelvärdet, eftersom det tar med alla", "Variationsbredden", "Den högsta lönen"], "En mycket hög lön påverkar medelvärdet mycket men medianen lite. <b>Medianen</b> är bäst.")

    sets = [("Medelvärde", [(medel, 20)]), ("Median", [(med, 20)]), ("Typvärde", [(typ_, 20)]), ("Variationsbredd", [(bredd, 20)]), ("Lägesmått i vardagen", [(text_, 14), (medel, 6)])]
    return unit("lagesmatt", "S", "Lägesmått: medelvärde, median, typvärde och variationsbredd", "Lägesmått",
                "Lägesmått och spridningsmått och hur de kan användas för att beskriva och jämföra data. Medelvärde, median, typvärde och variationsbredd.",
                "Arbetsblad om lägesmått för årskurs 7: medelvärde, median, typvärde, variationsbredd och vilket mått som passar bäst. 100 uppgifter med facit.",
                "Medianen är talet i mitten", "Ordna talen först.", sets,
                ["Medelvärdet får du genom att lägga ihop alla värden och dela med antalet.",
                 "Medianen är det mittersta värdet när talen står i storleksordning. Finns det två i mitten tar du medelvärdet av dem.",
                 "Typvärdet är det vanligaste värdet. Variationsbredden är största värdet minus minsta och visar spridningen."],
                [("Medelvärdet av 4, 7, 7, 10", ["4 + 7 + 7 + 10 = 28", "28/4"], "7"), ("Medianen av 3, 9, 4, 8", ["Ordna: 3, 4, 8, 9", "(4 + 8)/2"], "6")],
                [["Medianen utan att ordna", "Ordna talen först"], ["Delar med fel antal", "Dela med hur många värden det finns"], ["Variationsbredden är det största värdet", "Största minus minsta"]],
                [("När är medianen bättre än medelvärdet?", "När det finns något enstaka värde som är mycket större eller mindre än de andra."),
                 ("Kan det finnas flera typvärden?", "Ja, om flera värden är lika vanliga. Ibland finns inget typvärde."), ("Vad visar variationsbredden?", "Hur utspridda värdena är.")])


# ============================================================ spridningsmått (åk 9)
def kvart(xs):
    s = sorted(xs)
    n = len(s)
    lo, hi = s[:n // 2], s[(n + 1) // 2:]
    return median(lo), median(s), median(hi)


def ladagram(mn, q1, md, q3, mx, lo=0, hi=50, step=5):
    W = 440
    X = lambda v: 30 + (float(v) - lo) / (hi - lo) * (W - 60)
    y = 60
    s = [line(X(lo), 110, X(hi), 110, INK, 1.6)]
    v = lo
    while v <= hi:
        s.append(line(X(v), 106, X(v), 114, INK, 1.4) + text(X(v), 130, d(v), 12, weight=400))
        v += step
    s.append(line(X(mn), y, X(q1), y, INK, 2) + line(X(q3), y, X(mx), y, INK, 2))
    s.append(line(X(mn), y - 12, X(mn), y + 12, INK, 2) + line(X(mx), y - 12, X(mx), y + 12, INK, 2))
    s.append("<rect x='%.1f' y='%d' width='%.1f' height='40' fill='%s' stroke='%s' stroke-width='2'/>" % (X(q1), y - 20, X(q3) - X(q1), FILL, GREEN))
    s.append(line(X(md), y - 20, X(md), y + 20, RED, 2.6))
    return fig(wrap(W, 140, "".join(s), "lådagram", lg=True))


def spridning(lv):
    def kvartil():
        n = ch([7, 8, 9, 10, 11])
        xs = dat(n, 1, 40)
        q1, m, q3 = kvart(xs)
        if (q1 * 2).denominator != 1 or (q3 * 2).denominator != 1:
            return None
        k = ri(0, 2)
        if k == 0:
            return MN("Bestäm nedre kvartilen för %s." % L(xs), q1, [m, q3, min(xs)], "Ordna: %s. Nedre kvartilen är medianen av den nedre halvan: <b>%s</b>." % (L(sorted(xs)), d(q1)))
        if k == 1:
            return MN("Bestäm övre kvartilen för %s." % L(xs), q3, [m, q1, max(xs)], "Ordna: %s. Övre kvartilen är medianen av den övre halvan: <b>%s</b>." % (L(sorted(xs)), d(q3)))
        return MN("Bestäm kvartilavståndet för %s." % L(xs), q3 - q1, [max(xs) - min(xs), q3, m], "Kvartilerna är %s och %s. %s − %s = <b>%s</b>." % (d(q1), d(q3), d(q3), d(q1), d(q3 - q1)))

    def lada():
        mn = ri(0, 10)
        q1 = mn + ri(2, 8)
        md = q1 + ri(2, 8)
        q3 = md + ri(2, 8)
        mx = min(q3 + ri(2, 10), 50)
        pic = ladagram(mn, q1, md, q3, mx)
        k = ri(0, 3)
        if k == 0:
            return MN("Lådagrammet visar resultat på ett prov. Vad är medianen?" + pic, md, [q1, q3, F(mn + mx, 2) if F(mn + mx, 2) != md else mx], "Medianen är det röda strecket i lådan: <b>%d</b>." % md)
        if k == 1:
            return MN("Lådagrammet visar resultat på ett prov. Vad är kvartilavståndet?" + pic, q3 - q1, [mx - mn, q3, md - q1], "Lådans bredd: %d − %d = <b>%d</b>." % (q3, q1, q3 - q1))
        if k == 2:
            return MN("Lådagrammet visar resultat på ett prov. Vad är variationsbredden?" + pic, mx - mn, [q3 - q1, mx, md], "Från minsta till största värdet: %d − %d = <b>%d</b>." % (mx, mn, mx - mn))
        return M("Lådagrammet visar resultat på ett prov. Hur stor andel av eleverna fick minst %d poäng?" % q3 + pic, "25 %", ["75 %", "50 %", "%d %%" % q3], "Övre kvartilen är %d. Över den finns en fjärdedel: <b>25 %%</b>." % q3)

    def jamfor():
        a = [ri(15, 25) for _ in range(6)]
        b = [ri(5, 35) for _ in range(6)]
        ra, rb = max(a) - min(a), max(b) - min(b)
        if ra == rb:
            return None
        nm1, nm2 = K().two()
        return M("%s fick %s poäng och %s fick %s poäng i sex matcher. Vem hade jämnast resultat?" % (nm1, L(a), nm2, L(b)), nm1 if ra < rb else nm2, [nm2 if ra < rb else nm1, "De var lika jämna", "Det går inte att avgöra"], "Variationsbredden är %d för %s och %d för %s. Minst spridning: <b>%s</b>." % (ra, nm1, rb, nm2, nm1 if ra < rb else nm2))

    def frekvens():
        vals = sorted(set(ri(0, 6) for _ in range(6)))
        if len(vals) < 4:
            return None
        f = [ri(1, 8) for _ in vals]
        n = sum(f)
        t = tab(["Antal syskon"] + [str(v) for v in vals], [["Frekvens"] + [str(x) for x in f]])
        k = ri(0, 1)
        m = F(sum(v * x for v, x in zip(vals, f)), n)
        if k == 0:
            return M("Tabellen visar hur många syskon eleverna i en klass har. Vad är medelvärdet? Avrunda till en decimal.%s" % t, rd(m, 1), [rd(F(sum(vals), len(vals)), 1), rd(F(n, len(vals)), 1), rd(m + F(1, 2), 1)], "Summan är %d och antalet elever %d: %d/%d ≈ <b>%s</b>." % (sum(v * x for v, x in zip(vals, f)), n, sum(v * x for v, x in zip(vals, f)), n, rd(m, 1)))
        allv = sorted(v for v, x in zip(vals, f) for _ in range(x))
        md = median(allv)
        return MN("Tabellen visar hur många syskon eleverna i en klass har. Vad är medianen?%s" % t, md, [vals[len(vals) // 2] if vals[len(vals) // 2] != md else md + 1, max(f), F(n, 2)], "Det finns %d elever. Den mittersta har <b>%s</b> syskon." % (n, d(md)))

    sets = [("Kvartiler", [(kvartil, 20)]), ("Lådagram", [(lada, 20)]), ("Jämför spridning", [(jamfor, 20)]), ("Frekvenstabeller", [(frekvens, 20)]), ("Blandat", [(kvartil, 7), (lada, 7), (frekvens, 6)])]
    return unit("spridningsmatt", "S", "Spridningsmått: kvartiler, lådagram och variationsbredd", "Spridningsmått",
                "Lägesmått och spridningsmått och hur de kan användas för att beskriva och jämföra data. Kvartiler, kvartilavstånd, lådagram och frekvenstabeller.",
                "Arbetsblad om spridningsmått för årskurs 9: kvartiler, kvartilavstånd, lådagram, jämför spridning och frekvenstabeller. 100 uppgifter med facit.",
                "Kvartilavstånd = övre − nedre kvartil", "Hälften av värdena ligger i lådan.", sets,
                ["Spridningsmått visar hur utspridda värdena är. Variationsbredden är största minus minsta värdet.",
                 "Dela de ordnade värdena i en nedre och en övre halva. Medianen av den nedre halvan är nedre kvartilen och av den övre halvan övre kvartilen.",
                 "Ett lådagram visar minsta värde, nedre kvartil, median, övre kvartil och största värde. Lådan innehåller den mittersta hälften av värdena."],
                [("Kvartiler för 2, 4, 5, 7, 8, 10, 12, 15", ["Nedre halvan 2, 4, 5, 7: (4 + 5)/2 = 4,5", "Övre halvan 8, 10, 12, 15: (10 + 12)/2 = 11"], "4,5 och 11")],
                [["Kvartiler utan att ordna", "Ordna talen först"], ["Kvartilavstånd = största − minsta", "Det är variationsbredden. Kvartilavstånd = övre − nedre kvartil"], ["Hela lådan är 75 %", "Lådan är 50 % av värdena"]],
                [("Varför använda kvartilavstånd?", "Det påverkas inte av enstaka extrema värden, som variationsbredden gör."),
                 ("Vad visar ett lådagram?", "Hur värdena är fördelade: var mitten är och hur utspridda de är."), ("Ingår medianen i halvorna?", "Med ett udda antal värden räknas medianen inte med i någon halva.")])


# ============================================================ tabeller och diagram (åk 8)
def diagram(lv):
    CAT = [("buss", "cykel", "bil", "gång"), ("fotboll", "simning", "dans", "ridning"), ("äpple", "banan", "päron", "apelsin"), ("rock", "pop", "hiphop", "jazz")]

    def stap():
        cats = ch(CAT)
        vals = [ri(1, 12) for _ in cats]
        pic = stapel(list(zip(cats, vals)), "antal elever")
        k = ri(0, 2)
        tot = sum(vals)
        i = ri(0, 3)
        if k == 0:
            return MN("Diagrammet visar svaren från en klass. Hur många svarade totalt?" + pic, tot, [max(vals), tot - vals[0], tot + 2], "%s = <b>%d</b>." % (" + ".join(str(v) for v in vals), tot))
        if k == 1:
            p = F(vals[i] * 100, tot)
            return M("Diagrammet visar svaren från en klass. Hur många procent valde %s? Avrunda till heltal." % cats[i] + pic, rd(p, 0) + NB + "%", [str(vals[i]) + NB + "%", rd(F(100, 4), 0) + NB + "%" if rd(p, 0) != "25" else "20" + NB + "%", rd(p + 10, 0) + NB + "%"], "%d/%d ≈ <b>%s %%</b>." % (vals[i], tot, rd(p, 0)))
        j = (i + 1) % 4
        if vals[i] == vals[j]:
            return None
        return MN("Diagrammet visar svaren från en klass. Hur många fler valde %s än %s?" % ((cats[i], cats[j]) if vals[i] > vals[j] else (cats[j], cats[i])) + pic, abs(vals[i] - vals[j]), [vals[i] + vals[j], max(vals[i], vals[j]), abs(vals[i] - vals[j]) + 1], "%d − %d = <b>%d</b>." % (max(vals[i], vals[j]), min(vals[i], vals[j]), abs(vals[i] - vals[j])))

    def relativ():
        cats = ch(CAT)
        n = ch([20, 25, 40, 50])
        a = [ri(1, n // 3) for _ in range(3)]
        a.append(n - sum(a))
        if a[3] <= 0:
            return None
        t = tab(["Svar"] + list(cats), [["Frekvens"] + [str(x) for x in a]])
        i = ri(0, 3)
        p = F(a[i] * 100, n)
        return M("Vad är den relativa frekvensen för %s i procent?%s" % (cats[i], t), d(p) + NB + "%", [str(a[i]) + NB + "%", d(F(a[i] * 100, n + 10)) + NB + "%" if (F(a[i] * 100, n + 10) * 10).denominator == 1 else d(p + 5) + NB + "%", d(100 - p) + NB + "%"], "%d av %d: %d/%d = %s = <b>%s %%</b>." % (a[i], n, a[i], n, d(F(a[i], n)), d(p)))

    def cirkel():
        cats = ch(CAT)
        ps = ch([(50, 25, 15, 10), (40, 30, 20, 10), (25, 25, 25, 25), (45, 30, 15, 10), (35, 35, 20, 10), (60, 20, 10, 10), (30, 30, 30, 10), (40, 25, 25, 10)])
        ps = sh(list(ps))
        pic = fig(rl(tr_g.pie_chart(["%s %d %%" % (c, p) for c, p in zip(cats, ps)], ps), "cirkeldiagram"))
        i = ri(0, 3)
        n = ch([20, 40, 60, 80, 120, 200, 300, 400])
        k = ri(0, 1)
        if k == 0:
            v = F(ps[i] * 360, 100)
            return MN("Hur stor är medelpunktsvinkeln för %s i cirkeldiagrammet?" % cats[i] + pic, v, [ps[i], 360 - v, v / 2], "%d %% av 360° = %s · 360° = <b>%s°</b>." % (ps[i], d(F(ps[i], 100)), d(v)), "°")
        v = F(ps[i] * n, 100)
        return MN("Cirkeldiagrammet visar svaren från %d personer. Hur många svarade %s?" % (n, cats[i]) + pic, v, [ps[i], n - v, v * 2], "%d %% av %d = <b>%s</b>." % (ps[i], n, d(v)), "personer") if v.denominator == 1 else None

    def linje():
        m = ["apr", "maj", "jun", "jul", "aug", "sep"]
        vals = [ri(a, b) for a, b in ((2, 10), (7, 15), (11, 20), (14, 25), (13, 23), (8, 16))]

        def f(x):
            i = int(x) - 1
            if i >= 5:
                return vals[5]
            if i < 0:
                return None
            return vals[i] + (vals[i + 1] - vals[i]) * (x - 1 - i)
        import de_k10
        pic = fig(rl(de_k10.kurve([(f, BLUE, "")], (0, 6, 1), (0, 30, 5), [(i + 1, v, "") for i, v in enumerate(vals)], 340, 250, "linjediagram", xlab=lambda x: m[int(round(x)) - 1] if 1 <= x <= 6 else ""), "linjediagram över temperatur"))
        k = ri(0, 1)
        if k == 0:
            i = ri(0, 4)
            dd = vals[i + 1] - vals[i]
            if not dd:
                return None
            return MN("Linjediagrammet visar medeltemperaturen. Hur mycket ändrades temperaturen från %s till %s?" % (m[i], m[i + 1]) + pic, dd, [-dd if dd else 1, vals[i + 1], vals[i]], "%s − %s = <b>%s grader</b>." % (sg(vals[i + 1]), par(vals[i]), d(dd)), "grader") if dd else None
        return MN("Linjediagrammet visar medeltemperaturen. Vad är skillnaden mellan högsta och lägsta temperaturen?" + pic, max(vals) - min(vals), [max(vals), max(vals) + min(vals), max(vals) - min(vals) - 2], "%s − %s = <b>%s grader</b>." % (sg(max(vals)), par(min(vals)), d(max(vals) - min(vals))), "grader")

    def vilsen():
        P = [("Ett diagram visar att försäljningen ökat från 100 till 110 men y-axeln börjar på 95. Vad är problemet?", "Ökningen ser mycket större ut än den är", ["Det finns ingen ökning", "Försäljningen har minskat", "Det är rätt och tydligt"]),
             ("Vilket diagram passar bäst för att visa hur temperaturen ändras under ett år?", "Linjediagram", ["Cirkeldiagram", "Stapeldiagram med kategorier", "Tabell utan värden"]),
             ("Vilket diagram passar bäst för att visa hur stor andel av en budget som går till olika saker?", "Cirkeldiagram", ["Linjediagram", "Lådagram", "Punktdiagram"]),
             ("En undersökning frågade bara 5 personer. Vad är problemet?", "Urvalet är för litet för att dra slutsatser", ["Diagrammet blir för stort", "Det blir för många svar", "Inget problem"]),
             ("En enkät om skolmaten delades bara ut till elever som äter i matsalen varje dag. Vad är problemet?", "Urvalet är inte representativt för alla elever", ["Enkäten var för lång", "Det är för många elever", "Inget problem"]),
             ("Vilket diagram passar bäst för att jämföra antal elever i olika klasser?", "Stapeldiagram", ["Linjediagram", "Cirkeldiagram över tid", "Lådagram"])]
        q, r, w = ch(P)
        return M(q, r, w, "<b>%s</b>." % r)

    sets = [("Stapeldiagram", [(stap, 20)]), ("Relativ frekvens", [(relativ, 20)]), ("Cirkeldiagram", [(cirkel, 20)]), ("Linjediagram", [(linje, 20)]), ("Välj och granska diagram", [(vilsen, 6), (stap, 7), (cirkel, 7)])]
    return unit("tabeller-och-diagram", "S", "Tabeller och diagram: relativ frekvens, cirkel- och linjediagram", "Tabeller och diagram",
                "Tabeller och diagram för att beskriva resultat från undersökningar. Hur de kan tolkas och granskas, även hur de kan vara vilseledande. Relativ frekvens.",
                "Arbetsblad om tabeller och diagram för årskurs 8: stapeldiagram, relativ frekvens, cirkeldiagram, linjediagram och att välja och granska diagram. 100 uppgifter med facit.",
                "Relativ frekvens = frekvens/totalt", "I ett cirkeldiagram är 100 % hela 360°.", sets,
                ["Frekvensen är hur många gånger något förekommer. Den relativa frekvensen är andelen av alla: frekvens delat med totalt antal.",
                 "Stapeldiagram jämför kategorier, linjediagram visar förändring över tid och cirkeldiagram visar andelar av en helhet.",
                 "Granska alltid axlarna. En axel som inte börjar på 0 kan få små skillnader att se stora ut."],
                [("8 av 40 svarade ja", ["8/40 = 0,2"], "20 %"), ("30 % i ett cirkeldiagram", ["0,30 · 360°"], "108°")],
                [["Relativ frekvens = frekvensen", "Dela med totalen: 8/40 = 20 %"], ["Cirkeldiagram för temperatur över tid", "Linjediagram visar förändring"], ["Tittar inte på axelns början", "Kontrollera var y-axeln börjar"]],
                [("Vad är skillnaden på frekvens och relativ frekvens?", "Frekvensen är ett antal, den relativa frekvensen är en andel."), ("Varför kan diagram vara vilseledande?", "Avbrutna axlar, ojämna skalor och för små urval kan ge fel bild."),
                 ("Hur räknar jag vinklar i ett cirkeldiagram?", "Andelen gånger 360°.")])


# ============================================================ sannolikhet (åk 7, 8, 9)
def sannolikhet(lv):
    def enkel():
        k = ri(0, 2)
        if k == 0:
            cols = [("röda", ri(1, 9)), ("blå", ri(1, 9)), ("gröna", ri(1, 9))]
            n = sum(c for _, c in cols)
            i = ri(0, 2)
            p = F(cols[i][1], n)
            return M("I en påse finns %s. Du tar en kula utan att titta. Vad är sannolikheten att den är %s?" % (lista("%d %s kulor" % (c, nm) if c > 1 else "%d %s kula" % (c, nm[:-1] if nm.endswith("a") else nm) for nm, c in cols), cols[i][0][:-1] if cols[i][0].endswith("a") else cols[i][0]),
                     fq(p), [fr(cols[i][1], n - cols[i][1]) if n - cols[i][1] > 0 and F(cols[i][1], n - cols[i][1]) != p else fq(p + F(1, n)), fq(1 - p) if 1 - p != p else fq(p / 2), fr(1, 3) if p != F(1, 3) else fr(1, 2)], "Gynnsamma %d av möjliga %d: <b>%s</b>." % (cols[i][1], n, fq(p)))
        if k == 1:
            e = ri(0, 3)
            if e == 0:
                v = ri(1, 6)
                return M("Du kastar en tärning. Vad är sannolikheten att få %d?" % v, fr(1, 6), [fr(v, 6) if v > 1 else fr(1, 2), fr(1, 2) if v > 1 else fr(2, 6), fr(5, 6)], "En gynnsam av sex möjliga: <b>1/6</b>.") if v > 1 else None
            if e == 1:
                v = ri(2, 5)
                return M("Du kastar en tärning. Vad är sannolikheten att få mer än %d?" % v, fq(F(6 - v, 6)), [fq(F(v, 6)), fq(F(6 - v + 1, 6)), fr(1, 6) if F(6 - v, 6) != F(1, 6) else fr(1, 2)], "%s ger %d av 6: <b>%s</b>." % (lista(str(x) for x in range(v + 1, 7)), 6 - v, fq(F(6 - v, 6))))
            if e == 2:
                return M("Du kastar en tärning. Vad är sannolikheten att få ett jämnt tal?", fr(1, 2), [fr(1, 3), fr(1, 6), fr(2, 3)], "2, 4 och 6 ger 3 av 6 = <b>1/2</b>.")
            v = ri(1, 3)
            return M("Du kastar en tärning. Vad är sannolikheten att få %d eller %d?" % (v, v + 3), fr(1, 3), [fr(1, 6), fr(1, 2), fr(2, 3)], "2 gynnsamma av 6: <b>1/3</b>.")
        n = ch([10, 20, 30, 50, 100])
        w = ri(1, n // 4)
        p = F(w, n)
        return M("I ett lotteri finns %d lotter och %d av dem ger vinst. Du köper en lott. Vad är sannolikheten att vinna i procent?" % (n, w), d(p * 100) + NB + "%", [d(F(w, 1)) + NB + "%" if w * 100 != w * n else d(p * 100 + 5) + NB + "%", d(100 - p * 100) + NB + "%", d(p * 1000) + NB + "%" if p * 1000 <= 100 else d(p * 50) + NB + "%"], "%d/%d = %s = <b>%s %%</b>." % (w, n, d(p), d(p * 100)))

    def komplement():
        p = ch([F(1, 4), F(1, 5), F(3, 10), F(2, 5), F(1, 3), F(1, 6), F(3, 8), F(7, 10), F(9, 20), F(1, 10), F(3, 20), F(2, 7), F(3, 5), F(5, 8), F(4, 9), F(1, 8)])
        ctx = ch([("det regnar i morgon", "det inte regnar"), ("bussen är sen", "bussen kommer i tid"), ("du vinner på en lott", "du inte vinner"),
                  ("en lampa är trasig", "lampan fungerar"), ("ditt lag vinner", "ditt lag inte vinner"), ("det snöar på julafton", "det inte snöar")])
        if coin():
            return M("Sannolikheten att %s är %s. Vad är sannolikheten att %s?" % (ctx[0], fq(p), ctx[1]), fq(1 - p), [fq(p), fq(1 - p / 2), fq(p + F(1, 10))], "P(inte) = 1 − %s = <b>%s</b>." % (fq(p), fq(1 - p)))
        pp = ch([5, 10, 15, 20, 25, 30, 35, 40, 45, 55, 60, 65, 70, 75, 80, 85, 90, 95])
        return M("Sannolikheten att %s är %d %%. Vad är sannolikheten att %s?" % (ctx[0], pp, ctx[1]), "%d %%" % (100 - pp), ["%d %%" % pp, "%d %%" % (100 - pp // 2), "%d %%" % (100 - pp + 10) if 100 - pp + 10 <= 100 else "50 %"], "100 %% − %d %% = <b>%d %%</b>." % (pp, 100 - pp))

    def frekv():
        n = ch([50, 100, 200, 400, 500])
        x = ri(n // 10, n // 2)
        k = ri(0, 1)
        if k == 0:
            return M("Ett häftstift kastades %d gånger och landade med spetsen upp %d gånger. Vad är den relativa frekvensen?" % (n, x), d(F(x, n)), [d(F(x, n - x)) if (F(x, n - x) * 1000).denominator == 1 else d(F(x, n) + F(1, 10)), d(1 - F(x, n)), d(F(x, 100)) if n != 100 else d(F(x, 1000))], "%d/%d = <b>%s</b>." % (x, n, d(F(x, n))))
        p = ch([F(1, 6), F(1, 2), F(1, 4), F(1, 5), F(1, 10), F(3, 10)])
        N = ch([60, 120, 300, 600, 1200]) if p == F(1, 6) else ch([100, 200, 400, 1000])
        v = p * N
        if v.denominator != 1:
            return None
        return MN("Sannolikheten för en händelse är %s. Hur många gånger kan du vänta dig att den inträffar på %s försök?" % (fq(p), num(N)), v, [v * 2, N - v, v + 10], "%s · %s = <b>%s</b>." % (fq(p), num(N), num(v)), "gånger")

    def tvasteg():
        k = ri(0, 3)
        if k == 0:
            a, b = ri(1, 6), ri(1, 6)
            return M("Du kastar två tärningar. Vad är sannolikheten att få %d på den första och %d på den andra?" % (a, b), fr(1, 36), [fr(1, 12), fr(2, 36) if a != b else fr(1, 6), fr(1, 6) if a != b else fr(2, 36)], "1/6 · 1/6 = <b>1/36</b>.") if True else None
        if k == 1:
            s = ri(2, 12)
            c = sum(1 for x in range(1, 7) for y in range(1, 7) if x + y == s)
            return M("Du kastar två tärningar. Vad är sannolikheten att summan blir %d?" % s, fq(F(c, 36)), [fq(F(c + 1, 36)), fr(1, 11), fq(F(1, s)) if F(1, s) != F(c, 36) else fr(1, 6)], "%d av 36 kombinationer ger summan %d: <b>%s</b>." % (c, s, fq(F(c, 36))))
        if k == 2:
            p = ch([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(2, 5), F(3, 5)])
            n = ri(2, 4)
            v = p ** n
            return M("Sannolikheten att ett lag vinner en match är %s. Vad är sannolikheten att de vinner %d matcher i rad?" % (fq(p), n), fq(v), [fq(p * n) if p * n <= 1 else fq(v * 2), fq(p), fq(1 - v)], "%s%s = <b>%s</b>." % ("(%s)" % fq(p) if True else fq(p), sup(n), fq(v)))
        a, b = ri(2, 6), ri(2, 6)
        n = a + b
        if coin():
            v = F(a, n) * F(a - 1, n - 1)
            return M("I en låda finns %d röda och %d blå kulor. Du tar två kulor utan att lägga tillbaka. Vad är sannolikheten att båda är röda?" % (a, b), fq(v), [fq(F(a, n) ** 2), fq(F(a, n) * F(a, n - 1)), fq(F(2 * a, n))if F(2 * a, n) < 1 else fq(v / 2)], "%s · %s = <b>%s</b>." % (fr(a, n), fr(a - 1, n - 1), fq(v)))
        v = F(a, n) * F(b, n - 1) + F(b, n) * F(a, n - 1)
        return M("I en låda finns %d röda och %d blå kulor. Du tar två kulor utan att lägga tillbaka. Vad är sannolikheten att de har olika färg?" % (a, b), fq(v), [fq(F(a, n) * F(b, n - 1)), fq(2 * F(a, n) * F(b, n)), fq(1 - v)], "röd–blå eller blå–röd: %s · %s + %s · %s = <b>%s</b>." % (fr(a, n), fr(b, n - 1), fr(b, n), fr(a, n - 1), fq(v))) if 1 - v != v else None

    def mynt():
        n = ri(2, 5)
        k = ri(0, 4)
        if k == 0:
            return M("Du singlar slant %d gånger. Vad är sannolikheten att det blir krona varje gång?" % n, fr(1, 2 ** n), [fr(1, 2 * n), fr(1, 2), fr(n, 2 ** n)], "(1/2)%s = <b>1/%d</b>." % (sup(n), 2 ** n))
        if k == 1:
            return M("Du singlar slant %d gånger. Vad är sannolikheten att det blir minst en klave?" % n, fq(1 - F(1, 2 ** n)), [fr(1, 2 ** n), fr(1, 2), fq(F(n, 2 ** n))], "Motsatsen är krona varje gång: 1 − 1/%d = <b>%s</b>." % (2 ** n, fq(1 - F(1, 2 ** n))))
        if k == 2:
            return M("Du singlar slant två gånger. Vad är sannolikheten att det blir en krona och en klave?", fr(1, 2), [fr(1, 4), fr(1, 3), fr(3, 4)], "Utfallen är KK, KL, LK och LL. Två av fyra: <b>1/2</b>.")
        m = ri(2, 3)
        if k == 3:
            return M("Du kastar %d tärningar. Vad är sannolikheten att ingen visar en sexa?" % m, fq(F(5, 6) ** m), [fq(F(1, 6) ** m), fq(1 - F(5, 6) ** m), fq(F(5, 6 * m))], "(5/6)%s = <b>%s</b>." % (sup(m), fq(F(5, 6) ** m)))
        return M("Du kastar %d tärningar. Vad är sannolikheten att minst en visar en sexa?" % m, fq(1 - F(5, 6) ** m), [fq(F(m, 6)), fq(F(5, 6) ** m), fq(F(1, 6) ** m)], "Motsatsen är ingen sexa: 1 − (5/6)%s = <b>%s</b>." % (sup(m), fq(1 - F(5, 6) ** m)))

    if lv == 7:
        sets = [("Sannolikhet som bråk", [(enkel, 20)]), ("Sannolikhet i procent", [(enkel, 10), (komplement, 10)]), ("Komplementhändelse", [(komplement, 20)]),
                ("Relativ frekvens", [(frekv, 20)]), ("Två mynt och två tärningar", [(mynt, 10), (tvasteg, 10)])]
        title = "Sannolikhet: gynnsamma utfall, komplement och relativ frekvens"
    elif lv == 8:
        sets = [("Sannolikhet för en händelse", [(enkel, 20)]), ("Komplementhändelse", [(komplement, 20)]), ("Två tärningar", [(tvasteg, 20)]),
                ("Slantsingling", [(mynt, 8), (tvasteg, 12)]), ("Försök och förväntat antal", [(frekv, 20)])]
        title = "Sannolikhet: slumpförsök i flera steg"
    else:
        sets = [("Sannolikhet och komplement", [(enkel, 10), (komplement, 10)]), ("Flera steg", [(tvasteg, 20)]), ("Utan återläggning", [(tvasteg, 20)]),
                ("Minst en gång", [(mynt, 8), (komplement, 12)]), ("Relativ frekvens och förväntan", [(frekv, 20)])]
        title = "Sannolikhet: flera steg, utan återläggning och minst en gång"
    return unit("sannolikhet", "S", title, "Sannolikhet",
                "Sannolikhet, chans och risk grundat på observationer, simuleringar eller statistiskt material från vardagliga situationer. Jämförelse mellan experimentell och teoretisk sannolikhet. Slumpförsök i flera steg.",
                "Arbetsblad om sannolikhet för årskurs %d: sannolikhet som bråk och procent, komplementhändelse, relativ frekvens, försök i flera steg och slantsingling. 100 uppgifter med facit." % lv,
                "P = gynnsamma/möjliga", "P(inte A) = 1 − P(A).", sets,
                ["Sannolikheten för en händelse är antalet gynnsamma utfall delat med antalet möjliga utfall. Den är alltid mellan 0 och 1.",
                 "Sannolikheten att något inte händer är 1 minus sannolikheten att det händer.",
                 "Vid försök i flera steg multiplicerar du sannolikheterna längs vägen i ett träddiagram. Tar du utan att lägga tillbaka ändras antalet i andra steget."],
                [("3 röda av 10 kulor", ["3 gynnsamma av 10"], "3/10"), ("Två sexor med två tärningar", ["1/6 · 1/6"], "1/36")],
                [["P(sexa) = 6/6", "En sexa av sex sidor: 1/6"], ["Adderar sannolikheter i flera steg", "Multiplicera längs grenarna"], ["Glömmer att en kula är borta", "Utan återläggning blir det en kula mindre"]],
                [("Vad är skillnaden på relativ frekvens och sannolikhet?", "Relativ frekvens räknas från försök. Sannolikhet är det teoretiska värdet som frekvensen närmar sig vid många försök."),
                 ("Kan en sannolikhet vara större än 1?", "Nej. 1 betyder att det är säkert, 0 att det är omöjligt."), ("Vad är ett träddiagram?", "En bild där varje gren är ett möjligt utfall. Sannolikheterna multipliceras längs grenarna.")])


# ============================================================ kombinatorik (åk 8)
def kombinatorik(lv):
    def multi():
        a, b = ri(2, 8), ri(2, 8)
        c = ri(2, 5)
        k = ri(0, 2)
        if k == 0:
            return MN("På en restaurang finns %d förrätter och %d huvudrätter. Hur många olika middagar med en förrätt och en huvudrätt kan man välja?" % (a, b), a * b, [a + b, a * b + 1, 2 * a * b], "%d · %d = <b>%d</b>." % (a, b, a * b), "middagar")
        if k == 1:
            return MN("%s har %d tröjor, %d byxor och %d par skor. Hur många olika klädkombinationer finns det?" % (K().name(), a, b, c), a * b * c, [a + b + c, a * b, a * b * c - 1], "%d · %d · %d = <b>%d</b>." % (a, b, c, a * b * c), "kombinationer")
        n = ri(2, 5)
        s = ri(2, 10)
        return MN("Ett lås har %d hjul med siffrorna 0–%d på varje. Hur många koder finns det?" % (n, s - 1), s ** n, [s * n, n ** s if n ** s < 10 ** 6 else s ** n * 2, s ** (n - 1)], "%d%s = <b>%s</b>." % (s, sup(n), num(s ** n)), "koder")

    def ordning():
        n = ri(3, 7)
        f = math.factorial(n)
        k = ri(0, 2)
        if k == 0:
            return MN("På hur många sätt kan %d personer ställa sig i en kö?" % n, f, [n * n, n * (n - 1), f // 2], "%s = <b>%s</b>." % (" · ".join(str(x) for x in range(n, 0, -1)), num(f)), "sätt")
        if k == 1:
            m = ri(8, 15)
            v = m * (m - 1) * (m - 2)
            return MN("%d löpare tävlar. På hur många sätt kan guld, silver och brons fördelas?" % m, v, [m * 3, m ** 3, v // 6], "%d · %d · %d = <b>%s</b>." % (m, m - 1, m - 2, num(v)), "sätt")
        if coin():
            n = ri(3, 9)
            sak = ch(["böcker i en hylla", "bilder på en vägg", "koppar på en rad", "elever på en bänk"])
            return MN("På hur många sätt kan %d %s ordnas?" % (n, sak), math.factorial(n), [n * n, n * (n - 1), math.factorial(n - 1)], "%d! = <b>%s</b>." % (n, num(math.factorial(n))), "sätt")
        w = ch(["SOL", "BIL", "HUND", "KATT", "MATS", "LAMPA", "BORD", "STOL", "FISK", "TRÄD", "ÖGA", "NOLL", "BOLL", "SKOLA", "BUSS"])
        letters = list(w)
        cnt = math.factorial(len(w))
        for c in set(letters):
            cnt //= math.factorial(letters.count(c))
        return MN("Hur många olika ord (med eller utan betydelse) kan man bilda av alla bokstäverna i %s?" % w, cnt, [math.factorial(len(w)) if math.factorial(len(w)) != cnt else cnt * 2, len(w) ** 2, len(w) * (len(w) - 1)], "%d bokstäver kan ordnas på %d! sätt%s: <b>%d</b>." % (len(w), len(w), " delat med de lika bokstävernas byten" if cnt != math.factorial(len(w)) else "", cnt), "ord")

    def val():
        n = ri(4, 10)
        k = ri(0, 1)
        if k == 0:
            v = n * (n - 1) // 2
            return MN("%d personer hälsar på varandra en gång var. Hur många handslag blir det?" % n, v, [n * (n - 1), n * n, n], "%d · %d/2 = <b>%d</b>. Varje handslag räknas bara en gång." % (n, n - 1, v), "handslag")
        v = n * (n - 1) // 2
        return MN("%d lag spelar en serie där alla möter alla en gång. Hur många matcher blir det?" % n, v, [n * (n - 1), n * 2, v + n], "%d · %d/2 = <b>%d</b>." % (n, n - 1, v), "matcher")

    def trad():
        k = ri(0, 2)
        if k == 0:
            n = ri(2, 6)
            return MN("En slant singlas %d gånger. Hur många olika utfall finns det?" % n, 2 ** n, [2 * n, n * n, 2 ** n - 1], "2%s = <b>%d</b>." % (sup(n), 2 ** n), "utfall")
        if k == 1:
            m = ri(1, 3)
            return MN("Du kastar %d %s och singlar en slant. Hur många utfall finns det?" % (m, "tärning" if m == 1 else "tärningar"), 6 ** m * 2, [6 * m + 2, 6 ** m, 6 ** m * 2 - 1], "6%s · 2 = <b>%d</b>." % (sup(m), 6 ** m * 2), "utfall")
        a, b = ri(3, 8), ri(2, 6)
        return MN("Du väljer en av %d glassorter och en av %d strutar. Hur många olika glassar kan du få?" % (a, b), a * b, [a + b, a * b * 2, a * b - 1], "%d · %d = <b>%d</b>." % (a, b, a * b), "glassar")

    def kod():
        k = ri(0, 2)
        if k == 0:
            n = ri(3, 6)
            m = ch([10, 9, 6, 5, 4])
            q = "En pinkod har %d siffror (0–9). Hur många koder finns det?" % n if m == 10 else "En kod har %d tecken och varje tecken är en av %d färger. Hur många koder finns det?" % (n, m)
            return MN(q, m ** n, [m * n, (m - 1) ** n, m ** (n - 1)], "%d%s = <b>%s</b>." % (m, sup(n), num(m ** n)), "koder")
        if k == 1:
            l, s = ri(2, 3), ri(2, 4)
            v = 26 ** l * 10 ** s if False else 29 ** l * 10 ** s
            return MN("En kod börjar med %d bokstäver (A–Ö, 29 st) följt av %d siffror. Hur många koder finns det?" % (l, s), v, [29 * l + 10 * s, 29 ** l + 10 ** s, v // 2], "29%s · 10%s = <b>%s</b>." % (sup(l), sup(s), num(v)), "koder")
        n = ri(3, 5)
        v = 10 * 9 ** (n - 1) if False else 10 * 9 * 8 if n == 3 else 10 * 9 * 8 * 7 if n == 4 else 10 * 9 * 8 * 7 * 6
        return MN("En kod har %d siffror och samma siffra får inte användas två gånger. Hur många koder finns det?" % n, v, [10 ** n, v // 2, 9 ** n], "%s = <b>%s</b>." % (" · ".join(str(10 - i) for i in range(n)), num(v)), "koder")

    sets = [("Multiplikationsprincipen", [(multi, 20)]), ("Ordning och köer", [(ordning, 20)]), ("Handslag och matcher", [(val, 10), (multi, 10)]),
            ("Utfall och träddiagram", [(trad, 10), (ordning, 10)]), ("Koder", [(kod, 20)])]
    return unit("kombinatorik", "S", "Kombinatorik: multiplikationsprincipen, ordning och koder", "Kombinatorik",
                "Kombinatoriska principer och metoder för att lösa problem i vardagliga och matematiska situationer. Multiplikationsprincipen, permutationer och kombinationer.",
                "Arbetsblad om kombinatorik för årskurs 8: multiplikationsprincipen, ordning och köer, handslag och matcher, utfall och koder. 100 uppgifter med facit.",
                "Antal val · antal val · …", "Spelar ordningen roll eller inte?", sets,
                ["Multiplikationsprincipen: om du först har a val och sedan b val finns det a · b möjligheter.",
                 "Spelar ordningen roll blir det fler möjligheter: 5 personer i en kö kan stå på 5 · 4 · 3 · 2 · 1 = 120 sätt.",
                 "Spelar ordningen ingen roll, som vid handslag, räknar du varje par en gång: n · (n − 1)/2."],
                [("3 tröjor och 4 byxor", ["3 · 4"], "12 kombinationer"), ("6 personer hälsar", ["6 · 5/2"], "15 handslag")],
                [["Adderar antalet val", "Multiplicera: 3 · 4 = 12"], ["Handslag: 6 · 5 = 30", "Varje handslag räknas två gånger, dela med 2"], ["Kö med 4 personer: 4 · 4", "Varje plats har ett val mindre: 4 · 3 · 2 · 1"]],
                [("Vad är n!?", "n fakultet: n · (n − 1) · … · 1. Till exempel 4! = 24."), ("När spelar ordningen roll?", "När ABC och BCA räknas som olika, till exempel koder och placeringar."),
                 ("Hur ritar jag ett träddiagram?", "En gren för varje val i första steget, och från varje gren nya grenar för nästa steg.")])


# ============================================================ problemlösning
def problemlosning(lv):
    def kvitto():
        nm, g = K().next()
        hon = "hon" if g == "f" else "han"
        a, b = ri(15, 60), ri(8, 40)
        n1, n2 = ri(2, 5), ri(2, 6)
        tot = n1 * a + n2 * b
        pay = ((tot // 100) + 1) * 100 if tot % 100 else tot + 100
        return MN("%s köper %d smörgåsar för %s styck och %d drickor för %s styck. %s betalar med %s. Hur mycket får %s tillbaka?" % (nm, n1, kr(a), n2, kr(b), cap(hon), kr(pay), hon),
                  pay - tot, [tot, pay - n1 * a, pay - a - b], "%d · %d + %d · %d = %d. %d − %d = <b>%d kr</b>." % (n1, a, n2, b, tot, pay, tot, pay - tot), "kr")

    def baklanges():
        x = ri(5, 40)
        a, b = ri(2, 5), ri(3, 30)
        k = ri(0, 1)
        if k == 0:
            r = x * a + b
            return MN("Jag tänker på ett tal. Jag multiplicerar det med %d och adderar %d. Då får jag %d. Vilket tal tänkte jag på?" % (a, b, r), x, [r - b, F(r, a) if F(r, a).denominator == 1 and F(r, a) != x else x + 1, (r + b) // a if (r + b) % a == 0 and (r + b) // a != x else x - 1], "Räkna baklänges: (%d − %d)/%d = <b>%d</b>." % (r, b, a, x))
        h = ri(2, 5) * 2
        start = h * ri(5, 20)
        after = start // 2 - b
        if after <= 0:
            return None
        nm, g = K().next()
        hon = "hon" if g == "f" else "han"
        return MN("%s hade några kronor. Först gav %s bort hälften och sedan köpte %s en glass för %s. Nu har %s %s kvar. Hur mycket hade %s från början?" % (nm, hon, hon, kr(b), hon, kr(after), hon), start, [after * 2, (after + b) * 2 + b, after + b], "Baklänges: %d + %d = %d. Dubbelt: <b>%d kr</b>." % (after, b, after + b, start), "kr")

    def logik():
        k = ri(0, 3)
        if k == 0:
            n = ri(10, 40)
            a, b = ri(n // 3, n - 2), ri(n // 3, n - 2)
            both = a + b - n
            if both <= 0:
                return None
            return MN("I en klass med %d elever spelar %d fotboll och %d innebandy. Alla spelar minst en av sporterna. Hur många spelar båda?" % (n, a, b), both, [a + b, n - a, abs(a - b)], "%d + %d = %d. Det är %d fler än antalet elever, så <b>%d</b> spelar båda." % (a, b, a + b, both, both), "elever")
        if k == 1:
            t, b = ri(2, 6), ri(2, 9)
            sid = ri(3, 8)
            return MN("Ett staket ska vara %d m långt med en stolpe var %d:e meter. Hur många stolpar behövs, om det ska finnas en i varje ände?" % (sid * t, t), sid + 1, [sid, sid * t, sid + 2], "%d/%d = %d mellanrum. Stolparna är en fler: <b>%d</b>." % (sid * t, t, sid, sid + 1), "stolpar")
        if k == 2:
            nm, g = K().next()
            x = ri(8, 16)
            m = ri(25, 45)
            y = ri(2, 10)
            return MN("%s är %d år och %s mamma är %d år. Om hur många år är mamman dubbelt så gammal som %s?" % (nm, x, "hennes" if g == "f" else "hans", m, nm), m - 2 * x, [m - x, 2 * x - m if 2 * x - m > 0 else m - 2 * x + 2, m - 2 * x + 1], "Om t år: %d + t = 2(%d + t) ger t = %d − %d = <b>%d</b>." % (m, x, m, 2 * x, m - 2 * x), "år") if m - 2 * x > 0 else None
        s = ri(2, 7)
        n = s * (s + 1) // 2
        return MN("Klossar staplas som en trappa: 1 kloss överst, sedan 2, sedan 3 och så vidare. Hur många klossar behövs till en trappa med %d steg?" % s, n, [s * s, s * 2, n - 1], "%s = <b>%d</b>." % (" + ".join(str(i) for i in range(1, s + 1)), n), "klossar")

    def jamfor():
        k = ri(0, 2)
        if k == 0:
            a, pa = ri(2, 6), ri(20, 45)
            b, pb = a + ri(1, 4), None
            pb = ri(pa + 5, pa * 2)
            ja, jb = F(pa, a), F(pb, b)
            if ja == jb:
                return None
            return M("Butik A säljer %d kg potatis för %s. Butik B säljer %d kg för %s. Var är potatisen billigast per kilo?" % (a, kr(pa), b, kr(pb)), "Butik A" if ja < jb else "Butik B", ["Butik B" if ja < jb else "Butik A", "Lika billigt", "Det går inte att avgöra"], "A: %s kr/kg, B: %s kr/kg. Billigast: <b>%s</b>." % (rd(ja, 2), rd(jb, 2), "butik A" if ja < jb else "butik B"))
        if k == 1:
            f1, p1 = ri(0, 2) * 50, ri(15, 30)
            f2, p2 = f1 + ri(2, 8) * 50, p1 - ri(5, 12)
            if p2 <= 0:
                return None
            x = F(f2 - f1, p1 - p2)
            if x.denominator != 1:
                return None
            n = int(x) + ri(1, 5)
            c1, c2 = f1 + p1 * n, f2 + p2 * n
            return M("Gym A kostar %s plus %s per besök. Gym B kostar %s plus %s per besök. Vilket är billigast för %d besök?" % (kr(f1), kr(p1), kr(f2), kr(p2), n), "Gym A" if c1 < c2 else "Gym B" if c2 < c1 else "Lika", ["Gym B" if c1 < c2 else "Gym A", "Lika" if c1 != c2 else "Gym A", "Det går inte att avgöra"], "A: %d kr, B: %d kr. Billigast: <b>%s</b>." % (c1, c2, "gym A" if c1 < c2 else "gym B" if c2 < c1 else "lika"))
        v1, v2 = ri(4, 12) * 10, ri(4, 12) * 10
        s = ri(2, 10) * 40
        if v1 == v2:
            return None
        t1, t2 = F(s, v1), F(s, v2)
        diff = abs(t1 - t2) * 60
        if diff.denominator != 1:
            return None
        return MN("Två bilar kör %d km. Den ena håller %d km/h och den andra %d km/h. Hur många minuter tidigare kommer den snabbare fram?" % (s, v1, v2), diff, [abs(v1 - v2), diff + 30, diff / 2], "%d/%d = %s h och %d/%d = %s h. Skillnaden är <b>%s min</b>." % (s, v1, d(t1) if (t1 * 100).denominator == 1 else rd(t1, 2), s, v2, d(t2) if (t2 * 100).denominator == 1 else rd(t2, 2), d(diff)), "min")

    def rimlig():
        P = [("Ungefär hur lång är en vuxen persons steg?", "70 cm", ["7 cm", "7 m", "700 m"]), ("Ungefär hur mycket väger en liter mjölk?", "1 kg", ["100 g", "10 kg", "1 g"]),
             ("Ungefär hur lång tid tar det att gå 1 km?", "12 minuter", ["1 minut", "2 timmar", "12 sekunder"]), ("Ungefär hur många hjärtslag gör ett hjärta på en dag?", "100 000", ["1 000", "10 000 000", "100"]),
             ("Ungefär hur stor är en vanlig skolgård?", "3 000 m²", ["30 m²", "300 km²", "3 m²"]), ("Ungefär hur mycket vatten rymmer ett badkar?", "200 liter", ["20 liter", "2 000 liter", "2 liter"]),
             ("Ungefär hur högt är ett hus med fyra våningar?", "13 m", ["1,3 m", "130 m", "40 m"]), ("Ungefär hur mycket väger en personbil?", "1,5 ton", ["150 kg", "15 ton", "15 kg"]),
             ("Ungefär hur många sekunder är ett dygn?", "86 400", ["8 640", "864 000", "1 440"]), ("Ungefär hur långt är det från Malmö till Kiruna?", "1 500 km", ["150 km", "15 000 km", "50 km"])]
        q, r, w = ch(P)
        return M(q, r, w, "Gör ett överslag. Det rimliga svaret är <b>%s</b>." % r)

    if lv == 7:
        sets = [("Vardagsproblem", [(kvitto, 20)]), ("Räkna baklänges", [(baklanges, 20)]), ("Logiska problem", [(logik, 20)]), ("Jämför och välj", [(jamfor, 20)]), ("Rimlighet", [(rimlig, 10), (kvitto, 10)])]
    elif lv == 8:
        sets = [("Räkna baklänges", [(baklanges, 20)]), ("Logiska problem", [(logik, 20)]), ("Jämför och välj", [(jamfor, 20)]), ("Vardagsproblem", [(kvitto, 20)]), ("Rimlighet", [(rimlig, 10), (logik, 10)])]
    else:
        sets = [("Jämför och välj", [(jamfor, 20)]), ("Logiska problem", [(logik, 20)]), ("Räkna baklänges", [(baklanges, 20)]), ("Vardagsproblem", [(kvitto, 20)]), ("Rimlighet och överslag", [(rimlig, 10), (jamfor, 10)])]
    return unit("problemlosning", "P", "Problemlösning: strategier för matematiska problem", "Problemlösning",
                "Strategier för problemlösning i vardagliga och matematiska situationer. Formulering av matematiska frågeställningar och värdering av valda strategier, metoder och resultat.",
                "Arbetsblad om problemlösning för årskurs %d: vardagsproblem, räkna baklänges, logiska problem, jämför och välj och rimlighet. 100 uppgifter med facit." % lv,
                "Förstå, planera, lös, kontrollera", "Pröva en annan strategi om du kör fast.", sets,
                ["Läs problemet noga och skriv upp vad du vet och vad du ska ta reda på.",
                 "Välj en strategi: rita en bild, gör en tabell, räkna baklänges, pröva dig fram eller ställ upp en ekvation.",
                 "Kontrollera till sist att svaret är rimligt och att du har svarat på frågan."],
                [("Ett tal gånger 3 plus 5 blir 26", ["Baklänges: 26 − 5 = 21", "21/3"], "7"), ("12 m staket med stolpe var 3:e meter", ["12/3 = 4 mellanrum", "En stolpe till"], "5 stolpar")],
                [["Räknar bara ut en del av svaret", "Läs frågan igen innan du svarar"], ["Glömmer stolpen i änden", "Rita en bild, det blir en stolpe mer än mellanrummen"], ["Kontrollerar inte rimligheten", "Gör ett överslag och jämför"]],
                [("Vad gör jag om jag inte vet hur jag ska börja?", "Rita en bild eller pröva med små tal först."), ("Finns det bara ett rätt sätt?", "Nej, ofta finns det flera strategier som ger samma svar."),
                 ("Hur vet jag att svaret är rimligt?", "Gör ett överslag och tänk på om storleken stämmer med verkligheten.")])


UNITS = {"lagesmatt": lagesmatt, "spridningsmatt": spridning, "tabeller-och-diagram": diagram, "sannolikhet": sannolikhet, "kombinatorik": kombinatorik, "problemlosning": problemlosning}
