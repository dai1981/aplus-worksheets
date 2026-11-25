# -*- coding: utf-8 -*-
"""Schweiz Gymnasium: Vektoren, Skalar- und Vektorprodukt, Geraden und Ebenen, Kombinatorik, bedingte Wahrscheinlichkeit, Binomialverteilung"""
import math
from fractions import Fraction as Fr
import de_common as D
from ch_gym import mcq, z, fz, par, poly, ri, vec, pt, MI, NB

QUADS = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (0, 3, 4, 5), (0, 6, 8, 10), (0, 5, 12, 13)]


def V(R, lo=-6, hi=6):
    return [R.randint(lo, hi) for _ in range(3)]


def add(a, b, k=1):
    return [x + k * y for x, y in zip(a, b)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def quad(R, k=1):
    a, b, c, l = R.choice(QUADS)
    v = [a, b, c]
    R.shuffle(v)
    v = [x * R.choice([1, -1]) * k for x in v]
    return v, l * k


def nonzero(v):
    return any(v)


def ve(v):
    return vec(*v)


def P3(n, v):
    return pt(n, *v)


# ============================================================ Vektoren
def vektoren(R):
    def ab():
        A, B = V(R), V(R)
        good = ve(add(B, A, -1))
        return mcq("Gegeben sind %s und %s. Welcher Vektor ist <span class='vec'>AB</span>?" % (P3("A", A), P3("B", B)), good,
                   [ve(add(A, B, -1)), ve(add(A, B)), ve([B[0] - A[0], A[1] - B[1], B[2] - A[2]])],
                   "Spitze minus Fuss: <span class='vec'>AB</span> = B − A = <b>%s</b>." % good)

    def mitte():
        A = V(R)
        B = [a + 2 * R.randint(-4, 4) for a in A]
        M = [(a + b) // 2 for a, b in zip(A, B)]
        good = P3("M", M)
        return mcq("Wie heisst der Mittelpunkt M der Strecke AB mit %s und %s?" % (P3("A", A), P3("B", B)), good,
                   [P3("M", [(b - a) // 2 for a, b in zip(A, B)]), P3("M", add(A, B)), P3("M", [(b - a) for a, b in zip(A, B)])],
                   "M = ½ · (A + B): jede Koordinate halbieren. <b>%s</b>." % good)

    def betrag():
        v, l = quad(R, R.choice([1, 1, 2]))
        return mcq("Wie lang ist der Vektor %s?" % ve(v), z(l), [z(sum(abs(x) for x in v)), z(l * l), z(l + 1)],
                   "|v| = √(%s) = √%d = <b>%s</b>." % (" + ".join(par(x) + "²" for x in v), l * l, z(l)))

    def abst():
        A = V(R)
        v, l = quad(R)
        B = add(A, v)
        return mcq("Wie weit sind %s und %s voneinander entfernt?" % (P3("A", A), P3("B", B)), z(l),
                   [z(sum(abs(x) for x in v)), z(l * l), z(math.isqrt(sum(x * x for x in add(A, B))))],
                   "<span class='vec'>AB</span> = %s, |<span class='vec'>AB</span>| = √%d = <b>%s</b>." % (ve(v), l * l, z(l)))

    def lin():
        a, b = V(R, -5, 5), V(R, -5, 5)
        r, s = ri(R, -3, 4, (0,)), ri(R, -3, 3, (0,))
        res = [r * x + s * y for x, y in zip(a, b)]
        op = "%s · a %s %s · b" % (z(r), "+" if s > 0 else "−", z(abs(s)))
        return mcq("Berechne %s für a = %s und b = %s." % (op, ve(a), ve(b)), ve(res),
                   [ve([r * x - s * y for x, y in zip(a, b)]), ve([r * x + y for x, y in zip(a, b)]), ve([s * x + r * y for x, y in zip(a, b)])],
                   "Komponentenweise rechnen: <b>%s</b>." % ve(res))

    def parallel():
        a = [ri(R, -4, 4, (0,)) for _ in range(3)]
        k = R.choice([2, 3, -2, Fr(1, 2), -3])
        i = R.randrange(3)
        b = [k * x for x in a]
        t = b[i]
        bb = [z(x) for x in b]
        bb[i] = "t"
        return mcq("Für welches t ist b = %s parallel zu a = %s?" % (vec(*bb), ve(a)), z(t), [z(-t), z(a[i]), z(t + 1)],
                   "Parallel heisst b = k · a. Aus den anderen Komponenten folgt k = %s, also t = %s · %s = <b>%s</b>." % (z(k), z(k), par(a[i]), z(t)))

    def parallelogramm():
        A, B, Cc = V(R), V(R), V(R)
        Dd = add(add(A, Cc), B, -1)
        good = P3("D", Dd)
        return mcq("ABCD ist ein Parallelogramm mit %s, %s und %s. Wie heisst D?" % (P3("A", A), P3("B", B), P3("C", Cc)), good,
                   [P3("D", add(add(B, Cc), A, -1)), P3("D", add(add(A, B), Cc, -1)), P3("D", add(Cc, B, -1))],
                   "<span class='vec'>AD</span> = <span class='vec'>BC</span>, also D = A + C − B = <b>%s</b>." % good)

    return dict(
        title="Vektoren in der Ebene und im Raum",
        short="Vektoren",
        meta="Vektorgeometrie am Gymnasium: Verbindungsvektor, Mittelpunkt, Betrag und Abstand, Linearkombinationen, parallele Vektoren und Parallelogramme. 100 Aufgaben mit Lösungen.",
        kb="Verbindungsvektor: Spitze minus Fuss.",
        ks="Betrag: Wurzel aus der Summe der Quadrate der Komponenten",
        think=["Ein <b>Vektor</b> beschreibt eine Verschiebung. Im Raum hat er drei Komponenten.",
               "Der Vektor von A nach B ist <span class='vec'>AB</span> = B − A (Spitze minus Fuss).",
               "Der <b>Betrag</b> |v| ist die Länge: |v| = √(v<sub>1</sub>² + v<sub>2</sub>² + v<sub>3</sub>²).",
               "Zwei Vektoren sind <b>parallel</b> (kollinear), wenn der eine ein Vielfaches des anderen ist: b = k · a.",
               "Mittelpunkt: M = ½ · (A + B). Parallelogramm ABCD: D = A + C − B."],
        ex=[("A(1 | 2 | 3), B(4 | 6 | 3): Länge von AB", ["AB = (3, 4, 0)", "|AB| = √(9 + 16 + 0)"], "5"),
            ("a = (2, −1, 3), b = (4, t, 6) parallel", ["k = 2 (aus 4 = 2 · 2)", "t = 2 · (−1)"], "t = −2")],
        mist=[["AB = A − B", "Spitze minus Fuss: AB = B − A"],
              ["|v| = v₁ + v₂ + v₃", "Quadrieren, addieren, Wurzel ziehen"],
              ["Mittelpunkt = ½ · (B − A)", "M = ½ · (A + B); ½ · (B − A) ist nur der halbe Verbindungsvektor"]],
        faq=[{"q": "Was ist der Unterschied zwischen Punkt und Vektor?", "a": "Ein Punkt ist ein Ort. Ein Vektor ist eine Verschiebung mit Richtung und Länge. Der Ortsvektor eines Punktes zeigt vom Ursprung zum Punkt."},
             {"q": "Wie berechne ich die Länge eines Vektors?", "a": "Mit Pythagoras im Raum: Wurzel aus der Summe der Quadrate der drei Komponenten."},
             {"q": "Wann sind zwei Vektoren parallel?", "a": "Wenn es eine Zahl k gibt mit b = k · a. Alle Komponenten müssen dasselbe Verhältnis haben."},
             {"q": "Wie finde ich den vierten Punkt eines Parallelogramms?", "a": "Für ABCD gilt D = A + C − B, denn der Vektor AD ist gleich dem Vektor BC."}],
        sets=[("Verbindungsvektor und Mittelpunkt", [(ab, 10), (mitte, 10)]), ("Betrag und Abstand", [(betrag, 10), (abst, 10)]),
              ("Mit Vektoren rechnen", [(lin, 20)]), ("Parallele Vektoren", [(parallel, 20)]), ("Parallelogramme", [(parallelogramm, 20)])])


# ============================================================ Skalarprodukt, Winkel, Vektorprodukt
ANG = [((1, 1, 0), (1, 0, 0), 45), ((1, 1, 0), (0, 1, 1), 60), ((1, 0, 1), (-1, 1, 0), 120), ((1, 1, 0), (-1, 0, 0), 135),
       ((1, 2, 2), (2, 1, -2), 90), ((1, 0, 0), (-1, 0, 0), 180), ((2, 1, 2), (2, 2, 1), None), ((1, 1, 1), (1, 1, -1), None),
       ((1, 0, 1), (1, 1, 0), 60), ((0, 1, 1), (0, 1, 0), 45), ((1, 1, 0), (0, -1, -1), 120), ((1, 2, 3), (3, 0, -1), 90)]


def skalar(R):
    def sk():
        a, b = V(R, -6, 6), V(R, -6, 6)
        s = dot(a, b)
        return mcq("Berechne das Skalarprodukt a · b für a = %s und b = %s." % (ve(a), ve(b)), z(s),
                   [z(sum(abs(x * y) for x, y in zip(a, b))), z(s + 2 * a[0] * b[0]), z(dot(a, b[::-1]))],
                   "a · b = %s = <b>%s</b>." % (" + ".join("%s · %s" % (par(x), par(y)) for x, y in zip(a, b)), z(s)))

    def orth():
        a = [ri(R, -5, 5, (0,)) for _ in range(3)]
        if R.random() < 0.5:
            b0, b2 = ri(R, -4, 4), ri(R, -4, 4)
            r = -(a[0] * b0 + a[2] * b2)
            if r % a[1]:
                return None
            b = [b0, r // a[1], b2]
        else:
            b = V(R, -5, 5)
        if not nonzero(b):
            return None
        s = dot(a, b)
        good = "Ja, denn a · b = 0." if s == 0 else "Nein, denn a · b = %s." % z(s)
        bad = ["Nein, denn a · b = 0.", "Ja, denn a · b = %s." % z(s if s else 1), "Nein, denn a und b sind nicht parallel."] if s == 0 else \
              ["Ja, denn a · b = 0.", "Ja, denn a · b = %s." % z(s), "Nein, denn a · b = %s." % z(-s)]
        return mcq("Stehen a = %s und b = %s senkrecht aufeinander?" % (ve(a), ve(b)), good, bad,
                   "Senkrecht genau dann, wenn das Skalarprodukt 0 ist. a · b = %s. %s" % (z(s), good))

    def tsuch():
        a = [ri(R, -5, 5, (0,)) for _ in range(3)]
        b0, b2, k = ri(R, -5, 5), ri(R, -5, 5), ri(R, -4, 4)
        r = -(a[0] * b0 + a[2] * b2)
        if r % a[1]:
            return None
        t = r // a[1]
        return mcq("Für welches t steht a = %s senkrecht auf b = %s?" % (ve(a), vec(z(b0), "t", z(b2))), z(t), [z(-t), z(t + 1), z(r)],
                   "a · b = %s · %s + %s · t + %s · %s = 0 ⇒ %st = %s ⇒ t = <b>%s</b>." % (par(a[0]), par(b0), par(a[1]), par(a[2]), par(b2), z(a[1]), z(r), z(t)))

    def winkel():
        a, b, w = R.choice([x for x in ANG if x[2]])
        p = [0, 1, 2]
        R.shuffle(p)
        sg = [R.choice([1, -1]) for _ in range(3)]
        k1, k2 = R.randint(1, 3), R.randint(1, 3)
        a = [k1 * sg[i] * a[p[i]] for i in range(3)]
        b = [k2 * sg[i] * b[p[i]] for i in range(3)]
        others = [x for x in (30, 45, 60, 90, 120, 135, 150, 180) if x != w]
        R.shuffle(others)
        return mcq("Wie gross ist der Winkel zwischen a = %s und b = %s?" % (ve(a), ve(b)), "%d°" % w, ["%d°" % x for x in others[:3]],
                   "cos φ = a · b : (|a| · |b|) = %s : (%s). Also φ = <b>%d°</b>." % (z(dot(a, b)), "%s · %s" % ("√%d" % dot(a, a), "√%d" % dot(b, b)), w))

    def cosw():
        a, la = quad(R)
        b, lb = quad(R)
        s = dot(a, b)
        c = Fr(s, la * lb)
        return mcq("Berechne cos φ für den Winkel zwischen a = %s und b = %s." % (ve(a), ve(b)), fz(c),
                   [fz(Fr(s, la * la * lb * lb)) if s else "1", fz(Fr(s, la + lb)), fz(-c) if c else "1"],
                   "a · b = %s, |a| = %d, |b| = %d. cos φ = %s : %d = <b>%s</b>." % (z(s), la, lb, z(s), la * lb, fz(c)))

    def kreuz():
        a, b = V(R, -4, 4), V(R, -4, 4)
        c = cross(a, b)
        if not nonzero(c):
            return None
        return mcq("Berechne das Vektorprodukt a × b für a = %s und b = %s." % (ve(a), ve(b)), ve(c),
                   [ve(cross(b, a)), ve([x * y for x, y in zip(a, b)]), ve([c[0], -c[1], c[2]])],
                   "a × b = (a<sub>2</sub>b<sub>3</sub> − a<sub>3</sub>b<sub>2</sub>, a<sub>3</sub>b<sub>1</sub> − a<sub>1</sub>b<sub>3</sub>, a<sub>1</sub>b<sub>2</sub> − a<sub>2</sub>b<sub>1</sub>) = <b>%s</b>." % ve(c))

    def flaeche():
        a = [ri(R, -6, 6), ri(R, -6, 6), 0]
        b = [ri(R, -6, 6), ri(R, -6, 6), 0]
        A = abs(a[0] * b[1] - a[1] * b[0])
        if A == 0:
            return None
        kind = R.choice(["Parallelogramm", "Dreieck"])
        ans = Fr(A) if kind == "Parallelogramm" else Fr(A, 2)
        return mcq("Wie gross ist der Flächeninhalt des %s, das von a = %s und b = %s aufgespannt wird?" % ("Parallelogramms" if kind == "Parallelogramm" else "Dreiecks", ve(a), ve(b)),
                   z(ans), [z(Fr(A, 2) if kind == "Parallelogramm" else A), z(abs(dot(a, b))), z(A + 2)],
                   "a × b = %s, |a × b| = %d. %s: <b>%s</b>." % (ve(cross(a, b)), A, "Parallelogramm = |a × b|" if kind == "Parallelogramm" else "Dreieck = ½ · |a × b|", z(ans)))

    return dict(
        title="Skalarprodukt, Winkel und Vektorprodukt",
        short="Skalarprodukt und Winkel",
        meta="Skalarprodukt, senkrechte Vektoren, Winkel zwischen Vektoren, Vektorprodukt und Flächen von Parallelogramm und Dreieck. 100 Aufgaben mit Lösungen.",
        kb="a · b = 0 heisst: a und b stehen senkrecht.",
        ks="cos φ = a · b : (|a| · |b|)",
        think=["Das <b>Skalarprodukt</b> ist eine Zahl: a · b = a<sub>1</sub>b<sub>1</sub> + a<sub>2</sub>b<sub>2</sub> + a<sub>3</sub>b<sub>3</sub>.",
               "Zwei Vektoren (≠ 0) stehen genau dann <b>senkrecht</b>, wenn a · b = 0.",
               "Winkel: cos φ = a · b : (|a| · |b|).",
               "Das <b>Vektorprodukt</b> a × b ist ein Vektor, der auf a und b senkrecht steht. Sein Betrag ist der Flächeninhalt des Parallelogramms aus a und b."],
        ex=[("a = (1, 2, 2), b = (2, 1, −2)", ["a · b = 2 + 2 − 4"], "0, also senkrecht"),
            ("a = (1, 1, 0), b = (1, 0, 0): Winkel", ["a · b = 1, |a| = √2, |b| = 1", "cos φ = 1 : √2"], "45°")],
        mist=[["Beim Skalarprodukt einen Vektor als Ergebnis schreiben", "Das Skalarprodukt ist eine Zahl"],
              ["cos φ = a · b", "Durch das Produkt der Beträge teilen"],
              ["a × b = b × a", "Vertauschen dreht das Vorzeichen: b × a = −(a × b)"]],
        faq=[{"q": "Wofür braucht man das Skalarprodukt?", "a": "Um Winkel zu berechnen und um zu prüfen, ob zwei Vektoren senkrecht aufeinander stehen."},
             {"q": "Was ist der Unterschied zwischen Skalarprodukt und Vektorprodukt?", "a": "Das Skalarprodukt a · b ist eine Zahl. Das Vektorprodukt a × b ist ein Vektor, der senkrecht auf a und b steht."},
             {"q": "Wie berechne ich den Flächeninhalt eines Dreiecks mit Vektoren?", "a": "Halber Betrag des Vektorprodukts der zwei Seitenvektoren: A = ½ · |a × b|."},
             {"q": "Was bedeutet ein negatives Skalarprodukt?", "a": "Der Winkel zwischen den Vektoren ist grösser als 90°."}],
        sets=[("Skalarprodukt berechnen", [(sk, 20)]), ("Senkrechte Vektoren", [(orth, 10), (tsuch, 10)]),
              ("Winkel zwischen Vektoren", [(winkel, 12), (cosw, 8)]), ("Vektorprodukt", [(kreuz, 20)]), ("Flächen mit dem Vektorprodukt", [(flaeche, 20)])])


# ============================================================ Geraden und Ebenen
def gerade(Pv, dv, p="t"):
    return "x = %s + %s · %s" % (ve(Pv), p, ve(dv))


def ebene(n, d):
    return "%s = %s" % (poly({"x": n[0], "y": n[1], "z": n[2]}), z(d))


def raum(R):
    def param():
        A, B = V(R, -5, 5), V(R, -5, 5)
        d = add(B, A, -1)
        if not nonzero(d):
            return None
        good = gerade(A, d)
        return mcq("Welche Gleichung beschreibt die Gerade durch %s und %s?" % (P3("A", A), P3("B", B)), good,
                   [gerade(A, B), gerade(d, A), gerade(A, add(A, B))],
                   "Stützvektor A, Richtungsvektor <span class='vec'>AB</span> = B − A = %s: <b>%s</b>." % (ve(d), good))

    def punkt():
        A, d = V(R, -5, 5), [ri(R, -4, 4, (0,)) for _ in range(3)]
        t = ri(R, -3, 4, (0,))
        P = add(A, d, t)
        on = R.random() < 0.55
        if not on:
            P = list(P)
            P[R.randrange(3)] += R.choice([-2, -1, 1, 2])
        good = ("Ja, für t = %s." % z(t)) if on else "Nein."
        bad = ["Nein.", "Ja, für t = %s." % z(-t), "Ja, für t = %s." % z(t + 1)] if on else ["Ja, für t = %s." % z(t), "Ja, für t = %s." % z(-t), "Ja, für t = 0."]
        return mcq("Liegt %s auf der Geraden g: %s?" % (P3("P", P), gerade(A, d)), good, bad,
                   "Gleichungen A + t · d = P aufstellen. %s" % ("Alle drei liefern t = %s. <b>Ja</b>." % z(t) if on else "Die drei Gleichungen liefern verschiedene t. <b>Nein</b>."))

    def lage():
        k = R.choice(["parallel", "identisch", "schneidend", "windschief"])
        A, d = V(R, -4, 4), [ri(R, -3, 3, (0,)) for _ in range(3)]
        if k in ("parallel", "identisch"):
            f = R.choice([2, -1, 3, -2])
            e = [f * x for x in d]
            s = ri(R, -2, 3, (0,))
            B = add(A, d, s)
            if k == "parallel":
                B[R.randrange(3)] += R.choice([1, 2, -1])
        else:
            while True:
                e = [ri(R, -3, 3) for _ in range(3)]
                if nonzero(cross(d, e)):
                    break
            if k == "schneidend":
                t, s = ri(R, -2, 3), ri(R, -2, 3)
                S = add(A, d, t)
                B = add(S, e, -s)
            else:
                n = cross(d, e)
                B = add(A, n, R.choice([1, -1]))
        good = {"parallel": "parallel, aber nicht identisch", "identisch": "identisch", "schneidend": "Sie schneiden sich.", "windschief": "windschief"}[k]
        others = [x for x in ["parallel, aber nicht identisch", "identisch", "Sie schneiden sich.", "windschief"] if x != good]
        return mcq("Wie liegen g: %s und h: %s zueinander?" % (gerade(A, d), gerade(B, e, "s")), good, others,
                   "Richtungsvektoren %s Vielfache voneinander. %s" % ("sind" if k in ("parallel", "identisch") else "sind keine",
                    {"parallel": "Der Stützpunkt von h liegt nicht auf g: <b>parallel</b>.", "identisch": "Der Stützpunkt von h liegt auf g: <b>identisch</b>.",
                     "schneidend": "Das Gleichungssystem hat eine Lösung: <b>Sie schneiden sich</b>.", "windschief": "Das Gleichungssystem hat keine Lösung: <b>windschief</b>."}[k]))

    def koord():
        n = [ri(R, -4, 4) for _ in range(3)]
        if sum(1 for x in n if x) < 2:
            return None
        P = V(R, -4, 4)
        d = dot(n, P)
        good = ebene(n, d)
        return mcq("Die Ebene E geht durch %s und hat den Normalenvektor n = %s. Wie lautet ihre Koordinatengleichung?" % (P3("P", P), ve(n)), good,
                   [ebene(n, -d) if d else ebene(n, 1), ebene(P, dot(n, P)) if P != n and nonzero(P) else ebene(n, d + 2), ebene(n, sum(n))],
                   "n<sub>1</sub>x + n<sub>2</sub>y + n<sub>3</sub>z = n · P = %s: <b>%s</b>." % (z(d), good))

    def spur():
        n = [ri(R, 1, 6) * R.choice([1, -1]) for _ in range(3)]
        i = R.randrange(3)
        m = 1
        for x in n:
            m = m * abs(x) // math.gcd(m, abs(x))
        d = m * R.choice([1, 2, -1])
        ax = "xyz"[i]
        S = [0, 0, 0]
        S[i] = Fr(d, n[i])
        good = P3("S", S)
        W = [0, 0, 0]
        W[i] = Fr(-d, n[i])
        W2 = [0, 0, 0]
        W2[i] = d
        W3 = [0, 0, 0]
        W3[(i + 1) % 3] = Fr(d, n[i])
        return mcq("In welchem Punkt schneidet die Ebene E: %s die %s-Achse?" % (ebene(n, d), ax), good, [P3("S", W), P3("S", W2), P3("S", W3)],
                   "Auf der %s-Achse sind die anderen Koordinaten 0: %s · %s = %s ⇒ %s = %s. <b>%s</b>." % (ax, z(n[i]), ax, z(d), ax, z(S[i]), good))

    def schnitt():
        A, d = V(R, -5, 5), [ri(R, -3, 3) for _ in range(3)]
        n = [ri(R, -3, 3) for _ in range(3)]
        if dot(n, d) == 0 or not nonzero(n):
            return None
        t = ri(R, -3, 3)
        S = add(A, d, t)
        c = dot(n, S)
        good = P3("S", S)
        return mcq("Wo schneidet die Gerade g: %s die Ebene E: %s?" % (gerade(A, d), ebene(n, c)), good,
                   [P3("S", add(A, d, -t)), P3("S", add(A, d, t + 1)), P3("S", d)],
                   "Geradengleichung in E einsetzen: t = %s. In g einsetzen: <b>%s</b>." % (z(t), good))

    def abstand():
        n, l = quad(R)
        P = V(R, -5, 5)
        k = ri(R, 1, 4)
        c = dot(n, P) - k * l * R.choice([1, -1])
        return mcq("Wie weit ist %s von der Ebene E: %s entfernt?" % (P3("P", P), ebene(n, c)), z(k),
                   [z(k * l), z(abs(dot(n, P) - c) * l), z(abs(c))],
                   "Abstand = |n · P − d| : |n| = |%s − %s| : %d = <b>%s</b>." % (z(dot(n, P)), par(c), l, z(k)))

    return dict(
        title="Geraden und Ebenen im Raum",
        short="Geraden und Ebenen",
        meta="Geraden und Ebenen im Raum: Parametergleichung, Punktprobe, gegenseitige Lage zweier Geraden, Koordinatengleichung, Spurpunkte, Schnittpunkt und Abstand. 100 Aufgaben mit Lösungen.",
        kb="Gerade: Stützvektor + t · Richtungsvektor",
        ks="Ebene: n1x + n2y + n3z = d mit dem Normalenvektor n",
        think=["Eine <b>Gerade</b> im Raum: x = A + t · v (Stützvektor A, Richtungsvektor v).",
               "<b>Punktprobe</b>: Für einen Punkt auf der Geraden liefern alle drei Komponentengleichungen dasselbe t.",
               "Zwei Geraden sind identisch, parallel, schneidend oder <b>windschief</b> (nicht parallel und ohne Schnittpunkt).",
               "Eine <b>Ebene</b> mit Normalenvektor n durch P: n<sub>1</sub>x + n<sub>2</sub>y + n<sub>3</sub>z = n · P.",
               "Abstand von P zur Ebene n · x = d: |n · P − d| : |n|."],
        ex=[("Gerade durch A(1 | 0 | 2) und B(3 | 1 | 0)", ["Richtung B − A = (2, 1, −2)"], "x = (1, 0, 2) + t · (2, 1, −2)"),
            ("E: x + 2y + 2z = 9, Spurpunkt auf der x-Achse", ["y = z = 0", "x = 9"], "S(9 | 0 | 0)")],
        mist=[["Als Richtung den Ortsvektor von B nehmen", "Richtung ist B − A"],
              ["Nicht parallel ⇒ sie schneiden sich", "Im Raum gibt es auch windschiefe Geraden"],
              ["Abstand = |n · P − d|", "Noch durch |n| teilen"]],
        faq=[{"q": "Was heisst windschief?", "a": "Zwei Geraden im Raum sind windschief, wenn sie nicht parallel sind und sich auch nicht schneiden."},
             {"q": "Wie finde ich die Koordinatengleichung einer Ebene?", "a": "Mit dem Normalenvektor n und einem Punkt P: n1x + n2y + n3z = n · P. Den Normalenvektor erhält man zum Beispiel als Vektorprodukt zweier Richtungsvektoren."},
             {"q": "Wie berechne ich den Schnittpunkt von Gerade und Ebene?", "a": "Die Komponenten der Geradengleichung in die Ebenengleichung einsetzen, t berechnen und in die Gerade einsetzen."},
             {"q": "Was sind Spurpunkte?", "a": "Die Schnittpunkte einer Ebene mit den Koordinatenachsen."}],
        sets=[("Geradengleichungen und Punktprobe", [(param, 10), (punkt, 10)]), ("Lage zweier Geraden", [(lage, 20)]),
              ("Koordinatengleichung und Spurpunkte", [(koord, 10), (spur, 10)]), ("Schnitt von Gerade und Ebene", [(schnitt, 20)]),
              ("Abstand Punkt–Ebene", [(abstand, 20)])])


# ============================================================ Kombinatorik
def C_(n, k):
    return math.comb(n, k)


def P_(n, k):
    return math.perm(n, k)


WORDS = ["ANANAS", "KAKAO", "BANANE", "TOMATE", "KOKOS", "LAMA", "PAPAGEI", "ZUCCHINI", "MATHEMATIK", "SALAT", "BASEL", "THUN", "ROSSO", "TESSIN", "AARAU",
         "OTTO", "ANNA", "RAPPEN", "FRANKEN", "LUZERN", "BERN", "MINIMUM", "STATISTIK", "ALPEN"]


def kombi(R):
    def reihe():
        n = R.randint(3, 9)
        nm = R.choice(["Personen stellen sich in eine Reihe", "Bücher werden nebeneinander ins Regal gestellt", "Läuferinnen laufen ins Ziel (ohne Gleichstand)",
                       "Kinder setzen sich auf %d Stühle", "Buchstaben werden in eine Reihe gelegt"])
        if "%d" in nm:
            nm = nm % n
        return mcq("%d %s. Wie viele Reihenfolgen gibt es?" % (n, nm), z(math.factorial(n)), [z(n * n), z(n * (n - 1)), z(math.factorial(n - 1))],
                   "%d · %d · … · 1 = %d! = <b>%s</b>." % (n, n - 1, n, z(math.factorial(n))))

    def code():
        b, k = R.choice([(10, 3), (10, 4), (10, 5), (10, 6), (2, 8), (2, 10), (26, 2), (26, 3), (6, 3), (6, 4), (4, 5), (3, 6)])
        what = {10: "Ziffern 0 bis 9", 2: "Zeichen 0 und 1", 26: "26 Buchstaben", 6: "Augenzahlen eines Würfels", 4: "4 Farben", 3: "3 Farben"}[b]
        ctx = ["Wie viele %d-stellige Codes kann man aus den %s bilden (Wiederholungen erlaubt)?",
               "Ein Passwort hat %d Zeichen aus den %s (Wiederholungen erlaubt). Wie viele Passwörter gibt es?"]
        if b == 10:
            ctx.append("Ein Zahlenschloss hat %d Rädchen mit den %s. Wie viele Einstellungen gibt es?")
        if b in (3, 4):
            ctx.append("Eine Reihe von %d Feldern wird mit %s angemalt, jedes Feld mit einer Farbe. Wie viele Muster gibt es?")
        ctx = R.choice(ctx)
        return mcq(ctx % (k, what), z(b ** k),
                   [z(b * k), z(k ** b), z(P_(b, k)) if k <= b else z(b ** (k - 1))],
                   "Für jede der %d Stellen gibt es %d Möglichkeiten: %d<sup>%d</sup> = <b>%s</b>." % (k, b, b, k, z(b ** k)))

    def podest():
        n, k = R.randint(6, 15), R.choice([2, 3, 3, 4])
        what = {2: "einen Präsidenten und eine Kassierin", 3: "Gold, Silber und Bronze", 4: "die ersten vier Plätze"}[k]
        return mcq("%d Personen nehmen teil. Wie viele Möglichkeiten gibt es für %s?" % (n, what), z(P_(n, k)), [z(C_(n, k)), z(n ** k), z(n * k)],
                   "Reihenfolge wichtig, ohne Wiederholung: %s = <b>%s</b>." % (" · ".join(str(n - i) for i in range(k)), z(P_(n, k))))

    def auswahl():
        n, k = R.randint(5, 20), R.randint(2, 5)
        if k >= n:
            return None
        ctx = R.choice(["Aus %d Schülerinnen und Schülern wird eine Gruppe von %d gewählt.", "Aus %d Sorten Glace wählst du %d verschiedene.",
                        "Beim Lotto werden %d Zahlen angeboten und %d angekreuzt.", "Aus %d Spielern bildet der Trainer ein Team von %d."])
        return mcq(ctx % (n, k) + " Wie viele Möglichkeiten gibt es?", z(C_(n, k)), [z(P_(n, k)), z(n ** k), z(C_(n, k - 1))],
                   "Reihenfolge egal: „%d über %d“ = %d! : (%d! · %d!) = <b>%s</b>." % (n, k, n, k, n - k, z(C_(n, k))))

    def haende():
        n = R.randint(4, 30)
        t = R.choice(["Hand", "Spiel"])
        q = ("%d Personen geben sich alle gegenseitig die Hand. Wie viele Händedrücke sind es?" % n) if t == "Hand" else \
            ("In einer Gruppe spielen %d Mannschaften jede gegen jede einmal. Wie viele Spiele gibt es?" % n)
        return mcq(q, z(C_(n, 2)), [z(n * (n - 1)), z(n * n), z(C_(n, 2) + n)],
                   "Jedes Paar zählt einmal: „%d über 2“ = %d · %d : 2 = <b>%s</b>." % (n, n, n - 1, z(C_(n, 2))))

    def wort():
        w = R.choice(WORDS)
        from collections import Counter
        c = Counter(w)
        v = math.factorial(len(w))
        for x in c.values():
            v //= math.factorial(x)
        if v == math.factorial(len(w)):
            bad = [z(len(w) ** len(w)), z(math.factorial(len(w) - 1)), z(len(w) * (len(w) - 1))]
        else:
            bad = [z(math.factorial(len(w))), z(v // 2) if v % 2 == 0 else z(v * 2), z(math.factorial(len(w) - 1))]
        rep = ", ".join("%s %d-mal" % (k, x) for k, x in sorted(c.items()) if x > 1)
        return mcq("Wie viele verschiedene Wörter (auch sinnlose) entstehen, wenn man die Buchstaben von %s vertauscht?" % w, z(v), bad,
                   "%d Buchstaben: %d!%s = <b>%s</b>." % (len(w), len(w), (" : (gleiche Buchstaben: " + rep + ")") if rep else "", z(v)))

    def menu():
        a, b, c = R.randint(2, 6), R.randint(2, 8), R.randint(2, 5)
        return mcq("Ein Restaurant bietet %d Vorspeisen, %d Hauptgänge und %d Desserts an. Wie viele verschiedene Menüs aus je einem Gang gibt es?" % (a, b, c),
                   z(a * b * c), [z(a + b + c), z(a * b + c), z((a + b + c) ** 2)], "Produktregel: %d · %d · %d = <b>%s</b>." % (a, b, c, z(a * b * c)))

    def koeff():
        n, k = R.randint(5, 15), R.randint(2, 6)
        if k >= n:
            return None
        return mcq("Berechne den Binomialkoeffizienten „%d über %d“." % (n, k), z(C_(n, k)), [z(P_(n, k)), z(C_(n, k - 1)), z(Fr(n, k)) if n % k == 0 else z(n * k)],
                   "„%d über %d“ = %s : %d! = <b>%s</b>." % (n, k, " · ".join(str(n - i) for i in range(k)), k, z(C_(n, k))))

    return dict(
        title="Kombinatorik: Permutationen, Variationen und Kombinationen",
        short="Kombinatorik",
        meta="Kombinatorik am Gymnasium: Produktregel, Fakultät, Codes mit Wiederholung, Reihenfolgen, Auswahlen mit dem Binomialkoeffizienten und Anagramme. 100 Aufgaben mit Lösungen.",
        kb="Zuerst fragen: Ist die Reihenfolge wichtig? Gibt es Wiederholungen?",
        ks="n! Reihenfolgen, n hoch k Codes, n über k Auswahlen",
        think=["<b>Produktregel</b>: Bei mehreren Entscheidungen nacheinander die Anzahlen multiplizieren.",
               "n Dinge in eine Reihe: n! = n · (n − 1) · … · 1 Möglichkeiten.",
               "k Stellen aus n Zeichen <b>mit</b> Wiederholung: n<sup>k</sup>.",
               "k aus n <b>mit</b> Reihenfolge, ohne Wiederholung: n · (n − 1) · … (k Faktoren).",
               "k aus n <b>ohne</b> Reihenfolge: Binomialkoeffizient „n über k“ = n! : (k! · (n − k)!)."],
        ex=[("4-stellige Codes aus 0–9", ["10 · 10 · 10 · 10"], "10 000"),
            ("3 aus 10 auswählen", ["10 · 9 · 8 : 3!"], "120")],
        mist=[["Bei einer Auswahl ohne Reihenfolge 10 · 9 · 8 rechnen", "Noch durch 3! teilen, weil die Reihenfolge egal ist"],
              ["Codes: 10 · 4", "Jede Stelle hat 10 Möglichkeiten: 10⁴"],
              ["Bei ANANAS 6! Wörter", "Gleiche Buchstaben vertauschen gibt kein neues Wort: 6! : (3! · 2!)"]],
        faq=[{"q": "Was ist der Unterschied zwischen Permutation und Kombination?", "a": "Bei einer Permutation (Anordnung) ist die Reihenfolge wichtig, bei einer Kombination (Auswahl) nicht."},
             {"q": "Was bedeutet n!?", "a": "n Fakultät ist das Produkt 1 · 2 · … · n. Es ist die Anzahl Reihenfolgen von n verschiedenen Dingen."},
             {"q": "Wie berechne ich „n über k“?", "a": "n! : (k! · (n − k)!). Zum Beispiel „5 über 2“ = 120 : (2 · 6) = 10."},
             {"q": "Wie viele Möglichkeiten gibt es beim Schweizer Lotto 6 aus 42?", "a": "„42 über 6“ = 5 245 786."}],
        sets=[("Produktregel und Reihenfolgen", [(menu, 8), (reihe, 12)]), ("Codes mit Wiederholung", [(code, 20)]),
              ("Reihenfolge wichtig", [(podest, 12), (wort, 8)]), ("Auswahlen ohne Reihenfolge", [(auswahl, 12), (koeff, 8)]),
              ("Sachaufgaben", [(haende, 10), (wort, 10)])])


# ============================================================ bedingte Wahrscheinlichkeit
def pc(v, k=1):
    """Fraction → Prozent mit k Nachkommastellen (deutsch, Komma)"""
    x = Fr(v) * 100
    f = 10 ** k
    r = int(x * f + Fr(1, 2))
    s = "%d,%0*d" % (r // f, k, r % f) if k else "%d" % r
    return s + NB + "%"


def dec(v):
    v = Fr(v)
    from de_k6 import dz, endlich
    return dz(v) if endlich(v) else bh(v)


from de_k6 import bh  # noqa: E402


def bedingt(R):
    def ziehen():
        r, b = R.randint(2, 8), R.randint(2, 8)
        n = r + b
        ohne = Fr(r, n) * Fr(r - 1, n - 1)
        mit = Fr(r, n) ** 2
        return mcq("Eine Urne enthält %d rote und %d blaue Kugeln. Du ziehst zwei Kugeln ohne Zurücklegen. Wie gross ist P(beide rot)?" % (r, b), fz(ohne),
                   [fz(mit), fz(Fr(r, n) + Fr(r - 1, n - 1)) if Fr(r, n) + Fr(r - 1, n - 1) < 1 else fz(Fr(r - 1, n)), fz(Fr(r, n) * Fr(r - 1, n))],
                   "Pfadregel: %s · %s = <b>%s</b>." % (fz(Fr(r, n)), fz(Fr(r - 1, n - 1)), fz(ohne)))

    def zwei_farben():
        r, b = R.randint(2, 8), R.randint(2, 8)
        n = r + b
        p = Fr(r, n) * Fr(b, n - 1) * 2
        return mcq("Eine Urne enthält %d rote und %d blaue Kugeln. Du ziehst zwei Kugeln ohne Zurücklegen. Wie gross ist P(verschiedene Farben)?" % (r, b), fz(p),
                   [fz(p / 2), fz(Fr(2 * r * b, n * n)), fz(1 - p / 2)],
                   "Zwei Pfade: rot–blau und blau–rot. 2 · %s · %s = <b>%s</b>." % (fz(Fr(r, n)), fz(Fr(b, n - 1)), fz(p)))

    def cond():
        pa = Fr(R.choice([20, 25, 30, 40, 50, 60, 75, 80]), 100)
        q = Fr(R.choice([10, 20, 25, 40, 50, 60, 75, 80]), 100)
        pab = pa * q
        return mcq("Es gilt P(A) = %s und P(A ∩ B) = %s. Berechne P(B | A)." % (dec(pa), dec(pab)), dec(q),
                   [dec(pab * pa), dec(pab), dec(pa - pab)],
                   "P(B | A) = P(A ∩ B) : P(A) = %s : %s = <b>%s</b>." % (dec(pab), dec(pa), dec(q)))

    CTX = [("Eine Krankheit tritt bei %s der Bevölkerung auf. Ein Test ist bei Kranken mit einer Wahrscheinlichkeit von %s positiv, bei Gesunden mit %s.", "positiv"),
           ("An %s der Schultage regnet es. Bei Regen ist der Bus mit einer Wahrscheinlichkeit von %s verspätet, sonst mit %s.", "Verspätung"),
           ("%s der Bauteile stammen von Maschine A. Von den Bauteilen aus A sind %s defekt, von den übrigen %s.", "defekt")]

    def setup():
        i = R.randrange(3)
        if i == 0:
            a, b1, b2 = R.choice([1, 2, 5, 10, 20]), R.choice([80, 90, 95, 98, 99]), R.choice([2, 5, 10, 20])
        elif i == 1:
            a, b1, b2 = R.choice([10, 20, 25, 30, 40]), R.choice([30, 40, 50, 60, 70]), R.choice([5, 10, 15, 20])
        else:
            a, b1, b2 = R.choice([20, 30, 40, 50, 60]), R.choice([2, 3, 4, 5, 8, 10]), R.choice([1, 2, 3, 4, 5])
        return Fr(a, 100), Fr(b1, 100), Fr(b2, 100), i

    def total():
        a, b1, b2, i = setup()
        t, w = CTX[i]
        PB = a * b1 + (1 - a) * b2
        txt = t % (pc(a, 0), pc(b1, 0), pc(b2, 0))
        q = {"positiv": "Mit welcher Wahrscheinlichkeit ist ein Test positiv?", "Verspätung": "Mit welcher Wahrscheinlichkeit hat der Bus Verspätung?",
             "defekt": "Mit welcher Wahrscheinlichkeit ist ein Bauteil defekt?"}[w]
        return mcq(txt + " " + q, pc(PB), [pc(a * b1), pc(b1 + b2) if b1 + b2 < 1 else pc(b1 * b2), pc((b1 + b2) / 2)],
                   "Totale Wahrscheinlichkeit: %s · %s + %s · %s = <b>%s</b>." % (dec(a), dec(b1), dec(1 - a), dec(b2), pc(PB)))

    def bayes():
        a, b1, b2, i = setup()
        t, w = CTX[i]
        PB = a * b1 + (1 - a) * b2
        PA = a * b1 / PB
        txt = t % (pc(a, 0), pc(b1, 0), pc(b2, 0))
        q = {"positiv": "Ein Test ist positiv. Mit welcher Wahrscheinlichkeit ist die Person krank?", "Verspätung": "Der Bus hat Verspätung. Mit welcher Wahrscheinlichkeit regnet es?",
             "defekt": "Ein Bauteil ist defekt. Mit welcher Wahrscheinlichkeit stammt es von Maschine A?"}[w]
        return mcq(txt + " " + q, "≈ " + pc(PA), ["≈ " + pc(b1), "≈ " + pc(a * b1), "≈ " + pc(PB)],
                   "Bayes: P = %s · %s : %s = %s : %s ≈ <b>%s</b>." % (dec(a), dec(b1), dec(PB), dec(a * b1), dec(PB), pc(PA)))

    def unab():
        pa = Fr(R.choice([2, 3, 4, 5, 6]), 10)
        pb = Fr(R.choice([2, 3, 4, 5, 7]), 10)
        if R.random() < 0.5:
            pab = pa * pb
        else:
            pab = pa * pb + Fr(R.choice([-1, 1, 2]), 100)
        yes = pab == pa * pb
        good = "Ja, denn P(A) · P(B) = P(A ∩ B)." if yes else "Nein, denn P(A) · P(B) = %s ≠ P(A ∩ B)." % dec(pa * pb)
        bad = ["Nein, denn P(A) · P(B) = %s ≠ P(A ∩ B)." % dec(pa * pb + Fr(1, 100)), "Ja, denn P(A) + P(B) ≤ 1.", "Nein, denn P(A) ≠ P(B)."] if yes else \
              ["Ja, denn P(A) · P(B) = P(A ∩ B).", "Ja, denn P(A) + P(B) ≤ 1.", "Nein, denn P(A) ≠ P(B)."]
        return mcq("Es gilt P(A) = %s, P(B) = %s und P(A ∩ B) = %s. Sind A und B unabhängig?" % (dec(pa), dec(pb), dec(pab)), good, bad,
                   "Unabhängig heisst P(A ∩ B) = P(A) · P(B). Hier ist P(A) · P(B) = %s. %s" % (dec(pa * pb), good))

    return dict(
        title="Bedingte Wahrscheinlichkeit und Satz von Bayes",
        short="Bedingte Wahrscheinlichkeit",
        meta="Bedingte Wahrscheinlichkeit am Gymnasium: Ziehen ohne Zurücklegen, P(B | A), totale Wahrscheinlichkeit, Satz von Bayes und unabhängige Ereignisse. 100 Aufgaben mit Lösungen.",
        kb="P(B | A) = P(A ∩ B) : P(A)",
        ks="Im Baumdiagramm: entlang eines Pfades multiplizieren, Pfade addieren",
        think=["P(B | A) ist die Wahrscheinlichkeit von B, wenn man schon weiss, dass A eingetreten ist: P(B | A) = P(A ∩ B) : P(A).",
               "Im <b>Baumdiagramm</b> multipliziert man entlang eines Pfades (Pfadregel) und addiert die Pfade (Summenregel).",
               "<b>Totale Wahrscheinlichkeit</b>: P(B) = P(A) · P(B | A) + P(Ā) · P(B | Ā).",
               "<b>Satz von Bayes</b>: P(A | B) = P(A) · P(B | A) : P(B).",
               "A und B sind <b>unabhängig</b>, wenn P(A ∩ B) = P(A) · P(B)."],
        ex=[("Krankheit 10 %, Test bei Kranken 90 % positiv, bei Gesunden 20 %", ["P(positiv) = 0,1 · 0,9 + 0,9 · 0,2 = 0,27", "P(krank | positiv) = 0,09 : 0,27"], "≈ 33,3 %"),
            ("3 rote, 2 blaue Kugeln, zwei ohne Zurücklegen", ["P(rot, rot) = 3/5 · 2/4"], "3/10")],
        mist=[["P(B | A) = P(A) · P(A ∩ B)", "Durch P(A) teilen"],
              ["Beim zweiten Zug ohne Zurücklegen wieder durch n teilen", "Es sind nur noch n − 1 Kugeln"],
              ["P(krank | positiv) = P(positiv | krank)", "Die Bedingung umdrehen ändert die Wahrscheinlichkeit: Bayes verwenden"]],
        faq=[{"q": "Was bedeutet P(B | A)?", "a": "Die Wahrscheinlichkeit für B unter der Bedingung, dass A eingetreten ist."},
             {"q": "Wann brauche ich den Satz von Bayes?", "a": "Wenn man P(B | A) kennt, aber P(A | B) sucht, zum Beispiel: Wie wahrscheinlich ist man krank, wenn der Test positiv ist?"},
             {"q": "Wann sind zwei Ereignisse unabhängig?", "a": "Wenn P(A ∩ B) = P(A) · P(B). Dann ändert das Wissen über A die Wahrscheinlichkeit von B nicht."},
             {"q": "Warum ist ein positiver Test oft nicht sicher?", "a": "Wenn eine Krankheit selten ist, sind viele positive Tests falsch-positiv. Der Satz von Bayes zeigt, wie gross dieser Anteil ist."}],
        sets=[("Ziehen ohne Zurücklegen", [(ziehen, 12), (zwei_farben, 8)]), ("Bedingte Wahrscheinlichkeit", [(cond, 20)]),
              ("Totale Wahrscheinlichkeit", [(total, 20)]), ("Satz von Bayes", [(bayes, 20)]), ("Unabhängige Ereignisse", [(unab, 20)])])


# ============================================================ Binomialverteilung
def r4(x):
    r = int(x * 10000 + 0.5)
    return "%d,%04d" % (r // 10000, r % 10000)


def binom(R):
    PS = [(Fr(1, 2), "eine Münze", "Kopf"), (Fr(1, 6), "ein Würfel", "eine Sechs"), (Fr(1, 3), "ein Glücksrad mit drei gleich grossen Feldern", "Rot"),
          (Fr(1, 4), "ein Glücksrad mit vier gleich grossen Feldern", "Gelb"), (Fr(1, 5), "ein Glücksrad mit fünf gleich grossen Feldern", "Blau"),
          (Fr(1, 10), "ein Glücksrad mit zehn gleich grossen Feldern", "die Zahl 7")]
    VB = lambda w: "gedreht" if "Glücksrad" in w else "geworfen"

    def exakt():
        p, w, e = R.choice(PS)
        n = R.randint(3, 6) if p != Fr(1, 2) else R.randint(3, 8)
        k = R.randint(1, n - 1)
        v = C_(n, k) * p ** k * (1 - p) ** (n - k)
        return mcq("%s wird %d-mal %s. Wie gross ist die Wahrscheinlichkeit für genau %d-mal %s?" % (w[0].upper() + w[1:], n, VB(w), k, e), fz(v),
                   [fz(p ** k * (1 - p) ** (n - k)), fz(C_(n, k) * p ** k), fz(p ** k)],
                   "P(X = %d) = „%d über %d“ · %s<sup>%d</sup> · %s<sup>%d</sup> = <b>%s</b>." % (k, n, k, fz(p), k, fz(1 - p), n - k, fz(v)))

    def dezimal():
        p = Fr(R.choice([1, 2, 3, 4, 6, 7, 8, 9]), 10)
        n, k = R.randint(4, 10), None
        k = R.randint(0, n)
        v = C_(n, k) * p ** k * (1 - p) ** (n - k)
        if v < Fr(1, 1000):
            return None
        return mcq("X ist binomialverteilt mit n = %d und p = %s. Berechne P(X = %d) auf vier Stellen." % (n, z(p), k), r4(v),
                   [r4(p ** k * (1 - p) ** (n - k)), r4(min(Fr(C_(n, k)) * p ** k, Fr(9999, 10000))), r4(C_(n, k) * p ** (n - k) * (1 - p) ** k) if p != Fr(1, 2) else r4(v / 2)],
                   "„%d über %d“ · %s<sup>%d</sup> · %s<sup>%d</sup> ≈ <b>%s</b>." % (n, k, z(p), k, z(1 - p), n - k, r4(v)))

    def erw():
        n = R.choice([10, 20, 25, 30, 40, 50, 60, 80, 100, 120, 150, 200, 300, 500])
        p = Fr(R.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), 10) if R.random() < 0.7 else R.choice([Fr(1, 6), Fr(1, 4), Fr(1, 2), Fr(1, 5)])
        E = n * p
        Vr = n * p * (1 - p)
        what = R.choice(["E", "V"])
        if what == "E":
            return mcq("X ist binomialverteilt mit n = %d und p = %s. Wie gross ist der Erwartungswert E(X)?" % (n, fz(p)), z(E), [z(Vr), z(n * (1 - p)), z(n + p) if (n + p).denominator <= 20 else z(E + 1)],
                       "E(X) = n · p = %d · %s = <b>%s</b>." % (n, fz(p), z(E)))
        return mcq("X ist binomialverteilt mit n = %d und p = %s. Wie gross ist die Varianz V(X)?" % (n, fz(p)), z(Vr), [z(E), z(n * p * p), z(Vr + 1)],
                   "V(X) = n · p · (1 − p) = %d · %s · %s = <b>%s</b>." % (n, fz(p), fz(1 - p), z(Vr)))

    def mind():
        p, w, e = R.choice(PS)
        n = R.randint(2, 7 if p.denominator <= 4 else 4)
        v = 1 - (1 - p) ** n
        return mcq("%s wird %d-mal %s. Wie gross ist die Wahrscheinlichkeit für mindestens einmal %s?" % (w[0].upper() + w[1:], n, VB(w), e), fz(v),
                   [fz((1 - p) ** n), fz(min(n * p, Fr(99, 100))), fz(1 - p ** n)],
                   "Gegenereignis „nie“: P(X ≥ 1) = 1 − %s<sup>%d</sup> = <b>%s</b>." % (fz(1 - p), n, fz(v)))

    def param():
        t = R.choice(["wuerfel", "muenze", "umfrage", "lose"])
        if t == "wuerfel":
            n = R.randint(5, 30)
            q, ans = "Ein Würfel wird %d-mal geworfen. X zählt die Sechsen." % n, (n, Fr(1, 6))
        elif t == "muenze":
            n = R.randint(5, 30)
            q, ans = "Eine Münze wird %d-mal geworfen. X zählt, wie oft Zahl fällt." % n, (n, Fr(1, 2))
        elif t == "umfrage":
            n, p = R.choice([20, 30, 40, 50, 80, 100]), Fr(R.choice([15, 20, 25, 30, 35, 40, 60, 70]), 100)
            q, ans = "%s der Jugendlichen fahren mit dem Velo zur Schule. Man befragt %d zufällig ausgewählte Jugendliche. X zählt die Velofahrer." % (pc(p, 0), n), (n, p)
        else:
            n, p = R.choice([5, 8, 10, 12, 15]), Fr(R.choice([5, 10, 20, 25]), 100)
            q, ans = "Bei einer Lotterie gewinnt jedes Los mit %s. Du kaufst %d Lose. X zählt die Gewinne." % (pc(p, 0), n), (n, p)
        n, p = ans
        f = lambda a, b: "n = %d, p = %s" % (a, dec(b))
        return mcq(q + " Welche Parameter hat die Binomialverteilung von X?", f(n, p), [f(n, 1 - p), "n = %d, p = %s" % (n * 2, dec(p)) if t != "muenze" else f(n + 1, p), "n = %s, p = %d" % (dec(p), n)],
                   "n = Anzahl Wiederholungen, p = Trefferwahrscheinlichkeit: <b>%s</b>." % f(n, p))

    return dict(
        title="Bernoulli-Ketten und Binomialverteilung",
        short="Binomialverteilung",
        meta="Binomialverteilung am Gymnasium: Parameter n und p, P(X = k) mit der Formel von Bernoulli, mindestens einmal, Erwartungswert und Varianz. 100 Aufgaben mit Lösungen.",
        kb="P(X = k) = (n über k) · p^k · (1 − p)^(n − k)",
        ks="Erwartungswert E(X) = n · p, Varianz V(X) = n · p · (1 − p)",
        think=["Eine <b>Bernoulli-Kette</b>: Ein Versuch mit Treffer oder Niete wird n-mal unabhängig wiederholt, die Trefferwahrscheinlichkeit p bleibt gleich.",
               "X = Anzahl Treffer ist <b>binomialverteilt</b>: P(X = k) = „n über k“ · p<sup>k</sup> · (1 − p)<sup>n − k</sup>.",
               "„n über k“ zählt, an welchen Stellen die k Treffer liegen können.",
               "Mindestens ein Treffer: P(X ≥ 1) = 1 − (1 − p)<sup>n</sup>.",
               "E(X) = n · p und V(X) = n · p · (1 − p)."],
        ex=[("Münze 4-mal, genau 2-mal Kopf", ["„4 über 2“ = 6", "6 · (½)² · (½)²"], "6/16 = 3/8"),
            ("Würfel 3-mal, mindestens eine Sechs", ["1 − (5/6)³"], "91/216")],
        mist=[["P(X = 2) = p² · (1 − p)ⁿ⁻² ohne „n über k“", "Mit der Anzahl Anordnungen multiplizieren"],
              ["Mindestens einmal = n · p", "Über das Gegenereignis rechnen: 1 − (1 − p)ⁿ"],
              ["Ziehen ohne Zurücklegen als Binomialverteilung", "Dann ändert sich p von Zug zu Zug: keine Bernoulli-Kette"]],
        faq=[{"q": "Wann ist X binomialverteilt?", "a": "Wenn ein Versuch mit zwei Ausgängen n-mal unabhängig wiederholt wird, p immer gleich bleibt und X die Treffer zählt."},
             {"q": "Was bedeutet der Erwartungswert n · p?", "a": "So viele Treffer erwartet man im Durchschnitt, wenn man das Experiment sehr oft durchführt."},
             {"q": "Wie berechne ich P(mindestens einmal)?", "a": "Mit dem Gegenereignis: 1 − P(nie) = 1 − (1 − p) hoch n."},
             {"q": "Was ist die Standardabweichung?", "a": "Die Wurzel aus der Varianz: σ = √(n · p · (1 − p))."}],
        sets=[("Parameter n und p", [(param, 20)]), ("Genau k Treffer", [(exakt, 20)]), ("Mit dem Taschenrechner", [(dezimal, 20)]),
              ("Mindestens ein Treffer", [(mind, 20)]), ("Erwartungswert und Varianz", [(erw, 20)])])
