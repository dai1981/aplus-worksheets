# -*- coding: utf-8 -*-
"""Sverige årskurs 7–9: samband och förändring（procent, förändringsfaktor, proportionalitet, funktioner, räta linjen, grafer, ränta och lån, exponentiell förändring）"""
import math
from fractions import Fraction as F
from se_h import (gen, MQ, lista, ri, ch, sh, cap, fr, fq, d, par, sg, M, MN, rd, sup, unit, tab, K, num, kr, NB, MIN, coin, expr, lin, kosy, kurve, RED, BLUE, GREEN)


def nz(a, b):
    while True:
        v = ri(a, b)
        if v:
            return v


def pc(x):
    return d(x) + NB + "%"


def krd(x):
    """belopp: heltal eller två decimaler"""
    x = F(x)
    return (d(x) if x.denominator == 1 else rd(x, 2)) + NB + "kr"


# ============================================================ procent (åk 7)
def procent(lv):
    def av():
        p = ch([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 12, 35, 8, 3])
        t = ri(2, 60) * ch([10, 20, 40, 100])
        v = F(p * t, 100)
        return MN("Hur mycket är %s av %s?" % (pc(p), num(t)), v, [F(t, p) if t % p == 0 else v + 10, v * 10, t - v], "%s = %s. %s · %s = <b>%s</b>." % (pc(p), d(F(p, 100)), d(F(p, 100)), num(t), d(v)))

    def andel():
        t = ch([20, 25, 40, 50, 80, 200, 250, 400, 500])
        dl = ri(1, t - 1)
        p = F(dl * 100, t)
        if p.denominator != 1:
            return None
        nm = K().name()
        k = ri(0, 2)
        if k == 0:
            q = "I en klass med %d elever %s. Hur stor andel är det i procent?" % (t, "har %d elever cykel" % dl) if t <= 40 else "Av %d tillfrågade svarade %d ja. Hur många procent svarade ja?" % (t, dl)
        elif k == 1:
            q = "%s fick %d poäng av %d möjliga på ett prov. Hur många procent är det?" % (nm, dl, t)
        else:
            q = "Ett lag vann %d av %d matcher. Hur många procent av matcherna vann laget?" % (dl, t)
        return MN(q, p, [dl, F(t, dl) if F(t, dl).denominator == 1 and F(t, dl) != p else p + 5, 100 - p], "Andelen är %d/%d = %s = <b>%s %%</b>." % (dl, t, d(F(dl, t)), d(p)), "%")

    def omvandla():
        P = [(F(1, 2), "50"), (F(1, 4), "25"), (F(3, 4), "75"), (F(1, 5), "20"), (F(2, 5), "40"), (F(3, 5), "60"), (F(4, 5), "80"), (F(1, 10), "10"),
             (F(3, 10), "30"), (F(7, 10), "70"), (F(9, 10), "90"), (F(1, 20), "5"), (F(3, 20), "15"), (F(1, 8), "12,5"), (F(3, 8), "37,5"), (F(1, 25), "4"), (F(7, 20), "35"), (F(1, 100), "1"), (F(13, 20), "65"), (F(9, 20), "45")]
        f, p = ch(P)
        k = ri(0, 2)
        if k == 0:
            return M("Skriv %s i procent." % fq(f), p + NB + "%", [d(f * 10) + NB + "%", d(f) + NB + "%", str(f.denominator) + NB + "%" if str(f.denominator) != p else "1" + NB + "%"], "%s = %s = <b>%s %%</b>." % (fq(f), d(f), p))
        if k == 1:
            return M("Skriv %s %% som decimaltal." % p, d(f), [p, d(f * 10), d(f / 10)], "%s %% = %s/100 = <b>%s</b>." % (p, p, d(f)))
        return M("Skriv %s %% som ett bråk i enklaste form." % p, fq(f), [fr(int(p) if "," not in p else 125, 10), fq(f + F(1, 10)), fr(f.denominator, 100) if F(f.denominator, 100) != f else fq(f / 2)], "%s %% = %s/100 = <b>%s</b>." % (p, p, fq(f))) if "," not in p else None

    def rabatt():
        p = ch([10, 15, 20, 25, 30, 40, 50, 60, 70])
        pris = ri(4, 90) * 10
        r = F(p * pris, 100)
        if r.denominator != 1:
            return None
        k = ri(0, 1)
        if k == 0:
            return MN("En jacka kostar %s. Den säljs med %d %% rabatt. Vad kostar jackan nu?" % (kr(pris), p), pris - r, [r, pris - p, pris + r], "Rabatten är %s %% av %d = %s kr. %d − %s = <b>%s kr</b>." % (p, pris, d(r), pris, d(r), d(pris - r)), "kr")
        return MN("Priset på en cykel på %s höjs med %d %%. Vad kostar cykeln nu?" % (kr(pris), p), pris + r, [r, pris + p, pris - r], "Höjningen är %s kr. %d + %s = <b>%s kr</b>." % (d(r), pris, d(r), d(pris + r)), "kr")

    def okning():
        a = ri(2, 40) * 10
        p = ch([5, 10, 20, 25, 30, 40, 50, 60, 75, 100])
        b = a + a * p // 100 if a * p % 100 == 0 else None
        if b is None:
            return None
        if coin():
            return MN("Priset ökade från %s till %s. Hur många procent var ökningen?" % (kr(a), kr(b)), p, [b - a, F((b - a) * 100, b), F(b * 100, a)], "Ökningen är %d kr. %d/%d = %s = <b>%d %%</b>." % (b - a, b - a, a, d(F(p, 100)), p), "%")
        return MN("Priset sänktes från %s till %s. Hur många procent var sänkningen?" % (kr(b), kr(a)), F((b - a) * 100, b), [p, b - a, F(a * 100, b)], "Sänkningen är %d kr av %d kr: %s = <b>%s %%</b>." % (b - a, b, rd(F(b - a, b), 3), rd(F((b - a) * 100, b), 1)), "%") if F((b - a) * 100, b).denominator in (1, 2, 4, 5, 10) else None

    sets = [("Procent av ett tal", [(av, 20)]), ("Hur många procent?", [(andel, 20)]), ("Bråk, decimaltal och procent", [(omvandla, 20)]),
            ("Rabatt och prishöjning", [(rabatt, 20)]), ("Procentuell förändring", [(okning, 20)])]
    return unit("procent", "F", "Procent: andel, rabatt och procentuell förändring", "Procent",
                "Procent för att uttrycka förändring och förändringsfaktor samt beräkningar med procent i vardagliga situationer. Andelar uttryckta i bråk, decimaltal och procent.",
                "Arbetsblad om procent för årskurs 7: procent av ett tal, hur många procent, bråk och decimaltal i procent, rabatt och procentuell förändring. 100 uppgifter med facit.",
                "Procent betyder hundradelar", "Delen delat med det hela ger andelen.", sets,
                ["Procent betyder hundradelar: 25 % = 25/100 = 0,25.",
                 "Procent av ett tal: multiplicera med decimaltalet. 30 % av 400 = 0,30 · 400 = 120.",
                 "Hur många procent: dela delen med det hela. 12 av 48 = 12/48 = 0,25 = 25 %. Vid förändring jämför du alltid med det ursprungliga värdet."],
                [("30 % av 400", ["0,30 · 400"], "120"), ("Priset ökar från 80 kr till 100 kr", ["Ökningen 20 kr", "20/80 = 0,25"], "25 %")],
                [["12 av 48 är 12 %", "12/48 = 0,25 = 25 %"], ["Ökningen 80 → 100 är 20 %", "Jämför med 80: 20/80 = 25 %"], ["5 % = 0,5", "5 % = 0,05"]],
                [("Vad är skillnaden mellan andel och procent?", "Andelen kan skrivas som bråk, decimaltal eller procent. Procent är andelen i hundradelar."),
                 ("Kan det bli mer än 100 %?", "Ja, en ökning på 150 % betyder att det nya värdet är 2,5 gånger så stort."), ("Vad jämför jag med vid förändring?", "Alltid det gamla värdet, det som fanns före förändringen.")])


