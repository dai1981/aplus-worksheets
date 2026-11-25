# -*- coding: utf-8 -*-
"""Sverige gymnasiet: Matematik nivå 3c（Gy25）"""
import math
from fractions import Fraction as F
from se_g import nz, xp, pol, deriv, ev, integ, U, graf, MQ, ri, ch, sh, fq, d, par, sg, M, MN, rd, sup, num, NB, MIN, coin, expr, figure

P_ = "′"


def fl(x, k=2):
    return rd(F(x).limit_denominator(10 ** 9), k)


def rpol(deg, lo=-6, hi=6, lead=None):
    cs = {e: ri(lo, hi) for e in range(deg)}
    cs[deg] = lead if lead is not None else nz(-5, 5)
    return {e: c for e, c in cs.items() if c}


def wr_deriv(cs):
    """vanliga felaktiga derivator"""
    a = {e - 1: c for e, c in cs.items() if e}                       # glömmer att multiplicera
    b = {e - 1: c * e for e, c in cs.items()}                         # konstanten blir kvar
    b = {e if e >= 0 else 0: c for e, c in b.items()}
    for e, c in cs.items():
        if e == 0:
            b[0] = b.get(0, 0) + c
    c_ = {e: c * e for e, c in cs.items() if e}                       # behåller exponenten
    return [a, b, c_]


def ps(cs, v="x"):
    cs = {e: c for e, c in cs.items() if c}
    return pol(cs, v) if cs else "0"


def ekx(k, a=1):
    kk = "" if k == 1 else (MIN if k == -1 else sg(k))
    co = "" if a == 1 else (MIN if a == -1 else sg(a))
    return "%se<sup>%sx</sup>" % (co, kk)


# ============================================================ absolutbelopp och rationella uttryck
def rationella():
    def forkorta():
        a = nz(-9, 9)
        k = ri(0, 2)
        if k == 0:
            return M("Förenkla %s." % frac_html(pol({2: 1, 0: -a * a}), "x %s %d" % ("−" if a > 0 else "+", abs(a))), "x %s %d" % ("+" if a > 0 else "−", abs(a)),
                     ["x %s %d" % ("−" if a > 0 else "+", abs(a)), "x − %d" % (a * a), "x"], "Konjugatregeln: (x + %s)(x − %s) / (x − %s) = <b>x %s %d</b>." % (par(a), par(a), par(a), "+" if a > 0 else "−", abs(a)))
        if k == 1:
            m = ri(2, 9)
            return M("Förenkla %s." % frac_html("%dx + %d" % (m, m * abs(a)), "%d" % m), "x + %d" % abs(a), ["x + %d" % (m * abs(a)), "%dx + %d" % (m, abs(a)), "x + %d" % (abs(a) + m)], "Bryt ut %d i täljaren: %d(x + %d)/%d = <b>x + %d</b>." % (m, m, abs(a), m, abs(a)))
        b = nz(-9, 9)
        if a == b:
            return None
        return M("Förenkla %s." % frac_html(pol({2: 1, 1: -(a + b), 0: a * b}), "x %s %d" % ("−" if a > 0 else "+", abs(a))), "x %s %d" % ("−" if b > 0 else "+", abs(b)),
                 ["x %s %d" % ("+" if b > 0 else "−", abs(b)), "x %s %d" % ("+" if a > 0 else "−", abs(a)), "x %s %d" % ("−" if a * b > 0 else "+", abs(a * b))], "Faktorisera täljaren: (x %s %d)(x %s %d). Förkorta: <b>x %s %d</b>." % ("−" if a > 0 else "+", abs(a), "−" if b > 0 else "+", abs(b), "−" if b > 0 else "+", abs(b)))

    def defm():
        a = nz(-9, 9)
        k = ri(0, 1)
        if k == 0:
            return M("För vilket x är uttrycket %s inte definierat?" % frac_html("%d" % ri(1, 9), "x %s %d" % ("−" if a > 0 else "+", abs(a))), "x = %s" % sg(a), ["x = %s" % sg(-a), "x = 0", "x = %s" % sg(a + 1)], "Nämnaren får inte vara 0: x %s %d = 0 ger <b>x = %s</b>." % ("−" if a > 0 else "+", abs(a), sg(a)))
        b = abs(a)
        return M("För vilka x är uttrycket %s inte definierat?" % frac_html("x + 1", pol({2: 1, 0: -b * b})), "x = ±%d" % b, ["x = %d" % b, "x = %d" % (b * b), "x = −%d" % b], "x² − %d = 0 ger <b>x = ±%d</b>." % (b * b, b))

    def addera():
        a, b = ri(1, 9), ri(1, 9)
        k = ri(0, 2)
        if k == 0:
            return M("Förenkla %s + %s." % (frac_html(str(a), "x"), frac_html(str(b), "x")), frac_html(str(a + b), "x"), [frac_html(str(a + b), "2x"), frac_html(str(a * b), "x"), frac_html(str(a + b), "x²")], "Samma nämnare: addera täljarna: <b>%d/x</b>." % (a + b))
        if k == 1:
            return M("Förenkla %s · %s." % (frac_html("%dx" % a, "%d" % (b + 1)), frac_html("%d" % (b + 1), "x²")), frac_html(str(a), "x"), [frac_html(str(a), "x²"), str(a), frac_html("%d" % (a * (b + 1)), "x")], "Förkorta (b + 1) och x: <b>%d/x</b>." % a)
        return M("Förenkla %s − %s." % (frac_html(str(a), "x"), frac_html(str(b), "2x")), frac_html(str(2 * a - b), "2x") if 2 * a != b else "0", [frac_html(str(a - b), "x") if a != b else "1", frac_html(str(a - b), "2x") if a != b else "2", frac_html(str(2 * a - b), "x") if 2 * a != b else "x"],
                 "Förläng den första med 2: (%d − %d)/(2x) = <b>%s</b>." % (2 * a, b, "%d/(2x)" % (2 * a - b) if 2 * a != b else "0"))

    def absv():
        a, b = nz(-9, 9), ri(1, 9)
        k = ri(0, 2)
        if k == 0:
            return M("Lös ekvationen |x %s %d| = %d." % ("−" if a > 0 else "+", abs(a), b), "x₁ = %s, x₂ = %s" % (sg(min(a - b, a + b)), sg(max(a - b, a + b))),
                     ["x = %s" % sg(a + b), "x₁ = %s, x₂ = %s" % (sg(min(-a - b, -a + b)), sg(max(-a - b, -a + b))), "x = ±%d" % b], "x %s %d = %d eller x %s %d = −%d: <b>x₁ = %s, x₂ = %s</b>." % ("−" if a > 0 else "+", abs(a), b, "−" if a > 0 else "+", abs(a), b, sg(min(a - b, a + b)), sg(max(a - b, a + b))))
        if k == 1:
            x = nz(-12, 12)
            return MN("Beräkna |%s| + |%d|." % (sg(x), b), abs(x) + b, [x + b, abs(x - b), -abs(x) - b], "Absolutbeloppet är avståndet till 0: %d + %d = <b>%d</b>." % (abs(x), b, abs(x) + b))
        p, q = nz(-9, 9), nz(-9, 9)
        if p == q:
            return None
        return MN("Vilket är avståndet mellan talen %s och %s på tallinjen?" % (sg(p), sg(q)), abs(p - q), [abs(p + q) if abs(p + q) != abs(p - q) else abs(p - q) + 2, p - q if p < q else q - p, abs(p) + abs(q) + 1], "Avståndet är |%s − %s| = <b>%d</b>." % (sg(p), par(q), abs(p - q)))

    sets = [("Förkorta rationella uttryck", [(forkorta, 20)]), ("Definitionsmängd", [(defm, 20)]), ("Räkna med rationella uttryck", [(addera, 20)]), ("Absolutbelopp", [(absv, 20)]), ("Blandat", [(forkorta, 7), (addera, 7), (absv, 6)])]
    return U("absolutbelopp-och-rationella-uttryck", "AF", "Absolutbelopp och rationella uttryck", "Rationella uttryck",
             "Begreppet absolutbelopp. Rationella uttryck: förenkling, definitionsmängd och räkneregler.",
             "Uppgifter om rationella uttryck och absolutbelopp för Matematik 3c: förkorta, definitionsmängd, räkna med rationella uttryck och absolutbelopp. 100 uppgifter med facit.",
             "Faktorisera först, förkorta sedan", "Nämnaren får aldrig vara 0.", sets,
             ["Ett rationellt uttryck är en kvot av två polynom. Faktorisera täljare och nämnare och förkorta gemensamma faktorer.",
              "Uttrycket är inte definierat för de x som gör nämnaren lika med 0.",
              "Absolutbeloppet |a| är avståndet från a till 0. |x − 3| = 5 ger x − 3 = 5 eller x − 3 = −5."],
             [("(x² − 9)/(x − 3)", ["(x + 3)(x − 3)/(x − 3)"], "x + 3"), ("|x + 2| = 4", ["x + 2 = 4 eller x + 2 = −4"], "x = 2 eller x = −6")],
             [["Förkortar termer i stället för faktorer", "(x + 3)/3 ≠ x + 1"], ["Glömmer den negativa lösningen", "|x| = 5 ger x = ±5"], ["Glömmer definitionsmängden", "Kontrollera nämnaren"]],
             [("Vad är ett rationellt uttryck?", "En kvot där täljare och nämnare är polynom."), ("Vad betyder |x − a|?", "Avståndet mellan x och a på tallinjen."), ("Varför får nämnaren inte vara 0?", "Division med 0 är inte definierad.")])


