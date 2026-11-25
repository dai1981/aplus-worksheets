# -*- coding: utf-8 -*-
"""Sverige åk 4–6: statistik, sannolikhet, kombinatorik och problemlösning（lv = 4, 5, 6）"""
import math
from fractions import Fraction as F
import se_m as S
from se_m import num, kr, M, fr, fq, d, ri, ch, sh, cap, unit, tab
from se_common import wrap, text, line, fig, stapel, INK, GREEN, FILL, RED, BLUE
from se_m_a import R0


def K():
    return S.K


CATS = [("Favoritsport", ["fotboll", "simning", "innebandy", "ridning", "dans", "hockey"]), ("Favoritfrukt", ["äpple", "banan", "päron", "apelsin", "vindruvor"]),
        ("Husdjur", ["hund", "katt", "kanin", "fisk", "häst", "marsvin"]), ("Färdsätt till skolan", ["går", "cyklar", "buss", "bil", "sparkcykel"])]
MAN = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]


def linjediagram(vals, labs, ylab, step):
    W, H, x0, y0 = 340, 190, 46, 170
    top = int(math.ceil(max(vals) / float(step))) * step
    lo = 0
    Y = lambda v: y0 - (v - lo) / float(top - lo) * 150
    s = []
    for v in range(lo, top + 1, step):
        s.append(line(x0, Y(v), x0 + 280, Y(v), "#dddddd", 1) + text(x0 - 6, Y(v) + 4, num(v), 11, anchor="end", weight=400))
    s.append(line(x0, y0, x0 + 280, y0, INK, 2) + line(x0, y0, x0, 14, INK, 2))
    gx = 280.0 / (len(vals) - 1)
    pts = [(x0 + i * gx, Y(v)) for i, v in enumerate(vals)]
    s.append("<polyline points='%s' fill='none' stroke='%s' stroke-width='2.5'/>" % (" ".join("%.1f,%.1f" % p for p in pts), RED))
    for (x, y), l in zip(pts, labs):
        s.append("<circle cx='%.1f' cy='%.1f' r='3.5' fill='%s'/>" % (x, y, RED) + text(x, y0 + 16, l, 11, weight=400))
    s.append(text(8, 10, ylab, 11, anchor="start", weight=600))
    return wrap(W + 20, H + 14, "".join(s), "linjediagram", lg=True)


def cirkel(parts):
    """parts: [(namn, andel i hundradelar)] som summerar till 100"""
    cols = ["#e07a5f", "#6a9fd4", "#f2c94c", "#81b29a", "#c9a6d8"]
    cx, cy, r = 90, 90, 76
    s = []
    a0 = -90.0
    leg = []
    for i, (n, p) in enumerate(parts):
        a1 = a0 + 360.0 * p / 100
        large = 1 if a1 - a0 > 180 else 0
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z' fill='%s' stroke='#ffffff' stroke-width='2'/>" % (cx, cy, x0, y0, r, r, large, x1, y1, cols[i]))
        leg.append("<rect x='190' y='%d' width='14' height='14' fill='%s'/>" % (24 + i * 24, cols[i]) + text(210, 36 + i * 24, "%s %d %%" % (n, p), 12, anchor="start", weight=400))
        a0 = a1
    return wrap(330, 184, "".join(s + leg), "cirkeldiagram", lg=True)