# ============================================================ procent och förändringsfaktor (åk 8)
def forandring(lv):
    def ff():
        p = ch([2, 3, 4, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75, 100, 150])
        if coin():
            return M("Vilken förändringsfaktor motsvarar en ökning med %d %%?" % p, d(1 + F(p, 100)), [d(F(p, 100)), d(1 - F(p, 100)) if p < 100 else d(F(p, 10)), d(1 + F(p, 10)) if p < 10 else d(F(100 + p, 10))], "100 %% + %d %% = %d %% = <b>%s</b>." % (p, 100 + p, d(1 + F(p, 100))))
        if p >= 100:
            return None
        return M("Vilken förändringsfaktor motsvarar en minskning med %d %%?" % p, d(1 - F(p, 100)), [d(F(p, 100)), d(1 + F(p, 100)), d(1 - F(p, 10)) if p < 10 else d(F(100 - p, 10))], "100 %% − %d %% = %d %% = <b>%s</b>." % (p, 100 - p, d(1 - F(p, 100))))

    def anvand():
        p = ch([5, 10, 12, 15, 20, 25, 30, 35, 40])
        t = ri(4, 80) * 25
        up = coin()
        f = 1 + F(p, 100) if up else 1 - F(p, 100)
        v = t * f
        thing = ch([("En lägenhet hyrs ut för %s i månaden." % kr(t), "Hyran höjs", "sänks"), ("En mobil kostar %s." % kr(t), "Priset höjs", "sänks"), ("En förening har %s i kassan." % kr(t), "Kassan ökar", "minskar")])
        verb = thing[1] if up else thing[1].replace("höjs", "sänks").replace("ökar", "minskar")
        return MN("%s %s med %d %%. Hur mycket blir det? Använd förändringsfaktorn." % (thing[0], verb, p), v, [t * F(p, 100), t * (1 - F(p, 100)) if up else t * (1 + F(p, 100)), t + p if up else t - p], "Förändringsfaktorn är %s. %s · %s = <b>%s kr</b>." % (d(f), num(t), d(f), d(v)), "kr")

    def tolka():
        f = ch([F(103, 100), F(108, 100), F(112, 100), F(125, 100), F(15, 10), F(2), F(97, 100), F(9, 10), F(85, 100), F(6, 10), F(75, 100), F(4, 10), F(105, 100), F(92, 100), F(118, 100), F(65, 100), F(135, 100), F(98, 100), F(7, 10), F(3, 10)])
        p = (f - 1) * 100
        r = ("en ökning med %s %%" % d(p)) if p > 0 else ("en minskning med %s %%" % d(-p))
        w = [("en ökning med %s %%" % d(f * 100)), ("en minskning med %s %%" % d(p)) if p > 0 else ("en ökning med %s %%" % d(-p)), ("en minskning med %s %%" % d(f * 100)) if f < 1 else ("en ökning med %s %%" % d(p / 10 if p >= 10 else p * 10))]
        return M("Ett värde multipliceras med förändringsfaktorn %s. Vad betyder det?" % d(f), cap(r), [cap(x) for x in w], "%s = %s %%. Jämfört med 100 %% är det <b>%s</b>." % (d(f), d(f * 100), r))

    def ursprung():
        p = ch([10, 20, 25, 30, 40, 50, 60, 75])
        o = ri(4, 60) * 20
        if coin():
            o = ri(20, 150) * 100
            n = o * (1 - F(p, 100))
            return MN("Efter %d %% rabatt kostar en soffa %s. Vad kostade den från början?" % (p, krd(n)), o, [n * (1 + F(p, 100)), n + p, n / F(p, 100) if (n / F(p, 100)).denominator == 1 else n + 100], "Ursprungspriset · %s = %s. %s/%s = <b>%s kr</b>." % (d(1 - F(p, 100)), d(n), d(n), d(1 - F(p, 100)), num(o)), "kr")
        n = o * (1 + F(p, 100))
        return MN("Efter en höjning med %d %% kostar en konsert %s. Vad kostade den innan?" % (p, krd(n)), o, [n * (1 - F(p, 100)), n - p, n * F(p, 100)], "Det gamla priset · %s = %s. %s/%s = <b>%s kr</b>." % (d(1 + F(p, 100)), d(n), d(n), d(1 + F(p, 100)), num(o)), "kr")

    def enheter():
        a = ri(5, 40)
        b = a + nz(-8, 12)
        if b <= 0 or a == b:
            return None
        k = ri(0, 2)
        if k == 0:
            diff = b - a
            pp = F(diff * 100, a)
            return M("Räntan på ett lån ändras från %d %% till %d %%. Hur många procentenheter ändras räntan?" % (a, b), "%s procentenheter" % d(abs(diff)), ["%s procentenheter" % rd(abs(pp), 1), "%s procentenheter" % d(a + b), "%s procentenheter" % d(abs(diff) * 10)], "%d − %d = %s. Skillnaden mellan två procentsatser mäts i <b>procentenheter</b>: %s." % (max(a, b), min(a, b), d(abs(diff)), d(abs(diff))))
        if k == 1:
            pp = F((b - a) * 100, a)
            if pp.denominator not in (1, 2, 4, 5, 10):
                return None
            return M("Ett parti fick %d %% av rösterna i ett val och %d %% i nästa. Hur många procent ändrades partiets andel?" % (a, b), "%s %%" % d(abs(pp)), ["%s %%" % d(abs(b - a)), "%s %%" % d(F(b * 100, a)), "%s %%" % d(abs(pp) + 10)], "Andelen ändrades %s procentenheter. Jämfört med %d %%: %s/%d = <b>%s %%</b>." % (d(abs(b - a)), a, d(abs(b - a)), a, d(abs(pp))))
        p1, p2 = ch([10, 20, 25, 50]), ch([10, 20, 25, 50])
        f = (1 + F(p1, 100)) * (1 - F(p2, 100))
        tot = (f - 1) * 100
        return M("Ett pris höjs först med %d %% och sänks sedan med %d %%. Hur stor är den totala förändringen?" % (p1, p2), ("ökning med %s %%" % d(tot)) if tot > 0 else ("minskning med %s %%" % d(-tot)) if tot < 0 else "ingen förändring",
                 ["ökning med %s %%" % d(p1 - p2) if p1 > p2 else "minskning med %s %%" % d(p2 - p1) if p2 > p1 else "ökning med 5 %", "ingen förändring" if tot else "minskning med 5 %", "ökning med %s %%" % d(p1 + p2)],
                 "%s · %s = %s. Det är en <b>%s</b>." % (d(1 + F(p1, 100)), d(1 - F(p2, 100)), d(f), ("ökning med %s %%" % d(tot)) if tot > 0 else ("minskning med %s %%" % d(-tot)) if tot < 0 else "förändring på 0 %"))

    def moms():
        p = ri(4, 200) * 4
        k = ri(0, 2)
        if k == 0:
            return MN("Ett pris utan moms är %s. Momsen är 25 %%. Vad är priset med moms?" % kr(p), F(p * 5, 4), [F(p, 4), F(p * 4, 5), p + 25], "%d · 1,25 = <b>%s kr</b>." % (p, d(F(p * 5, 4))), "kr")
        if k == 1:
            return MN("Ett pris med 25 %% moms är %s. Vad är priset utan moms?" % kr(p * 5), 4 * p, [F(p * 5 * 3, 4), p, p * 5 - 25], "%d/1,25 = <b>%d kr</b>. Att dra bort 25 %% ger fel." % (p * 5, 4 * p), "kr")
        return MN("Ett pris med 25 %% moms är %s. Hur mycket av priset är moms?" % kr(p * 5), p, [F(p * 5, 4), 4 * p, p * 5 - 25], "Utan moms: %d/1,25 = %d. Momsen är %d − %d = <b>%d kr</b>." % (p * 5, 4 * p, 5 * p, 4 * p, p), "kr")

    sets = [("Förändringsfaktor", [(ff, 20)]), ("Räkna med förändringsfaktor", [(anvand, 20)]), ("Tolka förändringsfaktorn", [(tolka, 20)]),
            ("Ursprungligt värde och moms", [(ursprung, 12), (moms, 8)]), ("Procentenheter och flera förändringar", [(enheter, 20)])]
    return unit("procent-och-forandringsfaktor", "F", "Procent och förändringsfaktor: ökning, minskning och moms", "Procent och förändringsfaktor",
                "Procent för att uttrycka förändring och förändringsfaktor samt beräkningar med procent i vardagliga situationer. Procentenheter.",
                "Arbetsblad om procent och förändringsfaktor för årskurs 8: förändringsfaktor vid ökning och minskning, ursprungligt värde, moms, procentenheter och upprepade förändringar. 100 uppgifter med facit.",
                "Ökning med 20 % = gånger 1,20", "Minskning med 20 % = gånger 0,80.", sets,
                ["Förändringsfaktorn är det nya värdet delat med det gamla. En ökning med 20 % ger 120 % = 1,20.",
                 "En minskning med 15 % ger 85 % = 0,85. Nytt värde = gammalt värde · förändringsfaktor.",
                 "Skillnaden mellan två procentsatser mäts i procentenheter: från 4 % till 6 % är en ökning med 2 procentenheter, men 50 %."],
                [("Ett pris på 640 kr höjs med 15 %", ["Förändringsfaktor 1,15", "640 · 1,15"], "736 kr"), ("Pris med moms 500 kr. Utan moms?", ["500/1,25"], "400 kr")],
                [["Minskning med 15 % ger faktorn 0,15", "Det som är kvar är 85 %: 0,85"], ["+20 % och sedan −20 % blir som förut", "1,20 · 0,80 = 0,96, en minskning med 4 %"], ["Från 4 % till 6 % är 2 %", "Det är 2 procentenheter, men 50 %"]],
                [("Varför använda förändringsfaktor?", "Du räknar ut det nya värdet i ett steg, och flera förändringar efter varandra multipliceras."),
                 ("Vad är moms?", "Mervärdesskatt. På de flesta varor är den 25 %, på mat 12 % och på böcker 6 %."), ("Hur räknar jag ut ett gammalt pris?", "Dela det nya priset med förändringsfaktorn.")])