def frac_html(t, n):
    return "<span class='fr'><span class='fn'>%s</span><span class='fd'>%s</span></span>" % (t, n)


# ============================================================ polynom
def polynom():
    def grad():
        cs = rpol(ri(2, 5))
        n = max(cs)
        return MN("Vilket gradtal har polynomet p(x) = %s?" % ps(cs), n, [n + 1, len(cs), cs[n] if cs[n] not in (n, n + 1) else n - 1], "Den högsta exponenten är %d: <b>%d</b>." % (n, n))

    def varde():
        cs = rpol(ri(2, 3), -5, 5)
        x = nz(-3, 3)
        v = ev(cs, x)
        return MN("Beräkna p(%s) om p(x) = %s." % (sg(x), ps(cs)), v, [ev(cs, -x), v + 2 * x, ev({e: abs(c) for e, c in cs.items()}, abs(x))], "Sätt in x = %s: <b>%s</b>." % (sg(x), sg(v)))

    def mult():
        a, b, c = nz(-6, 6), nz(-6, 6), nz(-6, 6)
        r = {2: a, 1: a * c + b, 0: b * c}
        return M("Multiplicera (%s)(x %s %d)." % (pol({1: a, 0: b}), "+" if c > 0 else "−", abs(c)), ps(r), [ps({2: a, 0: b * c}), ps({2: a, 1: a + b, 0: b * c}), ps({2: a, 1: a * c - b, 0: -b * c})], "Multiplicera varje term: <b>%s</b>." % ps(r))

    def noll():
        rs = sorted(set([nz(-6, 6) for _ in range(3)]))
        if len(rs) < 3:
            return None
        m = ch([1, 2, -1, 3])
        fs = "".join("(x %s %d)" % ("−" if r > 0 else "+", abs(r)) for r in rs)
        r = ", ".join(sg(x) for x in rs)
        return M("Bestäm nollställena till p(x) = %s%s." % ("" if m == 1 else MIN if m == -1 else str(m), fs), "x = " + r, ["x = " + ", ".join(sg(-x) for x in sorted(rs, reverse=True)), "x = " + ", ".join(sg(x) for x in rs[:2]), "x = %s" % sg(m)], "En produkt är 0 när någon faktor är 0: <b>x = %s</b>." % r)

    def division():
        r = nz(-6, 6)
        a, b = nz(-6, 6), nz(-6, 6)
        cs = {2: 1, 1: a + b - 0, 0: 0}
        # (x − r)(x + s)
        s = nz(-7, 7)
        num_ = {2: 1, 1: s - r, 0: -r * s}
        return M("Utför divisionen (%s)/(x %s %d)." % (ps(num_), "−" if r > 0 else "+", abs(r)), "x %s %d" % ("+" if s > 0 else "−", abs(s)), ["x %s %d" % ("−" if s > 0 else "+", abs(s)), "x %s %d" % ("+" if r > 0 else "−", abs(r)), "x %s %d" % ("+" if s - r > 0 else "−", abs(s - r)) if s - r else "x"],
                 "%s = (x %s %d)(x %s %d). Kvoten blir <b>x %s %d</b>." % (ps(num_), "−" if r > 0 else "+", abs(r), "+" if s > 0 else "−", abs(s), "+" if s > 0 else "−", abs(s)))

    sets = [("Gradtal och koefficienter", [(grad, 20)]), ("Polynomets värde", [(varde, 20)]), ("Multiplicera polynom", [(mult, 20)]), ("Nollställen ur faktorform", [(noll, 20)]), ("Polynomdivision", [(division, 20)])]
    return U("polynom", "AF", "Polynom: gradtal, värden, multiplikation och nollställen", "Polynom",
             "Polynom, gradtal och nollställen samt räkning med polynom.",
             "Uppgifter om polynom för Matematik 3c: gradtal, polynomets värde, multiplikation, nollställen ur faktorform och enkel polynomdivision. 100 uppgifter med facit.",
             "Gradtalet = högsta exponenten", "Faktorform visar nollställena direkt.", sets,
             ["Ett polynom är en summa av termer axⁿ där n är ett naturligt tal. Den högsta exponenten är gradtalet.",
              "I faktorform p(x) = (x − a)(x − b) kan du läsa av nollställena a och b direkt.",
              "Division med (x − a) går jämnt ut om a är ett nollställe."],
             [("p(x) = 2x³ − x + 4, p(−1)", ["2 · (−1)³ − (−1) + 4"], "3")],
             [["Gradtalet = antalet termer", "Det är den högsta exponenten"], ["(x − 2) ger nollstället −2", "Nollstället är 2"], ["Glömmer parentes vid negativa x", "(−1)³ = −1"]],
             [("Vad är en koefficient?", "Talet framför variabeln i en term."), ("Hur många nollställen kan ett polynom ha?", "Högst lika många som gradtalet."), ("Var används polynom?", "Som modeller för till exempel kostnader och kastbanor.")])


# ============================================================ gränsvärden
def gransvarden():
    def insatt():
        cs = rpol(2, -5, 5)
        a = nz(-3, 3)
        v = ev(cs, a)
        return MN("Bestäm lim<sub>x→%s</sub> (%s)." % (sg(a), ps(cs)), v, [ev(cs, -a), v + 1, 0 if v else 1], "Polynomet är kontinuerligt: sätt in x = %s. <b>%s</b>." % (sg(a), sg(v)))

    def kvot():
        a = nz(-8, 8)
        k = ri(0, 1)
        if k == 0:
            return MN("Bestäm lim<sub>x→%s</sub> %s." % (sg(a), frac_html(pol({2: 1, 0: -a * a}), "x %s %d" % ("−" if a > 0 else "+", abs(a)))), 2 * a, [0, a, a * a], "Förkorta: x + %s → %s + %s = <b>%s</b>." % (par(a), sg(a), par(a), sg(2 * a)))
        b = nz(-8, 8)
        if a == b:
            return None
        return MN("Bestäm lim<sub>x→%s</sub> %s." % (sg(a), frac_html(pol({2: 1, 1: -(a + b), 0: a * b}), "x %s %d" % ("−" if a > 0 else "+", abs(a)))), a - b, [b - a, 0, a + b], "Förkorta till x %s %d och sätt in: %s − %s = <b>%s</b>." % ("−" if b > 0 else "+", abs(b), sg(a), par(b), sg(a - b)))

    def oandl():
        a, b, c, e = nz(-9, 9), nz(-9, 9), nz(1, 9), nz(-9, 9)
        return MN("Bestäm lim<sub>x→∞</sub> %s." % frac_html(pol({1: a, 0: b}), pol({1: c, 0: e})), F(a, c), [F(b, e), 0, F(a + b, c + e) if c + e else F(a, c) + 1], "Dela täljare och nämnare med x: termer med 1/x går mot 0. <b>%s</b>." % sg(F(a, c)))

    def noll_():
        a = ri(1, 9)
        k = ri(1, 3)
        return MN("Bestäm lim<sub>x→∞</sub> %s." % frac_html(str(a), xp(k)), 0, [a, 1, F(a, k)], "Nämnaren växer obegränsat: <b>0</b>.")

    def andr():
        cs = rpol(2, -4, 4)
        a, b = ri(-3, 2), 0
        b = a + ri(1, 3)
        v = (ev(cs, b) - ev(cs, a)) / (b - a)
        return MN("Beräkna ändringskvoten Δy/Δx för f(x) = %s mellan x = %s och x = %s." % (ps(cs), sg(a), sg(b)), v, [ev(cs, b) - ev(cs, a) if b - a != 1 else v + 1, (ev(cs, b) + ev(cs, a)) / (b - a), -v if v else 2], "(f(%s) − f(%s))/(%s − %s) = (%s − %s)/%d = <b>%s</b>." % (sg(b), sg(a), sg(b), par(a), sg(ev(cs, b)), par(ev(cs, a)), b - a, sg(v)))

    sets = [("Sätt in värdet", [(insatt, 20)]), ("Förkorta först", [(kvot, 20)]), ("Gränsvärden när x → ∞", [(oandl, 14), (noll_, 6)]), ("Ändringskvot", [(andr, 20)]), ("Blandat", [(insatt, 5), (kvot, 6), (oandl, 5), (andr, 4)])]
    return U("gransvarden", "DI", "Gränsvärden och ändringskvoter", "Gränsvärden",
             "Gränsvärden och genomsnittlig förändringshastighet som förberedelse för derivatan.",
             "Uppgifter om gränsvärden för Matematik 3c: sätt in värdet, förkorta först, gränsvärden när x går mot oändligheten och ändringskvot. 100 uppgifter med facit.",
             "lim x→a: vad närmar sig f(x)?", "Förkorta om du får 0/0.", sets,
             ["Gränsvärdet lim<sub>x→a</sub> f(x) är det värde som f(x) närmar sig när x närmar sig a.",
              "För polynom kan du sätta in värdet direkt. Ger insättningen 0/0, faktorisera och förkorta först.",
              "När x → ∞ går termer som a/x mot 0. Ändringskvoten Δy/Δx är den genomsnittliga förändringshastigheten."],
             [("lim x→3 (x² − 9)/(x − 3)", ["= lim (x + 3)"], "6"), ("lim x→∞ (2x + 1)/(x − 4)", ["Dela med x: (2 + 1/x)/(1 − 4/x)"], "2")],
             [["Svarar 0/0", "Förkorta först"], ["Tror att a/x → a när x → ∞", "a/x → 0"], ["Byter plats på täljare och nämnare i Δy/Δx", "Δy uppe, Δx nere"]],
             [("Måste funktionen vara definierad i a?", "Nej, gränsvärdet handlar om värden nära a."), ("Varför behövs gränsvärden?", "Derivatan definieras som ett gränsvärde."), ("Vad betyder lim?", "Limes, latin för gräns.")])


