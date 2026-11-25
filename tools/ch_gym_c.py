# -*- coding: utf-8 -*-
"""Schweiz Gymnasium: Ableitung und Tangente, Ableitungsregeln, Kurvendiskussion, Extremwertaufgaben, Stammfunktionen, Integrale und Flächen, statistische Kennzahlen"""
import math
from fractions import Fraction as Fr
import de_common as D
from ch_gym import mcq, z, fz, par, poly, lin, ri, sup, MI, NB

E = lambda s: "e<sup>%s</sup>" % s


def deriv(c):
    return {e - 1: k * e for e, k in c.items() if e != 0}


def integ(c):
    return {e + 1: Fr(k, e + 1) for e, k in c.items()}


def ev(c, x):
    return sum(Fr(k) * Fr(x) ** e for e, k in c.items())


def rpoly(R, deg, lo=-5, hi=5, lead_nz=True):
    c = {e: R.randint(lo, hi) for e in range(deg + 1)}
    if lead_nz and c[deg] == 0:
        c[deg] = R.choice([1, 2, -1, 3])
    return c


def F_(c, name="f"):
    return "%s(x) = %s" % (name, poly(c))


# ============================================================ Ableitung und Tangente
def tangente(R):
    def rate():
        a, b, c = ri(R, -3, 3, (0,)), ri(R, -5, 5), ri(R, -5, 5)
        f = {2: a, 1: b, 0: c}
        x1 = ri(R, -4, 3)
        x2 = x1 + R.randint(1, 4)
        m = (ev(f, x2) - ev(f, x1)) / (x2 - x1)
        return mcq("Wie gross ist die mittlere Änderungsrate von %s im Intervall [%s; %s]?" % (F_(f), z(x1), z(x2)), fz(m),
                   [fz(ev(f, x2) - ev(f, x1)), fz(ev(deriv(f), x1)), fz((ev(f, x2) + ev(f, x1)) / (x2 - x1))],
                   "(f(%s) − f(%s)) : (%s − %s) = (%s − %s) : %d = <b>%s</b>." % (z(x2), z(x1), z(x2), par(x1), z(ev(f, x2)), par(ev(f, x1)), x2 - x1, fz(m)))

    def hmeth():
        a, x0 = ri(R, 1, 4), ri(R, -5, 6, (0,))
        good = "%s" % poly({"h": a, 0: 2 * a * x0})
        return mcq("Für f(x) = %s gilt (f(%s + h) − f(%s)) : h = …" % (poly({2: a}), z(x0), z(x0)), good,
                   [z(2 * a * x0), poly({"h": a, 0: a * x0 * x0}), poly({"h²": a, "h": 2 * a * x0})],
                   "f(%s + h) = %s(%s + h)² = %s. Minus f(%s), durch h teilen: <b>%s</b>. Für h → 0: f′(%s) = %s." % (
                       z(x0), "" if a == 1 else z(a), z(x0), poly({"h²": a, "h": 2 * a * x0, 0: a * x0 * x0}), z(x0), good, z(x0), z(2 * a * x0)))

    def steig():
        f = rpoly(R, 3, -4, 4)
        x0 = ri(R, -3, 3)
        m = ev(deriv(f), x0)
        return mcq("Wie gross ist die Steigung des Graphen von %s an der Stelle x = %s?" % (F_(f), z(x0)), z(m),
                   [z(ev(f, x0)), z(ev(deriv(f), -x0)) if ev(deriv(f), -x0) != m else z(m + 1), z(ev({e: k * e for e, k in f.items()}, x0) + 1)],
                   "f′(x) = %s, f′(%s) = <b>%s</b>." % (poly(deriv(f)), z(x0), z(m)))

    def tang():
        a, b, c = ri(R, -3, 3, (0,)), ri(R, -6, 6), ri(R, -6, 6)
        f = {2: a, 1: b, 0: c}
        x0 = ri(R, -3, 3)
        m, y0 = ev(deriv(f), x0), ev(f, x0)
        q = y0 - m * x0
        g = lambda mm, qq: "y = %s" % lin(mm, qq) if mm else "y = %s" % z(qq)
        good = g(m, q)
        return mcq("Wie lautet die Gleichung der Tangente an den Graphen von %s im Punkt mit x = %s?" % (F_(f), z(x0)), good,
                   [g(m, y0) if y0 != q else g(m, q + 1), g(y0, q) if y0 != m else g(m + 1, q), g(m, q + 2 * m * x0) if m * x0 else g(-m, q)],
                   "f(%s) = %s, f′(%s) = %s. y = %s · (x − %s) + %s ⇒ <b>%s</b>." % (z(x0), z(y0), z(x0), z(m), z(m), par(x0), par(y0), good))

    def normal():
        a, b = ri(R, -3, 3, (0,)), ri(R, -6, 6)
        f = {2: a, 1: b, 0: ri(R, -5, 5)}
        x0 = ri(R, -3, 3)
        m = ev(deriv(f), x0)
        if m == 0:
            return None
        return mcq("Welche Steigung hat die Normale an den Graphen von %s an der Stelle x = %s?" % (F_(f), z(x0)), fz(Fr(-1) / m),
                   [fz(m), fz(-m), fz(Fr(1) / m)],
                   "Tangente: m = %s. Normale steht senkrecht: m<sub>n</sub> = −1 : m = <b>%s</b>." % (z(m), fz(Fr(-1) / m)))

    def stelle():
        a, b, c = ri(R, -3, 3, (0,)), ri(R, -8, 8), ri(R, -5, 5)
        f = {2: a, 1: b, 0: c}
        x0 = ri(R, -5, 5)
        m = 2 * a * x0 + b
        return mcq("An welcher Stelle hat der Graph von %s die Steigung %s?" % (F_(f), z(m)), "x = %s" % z(x0),
                   ["x = %s" % fz(Fr(m - b, a)), "x = %s" % fz(Fr(m, 2 * a)), "x = %s" % z(-x0) if x0 else "x = 1"],
                   "f′(x) = %s = %s ⇒ x = <b>%s</b>." % (lin(2 * a, b), z(m), z(x0)))

    return dict(
        title="Ableitung, Tangente und Normale",
        short="Ableitung und Tangente",
        meta="Differenzialrechnung am Gymnasium: mittlere Änderungsrate, Differenzenquotient, Steigung an einer Stelle, Tangentengleichung und Normale. 100 Aufgaben mit Lösungen.",
        kb="f′(x0) ist die Steigung der Tangente im Punkt (x0 | f(x0)).",
        ks="Tangente: y = f′(x0) · (x − x0) + f(x0)",
        think=["Die <b>mittlere Änderungsrate</b> auf [a; b] ist (f(b) − f(a)) : (b − a), die Steigung der Sekante.",
               "Lässt man den Abstand h gegen 0 gehen, wird aus der Sekante die Tangente: f′(x<sub>0</sub>) = lim (f(x<sub>0</sub> + h) − f(x<sub>0</sub>)) : h.",
               "Potenzregel: (x<sup>n</sup>)′ = n · x<sup>n − 1</sup>.",
               "Tangente in x<sub>0</sub>: y = f′(x<sub>0</sub>) · (x − x<sub>0</sub>) + f(x<sub>0</sub>). Die <b>Normale</b> hat die Steigung −1 : f′(x<sub>0</sub>)."],
        ex=[("f(x) = x², Tangente bei x = 3", ["f(3) = 9, f′(x) = 2x, f′(3) = 6", "y = 6(x − 3) + 9"], "y = 6x − 9"),
            ("f(x) = x³ − 2x, Steigung bei x = 1", ["f′(x) = 3x² − 2"], "f′(1) = 1")],
        mist=[["Steigung bei x₀ = f(x₀)", "Die Steigung ist f′(x₀), nicht der Funktionswert"],
              ["Tangente: y = f′(x₀) · x + f(x₀)", "Den Punkt einsetzen: y = f′(x₀)(x − x₀) + f(x₀)"],
              ["Normale: Steigung −f′(x₀)", "Negativer Kehrwert: −1 : f′(x₀)"]],
        faq=[{"q": "Was ist die Ableitung anschaulich?", "a": "Die Steigung des Graphen an einer Stelle, also die momentane Änderungsrate."},
             {"q": "Was ist der Unterschied zwischen Sekante und Tangente?", "a": "Die Sekante geht durch zwei Punkte des Graphen. Die Tangente berührt den Graphen in einem Punkt und hat dort dieselbe Steigung."},
             {"q": "Wie stelle ich die Tangentengleichung auf?", "a": "f(x0) und f′(x0) berechnen und in y = f′(x0) · (x − x0) + f(x0) einsetzen."},
             {"q": "Was ist die Normale?", "a": "Die Gerade, die im Berührpunkt senkrecht auf der Tangente steht. Ihre Steigung ist −1 : f′(x0)."}],
        sets=[("Mittlere Änderungsrate", [(rate, 20)]), ("Vom Differenzenquotienten zur Ableitung", [(hmeth, 20)]), ("Steigung an einer Stelle", [(steig, 12), (stelle, 8)]),
              ("Tangentengleichungen", [(tang, 20)]), ("Normale und Steigung", [(normal, 12), (stelle, 8)])])