# ============================================================ proportionalitet
def proportionalitet(lv):
    def jamfor():
        a, pa = ri(2, 9) * 100, ri(15, 80)
        b, pb = a + ch([100, 200, 250, 500]), None
        pb = int(pa * b / a) + nz(-6, 6)
        ja, jb = F(pa * 1000, a), F(pb * 1000, b)
        if ja == jb:
            return None
        best = "%d g" % a if ja < jb else "%d g" % b
        return M("En förpackning på %d g kostar %s och en på %d g kostar %s. Vilken har lägst jämförpris?" % (a, kr(pa), b, kr(pb)), "Den på %s" % best, ["Den på %s" % ("%d g" % b if best == "%d g" % a else "%d g" % a), "De kostar lika mycket per kilo", "Det går inte att avgöra"],
                 "Jämförpris: %s kr/kg och %s kr/kg. Lägst har <b>den på %s</b>." % (rd(ja, 2), rd(jb, 2), best))

    def fart():
        k = ri(0, 2)
        v, t = ri(4, 24) * 5, ch([F(1, 2), F(3, 2), F(2), F(5, 2), F(3), F(1, 4), F(3, 4), F(4)])
        s = v * t
        if s.denominator != 1:
            return None
        tt = d(t) + " h"
        if k == 0:
            return MN("En bil kör med farten %d km/h i %s. Hur långt kommer den?" % (v, tt), s, [v + t, v, s * 2], "s = v · t = %d · %s = <b>%s km</b>." % (v, d(t), d(s)), "km")
        if k == 1:
            return MN("Ett tåg åker %s km på %s. Vilken är medelfarten?" % (d(s), tt), v, [s * t, v * 2, s + t], "v = s/t = %s/%s = <b>%d km/h</b>." % (d(s), d(t), v), "km/h")
        m = int(t * 60)
        return MN("En buss kör %s km med farten %d km/h. Hur många minuter tar det?" % (d(s), v), m, [m // 2 if m > 2 else m + 30, int(F(v, s) * 60) if F(v, s) * 60 != m else m + 15, m + 60], "t = s/v = %s/%d = %s h = <b>%d min</b>." % (d(s), v, d(t), m), "min")

    def tabell():
        k = ri(2, 15)
        xs = sorted(sh(range(1, 10))[:4])
        miss = ri(0, 3)
        rows = [[str(x) for x in xs], [str(k * x) if i != miss else "?" for i, x in enumerate(xs)]]
        t = tab(["Antal (st)"] + rows[0], [["Pris (kr)"] + rows[1]])
        v = k * xs[miss]
        return MN("Priset är proportionellt mot antalet. Vilket tal saknas i tabellen?%s" % t, v, [v + k, v - 1, xs[miss] + k], "Ett styck kostar %d kr. %d · %d = <b>%d</b>." % (k, k, xs[miss], v))

    def recept():
        p1 = ch([2, 4, 6])
        p2 = ch([3, 5, 8, 10, 12])
        if p1 == p2:
            return None
        ing = ch([("dl mjöl", ri(3, 9)), ("dl mjölk", ri(2, 8)), ("g smör", ri(5, 15) * 10), ("ägg", ri(1, 4))])
        a = F(ing[1] * p2, p1)
        return M("Ett recept för %d personer behöver %d %s. Hur mycket behövs för %d personer?" % (p1, ing[1], ing[0], p2), "%s %s" % (d(a) if (a * 10).denominator == 1 else rd(a, 1), ing[0]),
                 ["%s %s" % (d(x) if (F(x) * 10).denominator == 1 else rd(x, 1), ing[0]) for x in (ing[1] + p2 - p1, F(ing[1] * p1, p2), ing[1] * p2)], "Per person: %d/%d. Gånger %d: <b>%s %s</b>." % (ing[1], p1, p2, d(a) if (a * 10).denominator == 1 else rd(a, 1), ing[0])) if (a * 10).denominator == 1 else None

    def omvand():
        n, t = ri(2, 6), ri(2, 12)
        w = n * t
        m = ch([x for x in range(2, 13) if w % x == 0 and x != n])
        k = ri(0, 1)
        if k == 0:
            return MN("%d målare behöver %d dagar för att måla ett hus. Hur lång tid tar det för %d målare?" % (n, t, m), F(w, m), [F(t * m, n), t + m - n if t + m - n > 0 else t + 1, w], "Arbetet är %d · %d = %d dagsverken. %d/%d = <b>%s dagar</b>." % (n, t, w, w, m, d(F(w, m))), "dagar")
        v = ri(4, 12) * 10
        tt = F(ri(1, 6), 2)
        s = v * tt
        v2 = ch([x for x in range(30, 130, 10) if (s / x * 60).denominator == 1 and x != v] or [v + 10])
        return MN("Med farten %d km/h tar en resa %s timmar. Hur många minuter tar den med farten %d km/h?" % (v, d(tt), v2), s / v2 * 60, [tt * 60 * v2 / v, tt * 60, s / v2 * 120], "Sträckan är %s km. %s/%d h = <b>%s min</b>." % (d(s), d(s), v2, d(s / v2 * 60)), "min") if (s / v2 * 60).denominator == 1 else None

    def vilken():
        k = ri(2, 9)
        xs = [1, 2, 3, 4]
        S_ = [("y = %dx" % k, "proportionella"), ("y = %dx + %d" % (k, ri(1, 9)), "inte proportionella"), ("y = %d/x" % (k * 12), "omvänt proportionella")]
        f, r = ch(S_)
        return M("Hur hänger x och y ihop i sambandet %s?" % f, "De är %s" % r, ["De är %s" % x for x in ("proportionella", "inte proportionella", "omvänt proportionella") if x != r] + ["De är lika stora"],
                 "<b>%s</b>: %s." % ({"proportionella": "Proportionella", "inte proportionella": "Inte proportionella", "omvänt proportionella": "Omvänt proportionella"}[r], {"proportionella": "y = kx, en dubbelt så stor x ger dubbelt så stor y", "inte proportionella": "konstanttermen gör att y inte är 0 när x = 0", "omvänt proportionella": "x · y är konstant, dubbelt så stor x ger hälften så stor y"}[r]))

    def graf():
        k = ch([F(1, 2), F(1), F(2), F(3), F(3, 2), F(4)])
        x0 = ri(1, 4)
        fig = kosy([(k, 0, BLUE, "")], [], 0, 10, 24, "graf för ett proportionellt samband")
        x = ri(2, 8)
        v = k * x
        if v > 10 or v.denominator != 1:
            return None
        return MN("Grafen visar ett proportionellt samband. Vad är y när x = %d?<div class='qfig'>%s</div>" % (x, fig), v, [v + 1, x, k * (x + 1)], "Grafen går genom origo och ökar %s per steg. y = %s · %d = <b>%s</b>." % (d(k), d(k), x, d(v)))

    if lv == 7:
        sets = [("Jämförpris", [(jamfor, 20)]), ("Fart, sträcka och tid", [(fart, 20)]), ("Proportionella tabeller", [(tabell, 20)]),
                ("Recept och skalning", [(recept, 20)]), ("Grafer och tabeller", [(graf, 10), (tabell, 10)])]
        title, meta = "Proportionalitet: jämförpris, fart och recept", "Arbetsblad om proportionalitet för årskurs 7: jämförpris, fart, sträcka och tid, proportionella tabeller, recept och grafer. 100 uppgifter med facit."
    else:
        sets = [("Proportionella samband", [(tabell, 10), (graf, 10)]), ("Omvänt proportionella samband", [(omvand, 20)]), ("Vilket samband?", [(vilken, 6), (tabell, 14)]),
                ("Fart, sträcka och tid", [(fart, 20)]), ("Jämförpris och recept", [(jamfor, 10), (recept, 10)])]
        title, meta = "Proportionalitet: proportionella och omvänt proportionella samband", "Arbetsblad om proportionalitet för årskurs 8: proportionella och omvänt proportionella samband, tabeller, grafer, fart och jämförpris. 100 uppgifter med facit."
    return unit("proportionalitet", "F", title, "Proportionalitet",
                "Proportionalitet och procent samt deras samband. Hur proportionella samband kan beskrivas med tabeller, grafer och formler. Jämförpris och hastighet." + (" Omvänd proportionalitet." if lv == 8 else ""),
                meta, "y = kx: dubbla x ger dubbla y", "Grafen är en rät linje genom origo.", sets,
                ["Två storheter är proportionella om de ökar i samma takt: dubbelt så många ger dubbelt så mycket. Sambandet kan skrivas y = kx.",
                 "Jämförpris visar priset per kilo eller liter, så att du kan jämföra olika förpackningar.",
                 "Fart, sträcka och tid hänger ihop: s = v · t." + (" Vid omvänd proportionalitet är produkten konstant: dubbelt så många målare ger halva tiden." if lv == 8 else "")],
                [("500 g kostar 32 kr. Jämförpris?", ["32/0,5"], "64 kr/kg"), ("80 km/h i 2,5 h", ["s = 80 · 2,5"], "200 km")],
                [["y = 2x + 3 är proportionellt", "Proportionellt kräver y = 0 när x = 0: y = kx"], ["Större förpackning är alltid billigast", "Räkna jämförpriset för att se"], ["1,5 h = 1 h 50 min", "1,5 h = 1 h 30 min"]],
                [("Hur ser jag om en tabell är proportionell?", "Dela y med x. Om kvoten är lika i alla kolumner är sambandet proportionellt."),
                 ("Vad betyder k i y = kx?", "Proportionalitetskonstanten, till exempel priset per styck."), ("Vad är omvänd proportionalitet?", "När x · y är konstant. Om x blir dubbelt så stort blir y hälften så stort.")])


# ============================================================ funktioner och grafer (åk 8)
def funktioner(lv):
    def koord():
        x, y = nz(-5, 5), nz(-5, 5)
        pts = [(x, y, "P")]
        fig = kosy([], pts, -5, 5, 22, "koordinatsystem med punkten P")
        return M("Vilka koordinater har punkten P?<div class='qfig'>%s</div>" % fig, "(%s, %s)" % (d(x), d(y)), ["(%s, %s)" % (d(y), d(x)), "(%s, %s)" % (d(-x), d(y)), "(%s, %s)" % (d(x), d(-y))], "x-koordinaten först, sedan y-koordinaten: <b>(%s, %s)</b>." % (d(x), d(y)))

    def tabell():
        k, m = nz(-4, 5), nz(-6, 8)
        xs = [-1, 0, 1, 2, 3]
        miss = ri(0, 4)
        t = tab(["x"] + [d(x) for x in xs], [["y"] + [d(k * x + m) if i != miss else "?" for i, x in enumerate(xs)]])
        v = k * xs[miss] + m
        return MN("Värdetabellen gäller för %s. Vilket tal saknas?%s" % (lin(k, m), t), v, [v + k, k * xs[miss], -v if v else 1], "%s · %s %s %d = <b>%s</b>." % (sg(k), par(xs[miss]), "+" if m > 0 else "−", abs(m), d(v)))

    def avlas():
        k, m = ch([F(1), F(2), F(-1), F(1, 2), F(-2), F(3), F(-1, 2)]), nz(-3, 3)
        x = nz(-3, 3)
        y = k * x + m
        if y.denominator != 1 or abs(y) > 5:
            return None
        fig = kosy([(k, m, BLUE, "")], [], -5, 5, 22, "graf till en funktion")
        if coin():
            return MN("Läs av i grafen: vad är y när x = %s?<div class='qfig'>%s</div>" % (sg(x), fig), y, [x, y + 1, -y if y else 2], "Gå till x = %s och upp eller ner till linjen: <b>y = %s</b>." % (sg(x), d(y)))
        return MN("Läs av i grafen: vilket x ger y = %s?<div class='qfig'>%s</div>" % (sg(y), fig), x, [y, x + 1, -x], "Gå till y = %s och åt sidan till linjen: <b>x = %s</b>." % (sg(y), d(x)))

    def varde():
        k, m = nz(-5, 6), nz(-9, 9)
        x = nz(-6, 8)
        f = ch(["f", "g", "h"])
        k2 = ri(0, 2)
        if k2 == 0:
            return MN("%s(x) = %s. Beräkna %s(%s)." % (f, expr([(k, "x"), (m, "")]), f, sg(x)), k * x + m, [k + x + m, k * (x + m), -(k * x + m)], "%s(%s) = %s · %s %s %d = <b>%s</b>." % (f, sg(x), sg(k), par(x), "+" if m > 0 else "−", abs(m), d(k * x + m)))
        if k2 == 1:
            a = ri(1, 3)
            v = a * x * x + m
            return MN("%s(x) = %s. Beräkna %s(%s)." % (f, expr([(a, "x²"), (m, "")]), f, sg(x)), v, [a * 2 * x + m, -a * x * x + m, (a * x) ** 2 + m] if a > 1 else [2 * x + m, -x * x + m, x + m], "%s(%s) = %s · %s² %s %d = <b>%s</b>." % (f, sg(x), d(a), par(x), "+" if m > 0 else "−", abs(m), d(v)))
        y = k * x + m
        return MN("%s(x) = %s. För vilket x är %s(x) = %s?" % (f, expr([(k, "x"), (m, "")]), f, d(y)), x, [k * y + m, y - m, -x], "%s = %s ger %sx = %s och <b>x = %s</b>." % (expr([(k, "x"), (m, "")]), d(y), sg(k) if abs(k) != 1 else ("−" if k < 0 else ""), d(y - m), d(x)))

    def vardag():
        k = ri(0, 3)
        if k == 0:
            g, p = ri(2, 8) * 10, ri(5, 25)
            x = ri(3, 30)
            return MN("Ett gym kostar %s i startavgift och %s per besök. Kostnaden y kr för x besök är y = %dx + %d. Vad kostar %d besök?" % (kr(g), kr(p), p, g, x), p * x + g, [p * x, (p + g) * x, p + g + x], "y = %d · %d + %d = <b>%d kr</b>." % (p, x, g, p * x + g), "kr")
        if k == 1:
            start, per = ri(5, 30), ri(2, 6)
            t = ri(2, 12)
            return MN("En planta är %d cm hög och växer %d cm per vecka. Hur hög är den efter %d veckor?" % (start, per, t), start + per * t, [start * per * t, start + t, per * t], "h = %d + %d · %d = <b>%d cm</b>." % (start, per, t, start + per * t), "cm")
        if k == 2:
            v, per = ri(30, 80), ri(2, 6)
            if v % per:
                return None
            return MN("En vattentank har %d liter och töms med %d liter per minut. Efter hur många minuter är den tom?" % (v, per), v // per, [v * per, v - per, v // per + per], "%d − %dx = 0 ger x = %d/%d = <b>%d min</b>." % (v, per, v, per, v // per), "min")
        a, b = ri(100, 300), ri(20, 60)
        x = ri(2, 10)
        return MN("En hantverkare tar %s för resan och %s per timme. Hur många timmar arbetade hon om räkningen blev %s?" % (kr(a), kr(b), kr(a + b * x)), x, [x + 1, F(a + b * x, b) if F(a + b * x, b) != x else x + 2, x - 1], "%d + %dx = %d ger %dx = %d och <b>x = %d</b>." % (a, b, a + b * x, b, b * x, x), "timmar")

    sets = [("Koordinater", [(koord, 20)]), ("Värdetabeller", [(tabell, 20)]), ("Läs av grafer", [(avlas, 20)]),
            ("Funktionsvärden", [(varde, 20)]), ("Funktioner i vardagen", [(vardag, 20)])]
    return unit("funktioner-och-grafer", "F", "Funktioner och grafer: värdetabell, graf och funktionsvärde", "Funktioner och grafer",
                "Funktioner och räta linjens ekvation. Hur funktioner kan användas för att undersöka förändring, förändringstakt och andra samband. Värdetabeller, grafer och formler.",
                "Arbetsblad om funktioner och grafer för årskurs 8: koordinater, värdetabeller, läs av grafer, funktionsvärden som f(3) och funktioner i vardagen. 100 uppgifter med facit.",
                "Varje x ger exakt ett y", "En funktion kan visas som formel, tabell och graf.", sets,
                ["En funktion är ett samband där varje x-värde ger exakt ett y-värde.",
                 "Samma funktion kan visas på tre sätt: som formel (y = 2x + 1), som värdetabell och som graf i ett koordinatsystem.",
                 "f(3) betyder funktionens värde när x = 3. Om f(x) = 2x + 1 är f(3) = 2 · 3 + 1 = 7."],
                [("f(x) = 2x + 1. Beräkna f(3)", ["2 · 3 + 1"], "7"), ("Punkten (−2, 4)", ["Gå 2 steg åt vänster", "Gå 4 steg upp"], "x = −2, y = 4")],
                [["Punkten (3, 1) är 1 åt höger och 3 upp", "x först: 3 åt höger, 1 upp"], ["f(3) = f · 3", "f(3) är värdet när x = 3"], ["Läser av fel axel", "x är den vågräta axeln och y den lodräta"]],
                [("Vad är skillnaden mellan x och y?", "x är det du väljer, y är det som beror på x."), ("Varför skriver man f(x)?", "Det visar tydligt vilket x-värde du räknar med, och flera funktioner kan få olika namn: f, g, h."),
                 ("Är alla grafer räta linjer?", "Nej. y = x² ger en böjd kurva, en parabel.")])


# ============================================================ linjära funktioner (åk 9)
def linjara(lv):
    def km():
        k, m = nz(-6, 6), nz(-9, 9)
        f = lin(k, m)
        if coin():
            return M("Vad är k-värdet (lutningen) för linjen %s?" % f, "k = %s" % d(k), ["k = %s" % d(m), "k = %s" % d(-k), "k = %s" % d(k + m) if k + m != k else "k = 0"], "I y = kx + m står k framför x: <b>k = %s</b>." % d(k))
        return M("I vilken punkt skär linjen %s y-axeln?" % f, "(0, %s)" % d(m), ["(%s, 0)" % d(m), "(0, %s)" % d(k), "(0, %s)" % d(-m)], "m-värdet visar var linjen skär y-axeln: <b>(0, %s)</b>." % d(m))

    def tva():
        x1, y1 = nz(-5, 5), nz(-8, 8)
        k = nz(-4, 4)
        dx = ri(1, 4)
        x2, y2 = x1 + dx, y1 + k * dx
        return M("En linje går genom punkterna (%s, %s) och (%s, %s). Vad är k-värdet?" % (d(x1), d(y1), d(x2), d(y2)), "k = %s" % d(k), ["k = %s" % fq(F(dx, k * dx)) if k else "k = 1", "k = %s" % d(-k), "k = %s" % d(k * dx) if dx > 1 else "k = %s" % d(k + 1)], "k = (y₂ − y₁)/(x₂ − x₁) = %s/%d = <b>%s</b>." % (d(y2 - y1), dx, d(k)))

    def graf():
        k, m = ch([F(1), F(2), F(-1), F(1, 2), F(-2), F(3), F(-1, 2), F(-3), F(3, 2)]), nz(-3, 3)
        fig = kosy([(k, m, BLUE, "")], [], -5, 5, 22, "graf till en rät linje")
        if coin():
            return M("Vilket k-värde har linjen?<div class='qfig'>%s</div>" % fig, "k = %s" % sg(k), ["k = %s" % sg(-k), "k = %s" % sg(1 / k) if 1 / k != k else "k = %s" % sg(k + 1), "k = %s" % d(m)], "Gå ett steg åt höger. Linjen %s %s: <b>k = %s</b>." % ("stiger" if k > 0 else "sjunker", fq(abs(k)), sg(k)))
        return M("Vilken ekvation har linjen?<div class='qfig'>%s</div>" % fig, lin(k, m), [lin(-k, m), lin(k, -m), lin(m, k) if m != k else lin(k, m + 1)], "Linjen skär y-axeln i %s och lutningen är %s: <b>%s</b>." % (d(m), sg(k), lin(k, m)))

    def parallell():
        k, m = nz(-5, 5), nz(-8, 8)
        m2 = m + nz(-6, 6)
        r = lin(k, m2)
        return MQ("Vilken linje är parallell med %s:" % lin(k, m), r, [lin(-k, m), lin(m, k) if m != k else lin(k + 1, m), lin(k + 1, m2)], "Parallella linjer har samma k-värde, %s: <b>%s</b>." % (d(k), r))

    def punkt():
        k, m = nz(-4, 5), nz(-8, 8)
        x = nz(-5, 5)
        y = k * x + m
        r = "(%s, %s)" % (d(x), d(y))
        return MQ("Vilken punkt ligger på linjen %s:" % lin(k, m), r, ["(%s, %s)" % (d(y), d(x)), "(%s, %s)" % (d(x), d(y + 1)), "(%s, %s)" % (d(-x), d(y))], "Sätt in x = %s: y = %s · %s %s %d = %s. <b>%s</b>." % (d(x), sg(k), par(x), "+" if m > 0 else "−", abs(m), d(y), r))

    sets = [("k-värde och m-värde", [(km, 20)]), ("k-värdet från två punkter", [(tva, 20)]), ("Läs av grafen", [(graf, 20)]),
            ("Parallella linjer", [(parallell, 20)]), ("Punkter på linjen", [(punkt, 20)])]
    return unit("linjara-funktioner", "F", "Linjära funktioner: k-värde, m-värde och lutning", "Linjära funktioner",
                "Linjära funktioner och räta linjens ekvation y = kx + m. Hur k-värdet beskriver förändringstakten och m-värdet startvärdet, samt hur grafer kan tolkas.",
                "Arbetsblad om linjära funktioner för årskurs 9: k-värde och m-värde, lutning från två punkter, läs av grafer, parallella linjer och punkter på linjen. 100 uppgifter med facit.",
                "y = kx + m", "k är lutningen, m är var linjen skär y-axeln.", sets,
                ["En linjär funktion har formen y = kx + m. Grafen är en rät linje.",
                 "k-värdet är lutningen: hur mycket y ändras när x ökar med 1. Positivt k ger en stigande linje, negativt en sjunkande.",
                 "m-värdet är y-värdet där linjen skär y-axeln. Med två punkter räknar du k = (y₂ − y₁)/(x₂ − x₁)."],
                [("k-värde genom (1, 3) och (4, 9)", ["(9 − 3)/(4 − 1) = 6/3"], "k = 2"), ("y = −3x + 5", ["k = −3, m = 5"], "Sjunkande, skär y-axeln i (0, 5)")],
                [["I y = 2x + 5 är k = 5", "k står framför x: k = 2"], ["k = (x₂ − x₁)/(y₂ − y₁)", "y-skillnaden står överst: k = (y₂ − y₁)/(x₂ − x₁)"], ["Parallella linjer har samma m", "Parallella linjer har samma k"]],
                [("Vad betyder k = 0?", "Linjen är vågrät, y är lika stort för alla x."), ("Kan k vara ett bråk?", "Ja. k = 1/2 betyder att linjen stiger ett steg för varje två steg åt höger."),
                 ("Vad är skillnaden mellan funktion och ekvation här?", "y = 2x + 1 beskriver en funktion. Varje punkt på linjen är en lösning till ekvationen.")])


# ============================================================ räta linjens ekvation (åk 9)
def ratalinjen(lv):
    def tva():
        x1, y1 = nz(-5, 5), nz(-8, 8)
        k = nz(-4, 4)
        dx = ri(1, 4)
        x2, y2 = x1 + dx, y1 + k * dx
        m = y1 - k * x1
        return M("Bestäm ekvationen för linjen genom (%s, %s) och (%s, %s)." % (d(x1), d(y1), d(x2), d(y2)), lin(k, m), [lin(k, y1), lin(-k, m), lin(k, m + k)], "k = %s/%d = %s. Sätt in (%s, %s): %s = %s · %s + m ger m = %s. <b>%s</b>." % (d(y2 - y1), dx, d(k), d(x1), d(y1), d(y1), sg(k), par(x1), d(m), lin(k, m)))

    def kpunkt():
        k, x1, y1 = nz(-5, 5), nz(-5, 5), nz(-9, 9)
        m = y1 - k * x1
        return M("En linje har k = %s och går genom punkten (%s, %s). Vilken är linjens ekvation?" % (d(k), d(x1), d(y1)), lin(k, m), [lin(k, y1), lin(k, y1 + k * x1) if y1 + k * x1 != m else lin(k, m + 1), lin(x1, y1) if x1 != k else lin(k, -m)], "%s = %s · %s + m ger m = %s: <b>%s</b>." % (d(y1), sg(k), par(x1), d(m), lin(k, m)))

    def graf():
        k, m = ch([F(1), F(2), F(-1), F(1, 2), F(-2), F(3), F(-1, 2), F(-3), F(3, 2), F(-3, 2)]), nz(-4, 4)
        fig = kosy([(k, m, BLUE, "")], [], -5, 5, 22, "rät linje")
        return M("Skriv ekvationen för linjen i figuren.<div class='qfig'>%s</div>" % fig, lin(k, m), [lin(-k, m), lin(k, -m), lin(m, k) if m != k else lin(k, m + 1)], "m = %s där linjen skär y-axeln och k = %s: <b>%s</b>." % (d(m), sg(k), lin(k, m)))

    def vardag():
        k = ri(0, 3)
        if k == 0:
            g, p = ri(3, 10) * 10, ri(8, 20)
            return M("En taxi kostar %s i grundavgift och %s per kilometer. Vilken formel ger priset y kr för x km?" % (kr(g), kr(p)), lin(p, g), [lin(g, p), lin(p + g, 0), "y = %d(x + %d)" % (p, g)], "Fast avgift = m = %d och pris per km = k = %d: <b>%s</b>." % (g, p, lin(p, g)))
        if k == 1:
            a, b = ri(2, 6), ri(10, 40)
            x1, x2 = ri(1, 4), ri(5, 10)
            return M("Ett ljus är %d cm efter %d timmar och %d cm efter %d timmar. Det brinner lika fort hela tiden. Vilken formel ger längden y cm efter x timmar?" % (b + 40 - a * x1, x1, b + 40 - a * x2, x2), lin(-a, b + 40), [lin(a, b + 40), lin(-a, b + 40 - a * x1), lin(-(b + 40), a)], "k = (%d − %d)/(%d − %d) = %d. m = %d + %d · %d = %d: <b>%s</b>." % (b + 40 - a * x2, b + 40 - a * x1, x2, x1, -a, b + 40 - a * x1, a, x1, b + 40, lin(-a, b + 40)))
        if k == 2:
            a = ri(150, 400)
            b = ri(30, 90)
            return M("Ett mobilabonnemang kostar %s per månad plus %s i startavgift. Vilken formel ger totalkostnaden y kr efter x månader?" % (kr(b), kr(a)), lin(b, a), [lin(a, b), lin(a + b, 0), "y = %dx − %d" % (b, a)], "Startavgift m = %d, månadskostnad k = %d: <b>%s</b>." % (a, b, lin(b, a)))
        t0, r = ri(-10, 5), ri(2, 6)
        return M("Temperaturen är %s °C klockan 6 och stiger %d grader per timme. Vilken formel ger temperaturen y °C x timmar efter klockan 6?" % (sg(t0), r), lin(r, t0), [lin(t0, r), lin(r, -t0) if t0 else lin(r, 6), lin(r, t0 + 6)], "Startvärde %s och ökning %d per timme: <b>%s</b>." % (sg(t0), r, lin(r, t0)))

    def skarning():
        k, m = nz(-5, 5), nz(-9, 9)
        if coin():
            x = F(-m, k)
            return M("Var skär linjen %s x-axeln?" % lin(k, m), "(%s, 0)" % sg(x), ["(0, %s)" % d(m), "(%s, 0)" % sg(-x) if x else "(1, 0)", "(%s, 0)" % sg(F(m, k)) if F(m, k) != x and F(m, k) != -x else "(%s, 0)" % sg(x + 1)], "Sätt y = 0: %s = 0 ger x = %s. <b>(%s, 0)</b>." % (expr([(k, "x"), (m, "")]), sg(x), sg(x)))
        k2 = nz(-5, 5)
        if k2 == k:
            return None
        m2 = nz(-9, 9)
        x = F(m2 - m, k - k2)
        if x.denominator != 1:
            return None
        y = k * x + m
        return M("I vilken punkt skär linjerna %s och %s varandra?" % (lin(k, m), lin(k2, m2)), "(%s, %s)" % (d(x), d(y)), ["(%s, %s)" % (d(y), d(x)), "(%s, %s)" % (d(-x), d(y)) if x else "(1, %s)" % d(y), "(%s, %s)" % (d(x), d(y + 1))], "%s = %s ger x = %s och y = %s: <b>(%s, %s)</b>." % (expr([(k, "x"), (m, "")]), expr([(k2, "x"), (m2, "")]), d(x), d(y), d(x), d(y)))

    sets = [("Linjen genom två punkter", [(tva, 20)]), ("k-värde och en punkt", [(kpunkt, 20)]), ("Ekvationen från grafen", [(graf, 20)]),
            ("Skärningspunkter", [(skarning, 20)]), ("Räta linjer i vardagen", [(vardag, 20)])]
    return unit("rata-linjens-ekvation", "F", "Räta linjens ekvation: bestäm y = kx + m", "Räta linjens ekvation",
                "Funktioner och räta linjens ekvation. Att bestämma räta linjens ekvation utifrån punkter, grafer och vardagliga situationer samt skärningspunkter.",
                "Arbetsblad om räta linjens ekvation för årskurs 9: linjen genom två punkter, k-värde och en punkt, ekvationen från grafen, skärningspunkter och linjer i vardagen. 100 uppgifter med facit.",
                "Bestäm k först, sedan m", "Sätt in en punkt i y = kx + m för att få m.", sets,
                ["Bestäm först k med två punkter: k = (y₂ − y₁)/(x₂ − x₁).",
                 "Sätt sedan in en av punkterna i y = kx + m och lös ut m.",
                 "I vardagen är m ofta ett startvärde eller en fast avgift och k en förändring per enhet, till exempel kronor per kilometer."],
                [("Genom (1, 5) och (3, 9)", ["k = (9 − 5)/(3 − 1) = 2", "5 = 2 · 1 + m ger m = 3"], "y = 2x + 3"), ("Var skär y = 2x − 6 x-axeln?", ["2x − 6 = 0", "x = 3"], "(3, 0)")],
                [["m är y-värdet i första punkten", "m är y-värdet där x = 0"], ["Skärning med x-axeln: sätt x = 0", "Sätt y = 0 för x-axeln"], ["Fast avgift är k", "Fast avgift är m, priset per enhet är k"]],
                [("Hur kontrollerar jag ekvationen?", "Sätt in båda punkterna. Båda ska stämma."), ("Vad betyder ett negativt k i vardagen?", "Att något minskar, till exempel vatten som rinner ut ur en tank."),
                 ("Kan en linje sakna m?", "Om m = 0 går linjen genom origo: y = kx.")])


# ============================================================ tolka grafer (åk 9)
def grafer(lv):
    def stracka():
        v1, t1 = ri(2, 6), ri(2, 4)
        p = ri(1, 3)
        v2 = ri(1, 4)
        t2 = ri(2, 4)
        pts = [(0, 0), (t1, v1 * t1), (t1 + p, v1 * t1), (t1 + p + t2, v1 * t1 + v2 * t2)]
        T = t1 + p + t2
        S = v1 * t1 + v2 * t2
        if S > 24 or T > 12:
            return None

        def f(x):
            for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                if xa <= x <= xb:
                    return ya + (yb - ya) * (x - xa) / float(xb - xa)
            return None
        fig = kurve([(f, BLUE, "")], (0, 12, 1), (0, 24, 2), (), 340, 250, "graf över sträcka och tid")
        k = ri(0, 2)
        if k == 0:
            return M("Grafen visar %s promenad. x är tiden i minuter och y sträckan i hundratals meter. Hur länge stod %s stilla?<div class='qfig'>%s</div>" % (gen(K().name()), "hon eller han", fig), "%d min" % p, ["%d min" % t1, "%d min" % t2 if t2 != p else "%d min" % (p + 1), "%d min" % T], "Där grafen är vågrät ändras inte sträckan: från %d till %d, alltså <b>%d min</b>." % (t1, t1 + p, p))
        if k == 1:
            return M("Grafen visar en promenad. x är tiden i minuter och y sträckan i hundratals meter. Hur lång var promenaden totalt?<div class='qfig'>%s</div>" % fig, "%d00 m" % S, ["%d00 m" % (v1 * t1), "%d00 m" % T, "%d00 m" % (S + 2)], "Läs av y-värdet i slutet: %d hundra meter = <b>%d00 m</b>." % (S, S))
        if v1 == v2:
            return None
        return M("Grafen visar en promenad. När gick personen fortast?<div class='qfig'>%s</div>" % fig, "Under de första %d minuterna" % t1 if v1 > v2 else "Under de sista %d minuterna" % t2, ["Under de första %d minuterna" % t1 if v1 < v2 else "Under de sista %d minuterna" % t2, "När grafen är vågrät", "Lika fort hela tiden"], "Brantast lutning betyder störst fart: <b>%s</b>." % ("de första %d minuterna" % t1 if v1 > v2 else "de sista %d minuterna" % t2))

    def situation():
        P = [("Ett badkar fylls med vatten i jämn takt.", "En rät linje som stiger", ["En vågrät linje", "En rät linje som sjunker", "En kurva som först stiger och sedan sjunker"]),
             ("En kopp kaffe svalnar på ett bord.", "En kurva som sjunker allt långsammare", ["En rät linje som stiger", "En vågrät linje", "En kurva som stiger allt snabbare"]),
             ("En boll kastas rakt upp och faller ner igen. Grafen visar höjden.", "En kurva som stiger och sedan sjunker", ["En rät linje som stiger", "En vågrät linje", "En rät linje som sjunker"]),
             ("En bil står parkerad hela dagen. Grafen visar sträckan från hemmet.", "En vågrät linje", ["En rät linje som stiger", "En kurva som stiger", "En rät linje som sjunker"]),
             ("Ett ljus brinner ner i jämn takt. Grafen visar ljusets längd.", "En rät linje som sjunker", ["En rät linje som stiger", "En vågrät linje", "En kurva som stiger och sedan sjunker"]),
             ("Pengar på ett sparkonto växer med ränta på ränta.", "En kurva som stiger allt snabbare", ["En rät linje som sjunker", "En vågrät linje", "En kurva som sjunker allt långsammare"]),
             ("Arean av en kvadrat beroende på sidans längd.", "En kurva som stiger allt snabbare", ["En rät linje som stiger", "En vågrät linje", "En rät linje som sjunker"]),
             ("Omkretsen av en kvadrat beroende på sidans längd.", "En rät linje som stiger", ["En kurva som stiger allt snabbare", "En vågrät linje", "En rät linje som sjunker"]),
             ("Ett is-block smälter i ett varmt rum. Grafen visar massan.", "En kurva som sjunker", ["En rät linje som stiger", "En vågrät linje", "En kurva som stiger och sedan sjunker"]),
             ("Antal personer i en simhall under en dag, från öppning till stängning.", "En kurva som stiger och sedan sjunker", ["En rät linje som stiger", "En vågrät linje", "En rät linje som sjunker"])]
        q, r, w = ch(P)
        return M("%s Vilken graf passar bäst?" % q, r, w, "<b>%s</b>." % r)

    def tabell():
        a = ri(1, 3)
        c = nz(-5, 5)
        xs = [-2, -1, 0, 1, 2, 3]
        miss = ri(0, 5)
        t = tab(["x"] + [d(x) for x in xs], [["y"] + [d(a * x * x + c) if i != miss else "?" for i, x in enumerate(xs)]])
        v = a * xs[miss] ** 2 + c
        return MN("Tabellen gäller för y = %s. Vilket tal saknas?%s" % (expr([(a, "x²"), (c, "")]), t), v, [a * 2 * xs[miss] + c, -v if v else 1, a * xs[miss] + c if a * xs[miss] + c != v else v + 2], "y = %s · %s² %s %d = <b>%s</b>." % (d(a), par(xs[miss]), "+" if c > 0 else "−", abs(c), d(v)))

    def parabel():
        a, c = ch([1, -1]), nz(-4, 4)
        fig = kurve([(lambda x: a * x * x + c, BLUE, "")], (-4, 4, 1), (-8, 8, 2), (), 300, 260, "graf till en andragradsfunktion")
        k = ri(0, 1)
        if k == 0:
            return M("Grafen visar en andragradsfunktion. Vilken är dess %s?<div class='qfig'>%s</div>" % ("minsta värde" if a > 0 else "största värde", fig), "y = %s" % d(c), ["y = %s" % d(-c), "y = 0", "y = %s" % d(c + 2)], "Vändpunkten ligger i (0, %s). %s är <b>y = %s</b>." % (d(c), "Minsta värdet" if a > 0 else "Största värdet", d(c)))
        r = expr([(a, "x²"), (c, "")])
        return M("Vilken formel passar till grafen?<div class='qfig'>%s</div>" % fig, "y = %s" % r, ["y = %s" % expr([(-a, "x²"), (c, "")]), "y = %s" % expr([(a, "x²"), (-c, "")]), "y = %s" % expr([(a, "x"), (c, "")])], "Grafen %s och skär y-axeln i %s: <b>y = %s</b>." % ("öppnar sig uppåt (+x²)" if a > 0 else "öppnar sig nedåt (−x²)", d(c), r))

    def takt():
        k = ri(0, 2)
        if k == 0:
            a, b = ri(100, 400), ri(10, 60)
            t = ri(2, 8)
            return MN("En vattenreservoar hade %d m³ klockan 8 och %d m³ klockan %d. Hur stor var förändringen per timme i genomsnitt?" % (a, a + b * t, 8 + t), b, [b * t, a + b, F(a + b * t, t)], "(%d − %d)/%d = <b>%d m³ per timme</b>." % (a + b * t, a, t, b), "m³/h")
        if k == 1:
            p1, p2 = ri(10, 40), ri(41, 120)
            y = ri(2, 10)
            if (p2 - p1) % y:
                return None
            return MN("En aktie kostade %s och %d år senare %s. Hur mycket ökade priset i genomsnitt per år?" % (kr(p1), y, kr(p2)), (p2 - p1) // y, [p2 - p1, F(p2, y) if F(p2, y).denominator == 1 else p2 - p1 + 1, (p2 - p1) // y + 1], "(%d − %d)/%d = <b>%d kr per år</b>." % (p2, p1, y, (p2 - p1) // y), "kr")
        h = ri(2, 8) * 100
        t = ri(2, 10)
        if h % t:
            return None
        return MN("Ett flygplan sjönk från %d m till 0 m på %d minuter. Vad var förändringstakten?" % (h, t), -F(h, t), [F(h, t), -h, -F(t, h)], "(0 − %d)/%d = <b>%s m per minut</b>. Negativ eftersom höjden minskar." % (h, t, d(-F(h, t))), "m/min")

    sets = [("Sträcka och tid", [(stracka, 20)]), ("Vilken graf passar?", [(situation, 10), (stracka, 10)]), ("Andragradsfunktioner", [(tabell, 10), (parabel, 10)]),
            ("Förändringstakt", [(takt, 20)]), ("Tabeller och grafer", [(tabell, 10), (parabel, 10)])]
    return unit("tolka-grafer", "F", "Tolka grafer: sträcka, förändringstakt och kurvor", "Tolka grafer",
                "Hur funktioner kan användas för att undersöka förändring, förändringstakt och andra samband. Linjära och icke-linjära samband i vardagliga situationer.",
                "Arbetsblad om att tolka grafer för årskurs 9: sträcka och tid, vilken graf passar en situation, andragradsfunktioner, förändringstakt och tabeller. 100 uppgifter med facit.",
                "Brant graf = snabb förändring", "En vågrät del betyder att inget ändras.", sets,
                ["En graf visar hur en storhet ändras när en annan ändras. Ju brantare grafen är, desto snabbare går förändringen.",
                 "I en graf över sträcka och tid betyder en vågrät del att man står stilla.",
                 "Alla samband är inte linjära. y = x² ger en kurva, en parabel, med en vändpunkt där funktionen har sitt minsta eller största värde."],
                [("Förändringstakt från 120 m³ till 300 m³ på 6 h", ["(300 − 120)/6"], "30 m³ per timme"), ("Minsta värdet av y = x² − 3", ["Vändpunkten är (0, −3)"], "−3")],
                [["Vågrät graf betyder hög fart", "Vågrät graf betyder att sträckan inte ändras"], ["Alla grafer är räta linjer", "Till exempel y = x² och ränta på ränta ger kurvor"], ["Förändringstakt är bara skillnaden", "Dela skillnaden med tiden"]],
                [("Vad är förändringstakt?", "Hur mycket något ändras per tidsenhet, till exempel kilometer per timme."), ("Vad är en parabel?", "Grafen till en andragradsfunktion, till exempel y = x²."),
                 ("Hur ser jag om ett samband är linjärt?", "Om y ändras lika mycket varje gång x ökar med 1 är sambandet linjärt.")])


# ============================================================ ränta och lån (åk 9)
def ranta(lv):
    def enkel():
        b = ri(2, 60) * 1000
        r = ch([F(1, 2), 1, F(3, 2), 2, F(5, 2), 3, 4, 5, 6])
        v = b * F(r) / 100
        nm, g = K().next()
        return MN("%s sätter in %s på ett sparkonto med %s %% ränta per år. Hur mycket ränta får %s efter ett år?" % (nm, kr(b), d(r), "hon" if g == "f" else "han"), v, [b * F(r) / 10, b + v, F(r) * 100], "%s %% av %s = %s · %s = <b>%s kr</b>." % (d(r), num(b), d(F(r) / 100), num(b), d(v)), "kr")

    def rpr():
        b = ri(2, 50) * 1000
        r = ch([2, 3, 4, 5, 6, 8, 10])
        n = ri(2, 10)
        v = b * (1 + F(r, 100)) ** n
        return M("Du sätter in %s med %d %% ränta per år och tar inte ut räntan. Hur mycket finns på kontot efter %d år? Avrunda till hela kronor." % (kr(b), r, n), rd(v, 0) + NB + "kr", [rd(b * (1 + F(r * n, 100)), 0) + NB + "kr", rd(v * (1 + F(r, 100)), 0) + NB + "kr", rd(b * F(r, 100) * n, 0) + NB + "kr"], "%s · %s%s ≈ <b>%s kr</b>." % (num(b), d(1 + F(r, 100)), sup(n), rd(v, 0)))

    def lan():
        L = ri(5, 40) * 10000
        r = ch([3, 4, 5, 6, 7, 8, 12, 15, 20])
        k = ri(0, 2)
        if k == 0:
            v = F(L * r, 100 * 12)
            return MN("Ett lån på %s har %d %% ränta per år. Hur stor är räntekostnaden för en månad?" % (kr(L), r), rd(v, 0) if False else v, [v * 12, F(L * r, 100), v / 10], "%d %% av %s = %s kr per år. Delat med 12: <b>%s kr</b>." % (r, num(L), num(L * r // 100), rd(v, 2) if v.denominator != 1 else num(v)), "kr") if (v * 100).denominator == 1 else None
        if k == 1:
            n = ch([2, 4, 5, 8, 10])
            a = F(L, n)
            ra = F(L * r, 100)
            return MN("Ett lån på %s ska betalas av med lika mycket varje år i %d år. Räntan är %d %%. Hur mycket betalar du första året (amortering + ränta)?" % (kr(L), n, r), a + ra, [a, ra, a + F(a * r, 100)], "Amortering %s kr och ränta %s kr: <b>%s kr</b>." % (num(a), num(ra), num(a + ra)), "kr") if a.denominator == 1 and ra.denominator == 1 else None
        p = ri(10, 50) * 1000
        r1 = ch([15, 20, 25])
        m = ri(3, 12)
        v = F(p * r1 * m, 100 * 12)
        return MN("Du köper en TV för %s på avbetalning. Räntan är %d %% per år och du betalar efter %d månader. Hur mycket ränta blir det?" % (kr(p), r1, m), v, [F(p * r1, 100), F(p * r1 * m, 100), v * 2], "%d %% per år = %s kr. För %d månader: %s · %d/12 = <b>%s kr</b>." % (r1, num(p * r1 // 100), m, num(p * r1 // 100), m, d(v)), "kr") if v.denominator == 1 else None

    def jamfor():
        b = ri(1, 9) * 10000
        r = ch([3, 4, 5, 6])
        n = ch([5, 10, 20])
        rp = b * (1 + F(r, 100)) ** n
        en = b * (1 + F(r * n, 100))
        return M("%s placeras i %d år med %d %% årlig ränta. Hur mycket mer blir det med ränta på ränta än om räntan tas ut varje år? Avrunda till hela kronor." % (kr(b), n, r), rd(rp - en, 0) + NB + "kr", [rd(rp - b, 0) + NB + "kr", rd(en - b, 0) + NB + "kr", rd((rp - en) / n, 0) + NB + "kr"], "Ränta på ränta: %s kr. Utan: %s kr. Skillnad <b>%s kr</b>." % (rd(rp, 0), num(en), rd(rp - en, 0)))

    def ranta_baklanges():
        b = ri(2, 20) * 1000
        r = ch([2, 3, 4, 5, 6, 8])
        v = b * r // 100
        if coin():
            return MN("Efter ett år fick %s %s i ränta på %s. Vilken var räntesatsen?" % (K().name(), kr(v), kr(b)), r, [v, F(b, v) if F(b, v).denominator == 1 else r + 1, r * 10], "%d/%d = %s = <b>%d %%</b>." % (v, b, d(F(r, 100)), r), "%")
        return MN("Med %d %% ränta fick du %s i ränta efter ett år. Hur mycket hade du satt in?" % (r, kr(v)), b, [v * r, b + v, b // 10], "%d/%s = <b>%s kr</b>." % (v, d(F(r, 100)), num(b)), "kr")

    sets = [("Ränta efter ett år", [(enkel, 20)]), ("Ränta på ränta", [(rpr, 20)]), ("Lån och avbetalning", [(lan, 20)]),
            ("Räkna baklänges", [(ranta_baklanges, 20)]), ("Jämför sparande", [(jamfor, 10), (rpr, 10)])]
    return unit("ranta-och-lan", "F", "Ränta och lån: sparande, ränta på ränta och amortering", "Ränta och lån",
                "Procent för att uttrycka förändring och förändringsfaktor samt beräkningar med procent i vardagliga situationer och i situationer inom privatekonomi, till exempel ränta och lån.",
                "Arbetsblad om ränta och lån för årskurs 9: ränta på sparkonto, ränta på ränta, lån, amortering, avbetalning och räntesats. 100 uppgifter med facit.",
                "Ränta på ränta: multiplicera varje år", "Varje år räknas räntan på det nya beloppet.", sets,
                ["Ränta är det du får för att låna ut pengar till banken, eller det du betalar när du lånar. Räntan anges i procent per år.",
                 "Ränta på ränta: om räntan stannar på kontot multiplicerar du med förändringsfaktorn varje år. 10 000 kr med 5 % i 3 år blir 10 000 · 1,05³ ≈ 11 576 kr.",
                 "Ett lån betalas av med amortering. Dessutom betalar du ränta på det du har kvar att betala."],
                [("10 000 kr, 5 %, 3 år", ["10 000 · 1,05³"], "11 576 kr"), ("Lån 200 000 kr, 6 % ränta, en månad", ["200 000 · 0,06 = 12 000 per år", "12 000/12"], "1 000 kr")],
                [["5 % i 3 år = 15 %", "Ränta på ränta: 1,05³ ≈ 1,158, alltså 15,8 %"], ["Månadsräntan är 6 %", "Årsräntan 6 % delas med 12 för en månad"], ["Amortering är samma sak som ränta", "Amorteringen minskar skulden, räntan är en kostnad"]],
                [("Vad är skillnaden mellan amortering och ränta?", "Amorteringen är när du betalar tillbaka själva lånet. Räntan är kostnaden för att låna."),
                 ("Varför växer ränta på ränta snabbare?", "Du får ränta även på den ränta du har fått tidigare."), ("Vad är effektiv ränta?", "Räntan inklusive alla avgifter. Den är bra att jämföra lån med.")])


# ============================================================ exponentiell förändring (åk 9)
def exponentiell(lv):
    def vaxt():
        b = ri(2, 50) * 100
        p = ch([2, 3, 4, 5, 8, 10, 12, 15, 20])
        n = ri(2, 8)
        v = b * (1 + F(p, 100)) ** n
        thing = ch([("En stad har %s invånare. Folkmängden ökar med %d %% per år." % (num(b), p), "invånare", "Hur många invånare finns det efter %d år?" % n),
                    ("En bakteriekultur har %s bakterier och ökar med %d %% per timme." % (num(b), p), "bakterier", "Hur många finns det efter %d timmar?" % n),
                    ("Ett konstverk är värt %s och värdet ökar med %d %% per år." % (kr(b), p), "kr", "Vad är det värt efter %d år?" % n)])
        return M("%s %s Avrunda till heltal." % (thing[0], thing[2]), rd(v, 0) + NB + thing[1], [rd(b * (1 + F(p * n, 100)), 0) + NB + thing[1], rd(b * (1 + F(p, 100)) ** (n - 1), 0) + NB + thing[1], rd(b * F(p, 100) ** n * 100 if False else v * (1 + F(p, 100)), 0) + NB + thing[1]], "%s · %s%s ≈ <b>%s</b>." % (num(b), d(1 + F(p, 100)), sup(n), rd(v, 0)))

    def minsk():
        b = ri(10, 400) * 1000
        p = ch([10, 12, 15, 20, 25, 30])
        n = ri(2, 6)
        v = b * (1 - F(p, 100)) ** n
        return M("En bil köps för %s. Värdet minskar med %d %% per år. Vad är bilen värd efter %d år? Avrunda till hela kronor." % (kr(b), p, n), rd(v, 0) + NB + "kr", [rd(b * (1 - F(p * n, 100)), 0) + NB + "kr" if p * n < 100 else rd(v * 2, 0) + NB + "kr", rd(b * (1 - F(p, 100)) ** (n - 1), 0) + NB + "kr", rd(b * (1 + F(p, 100)) ** n, 0) + NB + "kr"], "%s · %s%s ≈ <b>%s kr</b>." % (num(b), d(1 - F(p, 100)), sup(n), rd(v, 0)))

    def halv():
        m = ch([16, 32, 64, 80, 96, 128, 160, 200, 240, 320, 400, 480, 640])
        t = ch([2, 3, 5, 6, 8, 10, 12, 30])
        n = ri(1, 4)
        v = F(m, 2 ** n)
        return MN("Ett radioaktivt ämne har halveringstiden %d år. Från början finns %d g. Hur mycket finns kvar efter %d år?" % (t, m, n * t), v, [F(m, 2 * n) if F(m, 2 * n) != v else v * 2, m - n * t if m - n * t > 0 else v + 10, v * 2], "%d år är %d halveringstider. %d · 0,5%s = <b>%s g</b>." % (n * t, n, m, sup(n), d(v)), "g")

    def vilken():
        b = ri(2, 12) * 10
        k = ri(0, 3)
        if k == 0:
            f = ch([2, 3, F(3, 2), F(5, 4), F(6, 5)])
            seq = [b * f ** i for i in range(4)]
            r = "Exponentiell, samma faktor %s varje gång" % d(f)
        elif k == 1:
            f = ch([F(1, 2), F(4, 5), F(9, 10), F(3, 4)])
            seq = [b * 8 * f ** i for i in range(4)]
            r = "Exponentiell, samma faktor %s varje gång" % d(f)
        elif k == 2:
            dd = ri(2, 30)
            seq = [b + dd * i for i in range(4)]
            r = "Linjär, ökar med %d varje gång" % dd
        else:
            dd = ri(2, 9)
            seq = [b + 40 - dd * i for i in range(4)]
            r = "Linjär, minskar med %d varje gång" % dd
        if any(F(x).denominator != 1 for x in seq):
            return None
        w = ["Linjär, ökar med %s varje gång" % d(seq[1] - seq[0]) if seq[1] > seq[0] else "Linjär, minskar med %s varje gång" % d(seq[0] - seq[1]),
             "Exponentiell, samma faktor %s varje gång" % d(F(seq[1], seq[0])), "Ingen regelbunden förändring", "Exponentiell, samma faktor %s varje gång" % d(seq[1] - seq[0])]
        return M("Talföljden är %s, … Vilken sorts förändring är det?" % ", ".join(d(x) for x in seq), r, w, "Jämför skillnad och kvot mellan talen: <b>%s</b>." % r)

    def faktor():
        a, b = ri(2, 30) * 100, None
        f = ch([F(11, 10), F(12, 10), F(105, 100), F(9, 10), F(8, 10), F(115, 100), F(125, 100), F(95, 100), F(75, 100), F(13, 10)])
        b = a * f
        if b.denominator != 1:
            return None
        p = (f - 1) * 100
        return M("Ett värde ändras från %s till %s per år på samma sätt varje år. Vilken är förändringsfaktorn och vad blir värdet året därpå?" % (num(a), num(b)), "%s och %s" % (d(f), d(b * f)), ["%s och %s" % (d(f), d(b + (b - a))) if b * f != 2 * b - a else "%s och %s" % (d(f), d(b * f + 1)), "%s och %s" % (d(p), d(b * f)), "%s och %s" % (d(1 / f) if (1 / f) * 1000 == int((1 / f) * 1000) else d(2 - f), d(b * f))],
                 "%s/%s = %s. %s · %s = <b>%s</b>." % (num(b), num(a), d(f), num(b), d(f), d(b * f)))

    sets = [("Exponentiell tillväxt", [(vaxt, 20)]), ("Värdeminskning", [(minsk, 20)]), ("Halveringstid", [(halv, 20)]),
            ("Förändringsfaktor varje år", [(faktor, 20)]), ("Linjärt eller exponentiellt?", [(vilken, 10), (vaxt, 5), (minsk, 5)])]
    return unit("exponentiell-forandring", "F", "Exponentiell förändring: tillväxt, värdeminskning och halveringstid", "Exponentiell förändring",
                "Procent för att uttrycka förändring och förändringsfaktor. Upprepad procentuell förändring, exponentiell tillväxt och minskning i vardagliga och naturvetenskapliga situationer.",
                "Arbetsblad om exponentiell förändring för årskurs 9: exponentiell tillväxt, värdeminskning, halveringstid, förändringsfaktor och skillnaden mot linjär förändring. 100 uppgifter med facit.",
                "Nytt värde = startvärde · faktorⁿ", "Samma procent varje gång ger exponentiell förändring.", sets,
                ["Om något ändras med samma procent varje år multiplicerar du med samma förändringsfaktor varje gång: startvärde · faktorⁿ.",
                 "En ökning med 10 % per år i 5 år ger faktorn 1,10⁵ ≈ 1,61, inte 1,50.",
                 "Halveringstid är tiden det tar för en mängd att halveras. Efter tre halveringstider finns 0,5³ = 1/8 kvar."],
                [("En bil för 200 000 kr tappar 15 % per år. Värde efter 3 år?", ["200 000 · 0,85³"], "122 825 kr"), ("80 g, halveringstid 5 år. Efter 15 år?", ["15 år = 3 halveringstider", "80 · 0,5³"], "10 g")],
                [["10 % per år i 5 år = 50 %", "1,10⁵ ≈ 1,61, alltså 61 %"], ["Minskning 15 % per år: · 0,15", "Faktorn är 0,85"], ["Exponentiellt = ökar lika mycket varje år", "Det ökar med lika många procent, så ökningen blir större"]],
                [("Vad är skillnaden mellan linjär och exponentiell förändring?", "Linjärt ökar med lika mycket, exponentiellt med lika många procent varje gång."),
                 ("Var finns exponentiell förändring?", "Ränta på ränta, befolkningstillväxt, bakterier, värdeminskning och radioaktivt sönderfall."), ("Hur räknar jag med miniräknaren?", "Använd knappen för potens, till exempel 1.05^10.")])


UNITS = {"procent": procent, "procent-och-forandringsfaktor": forandring, "proportionalitet": proportionalitet, "funktioner-och-grafer": funktioner,
         "linjara-funktioner": linjara, "rata-linjens-ekvation": ratalinjen, "tolka-grafer": grafer, "ranta-och-lan": ranta, "exponentiell-forandring": exponentiell}