# ============================================================ derivatans definition
def definition():
    def kvot_h():
        a = ri(-3, 4)
        h = ch([F(1), F(1, 10), F(1, 100), F(1, 2)])
        k = ri(0, 1)
        if k == 0:
            v = 2 * a + h
            return MN("f(x) = x². Beräkna (f(%s + h) − f(%s))/h för h = %s." % (sg(a), sg(a), d(h)), v, [2 * a, a * a + h, 2 * a + 2 * h], "(f(a + h) − f(a))/h = 2a + h = %s + %s = <b>%s</b>." % (sg(2 * a), d(h), d(v)))
        m = ri(2, 5)
        v = 2 * m * a + m * h
        return MN("f(x) = %dx². Beräkna (f(%s + h) − f(%s))/h för h = %s." % (m, sg(a), sg(a), d(h)), v, [2 * m * a, 2 * a + h, m * a * a + h], "(%d(%s + h)² − %d · %s²)/h = %d · (2 · %s + h) = <b>%s</b>." % (m, sg(a), m, par(a), m, par(a), d(v)))

    def gr():
        k = ri(0, 2)
        a = nz(-5, 5)
        if k == 0:
            return MN("Använd derivatans definition: f(x) = x². Bestäm f%s(%s)." % (P_, sg(a)), 2 * a, [a * a, a, 2 * a + 1], "f%s(a) = lim<sub>h→0</sub> (2a + h) = 2a = <b>%s</b>." % (P_, sg(2 * a)))
        if k == 1:
            m, c = nz(-9, 9), ri(-9, 9)
            return MN("Använd derivatans definition: f(x) = %s. Bestäm f%s(%s)." % (ps({1: m, 0: c}), P_, sg(a)), m, [m * a + c, c, m * a], "(f(a + h) − f(a))/h = %s för alla h: <b>%s</b>." % (sg(m), sg(m)))
        return MN("Använd derivatans definition: f(x) = x³. Bestäm f%s(%s)." % (P_, sg(a)), 3 * a * a, [a ** 3, 3 * a, 2 * a * a], "(f(a + h) − f(a))/h = 3a² + 3ah + h² → 3a² = <b>%s</b>." % sg(3 * a * a))

    def tolka():
        t = ri(2, 12)
        v = ri(-20, 40)
        if not v:
            return None
        P = [("V(t) är vattnets volym i liter efter t minuter. Vad betyder V%s(%d) = %s?" % (P_, t, sg(v)), "Volymen %s med %d liter per minut vid t = %d" % ("ökar" if v > 0 else "minskar", abs(v), t),
              ["Volymen är %s liter efter %d minuter" % (sg(v), t), "Volymen %s med %d liter på %d minuter" % ("ökar" if v > 0 else "minskar", abs(v), t), "Det tar %d minuter att få %s liter" % (t, sg(v))]),
             ("T(t) är temperaturen i °C efter t timmar. Vad betyder T%s(%d) = %s?" % (P_, t, sg(v)), "Temperaturen %s med %d °C per timme vid t = %d" % ("stiger" if v > 0 else "sjunker", abs(v), t),
              ["Temperaturen är %s °C efter %d timmar" % (sg(v), t), "Temperaturen ändras %d gånger" % abs(v), "Det tar %d timmar att nå %s °C" % (t, sg(v))])]
        q, r, w = ch(P)
        return M(q, r, w, "Derivatan är förändringshastigheten vid ett visst ögonblick: <b>%s</b>." % r.lower())

    def graf_():
        from se_g import kurve, BLUE, RED
        k = nz(-3, 3)
        x0 = ri(-2, 2)
        m = ri(-2, 2)
        a = ch([F(1, 2), F(-1, 2), 1, -1])
        f = lambda x: float(a) * (x - x0) ** 2 + k * (x - x0) + m
        t = lambda x: k * (x - x0) + m
        if abs(m + k) > 5:
            return None
        pic = kurve([(f, BLUE, ""), (t, RED, "")], (-5, 5, 1), (-6, 6, 1), [(x0, m, ""), (x0 + 1, m + k, "")], 330, 250, "graf med tangent")
        return MN("Den röda linjen är tangenten till grafen y = f(x) i punkten (%s, %s). Bestäm f%s(%s)." % (sg(x0), sg(m), P_, sg(x0)) + pic, k, [m, -k, x0 if x0 not in (k, m, -k) else k + 2], "Tangenten går 1 steg åt höger och %s steg %s: lutningen är <b>%s</b>." % (abs(k), "uppåt" if k > 0 else "nedåt", sg(k)))

    sets = [("Ändringskvot med h", [(kvot_h, 20)]), ("Derivatans definition", [(gr, 20)]), ("Tolka derivatan", [(tolka, 20)]), ("Derivata och lutning", [(graf_, 20)]), ("Blandat", [(kvot_h, 7), (gr, 7), (tolka, 6)])]
    return U("derivatans-definition", "DI", "Derivatans definition: f′(a) som gränsvärde", "Derivatans definition",
             "Begreppen sekant, tangent, ändringskvot och derivata för en funktion. Derivatans definition.",
             "Uppgifter om derivatans definition för Matematik 3c: ändringskvot med h, derivata från definitionen, tolka derivatan och derivatan som lutning. 100 uppgifter med facit.",
             "f′(a) = lim h→0 (f(a + h) − f(a))/h", "Derivatan är tangentens lutning.", sets,
             ["Ändringskvoten (f(a + h) − f(a))/h är lutningen för sekanten genom två punkter på grafen.",
              "När h går mot 0 blir sekanten en tangent. Gränsvärdet är derivatan f′(a).",
              "Derivatan anger förändringshastigheten. V′(5) = 3 betyder att V ökar med 3 enheter per tidsenhet just vid t = 5."],
             [("f(x) = x², f′(3)", ["((3 + h)² − 9)/h = 6 + h", "h → 0"], "6")],
             [["f′(a) = f(a)", "Derivatan är lutningen, inte värdet"], ["Tolkar V′(5) = 3 som volymen 3", "Det är en hastighet"], ["Låter h vara 0 för tidigt", "Förenkla först, låt sedan h → 0"]],
             [("Vad är en sekant?", "En linje genom två punkter på grafen."), ("Vad är en tangent?", "En linje som tangerar grafen i en punkt."), ("Hur skrivs derivatan?", "f′(x), y′ eller dy/dx.")])