# ============================================================ Ableitungsregeln
def regeln(R):
    def potenz():
        k = R.choice(["poly", "neg", "wurzel"])
        if k == "poly":
            f = rpoly(R, R.choice([3, 4, 5]), -6, 6)
            good = poly(deriv(f))
            bad = [poly({e: k_ * e for e, k_ in f.items()}), poly({e - 1: k_ for e, k_ in f.items() if e}), poly({e - 1: k_ * e for e, k_ in f.items() if e} | {0: f.get(0, 0)})]
            return mcq("Bilde die Ableitung von %s." % F_(f), "f′(x) = " + good, ["f′(x) = " + b for b in bad], "Potenzregel gliedweise, Konstante fällt weg: <b>f′(x) = %s</b>." % good)
        if k == "neg":
            a, n = ri(R, -6, 6, (0,)), R.randint(1, 4)
            f = "f(x) = %s : x%s" % (z(a), "" if n == 1 else sup(n))
            good = "f′(x) = %s" % poly({-(n + 1): -a * n})
            return mcq("Bilde die Ableitung von %s." % f, good, ["f′(x) = %s" % poly({-(n - 1): -a * n}) if n > 1 else "f′(x) = %s" % z(-a), "f′(x) = %s" % poly({-(n + 1): a * n}),
                                                                 "f′(x) = %s" % poly({-n: -a * n})],
                       "%s : x%s = %s. Potenzregel: <b>%s</b>." % (z(a), "" if n == 1 else sup(n), poly({-n: a}), good))
        a = R.choice([1, 2, 3, 4, 6, -2])
        good = "f′(x) = %s : √x" % fz(Fr(a, 2)) if a != 2 else "f′(x) = 1 : √x"
        return mcq("Bilde die Ableitung von f(x) = %s√x." % ("" if a == 1 else z(a)), good,
                   ["f′(x) = %s√x" % fz(Fr(a, 2)), "f′(x) = %s : √x" % z(a * 2), "f′(x) = %s : √x" % z(a)],
                   "√x = x<sup>½</sup>, Ableitung ½x<sup>−½</sup> = 1 : (2√x). Mal %s: <b>%s</b>." % (z(a), good))

    def produkt():
        n, t = R.randint(1, 4), R.choice(["exp", "sin", "cos", "lin"])
        xn = "x" + ("" if n == 1 else sup(n))
        dn = poly({n - 1: n}) if n > 1 else "1"
        if t == "exp":
            f, good = "%s · %s" % (xn, E("x")), "(%s) · %s" % (poly({n: 1, n - 1: n}), E("x"))
            bad = ["%s · %s" % (dn, E("x")), "%s · %s" % (xn, E("x")), "(%s) · %s" % (poly({n: 1, n - 1: -n}), E("x"))]
        elif t == "sin":
            f, good = "%s · sin x" % xn, "%s · sin x + %s · cos x" % (dn, xn)
            bad = ["%s · cos x" % dn, "%s · sin x − %s · cos x" % (dn, xn), "%s · cos x + %s · sin x" % (dn, xn)]
        elif t == "cos":
            f, good = "%s · cos x" % xn, "%s · cos x − %s · sin x" % (dn, xn)
            bad = ["−%s · sin x" % dn, "%s · cos x + %s · sin x" % (dn, xn), "%s · sin x − %s · cos x" % (dn, xn)]
        else:
            a, b, c, d = ri(R, 1, 5), ri(R, -6, 6, (0,)), ri(R, 1, 5), ri(R, -6, 6, (0,))
            f = "(%s) · (%s)" % (lin(a, b), lin(c, d))
            good = poly({1: 2 * a * c, 0: a * d + b * c})
            bad = [z(a * c), poly({1: a * c, 0: a * d + b * c}), poly({1: 2 * a * c, 0: a * d - b * c})]
        return mcq("Bilde die Ableitung von f(x) = %s mit der Produktregel." % f, "f′(x) = " + good, ["f′(x) = " + b for b in bad],
                   "(u · v)′ = u′ · v + u · v′: <b>f′(x) = %s</b>." % good)

    def quot():
        while True:
            a, b, c, d = ri(R, -5, 5, (0,)), ri(R, -6, 6), ri(R, 1, 4), ri(R, -6, 6, (0,))
            if a * d - b * c:
                break
        good = "f′(x) = %s : (%s)²" % (z(a * d - b * c), lin(c, d))
        return mcq("Bilde die Ableitung von f(x) = (%s) : (%s)." % (lin(a, b), lin(c, d)), good,
                   ["f′(x) = %s : (%s)²" % (z(a * d + b * c), lin(c, d)), "f′(x) = %s" % fz(Fr(a, c)), "f′(x) = %s : (%s)²" % (z(b * c - a * d), lin(c, d))],
                   "(u : v)′ = (u′v − uv′) : v² = (%s · (%s) − (%s) · %s) : (%s)² ⇒ <b>%s</b>." % (z(a), lin(c, d), lin(a, b), z(c), lin(c, d), good))

    def kette():
        t = R.choice(["pot", "exp", "sin", "ln", "cos"])
        if t == "pot":
            a, b, n = ri(R, 2, 5), ri(R, -7, 7, (0,)), R.randint(2, 6)
            u = "(%s)" % lin(a, b)
            good = "%s%s%s" % (z(n * a), u, "" if n == 2 else sup(n - 1))
            f = "%s%s" % (u, sup(n))
            bad = ["%s%s%s" % (z(n), u, "" if n == 2 else sup(n - 1)), "%s%s%s" % (z(n * a), u, sup(n)), "%s%s" % (z(a), u if n == 2 else u + sup(n - 1))]
        elif t == "exp":
            k = ri(R, -5, 6, (0, 1))
            f = E(poly({1: k}))
            good, bad = "%s%s" % (z(k), E(poly({1: k}))), [E(poly({1: k})), "%s%s" % (poly({1: k}), E(poly({1: k - 1}))), "%s%s" % (z(k), E("x"))]
        elif t == "sin":
            k = ri(R, 2, 6)
            f, good = "sin(%sx)" % z(k), "%scos(%sx)" % (z(k), z(k))
            bad = ["cos(%sx)" % z(k), "−%scos(%sx)" % (z(k), z(k)), "%scos x" % z(k)]
        elif t == "cos":
            k = ri(R, 2, 6)
            f, good = "cos(%sx)" % z(k), "−%ssin(%sx)" % (z(k), z(k))
            bad = ["%ssin(%sx)" % (z(k), z(k)), "−sin(%sx)" % z(k), "−%ssin x" % z(k)]
        else:
            a, b = ri(R, 2, 6), ri(R, -6, 6, (0,))
            f, good = "ln(%s)" % lin(a, b), "%s : (%s)" % (z(a), lin(a, b))
            bad = ["1 : (%s)" % lin(a, b), "%s : x" % z(a), "ln(%s)" % z(a)]
        return mcq("Bilde mit der Kettenregel die Ableitung von f(x) = %s." % f, "f′(x) = " + good, ["f′(x) = " + b for b in bad],
                   "Äussere Ableitung mal innere Ableitung: <b>f′(x) = %s</b>." % good)

    def spez():
        a, b = ri(R, -6, 6, (0,)), ri(R, -6, 6, (0,))
        t = R.choice(["sc", "ex", "ln"])
        if t == "sc":
            f = "%s sin x %s %s cos x" % (z(a), "+" if b > 0 else "−", z(abs(b)))
            good = "%s cos x %s %s sin x" % (z(a), "−" if b > 0 else "+", z(abs(b)))
            bad = ["%s cos x %s %s sin x" % (z(a), "+" if b > 0 else "−", z(abs(b))), "%s cos x %s %s sin x" % (z(-a), "−" if b > 0 else "+", z(abs(b))),
                   "%s sin x %s %s cos x" % (z(a), "−" if b > 0 else "+", z(abs(b)))]
        elif t == "ex":
            f = "%s%s %s %s" % (z(a) if a not in (1, -1) else ("−" if a < 0 else ""), E("x"), "+" if b > 0 else "−", poly({2: abs(b)}))
            good = "%s%s %s %s" % (z(a) if a not in (1, -1) else ("−" if a < 0 else ""), E("x"), "+" if b > 0 else "−", poly({1: 2 * abs(b)}))
            bad = ["%s%s %s %s" % (z(a) if a not in (1, -1) else ("−" if a < 0 else ""), E("x − 1"), "+" if b > 0 else "−", poly({1: 2 * abs(b)})),
                   "%s%s %s %s" % (z(a) if a not in (1, -1) else ("−" if a < 0 else ""), E("x"), "+" if b > 0 else "−", poly({1: abs(b)})),
                   "%s%s" % (z(a) if a not in (1, -1) else ("−" if a < 0 else ""), E("x"))]
        else:
            f = "%s ln x %s %s" % (z(a), "+" if b > 0 else "−", poly({1: abs(b)}))
            good = "%s : x %s %s" % (z(a), "+" if b > 0 else "−", z(abs(b)))
            bad = ["%s : x" % z(a), "%s ln x %s %s" % (z(a), "+" if b > 0 else "−", z(abs(b))), "%s x %s %s" % (z(a), "+" if b > 0 else "−", z(abs(b)))]
        return mcq("Bilde die Ableitung von f(x) = %s." % f, "f′(x) = " + good, ["f′(x) = " + b_ for b_ in bad],
                   "(sin x)′ = cos x, (cos x)′ = −sin x, (eˣ)′ = eˣ, (ln x)′ = 1 : x. Ergebnis: <b>f′(x) = %s</b>." % good)

    return dict(
        title="Ableitungsregeln: Potenz-, Produkt-, Quotienten- und Kettenregel",
        short="Ableitungsregeln",
        meta="Ableitungsregeln am Gymnasium: Potenz- und Summenregel, Ableitungen von sin, cos, eˣ und ln x, Produktregel, Quotientenregel und Kettenregel. 100 Aufgaben mit Lösungen.",
        kb="Produkt: u′v + uv′. Kette: äussere mal innere Ableitung.",
        ks="Quotient: (u′v − uv′) : v²",
        think=["Potenzregel: (x<sup>n</sup>)′ = n · x<sup>n − 1</sup>, auch für negative und gebrochene Exponenten. Konstanten fallen weg.",
               "(sin x)′ = cos x, (cos x)′ = −sin x, (e<sup>x</sup>)′ = e<sup>x</sup>, (ln x)′ = 1 : x.",
               "<b>Produktregel</b>: (u · v)′ = u′ · v + u · v′.",
               "<b>Quotientenregel</b>: (u : v)′ = (u′ · v − u · v′) : v².",
               "<b>Kettenregel</b>: f(g(x))′ = f′(g(x)) · g′(x), also äussere mal innere Ableitung."],
        ex=[("f(x) = x² · eˣ", ["u = x², v = eˣ", "2x · eˣ + x² · eˣ"], "(x² + 2x) · eˣ"),
            ("f(x) = (3x − 1)⁴", ["äussere: 4(3x − 1)³", "innere: 3"], "12(3x − 1)³")],
        mist=[["(u · v)′ = u′ · v′", "Produktregel: u′v + uv′"],
              ["((3x − 1)⁴)′ = 4(3x − 1)³", "Mit der inneren Ableitung 3 multiplizieren"],
              ["(cos x)′ = sin x", "(cos x)′ = −sin x"]],
        faq=[{"q": "Wann brauche ich die Kettenregel?", "a": "Wenn eine Funktion in eine andere eingesetzt ist, zum Beispiel (3x − 1)⁴, e hoch 2x oder sin(5x)."},
             {"q": "Wie leite ich 1 : x ab?", "a": "1 : x = x hoch −1. Mit der Potenzregel: −1 · x hoch −2 = −1 : x²."},
             {"q": "Was ist die Ableitung von √x?", "a": "√x = x hoch ½, also ½ · x hoch −½ = 1 : (2√x)."},
             {"q": "Warum ist die Ableitung von eˣ wieder eˣ?", "a": "Die Steigung von eˣ ist an jeder Stelle gleich dem Funktionswert. Das macht die Zahl e besonders."}],
        sets=[("Potenz- und Summenregel", [(potenz, 20)]), ("sin, cos, eˣ und ln x", [(spez, 20)]), ("Produktregel", [(produkt, 20)]),
              ("Quotientenregel", [(quot, 20)]), ("Kettenregel", [(kette, 20)])])