# ============================================================ tabeller och diagram
def diagram(lv):
    def data(k=4, lo=2, hi=15):
        t, cats = ch(CATS)
        names = S.R.sample(cats, k)
        vals = [ri(lo, hi) for _ in range(k)]
        if len(set(vals)) < k:
            return None
        return t, list(zip(names, vals))

    def stapel_las():
        dd = data(4, 2, 18 if lv == 4 else 40)
        if not dd:
            return None
        t, dv = dd
        n, v = ch(dv)
        return M(stapel(dv, "antal elever") + "%s. Hur många elever svarade %s?" % (t, n), str(v), [str(v + 1), str(v - 1), str(max(x for _, x in dv)) if v != max(x for _, x in dv) else str(v + 2)],
                 "Stapeln för %s når till <b>%d</b>." % (n, v))

    def skillnad():
        dd = data(4, 2, 30)
        if not dd:
            return None
        t, dv = dd
        (a, x), (b, y) = S.R.sample(dv, 2)
        if x < y:
            (a, x), (b, y) = (b, y), (a, x)
        if lv == 4 or R0():
            return M(stapel(dv, "antal elever") + "Hur många fler valde %s än %s?" % (a, b), str(x - y), [str(x + y), str(x), str(x - y + 1)], "%d − %d = <b>%d</b>." % (x, y, x - y))
        tot = sum(v for _, v in dv)
        return M(stapel(dv, "antal elever") + "Hur många elever svarade sammanlagt?", str(tot), [str(tot + 1), str(tot - max(v for _, v in dv)), str(tot - 2)], "%s = <b>%d</b>." % (" + ".join(str(v) for _, v in dv), tot))

    def frekvens():
        t, cats = ch(CATS)
        names = S.R.sample(cats, 3)
        svar = [ch(names) for _ in range(ri(12, 20))]
        n = ch(names)
        c = svar.count(n)
        if c == 0:
            return None
        return M("Eleverna svarade: <i>%s</i>. Hur många svarade %s?" % (", ".join(svar), n), str(c), [str(c + 1), str(c - 1) if c > 1 else str(c + 2), str(len(svar) - c)],
                 "Räkna eller gör en frekvenstabell. %s förekommer <b>%d</b> gånger." % (cap(n), c))

    def linje_las():
        start = ri(0, 6)
        labs = MAN[start:start + 6]
        st = ch([2, 5, 10])
        vals = [ri(1, 9) * st for _ in range(6)]
        k = ri(0, 5)
        if R0():
            return M(linjediagram(vals, labs, "mm regn", st) + "Hur mycket regnade det i %s?" % {"jan": "januari", "feb": "februari", "mar": "mars", "apr": "april", "maj": "maj", "jun": "juni", "jul": "juli", "aug": "augusti", "sep": "september", "okt": "oktober", "nov": "november", "dec": "december"}[labs[k]],
                     "%d mm" % vals[k], ["%d mm" % x for x in (vals[k] + st, vals[k] - st if vals[k] > st else vals[k] + 2 * st, vals[(k + 1) % 6] if vals[(k + 1) % 6] != vals[k] else vals[k] + 3 * st)],
                     "Läs av punkten för %s mot den lodräta axeln: <b>%d mm</b>." % (labs[k], vals[k]))
        if len(set(vals)) < 6:
            return None
        big = R0()
        i = vals.index(max(vals) if big else min(vals))
        return M(linjediagram(vals, labs, "mm regn", st) + "Vilken månad regnade det %s?" % ("mest" if big else "minst"), labs[i], [l for j, l in enumerate(labs) if j != i],
                 "Den %s punkten är <b>%s</b>." % ("högsta" if big else "lägsta", labs[i]))

    def cirkel_las():
        t, cats = ch(CATS)
        names = S.R.sample(cats, 4)
        ps = ch([[50, 25, 15, 10], [40, 30, 20, 10], [35, 25, 25, 15], [45, 25, 20, 10], [30, 30, 25, 15], [60, 20, 10, 10]])
        ps = sh(ps)
        if len(set(ps)) < len(ps) and R0():
            return None
        parts = list(zip(names, ps))
        tot = ch([20, 40, 60, 80, 100, 200])
        n, p = ch(parts)
        if tot * p % 100:
            return None
        return M(cirkel(parts) + "%s: %d elever svarade. Hur många svarade %s?" % (t, tot, n), str(tot * p // 100), [str(p), str(tot * p // 100 + 2), str(tot - tot * p // 100)],
                 "%d %% av %d = <b>%d</b>." % (p, tot, tot * p // 100))

    def valj():
        opts = [("Du vill visa hur temperaturen ändras under en vecka. Vilket diagram passar bäst?", "linjediagram"),
                ("Du vill visa hur stor del av klassen som valde varje sport. Vilket diagram passar bäst?", "cirkeldiagram"),
                ("Du vill jämföra hur många elever som har hund, katt och kanin. Vilket diagram passar bäst?", "stapeldiagram"),
                ("Du vill visa hur lång en växt blir dag för dag. Vilket diagram passar bäst?", "linjediagram"),
                ("Du vill visa hur stor del av veckopengen som går till godis, sparande och spel. Vilket diagram passar bäst?", "cirkeldiagram"),
                ("Du vill jämföra antalet besökare på biblioteket varje veckodag. Vilket diagram passar bäst?", "stapeldiagram")]
        q, a = ch(opts)
        return M(q, a, [x for x in ("stapeldiagram", "linjediagram", "cirkeldiagram", "tabell utan rubriker") if x != a], "Ett <b>%s</b> passar bäst här." % a)

    if lv == 4:
        sets = [("Frekvenstabeller", [(frekvens, 20)]), ("Läs av stapeldiagram", [(stapel_las, 20)]), ("Jämför staplar", [(skillnad, 20)]),
                ("Linjediagram", [(linje_las, 20)]), ("Blandat", [(stapel_las, 7), (skillnad, 7), (frekvens, 6)])]
    else:
        sets = [("Stapeldiagram", [(stapel_las, 12), (skillnad, 8)]), ("Linjediagram", [(linje_las, 20)]), ("Cirkeldiagram", [(cirkel_las, 20)]),
                ("Välj diagram", [(valj, 6), (frekvens, 14)]), ("Blandat", [(skillnad, 7), (linje_las, 7), (cirkel_las, 6)])]
    return unit("tabeller-och-diagram", "S", "Tabeller och diagram: stapel-, linje- och cirkeldiagram" if lv >= 5 else "Tabeller och diagram: frekvenstabeller, stapel- och linjediagram", "Tabeller och diagram",
                "Tabeller och diagram för att beskriva resultat från undersökningar, till exempel frekvenstabeller, stapeldiagram, cirkeldiagram och linjediagram.",
                "Arbetsblad om tabeller och diagram för årskurs %d: frekvenstabeller, stapeldiagram, linjediagram%s. 100 uppgifter med facit." % (lv, ", cirkeldiagram och att välja rätt diagram" if lv >= 5 else ""),
                "Läs rubriken och axlarna först", "Vad visar diagrammet och vilka enheter används?", sets,
                ["En frekvenstabell visar hur många gånger varje svar förekommer. Räkna gärna med streck först.",
                 "I ett stapeldiagram jämför du antal. I ett linjediagram ser du hur något förändras över tid.",
                 "Ett cirkeldiagram visar hur stor del av helheten varje svar är, ofta i procent." if lv >= 5 else "Läs alltid rubriken och vad axlarna visar innan du läser av ett värde."],
                [("Hund 12, katt 7", ["Hur många fler valde hund?", "12 − 7"], "5"), ("Cirkeldiagram: 25 % av 40 elever", ["25 % = 1/4", "40 : 4"], "10 elever") if lv >= 5 else ("Linjediagram: regn i maj", ["Hitta maj", "Läs av mot axeln"], "värdet vid punkten")],
                [["Läser av vid fel stapel", "Följ stapeln rakt till axeln"], ["Tror att varje streck på axeln är 1", "Se hur axeln är graderad"],
                 ["Adderar när frågan är hur många fler", "Fler betyder skillnad: subtrahera"]],
                [("Vilket diagram ska jag välja?", "Stapeldiagram för att jämföra, linjediagram för förändring över tid och cirkeldiagram för delar av en helhet."),
                 ("Vad är frekvens?", "Hur många gånger något förekommer."),
                 ("Varför behövs rubrik?", "Utan rubrik och axelnamn vet man inte vad diagrammet visar.")])


# ============================================================ medelvärde, typvärde och median
def lagesmatt(lv):
    def lista(n, lo, hi):
        return [ri(lo, hi) for _ in range(n)]

    def medel():
        n = ch([3, 4, 5])
        m = ri(4, 30)
        xs = lista(n - 1, max(1, m - 10), m + 10)
        last = m * n - sum(xs)
        if last <= 0:
            return None
        xs.append(last)
        xs = sh(xs)
        return M("Vad är medelvärdet av %s?" % ", ".join(map(str, xs)), str(m), [str(sum(xs)), str(m + 1), str(sorted(xs)[n // 2]) if sorted(xs)[n // 2] != m else str(m - 1)],
                 "Summan är %d. %d : %d = <b>%d</b>." % (sum(xs), sum(xs), n, m))

    def typ():
        xs = lista(6, 1, 9)
        c = {x: xs.count(x) for x in xs}
        best = max(c.values())
        modes = [x for x in c if c[x] == best]
        if len(modes) != 1 or best == 1:
            return None
        t = modes[0]
        srt = sorted(xs)
        return M("Vad är typvärdet av %s?" % ", ".join(map(str, xs)), str(t), [str(x) for x in sh(set(xs) - {t})] + [str(max(xs))],
                 "Typvärdet är det värde som förekommer flest gånger: %d förekommer %d gånger. Svar: <b>%d</b>." % (t, best, t))

    def median():
        n = ch([5, 7]) if lv == 5 else ch([5, 6, 7])
        xs = lista(n, 1, 30)
        srt = sorted(xs)
        if n % 2:
            md = F(srt[n // 2])
        else:
            md = F(srt[n // 2 - 1] + srt[n // 2], 2)
        if len(set(xs)) < n:
            return None
        ans = d(md)
        w = [str(xs[n // 2]), d(F(sum(xs), n)) if (F(sum(xs), n) * 10).denominator == 1 else str(srt[0] + srt[-1]), str(srt[n // 2 + 1])]
        return M("Vad är medianen av %s?" % ", ".join(map(str, xs)), ans, w,
                 "Ordna talen: %s. %s Svar: <b>%s</b>." % (", ".join(map(str, srt)), "Talet i mitten är medianen." if n % 2 else "Två tal i mitten: medianen är medelvärdet av dem.", ans))

    def varians():
        xs = lista(5, 1, 40)
        return M("Vad är variationsbredden för %s?" % ", ".join(map(str, xs)), str(max(xs) - min(xs)), [str(max(xs)), str(sum(xs) // 5), str(max(xs) - min(xs) + 1)],
                 "Största minus minsta: %d − %d = <b>%d</b>." % (max(xs), min(xs), max(xs) - min(xs)))

    def text_():
        n = K().name()
        k = ri(0, 2)
        if k == 0:
            m, c = ri(5, 15), ch([3, 4, 5])
            xs = [ri(m - 4, m + 4) for _ in range(c - 1)]
            last = m * c - sum(xs)
            if last <= 0:
                return None
            xs.append(last)
            return M("%s fick %s poäng på %d prov. Vad är medelvärdet?" % (n, ", ".join(map(str, xs)), c), "%d poäng" % m, ["%d poäng" % x for x in (sum(xs), m + 1, max(xs))],
                     "(%s) : %d = %d : %d = <b>%d poäng</b>." % (" + ".join(map(str, xs)), c, sum(xs), c, m))
        if k == 1:
            m, c = ri(10, 25), ch([3, 4])
            xs = [ri(m - 5, m + 5) for _ in range(c)]
            s = sum(xs)
            if s % c:
                return None
            m = s // c
            want = m + ri(1, 3)
            need = want * (c + 1) - s
            return M("%s har sprungit %d varv i snitt per dag i %d dagar (%s). Hur många varv måste %s springa dag %d för att medelvärdet ska bli %d?" % (n, m, c, ", ".join(map(str, xs)), n, c + 1, want),
                     str(need), [str(want), str(need - 1), str(want * c - s)], "Totalt behövs %d · %d = %d. %d − %d = <b>%d</b>." % (want, c + 1, want * (c + 1), want * (c + 1), s, need))
        ts = [ri(-5, 12) for _ in range(5)] if lv == 6 else [ri(1, 15) for _ in range(5)]
        sg = lambda v: ("−%d" % -v) if v < 0 else str(v)
        if sum(ts) % 5:
            return None
        m = sum(ts) // 5
        return M("Temperaturen mättes fem dagar: %s °C. Vad var medeltemperaturen?" % ", ".join(sg(t) for t in ts), "%s °C" % sg(m),
                 ["%s °C" % sg(x) for x in (sum(ts), m + 1, sorted(ts)[2] if sorted(ts)[2] != m else m - 1)], "Summan är %s. %s : 5 = <b>%s °C</b>." % (sg(sum(ts)), sg(sum(ts)), sg(m)))

    sets = [("Medelvärde", [(medel, 20)]), ("Typvärde", [(typ, 20)]), ("Median", [(median, 20)]),
            ("Variationsbredd", [(varians, 12), (medel, 8)]), ("Lägesmått i vardagen", [(text_, 20)])]
    return unit("medelvarde-typvarde-och-median", "S", "Medelvärde, typvärde och median", "Medelvärde och median",
                "Lägesmåtten medelvärde, typvärde och median samt hur de kan användas i statistiska undersökningar.",
                "Arbetsblad om lägesmått för årskurs %d: medelvärde, typvärde, median, variationsbredd och lägesmått i vardagen. 100 uppgifter med facit." % lv,
                "Tre sätt att beskriva mitten", "Medelvärde, typvärde och median.", sets,
                ["Medelvärdet får du genom att lägga ihop alla värden och dela med antalet: (4 + 6 + 8) : 3 = 6.",
                 "Typvärdet är det värde som förekommer flest gånger. Medianen är värdet i mitten när värdena står i storleksordning.",
                 "Variationsbredden är skillnaden mellan det största och det minsta värdet. Den visar hur utspridda värdena är."],
                [("Medelvärdet av 7, 3, 8", ["7 + 3 + 8 = 18", "18 : 3"], "6"), ("Medianen av 9, 2, 5, 7, 1", ["Ordna: 1, 2, 5, 7, 9"], "5")],
                [["Medianen av 9, 2, 5, 7, 1 är 5 för att det står i mitten i listan", "Ordna först: 1, 2, 5, 7, 9. Medianen är 5"],
                 ["Medelvärde: delar med fel antal", "Dela med hur många värden det finns"], ["Typvärdet är det största värdet", "Typvärdet är det vanligaste värdet"]],
                [("När är medianen bättre än medelvärdet?", "När något värde är mycket större eller mindre än de andra. Medianen påverkas inte lika mycket."),
                 ("Kan det finnas flera typvärden?", "Ja, om flera värden förekommer lika många gånger."),
                 ("Måste medelvärdet vara ett heltal?", "Nej, det kan bli ett decimaltal, till exempel 5,5.")])


# ============================================================ sannolikhet
def pase_svg(counts):
    col = {"röda": "#e07a5f", "blå": "#6a9fd4", "gula": "#f2c94c", "gröna": "#81b29a"}
    s = ["<path d='M20 30 Q10 130 40 150 L170 150 Q200 130 190 30 Z' fill='#f3ead7' stroke='%s' stroke-width='2'/>" % INK]
    i = 0
    for c, n in counts:
        for _ in range(n):
            s.append("<circle cx='%d' cy='%d' r='9' fill='%s' stroke='%s'/>" % (42 + (i % 7) * 21, 50 + (i // 7) * 20, col[c], INK))
            i += 1
    return wrap(210, 160, "".join(s), "en påse med kulor")


SING = {"röda": "röd", "blå": "blå", "gula": "gul", "gröna": "grön"}


def sannolikhet(lv):
    def ord_():
        opts = [("Att du får 7 när du slår en vanlig tärning", "omöjligt"), ("Att du får ett tal mellan 1 och 6 med en vanlig tärning", "säkert"),
                ("Att du får krona när du singlar slant", "lika stor chans som att inte få det"), ("Att du får en sexa med en vanlig tärning", "liten chans"),
                ("Att det blir måndag efter söndag", "säkert"), ("Att du drar en röd kula ur en påse med 9 röda och 1 blå", "stor chans"),
                ("Att du drar en blå kula ur en påse med 9 röda och 1 blå", "liten chans"), ("Att du drar en grön kula ur en påse med bara röda och blå kulor", "omöjligt")]
        q, a = ch(opts)
        return M("Hur stor är chansen? <i>%s</i>." % q, a, [x for x in ("omöjligt", "liten chans", "lika stor chans som att inte få det", "stor chans", "säkert") if x != a][:3] if False else sh([x for x in ("omöjligt", "liten chans", "lika stor chans som att inte få det", "stor chans", "säkert") if x != a]),
                 "Svaret är <b>%s</b>." % a)

    def pase():
        cs = S.R.sample(["röda", "blå", "gula", "gröna"], 3)
        ns = S.R.sample(range(1, 9), 3)
        counts = list(zip(cs, ns))
        tot = sum(ns)
        c, n = ch(counts)
        if lv == 4:
            most = R0()
            a = (max if most else min)(counts, key=lambda t: t[1])[0]
            return M(pase_svg(counts) + "Du drar en kula utan att titta. %s" % ("Vilken färg får du troligast?" if most else "Vilken färg är det minst troligt att du får?"),
                     SING[a], [SING[x] for x, _ in counts if x != a] + ["alla färger är lika troliga"], "Det finns %s %s kulor, så <b>%s</b> är %s." % ("flest" if most else "minst", a, SING[a], "troligast" if most else "minst troligt"))
        return M(pase_svg(counts) + "Du drar en kula utan att titta. Hur stor är sannolikheten att den är %s?" % SING[c], fr(n, tot),
                 [fr(n, tot - n) if tot - n != n else fr(n, tot + 1), fr(1, tot), fr(tot - n, tot) if tot - n != n else fr(1, 3), fr(1, 3) if fr(n, tot) != fr(1, 3) else fr(1, 2)],
                 "%d av %d kulor är %s: <b>%s</b>." % (n, tot, c, fr(n, tot) if F(n, tot).denominator == tot else "%s = %s" % (fr(n, tot), fq(F(n, tot)))))

    def tarning():
        k = ri(0, 5)
        if k == 5:
            a, b = sorted(S.R.sample(range(1, 7), 2))
            return M("Du slår en vanlig tärning. Hur stor är sannolikheten att du får %d eller %d?" % (a, b), fr(2, 6) if lv < 6 else fr(1, 3), [fr(1, 6), fr(2, 12), fr(4, 6)],
                     "Två av sex utfall är gynnsamma: <b>%s</b>." % (fr(2, 6) if lv < 6 else fr(2, 6) + " = " + fr(1, 3)))
        if k == 0:
            n = ri(1, 6)
            return M("Du slår en vanlig tärning. Hur stor är sannolikheten att du får %d?" % n, fr(1, 6), [fr(n, 6) if n != 1 else fr(2, 6), fr(1, n) if n > 1 else fr(1, 2), fr(5, 6)], "Ett av sex lika troliga utfall: <b>1/6</b>.")
        if k == 1:
            return M("Du slår en vanlig tärning. Hur stor är sannolikheten att du får ett jämnt tal?", fr(1, 2) if lv == 6 else fr(3, 6), [fr(1, 6), fr(2, 6), fr(4, 6)],
                     "2, 4 och 6 är jämna: 3 av 6 = <b>%s</b>." % (fr(1, 2) if lv == 6 else fr(3, 6)))
        if k == 2:
            n = ri(1, 4)
            g = 6 - n
            return M("Du slår en vanlig tärning. Hur stor är sannolikheten att du får mer än %d?" % n, fr(g, 6), [fr(n, 6), fr(g + 1, 6), fr(1, 6)] if g != n else [fr(g + 1, 6), fr(1, 6), fr(g - 1, 6)],
                     "Talen %s: %d av 6: <b>%s</b>." % (", ".join(str(i) for i in range(n + 1, 7)), g, fr(g, 6)))
        if k == 3:
            return M("Du singlar slant. Hur stor är sannolikheten att du får klave?", fr(1, 2), [fr(1, 3), fr(1, 4), "1"], "Två lika troliga utfall, krona och klave: <b>1/2</b>.")
        n = ri(2, 5)
        return M("Hur stor är sannolikheten att få %d eller lägre när du slår en tärning?" % n, fr(n, 6), [fr(n, 5), fr(6 - n, 6) if 6 - n != n else fr(n + 1, 6), fr(1, n)],
                 "Talen 1–%d: %d av 6 = <b>%s</b>." % (n, n, fr(n, 6)))

    def snurra():
        n = ch([3, 4, 5, 6, 8, 10, 12])
        k = ri(1, n - 1)
        s = []
        cx, cy, r = 70, 70, 60
        for i in range(n):
            a0, a1 = -90 + 360.0 * i / n, -90 + 360.0 * (i + 1) / n
            s.append("<path d='M%d %d L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='1.5'/>" % (
                cx, cy, cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)), r, r, cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)),
                "#e07a5f" if i < k else "#ffffff", INK))
        s.append("<circle cx='%d' cy='%d' r='4' fill='%s'/>" % (cx, cy, INK))
        pic = wrap(140, 140, "".join(s), "lyckohjul i %d lika delar" % n)
        return M(pic + "Lyckohjulet har %d lika stora delar. Hur stor är sannolikheten att det stannar på rött?" % n, fr(k, n), [fr(n - k, n) if n - k != k else fr(k, n + 1), fr(1, n) if k != 1 else fr(2, n), fr(k, n - k) if n - k != k else fr(1, 2)],
                 "%d av %d delar är röda: <b>%s</b>." % (k, n, fr(k, n)))

    def forsok():
        p = ch([F(1, 2), F(1, 4), F(1, 5), F(1, 10)])
        n = ch([x for x in (20, 30, 40, 50, 60, 80, 100, 120, 200, 300) if (x * p).denominator == 1])
        e = int(n * p)
        thing = {F(1, 2): ("singlar slant", "krona"), F(1, 4): ("snurrar ett lyckohjul med fyra lika delar", "blått"), F(1, 5): ("drar en kula ur en påse med 1 röd och 4 vita", "röd"), F(1, 10): ("drar en lapp ur en burk med lapparna 1–10", "lappen 7")}[p]
        return M("Du %s %d gånger. Ungefär hur många gånger kan du vänta dig att få %s?" % (thing[0], n, thing[1]), "ungefär %d gånger" % e,
                 ["ungefär %d gånger" % x for x in (n, e * 2, e // 2 if e // 2 else 1, n - e) if x != e], "Sannolikheten är %s. %s av %d = <b>ungefär %d gånger</b>." % (fq(p), fq(p), n, e))

    def chans_risk():
        a, b = ri(1, 9), ri(1, 9)
        c, dd = ri(1, 9), ri(1, 9)
        if F(a, a + b) == F(c, c + dd):
            return None
        best = "påse A" if F(a, a + b) > F(c, c + dd) else "påse B"
        return M("Du vinner om du drar en röd kula. Påse A har %d röda och %d blå. Påse B har %d röda och %d blå. Vilken påse ger störst chans att vinna?" % (a, b, c, dd),
                 best, ["påse B" if best == "påse A" else "påse A", "lika stor chans", "den med flest kulor"], "A: %s, B: %s. Störst chans ger <b>%s</b>." % (fr(a, a + b), fr(c, c + dd), best))

    if lv == 4:
        sets = [("Chans och risk", [(ord_, 8), (pase, 12)]), ("Dra en kula", [(pase, 20)]), ("Tärning och slant", [(tarning, 20)]),
                ("Lyckohjul", [(snurra, 20)]), ("Vilken påse är bäst?", [(chans_risk, 20)])]
    else:
        sets = [("Sannolikhet som bråk", [(pase, 20)]), ("Tärning och slant", [(tarning, 20)]), ("Lyckohjul", [(snurra, 20)]),
                ("Förutsäga resultat", [(forsok, 20)]), ("Jämför chanser", [(chans_risk, 14), (ord_, 6)])]
    return unit("sannolikhet", "S", "Sannolikhet: chans, risk och sannolikhet som bråk", "Sannolikhet",
                "Sannolikhet, chans och risk grundat på observationer, simuleringar eller statistiskt material från vardagliga situationer.",
                "Arbetsblad om sannolikhet för årskurs %d: chans och risk, dra kulor, tärning och slant, lyckohjul%s. 100 uppgifter med facit." % (lv, ", förutsäga resultat och jämföra chanser" if lv >= 5 else " och jämföra chanser"),
                "Gynnsamma av alla utfall", "Sannolikhet = antal gynnsamma / antal möjliga", sets,
                ["Sannolikhet beskriver hur troligt något är. Det kan vara omöjligt, ha liten chans, stor chans eller vara säkert.",
                 "När alla utfall är lika troliga är sannolikheten antal gynnsamma utfall delat med antal möjliga utfall. Att få en femma på en tärning: 1/6.",
                 "Ju större sannolikhet, desto oftare händer det när man gör många försök. Slår du en tärning 60 gånger kan du vänta dig ungefär 10 femmor."],
                [("Påse: 3 röda, 5 blå", ["8 kulor totalt", "3 är röda"], "3/8"), ("Slant 40 gånger", ["Sannolikhet för krona 1/2", "1/2 av 40"], "ungefär 20 gånger krona")],
                [["Tror att en sexa är svårare att få än en trea", "Alla tal på tärningen är lika troliga"], ["3 röda och 5 blå ger sannolikheten 3/5", "Dela med alla kulor: 3/8"],
                 ["Tror att 20 krona av 40 kast alltid blir exakt", "Det blir ungefär så, inte säkert"]],
                [("Vad är ett utfall?", "Ett möjligt resultat, till exempel 4 när du slår en tärning."),
                 ("Kan sannolikheten vara större än 1?", "Nej. 1 betyder säkert och 0 betyder omöjligt."),
                 ("Vad är skillnaden mellan chans och risk?", "Chans används om något bra, risk om något dåligt. Båda handlar om sannolikhet.")])


# ============================================================ kombinatorik
def kombinatorik(lv):
    def klader():
        a, b = ri(2, 5), ri(2, 5)
        c = ri(2, 3) if lv == 6 and R0() else 1
        x, y = ch([("tröjor", "byxor"), ("t-shirts", "shorts"), ("mössor", "halsdukar"), ("klänningar", "koftor")])
        if c == 1:
            return M("Du har %d %s och %d %s. Hur många olika sätt kan du klä dig på?" % (a, x, b, y), str(a * b), [str(a + b), str(a * b + 1), str(a * b - 1)],
                     "Varje plagg kan kombineras med varje annat: %d · %d = <b>%d</b>." % (a, b, a * b))
        if c > 1:
            return M("Du har %d tröjor, %d byxor och %d par skor. Hur många olika sätt kan du klä dig på?" % (a, b, c), str(a * b * c), [str(a + b + c), str(a * b), str(a * b * c + 1)],
                     "%d · %d · %d = <b>%d</b>." % (a, b, c, a * b * c))
        return M("Du har %d tröjor och %d byxor. Hur många olika sätt kan du klä dig på?" % (a, b), str(a * b), [str(a + b), str(a * b + 1), str(a * b - 1)],
                 "Varje tröja kan kombineras med varje byxa: %d · %d = <b>%d</b>." % (a, b, a * b))

    def meny():
        a, b, c = ri(2, 4), ri(2, 5), ri(2, 3)
        return M("På en restaurang finns %d förrätter, %d varmrätter och %d efterrätter. Hur många olika middagar med en av varje kan du välja?" % (a, b, c), str(a * b * c),
                 [str(a + b + c), str(a * b + c), str(a * b * c * 2)], "%d · %d · %d = <b>%d</b>." % (a, b, c, a * b * c))

    def ordning():
        n = ri(2, 5)
        f = math.factorial(n)
        return M(ch(["På hur många sätt kan %d personer ställa sig i en kö?", "På hur många sätt kan %d olika böcker ställas i en rad i bokhyllan?", "På hur många sätt kan %d löpare komma i mål om ingen kommer samtidigt?"]) % n, str(f), [str(n * n), str(n + n), str(f // n) if f // n != n else str(f + 1)],
                 "%s = <b>%d</b>." % (" · ".join(str(i) for i in range(n, 0, -1)), f))

    def siffror():
        ds = S.R.sample(range(1, 10), 3)
        if R0():
            return M("Hur många olika tresiffriga tal kan du bilda med siffrorna %s, om varje siffra används en gång?" % ", ".join(map(str, ds)), "6", ["3", "9", "27"],
                     "3 val för första platsen, 2 för andra, 1 för tredje: 3 · 2 · 1 = <b>6</b>.")
        return M("Hur många olika tvåsiffriga tal kan du bilda med siffrorna %s, om varje siffra används högst en gång?" % ", ".join(map(str, ds)), "6", ["3", "9", "5"],
                 "3 val för tiotalssiffran och 2 för entalssiffran: 3 · 2 = <b>6</b>.")

    def handslag():
        n = ri(3, 8)
        h = n * (n - 1) // 2
        return M(ch(["%d kompisar hälsar på varandra. Alla tar alla i hand en gång. Hur många handslag blir det?", "%d spelare i ett lag gör high five med varandra, alla med alla en gång. Hur många high fives blir det?"]) % n, str(h), [str(n * (n - 1)), str(n * n), str(h + 1)],
                 "%s = <b>%d</b>." % (" + ".join(str(i) for i in range(n - 1, 0, -1)), h))

    def matcher():
        n = ri(3, 8)
        h = n * (n - 1) // 2
        return M(ch(["%d lag spelar en serie där alla möter alla en gång. Hur många matcher blir det?", "%d elever spelar pingis. Alla spelar en match mot alla andra. Hur många matcher blir det?"]) % n, str(h), [str(n * (n - 1)), str(n), str(h - 1), str(h + 1)],
                 "Varje lag möter %d lag: %d · %d = %d, men varje match räknas då två gånger. %d : 2 = <b>%d</b>." % (n - 1, n, n - 1, n * (n - 1), n * (n - 1), h))

    def kod():
        k = ri(2, 3)
        n = ri(2, 6) if k == 3 else ri(2, 10)
        return M(ch(["En kod har %d siffror. Varje siffra kan vara %s. Hur många olika koder finns det?", "Ett cykellås har %d hjul. Varje hjul kan visa %s. Hur många olika koder finns det?"]) % (k, "0–9" if n == 10 else "1–%d" % n), num(n ** k), [num(n * k), num(n ** k - 1), num(n + k)],
                 "%s = <b>%s</b>." % (" · ".join([str(n)] * k), num(n ** k)))

    sets = [("Kombinera kläder", [(klader, 20)]), ("Menyer och val", [(meny, 14), (kod, 6)]), ("Ordning", [(ordning, 6), (siffror, 4), (kod, 10)]),
            ("Handslag och matcher", [(handslag, 6), (matcher, 6), (klader, 8)]), ("Blandat", [(kod, 6), (klader, 8), (siffror, 6)])]
    return unit("kombinatorik", "S", "Kombinatorik: kombinationer och ordningar", "Kombinatorik",
                "Enkel kombinatorik i konkreta situationer. Systematiska metoder för att räkna kombinationer.",
                "Arbetsblad om kombinatorik för årskurs %d: kombinera kläder, menyer, koder, ordningar, handslag och matcher. 100 uppgifter med facit." % lv,
                "Multiplicera antalet val", "3 tröjor och 4 byxor ger 3 · 4 = 12 sätt.", sets,
                ["När du ska välja en sak från varje grupp multiplicerar du antalet val: 3 tröjor och 4 byxor ger 3 · 4 = 12 kombinationer.",
                 "När ordningen spelar roll minskar valen för varje plats: 4 personer i en kö kan stå på 4 · 3 · 2 · 1 = 24 sätt.",
                 "Rita ett träddiagram eller gör en lista för att räkna systematiskt."],
                [("2 förrätter och 3 varmrätter", ["2 · 3"], "6 middagar"), ("5 lag där alla möter alla", ["5 · 4 = 20", "20 : 2"], "10 matcher")],
                [["3 tröjor och 4 byxor = 7 sätt", "Multiplicera: 12"], ["Räknar varje handslag två gånger", "Dela med 2"],
                 ["4 personer i en kö = 16 sätt", "4 · 3 · 2 · 1 = 24"]],
                [("Vad är ett träddiagram?", "En bild där varje gren är ett val. Antalet grenar längst ut är antalet kombinationer."),
                 ("När ska jag dela med 2?", "När ordningen inte spelar roll och varje par annars räknas två gånger, som vid handslag."),
                 ("Vad betyder att ordningen spelar roll?", "Att 12 och 21 räknas som olika, eller att Ali först och Saga sist är något annat än tvärtom.")])


# ============================================================ problemlösning
def problemlosning(lv):
    def tvasteg():
        n, g = K().next()
        k = ri(0, 3)
        if k == 0:
            p, m, c = ri(15, 60), ri(2, 6), ri(10, 50)
            have = ch([200, 300, 500])
            r = have - p * m - c
            if r < 0:
                return None
            return M("%s har %s. %s köper %d biljetter för %d kr styck och en dricka för %d kr. Hur mycket har %s kvar?" % (n, kr(have), cap("hon" if g == "f" else "han"), m, p, c, "hon" if g == "f" else "han"),
                     kr(r), [kr(x) for x in (have - p - c, have - p * m, p * m + c)], "%d − %d · %d − %d = <b>%s</b>." % (have, m, p, c, kr(r)))
        if k == 1:
            a, b = ri(120, 480), ri(40, 160)
            return M("En bokhandel har %d böcker. De säljer %d på måndagen och dubbelt så många på tisdagen. Hur många böcker är kvar?" % (a + 3 * b, b), num(a), [num(a + b), num(a + 2 * b), num(a - b) if a > b else num(a + 10)],
                     "%d + 2 · %d = %d sålda. %d − %d = <b>%s</b>." % (b, b, 3 * b, a + 3 * b, 3 * b, num(a)))
        if k == 2:
            x = ri(12, 60)
            y = x + ri(5, 30)
            return M("Två syskon har tillsammans %d kr. Det ena har %d kr mer än det andra. Hur mycket har det som har minst?" % (x + y, y - x), kr(x), [kr((x + y) // 2), kr(y), kr(x + y - (y - x))],
                     "Ta bort skillnaden: %d − %d = %d. Dela lika: %d : 2 = <b>%s</b>." % (x + y, y - x, 2 * x, 2 * x, kr(x)))
        a = ri(3, 8)
        b = ri(3, 8)
        return M("I en hage finns höns och kaniner. Det finns %d djur och %d ben. Hur många kaniner finns det?" % (a + b, 2 * a + 4 * b), str(b), [str(a), str(a + b), str((2 * a + 4 * b) // 4)] if a != b else [str(a + 1), str(a + b), str(b - 1)],
                 "Om alla vore höns blir det %d ben. %d − %d = %d extra ben, och varje kanin har 2 extra: %d : 2 = <b>%d</b>." % (2 * (a + b), 2 * a + 4 * b, 2 * (a + b), 2 * b, 2 * b, b))

    def baklanges():
        n, g = K().next()
        start = ri(40, 200)
        sp, go = ri(10, 40), ri(5, 30)
        mid = start - sp
        end = mid * 2 - go if lv >= 5 and R0() else mid + go
        dub = end != mid + go
        if dub:
            txt = "%s hade några kronor. %s köpte en bok för %d kr. Sedan fick %s dubbelt så mycket som %s hade kvar i present och köpte till sist en glass för %d kr. Nu har %s %d kr. Hur mycket hade %s från början?" % (
                n, cap("hon" if g == "f" else "han"), sp, "hon" if g == "f" else "han", "hon" if g == "f" else "han", go, "hon" if g == "f" else "han", end + mid if False else end, "hon" if g == "f" else "han")
            end = mid * 3 - go
            txt = txt.replace(" %d kr. Hur" % (mid * 2 - go), " %d kr. Hur" % end)
            return None
        return M("%s hade några kronor. %s köpte en bok för %d kr och fick sedan %d kr av mormor. Nu har %s %d kr. Hur mycket hade %s från början?" % (
            n, cap("hon" if g == "f" else "han"), sp, go, "hon" if g == "f" else "han", end, "hon" if g == "f" else "han"), kr(start),
            [kr(x) for x in (end + sp + go, end - sp + go, end)], "Räkna baklänges: %d − %d + %d = <b>%s</b>." % (end, go, sp, kr(start)))

    def gissa():
        a = ri(2, 30)
        b = ri(2, 30)
        if a == b:
            return None
        s, p = a + b, a * b
        lo_, hi_ = min(a, b), max(a, b)
        return M("Två tal har summan %d och produkten %d. Vilka är talen?" % (s, p), "%d och %d" % (lo_, hi_),
                 ["%d och %d" % (lo_ + 1, hi_ - 1), "%d och %d" % (lo_ - 1, hi_ + 1) if lo_ > 1 else "%d och %d" % (lo_ + 2, hi_ - 2), "%d och %d" % (lo_, s)],
                 "Pröva systematiskt: %d + %d = %d och %d · %d = %d. Svar: <b>%d och %d</b>." % (lo_, hi_, s, lo_, hi_, p, lo_, hi_))

    def monstret():
        k = ri(3, 6)
        v = ri(5, 12)
        return M("En trappa byggs av tändstickor. Ett steg kräver %d stickor och varje nytt steg kräver %d till. Hur många stickor behövs för %d steg?" % (k, k - 1, v),
                 str(k + (k - 1) * (v - 1)), [str(k * v), str(k + (k - 1) * v), str((k - 1) * v)], "%d + %d · %d = <b>%d</b>." % (k, k - 1, v - 1, k + (k - 1) * (v - 1)))

    def rimlighet():
        n = K().name()
        p = ri(15, 45)
        m = ri(6, 14)
        tot = p * m
        cands = [tot, tot * 10, tot // 10, tot + 1000]
        return M("%s köper %d paket kakor för %d kr styck. Vilket svar är rimligt?" % (n, m, p), kr(tot), [kr(x) for x in cands[1:]],
                 "Överslag: %d · %d ≈ %d. Bara <b>%s</b> är rimligt." % (m, p, m * (p // 10 * 10 + 10 if p % 10 >= 5 else p // 10 * 10), kr(tot)))

    def rakna_rum():
        a, b = ri(3, 8), ri(3, 8)
        p = ch([150, 200, 250, 300])
        return M("Ett golv är %d m långt och %d m brett. Golvbrädor kostar %d kr per m². Vad kostar brädorna till hela golvet?" % (a, b, p), kr(a * b * p),
                 [kr(2 * (a + b) * p), kr((a + b) * p), kr(a * b * p // 10)], "Area: %d · %d = %d m². %d · %d = <b>%s</b>." % (a, b, a * b, a * b, p, kr(a * b * p)))

    sets = [("Problem i flera steg", [(tvasteg, 20)]), ("Räkna baklänges", [(baklanges, 20)]), ("Pröva systematiskt", [(gissa, 20)]),
            ("Hitta mönstret", [(monstret, 12), (rimlighet, 8)]), ("Vardagsproblem", [(rakna_rum, 10), (tvasteg, 5), (rimlighet, 5)])]
    return unit("problemlosning", "P", "Problemlösning: strategier och problem i flera steg", "Problemlösning",
                "Strategier för problemlösning i vardagliga situationer. Formulering av frågeställningar och val av metod och räknesätt.",
                "Arbetsblad om problemlösning för årskurs %d: problem i flera steg, räkna baklänges, pröva systematiskt, hitta mönster och bedöm rimlighet. 100 uppgifter med facit." % lv,
                "Förstå, planera, lös, kontrollera", "Välj en strategi: rita, pröva, räkna baklänges.", sets,
                ["Läs problemet noga. Vad vet du och vad ska du ta reda på? Skriv upp talen.",
                 "Välj en strategi: rita en bild, gör en tabell, pröva systematiskt, räkna baklänges eller leta efter ett mönster.",
                 "Kontrollera att svaret är rimligt och att du har svarat på frågan, med rätt enhet."],
                [("Två syskon har 80 kr tillsammans. Det ena har 20 kr mer", ["80 − 20 = 60", "60 : 2 = 30", "30 och 50"], "30 kr och 50 kr"),
                 ("Höns och kaniner: 10 djur och 28 ben", ["Om alla vore höns: 20 ben", "8 extra ben, 2 per kanin"], "4 kaniner")],
                [["Räknar bara första steget", "Läs frågan igen: vad ska du ta reda på?"], ["Delar 80 med 2 direkt", "Ta först bort skillnaden"],
                 ["Svarar utan enhet", "Skriv kr, cm eller vad det gäller"]],
                [("Vad gör jag om jag kör fast?", "Pröva en annan strategi, till exempel att rita eller pröva med små tal."),
                 ("Måste jag skriva hur jag tänkte?", "Det är bra. Då kan du och andra se om metoden stämmer."),
                 ("Hur vet jag att svaret är rimligt?", "Gör ett överslag och tänk efter om svaret passar i situationen.")])


UNITS = {"tabeller-och-diagram": diagram, "medelvarde-typvarde-och-median": lagesmatt, "sannolikhet": sannolikhet,
         "kombinatorik": kombinatorik, "problemlosning": problemlosning}