# ============================================================ deriveringsregler
def regler():
    def polder():
        cs = rpol(ri(2, 4), -7, 7)
        r = deriv(cs)
        return M("Derivera f(x) = %s." % ps(cs), "f%s(x) = %s" % (P_, ps(r)), ["f%s(x) = %s" % (P_, ps(w)) for w in wr_deriv(cs)], "Derivera term för term: (axⁿ)′ = naxⁿ⁻¹. <b>f%s(x) = %s</b>." % (P_, ps(r)))

    def potens():
        k = ri(0, 2)
        a = nz(-6, 6)
        if k == 0:
            n = ri(1, 3)
            return M("Derivera f(x) = %s." % ("%s/x%s" % (sg(a), sup(n) if n > 1 else "")).replace("1/", "1/") if False else "Derivera f(x) = %s." % (frac_html(sg(a), xp(n))),
                     "f%s(x) = %s" % (P_, (MIN if a > 0 else "") + frac_html(str(abs(a * n)), xp(n + 1))),
                     ["f%s(x) = %s" % (P_, frac_html(sg(a * n), xp(n - 1)) if n > 1 else sg(a * n)), "f%s(x) = %s" % (P_, frac_html(sg(a), xp(n + 1))), "f%s(x) = %s" % (P_, frac_html(sg(a * n), xp(n + 1)))],
                     "Skriv som %sx%s. Derivatan blir %sx%s = <b>%s</b>." % (sg(a), sup(-n), sg(-a * n), sup(-n - 1), (MIN if a > 0 else "") + frac_html(str(abs(a * n)), xp(n + 1))))
        if k == 1:
            return M("Derivera f(x) = %s√x." % ("" if a == 1 else MIN if a == -1 else sg(a)), "f%s(x) = %s" % (P_, frac_html(sg(a), "2√x")), ["f%s(x) = %s" % (P_, frac_html(sg(a), "√x")), "f%s(x) = %s" % (P_, frac_html(sg(2 * a), "√x")), "f%s(x) = %s√x" % (P_, sg(F(a, 2)))],
                     "√x = x<sup>1/2</sup> ger derivatan ½x<sup>−1/2</sup>: <b>%s</b>." % frac_html(sg(a), "2√x"))
        n = ri(5, 12)
        return M("Derivera f(x) = %s." % pol({n: a}), "f%s(x) = %s" % (P_, pol({n - 1: a * n})), ["f%s(x) = %s" % (P_, pol({n - 1: a})), "f%s(x) = %s" % (P_, pol({n: a * n})), "f%s(x) = %s" % (P_, pol({n + 1: a * n}))], "<b>f%s(x) = %s</b>." % (P_, pol({n - 1: a * n})))

    def varde():
        cs = rpol(ri(2, 3), -5, 5)
        x = nz(-3, 3)
        r = ev(deriv(cs), x)
        return MN("Beräkna f%s(%s) om f(x) = %s." % (P_, sg(x), ps(cs)), r, [ev(cs, x), ev(deriv(cs), -x), r + 1], "f%s(x) = %s. f%s(%s) = <b>%s</b>." % (P_, ps(deriv(cs)), P_, sg(x), sg(r)))

    def var():
        a, b = nz(-9, 9), ri(1, 9)
        t = ch([("s(t) = %s" % ps({2: a, 1: b}, "t"), "s%s(t) = %s" % (P_, ps({1: 2 * a, 0: b}, "t")), ["s%s(t) = %s" % (P_, ps({1: a, 0: b}, "t")), "s%s(t) = %s" % (P_, ps({1: 2 * a}, "t")), "s%s(t) = %s" % (P_, ps({2: 2 * a, 1: b}, "t"))]),
                ("A(r) = %s" % ps({2: a, 0: b}, "r"), "A%s(r) = %s" % (P_, ps({1: 2 * a}, "r")), ["A%s(r) = %s" % (P_, ps({1: 2 * a, 0: b}, "r")), "A%s(r) = %s" % (P_, ps({1: a}, "r")), "A%s(r) = %s" % (P_, ps({2: 2 * a}, "r"))])])
        q, r, w = t
        return M("Derivera %s." % q, r, w, "Variabeln heter något annat, men reglerna är desamma: <b>%s</b>." % r)

    sets = [("Derivera polynom", [(polder, 20)]), ("Potenser och rötter", [(potens, 20)]), ("Derivatans värde", [(varde, 20)]), ("Andra variabler", [(var, 20)]), ("Blandat", [(polder, 7), (potens, 7), (varde, 6)])]
    return U("deriveringsregler", "DI", "Deriveringsregler för potens- och polynomfunktioner", "Deriveringsregler",
             "Härledning och användning av deriveringsregler för potens- och polynomfunktioner.",
             "Uppgifter om deriveringsregler för Matematik 3c: derivera polynom, potenser och rötter, beräkna derivatans värde och derivera med andra variabler. 100 uppgifter med facit.",
             "(xⁿ)′ = nxⁿ⁻¹", "Konstanter försvinner vid derivering.", sets,
             ["Deriveringsregeln: om f(x) = axⁿ så är f′(x) = naxⁿ⁻¹. Den gäller även för negativa exponenter och bråk.",
              "Derivera en summa term för term. En konstant har derivatan 0.",
              "Skriv om 1/x² = x⁻² och √x = x<sup>1/2</sup> innan du deriverar."],
             [("f(x) = 4x³ − 2x + 7", ["12x² − 2"], "f′(x) = 12x² − 2"), ("f(x) = 3/x", ["3x⁻¹ ger −3x⁻²"], "f′(x) = −3/x²")],
             [["Behåller konstanten", "Derivatan av 7 är 0"], ["(x³)′ = 3x³", "Exponenten minskar med 1"], ["Deriverar 1/x till 1/1", "Skriv 1/x = x⁻¹"]],
             [("Varför blir konstanten 0?", "En konstant ändras inte, så förändringshastigheten är 0."), ("Kan jag derivera med räknare?", "Ja, men du ska kunna reglerna själv."), ("Vad är f′(x)?", "Derivatafunktionen som ger lutningen för varje x.")])


# ============================================================ tangenter
def tangenter():
    def ekv():
        cs = rpol(2, -4, 4, nz(-2, 2))
        a = nz(-3, 3)
        k = ev(deriv(cs), a)
        y0 = ev(cs, a)
        m = y0 - k * a
        r = "y = %s" % expr([(k, "x"), (m, "")])
        return M("Bestäm ekvationen för tangenten till y = %s i punkten där x = %s." % (ps(cs), sg(a)), r, ["y = %s" % expr([(k, "x"), (y0, "")]), "y = %s" % expr([(y0, "x"), (m, "")]), "y = %s" % expr([(-k, "x"), (y0 + k * a, "")])],
                 "y(%s) = %s och y%s(%s) = %s. m = %s − %s · %s = %s. <b>%s</b>." % (sg(a), sg(y0), P_, sg(a), sg(k), sg(y0), par(k), par(a), sg(m), r))

    def lutning():
        cs = rpol(3, -4, 4, nz(-2, 2))
        a = nz(-2, 2)
        k = ev(deriv(cs), a)
        return MN("Vilken lutning har tangenten till y = %s i x = %s?" % (ps(cs), sg(a)), k, [ev(cs, a), -k, ev(deriv(cs), -a)], "y%s = %s. y%s(%s) = <b>%s</b>." % (P_, ps(deriv(cs)), P_, sg(a), sg(k)))

    def punkt():
        a = nz(-3, 3)
        b = ri(-6, 6)
        k = nz(-8, 8)
        # y = a x² + b x, y' = 2ax + b = k
        x = F(k - b, 2 * a)
        if x.denominator != 1:
            return None
        return MN("I vilken punkt har kurvan y = %s en tangent med lutningen %s? Ange x-koordinaten." % (ps({2: a, 1: b}), sg(k)), x, [F(k, 2 * a) if F(k, 2 * a) != x else x + 1, k - b, -x if x else 1], "y%s = %s = %s ger <b>x = %s</b>." % (P_, ps({1: 2 * a, 0: b}), sg(k), sg(x)))

    def vagr():
        a = nz(-3, 3)
        b = ri(-6, 6)
        x = F(-b, 2 * a)
        return MN("Var har kurvan y = %s en vågrät tangent? Ange x-koordinaten." % ps({2: a, 1: b, 0: ri(-5, 5)}), x, [F(b, 2 * a) if b else 1, -b, F(-b, a) if b else 2], "Vågrät tangent: y%s = 0. %s = 0 ger <b>x = %s</b>." % (P_, ps({1: 2 * a, 0: b}), sg(x)))

    def normal():
        cs = rpol(2, -4, 4, nz(-2, 2))
        a = nz(-3, 3)
        k = ev(deriv(cs), a)
        if k == 0:
            return None
        return MN("Tangenten till y = %s i x = %s har lutningen %s. Vilken lutning har normalen i samma punkt?" % (ps(cs), sg(a), sg(k)), -1 / k, [k, -k, 1 / k], "Normalen är vinkelrät mot tangenten: k₁ · k₂ = −1 ger <b>%s</b>." % sg(-1 / k))

    sets = [("Tangentens lutning", [(lutning, 20)]), ("Tangentens ekvation", [(ekv, 20)]), ("Punkt med given lutning", [(punkt, 20)]), ("Vågräta tangenter", [(vagr, 20)]), ("Tangent och normal", [(normal, 10), (ekv, 10)])]
    return U("tangenter", "DI", "Tangenter: lutning och tangentens ekvation", "Tangenter",
             "Tangentens ekvation och lutning bestämda med derivata. Vågräta tangenter och normaler.",
             "Uppgifter om tangenter för Matematik 3c: tangentens lutning, tangentens ekvation, punkt med given lutning, vågräta tangenter och normaler. 100 uppgifter med facit.",
             "Tangentens lutning k = f′(a)", "Punkten (a, f(a)) ligger på tangenten.", sets,
             ["Tangentens lutning i x = a är f′(a). Tangenten går genom punkten (a, f(a)).",
              "Sätt in i y = kx + m och lös ut m: m = f(a) − k · a.",
              "En vågrät tangent har lutningen 0. Normalen är vinkelrät mot tangenten och har lutningen −1/k."],
             [("y = x² − 3x i x = 2", ["y(2) = −2", "y′(2) = 1", "m = −2 − 2 = −4"], "y = x − 4")],
             [["Använder f(a) som lutning", "Lutningen är f′(a)"], ["Glömmer att räkna ut m", "Sätt in punkten"], ["Normalens lutning = −k", "Den är −1/k"]],
             [("Varför tangerar tangenten bara i en punkt?", "Nära punkten är den bästa linjära approximationen av kurvan."), ("Vad är en normal?", "En linje vinkelrät mot tangenten."), ("Kan en tangent skära kurvan igen?", "Ja, längre bort kan den göra det.")])