# ============================================================ Kurvendiskussion
def kurven(R):
    def cubic():
        while True:
            p, q = sorted(R.sample(range(-4, 5), 2))
            k = R.choice([3, -3, 6, -6])
            if (k * (p + q)) % 2 == 0:
                break
        c0 = ri(R, -6, 6)
        f = {3: Fr(k, 3), 2: Fr(-k * (p + q), 2), 1: k * p * q, 0: c0}
        return f, p, q, k

    def extr():
        f, p, q, k = cubic()
        good = "x = %s und x = %s" % (z(p), z(q))
        return mcq("An welchen Stellen hat %s waagrechte Tangenten?" % F_(f), good,
                   ["x = %s und x = %s" % (z(-q), z(-p)), "x = %s" % fz(Fr(p + q, 2)), "x = 0 und x = %s" % z(p + q)],
                   "f′(x) = %s = %s(%s)(%s) = 0 ⇒ <b>%s</b>." % (poly(deriv(f)), z(k), lin(1, -p), lin(1, -q), good))

    def art():
        f, p, q, k = cubic()
        x0 = R.choice([p, q])
        y0 = ev(f, x0)
        hoch = (k > 0 and x0 == p) or (k < 0 and x0 == q)
        good = ("Hochpunkt H(%s" if hoch else "Tiefpunkt T(%s") % ("%s%s|%s%s)" % (z(x0), NB, NB, fz(y0)))
        other = ("Tiefpunkt T(%s" if hoch else "Hochpunkt H(%s") % ("%s%s|%s%s)" % (z(x0), NB, NB, fz(y0)))
        return mcq("%s hat bei x = %s eine waagrechte Tangente. Was liegt dort vor?" % (F_(f), z(x0)), good,
                   [other, "Wendepunkt W(%s%s|%s%s)" % (z(x0), NB, NB, fz(y0)), ("Hochpunkt H(%s" if hoch else "Tiefpunkt T(%s") % ("%s%s|%s%s)" % (z(x0), NB, NB, fz(y0 + 1)))],
                   "f″(x) = %s, f″(%s) = %s %s 0 ⇒ <b>%s</b>." % (poly(deriv(deriv(f))), z(x0), z(ev(deriv(deriv(f)), x0)), "&lt;" if hoch else "&gt;", good))

    def wende():
        f, p, q, k = cubic()
        w = Fr(p + q, 2)
        good = "x = %s" % fz(w)
        return mcq("Wo hat der Graph von %s seinen Wendepunkt?" % F_(f), good, ["x = %s" % z(p), "x = %s" % fz(-w) if w else "x = 1", "x = %s" % z(q)],
                   "f″(x) = %s = 0 ⇒ <b>%s</b>." % (poly(deriv(deriv(f))), good))

    def sym():
        t = R.choice(["gerade", "ungerade", "keine"])
        if t == "gerade":
            f = {4: ri(R, -3, 3, (0,)), 2: ri(R, -6, 6, (0,)), 0: ri(R, -6, 6)}
            good = "achsensymmetrisch zur y-Achse"
        elif t == "ungerade":
            f = {5: ri(R, -3, 3, (0,)), 3: ri(R, -6, 6), 1: ri(R, -6, 6, (0,))}
            good = "punktsymmetrisch zum Ursprung"
        else:
            f = {3: ri(R, -3, 3, (0,)), 2: ri(R, -6, 6, (0,)), 1: ri(R, -6, 6), 0: ri(R, -5, 5)}
            good = "weder achsensymmetrisch zur y-Achse noch punktsymmetrisch zum Ursprung"
        others = [x for x in ["achsensymmetrisch zur y-Achse", "punktsymmetrisch zum Ursprung", "weder achsensymmetrisch zur y-Achse noch punktsymmetrisch zum Ursprung",
                              "achsensymmetrisch zur x-Achse"] if x != good]
        return mcq("Welche Symmetrie hat der Graph von %s?" % F_(f), good, others,
                   "Nur gerade Exponenten ⇒ achsensymmetrisch zur y-Achse, nur ungerade ⇒ punktsymmetrisch zum Ursprung. Hier: <b>%s</b>." % good)

    def mono():
        f, p, q, k = cubic()
        inner = "%s ≤ x ≤ %s" % (z(p), z(q))
        outer = "x ≤ %s oder x ≥ %s" % (z(p), z(q))
        good, bad1 = (inner, outer) if k > 0 else (outer, inner)
        return mcq("Wo ist %s monoton fallend?" % F_(f), "für " + good, ["für " + bad1, "für x ≤ %s" % fz(Fr(p + q, 2)), "für x ≥ %s" % fz(Fr(p + q, 2))],
                   "f′(x) = %s(%s)(%s) ist %szwischen den Nullstellen negativ. Fallend <b>für %s</b>." % (z(k), lin(1, -p), lin(1, -q), "" if k > 0 else "nicht ", good))

    def null():
        r = sorted(R.sample(range(-5, 6), 3))
        a = R.choice([1, -1, 2])
        f = {3: a, 2: -a * sum(r), 1: a * (r[0] * r[1] + r[0] * r[2] + r[1] * r[2]), 0: -a * r[0] * r[1] * r[2]}
        good = "x = %s, x = %s und x = %s" % tuple(z(v) for v in r)
        neg = sorted(-v for v in r)
        return mcq("Welche Nullstellen hat %s? (Tipp: f(x) = %s(x − x<sub>1</sub>)(x − x<sub>2</sub>)(x − x<sub>3</sub>))" % (F_(f), "" if a == 1 else z(a)), good,
                   ["x = %s, x = %s und x = %s" % tuple(z(v) for v in neg), "x = %s, x = %s und x = %s" % (z(r[0]), z(r[1]), z(-r[2])), "x = %s" % z(-f[0]) if f[0] else "x = 1"],
                   "Probe: f(%s) = f(%s) = f(%s) = 0. <b>%s</b>." % (z(r[0]), z(r[1]), z(r[2]), good))

    return dict(
        title="Kurvendiskussion: Extrempunkte, Wendepunkte und Symmetrie",
        short="Kurvendiskussion",
        meta="Kurvendiskussion am Gymnasium: Nullstellen, Symmetrie, Monotonie, Hoch- und Tiefpunkte mit der zweiten Ableitung und Wendepunkte. 100 Aufgaben mit Lösungen.",
        kb="Extremstelle: f′(x) = 0. Die zweite Ableitung entscheidet.",
        ks="f″ kleiner 0: Hochpunkt, f″ grösser 0: Tiefpunkt, f″ = 0: Kandidat für Wendepunkt",
        think=["<b>Nullstellen</b>: f(x) = 0. <b>Symmetrie</b>: nur gerade Exponenten ⇒ zur y-Achse, nur ungerade ⇒ zum Ursprung.",
               "Wo f′(x) &gt; 0 ist, steigt der Graph, wo f′(x) &lt; 0 ist, fällt er (<b>Monotonie</b>).",
               "Kandidaten für Extremstellen: f′(x) = 0. Ist f″(x) &lt; 0, liegt ein <b>Hochpunkt</b> vor, ist f″(x) &gt; 0, ein <b>Tiefpunkt</b>.",
               "<b>Wendestellen</b>: f″(x) = 0 und Vorzeichenwechsel von f″. Bei einer Funktion 3. Grades liegt sie genau in der Mitte der Extremstellen."],
        ex=[("f(x) = x³ − 3x", ["f′(x) = 3x² − 3 = 0 ⇒ x = ±1", "f″(x) = 6x: f″(−1) = −6, f″(1) = 6"], "H(−1 | 2), T(1 | −2), W(0 | 0)")],
        mist=[["f′(x) = 0 ⇒ sicher ein Extremum", "Auch Sattelpunkte haben waagrechte Tangenten: f″ oder Vorzeichenwechsel prüfen"],
              ["f″ kleiner 0 ⇒ Tiefpunkt", "f″ kleiner 0 heisst rechtsgekrümmt: Hochpunkt"],
              ["Die y-Koordinate mit f′ berechnen", "Die y-Koordinate kommt aus f(x₀)"]],
        faq=[{"q": "Was gehört zu einer Kurvendiskussion?", "a": "Definitionsmenge, Symmetrie, Nullstellen, Extrempunkte, Wendepunkte, Verhalten für x → ±∞ und eine Skizze des Graphen."},
             {"q": "Wie unterscheide ich Hoch- und Tiefpunkt?", "a": "Mit der zweiten Ableitung: f″(x0) < 0 ergibt einen Hochpunkt, f″(x0) > 0 einen Tiefpunkt."},
             {"q": "Was ist ein Wendepunkt?", "a": "Ein Punkt, in dem der Graph von einer Links- in eine Rechtskurve wechselt oder umgekehrt."},
             {"q": "Was ist ein Sattelpunkt?", "a": "Ein Wendepunkt mit waagrechter Tangente, zum Beispiel bei f(x) = x³ im Ursprung."}],
        sets=[("Nullstellen und Symmetrie", [(null, 10), (sym, 10)]), ("Waagrechte Tangenten", [(extr, 20)]), ("Hoch- oder Tiefpunkt?", [(art, 20)]),
              ("Monotonie", [(mono, 20)]), ("Wendepunkte", [(wende, 20)])])