# ============================================================ talet e och ln
def tal_e():
    def der():
        k, a = nz(-6, 6), nz(-5, 5)
        return M("Derivera f(x) = %s." % ekx(k, a), "f%s(x) = %s" % (P_, ekx(k, a * k)), ["f%s(x) = %s" % (P_, ekx(k, a)), "f%s(x) = %s" % (P_, ekx(k - 1, a * k)) if k != 1 else "f%s(x) = %se<sup>x</sup>" % (P_, sg(a + 1)), "f%s(x) = %s" % (P_, ekx(k, k))] if a * k != k else
                 ["f%s(x) = %s" % (P_, ekx(k, a)), "f%s(x) = %s" % (P_, ekx(k, a + k)), "f%s(x) = %s" % (P_, ekx(k + 1, a * k))], "(ae<sup>kx</sup>)′ = ake<sup>kx</sup>: <b>%s</b>." % ekx(k, a * k))

    def ln_():
        v = ri(2, 99)
        k = ri(0, 2)
        if k == 0:
            return M("Lös ekvationen e<sup>x</sup> = %d. Avrunda till två decimaler." % v, "x ≈ %s" % fl(math.log(v)), ["x ≈ %s" % fl(math.log10(v)), "x ≈ %s" % fl(v / math.e), "x ≈ %s" % fl(math.exp(1) * v / 10)], "x = ln %d ≈ <b>%s</b>." % (v, fl(math.log(v))))
        if k == 1:
            c = ri(2, 9)
            return M("Lös ekvationen %de<sup>x</sup> = %d. Avrunda till två decimaler." % (c, v * c), "x ≈ %s" % fl(math.log(v)), ["x ≈ %s" % fl(math.log(v * c)), "x ≈ %s" % fl(math.log(v * c) / c), "x ≈ %s" % fl(math.log10(v))], "e<sup>x</sup> = %d ger x = ln %d ≈ <b>%s</b>." % (v, v, fl(math.log(v))))
        a = ri(2, 9)
        return M("Lös ekvationen e<sup>%dx</sup> = %d. Avrunda till två decimaler." % (a, v), "x ≈ %s" % fl(math.log(v) / a), ["x ≈ %s" % fl(math.log(v)), "x ≈ %s" % fl(math.log(v / a)), "x ≈ %s" % fl(math.log(v) * a)], "%dx = ln %d ger x ≈ <b>%s</b>." % (a, v, fl(math.log(v) / a)))

    def ax():
        a = ch([2, 3, 5, 10, F(1, 2)])
        A = d(a) if a.__class__ is F and a.denominator != 1 else str(a)
        c = ri(1, 9)
        r = "%sf%s(x) = %s · %s<sup>x</sup> · ln %s" % ("", P_, c, A, A) if c != 1 else "f%s(x) = %s<sup>x</sup> · ln %s" % (P_, A, A)
        return M("Derivera f(x) = %s%s<sup>x</sup>." % ("" if c == 1 else "%d · " % c, A), r.replace("1 · ", ""), ["f%s(x) = %sx · %s<sup>x − 1</sup>" % (P_, "" if c == 1 else "%d" % c, A), "f%s(x) = %s%s<sup>x</sup>" % (P_, "" if c == 1 else "%d · " % c, A), "f%s(x) = %s%s<sup>x</sup> · lg %s" % (P_, "" if c == 1 else "%d · " % c, A, A)],
                 "(aˣ)′ = aˣ · ln a: <b>%s</b>." % r)

    def varde():
        k = nz(-3, 3)
        a = ri(1, 6)
        x = ri(0, 2)
        v = a * k * math.exp(k * x)
        return M("Beräkna f%s(%d) om f(x) = %s. Avrunda till en decimal." % (P_, x, ekx(k, a)), fl(v, 1), [fl(a * math.exp(k * x), 1), fl(a * k * math.exp(x), 1), fl(a * k * x, 1) if x else fl(a * k + 1, 1)], "f%s(x) = %s. f%s(%d) ≈ <b>%s</b>." % (P_, ekx(k, a * k), P_, x, fl(v, 1)))

    def till():
        N0 = ri(2, 50) * 100
        k = ch([F(1, 10), F(2, 10), F(5, 100), F(3, 10), F(-1, 10), F(-2, 10)])
        t = ri(1, 10)
        v = float(N0 * k) * math.exp(float(k) * t)
        return M("Antalet bakterier är N(t) = %s · e<sup>%st</sup> efter t timmar. Med vilken hastighet ändras antalet efter %d timmar? Avrunda till heltal." % (num(N0), d(k), t), "%s per timme" % num(int(round(v))) if v > 0 else "%s per timme" % (MIN + num(int(round(-v)))),
                 ["%s per timme" % num(int(round(N0 * math.exp(float(k) * t)))), "%s per timme" % num(int(round(abs(float(N0 * k) * t)))) if t > 1 else "%s per timme" % num(int(round(abs(v))) + 7), "%s per timme" % num(int(round(abs(float(N0 * k)))))],
                 "N%s(t) = %s · e<sup>%st</sup>. N%s(%d) ≈ <b>%s per timme</b>." % (P_, d(N0 * k), d(k), P_, t, num(int(round(v))) if v > 0 else MIN + num(int(round(-v)))))

    sets = [("Derivera eᵏˣ", [(der, 20)]), ("Ekvationer med ln", [(ln_, 20)]), ("Derivera aˣ", [(ax, 20)]), ("Derivatans värde", [(varde, 20)]), ("Tillämpningar", [(till, 20)])]
    return U("talet-e-och-ln", "DI", "Talet e, naturliga logaritmer och derivatan av eˣ", "Talet e och ln",
             "Talet e och dess egenskaper. Den naturliga logaritmen och deriveringsregler för exponentialfunktioner.",
             "Uppgifter om talet e och ln för Matematik 3c: derivera eᵏˣ och aˣ, ekvationer med ln, derivatans värde och tillämpningar. 100 uppgifter med facit.",
             "(eᵏˣ)′ = keᵏˣ", "ln är logaritmen med basen e.", sets,
             ["Talet e ≈ 2,718 är den bas där (eˣ)′ = eˣ. Allmänt gäller (eᵏˣ)′ = keᵏˣ.",
              "Den naturliga logaritmen ln x är logaritmen med basen e: eˣ = 5 ger x = ln 5.",
              "Eftersom aˣ = e<sup>x ln a</sup> blir (aˣ)′ = aˣ · ln a."],
             [("f(x) = 3e<sup>2x</sup>", ["3 · 2e<sup>2x</sup>"], "f′(x) = 6e<sup>2x</sup>"), ("e<sup>x</sup> = 20", ["x = ln 20"], "≈ 3,00")],
             [["(e<sup>3x</sup>)′ = e<sup>3x</sup>", "Glöm inte faktorn 3"], ["(2ˣ)′ = x · 2ˣ⁻¹", "Det är 2ˣ · ln 2"], ["Blandar ihop ln och lg", "ln har basen e, lg basen 10"]],
             [("Varför är e speciellt?", "eˣ är sin egen derivata."), ("Vad är ln 1?", "0, eftersom e⁰ = 1."), ("Var används e?", "I modeller för tillväxt, sönderfall och ränta.")])


# ============================================================ extrempunkter
def extrem():
    def cubic():
        """f(x) = x³ + px² + qx + c med heltal stationära punkter a < b"""
        a, b = sorted(sh(list(range(-4, 5)))[:2])
        if a == b:
            return None
        m = ch([1, -1])
        # f' = 3m(x − a)(x − b) = 3m x² − 3m(a + b) x + 3m ab → f = m x³ − (3m(a+b)/2) x² + 3m ab x + c
        if (3 * (a + b)) % 2:
            return None
        c = ri(-5, 5)
        cs = {3: m, 2: -F(3 * m * (a + b), 2), 1: 3 * m * a * b, 0: c}
        return cs, a, b, m

    def stat():
        r = cubic()
        if not r:
            return None
        cs, a, b, m = r
        return M("Bestäm x-koordinaterna för de stationära punkterna till f(x) = %s." % ps(cs), "x₁ = %s, x₂ = %s" % (sg(a), sg(b)), ["x₁ = %s, x₂ = %s" % (sg(-b), sg(-a)), "x = %s" % sg(F(a + b, 2)), "x₁ = 0, x₂ = %s" % sg(a + b) if a + b else "x₁ = 0, x₂ = 1"],
                 "f%s(x) = %s = 0 ger <b>x₁ = %s, x₂ = %s</b>." % (P_, ps(deriv(cs)), sg(a), sg(b)))

    def typ():
        r = cubic()
        if not r:
            return None
        cs, a, b, m = r
        x = ch([a, b])
        f2 = ev(deriv(deriv(cs)), x)
        t = "Maximipunkt" if f2 < 0 else "Minimipunkt"
        return M("f(x) = %s har en stationär punkt i x = %s. Vilken sort är den?" % (ps(cs), sg(x)), t, [x_ for x_ in ("Maximipunkt", "Minimipunkt", "Terrasspunkt", "Ingen extrempunkt") if x_ != t], "f%s%s(%s) = %s %s 0: <b>%s</b>." % (P_, P_, sg(x), sg(f2), "&lt;" if f2 < 0 else "&gt;", t.lower()))

    def andra():
        cs = rpol(ri(3, 4), -6, 6)
        x = nz(-3, 3)
        v = ev(deriv(deriv(cs)), x)
        return MN("Beräkna f%s%s(%s) om f(x) = %s." % (P_, P_, sg(x), ps(cs)), v, [ev(deriv(cs), x), ev(cs, x), -v if v else 1], "f%s(x) = %s och f%s%s(x) = %s. <b>%s</b>." % (P_, ps(deriv(cs)), P_, P_, ps(deriv(deriv(cs))), sg(v)))

    def vaxande():
        a = nz(-3, 3)
        b = ri(-8, 8)
        c = ri(-5, 5)
        x0 = F(-b, 2 * a)
        if x0.denominator != 1:
            return None
        if a > 0:
            r = "x &gt; %s" % sg(x0)
            w = ["x &lt; %s" % sg(x0), "x &gt; %s" % sg(-x0) if x0 else "x &gt; 1", "x &gt; %s" % sg(c) if c != x0 else "alla x"]
        else:
            r = "x &lt; %s" % sg(x0)
            w = ["x &gt; %s" % sg(x0), "x &lt; %s" % sg(-x0) if x0 else "x &lt; 1", "x &lt; %s" % sg(c) if c != x0 else "alla x"]
        return M("För vilka x är f(x) = %s växande?" % ps({2: a, 1: b, 0: c}), r, w, "f%s(x) = %s &gt; 0 ger <b>%s</b>." % (P_, ps({1: 2 * a, 0: b}), r))

    def tecken():
        r = cubic()
        if not r:
            return None
        cs, a, b, m = r
        fa, fb = ev(cs, a), ev(cs, b)
        mx, mn = (a, fa), (b, fb)
        if m < 0:
            mx, mn = (b, fb), (a, fa)
        return M("Bestäm maximipunkten till f(x) = %s." % ps(cs), "(%s, %s)" % (sg(mx[0]), sg(mx[1])), ["(%s, %s)" % (sg(mn[0]), sg(mn[1])), "(%s, %s)" % (sg(mx[0]), sg(mn[1])), "(%s, 0)" % sg(mx[0])],
                 "Stationära punkter i x = %s och x = %s. Teckentabell eller andraderivata ger maximum i x = %s: <b>(%s, %s)</b>." % (sg(a), sg(b), sg(mx[0]), sg(mx[0]), sg(mx[1])))

    sets = [("Stationära punkter", [(stat, 20)]), ("Maximum eller minimum?", [(typ, 20)]), ("Andraderivata", [(andra, 20)]), ("Växande och avtagande", [(vaxande, 20)]), ("Bestäm maximipunkten", [(tecken, 20)])]
    return U("extrempunkter-och-andraderivata", "DI", "Extrempunkter, teckentabell och andraderivata", "Extrempunkter",
             "Sambandet mellan en funktions graf och funktionens första- och andraderivata. Extrempunkter och växande och avtagande funktioner.",
             "Uppgifter om extrempunkter för Matematik 3c: stationära punkter, maximum eller minimum, andraderivata, växande och avtagande samt maximipunkter. 100 uppgifter med facit.",
             "f′(x) = 0 i stationära punkter", "f″ &lt; 0: max, f″ &gt; 0: min.", sets,
             ["I en stationär punkt är f′(x) = 0. Den kan vara en maximipunkt, en minimipunkt eller en terrasspunkt.",
              "Teckentabell: om f′ byter tecken från + till − är det ett maximum, från − till + ett minimum.",
              "Andraderivatan: f″(a) &lt; 0 ger maximum och f″(a) &gt; 0 ger minimum. f är växande där f′(x) &gt; 0."],
             [("f(x) = x³ − 3x", ["f′(x) = 3x² − 3 = 0", "x = ±1", "f″(−1) = −6, f″(1) = 6"], "Max i (−1, 2), min i (1, −2)")],
             [["Svarar bara med x", "En punkt har två koordinater"], ["f″ &gt; 0 ger maximum", "f″ &gt; 0 ger minimum"], ["f′ = 0 betyder alltid extrempunkt", "Det kan vara en terrasspunkt"]],
             [("Vad är en terrasspunkt?", "En stationär punkt där f′ inte byter tecken."), ("Vad visar f″?", "Hur lutningen ändras: om grafen är konvex eller konkav."), ("Kan en funktion sakna extrempunkter?", "Ja, till exempel f(x) = x³ + x.")])