# ============================================================ Extremwertaufgaben
def extrem(R):
    def mauer():
        k = R.randint(3, 40)
        L = 4 * k
        return mcq("Mit %s m Zaun soll ein rechteckiges Gehege an einer Mauer eingezäunt werden (die Mauer ist eine Seite). Wie gross ist die grösste mögliche Fläche?" % z(L),
                   "%s m²" % z(2 * k * k), ["%s m²" % z(k * k), "%s m²" % z(L * L // 9), "%s m²" % z(4 * k * k)],
                   "A(x) = x · (%s − 2x), A′(x) = %s − 4x = 0 ⇒ x = %d m. A = %d · %d = <b>%s m²</b>." % (z(L), z(L), k, k, 2 * k, z(2 * k * k)))

    def umfang():
        k = R.randint(2, 50)
        U = 4 * k
        return mcq("Ein Rechteck hat den Umfang %s cm. Wie lang muss eine Seite sein, damit der Flächeninhalt am grössten ist?" % z(U), "%s cm" % z(k),
                   ["%s cm" % z(2 * k), "%s cm" % z(Fr(U, 3)) if U % 3 == 0 else "%s cm" % z(k + 1), "%s cm" % z(k * k)],
                   "A(x) = x · (%s − x), A′(x) = %s − 2x = 0 ⇒ x = <b>%s cm</b> (ein Quadrat)." % (z(2 * k), z(2 * k), z(k)))

    def zahlen():
        S = R.randint(6, 80)
        t = R.choice(["prod", "quad"])
        if t == "prod":
            return mcq("Zwei Zahlen haben die Summe %s. Ihr Produkt soll möglichst gross sein. Wie gross ist das grösste Produkt?" % z(S), fz(Fr(S * S, 4)),
                       [fz(Fr(S, 2)), fz(Fr(S * S, 2)), fz(Fr(S * S, 4) - 1)],
                       "P(x) = x(%s − x), P′(x) = %s − 2x = 0 ⇒ x = %s. P = <b>%s</b>." % (z(S), z(S), fz(Fr(S, 2)), fz(Fr(S * S, 4))))
        return mcq("Zwei Zahlen haben die Summe %s. Die Summe ihrer Quadrate soll möglichst klein sein. Wie heisst die kleinere Zahl?" % z(S), fz(Fr(S, 2)),
                   ["0", fz(Fr(S, 4)), fz(Fr(S, 3))],
                   "Q(x) = x² + (%s − x)², Q′(x) = 4x − %s = 0 ⇒ x = <b>%s</b>." % (z(S), z(2 * S), fz(Fr(S, 2))))

    def schachtel():
        k = R.randint(1, 8)
        a = 6 * k
        V = k * (a - 2 * k) ** 2
        t = R.choice(["x", "V"])
        q = "Aus einem quadratischen Karton mit der Seite %s cm werden an den Ecken gleich grosse Quadrate ausgeschnitten. Daraus wird eine oben offene Schachtel gefaltet. " % z(a)
        if t == "x":
            return mcq(q + "Wie gross muss die Seite der ausgeschnittenen Quadrate sein, damit das Volumen am grössten ist?", "%s cm" % z(k),
                       ["%s cm" % z(2 * k), "%s cm" % z(Fr(a, 4)), "%s cm" % z(Fr(a, 3))],
                       "V(x) = x(%s − 2x)². V′(x) = 0 ⇒ x = %s : 6 = <b>%s cm</b>." % (z(a), z(a), z(k)))
        return mcq(q + "Wie gross ist das grösste Volumen?", "%s cm³" % z(V), ["%s cm³" % z(k * (a - k) ** 2), "%s cm³" % z((a - 2 * k) ** 2), "%s cm³" % z(a ** 3 // 27)],
                   "Bestes x = %s cm. V = %s · %s² = <b>%s cm³</b>." % (z(k), z(k), z(a - 2 * k), z(V)))

    def parabel():
        k, a = R.randint(1, 5), R.choice([1, 2, 3])
        c = 3 * a * k * k
        y = "y = %s − %s" % (z(c), poly({2: a}))
        q = "Unter der Parabel %s liegt im ersten Quadranten ein Rechteck mit einer Ecke im Ursprung und einer Ecke auf der Parabel. " % y
        if R.random() < 0.5:
            return mcq(q + "Wie gross ist der grösste Flächeninhalt?", z(2 * a * k ** 3), [z(k * c), z(c), z(2 * a * k ** 3 + k)],
                       "A(x) = x(%s − %s), A′(x) = %s − %s = 0 ⇒ x = %d. A = %d · %d = <b>%s</b>." % (z(c), poly({2: a}), z(c), poly({2: 3 * a}), k, k, c - a * k * k, z(2 * a * k ** 3)))
        return mcq(q + "Für welches x (Breite des Rechtecks) ist der Flächeninhalt am grössten?", "x = %d" % k, ["x = %d" % (2 * k), "x = %s" % z(Fr(c, 2)), "x = %d" % (k + 1)],
                   "A(x) = x(%s − %s), A′(x) = %s − %s = 0 ⇒ <b>x = %d</b>." % (z(c), poly({2: a}), z(c), poly({2: 3 * a}), k))

    def gewinn():
        a, xs = R.choice([1, 2, 5, 10]), R.randint(5, 60)
        b = 2 * a * xs
        c = R.randint(50, 2000)
        G = a * xs * xs - c
        if G <= 0:
            return None
        return mcq("Der Gewinn einer Firma ist G(x) = %s (x Stück, G in Franken). Bei wie vielen Stück ist der Gewinn am grössten?" % poly({2: -a, 1: b, 0: -c}),
                   "%s Stück" % z(xs), ["%s Stück" % z(2 * xs), "%s Stück" % z(b), "%s Stück" % z(xs + 1)],
                   "G′(x) = %s = 0 ⇒ x = <b>%s</b>. Der grösste Gewinn ist G(%s) = %s Franken." % (lin(-2 * a, b), z(xs), z(xs), z(G)))

    return dict(
        title="Extremwertaufgaben",
        short="Extremwertaufgaben",
        meta="Extremwertaufgaben am Gymnasium: Zielfunktion aufstellen, Nebenbedingung einsetzen, Ableitung null setzen. Rechteck, Zaun, Schachtel, Parabel und Gewinn. 100 Aufgaben mit Lösungen.",
        kb="Zielfunktion aufstellen, Ableitung gleich 0 setzen.",
        ks="Mit der Nebenbedingung zuerst eine Variable eliminieren",
        think=["1. Was soll gross oder klein werden? Das ist die <b>Zielfunktion</b>.",
               "2. Die <b>Nebenbedingung</b> verbindet die Variablen. Damit eine Variable ersetzen.",
               "3. Zielfunktion ableiten und f′(x) = 0 setzen.",
               "4. Prüfen, ob es wirklich ein Maximum bzw. Minimum ist (f″ oder Randwerte), und die gesuchte Grösse angeben."],
        ex=[("Umfang 20 cm, Fläche maximal", ["A = x · (10 − x)", "A′ = 10 − 2x = 0"], "x = 5 cm, ein Quadrat"),
            ("Karton 12 cm, offene Schachtel", ["V = x(12 − 2x)²", "V′ = 0 ⇒ x = 2"], "V = 2 · 8² = 128 cm³")],
        mist=[["Mit zwei Variablen ableiten", "Zuerst mit der Nebenbedingung eine Variable ersetzen"],
              ["Nur x angeben, wenn das Volumen gesucht ist", "Den Wert in die Zielfunktion einsetzen"],
              ["Bei der Schachtel (a − x)² statt (a − 2x)²", "An beiden Seiten wird x weggeschnitten"]],
        faq=[{"q": "Wie gehe ich bei einer Extremwertaufgabe vor?", "a": "Zielfunktion aufstellen, Nebenbedingung einsetzen, ableiten, Ableitung null setzen und das Ergebnis prüfen."},
             {"q": "Was ist die Nebenbedingung?", "a": "Eine Gleichung, die die Variablen verbindet, zum Beispiel ein fester Umfang oder eine feste Zaunlänge."},
             {"q": "Warum ist bei festem Umfang das Quadrat am grössten?", "a": "A(x) = x · (U/2 − x) hat das Maximum bei x = U/4. Dann sind alle Seiten gleich lang."},
             {"q": "Muss ich die zweite Ableitung prüfen?", "a": "Ja, oder die Randwerte vergleichen. So weiss man, ob es ein Maximum oder ein Minimum ist."}],
        sets=[("Rechtecke mit festem Umfang", [(umfang, 20)]), ("Zahlenrätsel", [(zahlen, 20)]), ("Gehege an der Mauer", [(mauer, 20)]),
              ("Schachtel und Parabel", [(schachtel, 12), (parabel, 8)]), ("Gewinn", [(gewinn, 20)])])


# ============================================================ Stammfunktionen
def stamm(R):
    def fpoly():
        while True:
            f = {e: R.randint(-8, 8) for e in range(R.choice([2, 3, 4]) + 1)}
            if any(f.values()) and max(e for e, k in f.items() if k) >= 1:
                break
        good = poly(integ(f)) + " + C"
        bad = [poly(deriv(f)) + " + C", poly({e + 1: k for e, k in f.items()}) + " + C", poly({e: Fr(k, e + 1) for e, k in f.items()}) + " + C"]
        return mcq("Welche Funktion ist eine Stammfunktion von %s?" % F_(f), "F(x) = " + good, ["F(x) = " + b for b in bad],
                   "Exponent um 1 erhöhen, durch den neuen Exponenten teilen: <b>F(x) = %s</b>." % good)

    def spez():
        t = R.choice(["exp", "sin", "cos", "inv", "ekx", "neg"])
        a = ri(R, 2, 9)
        if t == "exp":
            f, good, bad = "%s%s" % (z(a), E("x")), "%s%s + C" % (z(a), E("x")), ["%s%s + C" % (fz(Fr(a, 2)), E("x²")), "%sx%s + C" % (z(a), E("x")), "%s%s + C" % (z(a), E("x + 1"))]
        elif t == "sin":
            f, good, bad = "%s sin x" % z(a), "−%s cos x + C" % z(a), ["%s cos x + C" % z(a), "−%s sin x + C" % z(a), "%s cos x + C" % fz(Fr(a, 2))]
        elif t == "cos":
            f, good, bad = "%s cos x" % z(a), "%s sin x + C" % z(a), ["−%s sin x + C" % z(a), "%s cos x + C" % z(a), "−%s cos x + C" % z(a)]
        elif t == "inv":
            f, good, bad = "%s : x" % z(a), "%s ln|x| + C" % z(a), ["%s : x² + C" % z(-a), "%s ln|x| + C" % fz(Fr(1, a)), "%sx + C" % z(a)]
        elif t == "ekx":
            f, good, bad = E(poly({1: a})), "%s%s + C" % (fz(Fr(1, a)), E(poly({1: a}))), ["%s%s + C" % (z(a), E(poly({1: a}))), E(poly({1: a})) + " + C", "%s%s + C" % (fz(Fr(1, a + 1)), E(poly({1: a + 1})))]
        else:
            f, good, bad = "%s : x²" % z(a), "%s : x + C" % z(-a), ["%s : x + C" % z(a), "%s : x³ + C" % z(-a), "%s ln|x| + C" % z(a)]
        return mcq("Bestimme eine Stammfunktion von f(x) = %s." % f, "F(x) = " + good, ["F(x) = " + b for b in bad],
                   "Rückwärts ableiten und prüfen: F′(x) = f(x). <b>F(x) = %s</b>." % good)

    def bed():
        f = {e: R.randint(-6, 6) for e in range(R.choice([1, 2]) + 1)}
        f[max(f)] = f[max(f)] or 2
        x0, y0 = ri(R, -3, 3), ri(R, -10, 10)
        Fi = integ(f)
        Cc = y0 - ev(Fi, x0)
        Fi2 = dict(Fi)
        Fi2[0] = Fi2.get(0, 0) + Cc
        good = poly(Fi2)
        return mcq("Welche Stammfunktion F von %s erfüllt F(%s) = %s?" % (F_(f), z(x0), z(y0)), "F(x) = " + good,
                   ["F(x) = " + poly({**Fi, 0: y0}) if y0 != Cc else "F(x) = " + poly({**Fi, 0: Cc + 1}), "F(x) = " + poly(Fi),
                    "F(x) = " + poly({**Fi, 0: -Cc}) if Cc else "F(x) = " + poly({**Fi, 0: 1})],
                   "F(x) = %s + C. F(%s) = %s ⇒ C = %s. <b>F(x) = %s</b>." % (poly(Fi), z(x0), z(y0), fz(Cc), good))

    def wurzel():
        a = R.choice([1, 2, 3, 4, 5, 6, 8, 9, 10, 12])
        t = R.choice(["sqrt", "x2", "x3"])
        if t == "sqrt":
            good = "%sx√x + C" % fz(Fr(2 * a, 3)) if Fr(2 * a, 3) != 1 else "x√x + C"
            return mcq("Bestimme eine Stammfunktion von f(x) = %s√x." % ("" if a == 1 else z(a)), "F(x) = " + good,
                       ["F(x) = %s : √x + C" % fz(Fr(a, 2)), "F(x) = %sx√x + C" % fz(Fr(3 * a, 2)), "F(x) = %s√x + C" % fz(Fr(2 * a, 3))],
                       "√x = x<sup>½</sup> ⇒ F = %s · x<sup>3/2</sup> : (3/2) = <b>%s</b>." % (z(a), good))
        if t == "x2":
            good = "%s : x + C" % z(-a)
            return mcq("Bestimme eine Stammfunktion von f(x) = %s : x²." % z(a), "F(x) = " + good,
                       ["F(x) = %s : x³ + C" % fz(Fr(-a, 3)), "F(x) = %s : x + C" % z(a), "F(x) = %s ln|x| + C" % z(a)],
                       "%s : x² = %s · x<sup>−2</sup> → %s · x<sup>−1</sup> : (−1). <b>F(x) = %s</b>." % (z(a), z(a), z(a), good))
        good = "%s : x² + C" % fz(Fr(-a, 2))
        return mcq("Bestimme eine Stammfunktion von f(x) = %s : x³." % z(a), "F(x) = " + good,
                   ["F(x) = %s : x⁴ + C" % fz(Fr(-a, 4)), "F(x) = %s : x² + C" % fz(Fr(a, 2)), "F(x) = %s : x² + C" % z(-3 * a)],
                   "x<sup>−3</sup> → x<sup>−2</sup> : (−2). <b>F(x) = %s</b>." % good)

    def pruef():
        f = rpoly(R, 3, -5, 5)
        Fx = poly(f)
        good = "f(x) = %s" % poly(deriv(f))
        return mcq("F(x) = %s ist eine Stammfunktion von welcher Funktion?" % Fx, good,
                   ["f(x) = %s" % poly(integ(f)), "f(x) = %s" % poly({e - 1: k for e, k in f.items() if e}), "f(x) = %s" % poly(deriv(deriv(f))) if len(f) > 2 else "f(x) = 0"],
                   "F ist Stammfunktion von f, wenn F′ = f. F′(x) = <b>%s</b>." % poly(deriv(f)))

    return dict(
        title="Stammfunktionen",
        short="Stammfunktionen",
        meta="Integralrechnung am Gymnasium: Stammfunktionen von Polynomen, eˣ, sin, cos, 1/x und Wurzeln, Integrationskonstante bestimmen und Stammfunktionen prüfen. 100 Aufgaben mit Lösungen.",
        kb="F ist Stammfunktion von f, wenn F′ = f.",
        ks="Potenz: x^n wird zu x^(n + 1) : (n + 1) (für n ≠ −1)",
        think=["Eine <b>Stammfunktion</b> F von f erfüllt F′(x) = f(x). Mit F ist auch F + C eine Stammfunktion.",
               "Potenzen: x<sup>n</sup> → x<sup>n + 1</sup> : (n + 1) für n ≠ −1. Für 1 : x ist F(x) = ln|x|.",
               "e<sup>x</sup> → e<sup>x</sup>, sin x → −cos x, cos x → sin x, e<sup>kx</sup> → (1 : k) · e<sup>kx</sup>.",
               "Mit einer Bedingung F(x<sub>0</sub>) = y<sub>0</sub> bestimmt man die Konstante C."],
        ex=[("f(x) = 6x² − 4x + 1", ["6 · x³ : 3 = 2x³", "4 · x² : 2 = 2x²"], "F(x) = 2x³ − 2x² + x + C"),
            ("f(x) = 2x, F(1) = 5", ["F(x) = x² + C", "1 + C = 5"], "F(x) = x² + 4")],
        mist=[["Stammfunktion von x³ = 3x²", "Das ist die Ableitung. Richtig: x⁴ : 4"],
              ["Stammfunktion von sin x = cos x", "(cos x)′ = −sin x, also F(x) = −cos x"],
              ["Das + C vergessen", "Stammfunktionen sind nur bis auf eine Konstante bestimmt"]],
        faq=[{"q": "Warum schreibt man + C?", "a": "Konstanten fallen beim Ableiten weg. Deshalb hat jede Funktion unendlich viele Stammfunktionen, die sich um eine Konstante unterscheiden."},
             {"q": "Wie prüfe ich eine Stammfunktion?", "a": "Ableiten. Kommt f heraus, ist F richtig."},
             {"q": "Was ist die Stammfunktion von 1 : x?", "a": "ln|x| + C. Die Potenzregel gilt hier nicht, weil man durch 0 teilen müsste."},
             {"q": "Was ist der Unterschied zwischen Stammfunktion und Integral?", "a": "Eine Stammfunktion ist eine Funktion. Ein bestimmtes Integral ist eine Zahl, die man mit einer Stammfunktion berechnet."}],
        sets=[("Stammfunktionen von Polynomen", [(fpoly, 20)]), ("Ableiten rückwärts", [(pruef, 20)]), ("eˣ, sin, cos und 1 : x", [(spez, 20)]),
              ("Wurzeln und negative Exponenten", [(wurzel, 20)]), ("Konstante bestimmen", [(bed, 20)])])


# ============================================================ bestimmte Integrale und Flächen
def integral(R):
    def bestimmt():
        f = {e: R.randint(-6, 6) for e in range(R.choice([1, 2, 3]) + 1)}
        if not any(f.values()):
            return None
        a = ri(R, -3, 2)
        b = a + R.randint(1, 3)
        Fi = integ(f)
        v = ev(Fi, b) - ev(Fi, a)
        return mcq("Berechne ∫<sub>%s</sub><sup>%s</sup> (%s) dx." % (z(a), z(b), poly(f)), fz(v),
                   [fz(ev(Fi, a) - ev(Fi, b)) if v else "1", fz(ev(f, b) - ev(f, a)) if ev(f, b) - ev(f, a) != v else fz(v + 1), fz(ev(Fi, b))],
                   "F(x) = %s. F(%s) − F(%s) = %s − %s = <b>%s</b>." % (poly(Fi), z(b), z(a), fz(ev(Fi, b)), par(ev(Fi, a)) if ev(Fi, a) >= 0 else "(%s)" % fz(ev(Fi, a)), fz(v)))

    def hs():
        Fa, Fb = ri(R, -20, 20), ri(R, -20, 30)
        a, b = ri(R, -3, 2), None
        b = a + R.randint(1, 5)
        return mcq("F ist eine Stammfunktion von f mit F(%s) = %s und F(%s) = %s. Berechne ∫<sub>%s</sub><sup>%s</sup> f(x) dx." % (z(a), z(Fa), z(b), z(Fb), z(a), z(b)),
                   z(Fb - Fa), [z(Fa - Fb) if Fa != Fb else "1", z(Fa + Fb), z(Fr(Fb - Fa, b - a))],
                   "Hauptsatz: ∫ = F(%s) − F(%s) = %s − %s = <b>%s</b>." % (z(b), z(a), z(Fb), par(Fa), z(Fb - Fa)))

    def flaeche_x():
        k = R.randint(1, 5)
        c = R.choice([1, 2, 3])
        A = Fr(4 * c * k ** 3, 3)
        return mcq("Wie gross ist die Fläche zwischen dem Graphen von f(x) = %s und der x-Achse?" % poly({2: -c, 0: c * k * k}), fz(A),
                   [fz(A / 2), fz(Fr(2 * c * k ** 3)), fz(2 * A)],
                   "Nullstellen ±%d. ∫<sub>−%d</sub><sup>%d</sup> (%s) dx = <b>%s</b>." % (k, k, k, poly({2: -c, 0: c * k * k}), fz(A)))

    def zwei():
        if R.random() < 0.7:
            a, m = R.choice([1, 2, 3]), R.randint(1, 8)
            xs = Fr(m, a)
            A = Fr(m ** 3, 6 * a * a)
            return mcq("Wie gross ist die Fläche zwischen der Parabel y = %s und der Geraden y = %s?" % (poly({2: a}), poly({1: m})), fz(A),
                       [fz(2 * A), fz(3 * A), fz(6 * A)],
                       "Schnittstellen x = 0 und x = %s. ∫<sub>0</sub><sup>%s</sup> (%s − %s) dx = <b>%s</b>." % (fz(xs), fz(xs), poly({1: m}), poly({2: a}), fz(A)))
        k = R.randint(1, 6)
        A = Fr(4 * k ** 3, 3)
        return mcq("Wie gross ist die Fläche zwischen der Parabel y = x² und der Geraden y = %s?" % z(k * k), fz(A),
                   [fz(A / 2), fz(Fr(2 * k ** 3)), fz(Fr(2 * k ** 3, 3))],
                   "Schnittstellen x = ±%d. ∫<sub>−%d</sub><sup>%d</sup> (%s − x²) dx = %s − %s = <b>%s</b>." % (k, k, k, z(k * k), z(2 * k ** 3), fz(Fr(2 * k ** 3, 3)), fz(A)))

    def vorz():
        a = R.randint(1, 6)
        t = R.choice(["lin", "cub"])
        if t == "lin":
            f = lin(1, -a)
            I, A = 0, a * a
            q = "Für f(x) = %s gilt ∫<sub>0</sub><sup>%d</sup> f(x) dx = 0. Wie gross ist die Fläche zwischen dem Graphen und der x-Achse im Intervall [0; %d]?" % (f, 2 * a, 2 * a)
            e = "Die Fläche unter und über der x-Achse ist je ½ · %d · %d. Zusammen <b>%s</b>." % (a, a, z(A))
        else:
            f = poly({3: 1})
            I, A = 0, Fr(a ** 4, 2)
            q = "Für f(x) = x³ gilt ∫<sub>−%d</sub><sup>%d</sup> f(x) dx = 0. Wie gross ist die Fläche zwischen dem Graphen und der x-Achse im Intervall [−%d; %d]?" % (a, a, a, a)
            e = "Punktsymmetrisch: 2 · ∫<sub>0</sub><sup>%d</sup> x³ dx = 2 · %s = <b>%s</b>." % (a, fz(Fr(a ** 4, 4)), fz(A))
        return mcq(q, fz(A), ["0", fz(A / 2), fz(2 * A)], e)

    def mittel():
        f = {2: ri(R, -3, 3, (0,)), 1: ri(R, -6, 6), 0: ri(R, -5, 5)}
        a = ri(R, -2, 2)
        b = a + R.choice([1, 2, 3, 4])
        Fi = integ(f)
        I = ev(Fi, b) - ev(Fi, a)
        m = I / (b - a)
        return mcq("Wie gross ist der Mittelwert von %s auf dem Intervall [%s; %s]?" % (F_(f), z(a), z(b)), fz(m),
                   [fz(I), fz((ev(f, a) + ev(f, b)) / 2) if (ev(f, a) + ev(f, b)) / 2 != m else fz(m + 1), fz(ev(f, Fr(a + b, 2))) if ev(f, Fr(a + b, 2)) != m else fz(m - 1)],
                   "m = ∫ f(x) dx : (b − a) = %s : %d = <b>%s</b>." % (fz(I), b - a, fz(m)))

    return dict(
        title="Bestimmtes Integral und Flächenberechnung",
        short="Integral und Flächen",
        meta="Integralrechnung am Gymnasium: bestimmte Integrale mit dem Hauptsatz, Flächen zwischen Graph und x-Achse, Flächen zwischen zwei Kurven und Mittelwerte. 100 Aufgaben mit Lösungen.",
        kb="∫ von a bis b f(x) dx = F(b) − F(a)",
        ks="Fläche: Nullstellen beachten, Teilflächen unter der x-Achse positiv zählen",
        think=["<b>Hauptsatz</b>: Ist F eine Stammfunktion von f, dann gilt ∫<sub>a</sub><sup>b</sup> f(x) dx = F(b) − F(a).",
               "Liegt der Graph über der x-Achse, ist das Integral gleich der Fläche. Unter der x-Achse ist das Integral negativ.",
               "Für Flächen: zuerst die Nullstellen bestimmen und die Teilflächen einzeln mit Betrag addieren.",
               "Fläche zwischen zwei Kurven: ∫ (obere Funktion − untere Funktion) dx zwischen den Schnittstellen.",
               "Mittelwert auf [a; b]: ∫<sub>a</sub><sup>b</sup> f(x) dx : (b − a)."],
        ex=[("∫ von 0 bis 2 (3x²) dx", ["F(x) = x³", "8 − 0"], "8"),
            ("Fläche zwischen y = x² und y = 2x", ["Schnittstellen 0 und 2", "∫ (2x − x²) dx = 4 − 8/3"], "4/3")],
        mist=[["F(a) − F(b)", "Obere minus untere Grenze: F(b) − F(a)"],
              ["Fläche = Integral, auch wenn der Graph die x-Achse kreuzt", "Teilflächen getrennt berechnen und Beträge addieren"],
              ["Bei zwei Kurven untere minus obere", "Obere minus untere Funktion"]],
        faq=[{"q": "Was ist der Hauptsatz der Differenzial- und Integralrechnung?", "a": "Er verbindet Ableitung und Integral: Das bestimmte Integral von f ist F(b) − F(a), wenn F′ = f."},
             {"q": "Kann ein Integral negativ sein?", "a": "Ja, wenn der Graph unter der x-Achse liegt. Eine Fläche ist dagegen immer positiv."},
             {"q": "Wie berechne ich die Fläche zwischen zwei Kurven?", "a": "Schnittstellen bestimmen und ∫ (obere − untere Funktion) dx zwischen ihnen berechnen."},
             {"q": "Braucht man beim bestimmten Integral + C?", "a": "Nein. Die Konstante fällt bei F(b) − F(a) weg."}],
        sets=[("Bestimmte Integrale", [(bestimmt, 20)]), ("Hauptsatz", [(hs, 20)]), ("Fläche mit der x-Achse", [(flaeche_x, 10), (vorz, 10)]),
              ("Fläche zwischen zwei Kurven", [(zwei, 20)]), ("Mittelwert einer Funktion", [(mittel, 20)])])


# ============================================================ statistische Kennzahlen
def statistik(R):
    def data(n=None, lo=1, hi=30):
        n = n or R.randint(5, 9)
        return [R.randint(lo, hi) for _ in range(n)]

    def L(d):
        return ", ".join(z(x) for x in d)

    def mw():
        d = data()
        m = Fr(sum(d), len(d))
        if m.denominator not in (1, 2, 4, 5):
            return None
        s = sorted(d)
        med = Fr(s[len(s) // 2]) if len(s) % 2 else Fr(s[len(s) // 2 - 1] + s[len(s) // 2], 2)
        return mcq("Berechne den Mittelwert der Daten %s." % L(d), z(m), [z(med) if med != m else z(m + 1), z(sum(d)), z(Fr(sum(d), len(d) - 1)) if Fr(sum(d), len(d) - 1).denominator in (1, 2, 4, 5) else z(m - 1)],
                   "Summe %s, Anzahl %d: %s : %d = <b>%s</b>." % (z(sum(d)), len(d), z(sum(d)), len(d), z(m)))

    def median():
        d = data(R.randint(6, 11))
        s = sorted(d)
        n = len(s)
        med = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
        return mcq("Bestimme den Median der Daten %s." % L(d), z(med), [z(d[n // 2]) if d[n // 2] != med else z(med + 1), z(Fr(sum(d), n)) if Fr(sum(d), n).denominator in (1, 2, 4, 5) and Fr(sum(d), n) != med else z(med + 2), z(s[n // 2 + 1]) if s[n // 2 + 1] != med else z(med - 1)],
                   "Sortiert: %s. %s <b>%s</b>." % (L(s), "Der mittlere Wert ist" if n % 2 else "Mittelwert der beiden mittleren Werte:", z(med)))

    def spann():
        d = data(R.randint(6, 10), 1, 60)
        s = sorted(d)
        n = len(s)
        h = n // 2
        lower, upper = s[:h], s[h + (n % 2):]
        med = lambda x: Fr(x[len(x) // 2]) if len(x) % 2 else Fr(x[len(x) // 2 - 1] + x[len(x) // 2], 2)
        t = R.choice(["R", "Q"])
        if t == "R":
            return mcq("Wie gross ist die Spannweite der Daten %s?" % L(d), z(s[-1] - s[0]), [z(d[-1] - d[0]) if d[-1] - d[0] != s[-1] - s[0] else z(s[-1]), z(s[-1] + s[0]), z(med(upper) - med(lower))],
                       "Grösster minus kleinster Wert: %s − %s = <b>%s</b>." % (z(s[-1]), z(s[0]), z(s[-1] - s[0])))
        q1, q3 = med(lower), med(upper)
        return mcq("Bestimme den Quartilsabstand der Daten %s (Quartile als Mediane der unteren und oberen Hälfte)." % L(d), z(q3 - q1),
                   [z(s[-1] - s[0]), z(q3 + q1), z(q3 - med(s)) if q3 - med(s) != q3 - q1 else z(q3 - q1 + 1)],
                   "Sortiert: %s. Q<sub>1</sub> = %s, Q<sub>3</sub> = %s, Q<sub>3</sub> − Q<sub>1</sub> = <b>%s</b>." % (L(s), z(q1), z(q3), z(q3 - q1)))

    def sd():
        a, m, k = R.randint(1, 6), R.randint(10, 60), R.choice([1, 2, 3])
        d = [m - a] * k + [m + a] * k
        if R.random() < 0.5:
            d += [m]
            var = Fr(2 * k * a * a, 2 * k + 1)
            if math.isqrt(var.numerator) ** 2 != var.numerator or math.isqrt(var.denominator) ** 2 != var.denominator:
                d = d[:-1]
        R.shuffle(d)
        var = Fr(sum((x - m) ** 2 for x in d), len(d))
        s = Fr(math.isqrt(var.numerator), math.isqrt(var.denominator))
        if s * s != var:
            return None
        return mcq("Berechne die Standardabweichung σ der Daten %s (Mittelwert %s)." % (L(d), z(m)), z(s), [z(var) if var != s else z(s + 1), z(2 * s), z(Fr(sum(abs(x - m) for x in d), len(d) - 1))],
                   "Abweichungen ±%d, Varianz = %s, σ = √%s = <b>%s</b>." % (a, z(var), z(var), z(s)))

    def trafo():
        m, s = R.randint(10, 60), R.randint(2, 9)
        t = R.choice(["plus", "mal"])
        c = R.randint(2, 15) if t == "plus" else R.choice([2, 3, 10])
        if t == "plus":
            good = "Mittelwert %s, Standardabweichung %s" % (z(m + c), z(s))
            bad = ["Mittelwert %s, Standardabweichung %s" % (z(m + c), z(s + c)), "Mittelwert %s, Standardabweichung %s" % (z(m), z(s + c)), "Mittelwert %s, Standardabweichung %s" % (z(m + c), z(s * c))]
            q = "Daten haben den Mittelwert %s und die Standardabweichung %s. Zu jedem Wert wird %d addiert. Was gilt danach?" % (z(m), z(s), c)
            e = "Verschieben ändert die Lage, nicht die Streuung: <b>%s</b>." % good
        else:
            good = "Mittelwert %s, Standardabweichung %s" % (z(m * c), z(s * c))
            bad = ["Mittelwert %s, Standardabweichung %s" % (z(m * c), z(s)), "Mittelwert %s, Standardabweichung %s" % (z(m * c), z(s * c * c)), "Mittelwert %s, Standardabweichung %s" % (z(m + c), z(s * c))]
            q = "Daten haben den Mittelwert %s und die Standardabweichung %s. Jeder Wert wird mit %d multipliziert. Was gilt danach?" % (z(m), z(s), c)
            e = "Mittelwert und Standardabweichung werden mit %d multipliziert: <b>%s</b>." % (c, good)
        return mcq(q, good, bad, e)

    def note():
        import ch_common as C
        nm = R.choice(D.GIRLS + D.BOYS)
        n = R.randint(3, 6)
        notes = [Fr(R.randint(7, 12), 2) for _ in range(n)]
        target = Fr(R.randint(9, 11), 2)
        need = target * (n + 1) - sum(notes)
        if not (1 <= need <= 6) or need.denominator > 2:
            return None
        f = lambda v: z(v)
        return mcq("%s hat die Noten %s. Welche Note braucht %s in der nächsten Prüfung für einen Durchschnitt von %s?" % (nm, ", ".join(f(x) for x in notes), nm, f(target)),
                   f(need), [f(x) for x in [target, need + Fr(1, 2), need - Fr(1, 2), need - 1, need + 1, Fr(sum(notes), n)] if 1 <= x <= 6 and x != need and (2 * x).denominator == 1],
                   "Summe nachher: %s · %d = %s. Bisher %s. Nötig: <b>%s</b>." % (f(target), n + 1, f(target * (n + 1)), f(sum(notes)), f(need)))

    return dict(
        title="Statistische Kennzahlen: Mittelwert, Median und Standardabweichung",
        short="Statistische Kennzahlen",
        meta="Statistik am Gymnasium: Mittelwert, Median, Spannweite, Quartilsabstand, Standardabweichung, Veränderung von Daten und Notendurchschnitt. 100 Aufgaben mit Lösungen.",
        kb="Lagemasse: Mittelwert und Median. Streumasse: Spannweite, Quartilsabstand, Standardabweichung.",
        ks="Varianz = Mittelwert der quadrierten Abweichungen, σ = Wurzel der Varianz",
        think=["<b>Mittelwert</b>: Summe der Werte durch die Anzahl. <b>Median</b>: der mittlere Wert der sortierten Daten.",
               "<b>Spannweite</b>: grösster minus kleinster Wert. <b>Quartilsabstand</b>: Q<sub>3</sub> − Q<sub>1</sub>.",
               "<b>Varianz</b>: Mittelwert der quadrierten Abweichungen vom Mittelwert. <b>Standardabweichung</b> σ: Wurzel der Varianz.",
               "Addiert man zu allen Werten c, verschiebt sich der Mittelwert um c, σ bleibt gleich. Multipliziert man mit c, werden beide mit c multipliziert."],
        ex=[("Daten 4, 8, 8, 12", ["Mittelwert 8", "Abweichungen −4, 0, 0, 4", "Varianz (16 + 0 + 0 + 16) : 4 = 8"], "σ = √8 ≈ 2,83"),
            ("Noten 4,5; 5; 5,5 – Durchschnitt 5 mit vier Noten", ["4 · 5 = 20", "20 − 15 = 5"], "Note 5")],
        mist=[["Median ohne Sortieren", "Zuerst der Grösse nach ordnen"],
              ["σ = Mittelwert der Abweichungen", "Abweichungen quadrieren, mitteln, Wurzel ziehen"],
              ["Nach + 5 ist auch σ um 5 grösser", "Verschieben ändert die Streuung nicht"]],
        faq=[{"q": "Wann ist der Median besser als der Mittelwert?", "a": "Wenn es Ausreisser gibt. Der Median wird von sehr grossen oder kleinen Werten kaum beeinflusst."},
             {"q": "Was sagt die Standardabweichung aus?", "a": "Wie stark die Werte im Durchschnitt um den Mittelwert streuen."},
             {"q": "Wie berechne ich den Quartilsabstand?", "a": "Daten sortieren, die untere und obere Hälfte bilden, deren Mediane Q1 und Q3 bestimmen und Q3 − Q1 rechnen."},
             {"q": "Wie berechne ich die nötige Note für einen Durchschnitt?", "a": "Zielschnitt mal Anzahl Noten ergibt die nötige Summe. Davon die Summe der bisherigen Noten abziehen."}],
        sets=[("Mittelwert", [(mw, 20)]), ("Median", [(median, 20)]), ("Spannweite und Quartilsabstand", [(spann, 20)]),
              ("Standardabweichung und Veränderungen", [(sd, 10), (trafo, 10)]), ("Notendurchschnitt", [(note, 20)])])