# ============================================================ optimering
def optimering():
    def staket():
        L = ri(10, 80) * 2
        x = F(L, 4)
        return MN("En bonde har %d m stängsel och vill hägna in en rektangulär hage längs en lång mur (muren behöver inget stängsel). Vilken är den största arean?" % L, x * (L - 2 * x), [F(L, 4) ** 2, F(L * L, 4), x * (L - x)],
                  "A(x) = x(%d − 2x). A%s(x) = %d − 4x = 0 ger x = %s och A = %s · %s = <b>%s m²</b>." % (L, P_, L, d(x), d(x), d(L - 2 * x), d(x * (L - 2 * x))), "m²")

    def vinst():
        a = ch([F(1, 10), F(1, 5), F(1, 2), 1, 2])
        p = ri(10, 60) * 10
        c = ri(1, 9) * 100
        a = F(a)
        x = F(p) / (2 * a)
        if (x).denominator != 1:
            return None
        V = -a * x * x + p * x - c
        return MN("Vinsten V(x) = %s kr vid x sålda enheter. Hur många enheter ger störst vinst?" % ("%s%sx² + %sx − %s" % (MIN, "" if a == 1 else d(a), num(p), num(c))), x, [x * 2, p, x - c // 100 if x - c // 100 > 0 else x + 10], "V%s(x) = %s = 0 ger <b>x = %s</b>." % (P_, "%s%sx + %s" % (MIN, "" if 2 * a == 1 else d(2 * a), num(p)), num(int(x))))

    def lada():
        L = ri(3, 15) * 6
        x = F(L, 6)
        V = x * (L - 2 * x) ** 2
        k = ri(0, 1)
        if k == 0:
            return MN("Från en kvadratisk skiva med sidan %d cm klipps lika stora kvadrater bort i hörnen, och sidorna viks upp till en låda utan lock. Hur stor ska sidan i hörnkvadraten vara för störst volym?" % L, x, [F(L, 4), F(L, 2), F(L, 3)], "V(x) = x(%d − 2x)². V%s(x) = 0 ger x = %d/6 = <b>%s cm</b>." % (L, P_, L, d(x)), "cm")
        return MN("Från en kvadratisk skiva med sidan %d cm görs en låda utan lock genom att klippa bort kvadrater med sidan x i hörnen. Vilken är den största volymen?" % L, V, [F(L, 4) * (L - 2 * F(L, 4)) ** 2, x * (L - x) ** 2, V / 2], "Maximum vid x = %s: V = %s · %s² = <b>%s cm³</b>." % (d(x), d(x), d(L - 2 * x), num(int(V))), "cm³")

    def kast():
        v = ri(8, 30)
        h0 = ri(1, 3)
        t = F(v, 10)
        H = h0 + v * t - 5 * t * t
        return MN("En boll kastas uppåt. Höjden är h(t) = %d + %dt − 5t² meter. Vid vilken tidpunkt är bollen som högst?" % (h0, v), t, [F(v, 5), F(v, 2), H], "h%s(t) = %d − 10t = 0 ger <b>t = %s s</b>." % (P_, v, d(t)), "s")

    def produkt():
        S = ri(6, 60) * 2
        k = ri(0, 1)
        if k == 0:
            return MN("Summan av två positiva tal är %d. Vilket är det största värdet produkten kan ha?" % S, F(S, 2) ** 2, [S * S, F(S, 2), F(S, 2) * (F(S, 2) - 1)], "P(x) = x(%d − x) är störst när x = %d: <b>%s</b>." % (S, S // 2, num(S * S // 4)))
        A = ri(2, 30) ** 2
        r = math.isqrt(A)
        return MN("En rektangel har arean %d cm². Vilken är den minsta omkrets den kan ha?" % A, 4 * r, [2 * (A + 1), 2 * r, A], "O(x) = 2x + %d/x. O%s(x) = 2 − %d/x² = 0 ger x = %d och O = <b>%d cm</b>." % (2 * A, P_, 2 * A, r, 4 * r), "cm")

    sets = [("Area med stängsel", [(staket, 20)]), ("Största vinst", [(vinst, 20)]), ("Lådan", [(lada, 20)]), ("Kast och rörelse", [(kast, 20)]), ("Summor, produkter och omkrets", [(produkt, 20)])]
    return U("optimering", "DI", "Optimering med derivata: största och minsta värde", "Optimering",
             "Algebraiska och grafiska metoder för att lösa optimeringsproblem med derivata.",
             "Uppgifter om optimering för Matematik 3c: area med stängsel, största vinst, lådproblemet, kast och rörelse samt summor och produkter. 100 uppgifter med facit.",
             "Ställ upp funktionen och sätt f′ = 0", "Kontrollera att det är ett maximum.", sets,
             ["Ställ upp en funktion för det som ska bli störst eller minst, uttryckt i en variabel.",
              "Derivera och sätt derivatan lika med 0. Kontrollera med teckentabell eller andraderivata att det är ett maximum eller minimum.",
              "Tänk på definitionsmängden: en längd kan inte vara negativ. Jämför också med värdena i ändpunkterna."],
             [("Summan 20, största produkt", ["P(x) = x(20 − x)", "P′(x) = 20 − 2x = 0", "x = 10"], "100")],
             [["Svarar med x i stället för det största värdet", "Läs vad som efterfrågas"], ["Glömmer att kontrollera max/min", "Använd f″ eller teckentabell"], ["Glömmer definitionsmängden", "Längder måste vara positiva"]],
             [("Vad är optimering?", "Att hitta det bästa värdet, till exempel störst area eller minst kostnad."), ("Kan jag lösa grafiskt?", "Ja, med räknare kan du läsa av maximum, men visa gärna derivatan."), ("Var används det?", "I ekonomi, teknik och design.")])


# ============================================================ primitiva funktioner
def primitiva():
    def polp():
        cs = rpol(ri(1, 3), -6, 6)
        cs = {e: c * (e + 1) for e, c in cs.items()}
        r = integ(cs)
        return M("Bestäm en primitiv funktion till f(x) = %s." % ps(cs), "F(x) = %s + C" % ps(r), ["F(x) = %s + C" % ps(deriv(cs)), "F(x) = %s + C" % ps({e + 1: c for e, c in cs.items()}), "F(x) = %s + C" % ps({e: F(c, e + 1) for e, c in cs.items()})],
                 "Öka exponenten med 1 och dela med den nya exponenten: <b>F(x) = %s + C</b>." % ps(r))

    def villkor():
        cs = {1: 2 * nz(-4, 4), 0: nz(-6, 6)}
        r = integ(cs)
        x0 = ri(0, 2)
        y0 = ri(-9, 9)
        C_ = y0 - ev(r, x0)
        res = dict(r)
        res[0] = C_
        return M("Bestäm den primitiva funktion F till f(x) = %s som uppfyller F(%d) = %s." % (ps(cs), x0, sg(y0)), "F(x) = %s" % ps(res), ["F(x) = %s" % ps(dict(list(r.items()) + [(0, y0)])), "F(x) = %s" % ps(dict(list(r.items()) + [(0, C_ + 1)])), "F(x) = %s" % ps({1: cs[1], 0: C_})],
                 "F(x) = %s + C. F(%d) = %s ger C = %s: <b>F(x) = %s</b>." % (ps(r), x0, sg(y0), sg(C_), ps(res)))

    def exp_():
        k, a = nz(-5, 5), nz(-6, 6)
        if a % k:
            return None
        return M("Bestäm en primitiv funktion till f(x) = %s." % ekx(k, a), "F(x) = %s + C" % ekx(k, F(a, k)), ["F(x) = %s + C" % ekx(k, a * k), "F(x) = %s + C" % ekx(k, a), "F(x) = %s + C" % ekx(k + 1, F(a, k + 1)) if k != -1 else "F(x) = %se<sup>x</sup> + C" % sg(a)],
                 "Primitiv till e<sup>kx</sup> är e<sup>kx</sup>/k: <b>F(x) = %s + C</b>." % ekx(k, F(a, k)))

    def kontroll():
        cs = rpol(2, -6, 6)
        Fc = integ(cs)
        Fc2 = dict(Fc)
        Fc2[0] = ri(-9, 9)
        good = "F(x) = %s" % ps(Fc2)
        return M("Vilken funktion är en primitiv funktion till f(x) = %s?" % ps(cs), good, ["F(x) = %s" % ps(deriv(cs)), "F(x) = %s" % ps({e + 1: c for e, c in cs.items()}), "F(x) = %s" % ps({e + 1: c * (e + 1) for e, c in cs.items()})],
                 "Kontrollera genom att derivera: F%s(x) = %s. <b>%s</b>." % (P_, ps(cs), good))

    def potensp():
        a = nz(-6, 6)
        n = ri(2, 3)
        return M("Bestäm en primitiv funktion till f(x) = %s." % frac_html(sg(a), xp(n)), "F(x) = %s + C" % ((MIN if a * F(1, n - 1) > 0 else "") + frac_html(fq(abs(F(a, n - 1))) if F(a, n - 1).denominator == 1 else fq(abs(F(a, n - 1))), xp(n - 1))),
                 ["F(x) = %s + C" % frac_html(sg(F(a, n - 1)), xp(n - 1)), "F(x) = %s + C" % frac_html(sg(-a * n), xp(n + 1)), "F(x) = %s + C" % frac_html(sg(a), xp(n + 1))],
                 "%sx%s har primitiven %sx%s: <b>%s</b>." % (sg(a), sup(-n), sg(F(-a, n - 1)), sup(1 - n), "F(x) = %s + C" % ((MIN if a > 0 else "") + frac_html(fq(abs(F(a, n - 1))), xp(n - 1)))))

    sets = [("Primitiva till polynom", [(polp, 20)]), ("Kontrollera genom derivering", [(kontroll, 20)]), ("Med villkor", [(villkor, 20)]), ("Exponentialfunktioner", [(exp_, 20)]), ("Blandat", [(polp, 6), (potensp, 8), (exp_, 6)])]
    return U("primitiva-funktioner", "DI", "Primitiva funktioner: polynom och eˣ", "Primitiva funktioner",
             "Begreppet primitiv funktion. Primitiva funktioner till polynom och exponentialfunktioner, med och utan villkor.",
             "Uppgifter om primitiva funktioner för Matematik 3c: polynom, kontroll genom derivering, primitiva med villkor, exponentialfunktioner och potenser. 100 uppgifter med facit.",
             "F′(x) = f(x)", "Glöm inte konstanten C.", sets,
             ["F är en primitiv funktion till f om F′(x) = f(x). Det finns oändligt många, som skiljer sig med en konstant C.",
              "Till xⁿ är en primitiv funktion xⁿ⁺¹/(n + 1). Till e<sup>kx</sup> är den e<sup>kx</sup>/k.",
              "Ett villkor som F(0) = 3 bestämmer konstanten C."],
             [("f(x) = 6x² − 4x", ["2x³ − 2x² + C"], "F(x) = 2x³ − 2x² + C")],
             [["Deriverar i stället för att integrera", "Exponenten ska öka"], ["Glömmer att dela med nya exponenten", "x² ger x³/3"], ["Glömmer C", "Skriv + C"]],
             [("Varför + C?", "Derivatan av en konstant är 0, så alla F + C har samma derivata."), ("Hur kontrollerar jag?", "Derivera F och se att du får f."), ("Vad används primitiva funktioner till?", "För att beräkna integraler.")])


# ============================================================ integraler
def integraler():
    def bestamd():
        cs = rpol(ri(1, 2), -5, 5)
        cs = {e: c * (e + 1) for e, c in cs.items()}
        a = ri(-2, 1)
        b = a + ri(1, 3)
        Fc = integ(cs)
        v = ev(Fc, b) - ev(Fc, a)
        return MN("Beräkna ∫<sub>%s</sub><sup>%s</sup> (%s) dx." % (sg(a), sg(b), ps(cs)), v, [ev(cs, b) - ev(cs, a), ev(Fc, b), ev(Fc, b) + ev(Fc, a)], "[%s] från %s till %s = %s − %s = <b>%s</b>." % (ps(Fc), sg(a), sg(b), sg(ev(Fc, b)), par(ev(Fc, a)), sg(v)))

    def area():
        a = ri(1, 3)
        b = ri(2, 6)
        k = ri(0, 1)
        if k == 0:
            v = F(b ** 3, 3) * a
            pic = graf(lambda x: a * x * x, (-1, b + 1, 1), (-2, a * b * b + 2, max(1, a * b * b // 6)), [], "parabel")
            return MN("Beräkna arean mellan kurvan y = %s, x-axeln och linjen x = %d." % (pol({2: a}), b), v, [a * b * b, F(a * b * b, 2), v * 3], "∫<sub>0</sub><sup>%d</sup> %s dx = [%s] = <b>%s a.e.</b>" % (b, pol({2: a}), ps({3: F(a, 3)}), sg(v)), "a.e.")
        c = ri(b * b + 1, b * b + 20)
        v = c * b - F(b ** 3, 3)
        return MN("Beräkna arean under kurvan y = %d − x² mellan x = 0 och x = %d." % (c, b), v, [c * b - b ** 2, c - F(b ** 3, 3), c * b], "∫<sub>0</sub><sup>%d</sup> (%d − x²) dx = %d − %s = <b>%s a.e.</b>" % (b, c, c * b, sg(F(b ** 3, 3)), sg(v)), "a.e.")

    def stracka():
        a = ri(1, 4)
        b = ri(0, 10)
        T = ri(2, 10)
        s = F(a * T * T, 2) + b * T
        return MN("Hastigheten är v(t) = %s m/s. Hur lång sträcka färdas föremålet de första %d sekunderna?" % (ps({1: a, 0: b}, "t"), T), s, [a * T + b, a * T * T + b * T, s + T], "∫<sub>0</sub><sup>%d</sup> v(t) dt = [%s] = <b>%s m</b>." % (T, ps({2: F(a, 2), 1: b}, "t"), d(s)), "m")

    def expi():
        k = ri(1, 3)
        b = ri(1, 3)
        c = ri(1, 8)
        v = c * (math.exp(k * b) - 1) / k
        cc = "" if c == 1 else "%d" % c
        return M("Beräkna ∫<sub>0</sub><sup>%d</sup> %se<sup>%sx</sup> dx. Avrunda till en decimal." % (b, cc, "" if k == 1 else str(k)), fl(v, 1), [fl(c * math.exp(k * b), 1), fl(c * math.exp(k * b) * k, 1), fl(v * k, 1) if k > 1 else fl(c * math.exp(b) + 1, 1)],
                 "[%s · e<sup>%sx</sup>/%d] från 0 till %d = %d(e<sup>%d</sup> − 1)/%d ≈ <b>%s</b>." % (c, "" if k == 1 else str(k), k, b, c, k * b, k, fl(v, 1)))

    def tolka():
        P = [("Vad betyder ∫<sub>0</sub><sup>%d</sup> v(t) dt om v(t) är hastigheten i m/s?", "Sträckan i meter under de första %d sekunderna", ["Hastigheten efter %d sekunder", "Accelerationen", "Medelhastigheten"]),
             ("Vad betyder ∫<sub>0</sub><sup>%d</sup> f(t) dt om f(t) är vattenflödet i liter per minut?", "Vattenmängden i liter som flödat under %d minuter", ["Flödet efter %d minuter", "Hur snabbt flödet ändras", "Den största vattenmängden"]),
             ("Vad betyder ∫<sub>0</sub><sup>%d</sup> P(t) dt om P(t) är effekten i kW och t är timmar?", "Energin i kWh under %d timmar", ["Effekten efter %d timmar", "Den högsta effekten", "Hur snabbt effekten ändras"])]
        t = ri(2, 12)
        q, r, w = ch(P)
        return M(q % t, r % t, [x % t if "%d" in x else x for x in w], "Integralen summerar en hastighet över tid: <b>%s</b>." % (r % t).lower())

    sets = [("Bestämda integraler", [(bestamd, 20)]), ("Area under kurvor", [(area, 20)]), ("Sträcka ur hastighet", [(stracka, 20)]), ("Integraler med e", [(expi, 20)]), ("Tolka integraler", [(tolka, 8), (bestamd, 12)])]
    return U("integraler", "DI", "Integraler: bestämda integraler och area", "Integraler",
             "Begreppet bestämd integral och sambandet mellan integral och derivata. Integraler för att beräkna area och tolka förändring.",
             "Uppgifter om integraler för Matematik 3c: bestämda integraler, area under kurvor, sträcka ur hastighet, integraler med e och tolkning. 100 uppgifter med facit.",
             "∫ från a till b f(x) dx = F(b) − F(a)", "Integralen är arean under kurvan.", sets,
             ["Den bestämda integralen ∫<sub>a</sub><sup>b</sup> f(x) dx = F(b) − F(a), där F är en primitiv funktion till f.",
              "Om f(x) ≥ 0 är integralen arean mellan kurvan och x-axeln från a till b.",
              "Integralen av en hastighet ger den totala förändringen, till exempel sträcka ur fart."],
             [("∫ från 1 till 3 av 2x dx", ["[x²] = 9 − 1"], "8"), ("v(t) = 2t + 1, 0 till 4 s", ["[t² + t] = 16 + 4"], "20 m")],
             [["F(a) − F(b)", "Övre gränsen först: F(b) − F(a)"], ["Sätter in i f i stället för F", "Använd den primitiva funktionen"], ["Glömmer att dela med exponenten", "x² ger x³/3"]],
             [("Varför försvinner C?", "C tar ut sig när man beräknar F(b) − F(a)."), ("Vad händer om kurvan är under x-axeln?", "Integralen blir negativ. Arean är då beloppet."), ("Vad är a.e.?", "Areaenheter.")])


# ============================================================ triangelsatser
def triangel():
    def sinr():
        A = ri(25, 80)
        B = ri(25, 80)
        if A + B > 150:
            return None
        a = ri(5, 30)
        b = a * math.sin(math.radians(B)) / math.sin(math.radians(A))
        return M("I triangeln ABC är vinkel A = %d°, vinkel B = %d° och sidan a = %d cm. Beräkna sidan b. Avrunda till en decimal." % (A, B, a), "%s cm" % fl(b, 1), ["%s cm" % fl(a * math.sin(math.radians(A)) / math.sin(math.radians(B)), 1), "%s cm" % fl(a * B / float(A), 1), "%s cm" % fl(a * math.sin(math.radians(B)), 1)],
                 "Sinussatsen: b = a · sin B / sin A = %d · sin %d° / sin %d° ≈ <b>%s cm</b>." % (a, B, A, fl(b, 1)))

    def cosr():
        b, c = ri(4, 20), ri(4, 20)
        A = ri(30, 140)
        a = math.sqrt(b * b + c * c - 2 * b * c * math.cos(math.radians(A)))
        return M("I triangeln ABC är b = %d cm, c = %d cm och vinkel A = %d°. Beräkna a. Avrunda till en decimal." % (b, c, A), "%s cm" % fl(a, 1), ["%s cm" % fl(math.sqrt(b * b + c * c), 1), "%s cm" % fl(math.sqrt(b * b + c * c + 2 * b * c * math.cos(math.radians(A))), 1), "%s cm" % fl(b + c - a / 3, 1)],
                 "Cosinussatsen: a² = %d² + %d² − 2 · %d · %d · cos %d° ger <b>a ≈ %s cm</b>." % (b, c, b, c, A, fl(a, 1)))

    def vinkel():
        a, b, c = ri(4, 15), ri(4, 15), ri(4, 15)
        if not (a < b + c and b < a + c and c < a + b):
            return None
        A = math.degrees(math.acos((b * b + c * c - a * a) / (2.0 * b * c)))
        return M("En triangel har sidorna a = %d cm, b = %d cm och c = %d cm. Beräkna vinkel A. Avrunda till en decimal." % (a, b, c), "%s°" % fl(A, 1), ["%s°" % fl(180 - A, 1), "%s°" % fl(math.degrees(math.acos((a * a + c * c - b * b) / (2.0 * a * c))), 1), "%s°" % fl(A / 2 + 20, 1)],
                 "cos A = (b² + c² − a²)/(2bc) = %s. <b>A ≈ %s°</b>." % (fl((b * b + c * c - a * a) / (2.0 * b * c), 3), fl(A, 1)))

    def areas():
        a, b = ri(3, 20), ri(3, 20)
        C_ = ri(20, 160)
        T = a * b * math.sin(math.radians(C_)) / 2
        return M("Två sidor i en triangel är %d cm och %d cm och vinkeln mellan dem är %d°. Beräkna arean. Avrunda till en decimal." % (a, b, C_), "%s cm²" % fl(T, 1), ["%s cm²" % fl(T * 2, 1), "%s cm²" % fl(a * b / 2.0, 1), "%s cm²" % fl(a * b * math.cos(math.radians(C_)) / 2, 1) if abs(math.cos(math.radians(C_))) > 0.05 else "%s cm²" % fl(T + 5, 1)],
                 "Areasatsen: T = ab · sin C / 2 = %d · %d · sin %d° / 2 ≈ <b>%s cm²</b>." % (a, b, C_, fl(T, 1)))

    def val_():
        P = [("Du känner två vinklar och en sida.", "Sinussatsen"), ("Du känner tre sidor och söker en vinkel.", "Cosinussatsen"), ("Du känner två sidor och mellanliggande vinkel och söker tredje sidan.", "Cosinussatsen"),
             ("Du känner två sidor och mellanliggande vinkel och söker arean.", "Areasatsen"), ("Du känner två sidor och en vinkel mitt emot en av dem.", "Sinussatsen")]
        q, r = ch(P)
        a, b = ri(3, 12), ri(3, 12)
        return M("%s Vilken sats använder du? (Exempel: %d cm och %d cm.)" % (q, a, b), r, [x for x in ("Sinussatsen", "Cosinussatsen", "Areasatsen", "Pythagoras sats") if x != r], "<b>%s</b>." % r)

    sets = [("Sinussatsen", [(sinr, 20)]), ("Cosinussatsen", [(cosr, 20)]), ("Beräkna en vinkel", [(vinkel, 20)]), ("Areasatsen", [(areas, 20)]), ("Välj sats", [(val_, 8), (sinr, 6), (areas, 6)])]
    return U("triangelsatser", "TV", "Triangelsatserna: sinussatsen, cosinussatsen och areasatsen", "Triangelsatser",
             "Bevis och användning av cosinus-, sinus- och areasatsen för en godtycklig triangel.",
             "Uppgifter om triangelsatser för Matematik 3c: sinussatsen, cosinussatsen, beräkna en vinkel, areasatsen och välja rätt sats. 100 uppgifter med facit.",
             "a/sin A = b/sin B = c/sin C", "a² = b² + c² − 2bc cos A", sets,
             ["Sinussatsen a/sin A = b/sin B = c/sin C används när du känner en sida och vinkeln mitt emot.",
              "Cosinussatsen a² = b² + c² − 2bc · cos A används med tre sidor eller två sidor och mellanliggande vinkel.",
              "Areasatsen T = ab · sin C / 2 ger arean ur två sidor och vinkeln mellan dem."],
             [("b = 5, c = 7, A = 60°", ["a² = 25 + 49 − 70 · 0,5 = 39"], "a ≈ 6,2")],
             [["Räknaren i radianer", "Ställ in grader"], ["Fel vinkel mitt emot sidan", "a står mitt emot A"], ["+ i stället för − i cosinussatsen", "a² = b² + c² − 2bc cos A"]],
             [("Gäller satserna i alla trianglar?", "Ja, även i trianglar utan rät vinkel."), ("Vad är specialfallet av cosinussatsen?", "Pythagoras sats när A = 90°."), ("Kan sinussatsen ge två lösningar?", "Ja, när man söker en vinkel kan det finnas två trianglar.")])


UNITS = {"absolutbelopp-och-rationella-uttryck": rationella, "polynom": polynom, "gransvarden": gransvarden, "derivatans-definition": definition, "deriveringsregler": regler,
         "tangenter": tangenter, "talet-e-och-ln": tal_e, "extrempunkter-och-andraderivata": extrem, "optimering": optimering, "primitiva-funktioner": primitiva,
         "integraler": integraler, "triangelsatser": triangel}
